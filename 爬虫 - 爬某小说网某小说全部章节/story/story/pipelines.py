# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class StoryPipeline(object):

    fp = None

    def open_spider(self,spider):
        print('开始爬取')
        self.fp = open('暗示.txt','w',encoding='utf-8')

    def process_item(self, item, spider):
        string = '\t'+item['title'] + '\n\n' + item['content']+'\n\n\n'

        self.fp.write(string)
        return item
    def close_spider(self,spider):
        print('结束爬取')
        self.fp.close()