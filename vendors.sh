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

set -o xtrace # Echo what get executed

BASEDIR=$(pwd)/$(dirname "$0")

# Locate the Vendors folder and zip file from the script location
VENDORS=$BASEDIR/Vendors

# Locate the requirements.txt file
REQUIREMENTS=$BASEDIR/requirements.txt

# Remove everything in the Vendors folder
rm -rf $VENDORS

# Build the Vendors folder
mkdir -p $VENDORS

python -m pip install --no-compile -r $REQUIREMENTS -t $VENDORS

set +o xtrace
