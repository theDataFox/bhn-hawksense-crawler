#!/usr/bin/env python

"""
Main entry point into scrapy program
"""
from sqlalchemy import exc, MetaData
from sqlalchemy.orm import sessionmaker, aliased

from crawler.models import connect_to_db, InLink, OutLink

# begin scrapy process
# process = CrawlerProcess(get_project_settings())
# process.crawl(crawler_or_spidercls=AuditSpider, start_urls=['https://www.fashionchoicecard.co.uk'])
# process.start()  # the script will block here until the crawling is complete

# after scrapy has populated tables create inlinks data
engine = connect_to_db()
metadata = MetaData(bind=engine)
# print(engine.table_names(schema='crawl'))

# create session
Session = sessionmaker(bind=engine)
session = Session()

try:
    in_t1 = InLink()
    session.add(in_t1)
    out_t1 = aliased(OutLink)
    out_t2 = aliased(OutLink)
    # create inlinks query
    in_links_result = session.query(out_t2.href.label('in_link'),
                                    out_t2.url).join(out_t1, out_t2.url == out_t1.href).filter(
        out_t2.external.is_(False))
    # insert values

    # session.add(insert_data)
    # in_t1.insert().from_select(names=['url', 'in_link'], select=in_links_result)
    session.commit()
except exc.SQLAlchemyError:
    session.rollback()
    raise
finally:
    session.close()
#
# select t2.href inlink, t2.url
#
# from out_links t1
# inner join out_links t2 on t1.href = t2.url
#
# where t1.url = 'https://www.fashionchoicecard.co.uk/faqs/balance-and-validity'
# and t2.external = FALSE


# for page_url, out_link_list in site.out_links.items():
#            # each value is a list of values ie. ['outlink1', 'outlink2', etc.]
#            if page.url != page_url:
#                for out_link in out_link_list:
#                    if page.url == out_link:
#                        page.in_links.append(page_url)
#        page.unique_in_links = list(set(page.in_links))


# check if table inlinks exists otherwise create
