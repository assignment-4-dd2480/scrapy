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
        return "[options] [<spidername>]"

    def short_desc(self):
        return "Get information about cached requests/responses"

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        parser.add_option("-l", "--list", dest="list", action="store_true",
                          help="List entries in cache. If spidername provided entries of that spider are listed")

    def retrieve_responses(self, spidername, cache):
        """Returns list of cached responses belonging to a spider"""
        spider_root_path = os.path.join(cache.cachedir, spidername)
        responses = []
        for (dirpath, dirnames, filenames) in os.walk(spider_root_path, topdown=True):
            if len(filenames) > 0:
                response = cache.retrieve_response_by_path(dirpath)
                response.fingerprint = os.path.basename(os.path.normpath(dirpath))  # last folder's name = fingeprint
                response.spidername = spidername
                responses += [response]
        return responses

    def print_cached_responses(self, cached_responses):
        """Format table of cache entries for console"""
        header = f"|{'{:-^15}'.format(f' Spider name ')}|{'{:-^32}'.format(f' Timestamp ')}|{'{:-^42}'.format(f' Fingerprint ')}|{'{:-^60}'.format(f' Response summary ')}|"
        print(header)
        for cache_entry in cached_responses:
            print(
                f"|{'{:^15}'.format(cache_entry.spidername)}"
                f"|{'{:^32}'.format(cache_entry.headers[b'Date'].decode())}"
                f"|{'{:^42}'.format(cache_entry.fingerprint)}"
                f"|{'{:^60}'.format(str(cache_entry))}|"
            )

    def process_list_option(args, cache):
        """Determine how cache entries should be listed by examining
           the argument (if any) passed to --list option"""
        spider_names = os.listdir(cache.cachedir)  # Cache keeps a dir for each spider
        if len(args) > 0:
            if args[0] in spider_names:  # 'scrapy cache --list spidername'
                cached_responses = self.retrieve_responses(args[0], cache)
                self.print_cached_responses(cached_responses)
            else:
                raise UsageError("The provided spidername doesn't exist")
        else:
            cached_responses = []
            for spider_name in spider_names:
                cached_responses += self.retrieve_responses(spider_name, cache)
            self.print_cached_responses(cached_responses)

    def run(self, args, opts):
        settings = self.crawler_process.settings
        settings_dict = settings._to_dict()

        if not settings_dict['HTTPCACHE_ENABLED']:
            raise UsageError("The Http-cache is disabled in settings")

        mw = HttpCacheMiddleware(settings, None)
        cache = mw.storage
        if not os.path.exists(cache.cachedir):
            print('The Http-cache is currently empty')
        elif opts.list:
            process_list_option(args, cache, spider_names)
        else:
            raise UsageError()  # Require option to be specified e.g '--list'
