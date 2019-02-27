# Report for assignment 4

## Group 13

Antonello Mondaca Tacchi, Anna Eklind, Felix Liljefors, Fredrik Flovén, Jacob Tärning

## Project

Name: Scrapy

URL: https://github.com/scrapy/scrapy

A fast high-level web crawling & scraping framework for Python. Has functionality for data mining, monitoring, and automated testing.

## Architectural overview 

Scrapy is an application framework for crawling web sites and extracting structured data which can be used for a wide range of useful applications, like data mining, information processing or historical archival.

Even though Scrapy was originally designed for web scraping, it can also be used to extract data using APIs (such as Amazon Associates Web Services) or as a general purpose web crawler.

The Scrapy project is well documented, and Scrapy's architecture is described in detail [here](https://docs.scrapy.org/en/master/topics/architecture.html). A summary is provided below:
![Architecture](https://docs.scrapy.org/en/master/_images/scrapy_architecture_02.png)
The data flow in Scrapy is controlled by the execution engine, and goes like
this:

1. The `Engine` gets the initial Requests to crawl from the `Spider`.

2. The `Engine` schedules the Requests in the `Scheduler` and asks for the next Requests to crawl.

3. The `Scheduler` returns the next Requests to the `Engine`.

4. The `Engine` sends the Requests to the `Downloader`, passing through the `Downloader Middlewares`.

5. Once the page finishes downloading the `Downloader` generates a Response (with that page) and sends it to the Engine, passing through the `Downloader Middlewares`.

6. The `Engine` receives the Response from the `Downloader` and sends it to the `Spider` for processing, passing through the `Spider Middleware`.

7. The `Spider` processes the Response and returns scraped items and new Requests (to follow) to the `Engine`, passing through the `Spider Middleware`.

8. The `Engine` sends processed items to `Item Pipelines`, then send processed Requests to the `Scheduler` and asks for possible next Requests to crawl.

9. The process repeats (from step 1) until there are no more requests from the `Scheduler`


## Selected issue

Title: provide a way to work with scrapy http cache without making requests

URL: https://github.com/scrapy/scrapy/issues/2365

Our refactoring concerns Scrapy’s `HttpCacheMiddleware` class.
The `HttpCacheMiddleware` is a type of `Downloader Middleware` (depicted in the architecture diagram above as purple rectangles between `Engine` and `Downloader`).
The http cache (if enabled) is used in steps 4-6 in the data flow description described above (section **Architectural overview**). First the request sent by a spider is stored, and later the corresponding response is stored in the "cache" as well.

The`HttpCacheMiddleware` component provides a low-level cache for HTTP requests and responses. If enabled, the cache stores every request and its corresponding response. It is configured by choosing one of multiple db-backends and also a cache policy (see [docs](https://docs.scrapy.org/en/latest/topics/downloader-middleware.html?highlight=filesystemcachestorage#module-scrapy.downloadermiddlewares.httpcache)). 

For the scope of this assignment, we've decided to focus on the default db-backend, namely the file system storage backend (implemented in the class `FilesystemCacheStorage`). If we have time left after refactoring it, we will look at refactoring the other db-backend solutions.

## Onboarding experience

We worked with Scrapy for assignment 3, so the onboarding experience was smooth for assignment 4. 

The only tool needed to install Scrapy is python’s package manager `pip` according to documentation. However, one of us had to install Visual Studio C++ build tool in order for Scrapy to work. 

**Dependencies installed for Scrapy:**
queuelib, six, w3lib, cssselect, lxml, functools32, parsel, pyasn1, pyasn1-modules, asn1crypto, enum34, ipaddress, pycparser, cffi, cryptography, attrs, service-identity, setuptools, PyHamcrest, zope.interface, idna, hyperlink, Automat, incremental, constantly, Twisted, PyDispatcher, pyOpenSSL


Most of the group members installed Scrapy in an isolated virtual environment called [virtualenv](https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv). `virtualenv` gathers all dependencies for Scrapy in a folder within our github repo. This ensures that previously installed packages won't interfere with the dependencies required for Scrapy.

The virtual environment was installed and configured as shown below:

```
pip3 install virtualenv &&
virtualenv venv &&
source venv/bin/activate &&
pip3 install --editable .
```

The last line installs the package from source in development mode, meaning that changes to the source directory will immediately affect the installed package without needing to re-install.

## Requirements
The requirements follow the [IEEE830 Software Requirements Specification](https://kth.instructure.com/courses/8227/files/1392422/download?verifier=ggm9vGGFZQ5uqTQZ6WNmKy1a2aRnElaobTXa7rSa&wrap=1), and are divided into two categories:

1. **Functional requirements:** _what_ the software system should do.
2. **Non-functional/Performance requirements:** constraints on _how_ the software system will meet functional reqs.


**Each requirement is defined by the following attributes:**
- `Title`: Unique identifier intended to improve readability when referencing other requirements.
- `Category`: Functional/Non-functional as described below.
- `Identifier`: Unique identifier in short format.
- `Requirement Description`: Concise description of what the require- ment concerns.
- `Rationale`: Motivation as to why this requirement is needed.
- `Priority`: Low/Medium/High decides the order in which requirements
are to be fulfilled.
- `Stability`: Stable/Unstable indicates whether the requirement may or may not be modified/deleted in the future. An unstable requirement may also need a more clearly defined verifiability.
- `Source`: Origin of the requirement.
- `Verifiability`: Explanation of how the requirement is to be verified. Must be possible to (1): check the requirement is in the design, (2) test that the software does implement the requirement.
- `Risk`: Outline of risk(s) associated with requirement.
- `Dependency`: Dependencies on other requirements.


### Old requirements affected by refactoring

--------

`Title:` ReadCacheEntry
`Category:` Functional
`Identifier:` OLD_1
`Requirement Description:` Allow reading individual cached Responses  by providing a `Spider` and a `Request` object as arguments to a function call (i.e `retrieve_response` in `FilesystemCacheStorage`). Return response if present in cache, or None otherwise
`Rationale:` User should be able to extract information from Scrapy cache
`Priority:` -
`Stability:` Stable
`Source:` Scrapy
`Verfiability:` Unit testing
`Risk:` Could negatively impact stored cached through file corruption
`Dependency:` OLD_2

--------

`Title`: GetPathToCache
`Category:` Functional
`Identifier:` OLD_2
`Requirement Description:` Allow reading the path to where cache stores its entries on the OS file system. The path is stored in a settings file as variable `HTTPCACHE_DIR`
`Rationale:` Needed to enable the user to reach cache entries 
`Priority:` -
`Stability:` Stable
`Source:` Scrapy
`Verfiability:` Unit testing
`Risk:` Incorrect file path yielded
`Dependency:` -

--------

`Title`: DisableExpirationLogic
`Category`: Functional
`Identifier:` OLD_3
`Requirement Description:` Allows the ability to set expiration time for cached requests in a settings file. Cached requests can be stored in a set time or indefinitely. A `FileSystemCacheStorage` object has a `settings` field which loads the value of  `HTTPCACHE_EXPIRATION_SECS` from the settings file
`Rationale:` So users may store responses indefinitely
`Priority:` -
`Stability:` Stable
`Source:` Scrapy
`Verfiability:` Unit testing
`Risk:` File system can get clogged with requests/response-files if  cache expiration is disabled
`Dependency:` -

--------
The following requirement was mentioned in issue #2365 as a part of refactoring `FilesystemCacheStorage`, the requested functionality was however already implemented in Scrapy. Thus, we made an old requirement of it. 

`Title`: DisableExpirationLogicCmdLine
`Category`: Functional
`Identifier:` OLD_4
`Requirement Description:` Allow to disable expiration logic via command line
`Rationale:` User should be able to decide how long entries are kept in the cache
`Priority:` -
`Stability:` Stable
`Source:` Issue #2365 Scrapy
`Verfiability:` Unit testing
`Risk:` File system can get clogged with requests/response-files if  cache expiration is disabled
`Dependency:` OLD_3

### New requirements

--------
`Title:` ListSpiderCacheEntriesCmdLine
`Category:` Functional
`Identifier:` NEW_1
`Requirement Description:` List all entries in cache for a specific spider from command line
`Rationale:` User should be able to get an overview of cache entries for a given spider
`Priority:` 2
`Stability:` Stable
`Source:` Issue #2365 Scrapy
`Verfiability:` Unit testing
`Risk:` Bug in existing code, feature scope too big
`Dependency:`OLD_1, OLD_2

--------

`Title:` ListCacheEntriesCmdLine
`Category:` Functional
`Identifier:` NEW_2
`Requirement Description:` List all entries in cache from command line. See [scrapy docs](https://docs.scrapy.org/en/latest/topics/downloader-middleware.html?highlight=filesystemcachestorage#filesystem-storage-backend-default) for details on cache entries.
`Rationale:` User should be able to get an overview of cache entries for all spiders
`Priority:` 1
`Stability:` Stable
`Source:` Issue #2365 Scrapy
`Verfiability:` Unit testing
`Risk:` Bug in existing code, feature scope too big
`Dependency:`OLD_1, OLD_2

--------

`Title:` ListCacheEntryByPath
`Category:` Functional
`Identifier:` NEW_3
`Requirement Description:` List a specific cache entry via function call by specifying its path in the file system
`Rationale:` User should be able to fetch a Response object stored in cache at will
`Priority:` 2
`Stability:` Stable
`Source:` Issue #2365 Scrapy
`Verfiability:` Unit testing
`Risk:` Bug in existing code, feature scope too big
`Dependency:`OLD_1, OLD_2

#### Non-functional requirements related to command line tool
--------

`Title:` ListCacheWhenDisabled
`Category:` Non-functional
`Identifier:` NEW_4
`Requirement Description:` Listing cache when caching is disabled should return correct and informative error message
`Rationale:` Clear and concise information is key when troubleshooting
`Priority:` 3
`Stability:` Stable
`Source:` Issue #2365 Scrapy
`Verfiability:` Unit testing
`Risk:` Bug in existing code, feature scope too big
`Dependency:`NEW_2

--------

`Title:` ListCacheWhenEmpty
`Category:` Non-functional
`Identifier:` NEW_5
`Requirement Description:` Listing cache when cache is empty should return correct and informative error message
`Rationale:`Clear and concise information is key when troubleshooting
`Priority:` 3
`Stability:` Stable
`Source:` Issue #2365 Scrapy
`Verfiability:` Unit testing
`Risk:` Bug in existing code, feature scope too big
`Dependency:`NEW_2

--------

`Title:` ListCacheNonExistingSpider
`Category:` Non-functional
`Identifier:` NEW_6
`Requirement Description:` Listing cache with non-existing spider name as argument should return correct and informative error message
`Rationale:`Clear and concise information is key when troubleshooting
`Priority:` 3
`Stability:` Stable
`Source:` Issue #2365 Scrapy
`Verfiability:` Unit testing
`Risk:` Bug in existing code, feature scope too big
`Dependency:`NEW_1

--------

`Title:` ListCacheExistingSpider
`Category:` Non-functional
`Identifier:` NEW_7
`Requirement Description:` Listing cache with existing spider name as argument should return a table summarizing cache entries belonging to spider
`Rationale:`Helps user find key information 
`Priority:` 3
`Stability:` Stable
`Source:` Issue #2365 Scrapy
`Verfiability:` Unit testing
`Risk:` Bug in existing code, feature scope too big
`Dependency:`NEW_1

--------

`Title:` ListCacheNoExtraArgument
`Category:` Non-functional
`Identifier:` NEW_8
`Requirement Description:` Listing cache with no argument provided should return a table summarising all cache entries
`Rationale:`Gives users an overview of cached spiders 
`Priority:` 3
`Stability:` Stable
`Source:` Issue #2365 Scrapy
`Verfiability:` Unit testing
`Risk:` Bug in existing code, feature scope too big
`Dependency:`NEW_2

#### Non-functional requirements related to retrieving Response objects from cache via function calls

--------

`Title:` RetrieveExistingCachedResponse
`Category:` Non-functional
`Identifier:` NEW_9
`Requirement Description:` Attempting to retrieve an existing cached response by calling `retrieve_response_by_path(dirpath)` should return corresponding Response object
`Rationale:`A direct request for a specific cache entry should not return a different item 
`Priority:` 3
`Stability:` Stable
`Source:` Issue #2365 Scrapy
`Verfiability:` Unit testing
`Risk:` Bug in existing code, feature scope too big, incorrect file retrieval causing confusion
`Dependency:` NEW_3

--------

`Title:` RetrieveNonExistingCachedResponse
`Category:` Non-functional
`Identifier:` NEW_10
`Requirement Description:` Attempting to retrieve a non-existing cached response by calling `retrieve_response_by_path(dirpath)` should return None
`Rationale:` If no entry exists then the returned value should reflect that 
`Priority:` 3
`Stability:` Stable
`Source:` Issue #2365 Scrapy
`Verfiability:` Unit testing
`Risk:` Bug in existing code, feature scope too big
`Dependency:`NEW_3

## Tests

### Existing test cases relating to refactored code

The tests cover the requirements ReadCacheEntry, GetPathToCache and DisableExpirationLogic, containing good assertions and examining the core features of FilesystemCacheStorage. Following tests can be found in `test_downloadermiddleware_httpcache.py`. 

`test_dont_cache:` Sets the field dont_cache to true/false, makes sure that None/a response is returned when trying to retrieve the given response. 

The assertions are good, covering the requirement ReadCacheEntry and GetPathToCache since the former is dependent on the latter. 

`test_storage`: Stores the given response in the cache, waits for the cache to expire, then tries to retrieve the given response.

Good assertions, covering the requirements ReadCacheEntry and GetPathToCache. The requirement DisableExpirationLogic is also covered, HTTPCACHE_EXPIRATION_SECS is set to 1, the response is stored in the cache, when 2 seconds have passed the assertion makes sure that the entry is no longer available since the cache has expired. 

`test_storage_never_expire`: Sets the field HTTPCACHE_EXPIRATION_SECS to 0, stores the given response in the cache, gives a chance for the entry in the cache to expire, then tries to retrieve the given response. 

The test covers ReadCacheEntry, GetPathToCache and DisableExpirationLogic. The assertion consists of checking whether a Response is retrieved from the cache after 0.5 seconds, thus disabling of the expiration logic is examined.
 
`test_middleware_ignore_schemes:` Examines the following. 
- http responses are cached by default
- file response is not cached by default
- s3 scheme repsonse is cached by default
- s3 scheme is ignored

The main focus of the test is not to examine the requirements ReadCacheEntry and GetPathToCache, they are however covered when "file response is not cached by default" and "s3 scheme is ignored" are tested. The assertions make sure that the cache returns None when a entry is requested. 


`test_middleware_ignore_http_codes:` Makes sure that a response of a request with given http code is cached/not cached.
 
ReadCacheEntry and GetPathToCache are covered, the assertion makes sure that a request with given http code is not cached. 

`test_request_cacheability:` Examines the following.
- corresponding response for a request with "no-store" header is not cached
- corresponding response for a request without "no-store" header is cached

ReadCacheEntry and GetPathToCache are covered, the assertion makes sure that a request with "no-store" header is not cached.

`test_response_cacheability:` Examines a number of responses, caches unconditionally unless a response contains a "no-store" header or is a 304.

ReadCacheEntry and GetPathToCache are covered, the assertions make sure that a response is cached/not cached if it contains "no-store" or is a 304. 

#### Branch coverage of existing tests
Following images show the branch coverage of `httpcache.py` in the extensions folder where `FilesystemCacheStorage` can be found. The branch coverage of the whole class was 94%. 

![](https://i.imgur.com/sbgHetA.png)
![](https://i.imgur.com/OHqiyJO.png)




### New test cases relating to refactored code
The requirements are listed above in the section **Requirements**. Our plan for testing these requirements is as follows:

#### Tests for cache command functionality

- [x] `test_list_disabled_cache`: When invoking the scrapy command line tool with the `cache` command and the cache is disabled, appropriate error message is returned. The test covers the non-functional requirement ListCacheWhenDisabled.

- [ ] `test_list_cache_entries`: When invoking the scrapy command line tool with the `cache` command and option `--list`, all entries of the httpcache are listed. The test covers the non-functional requirement ListCacheNoExtraArgument.

- [x] `test_list_empty_cache`: When invoking the scrapy command line tool with the `cache` command and option `--list` while the cache is empty, appropriate error message is returned. The test covers the non-functional requirement ListCacheWhenEmpty.

- [ ] `test_list_cache_existing_spider`: When invoking the scrapy command line tool with the `cache` command, option `--list` and an existing spider name as first and only argument, all entries of that spiders httpcaches are listed. The test covers the non-functional the requirement ListCacheExistingSpider.

- [x] `test_list_cache_non_existing_spider`: When invoking the scrapy command line tool with the `cache` command, option `--list` and a non-existing spider name as the first and only argument, appropriate error message is returned. The test covers the non-functional the requirement ListCacheNonExistingSpider.

- [ ] `test_list_cache_multiple_existing_spiders`: When invoking the scrapy command line tool with the `cache` command, option `--list` and multiple existing spider names as arguments, all entries of those spiders httpcaches are listed. 

- [ ] `test_list_cache_multiple_existing_and_non_existing_spiders`: When invoking the scrapy command line tool with the `cache` command, option `--list` and multiple existing spider names as well as non existing spider names as arguments, all entries of the existing spiders httpcaches are listed. 

#### Tests for cache command methods

- [ ] `test_retrieve_responses`: When invoking the method `test_retrieve_responses`, it should return responses from given spider name and cache. The test covers the non-functional requirement RetrieveExistingCachedResponse.

- [ ] `test_print_cached_responses`: When invoking the method `test_print_cached_responses`, it should print retrieved cached responses in a nice format. 

- [ ] `test_process_list_option`: When invoking the method `test_process_list_option`, it should print responses depending on amount of arguments. The test covers the non-functional requirements ListCacheNonExistingSpider, ListCacheExistingSpider, ListCacheNoExtraArgument, RetrieveExistingCachedResponse and RetrieveNonExistingCachedResponse.  

#### Tests for FilesystemCacheStorage methods

- [x] `test_retrieve_response_by_path`: When invoking the refactored method `retrieve_response_by_path` of `FilesystemCacheStorage` it should yield the object specified in the file path given as an argument. The test covers the non-functional requirement RetrieveExistingCachedResponse. 

- [x] `test_path_not_existing`: When invoking the refactored method `retrieve_response_by_path` of `FilesystemCacheStorage` it should yield `None` if the path given as an argument is non-existent. The test covers the non-functional requirement RetrieveNonExistingCachedResponse. 

## The refactoring carried out

### Original
![Original Class UML for response retrieval](https://i.imgur.com/u4p61Ji.png)
Figure 1. Original Class UML for response retrieval

![Original implementation of response retrieval](https://i.imgur.com/E7iYfqM.png)
Figure 2. Original implementation of response retrieval

### New
![Class UML for response retrieval by command line](https://i.imgur.com/snISvil.png)
Figure 3. Class UML for new response retrieval functionality through command line

![Implementation after refactoring of response retrieval](https://i.imgur.com/pf1mkiQ.png)
Figure 4. Implementation after refactoring of response retrieval

![New command logic for cache retrieval](https://i.imgur.com/IXLdD5x.png)

Figure 5. New command logic for cache retrieval

## Test logs

_Overall results with link to a copy of the logs (before/after refactoring)._

_The refactoring itself is documented by the git log._

**Before**: Test log of master branch before our edits: https://travis-ci.org/scrapy/scrapy/jobs/496023267

**After**: The build fails, but not due to the tests we added, there are no probelms with  `test_downloadermiddleware_httpcache.py` and `test_command_cache.py`. Specifically, there are two tests methods that fail in the test suite `tests/test_crawl.py`, although we haven't edited this file. This could be due to flaky tests written by previous developers, or an unforseen side-effect introduced by our new code/tests. Our suspicion is that the failing tests methods in `tests/test_crawl.py` fail due to simulated delays (in the test-cases) which causes inconsistent runtime behavior.

Another issue we've had is that Scrapy is built for 9 different versions of Python. This has slowed down the Travis build-time during development. Futhermore, our edits pass for some versions of Python and fail for others.

Test log of master branch after our edits:
https://travis-ci.com/assignment-4-dd2480/scrapy/jobs/180675331

The build however passes for Python 3.6:
https://travis-ci.com/assignment-4-dd2480/scrapy/jobs/180675332


## Changes to test suite
### Added/modified: 

Tests for `retrieve_response_by_path` with both valid and invalid file paths, have been added in `test_downloadermiddleware_httpcache.py` under the class `FilesystemStorageTest`. 

A new test class has been created `CacheTest`, which can be found in `test_command_cache.py`, containing working tests examining the listing of entries in the cache when:
- the cache is disabled
- the cache is empty
- a non-existing spider is used as an argument

See the marked boxes in section *New test cases relating to refactored code* for an overview.

### Left to do: 
See the unmarked boxes in section *New test cases relating to refactored code*.

## Patch
We have created a patch according to [Scrapy's guidlines for writting patches](https://docs.scrapy.org/en/master/contributing.html#writing-patches). 
- [x] Minimum amount of code
- [x] pass all unit-tests
- [x] include minimum one test case that test new functionality
- [x] include documentation

## Effort spent

For each team member, how much time was spent in

| Name | Anna | Antonello | Felix | Fredrik | Jacob |
|----- | ---- | --------- | ----- | ------- | ----- |
|**Meetings** | 6 hours | 6 hours | 6 hours | 6 hours | 6 hours |
|**Discussion**| 6 hours | 5 hours | 5 hours | 4 hours | 5 hours |
|**Reading documentation**| 4 hours | 4 hours | 6 hours | 6 hours | 3 hours |
|**Configuration**| 0 hours | 3 hours | 3 hours | 3 hours | 4 hours |
|**Analyzing code/output**| 8 hours | 5 hours | 8 hours | 3 hours | 5 hours |
|**Writing docs**| 8 hours | 2 hours | 2 hours | 5 hours | 3 hours |
|**Writing code**| 0 hours | 5 hours | 8 hours | 2 hours | 5 hours |
|**Running code**| 1 hours | 2 hours | 2 hours | 1 hours | 2 hours |

## Overall experience

#### **What are your main take-aways from this project?**
Issues can **easily** be interpreted in multiple ways unless the problem (and its sought after change) is clearly defined.

#### **What did you learn?**
Refactoring and relating requirements to tests. 

Jacob & Antonello learned about Python `**args` and `**kwargs`.

#### **Is there something special you want to mention here?**
Having students search for open refactoring issues on open source projects was a bad call, and should be changed for the next year. The search for such a specific issue was time-consuming, unrewarding and bothersome.

Perhaps an alternative solution could be for the teachers to select a few open source projects that are well suited for this assignment. Then each student group can choose one of these, and refactor it in a private repo. That way, the TA:s will be well acquainted with the projects before examination, and the students can focus more on refactoring and less on finding a suitable issue.

From Wikipedia: 
> "Code refactoring is the process of restructuring existing computer code **without changing** its external behavior." 

From Pass criteria 2: 
> "The **changes affect the code and/or functionality** of the software". 

The course specifications should refrain from acting as a client with conflicting goals. 

