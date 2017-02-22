#!/usr/bin/env python
# -*- coding:utf-8 -*-
import getpass


class Init(object):
    """功能：初始化"""

    def __init__(self):
        self.account = raw_input("input your login account: ")
        self.password = getpass.getpass("input your password: ")

    def read_qq_for_crawl(self, file_dir="./QQ_for_crawl.txt"):
        qqlist = []
        with open(file_dir, 'r') as file_qqlist:
            for line in file_qqlist.readlines():
                qqlist.append(line.strip())
        return qqlist
