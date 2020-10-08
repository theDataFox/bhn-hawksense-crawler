#!/usr/bin/env python

"""
Constructs the crawling AuditSpider class
"""
import hashlib
import os
import re
import string
from collections import Counter
from urllib.parse import urlparse

import nltk
import tldextract
import validators
from PIL import ImageFont
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.util import ngrams
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import PageItem, ImageItem, OutLinkItem, CanonicalLinkItem

nltk.download('stopwords')
nltk.download('punkt')
# define stop words
stop_list = set(stopwords.words('english'))
# define url validation
custom_cache_extract = tldextract.TLDExtract(cache_file=False)


# noinspection PyAbstractClass
class AuditSpider(CrawlSpider):
    name = "AuditSpider"

    def __init__(self, denied_paths, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowed_domains = [custom_cache_extract(self.start_urls[0]).registered_domain]
        AuditSpider.rules = [Rule(LinkExtractor(deny=denied_paths), callback='parse_item', follow=True)]
        super(AuditSpider, self)._compile_rules()

    def parse_item(self, response):
        """
        Parses the scraped page
        """

        page_item = PageItem()
        url = response.url
        domain = custom_cache_extract(response.url).registered_domain
        self.logger.info(f'Parse function called on {url}')
        # parse page
        page_item['url'] = url
        page_item['domain'] = domain
        page_item['valid_characters'] = self.parse_url(response)
        page_item['status_code'] = response.status
        page_item['redirects'] = response.request.meta.get('redirect_urls')
        page_item['title_text'], page_item['title_text_length'], page_item['title_text_pixel_width'] = self.parse_title(
            response)
        page_item['description_text'], page_item['description_text_length'], page_item[
            'description_text_pixel_width'] = self.parse_description(response)
        page_item['h1_text'], page_item['h1_text_length'] = self.parse_h1(response)
        page_item['h2_text'] = response.xpath("//h2/text()").getall()
        page_item['images'] = response.xpath("//img/@src").getall()
        page_item['external_links'], page_item['out_links'], page_item['canonical_links'] = self.parse_links(response)
        page_item['body_text'], page_item['unigrams'], page_item['bigrams'], page_item['trigrams'], page_item[
            'word_count'], page_item[
            'text_ratio'], page_item[
            'content_hash'] = self.parse_text(response)
        page_item['content_length'] = len(response.body)
        page_item['iframes'] = response.xpath("//iframe/@src").getall()
        page_item['objects'] = response.xpath("//object/@data").getall()
        page_item['embeds'] = response.xpath("//embed/@src").getall()

        # parse images
        images = response.css("img")
        for image in images:
            image_item = ImageItem()
            image_item['url'] = url
            image_item['domain'] = domain
            image_item['alt'] = image.attrib.get('alt')
            image_item['src'], image_item['file_name'] = self.parse_image_item(image)
            yield image_item

        # parse links
        # out_links and external links
        links = response.xpath("//a")
        for link in links:
            # remove # links from process
            try:
                if not link.attrib['href'].startswith(r'#'):
                    out_link_item = OutLinkItem()
                    out_link_item['url'] = url
                    out_link_item['domain'] = domain
                    out_link_item['href'], out_link_item['href_domain'], out_link_item[
                        'external'] = self.parse_out_link_item(
                        link=link, response=response)
                    yield out_link_item
            except KeyError:
                pass

        # canonical links
        canonical_links = response.xpath("//link[@rel='canonical' and @href]")
        for link in canonical_links:
            canonical_link_item = CanonicalLinkItem()
            canonical_link_item['url'] = url
            canonical_link_item['domain'] = domain
            canonical_link_item['href'], \
            canonical_link_item['self_ref'] = self.parse_canonical_link_item(link=link, response=response)
            yield canonical_link_item

        yield page_item

    @staticmethod
    def parse_url(response):
        """
        Check URL is valid and no special characters are in use
        """
        return validators.url(response.url)

    @staticmethod
    def parse_title(response):
        """
        Gather title info
        """
        title_text = response.xpath('/html/head/title/text()').get()
        title_text = title_text.strip()
        title_len = len(title_text)
        font = ImageFont.load_default()
        title_pw = font.getsize(title_text.encode('utf-8'))[0]

        return title_text, title_len, title_pw

    @staticmethod
    def parse_description(response):
        """
        Gather title info
        """
        desc = response.xpath('/html/head/meta[@name="description"]/@content').get()
        if desc:
            desc_len = len(desc)
            font = ImageFont.load_default()
            desc_pw = font.getsize(desc.encode('utf-8'))[0]
        else:
            desc_len = 0
            desc_pw = 0
        return desc, desc_len, desc_pw

    @staticmethod
    def parse_h1(response):
        """
        Gather h1 info
        """
        h1_tags = response.xpath('//h1/descendant-or-self::*/text()').getall()
        h1_text = []
        h1_len = []
        for h1 in h1_tags:
            if str.isspace(h1):
                continue
            else:
                h1_text.append(h1)
                h1_len.append(len(h1))

        return h1_tags, h1_len

    @staticmethod
    def parse_links(response):
        """
        parses the ahrefs and collects the attr of each link
        """
        links = response.xpath("//a/@href").getall()
        external_links = []
        out_links = []
        for link in links:
            # if domains are different
            if link.startswith('/') or link.startswith('#'):
                out_links.append(link)
            elif custom_cache_extract(link)[1] != custom_cache_extract(response.url)[1]:
                external_links.append(link)
            elif custom_cache_extract(link)[0] != custom_cache_extract(response.url)[0]:
                external_links.append(link)
            else:
                out_links.append(link)
        canonical_links = response.xpath("//link[@rel='canonical' and @href]/@href").getall()

        return external_links, out_links, canonical_links

    @staticmethod
    def parse_out_link_item(link, response):
        """
        parses the ahrefs and collects the attr of each link
        """

        url = response.url
        uri = urlparse(url)
        # use href here unless condition below applies
        href = link.attrib['href']
        href_domain = ''
        external = False
        if href == r'/':
            # href = homepage
            href = f'{uri.scheme}://{uri.netloc}/'
            href_domain = custom_cache_extract(url).registered_domain
            external = False
        elif href.startswith('/'):
            # create absolute
            href = f'{uri.scheme}://{uri.netloc}/{href[1:]}'
            href_domain = custom_cache_extract(url).registered_domain
            external = False
        elif custom_cache_extract(href)[1] == custom_cache_extract(url)[1]:
            href_domain = custom_cache_extract(url).registered_domain
        elif custom_cache_extract(href)[1] != custom_cache_extract(url)[1]:
            href_domain = custom_cache_extract(href).registered_domain
            external = True
        elif custom_cache_extract(href)[0] != custom_cache_extract(url)[0]:
            href_domain = custom_cache_extract(href).registered_domain
            external = True

        return href, href_domain, external

    @staticmethod
    def parse_canonical_link_item(link, response):
        """
        parses the ahrefs and collects the attr of each link
        """
        url = response.url
        href = link.attrib['href']

        # if link is rel=canonical
        if href == url:
            self_ref = True
        else:
            self_ref = False
        return href, self_ref

    @staticmethod
    def parse_image_item(image):
        """
        Get src, alt and file_name
        """
        src = image.attrib['src']
        file_name = os.path.basename(urlparse(src).path)
        return src, file_name

    @staticmethod
    def tokenize(text):
        # remove punctuation from text
        text_no_punc = text.translate(str.maketrans('', '', string.punctuation))
        # remove all non alphanumeric
        alpha = re.compile('[^a-zA-Z]')
        alpha.sub('', text_no_punc)
        # tokenise
        tokenized_sent = word_tokenize(text_no_punc.lower())
        # remove stop words
        tokenized_list = [token for token in tokenized_sent if token not in stop_list]
        return tokenized_list

    @staticmethod
    def n_grams(tokens, n):
        n_grams = Counter(ngrams(tokens, n))
        n_grams_count = dict(n_grams.most_common(10))
        n_grams_count = {k[0]: v for (k, v) in n_grams_count.items()}

        return n_grams_count

    def parse_text(self, response):
        """
        Gets body text then runs through nltk pipeline to extract NLP docs including n-grams, word count and text ratio
        """
        body_text_list = response.xpath("//*[not(self::script)]/text()").getall()
        body_text_list = [t.strip() for t in body_text_list]
        body_text = ' '.join(body_text_list).lower()
        content_hash = hashlib.sha1(body_text.encode('utf-8')).hexdigest()
        word_count = len(re.findall(r'\w+', body_text))
        token_list = self.tokenize(body_text)
        unigrams = self.n_grams(token_list, 1)
        bigrams = self.n_grams(token_list, 2)
        trigrams = self.n_grams(token_list, 3)
        text_ratio = round(word_count / len(response.body), 2)

        return body_text, unigrams, bigrams, trigrams, word_count, text_ratio, content_hash
