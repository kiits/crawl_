# -*- coding: utf-8 -*-
import scrapy

from scrapy_splash import SplashRequest
from scrapy.loader import ItemLoader
from home.items import HomeItem


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    start_urls = [
            'https://tj.lianjia.com/ershoufang/nankai/pg1/',
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse,
                                args={'wait': '0.5', 'images': 0})

    def parse(self, response):
        task = ItemLoader(item=HomeItem(), response=response)
        price = response.xpath(
                '/html/body/div[4]/div[1]/ul/li/div[1]/div[6]/div[2]/span/text()'
                ).re('\d+')
        task.add_xpath('price', price)
        # /html/body/div[4]/div[1]/ul/li[2]/div[1]/div[6]/div[2]/span
        # /html/body/div[4]/div[1]/ul/li[1]/div[1]/div[6]/div[2]/span
        next_page = response.xpath(
                    '/html/body/div[4]/div[1]/div[8]/div[2]/div/a[last()]/@href'
                    ).extract_first()
        if next_page and next_page != '/ershoufang/nankai/pg6/':
            yield SplashRequest('https://tj.lianjia.com' + next_page,
                                self.parse,
                                args={'wait': '0.5', 'images': 0})
        yield task.load_item()
