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

import sgtk
logger = sgtk.platform.get_logger(__name__)


def get_vendors_path():
    """Return the path to the vendors folder.

    The vendors folder is a way to package the dependecies of this framework in a "It just works" manner.

    Returns:
        str -- Path to the vendors folder
    """
    return os.path.abspath(os.path.join(
        os.path.dirname(__file__), "vendors.zip"))


def patch_environment():
    """
    This function patch the python path if the required modules are not available.

    It tries to import all the required dependecies and if one is missing, the vendor
    path get added at the end of the python path.

    Nothins is done if all the required packages are already available.
    """
    # Try to import websocket to see if we are good to go.
    try:
        import websocket        # websocket-client
        import cryptography     # cryptography

        logger.debug("Using global python libraries unaltered .")
    except ImportError:
        # We have our version of websocket packaged with the framework for this case.
        vendor_path = get_vendors_path()
        logger.debug("Adding {} to the python path".format(vendor_path))
        sys.path.append(vendor_path)

        import websocket        # websocket-client
        import cryptography     # cryptography


def unpatch_environment():
    """
    Removes the vendors path from the python path.
    """
    try:
        sys.path.remove(get_vendors_path())
    except ValueError:
        # vendor path is not in the sys path
        pass


class DesktopClientFramework(sgtk.platform.Framework):
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
