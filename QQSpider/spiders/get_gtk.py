#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys


class GetGtk(object):
    def LongToInt(self, value):  # 由于int+int超出范围后自动转为long型，通过这个转回来
        if isinstance(value, int):
            return int(value)
        else:
            return int(value & sys.maxint)

    def LeftShiftInt(self, number, step):  # 由于左移可能自动转为long型，通过这个转回来
        if isinstance((number << step), long):
            return int((number << step) - 0x200000000L)
        else:
            return int(number << step)

    def getOldGTK(self, skey):
        a = 5381
        for i in range(0, len(skey)):
            a = a + self.LeftShiftInt(a, 5) + ord(skey[i])
            a = self.LongToInt(a)
        return a & 0x7fffffff

    def getNewGTK(self, p_skey, skey, rv2):
        b = p_skey or skey or rv2
        a = 5381
        for i in range(0, len(b)):
            a = a + self.LeftShiftInt(a, 5) + ord(b[i])
            a = self.LongToInt(a)
        return a & 0x7fffffff

    def getGTK(self, cookie):
        if not cookie:
            return
        p_skey = cookie.get("p_skey", None)
        skey = cookie.get('skey', None)
        rv2 = cookie.get('rv2', None)
        return self.getNewGTK(p_skey, skey, rv2)
