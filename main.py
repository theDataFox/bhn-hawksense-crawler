#!/usr/bin/env python

"""
Main entry point into scrapy program
"""

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from sqlalchemy import MetaData

from crawler.spiders.auditspider import AuditSpider

# InLink, OutLink

metadata = MetaData()

# begin scrapy process
process = CrawlerProcess(get_project_settings())
process.crawl(crawler_or_spidercls=AuditSpider, start_urls=['https://www.fashionchoicecard.co.uk'])
process.start()  # the script will block here until the crawling is complete

# after scrapy has populated tables create inlinks data
# engine = connect_to_db()
# create_table(engine)
#
# # create session
# Session = sessionmaker(bind=engine)
# session = Session()
#
# in_link = InLink()
# try:
#     session.add(in_link)
#     session.commit()
# except exc.SQLAlchemyError:
#     session.rollback()
#     raise
# finally:
#     session.close()
#
# # create inlinks query
# in_links_result = session.query(OutLink.url, func.count(OutLink.href)).group_by(OutLink.url).all()
#
# # insert values
# in_links_table = metadata.tables['in_links']
# in_links_table.insert().from_select(names=['url', 'in_link'], select=in_links_result)

# check if table inlinks exists otherwise create
