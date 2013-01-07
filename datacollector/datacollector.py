# coding: utf-8
from __future__ import unicode_literals

import time
import logging
from abc import (
    ABCMeta,
    abstractmethod,
)

import requests
import slumber

logger = logging.getLogger(__name__)


class ResourceUnavailableError(Exception):
    def __init__(self, *args, **kwargs):
        super(ResourceUnavailableError, self).__init__(*args, **kwargs)


class DataCollector(object):
    """
    Responsible for collecting data from RESTful interfaces,
    and making them available as Python datastructures.

    Implements an iterable interface.
    """
    __metaclass__ = ABCMeta

    ITEMS_PER_REQUEST = 20

    def __init__(self, resource_url, slumber_lib=slumber, collection=None):
        self._resource_url = resource_url
        self._slumber_lib = slumber_lib

        self._api = self._slumber_lib.API(resource_url)
        self.resource = getattr(self._api, self._resource_name)

        self._collection = collection

        # memoization to avoid unecessary field lookups
        # Ex.: _memo['publishers']['1'] = 'Unesp'
        # self._memo = {}
        # self._last_resource = {}

    def fetch_data(self, offset, limit, collection=None):
        kwargs = {}

        if collection:
            kwargs['collection'] = collection

        return self.resource.get(offset=offset, limit=limit, **kwargs)

    def __iter__(self):
        offset = 0
        limit = self.ITEMS_PER_REQUEST
        err_count = 0

        while True:
            try:  # handles resource unavailability
                page = self.fetch_data(offset=offset, limit=limit,
                    collection=self._collection)
            except requests.exceptions.ConnectionError as exc:
                if err_count < 10:
                    wait_secs = err_count * 5
                    logger.info('Connection failed. Waiting %ss to retry.' % wait_secs)
                    time.sleep(wait_secs)
                    err_count += 1
                    continue
                else:
                    logger.error('Unable to connect to resource (%s).' % exc)
                    raise ResourceUnavailableError(exc)
            else:
                for obj in page['objects']:
                    # we are interested only in non-trashed items.
                    if obj.get('is_trashed'):
                        continue

                    yield self.get_data(obj)

                if not page['meta']['next']:
                    raise StopIteration()
                else:
                    offset += self.ITEMS_PER_REQUEST
                    err_count = 0

    def _lookup_field(self, endpoint, res_id, field):

        def http_lookup():
            """
            The last accessed resource is cached,
            in order to improve multiple fields lookup
            on the same resouce.
            """
            res_lookup_key = '%s-%s' % (endpoint, res_id)
            if res_lookup_key not in self._last_resource:
                self._last_resource = {}  # release the memory
                self._last_resource[res_lookup_key] = getattr(
                    self._api, endpoint)(res_id).get()

            return self._last_resource[res_lookup_key]

        one_step_before = self._memo.setdefault(
                endpoint, {}).setdefault(
                    res_id, {})

        try:
            return one_step_before[field]
        except KeyError:
            one_step_before[field] = http_lookup()[field]
            return one_step_before[field]

    def _lookup_fields(self, endpoint, res_id, fields):

        attr_list = {}

        for field in fields:
            attr_list[field] = self._lookup_field(endpoint, res_id, field)

        return attr_list

    @abstractmethod
    def get_data(self, obj):
        """
        Get data from the specified resource and returns
        it as Python native datastructures.
        """
