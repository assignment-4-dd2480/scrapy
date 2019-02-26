import os
from twisted.trial import unittest
from twisted.internet import defer
import scrapy
import sys
from scrapy.utils.testsite import SiteTest
from scrapy.utils.testproc import ProcessTest
import test_downloadermiddleware_httpcache




class CacheTest(ProcessTest, SiteTest, unittest.TestCase, _BaseTest):
    command = 'cache'
    self.storage_class = 'scrapy.extensions.httpcache.FileSystemCacheStorage'
    #will not work if cache is actually empty
    @defer.inlineCallbacks
    def test_cacheNotEmpty(self):
        _,out,_ = yield self.execute(['--list'])
        self.assertNotEqual(b'The Http-cache is currently empty\n', out)

    
    @defer.inlineCallbacks
    def test_new_command(self):
        self.command = 'version'
        encoding = getattr(sys.stdout, 'encoding') or 'utf-8'
        _, out, _ = yield self.execute([])
        self.assertEqual(
            out.strip().decode(encoding),
            "Scrapy %s" % scrapy.__version__,
        )

    @defer.inlineCallbacks
    def test_create_remove(self):
        self.command = 'genspider'
        self.spider_name = 'spooderman'
        if not os.path.exists(self.spider_name + ".py"):
            _,out,_ = yield self.execute([self.spider_name, "www.google.com"])
        if os.path.exists(self.spider_name + ".py"):
            pass
            #os.remove(self.spider_name + ".py")

        self.command = 'runspider'
        _,out,_ = yield  self.execute([self.spider_name])

    @defer.inlineCallbacks
    def test_cache_by_spider_name(self):
        self.command = 'cache'
        self.spider_name = 'spooderman'
        spiderNameIndex = 6
        _,out,_ = yield  self.execute(['--list', self.spider_name, ])
        list = [x.strip(' ') for x in out.decode("utf-8").split("|")]
        print(list)
        self.assertEqual(self.spider_name, list[spiderNameIndex])


    def test_storage(self):
        with self._storage() as storage:
            request2 = self.request.copy()
            assert storage.retrieve_response(self.spider, request2) is None

            storage.store_response(self.spider, self.request, self.response)
            response2 = storage.retrieve_response(self.spider, request2)
            assert isinstance(response2, HtmlResponse)  # content-type header
            self.assertEqualResponse(self.response, response2)

            time.sleep(2)  # wait for cache to expire
            assert storage.retrieve_response(self.spider, request2) is None

