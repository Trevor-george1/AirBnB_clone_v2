#!/usr/bin/python3
"""
This module provides a function to create a .tgz archive from web_static folder
"""

import os
from fabric.api import *
from datetime import datetime

# set the host IP address for web-01 && web-02
env.hosts = ['35.174.185.44', '54.164.121.37']
env.user = "ubuntu"


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


def do_deploy(archive_path):
    """use os module to check for valid file path"""
    if os.path.exists(archive_path):
        archive = archive_path.split('/')[1]
        a_path = "/tmp/{}".format(archive)
        folder = archive.split('.')[0]
        f_path = "/data/web_static/releases/{}/".format(folder)

        put(archive_path, a_path)
        run("mkdir -p {}".format(f_path))
        run("tar -xzf {} -C {}".format(a_path, f_path))
        run("rm {}".format(a_path))
        run("mv -f {}web_static/* {} || true".format(f_path, f_path))
        run("rm -rf {}web_static".format(f_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(f_path))
        return True
    return False


def deploy():
    """
    createa and archive and get its path
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
