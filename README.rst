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
    #. Create de virtual environment variables.

Environment variables
---------------------

    API_URL  # URL to the SciELO Manager API.

    API_USER  # You API user name in SciELO Manager.
    
    API_KEY  # Your API key in SciELO Manager.
    
    DELOREAN_URL  # domain to Delorean.
    
    COLLECTION_SLUG  # Collection Slug in SciELO Manager.
    
    SERIAL_SOURCE_DIR  # full path to the serial folder where the databases will be copied to.

Running
-------

    delorean2isis -c $COLLECTION_SLUG -o $SERIAL_SOURCE_DIR


How To Install with Docker
==========================

    docker build -t scieloorg/delorean2isis

Environment variables
---------------------

    API_URL  # URL to the SciELO Manager API.
    
    API_USER  # You API user name in SciELO Manager.
    
    API_KEY  # Your API key in SciELO Manager.
    
    DELOREAN_URL  # domain to Delorean.
    
    COLLECTION_SLUG  # Collection Slug in SciELO Manager.
    
    SERIAL_SOURCE_DIR  # full path to the serial folder where the databases will be copied to.


Running with Docker
-------------------

    docker run -it --rm --name delorean2isis -e DELOREAN_URL=http://200.136.72.82:6543/generate/ -e API_USER=<youruser> -e API_KEY=<yourkey> -e ISIS_PATH=/app/cisis/ -e COLLECTION_SLUG=espanha -e SERIAL_SOURCE_DIR=/app/serial -v ~/Trabalho/delorean2isis/serial/:/app/serial/ -v ~/Trabalho/web/proc/cisis/:/app/cisis/ delorean2isis delorean2isis -c espanha -o /app/serial
