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
import sgtk
import json

from framework import patch_environment


def main():
    from python.create_client import CreateClient

    user = sgtk.authentication.ShotgunAuthenticator().get_default_user()
    if not user:
        print("Unable to create a Desktop Client unauthenticated.")
        return 1

    sgtk.set_authenticated_user(user)

    client = CreateClient(user.create_sg_connection())
    commands = client.call_server_method("list_supported_commands")
    print("CreateClient standalone client")
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

    while True:
        try:
            print("Enter command ('exit' to exit )")
            try:
                user_input = raw_input("> ").strip()
            except NameError:
                user_input = input("> ").strip

            if not user_input:
                continue

            if user_input == "exit":
                return

            if "::" in user_input:
                command, args = user_input.split("::")
                command = str(command.strip())
                args = str(args.strip())
            else:
                command = user_input.strip()
                args = "{}"

            print()
            print("Command: {0}".format(command))
            print("Arguments: {0}".format(args))
            print()

            server_resp = client.call_server_method(command, json.loads(args))
            print(json.dumps(server_resp, indent=2, sort_keys=True))
            print()
        except RuntimeError as e:
            print(str(e))
            pass


if __name__ == "__main__":
    patch_environment()
    exit(main())
