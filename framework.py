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
import sys
import platform

import sgtk

logger = sgtk.platform.get_logger(__name__)


def get_vendors_path():
    """Return the path to the vendors folder.

    The vendors folder is a way to package the dependecies of this framework in a "It just works" manner.

    :returns: path to the vendors folder
    :rtype: str
    """

    return os.path.abspath(os.path.join(os.path.dirname(__file__), "Vendors"))


def patch_environment():
    """
    This function patch the python path to add the required modules to the python path.
    """
    # Try to import websocket to see if we are good to go.

    vendor_path = get_vendors_path()

    if vendor_path not in sys.path:
        logger.debug("Adding {} to the python path".format(vendor_path))
        sys.path.insert(0, vendor_path)


def unpatch_environment():
    """
    Removes the vendors path from the python path.
    """
    vendor_path = get_vendors_path()
    if vendor_path in sys.path:
        sys.path.remove(get_vendors_path())


class CreateClientFramework(sgtk.platform.Framework):
    def init_framework(self):
        """
        Implemented by deriving classes in order to initialize the app.
        Called by the engine as it loads the framework.
        """
        self.log_debug("%s: Initializing..." % self)
        patch_environment()

    def destroy_framework(self):
        """
        Implemented by deriving classes in order to tear down the framework.
        Called by the engine as it is being destroyed.
        """
        self.log_debug("%s: Destroying..." % self)
        unpatch_environment()
