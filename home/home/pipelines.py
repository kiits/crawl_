# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class HomePipeline(object):

    def __init__(self):
        self.prices = []
        self.num = 0

    def close_spider(self, spider):
        """
        This method is called when the spider is closed.
        """
        print('''\n
            ******************************************************************\n
            输出结果：|平米均价%s|总房源数%s|\n
            ******************************************************************\n
            ''' % (sum(self.prices)/self.num, self.num))

    def process_item(self, item, spider):
        """
        处理Items
        """
        self.prices = self.prices + list(map(lambda x: float(x), item['price']))
        self.num = self.num + len(item['price'])
        return item
