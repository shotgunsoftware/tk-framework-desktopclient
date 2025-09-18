[![VFX Platform](https://img.shields.io/badge/vfxplatform-2024%20%7C%202023%20%7C%202022%20%7C%202021-blue.svg)](http://www.vfxplatform.com/)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.10%20%7C%203.9%20%7C%203.7-blue.svg)](https://www.python.org/)
[![Build Status](https://dev.azure.com/shotgun-ecosystem/Toolkit/_apis/build/status/Frameworks/tk-framework-desktopclient?branchName=master)](https://dev.azure.com/shotgun-ecosystem/Toolkit/_build/latest?definitionId=75&branchName=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linting](https://img.shields.io/badge/PEP8%20by-Hound%20CI-a873d1.svg)](https://houndci.com)

## Documentation
This repository is a part of the Flow Production Tracking Toolkit.

- For more information about this app and for release notes, *see the wiki section*.
- For general information and documentation, click here: https://developer.shotgridsoftware.com/d587be80/?title=Integrations+User+Guide
- For information about Flow Production Tracking in general, click here: https://www.shotgridsoftware.com/integrations

## Using this app in your Setup
All the apps that are part of our standard app suite are pushed to our App Store.
This is where you typically go if you want to install an app into a project you are
working on. For an overview of all the Apps and Engines in the Toolkit App Store,
click here: https://developer.shotgridsoftware.com/162eaa4b/?title=Pipeline+Integration+Components

## Have a Question?
Don't hesitate to contact us! You can find us on https://www.autodesk.com/support

## Use the standalone client

This repository can be used as a command line tool. In order to make a request
to a Create app, you can execute a the `create_client.py` file using `python create_client.py`

## Build the vendors folder

Requirements:
  * [pyenv](https://github.com/pyenv/pyenv)
  * Install Python 3.7
    ```shell
    pyenv install 3.7.16
    ```

Rebuild:
 1. Load Python 3.7
    ```shell
    pyenv shell 3.7.16
    ```

 2. Run the `vendors.sh` script
    ```shell
    python dev/update_python_packages.py
    ```
