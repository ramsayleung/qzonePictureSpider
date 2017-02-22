# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import log


#自定义文件名
class QQImagesPipelines(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url, meta={'item': item})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        # 从URL提取图片的文件名
        # 拼接最终的文件名,格式:qq号/{相册名}/图片文件名.jpg
        image_guid = request.url.split('/')[-3]
        log.msg(image_guid, level=log.DEBUG)
        filename = u'{0[account]}/{0[album_name]}/{1}.jpg'.format(item,
                                                                  image_guid)
        return filename
