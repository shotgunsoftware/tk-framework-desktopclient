# Copyright (c) 2019 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import json
import time
import ssl

# Coming from the vendors folder
import websocket
from fernet import Fernet

import sgtk

try:
    # Six comes bundled with this framework, however there can be cases
    # where an older version of six has already been imported, so we should
    # try to import from the tank_vendor name space to avoid clashes.
    from tank_vendor import six
except ImportError:
    # sgtk isn't around and it is probably running standalone.
    import six

logger = sgtk.LogManager.get_logger(__name__)


class CreateClient(object):
    SG_CREATE_SETTINGS_KEY = "view_master_settings"
    SG_CREATE_WEBSOCKET_PORT_KEY = "websocket_port"
    SG_CREATE_DEFAULT_WEBSOCKET_PORT = 9006

    message_id = 0

    @classmethod
    def _get_next_message_id(cls):
        """
        Build a unique message id.

        :returns: Message id
        :rtype: int
        """
        cls.message_id += 1
        return cls.message_id

    def __init__(self, sg_connection=None, port_override=None):
        """
        Builds a WebSocket client used to send requests to a Shotgun WebSocket server such as
        Shotgun Create.

        The websocket client grab the Shotgun websocket port from Shotgun and do the server handshake so
        talking to a server is facilitated.

        Warning: You need to be authenticated to build a CreateClient instance.

        In order to be able to use the app as a standalone command line tool, we need to be able inject
        a shotgun connection object so it doesn't rely on the 'current_bundle'

        :param Shotgun sg_connection: Shotgun connection to use with this client.
                If not set, the connection from the current bundle is used.

        :param int port_override: The port number used for the connection. If not set,
                the value from Shotgun preferences or a default value is used
        """
        super(CreateClient, self).__init__()

        self._connection = None
        self._server_id = None
        self._secret = None
        self._protocol_version = None
        self._shotgun_connection = (
            sg_connection or sgtk.platform.current_bundle().shotgun
        )

        # We can't do anything without authenticated user.
        if self._current_user is None:
            raise RuntimeError(
                "Unable to create a ShotGrid Create Client unauthenticated."
            )

        if port_override is not None:
            self.shotgun_create_websocket_port = port_override
        else:
            # Grab the WebSocket server port from Shotgun
            prefs = self._shotgun_connection.preferences_read()
            sg_create_prefs = json.loads(
                prefs.get(CreateClient.SG_CREATE_SETTINGS_KEY, {})
            )
            self.shotgun_create_websocket_port = sg_create_prefs.get(
                CreateClient.SG_CREATE_WEBSOCKET_PORT_KEY,
                CreateClient.SG_CREATE_DEFAULT_WEBSOCKET_PORT,
            )

        # Initialize the connection
        if self._desktop_connection is None:
            raise RuntimeError("Unable to build the WebSocket connection.")

    def call_server_method(self, name, data=None):
        """
        Make a call to a WebSocket server method and return the reply as a python dict.

        :param str name: Name of the server method
        :param dict data: Arguments of the server method (default: {None})

        :returns: Reply from the server as a python object (reply json is part).
        :rtype: dict
        """
        # Get the server method as a Dict
        resp = json.loads(self._call_server_method(name, data))
        return resp.get("reply", "")

    @property
    def _desktop_connection(self):
        """
        Return the currently active websocket connection to the Shotgun WebSocket server.

        If there's no active connection, the function builds a new connection and do the
        handshake so it's ready to use.

        :returns: active websocket connection to the Shotgun WebSocket server.
        :rtype: WebSocket
        """
        try:
            if self._connection:
                # Ping the server to make sure the connection is still valid.
                try:
                    self._connection.ping()
                except RuntimeError as e:
                    logger.debug(
                        "Failed to reuse the active connection: {0}".format(str(e))
                    )
                    logger.debug("Destroying the connection.")
                    self._connection = None

            if not self._connection:
                ssl_defaults = ssl.get_default_verify_paths()

                self._connection = websocket.create_connection(
                    "wss://shotgunlocalhost.com:{0}".format(
                        self.shotgun_create_websocket_port
                    ),
                    sslopt={"ca_certs": ssl_defaults.cafile},
                )

                self._do_websocketserver_handshake()

        except Exception as e:
            logger.debug(
                "Failed to get a valid websocket connection: {0}".format(str(e))
            )
            self._connection = None
            raise

        return self._connection

    @property
    def _current_user(self):
        """
        Get the currently authenticated user.

        :returns: Currently authenticated user.
        :rtype: ShotgunUser
        """
        return sgtk.get_authenticated_user()

    def _send(self, payload):
        """
        Send a payload to the server.

        The payload is encrypted using the WebSocket server secret, if available.

        :param str payload: Payload to send to the server.
        """
        try:
            p = six.ensure_binary(payload)

            # self._secret is expected to be none at the beginning of the connection handshake.
            if self._secret:
                p = self._secret.encrypt(p)

            self._desktop_connection.send(p)
        except RuntimeError as e:
            logger.debug("Failed to send a payload to the server: {0}".format(str(e)))
            pass

    def _recv(self):
        """
        Receive a payload from the server.

        The payload is decrypted using the WebSocket server secret, if available.

        :returns: Message from the server as a string.
        :rtype: str
        """
        try:
            r = six.ensure_binary(self._desktop_connection.recv())

            # self._secret is expected to be none at the beginning of the connection handshake.
            if self._secret:
                r = self._secret.decrypt(r)

            return r
        except RuntimeError as e:
            logger.debug("Failed receive a payload from the server: {0}".format(str(e)))
            return "{}"

    def _send_and_recv(self, payload):
        """ Helper method that:
            - Send a payload to the server.
            - Receive a payload from the server.

        :param str payload: Payload to send to the server.

        :returns: Message from the server as a string.
        :rtype: str
        """
        self._send(payload)

        return self._recv()

    def _call_server_method(self, name, data=None):
        """
        Make a call to a WebSocket server method and return the raw server response as a string.

        :param str name: Name of the server method
        :param dict data: Arguments of the server method (default: {None})

        :returns: Reply from the server as a python object (reply json is part).
        :rtype: dict
        """
        command = {}

        if not data:
            data = {}

        command["name"] = name
        command["data"] = data

        user_info = self._shotgun_connection.find_one(
            "HumanUser",
            [["login", "is", self._current_user.login]],
            ["entity_hash", "groups", "permission_rule_set", "name"],
        )
        command_user = {}
        command_user["entity"] = {}
        command_user["entity"]["id"] = user_info["id"]
        command_user["entity"]["type"] = user_info["type"]
        command_user["entity"]["name"] = user_info["name"]
        command_user["entity"]["status"] = "act"
        command_user["entity"]["valid"] = "valid"
        command_user["group_ids"] = [group["id"] for group in user_info["groups"]]

        command_user["rule_set_display_name"] = user_info["permission_rule_set"]["name"]
        command_user["rule_set_id"] = user_info["permission_rule_set"]["id"]

        command["data"]["user"] = command_user

        message = {}
        message["protocol_version"] = self._protocol_version
        message["id"] = CreateClient._get_next_message_id()
        message["command"] = command
        message["timestamp"] = int(time.time() * 1000)

        return self._send_and_recv(json.dumps(message))

    def _do_websocketserver_handshake(self):
        """
        Execute the websocket server handshake on the currently active websocket connection.

        The handshake is:
            - Get the protocol version from the server
            - Get the WebSocket server ID
            - Get the WebSocket server secret from Shotgun (used to encrypt the communications)

        This function validates the handshake by doing a dummy call to the server at the end
        of the handshake.
        """
        self._secret = None

        # Grab the protocol version from the running Shotgun WebSocket server
        protocol_version_resp = self._send_and_recv("get_protocol_version")
        self._protocol_version = json.loads(protocol_version_resp)["protocol_version"]

        # Grab the WebSocket server ID from the Shotgun WebSocket server
        server_id_resp = json.loads(self._call_server_method("get_ws_server_id"))

        # dekstopserver and create return different structures for this. Allow a response from either server
        if "reply" in server_id_resp:
            server_id_resp = server_id_resp["reply"]

        self._server_id = server_id_resp["ws_server_id"]

        # Ask for the secret for this server id.
        response = self._shotgun_connection._call_rpc(
            "retrieve_ws_server_secret", {"ws_server_id": self._server_id}
        )
        ws_server_secret = six.ensure_binary(response["ws_server_secret"])
        if ws_server_secret[-1:] != b"=":
            ws_server_secret += b"="

        self._secret = Fernet(ws_server_secret)

        # Make a dummy call to the server to make sure that the handshake is correctly done
        supported_command_repsp = self._call_server_method("list_supported_commands")
        supported_commands = json.loads(supported_command_repsp).get("reply", [])

        if "list_supported_commands" not in supported_commands:
            raise RuntimeError("Unknown error in the websocket server handshake")
