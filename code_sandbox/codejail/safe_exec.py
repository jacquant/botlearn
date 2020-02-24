"""Safe execution of untrusted Python code."""

from __future__ import absolute_import

import inspect
import logging
import os.path
import shutil
import sys
import textwrap

try:
    import simplejson as json
except ImportError:
    import json

from codejail import jail_code
from codejail.util import temp_directory, change_directory

log = logging.getLogger("codejail")


# Flags to let developers temporarily change some behavior in this file.

# Set this to True to log all the code and globals being executed.
LOG_ALL_CODE = False
# Set this to True to use the unsafe code, so that you can debug it.
ALWAYS_BE_UNSAFE = False


class SafeExecException(Exception):
    """
    Python code running in the sandbox has failed.

    The message will be the stdout of the sandboxed process, which will usually
    contain the original exception message.

    """

    pass


def safe_exec(
    code, globals_dict, files=None, python_path=None, slug=None, extra_files=None
):
    """
    Execute code as "exec" does, but safely.

    `code` is a string of Python code.  `globals_dict` is used as the globals
    during execution.  Modifications the code makes to `globals_dict` are
    reflected in the dictionary on return.

    `files` is a list of file paths, either files or directories.  They will be
    copied into the temp directory used for execution.  No attempt is made to
    determine whether the file is appropriate or safe to copy.  The caller must
    determine which files to provide to the code.

    `python_path` is a list of directory or file paths.  These names will be
    added to `sys.path` so that modules they contain can be imported.  Only
    directories and zip files are supported.  If the name is not provided in
    `extras_files`, it will be copied just as if it had been listed in `files`.

    `slug` is an arbitrary string, a description that's meaningful to the
    caller, that will be used in log messages.

    `extra_files` is a list of pairs, each pair is a filename and a bytestring
    of contents to write into that file.  These files will be created in the
    temp directory and cleaned up automatically.  No subdirectories are
    supported in the filename.

    Returns None.  Changes made by `code` are visible in `globals_dict`.  If
    the code raises an exception, this function will raise `SafeExecException`
    with the stderr of the sandbox process, which usually includes the original
    exception message and traceback.

    """
    the_code = []

    files = list(files or ())
    extra_files = extra_files or ()
    python_path = python_path or ()

    extra_names = set(name for name, contents in extra_files)

    the_code.append(
        textwrap.dedent(
            """
        import sys
        # import six
        try:
            import simplejson as json
        except ImportError:
            import json
        """
            # We need to prevent the sandboxed code from printing to stdout,
            # or it will pollute the json we print there.  This isn't a
            # security concern (they can put any values in the json output
            # anyway, either by writing to sys.__stdout__, or just by defining
            # global values), but keeps accidents from happening.
            """
        class DevNull(object):
            def write(self, *args, **kwargs):
                pass

            def flush(self, *args, **kwargs):
                pass
        sys.stdout = DevNull()
        """
            # Read the code and the globals from the stdin.
            """
        code, g_dict = json.load(sys.stdin)
        """
        )
    )

    for pydir in python_path:
        pybase = os.path.basename(pydir)
        the_code.append("sys.path.append(%r)\n" % pybase)
        if pybase not in extra_names:
            files.append(pydir)

    the_code.append(
        textwrap.dedent(
            # Execute the sandboxed code.
            """
        exec(code, g_dict)
        """
        )
    )

    the_code.append(inspect.getsource(json_safe))

    the_code.append(
        textwrap.dedent(
            """
        g_dict = json_safe(g_dict)
        """
            # Write the globals back to the calling process.
            """
        json.dump(g_dict, sys.__stdout__)
        """
        )
    )

    stdin = json.dumps([code, json_safe(globals_dict)])
    jailed_code = "".join(the_code)

    # Turn this on to see what's being executed.
    if LOG_ALL_CODE:  # pragma: no cover
        log.debug("Jailed code: %s", jailed_code)
        log.debug("Exec: %s", code)
        log.debug("Stdin: %s", stdin)

    res = jail_code.jail_code(
        "python",
        code=jailed_code,
        stdin=stdin,
        files=files,
        slug=slug,
        extra_files=extra_files,
    )
    if LOG_ALL_CODE:
        log.debug("Status: %s", res.status)
        log.debug("Stdout: %s", res.stdout)
        log.debug("Stderr: %s", res.stderr)

    if res.status != 0:
        raise SafeExecException(
            (
                "Couldn't execute jailed code: stdout: {res.stdout!r}, "
                "stderr: {res.stderr!r} with status code: {res.status}"
            ).format(res=res)
        )
    globals_dict.update(json.loads(res.stdout.decode("utf-8")))


def json_safe(d):
    """
    Return only the JSON-safe part of d(a python dict object).

    Used to emulate reading data through a serialization straw.

    """

    # six.binary_type is here because bytes are sometimes ok if they represent valid utf8
    # so we consider them valid for now and try to decode them with decode_object.  If that
    # doesn't work they'll get dropped later in the process.
    ok_types = (type(None), int, float, bytes, str, list, tuple, dict)

    def decode_object(obj):
        """
        Convert an object to a JSON serializable form by decoding all byte strings.

        In particular if we find any byte strings try to convert them to
        utf-8 strings.  If we run into byte strings that can't be decoded as utf8 strings
        throw an exception.

        For other non-serializable objects we return them as is.

        raises: Exception
        """
        if isinstance(obj, bytes):
            return obj.decode("utf-8")
        elif isinstance(obj, (list, tuple)):
            new_list = []
            for i in obj:
                new_obj = decode_object(i)
                new_list.append(new_obj)
            return new_list
        elif isinstance(obj, dict):
            new_dict = {}
            for key, value in obj.items():
                new_key = decode_object(key)
                new_value = decode_object(value)
                new_dict[new_key] = new_value
            return new_dict
        else:
            return obj

    bad_keys = ("__builtins__",)
    jd = {}
    for key, value in d.items():
        if not isinstance(value, ok_types):
            continue
        if key in bad_keys:
            continue
        try:
            # Python's JSON encoder will produce output that
            # the JSON decoder cannot parse if the input string
            # contains unicode "unpaired surrogates" (only on Linux)
            # To test for this, we try decoding the output and check
            # for a ValueError
            value = json.loads(json.dumps(decode_object(value)))

            # Also ensure that the keys encode/decode correctly
            key = json.loads(json.dumps(decode_object(key)))
        except Exception:
            continue
        else:
            jd[key] = value
    return json.loads(json.dumps(jd))


def not_safe_exec(
    code, globals_dict, files=None, python_path=None, slug=None, extra_files=None
):
    """
    Another implementation of `safe_exec`, but not safe.

    This can be swapped in for debugging problems in sandboxed Python code.

    This is not thread-safe, due to temporarily changing the current directory
    and modifying sys.path.

    """
    g_dict = json_safe(globals_dict)

    with temp_directory() as tmpdir:
        with change_directory(tmpdir):
            # Copy the files here.
            for filename in files or ():
                dest = os.path.join(tmpdir, os.path.basename(filename))
                shutil.copyfile(filename, dest)
            for filename, contents in extra_files or ():
                dest = os.path.join(tmpdir, filename)
                with open(dest, "wb") as f:
                    f.write(contents)

            original_path = sys.path
            if python_path:
                sys.path.extend(python_path)
            try:
                exec(code, g_dict)
            except Exception as e:
                # Wrap the exception in a SafeExecException, but we don't
                # try here to include the traceback, since this is just a
                # substitute implementation.
                msg = "{0.__class__.__name__}: {0!s}".format(e)
                raise SafeExecException(msg)
            finally:
                sys.path = original_path

    globals_dict.update(json_safe(g_dict))
    return globals_dict


# If the developer wants us to be unsafe (ALWAYS_BE_UNSAFE), or if there isn't
# a configured jail for Python, then we'll be UNSAFE.
UNSAFE = ALWAYS_BE_UNSAFE or not jail_code.is_configured("python")

if UNSAFE:  # pragma: no cover
    # Make safe_exec actually call not_safe_exec, but log that we're doing so.

    def safe_exec(*args, **kwargs):  # pylint: disable=E0102
        """An actually-unsafe safe_exec, that warns it's being used."""

        # Because it would be bad if this function were used in production,
        # let's log a warning when it is used.  Developers can live with
        # one more log line.
        slug = kwargs.get("slug", None)
        log.warning("Using codejail/safe_exec.py:not_safe_exec for %s", slug)

        return not_safe_exec(*args, **kwargs)