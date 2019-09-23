# Copyright (c) 2019 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import sys
import os
import json
import time
import ssl
import tempfile

from functools import partial

# Comming from the vendors folder
import websocket
from cryptography.fernet import Fernet

import sgtk
from sgtk.authentication import ShotgunAuthenticator

logger = sgtk.LogManager.get_logger(__name__)


class DesktopClient(object):
    SG_DESKTOP_SETTINGS_KEY = "view_master_settings"
    SG_DESKTOP_WEBSOCKET_PORT_KEY = "websocket_port"
    SG_DESKTOP_DEFAULT_WEBSOCKET_PORT = 9006

    message_id = 0

    @staticmethod
    def get_next_message_id():
        """
        Build a unique message id.

        Returns:
            [int] -- Message id
        """
        DesktopClient.message_id += 1
        return DesktopClient.message_id

    def __init__(self):
        """
        Builds a WebSocket client used to send requests to a Shotgun WebSocket server such as
        Shotgun Create.

        The websocket client grab the Shotgun websocket port from Shotgun and do the server handshake so
        talking to a server is facilitated.

        Warning: You need to be authenticated to build a DesktopClient instance.

        Raises:
            RuntimeError: Raised if something go wrong while initializing the websocket client.
        """
        super(DesktopClient, self).__init__()

        self._connection = None
        self._server_id = None
        self._secret = None
        self._protocol_version = None

        # We can't do anything without authenticated user.
        if self._current_user is None:
            raise RuntimeError(
                "Unable to create a Shotgun Create Client unauthenticated.")

        # Grab the Desktop cerver CA Bundle from Shotgun and save it on disk
        certificates = self._shotgun_connection._call_rpc(
            "sg_desktop_certificates", {})
        self.ca_file = tempfile.NamedTemporaryFile(
            prefix="destop_ca_cert_", suffix=".pem")
        self.ca_file.write(certificates.get("sg_desktop_ca"))
        self.ca_file.flush()

        # Grab the WebSocket server port from Shotgun
        prefs = self._shotgun_connection.preferences_read()
        sg_create_prefs = json.loads(
            prefs.get(DesktopClient.SG_DESKTOP_SETTINGS_KEY, "{}"))
        self.shotgun_create_websocket_port = sg_create_prefs.get(DesktopClient.SG_DESKTOP_WEBSOCKET_PORT_KEY,
                                                                 DesktopClient.SG_DESKTOP_DEFAULT_WEBSOCKET_PORT)

        # Initialize the connection
        if self._desktop_connection is None:
            raise RuntimeError("Unable to build the WebSocket connection.")

    def call_server_method(self, name, data=None):
        """
        Make a call to a WebSocket server method and return the reply as a python dict.

        Arguments:
            name {str} -- Name of the server method

        Keyword Arguments:
            data {dict} -- Arguments of the server method (default: {None})

        Returns:
            dict -- Reply from the server as a python object (reply json is part).
        """
        # Get the server method as a Dict
        resp = json.loads(self._call_server_method(name, data))
        return resp.get("reply", "")

    @property
    def _desktop_connection(self):
        """
        Returns the currently active websocket connection to the Shotgun WebSocket server.

        If there's no active connectionn, the function builds a new connection and do the
        handshake so it's ready to use.

        Returns:
            WebSocket -- Active websocket connection to the Shotgun WebSocket server.
        """
        try:
            if self._connection:
                # Ping the server to make sure the connection is still valid.
                try:
                    self._connection.ping()
                except:
                    logger.debug(
                        "Failed to reuse the active connection. Destroying the connection.")
                    self._connection = None

            if not self._connection:
                os.environ["WEBSOCKET_CLIENT_CA_BUNDLE"] = self.ca_file.name
                self._connection = websocket.create_connection(
                    "wss://shotgunlocalhost.com:{}".format(
                        self.shotgun_create_websocket_port)
                )

                self._do_websocketserver_handshake()
        except:
            logger.debug(
                "Failed to get a valid websocket connection")
            self._connection = None
            raise

        return self._connection

    @property
    def _current_user(self):
        """
        Get the currently authenticated user.

        Returns:
            ShotgunUser -- Currently authenticated user.
        """
        return sgtk.get_authenticated_user()

    @property
    def _shotgun_connection(self):
        """
        Get a new Shotgun api connection using the currently authenticated user.

        Returns:
            Shotgun -- Shotgun connection.
        """
        return self._current_user.create_sg_connection()

    def _send(self, payload):
        """
        Send a payload to the server.

        The payload is encrypted using the WebSocket server secret, if available.

        Arguments:
            payload {str} -- Payload to send to the server.
        """
        try:
            p = payload

            if self._secret:
                p = self._secret.encrypt(p)

            self._desktop_connection.send(p)
        except:
            pass

    def _recv(self):
        """
        Receive a payload from the server.

        The payload is dencrypted using the WebSocket server secret, if available.

        Returns:
            str -- Message from the server as a string.
        """
        try:
            r = self._desktop_connection.recv()

            if self._secret:
                r = self._secret.decrypt(r)

            return r
        except:
            return "{}"

    def _send_and_recv(self, payload):
        """ Helper method that:
            - Send a payload to the server.
            - Receive a payload from the server.

        Arguments:
            payload {str} -- Payload to send to the server.

        Returns:
            str -- Message from the server as a string.
        """
        self._send(payload)

        return self._recv()

    def _call_server_method(self, name, data=None):
        """
        Make a call to a WebSocket server method and return the raw server response as a string.

        Arguments:
            name {str} -- Name of the server method

        Keyword Arguments:
            data {dict} -- Arguments of the server method (default: {None})

        Returns:
            dict -- Raw reply from the server as a string.
        """
        command = {}

        if not data:
            data = {}

        command["name"] = name
        command["data"] = data

        user_info = self._shotgun_connection.find_one(
            "HumanUser",
            [
                ["login", "is", self._current_user.login]
            ],
            ["entity_hash", "groups", "permission_rule_set", "name"]
        )
        command_user = {}
        command_user["entity"] = {}
        command_user["entity"]["id"] = user_info["id"]
        command_user["entity"]["type"] = user_info["type"]
        command_user["entity"]["name"] = user_info["name"]
        command_user["entity"]["status"] = "act"
        command_user["entity"]["valid"] = "valid"
        command_user["group_ids"] = [group["id"]
                                     for group in user_info["groups"]]

        command_user["rule_set_display_name"] = user_info["permission_rule_set"]["name"]
        command_user["rule_set_id"] = user_info["permission_rule_set"]["id"]

        command["data"]["user"] = command_user

        message = {}
        message["protocol_version"] = self._protocol_version
        message["id"] = DesktopClient.get_next_message_id()
        message["command"] = command
        message["timestamp"] = int(time.time() * 1000)

        return self._send_and_recv(json.dumps(message))

    def _do_websocketserver_handshake(self):
        """
        Execute the websocket server handshake on the currently active websocket connection.

        The hanshake is:
            - Get the protocol version from the server
            - Get the WebSocket server ID
            - Get the WebSocket server secret from Shotgun (used to encrypt the communications)

        This function validate the hanshake by doing a dummy call to the server at the end
        of the handshake.

        Raises:
            RuntimeError: Raised if the call to the dummy method fail at the end of the endshake
        """
        self._secret = None

        # Grab the protocol version from the running Shotgun WebSocket server
        protocol_version_resp = self._send_and_recv(
            "get_protocol_version")
        self._protocol_version = json.loads(protocol_version_resp)[
            "protocol_version"]

        # Grab the WebSocket server ID from the Shotgun WebSocket server
        server_id_resp = self._call_server_method("get_ws_server_id")
        self._server_id = json.loads(server_id_resp)["ws_server_id"]

        # Ask for the secret for this server id.
        response = self._shotgun_connection._call_rpc(
            "retrieve_ws_server_secret", {"ws_server_id": self._server_id}
        )
        ws_server_secret = response["ws_server_secret"]
        if ws_server_secret[-1] != "=":
            ws_server_secret += "="

        self._secret = Fernet(ws_server_secret)

        # Make a dummy call to the server to make sure that the handshake is correctly done
        supported_command_repsp = self._call_server_method(
            "list_supported_commands")
        supported_commands = json.loads(
            supported_command_repsp).get("reply", [])

        if "list_supported_commands" not in supported_commands:
            raise RuntimeError(
                "Unknown error in the websocket server handshake")
