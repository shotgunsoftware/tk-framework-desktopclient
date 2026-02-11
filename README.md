[![Supported VFX Platform: CY2022 - CY2026](https://img.shields.io/badge/VFX_Reference_Platform-CY2022_|_CY2023_|_CY2024_|_CY2025_|_CY2026-blue)](http://www.vfxplatform.com/ "Supported VFX Reference Platform versions")
[![Supported Python versions: 3.9, 3.10, 3.11, 3.13](https://img.shields.io/badge/Python-3.9_|_3.10_|_3.11_|_3.13-blue?logo=python&logoColor=f5f5f5)](https://www.python.org/ "Supported Python versions")
[![Build Status](https://dev.azure.com/shotgun-ecosystem/Toolkit/_apis/build/status/Frameworks/tk-framework-desktopclient?branchName=master)](https://dev.azure.com/shotgun-ecosystem/Toolkit/_build/latest?definitionId=75&branchName=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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
