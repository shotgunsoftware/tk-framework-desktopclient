#! /usr/bin/env bash

# Copyright (c) 2019 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

set -o xtrace # Echo what get logged

# Get the script location (which is the root of the repository)
BASEDIR=$(pwd)/$(dirname "$0")

# Locate the vendors folder and zip file from the script location
VENDORS=$BASEDIR/vendors

# Locate the requirements.txt file
REQUIREMENTS=$BASEDIR/requirements.txt

# Remove everything in the vendors folder
rm -rf $VENDORS

# Create an empty vendors folder
mkdir -p $VENDORS

# Fill the vendors folder with the content of requirements.txt
python -m pip install -r $REQUIREMENTS -t $VENDORS

set +o xtrace