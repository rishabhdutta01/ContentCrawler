# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from sqlalchemy.orm import sessionmaker
from newscrawler.models import Article, db_connect, create_table
from logging import info
from scrapy.exceptions import DropItem
from .models import Article


class DuplicatesPipeline(object):

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates tables.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
        info("***** DuplicatesPipeline: database connected *****")

    def process_item(self, item, spider):
        session = self.Session()
        exist_id = session.query(Article.id).filter_by(id = item["id"]).first()
        if exist_id is not None:  # the current id exists
            raise DropItem("Duplicate item found: %s" % item["id"])
            session.close()
        else:
            return item
            session.close()


class NewscrawlerPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)


    def process_item(self, item, spider):
        """Save quotes in the database
        This method is called for every item pipeline component
        """
        session = self.Session()
        article = Article()
        article.id = item["id"]
        article.date = item["date"]
        article.title = item["title"]
        article.content = item["content"]
        article.location = item["location"]
        article.author = item["author"]
        article.url = item["url"]

        try:
            session.add(article)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item
