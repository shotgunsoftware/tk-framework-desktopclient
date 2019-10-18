# Copyright (c) 2019 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

from create_client import *
from create_utils import *
import time


def is_create_running(sg_connection=None):
    """
    Launch Shotgun Create and inject the current authentication informations into the Shotgun Create session.

    :returns: The success of the Shotgun Create launch
    :rtype: bool
    """
    try:
        CreateClient(sg_connection)
        return True
    except Exception as e:
        return False


def ensure_create_server_is_running(sg_connection=None, retry_count=30):
    """
    This function ensure that Shotgun Create is running.

    This is an helper function that starts Shotgun Create with the right
    Shotgun Session if Create is not running and wait up to `retry_count`
    seconds for the WebSocket server to be initialized.

    :returns: Returns the success of connecting to the Shotgun Create
            websocket server.
    :rtype: bool
    """
    if is_create_running(sg_connection):
        return True

    launch_status = launch_shotgun_create(sg_connection)

    if not launch_status:
        return launch_status

    for _ in range(0, retry_count):
        time.sleep(1)

        if is_create_running(sg_connection):
            return True

    return False
