#coding:utf-8
from datacollector.datacollector import DataCollector


class TitleCollector(DataCollector):
    _resource_name = 'journals'

    def get_data(self, obj):
        del(obj['collections'])
        del(obj['issues'])
        del(obj['resource_uri'])

        # dateiso format
        obj['created'] = obj['created'][:10].replace('-', '')
        obj['updated'] = obj['updated'][:10].replace('-', '')

        # get id from a string like: /api/v1/users/1/
        userid = obj['creator'].strip('/').split('/')[-1]

        obj['creator'] = self._lookup_field('users', userid, 'username')

        obj['display'] = {}
        obj['display']['pt'] = u"^lpt"
        obj['display']['en'] = u"^len"
        obj['display']['es'] = u"^les"

        # lookup sponsors
        sponsors = []
        for sponsor in obj['sponsors']:
            spoid = sponsor.strip('/').split('/')[-1]
            sponsors.append(self._lookup_field('sponsors', spoid, 'name'))
        obj['sponsors'] = sponsors

        # Short Title
        if 'short_title':
            obj['display']['pt'] += u'^t' + unicode(obj['short_title'])
            obj['display']['en'] += u'^t' + unicode(obj['short_title'])
            obj['display']['es'] += u'^t' + unicode(obj['short_title'])

        return obj
