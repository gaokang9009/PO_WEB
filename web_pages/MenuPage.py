#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on 2020-
@Author: GaoKang
Project description：
菜单页面元素定义和基本操作定义
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from web_pages.BasePage import BasePage
from web_pages.LoginPage import LoginPage


class MenuPage(BasePage):

    def __init__(self, driver, base_url, page_title):
        super().__init__(driver, base_url, page_title)
        self.detail_SwitchButton = (By.ID, 'basic_SiwitchButtonId')
        self.menus_loc = (By.CSS_SELECTOR, '.x-tree-node-ct .x-tree-node')
        self.menu_loc_name = (By.XPATH, './/a/span')
        self.menu_tab_loc = (By.XPATH, '//*[@class="x-tab-strip x-tab-strip-top"]/li[3]//*[contains(@class,"x-tab-strip-text")]')
        self.tab_close_loc = (By.XPATH, '//*[@class="x-tab-strip x-tab-strip-top"]/li[3]/*[@class="x-tab-strip-close"]')

    def open_tab(self, ele):
        self.move_to_ele_simple(ele)
        self.force_wait(1)
        self.ele_click_simple(ele)
        self.force_wait(1)

    def close_tab(self):
        self.ele_click(self.tab_close_loc)

    def eles(self):
        return self.find_elements(*self.menus_loc)

    @property
    def ele_dict(self):
        dict_x = {'eles': self.eles}
        return dict_x


def main():
    """
    主函数
    """
    driver = webdriver.Chrome()
    base_url = 'http://120.0.61.254'
    page_title = '管理系统'
    login_web = LoginPage(driver, base_url, page_title)
    login_web.open_url()
    login_web.input_username('admin')
    login_web.input_password('admin')
    login_web.login_submit()
    login_web.force_wait(2)

    Menu = MenuPage(driver, base_url, page_title)
    Menu.ele_click(Menu.detail_SiwitchButton)
    menus = Menu.find_elements(*Menu.menus_loc)
    for menu in menus:
        menux = menu.find_element(*Menu.menu_loc_name)
        Menu.open_tab(menu)
        print(menux.text)
        Menu.force_wait(2)
        if menux.text == '设备快照':
            continue
        assert menux.text == Menu.ele_text(Menu.menu_tab_loc)
        Menu.close_tab()
    driver.quit()


if __name__ == "__main__":
    main()
