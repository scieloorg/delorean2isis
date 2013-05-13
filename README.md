=============
delorean2isis
=============

Script to get import journals metadata from Journal Manager to ISIS databases.


Requirements
============

    #. Python2.7
    #. Slumber
    #. Mako Templates

How to Install
==============

    #. Edit the config file according to your Journal Manager credentians.
    #. Run pip install -r requirements.py

Importing data
==============

python delorean2isis.py -c COLLECTION -o g:/SciELO/serial

where

-c is the collection slugname at Journal Manager
-o is the directory where the imported files will be copied