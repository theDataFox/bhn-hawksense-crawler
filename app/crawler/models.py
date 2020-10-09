#!/usr/bin/env python

"""
Constructs the database models for postgres for the spider to connect to
"""

from scrapy.utils.project import get_project_settings
from sqlalchemy import create_engine, Column, Text, Integer, Boolean, ARRAY, REAL, JSON, DateTime, func
from sqlalchemy.engine import url
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def connect_to_db():
    """
    Returns sqlalchemy engine instance.
    """
    conn_settings = get_project_settings().get("DATABASE")
    return create_engine(url.URL(**conn_settings))


def create_table(engine):
    """Constructing a base class for declarative class definitions (ORM)."""
    Base.metadata.create_all(engine)


class Page(Base):
    """Sqlalchemy model"""
    __tablename__ = "page"
    __table_args__ = {"schema": "crawl"}

    # setting up the table definition
    id = Column('id', Integer, primary_key=True, nullable=False)
    date_created = Column('date_created', DateTime(timezone=True), server_default=func.now())
    url = Column('url', Text)
    domain = Column('domain', Text)
    valid_characters = Column('valid_characters', Boolean)
    status_code = Column('status_code', Integer)
    redirects = Column('redirects', ARRAY(Text))
    title_text = Column('title_text', Text)
    title_text_length = Column('title_text_length', Integer)
    title_text_pixel_width = Column('title_text_pixel_width', Integer)
    description_text = Column('description_text', Text)
    description_text_length = Column('description_text_length', Integer)
    description_text_pixel_width = Column('description_text_pixel_width', Integer)
    h1_text = Column('h1_text', ARRAY(Text))  # could potentially be multiple
    h1_text_length = Column('h1_text_length', ARRAY(Integer))
    h2_text = Column('h2_text', ARRAY(Text))
    images = Column('images', ARRAY(Text))
    out_links = Column('out_links', ARRAY(Text))
    external_links = Column('external_links', ARRAY(Text))
    canonical_links = Column('canonical_links', ARRAY(Text))
    body_text = Column('body_text', Text)
    unigrams = Column('unigrams', JSON)
    bigrams = Column('bigrams', JSON)
    trigrams = Column('trigrams', JSON)
    content_hash = Column('content_hash', Text)
    content_length = Column('content_length', Integer)
    word_count = Column('word_count', Integer)
    text_ratio = Column('text_ratio', REAL)
    iframes = Column('iframe_list', ARRAY(Text))
    objects = Column('object_list', ARRAY(Text))
    embeds = Column('embed_list', ARRAY(Text))


class Image(Base):
    """Sqlalchemy model"""
    __tablename__ = "images"
    __table_args__ = {"schema": "crawl"}

    # setting up the table definition
    id = Column('id', Integer, primary_key=True, nullable=False)
    date_created = Column('date_created', DateTime(timezone=True), server_default=func.now())
    src = Column('src', Text)
    alt = Column('alt', Text)
    file_name = Column('file_name', Text)
    url = Column('url', Text)
    domain = Column('domain', Text)


class OutLink(Base):
    """Sqlalchemy model"""
    __tablename__ = "out_links"
    __table_args__ = {"schema": "crawl"}

    # setting up the table definition
    id = Column('id', Integer, primary_key=True, nullable=False)
    date_created = Column('date_created', DateTime(timezone=True), server_default=func.now())
    href = Column('href', Text)
    href_status_code = Column('status_code', Integer)  # todo: check the external links status
    href_domain = Column('href_domain', Text)
    url = Column('url', Text)
    domain = Column('domain', Text)
    external = Column('external', Boolean)  # external or out_link within same domain


class CanonicalLink(Base):
    """Sqlalchemy model"""
    __tablename__ = "canonical_links"
    __table_args__ = {"schema": "crawl"}

    # setting up the table definition
    id = Column('id', Integer, primary_key=True, nullable=False)
    date_created = Column('date_created', DateTime(timezone=True), server_default=func.now())
    href = Column('href', Text)
    url = Column('url', Text)
    domain = Column('domain', Text)
    self_ref = Column('self_ref', Boolean)  # self-referencing or canonicalised


# class Phrase(Base):
#     """Sqlalchemy model"""
#     __tablename__ = "seo_phrases"
#     __table_args__ = {"schema": "crawl"}
#
#     # setting up the table definition
#     id = Column('id', Integer, primary_key=True, nullable=False)
#     phrase = Column('phrase', Text)
#     count = Column('count', Text)
#     url = Column('url', Text)
#     domain = Column('domain', Text)
#     external = Column('external', CHAR)  # unigram, bigram or trigram


class InLink(Base):
    """Sqlalchemy model"""
    __tablename__ = "in_links"
    __table_args__ = {"schema": "crawl"}

    # setting up the table definition
    id = Column('id', Integer, primary_key=True, nullable=False)
    date_created = Column('date_created', DateTime(timezone=True), server_default=func.now())
    url = Column('url', Text)
    in_link = Column('in_link', Text)
