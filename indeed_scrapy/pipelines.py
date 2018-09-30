# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# If you don't want to store the information in the localhost MongoDB Database, comment this pipeline
from pymongo import MongoClient
from scrapy.conf import settings

class MongoIndeedPipeline(object):

    def __init__(self):
        connection = MongoClient(
            settings['MONGO_SERVER'],
            settings['MONGO_PORT']
        )

        mongo_db = connection[settings['MONGO_DB']]
        self.collection = mongo_db[settings['MONGO_COLLECTION']]

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item
