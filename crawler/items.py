#!/usr/bin/env python

"""
Constructs item classes for definitions in the crawl spider
"""
from scrapy import Field, Item


class PageItem(Item):
    url = Field()
    domain = Field()
    valid_characters = Field()
    status_code = Field()
    redirects = Field()
    title_text = Field()
    title_text_length = Field()
    title_text_pixel_width = Field()
    description_text = Field()
    description_text_length = Field()
    description_text_pixel_width = Field()
    h1_text = Field()
    h1_text_length = Field()
    h2_text = Field()
    images = Field()
    out_links = Field()
    external_links = Field()
    canonical_links = Field()
    body_text = Field()
    unigrams = Field()
    bigrams = Field()
    trigrams = Field()
    word_count = Field()
    text_ratio = Field()
    content_hash = Field()
    content_length = Field()
    iframes = Field()
    objects = Field()
    embeds = Field()


class ImageItem(Item):
    src = Field()
    alt = Field()
    file_name = Field()
    url = Field()
    domain = Field()


class OutLinkItem(Item):
    url = Field()
    domain = Field()
    href = Field()
    href_domain = Field()
    external = Field()


class CanonicalLinkItem(Item):
    url = Field()
    domain = Field()
    href = Field()
    self_ref = Field()


class PhraseItem(Item):
    url = Field()
    domain = Field()
    phrase = Field()
    count = Field()
    type = Field()
