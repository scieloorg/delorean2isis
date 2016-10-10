#!/usr/bin/python
#coding:utf-8

import os
import sys
import json
import urllib
import shutil
import tarfile
import urllib2
import tempfile
import argparse

import config

from titlecollector import TitleCollector
from transformer import Transformer

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DATABASES_FST = {
    'title': os.path.join(DIR_PATH, 'title.fst'),
    'issue': os.path.join(DIR_PATH, 'issue.fst')
}


def save_bundle_tar(file_name, data, path=""):
    try:
        bundle = open(os.path.join(path, file_name + '.tar'), "wb")
        bundle.write(data.read())
        bundle.close()
    except IOError, e:
        print 'IO Error:', e
        sys.exit()


def extract_tar(file_name, path=""):
    try:
        tarfile.open(os.path.join(path, file_name + '.tar'), 'r').extract(file_name + '.id', path)
        return os.path.join(path, file_name + '.id')
    except IOError, e:
        print "IOError:", e
        sys.exit()


def fetch_url(url, params=None):
    try:
        return urllib2.urlopen(url + "?%s" % params if params else url)
    except urllib2.HTTPError, e:
        print "HTTP Error:", e.code
        sys.exit()


def isis_exec(cmd):
    try:
        os.system(cmd)
    except OSError, e:
        print "OSError:", e
        sys.exit()


def append_ahead_issue(issue_id_path, collection, year):

    HERE = os.path.abspath(os.path.dirname(__file__))

    # data generator
    iter_data = TitleCollector(config.API_URL, collection=collection,
            username=config.API_USER, api_key=config.API_KEY)

    # id file rendering
    transformer = Transformer(filename=os.path.join(HERE,
        'templates/issue_db_entry.txt'))

    string_nahead = transformer.transform_list(iter_data, year)

    open(issue_id_path, 'a').write(string_nahead.encode('ISO-8859-1'))

    return issue_id_path


def main():

    parser = argparse.ArgumentParser(
        description='Script to get metadata from SciELO Manager \
            and generate databases for Title Manager')

    parser.add_argument('-c', '--collection',
        help='the collection name to get metadata', required=True)
    parser.add_argument('-o', '--output',
        help='the output path to isis databases', required=True)

    args = parser.parse_args()

    try:
        tmp_dir = tempfile.mkdtemp()
        print "Generated process directory: " + tmp_dir
    except OSError, e:
        print "OSError:", e
        sys.exit()

    for database in DATABASES_FST:
        print "Get metadata from database: " + database.upper() + " on collection " \
            + args.collection.upper() + "..."
        params = urllib.urlencode({'collection': args.collection})
        resource_response = fetch_url(config.DELOREAN_URL + database, params)
        bundle_dict = json.loads(resource_response.read())
        bundle = fetch_url(bundle_dict['expected_bundle_url'])

        print "Generate tar file..."
        save_bundle_tar(database, bundle, tmp_dir)

        print "Extract tar file and generate " + database + " id file."
        database_id_path = extract_tar(database, tmp_dir)

        if database == 'issue':
            append_ahead_issue(database_id_path, args.collection, 'CURRENT')
            append_ahead_issue(database_id_path, args.collection, 'LAST_YEAR')

        print "Generate isis database: " + database
        isis_exec(config.ISIS_PATH + 'id2i ' + database_id_path + ' create/app=' \
            + os.path.join(args.output, database, database))

        print "Generate isis index using fst: " + DATABASES_FST[database]
        isis_exec(config.ISIS_PATH + 'mx ' + os.path.join(args.output, database, database) \
            + ' fst=@' + config.DATABASES_FST[database] + ' fullinv/ansi=' \
            + os.path.join(args.output, database, DATABASES_FST[database]))

    print "Deleting temp directory: " + tmp_dir
    shutil.rmtree(tmp_dir)
    print "Finish process."
