# You'll need the below modules to create your spider:
# Replace "SpiderNameItem" with the class name in your items.py.
from collections import Counter, defaultdict

import tldextract
from loguru import logger
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


custom_cache_extract = tldextract.TLDExtract(cache_file=False)

# todo: these attributes need to be put into another class the spider needs to yield them using scrapy.Items()


class AuditSpider(CrawlSpider):
    name = "AuditSpider"
    rules = [Rule(LinkExtractor(), callback='analyze_page', follow=True)]

    def __init__(self, base_url, sitemap, branding, **kwargs):
        self.start_urls = [base_url]
        self.allowed_domains = [custom_cache_extract(self.base_url).registered_domain]
        super().__init__(**kwargs)
        self.text_ratio = {}
        self.word_count = {}
        self.embedded = {}
        self.objects = {}
        self.iframes = {}
        self.url_validation_urls = {}
        self.branding = branding
        self.domain = ''
        self.base_url = base_url
        self.sitemap = sitemap
        self.crawled_pages = []
        self.crawled_urls = set([])
        self.page_queue = []
        self.wordcount = Counter()
        self.bigrams = Counter()
        self.trigrams = Counter()
        self.content_hashes = defaultdict(set)
        self.h1_tags = {}
        self.h2_tags = {}
        self.out_links = {}
        self.external_links = {}
        self.canonical_links = {}
        self.titles = {}
        self.descriptions = {}
        self.redirects = {}
        self.images = {}
        self.statuses = {}
        self.keywords = {}

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.analyze_response(), dont_filter=True)

    def analyze_response(self, response, base_url, branding):
        """
        Runs the page analysis and builds the page queue and crawled pages list

        :return:
        """
        # analyze each page
        page = Page(response=response, base_url=base_url, branding=branding)

        # run page analysis
        page.analyze()

        # content hash
        self.content_hashes[page.content_hash].add(page.url)

        # word, bigrams and trigrams
        for w in page.word_counter:
            self.wordcount[w] += page.word_counter[w]

        for b in page.bigrams:
            self.bigrams[b] += page.bigrams[b]

        for t in page.trigrams:
            self.trigrams[t] += page.trigrams[t]

        # add links to crawled urls and page queue, collect audit report info
        self.crawled_urls.add(page.url)
        self.out_links[page.url] = page.out_links
        self.external_links[page.url] = page.external_links
        self.canonical_links[page.url] = page.canonical_links
        self.redirects[page.url] = page.redirect_uri
        self.h1_tags[page.url] = page.h1_tags
        self.h2_tags[page.url] = page.h2_tags
        self.descriptions[page.url] = page.description
        self.titles[page.url] = page.title
        self.images[page.url] = page.img_tags
        self.word_count[page.url] = page.word_count
        self.text_ratio[page.url] = page.text_ratio
        self.url_validation_urls[page.url] = page.url_validation
        self.objects[page.url] = page.objects
        self.iframes[page.url] = page.iframes
        self.embedded[page.url] = page.embedded
        self.statuses[page.url] = page.status_code
        self.keywords[page.url] = page.keywords
        filename = 'page-%s.txt' % response
        with open(filename, 'wb') as f:
            f.write(response.text)
        logger.info(f'Saved file: {filename}')
