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
set VENDORS="%~dp0Vendors"

rem Locate the requirements.txt file
set REQUIREMENTS="%~dp0requirements.txt"

rem Remove everything in the vendors folder
del /F/S/Q %VENDORS%  > NUL
RMDIR /S/Q %VENDORS%

python -m pip install --no-compile -r %REQUIREMENTS% -t %VENDORS%
