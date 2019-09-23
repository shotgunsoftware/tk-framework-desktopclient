## Documentation
This repository is a part of the Shotgun Pipeline Toolkit.

- For more information about this app and for release notes, *see the wiki section*.
- For general information and documentation, click here: https://support.shotgunsoftware.com/entries/95441257
- For information about Shotgun in general, click here: http://www.shotgunsoftware.com/toolkit

## Using this app in your Setup
All the apps that are part of our standard app suite are pushed to our App Store.
This is where you typically go if you want to install an app into a project you are
working on. For an overview of all the Apps and Engines in the Toolkit App Store,
click here: https://support.shotgunsoftware.com/entries/95441247.

## Have a Question?
Don't hesitate to contact us! You can find us on support@shotgunsoftware.com

## Use the standalone client

This repository can be used as a command line tool. In order to make a request to a Desktop Server, you can:

1) Execute __main__.py  `python __main__.py`
2) Execute the folder using `python tk-framework-desktopclient` (or `python .` from the root of the folder)
3) Execute a zip of this repository using `pythono tk-framework-desktopclient.zip`

## Build the vendors folder

In order to re-build the vendors folder, you need to:
- Clean the content of the vendors folder and create a new one using `rm -rf vendors && mkdir vendors`
- Fill the vendor folder using `python -m pip install -r requirements.txt -t vendors` from the root of the repository
- Zip that vendor folder using `cd vendors && zip -r ../vendors.zip * && cd -`
- Remove the vendors folder using `rm -rf vendors`
