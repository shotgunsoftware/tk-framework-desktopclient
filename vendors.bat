rem Copyright (c) 2019 Shotgun Software Inc.
rem
rem CONFIDENTIAL AND PROPRIETARY
rem
rem This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
rem Source Code License included in this distribution package. See LICENSE.
rem By accessing, using, copying or modifying this work you indicate your
rem agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
rem not expressly granted therein are reserved by Shotgun Software Inc.

rem Locate the vendors folder and zip file from the script location
set VENDORS="%~dp0Vendors\Windows"

rem Locate the requirements.txt file
set REQUIREMENTS="%~dp0requirements.txt"

rem Remove everything in the vendors folder
del /F/S/Q %VENDORS%  > NUL
RMDIR /S/Q %VENDORS%

rem Build the Vendors folder
mkdir %VENDORS%

mkdir %VENDORS%\2
python -m pip install -r %REQUIREMENTS% -t %VENDORS%\2

mkdir %VENDORS%\3
python3 -m pip install -r %REQUIREMENTS% -t %VENDORS%\3