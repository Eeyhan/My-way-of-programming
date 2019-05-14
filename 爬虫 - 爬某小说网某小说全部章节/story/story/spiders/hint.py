# -*- coding: utf-8 -*-
import scrapy
from story.items import StoryItem

class HintSpider(scrapy.Spider):
    name = 'hint'
    allowed_domains = ['www.shizongzui.cc']
    start_urls = ['http://www.shizongzui.cc/anshi/']

    def parse_detail(self,response):
        item = response.meta['item']
        content_list = response.xpath('//div[@class="bookcontent clearfix"]/text()').extract()
        content = ''
        for i in content_list:
            content += i.replace('\u3000','')

        item['content'] = content
        yield item

    def parse(self, response):

        detail_list = response.xpath('//div[@class="booklist clearfix"]/span/a')
        for span in detail_list:
            item = StoryItem()
            title = span.xpath('./text()').extract_first()
            url = span.xpath('./@href').extract_first()
            item['title'] = title
            item['url'] = url
            yield scrapy.Request(url=url,callback=self.parse_detail,meta={'item':item})