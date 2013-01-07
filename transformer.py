#coding:utf-8
import collections
from mako.template import Template
from mako.exceptions import RichTraceback
from datetime import datetime


class Transformer(object):
    """
    Responsible for rendering templates using the given
    dataset.
    """
    def __init__(self, *args, **kwargs):
        """
        Accepts a ``template`` as a string.
        """
        if args:
            self._template = Template(args[0])
        elif 'filename' in kwargs:
            self._template = Template(filename=kwargs['filename'],
                module_directory='/tmp/mako_modules')
        else:
            raise TypeError()

    def transform(self, data):
        """
        Renders a template using the given data.
        ``data`` must be dict.
        """
        if not isinstance(data, dict):
            raise TypeError('data must be dict')

        try:
            return self._template.render(**data)
        except NameError, exc:
            raise ValueError("there are some data missing: {}".format(exc))
        except:
            traceback = RichTraceback()
            for (filename, lineno, function, line) in traceback.traceback:
                print "File %s, line %s, in %s" % (filename, lineno, function)
                print line, "\n"
            print "%s: %s" % (str(traceback.error.__class__.__name__), traceback.error)

    def transform_list(self, data_list, year, callabl=None):
        """
        Renders a template using the given list of data.
        ``data_list`` must be list or tuple.
        """
        if isinstance(data_list, str) or isinstance(data_list, dict) or \
           isinstance(data_list, set):
            raise TypeError('data must be iterable')

        if not isinstance(data_list, collections.Iterable):
            raise TypeError('data must be iterable')

        res = []
        if callabl:
            callabl(data_list)

        for data in data_list:
            if year == 'CURRENT':
                data['publication_date'] = datetime.now().year
                data['current_total_documents'] = data['current_ahead_documents']
            if year == 'LAST_YEAR':
                data['publication_date'] = int(datetime.now().year) - 1
                data['previous_total_documents'] = data['previous_ahead_documents']

            res.append(self.transform(data))

        return '\n'.join(res)
