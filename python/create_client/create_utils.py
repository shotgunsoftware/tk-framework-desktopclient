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

from sgtk.util import ShotgunPath

CREATE_DEFAULT_LOCATION = ShotgunPath.from_shotgun_dict(
    {
        "windows_path": os.path.abspath(
            os.path.join(
                os.sep,
                # The name of the folder can change based on the locale.
                # https://www.samlogic.net/articles/program-files-folder-different-languages.htm
                # The safe way to retrieve the path to the Program Files folder is to read the env var
                # Warning: Running this code on non-window trigger a KeyError
                # This is why we use get with a dummy default value.
                os.environ.get("ProgramFiles", "%ProgramFiles%"),
                "Autodesk",
                "ShotGrid Create",
                "bin",
                "ShotGridCreate.exe",
            )
        ),
        "mac_path": os.path.abspath(
            os.path.join(
                os.sep,
                "Applications",
                "Autodesk",
                "ShotGrid Create.app",
                "Contents",
                "MacOS",
                "ShotGrid Create",
            )
        ),
        "linux_path": os.path.abspath(
            os.path.join(
                os.sep, "opt", "Autodesk", "ShotGridCreate", "bin", "ShotGridCreate"
            )
        ),
    }
)


def get_shotgun_create_path():
    """
    Returns the path to Shotgun Create. If the sgtk integration is started by Shotgun Create,
    the path is injected in the environment otherwise it returns the default Shotgun Create path.

    :returns: Path to the Shotgun Create executable
    :rtype: str
    """

    env_var_override_name = "SHOTGUN_CREATE_{0}_PATH".format(platform.system().upper())

    return os.environ.get(env_var_override_name, CREATE_DEFAULT_LOCATION.current_os)


def launch_shotgun_create(sg_connection=None):
    """
    Launch Shotgun Create and inject the current authentication informations into the Shotgun Create session.

    :param Shotgun sg_connection: Shotgun connection to use with this client. If not set, the connection
    from the current bundle is used.

    :returns: The success of the Shotgun Create launch
    :rtype: bool
    """
    try:
        create_env = os.environ.copy()

        # Set the current credentials so create starts in the right environment
        create_env["SHOTGUN_CREATE_AUTHENTICATION_SITE"] = sg_connection.base_url
        create_env[
            "SHOTGUN_CREATE_AUTHENTICATION_SESSION"
        ] = sg_connection.get_session_token()

        # Unset values that might cause Shotgun Create to not start
        # correctly. Some, originally set by Shotgun Desktop, might
        # affect the way Shotgun Create bootstrap it's engine.
        for environment_variable in [
            "SHOTGUN_PIPELINE_CONFIGURATION_ID",
            "SHOTGUN_SITE",
            "SHOTGUN_ENTITY_TYPE",
            "SHOTGUN_ENTITY_ID",
            "LD_LIBRARY_PATH",  # In Maya on Linux this which causes issues launching Create.
        ]:
            if environment_variable in create_env:
                del create_env[environment_variable]

        with open(os.devnull, "w") as devnull_f:
            subprocess.Popen(
                [get_shotgun_create_path()],
                stdout=devnull_f,
                stderr=devnull_f,
                env=create_env,
            )

            return True

    except Exception:
        return False


def is_create_installed():
    """
    Check if Shotgun Create is available on disk.

    :returns: The success of the Shotgun Create binary lookup
    :rtype: bool
    """

    return os.path.exists(get_shotgun_create_path())
