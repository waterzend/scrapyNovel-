# -*- coding: utf-8 -*-
import scrapy
import re


class DuFeiSpider(scrapy.Spider):
    name = "天才小毒妃"
    start_urls = ["http://www.diwangyanxiaoshuo.com/tiancaixiaodufei/140459.html"]

    def parse(self, response):
        title = response.xpath('//h1/text()').extract()
        page = response.xpath('//div[@class="m-tpage"]//a/@href').extract()
        content = response.xpath('//*[@id="content"]').extract()
        next_page = page[1]
        pattern = re.compile('[0-9]+')
        match = pattern.findall(next_page)
        id = pattern.findall(title[0])[0]
        yield {'id': id, 'title': title[0], 'content': content[0]}
        # 有下一页继续
        if match:
            yield response.follow(next_page, self.parse)
