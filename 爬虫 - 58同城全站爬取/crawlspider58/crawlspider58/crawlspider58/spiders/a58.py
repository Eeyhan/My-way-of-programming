# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from crawlspider58.items import Crawlspider58Item
from scrapy_redis.spiders import RedisCrawlSpider

class A58Spider(RedisCrawlSpider):
    name = '58'
    # allowed_domains = ['bj.58.com/chuzu']
    # start_urls = ['http://bj.58.com/chuzu/']

    redis_key = 'bj58'
    rules = (
        Rule(LinkExtractor(allow=r'https://bj.58.com/chuzu/pn\d+'), callback='parse_item', follow=True),
    )

    # 租房详情页请求
    def parse_detail(self,response):
        item = response.meta['item']

        # 价格
        price = response.xpath('//b[@class="f36 strongbox"]/text()').extract_first() + '元/月'
        # 付款方式
        payment = response.xpath('//div[@class="house-pay-way f16"]/span[2]/text()').extract_first()
        # 租赁方式
        method = response.xpath('//ul[@class="f14"]/li[1]/span[2]/text()').extract_first()
        # 租房类型
        house_type = response.xpath('//ul[@class="f14"]/li[2]/span[2]/text()').extract_first().replace(' ','')
        # 小区
        community = response.xpath('//ul[@class="f14"]/li[4]/span[2]/a/text()').extract_first()
        # 区域
        area = response.xpath('//ul[@class="f14"]/li[5]/span[2]/a/text()').extract()
        # 详细地址
        address= response.xpath('//span[@class="dz"]/text()').extract_first().strip()
        # 联系电话
        telphone = response.xpath('//span[@class="house-chat-txt strongbox"]/text()').extract_first()
        # 附近地铁
        subway_distance = response.xpath('//em[@class="dt c_888 f12"]/text()').extract_first()
        # 公司
        company = response.xpath('//*[@id="bigCustomer"]/p[2]/text()').extract_first()
        # 联系人
        contact = response.xpath('//*[@id="bigCustomer"]/p[1]/a/text()').extract_first()

        item['price'] = price
        item['payment'] = payment
        item['method'] = method
        item['house_type'] = house_type
        item['community'] = community
        item['area'] = area
        item['address'] = address
        item['telphone'] = telphone
        item['subway_distance'] = subway_distance
        item['company'] = company
        item['contact'] = contact
        yield item

    def parse_item(self, response):
        li = response.xpath('//ul[@class="listUl"]/li')
        for i in li:
            url_detail = 'https://'+i.xpath('./div[@class="img_list"]/a/@href').extract_first()
            # 租房图片url
            img_url = 'https://'+i.xpath('./div[@class="img_list"]/a/img/@src').extract_first()
            item = Crawlspider58Item()
            item['img_url'] = img_url
            yield scrapy.Request(url=url_detail,callback=self.parse_detail,meta={'item':item})

