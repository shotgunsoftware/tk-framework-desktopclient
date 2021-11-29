[![Python 2.7 3.7](https://img.shields.io/badge/python-2.7%20%7C%203.7-blue.svg)](https://www.python.org/)
[![Build Status](https://dev.azure.com/shotgun-ecosystem/Toolkit/_apis/build/status/Frameworks/tk-framework-desktopclient?branchName=master)](https://dev.azure.com/shotgun-ecosystem/Toolkit/_build/latest?definitionId=75&branchName=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linting](https://img.shields.io/badge/PEP8%20by-Hound%20CI-a873d1.svg)](https://houndci.com)

## Documentation
This repository is a part of the ShotGrid Pipeline Toolkit.

- For more information about this app and for release notes, *see the wiki section*.
- For general information and documentation, click here: https://developer.shotgridsoftware.com/d587be80/?title=Integrations+User+Guide
- For information about ShotGrid in general, click here: https://www.shotgridsoftware.com/integrations

## Using this app in your Setup
All the apps that are part of our standard app suite are pushed to our App Store.
This is where you typically go if you want to install an app into a project you are
working on. For an overview of all the Apps and Engines in the Toolkit App Store,
click here: https://developer.shotgridsoftware.com/162eaa4b/?title=Pipeline+Integration+Components

## Have a Question?
Don't hesitate to contact us! You can find us on https://knowledge.autodesk.com/contact-support

## Use the standalone client

This repository can be used as a command line tool. In order to make a request
to a ShotGrid Create, you can execute a the `create_client.py` file using `python create_client.py`

## Build the vendors folder

In order to re-build the Vendors folder, you need to run the `vendors.sh` on mac and on linux and the `vendors.bat` script on Windows. The `python` need to resolve to a valid Python2 interpreter and `python3` need to resolve to a valid Python3 interpreter.
