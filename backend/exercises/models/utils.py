import os
from datetime import datetime
from uuid import uuid4


def path_and_rename(instance, filename):
    upload_to = "exercises/{:%Y/%m/%d}".format(datetime.now())

    ext = filename.split(".")[-1]
    # get filename
    if instance.pk:
        filename = "{file_name}.{extension}".format(
            file_name=instance.pk, extension=ext
        )
    else:
        filename = "{file_name}.{extension}".format(
            file_name=uuid4().hex, extension=ext
        )
    # return the whole path of the file
    return os.path.join(upload_to, filename)
