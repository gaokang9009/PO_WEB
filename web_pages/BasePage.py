#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on 2020-
@Author: GaoKang
Project description：
基础类BasePage，封装所有页面都公用的方法，定义open函数，重定义find_element，switch_frame，send_keys等函数。
在初始化方法中定义驱动driver，基本url,title
WebDriverWait提供了显式等待方式。
"""
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException,\
                                       InvalidElementStateException, NoSuchFrameException, NoAlertPresentException,\
                                       NoSuchWindowException
import utils


class BasePage(object):
    """
    定义基类，实现常用函数
    """
    def __init__(self, selenium_driver, base_url, page_title):
        self.driver = selenium_driver
        self.base_url = base_url
        self.page_title = page_title
        self.main_handle = None

    @classmethod
    def force_wait(cls, seconds):
        time.sleep(seconds)

    def on_page(self, page_title):
        self.force_wait(2)
        return page_title in self.driver.title

    def open(self, url):
        self.driver.get(url)
        self.driver.maximize_window()

    def _open(self, url, page_title):
        self.driver.get(url)
        self.driver.maximize_window()
        assert self.on_page(page_title), f"打开网页失败 {url},期望page_title为'{page_title}'，实际page_title为'{self.driver.title}'"

    def open_url(self):
        self._open(self.base_url, self.page_title)
        self.main_handle = self.driver.window_handles[0]

    def find_element(self, *loc):
        try:
            # WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element(*loc).is_displayed())
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(loc))
            ele = self.driver.find_element(*loc)
        except Exception as e:
            self.save_screenshot(loc[0])
            print(f'定位方式 {loc[0]}->{loc[1]} 的元素未找到! {e}')
            ele = None
        return ele

    def find_elements(self, *loc):
        try:
            # WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element(*loc).is_displayed())
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(loc))
            ele = self.driver.find_elements(*loc)
        except TimeoutException:
            self.save_screenshot(loc[0])
            print(f'定位方式 {loc[0]}->{loc[1]} 的元素未找到!')
            ele = None
        return ele

    def save_screenshot(self, filename):
        shot_path = utils.SCREENSHOTPATH
        if not os.path.exists(shot_path):
            os.makedirs(shot_path)
        # 图片名称：模块名-页面名-函数名-年月日时分秒.png
        file_name = os.path.join(shot_path, 'find_ele_fail_' + filename + time.strftime('%Y%m%d%H%M%S') + '.png')
        self.driver.save_screenshot(file_name)
        print(f"成功获取截图，路径：{file_name}")

    def ele_send_keys(self, loc, value, clear_first=True, click_first=True):
        if self.find_element(*loc):
            try:
                # loc = getattr(self, "_%s" % loc)
                if click_first:
                    self.find_element(*loc).click()
                if clear_first:
                    self.find_element(*loc).clear()
                self.find_element(*loc).send_keys(value)
            except InvalidElementStateException as e:
                print(f"定位方式 {loc[0]}->{loc[1]} 的元素不存在send_keys属性，{e}")

    @staticmethod
    def ele_send_keys_simple(ele, value, clear_first=True, click_first=True):
        try:
            if click_first:
                ele.click()
            if clear_first:
                ele.clear()
            ele.send_keys(value)
        except InvalidElementStateException as e:
            print(f"{ele} 的元素不存在send_keys属性，{e}")

    def ele_click(self, loc):
        if self.find_element(*loc):
            try:
                self.find_element(*loc).click()
            except InvalidElementStateException as e:
                print(f"定位方式 {loc[0]}->{loc[1]} 的元素不存在click属性，{e}")

    @staticmethod
    def ele_click_simple(ele):
        try:
            ele.click()
        except InvalidElementStateException as e:
            print(f"{ele} 元素不存在click属性，{e}")

    def ele_text(self, loc):
        ele_txt = None
        if self.find_element(*loc):
            try:
                ele_txt = self.find_element(*loc).text
            except AttributeError as e:
                print(f"定位方式 {loc[0]}->{loc[1]} 的元素不存在text，{e}")
        return ele_txt

    @staticmethod
    def ele_text_simple(ele):
        ele_txt = None
        try:
            ele_txt = ele.text
        except AttributeError as e:
            print(f"{ele} 元素不存在text，{e}")
        return ele_txt

    def move_to_ele(self, loc):
        if self.find_element(*loc):
            ele = self.find_element(*loc)
            try:
                ActionChains(self.driver).move_to_element(ele).perform()
            except InvalidElementStateException as e:
                print(f"定位方式 {loc[0]}->{loc[1]} 的元素不存在move_to属性，{e}")

    def move_to_ele_simple(self, ele):
        try:
            ActionChains(self.driver).move_to_element(ele).perform()
        except InvalidElementStateException as e:
            print(f"{ele} 的元素不存在move_to属性，{e}")

    def move_to_click(self, loc):
        if self.find_element(*loc):
            ele = self.find_element(*loc)
            try:
                ActionChains(self.driver).move_to_element(ele).click(ele).perform()
            except InvalidElementStateException as e:
                print(f"定位方式 {loc[0]}->{loc[1]} 的元素不存在move_to and click属性，{e}")

    def move_to_click_simple(self, ele):
        try:
            ActionChains(self.driver).move_to_element(ele).click(ele).perform()
        except InvalidElementStateException as e:
            print(f"{ele} 的元素不存在move_to and click属性，{e}")

    def switch_frame(self, loc):
        try:
            self.driver.switch_to.frame(loc)
        except NoSuchFrameException as e:
            print(f"当前页面不存在iframe为{loc}的frame，{e}")

    def switch_alert(self):
        try:
            alert_x = self.driver.switch_to.alert()
            return alert_x
        except NoAlertPresentException as e:
            print(f"当前页面不存在alert，{e}")

    def switch_window(self, window_handle):
        try:
            alert_x = self.driver.switch_to.window(window_handle)
            return alert_x
        except NoSuchWindowException as e:
            print(f"当前页面不存在handle为{window_handle}的Window，{e}")

    def exec_script(self, src):
        self.driver.execute_script(src)

    def quit(self):
        self.driver.quit()


def main():
    """
    just test class BasePage
    """
    driver = webdriver.Chrome()
    # driver.switch_to.alert()
    base_url = 'http://120.0.60.7'
    page_title = '管理系统'
    basep = BasePage(driver, base_url, page_title)
    basep.open_url()
    print(driver.window_handles)
    username_loc = (By.ID, 'userName')
    pass_loc = (By.ID, 'password')
    login_loc = (By.ID, 'logonBt')
    basep.find_element(*username_loc).send_keys('admin')
    basep.ele_send_keys(pass_loc, 'admin')
    basep.ele_click(login_loc)
    time.sleep(5)
    driver.quit()


if __name__ == "__main__":
    main()
