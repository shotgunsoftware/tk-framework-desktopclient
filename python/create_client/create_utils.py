# Copyright (c) 2019 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import os
import platform
import subprocess

import sgtk

SHOTGUN_CREATE_PATH = dict()
SHOTGUN_CREATE_PATH_ENV = dict()

SHOTGUN_CREATE_PATH["windows"] = os.path.abspath(os.path.join(
    os.sep, "ProgramFiles", "Autodesk", "ShotgunCreate", "bin", "ShotgunCreate.exe"))
SHOTGUN_CREATE_PATH_ENV["windows"] = "SHOTGUN_CREATE_WINDOWS_PATH"

SHOTGUN_CREATE_PATH["darwin"] = os.path.abspath(os.path.join(
    os.sep, "Applications", "Autodesk", "Shotgun Create.app", "Contents", "MacOS", "Shotgun Create"))
SHOTGUN_CREATE_PATH_ENV["darwin"] = "SHOTGUN_CREATE_DARWIN_PATH"

SHOTGUN_CREATE_PATH["linux"] = os.path.abspath(os.path.join(
    os.sep, "opt", "Autodesk", "ShotgunCreate", "bin", "ShotgunCreate"))
SHOTGUN_CREATE_PATH_ENV["linux"] = "SHOTGUN_CREATE_LINUX_PATH"

PLATFORM = platform.system().lower()


def get_shotgun_create_path():
    """
    Returns the path to Shotgun Create. If the sgtk integration is started by Shotgun Create,
    the path is injected in the environment otherwise it returns the default Shotgun Create path.

    :returns: Path to the Shotgun Create executable
    :rtype: str
    """
    shotgun_create_default_path = SHOTGUN_CREATE_PATH[PLATFORM]
    env_var_override_name = SHOTGUN_CREATE_PATH_ENV[PLATFORM]

    return os.environ.get(env_var_override_name, shotgun_create_default_path)


def launch_shotgun_create(sg_connection):
    """
    Launch Shotgun Create and inject the current authentication informations into the Shotgun Create session.

    :returns: The success of the Shotgun Create launch
    :rtype: bool
    """
    try:
        # Set the current credentials so create starts in the right environment
        os.environ["SHOTGUN_CREATE_AUTHENTICATION_SITE"] = sg_connection.base_url
        os.environ["SHOTGUN_CREATE_AUTHENTICATION_SESSION"] = sg_connection.get_session_token()

        with open(os.devnull, 'w') as devnull_f:
            subprocess.Popen([get_shotgun_create_path()],
                            stdout=devnull_f, stderr=devnull_f)
            return True
    except:
        return False


def is_create_installed():
    """
    Check if Shotgun Create is available on disk.

    :returns: The success of the Shotgun Create binary lookup
    :rtype: bool
    """
    return os.path.exists(get_shotgun_create_path())
