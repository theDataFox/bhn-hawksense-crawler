# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PageItem(scrapy.Item):
    # define the fields for your item here like:
    embedded = {}
    objects = {}
    iframes = {}
    h1_tags = {}
    h2_tags = {}
    out_links = {}
    external_links = {}
    canonical_links = {}
    titles = {}
    descriptions = {}
    redirects = {}
    images = {}

