#!/usr/bin/env python

"""
Create pipeline classes for the spider to send the data to once it has been parsed
"""
import logging

from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker

from .items import ImageItem, PageItem, CanonicalLinkItem, OutLinkItem
from .models import connect_to_db, create_table, Page, Image, OutLink, CanonicalLink


class BasePipeline:
    def __init__(self):
        """
        Initializes database connection and sessionmaker for all sub classes
        """
        engine = connect_to_db()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def commit_to_db(self, table_instance):
        # create db session instance
        session = self.Session()
        try:
            session.add(table_instance)
            session.commit()
        except exc.SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()


class DBPipeline(BasePipeline):
    def __init__(self):
        super(DBPipeline, self).__init__()

    def process_item(self, item, spider):
        """Save info in the database.

        This method is called for every item pipeline component.

        """
        if isinstance(item, PageItem):
            logging.info(f'Item is a page')

            # create table instance
            page = Page()

            # assign page items
            page.url = item["url"]
            page.domain = item["domain"]
            page.valid_characters = item["valid_characters"]
            page.status_code = item["status_code"]
            page.redirects = item["redirects"]
            page.title_text = item["title_text"]
            page.title_text_length = item["title_text_length"]
            page.title_text_pixel_width = item["title_text_pixel_width"]
            page.description_text = item["description_text"]
            page.description_text_length = item["description_text_length"]
            page.description_text_pixel_width = item["description_text_pixel_width"]
            page.h1_text = item["h1_text"]
            page.h1_text_length = item["h1_text_length"]
            page.h2_text = item["h2_text"]
            page.images = item["images"]
            page.out_links = item["out_links"]
            page.external_links = item["external_links"]
            page.canonical_links = item["canonical_links"]
            page.body_text = item["body_text"]
            page.unigrams = item["unigrams"]
            page.bigrams = item["bigrams"]
            page.trigrams = item["trigrams"]
            page.word_count = item["word_count"]
            page.text_ratio = item["text_ratio"]
            page.content_hash = item["content_hash"]
            page.content_length = item["content_length"]
            page.iframes = item["iframes"]
            page.objects = item["objects"]
            page.embeds = item["embeds"]

            # commit item to db
            self.commit_to_db(table_instance=page)

            return item

        if isinstance(item, ImageItem):
            logging.info(f'Item is an image')
            # create table instance
            image = Image()

            # assign page items
            image.src = item["src"]
            image.alt = item["alt"]
            image.file_name = item["file_name"]
            image.url = item["url"]
            image.domain = item["domain"]

            # commit item to db
            self.commit_to_db(table_instance=image)

            return item

        if isinstance(item, OutLinkItem):
            # create table instance
            out_link = OutLink()

            # assign link items
            out_link.href = item["href"]
            out_link.href_domain = item["href_domain"]
            # out_link.href_status_code
            out_link.url = item["url"]
            out_link.domain = item["domain"]
            out_link.external = item["external"]

            # commit item to db
            self.commit_to_db(table_instance=out_link)

            return item

        if isinstance(item, CanonicalLinkItem):
            # create table instance
            canonical_link = CanonicalLink()

            # assign link items
            canonical_link.url = item["url"]
            canonical_link.domain = item["domain"]
            canonical_link.href = item["href"]
            canonical_link.self_ref = item["self_ref"]

            # commit item to db
            self.commit_to_db(table_instance=canonical_link)

            return item
