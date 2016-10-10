=============
delorean2isis
=============

Script to import journals metadata from Journal Manager to ISIS databases.


Requirements
============

    #. Python2.7 (http://python.org)
    #. pip (http://www.pip-installer.org/en/latest/installing.html)
    #. CISIS 10/30 (http://wiki.bireme.org/pt/index.php/CISIS)
        
How to Install
==============

    #. Run pip install -r requirements.txt
    #. Edit the config file according to your Journal Manager credentians.

Docker Install
==============

docker build -t scieloorg/delorean2isis



Environment variables
---------------------

    API_URL  # URL to the SciELO Manager API.
    API_USER  # You API user name in SciELO Manager.
    API_KEY  # Your API key in SciELO Manager.
    DELOREAN_URL  # domain to Delorean.
    COLLECTION_SLUG  # Collection Slug in SciELO Manager.
    SERIAL_SOURCE_DIR  # full path to the serial folder where the databases will be copied to.

Importing data
==============

python delorean2isis.py -c COLLECTION_SLUG -o g:/SciELO/serial

where

**-c** is the collection slugname at Journal Manager

**-o** is the directory where the imported files will be copied

