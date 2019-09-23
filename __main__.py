#! /usr/bin/env python

# Copyright (c) 2019 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

from __future__ import print_function, absolute_import

from framework import patch_environment
patch_environment()


def main():
    import sgtk
    import json

    from python import desktop_client

    sgtk.set_authenticated_user(
        sgtk.authentication.ShotgunAuthenticator().get_default_user())

    client = desktop_client.DesktopClient()
    commands = client.call_server_method("list_supported_commands")
    print("DesktopClient standalone client")
    print()
    print("Usage:")
    print("> COMMAND :: ARGUMENT")
    print()
    print()
    print("Example:")
    print("> set_media_path :: {\"path\": \"/media/Picture.jpeg\"}")
    print()
    print()
    print("Available commands:")
    for command in sorted(commands):
        print(" - " + str(command))
    print()
    print("Enter command ('exit' to exit )")

    while True:
        try:
            user_input = raw_input("> ").strip()

            if user_input == "exit":
                exit(0)

            if "::" in user_input:
                command, args = user_input.split("::")
                command = str(command.strip())
                args = str(args.strip())
            else:
                command = user_input.strip()
                args = "{}"

            print()
            print("Command: {}".format(command))
            print("Arguments: {}".format(args))
            print()

            server_resp = client.call_server_method(command, json.loads(args))
            print(server_resp)
        except RuntimeError as e:
            print(str(e))
            pass


if __name__ == "__main__":
    main()
