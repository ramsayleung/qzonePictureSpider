#!/usr/bin/env python
# -*- coding:utf-8 -*-
from scrapy.spiders import CrawlSpider
# from scrapy.selector import Selector
# from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.http import Request
import get_cookie
import get_gtk
import fileinput as fileinput
import sys
import json
from QQSpider.items import QqspiderItem
import init
from pprint import pprint
import logging


class QQSpider(CrawlSpider):
    name = 'qq'
    allowed_domains = ["qq.com"]

    def __init__(self):
        self.init_content = init.Init()
        self.account = self.init_content.account
        self.password = self.init_content.password
        self.account_list_for_crawl = self.init_content.read_qq_for_crawl()
        self.get_cookie_instance = get_cookie.GetCookie()
        self.cookie = get_cookie.GetCookie().getCookie(self.account,
                                                       self.password)
        self.get_gtk_instance = get_gtk.GetGtk()
        self.gtk = self.get_gtk_instance.getGTK(self.cookie)
        print(self.gtk)

    def start_requests(self):
        for account_for_crawl in self.account_list_for_crawl:

            item = QqspiderItem()
            item['account'] = account_for_crawl

            yield Request(
                url="http://h5.qzone.qq.com/proxy/domain/alist.photo.qq.com/fcgi-bin/fcg_list_album_v3?g_tk=%s"
                "&callback=shine0_Callback&t=955106858&hostUin=%s"
                "&uin=%s"
                "&appid=4&inCharset=utf-8&outCharset=utf-8&source=qzone&plat=qzone&format=jsonp&notice=0&filter=1&handset=4&pageNumModeSort=40&pageNumModeClass=15&needUserInfo=1&idcNum=0&callbackFun=shine0&_=1474681546872&mode=2&sortOrder=2&pageStart=0"
                % (self.gtk, account_for_crawl, self.account),
                cookies=self.cookie,
                meta={'item': item},
                callback=self.parse)

    def parse(self, response):
        item = response.meta['item']
        account_for_crawl = item['account']
        response_json = response.body
        # 将得到的请求结果保存到文件
        with open("response.txt", "wt") as tmpWrite:
            tmpWrite.write(response_json)
            # 对response进行修改，变成标准的json文件
        self.replaceAll("response.txt", "shine0_Callback({", "{")
        self.replaceAll("response.txt", ");", "")
        with open("response.txt") as data_file:
            json_formatted = json.load(data_file)
        pprint(json_formatted)
        # album_list_num = len(json_formatted["data"]["albumListModeSort"])
        try:
            for album_list in json_formatted["data"]["albumList"]:
                album_id = album_list['id']
                total_photo = album_list['total']
                print(album_id, total_photo)

                #qq空间最多只会返回200条数据
                image_counter = 0
                while image_counter < total_photo:
                    image_url = "http://h5.qzone.qq.com/webapp/json/mqzone_photo/getPhotoList2?g_tk={0}&uin={1}&albumid={2}&ps={3}&pn={4}&password=&password_cleartext=0&swidth=1920&sheight=1080&sid=Pp7O26sWwPQbVfSPlzR0XBaL7ZpyXD9D33d842420201%3D%3D".format(
                        self.gtk, account_for_crawl, album_id, image_counter,
                        total_photo)
                    image_counter += 200
                    yield Request(
                        image_url,
                        callback=self.parse_image,
                        meta={'item': item},
                        cookies=self.cookie, )
            #如果相册数太大，一次没法请求完，继续请求
            album_total = json_formatted["data"]["albumsInUser"]
            album_next_page = json_formatted["data"]["nextPageStart"]
            if album_total != album_next_page:
                yield Request(
                    url="http://h5.qzone.qq.com/proxy/domain/alist.photo.qq.com/fcgi-bin/fcg_list_album_v3?g_tk=%s"
                    "&callback=shine0_Callback&t=955106858&hostUin=%s&uin=%s"
                    "&appid=4&inCharset=utf-8&outCharset=utf-8&source=qzone&plat=qzone&format=jsonp&notice=0&filter=1&handset=4&pageNumModeSort=40&pageNumModeClass=15&needUserInfo=1&idcNum=0&callbackFun=shine0&_=1474681546872&mode=2&sortOrder=2&pageStart=%d"
                    % (self.gtk, account_for_crawl, self.account,
                       album_next_page),
                    cookies=self.cookie,
                    meta={'item': item},
                    callback=self.parse)

        except (KeyError, TypeError):
            logging.error("你登录的用户没有权限查看相册。请再次确认权限问题或者检查密码是否输入有误")

    def parse_image(self, response):
        # print(response.body)
        try:
            item = QqspiderItem()
            item['account'] = response.meta['item']['account']
            photos = json.loads(response.body)
            item['album_name'] = photos['data']['album']['name']
            logging.debug("albumid:" + photos['data']['album']['albumid'])
            logging.debug("album name: " + item['album_name'])
            image_urls = []
            for key in photos['data']['photos'].keys():
                for photo in photos['data']['photos'][key]:
                    image_url = photo['1']['url']
                    image_urls.append(image_url)
            item['image_urls'] = image_urls
            yield item

        except KeyError:
            logging.error("你的登陆账号没有权限查看该账号的该相册")

    def replaceAll(self, filename, searchExp, replaceExp):
        for line in fileinput.input(files=(filename), inplace=1):
            # for line in f:
            if searchExp in line:
                line = line.replace(searchExp, replaceExp)
            sys.stdout.write(line)
