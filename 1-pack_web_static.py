#!/usr/bin/python3
"""
This module provides a function to create a .tgz archive from web_static folder
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """Create a tar gzipped pf the directory web_static."""
    now = datetime.now().strftime("%Y%m%d%H%M%S")

    # construct path where archive will be saved
    archive_path = "versions/web_static_{}.tgz".format(now)

    # use fabric function to create directory if it doesn't exist
    local("mkdir -p versions")

    # use tar command to create a compress archive
    archived = local("tar -cvzf {} web_static".format(archive_path))

    # check archive creation statis
    if archived.return_code != 0:
        return None
    else:
        return archive_path
