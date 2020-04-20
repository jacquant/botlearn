import os
import pathlib
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage


def path_and_rename(instance, filename):
    """Function that will rename and save in the good path.

    :param instance: the object to save with an unique path
    :type instance: Exercise
    :param filename: the name of the file given to save
    :type filename: str
    :return: the path built
    :rtype: str (path)
    """
    upload_to = "exercises/{0}".format(
        uuid.uuid5(uuid.NAMESPACE_DNS, instance.name)
    )
    ext = "".join(pathlib.Path(filename).suffixes)
    # get filename
    filename = "archive{0}".format(ext)
    # return the whole path of the file
    return os.path.join(upload_to, filename)


def validate_file_extensions(object_to_save):
    """Validate the extension of the file (must be .tar/gz).

    :param object_to_save: [description]
    :type object_to_save: Exercise
    :raises ValidationError: if the obhect to save is not a gzip
    """
    ext = "".join(pathlib.Path(object_to_save.name).suffixes)
    if ext.lower() != ".tar.gz":
        raise ValidationError("Unsupported file extension.")


class OverwriteStorage(FileSystemStorage):
    """Custom Storage to overwrite file that already exists.

    If the file existe remove if before save it.
    """

    def get_available_name(self, name):
        """Check if the name of the file already exists and remove it.

        :param name: the name to check existence
        :type name: str
        :return: return the name given
        :rtype: str
        """
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name
