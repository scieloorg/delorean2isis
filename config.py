#coding:utf-8
#!/usr/bin/python

import os

API_URL = os.environ.get(API_URL, 'http://manager.scielo.org/api/v1/')
API_USER = os.environ.get(API_USER, '')
API_KEY = os.environ.get(API_KEY, '')
DELOREAN_URL = os.environ.get(DELOREAN_URL, 'http://localhost:6543/generate/')
ISIS_PATH = os.environ.get(DELOREAN_URL, '/app/cisis')
DATABASES = ["title", "issue"]
DATABASE_FST = {'title': 'tit_issn', 'issue': 'issue'}
