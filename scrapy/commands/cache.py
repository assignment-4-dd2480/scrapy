from __future__ import print_function
import os
import json

from scrapy.commands import ScrapyCommand
from scrapy.settings import BaseSettings, iter_default_settings
from scrapy.exceptions import UsageError
from scrapy.extensions.httpcache import FilesystemCacheStorage
from scrapy.downloadermiddlewares.httpcache import HttpCacheMiddleware


class Command(ScrapyCommand):

    requires_project = False
    default_settings = {'LOG_ENABLED': False}

    def syntax(self):
        return "[options]"

    def short_desc(self):
        return "Get information about cached requests/responses"

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        parser.add_option("-l", "--list", dest="list", action="store_true",
                          help="List entries in cache")

    def run(self, args, opts):
        settings = self.crawler_process.settings
        settings_dict = settings._to_dict()
        if not settings_dict['HTTPCACHE_ENABLED']:
            raise UsageError("The Http-cache is disabled in settings")
        else:
            mw = HttpCacheMiddleware(settings, None)  # TODO: unclear what 2nd arg 'stats' is for
            cache = mw.storage
            if os.path.exists(cache.cachedir) and len(os.listdir(cache.cachedir)) > 0:
                print('Cache entries found:')
                # os.walk() yields two lists for each directory it visits - files and dirs.
                for (dirpath, dirnames, filenames) in os.walk(cache.cachedir):
                    if len(filenames) > 0:
                        for filename in filenames:
                            print(f'{dirpath}/{filename}')
            else:
                print('The Http-cache is currently empty')
