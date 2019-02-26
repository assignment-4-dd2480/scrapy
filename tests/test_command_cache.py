from twisted.trial import unittest
from twisted.internet import defer
from scrapy.utils.testproc import ProcessTest
from scrapy.utils.test import get_testenv
from tests import mock
from scrapy.settings import default_settings


class CacheTest(ProcessTest, unittest.TestCase):

    command = 'cache'

    @defer.inlineCallbacks
    @mock.patch('scrapy.settings.default_settings', default_settings)
    def test_list_disabled_cache(self):
        default_settings.HTTPCACHE_ENABLED = False
        _, _, err = yield self.execute(['--list'], check_code=False)
        self.assertTrue(b'The Http-cache is disabled in settings\n', err)

    @defer.inlineCallbacks
    @mock.patch('scrapy.settings.default_settings', default_settings)
    def test_list_empty_cache(self):
        default_settings.HTTPCACHE_ENABLED = True
        _, _, err = yield self.execute(['--list'], check_code=False)
        self.assertTrue(b'The Http-cache is currently empty\n', err)

    @defer.inlineCallbacks
    @mock.patch('scrapy.settings.default_settings', default_settings)
    def test_list_cache_non_existing_spider(self):
        default_settings.HTTPCACHE_ENABLED = True
        _, _, err = yield self.execute(['--list', 'testspider'], check_code=False)
        self.assertTrue(b"The provided spider name doesn't exist\n", err)
    '''
    Non-working tests
    
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

    '''
