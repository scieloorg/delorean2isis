=============
delorean2isis
=============

Script to import journals metadata from Journal Manager to ISIS databases.


Requirements
============

    #. Python2.7 (http://python.org)
    #. easy_install (https://pypi.python.org/pypi/setuptools)
    #. pip (http://www.pip-installer.org/en/latest/installing.html)
        
How to Install
==============

    #. Run pip install -r requirements.py
    #. Edit the config file according to your Journal Manager credentians.

Importing data
==============

python delorean2isis.py -c COLLECTION -o g:/SciELO/serial

where

-c is the collection slugname at Journal Manager
-o is the directory where the imported files will be copied