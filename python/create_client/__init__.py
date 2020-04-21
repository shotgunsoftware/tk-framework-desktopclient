# Copyright (c) 2019 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

from .create_client import CreateClient
from .create_utils import (
    get_shotgun_create_path,
    launch_shotgun_create,
    is_create_installed,
)

import time
import webbrowser


def is_create_running(sg_connection=None):
    """
    Check for the status of Shotgun Create.

    :param Shotgun sg_connection: Shotgun connection to use with the CreateClient.
        If not set, the connection from the current bundle is used.

    :returns: ``True`` if Shotgun Create is running, ``False`` if not.
    :rtype: bool
    """
    try:
        CreateClient(sg_connection)
        return True
    except Exception:
        return False


def ensure_create_server_is_running(sg_connection=None, retry_count=30):
    """
    This function ensure that Shotgun Create is running.

    This is an helper function that starts Shotgun Create with the right
    Shotgun Session if Create is not running and wait up to ``retry_count``
    seconds for the WebSocket server to be initialized.

    :param Shotgun sg_connection: Shotgun connection to use with the CreateClient.
            If not set, the connection from the current bundle is used.

    :param int retry_count: Amount of retry to use when check if Shotgun Create is running.

    :returns: ``True`` is we could connect to Shotgun Create, ``False`` otherwise.
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


def open_shotgun_create_download_page(sg_connection):
    """
    Open the create download page on the preferred browser.
    """

    CREATE_DOWNLOAD_ENDPOINT = "page/create_download?showToolkitBanner"

    download_page = "/".join(
        [sg_connection.base_url.rstrip("/"), CREATE_DOWNLOAD_ENDPOINT]
    )

    webbrowser.open(download_page)
