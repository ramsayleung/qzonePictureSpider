#!/usr/bin/env python
# encoding=utf-8
import logging
import time

import selenium.webdriver.support.ui as ui
from selenium import webdriver


class GetCookie(object):

    def getCookie(self, account, password):
        """ 根据QQ号和密码获取cookie """
        failure = 0
        while failure < 2:
            try:
                browser = webdriver.PhantomJS(
                    executable_path="/usr/local/bin/phantomjs")
                wait = ui.WebDriverWait(browser, 10)
                browser.get(
                    'http://qzone.qq.com/?s_url=http://user.qzone.qq.com/869810754/')
                browser.switch_to_frame('login_frame')
                wait.until(
                    lambda browser: browser.find_element_by_id('switcher_plogin'))
                plogin = browser.find_element_by_id('switcher_plogin')
                plogin.click()
                wait.until(lambda browser: browser.find_element_by_id('u'))
                u = browser.find_element_by_id('u')
                u.send_keys('%s' % (account))
                p = browser.find_element_by_id('p')
                p.send_keys('%s' % (password))
                wait.until(
                    lambda browser: browser.find_element_by_xpath('//*[@id="login_button"]'))
                login = browser.find_element_by_xpath(
                    '//*[@id="login_button"]')
                time.sleep(2)
                login.click()
                time.sleep(1)
                try:
                    browser.switch_to_frame('vcode')
                    print('Failed!----------------reason:该QQ首次登录Web空间，需要输入验证码！')
                    break
                except Exception:
                    pass
                try:
                    err = browser.find_element_by_id('err_m')
                    time.sleep(2)
                    d = err.text
                    print(account, d)
                    if u'您输入的帐号或密码不正确' in d:
                        print('Failed!----------------reason:账号或者密码错误！')
                        logging.error("账号或者密码错误")
                        break
                    if u'网络繁忙' in d:
                        time.sleep(2)
                except Exception as e:
                    cookie = {}
                    for ck in browser.get_cookies():
                        cookie[ck['name']] = ck['value']
                        browser.quit()
                        print("Get the cookie of QQ:%s successfully!(共%d个键值对" % (
                            account, len(cookie)))
                    return cookie
            except Exception:
                failure = failure + 1
            except KeyboardInterrupt as e:
                raise e
