import os
import pathlib
import tarfile
from uuid import uuid4

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
import uuid


def path_and_rename(instance, filename):
    upload_to = "exercises/{}".format(uuid.uuid5(uuid.NAMESPACE_DNS, instance.name))
    ext = "".join(pathlib.Path(filename).suffixes)
    # get filename
    filename = "archive"+ext
    # return the whole path of the file
    return os.path.join(upload_to, filename)


def validate_file_extensions(value):
    ext = "".join(pathlib.Path(value.name).suffixes)
    valid_extensions = [".tar.gz"]
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported file extension.")


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name
