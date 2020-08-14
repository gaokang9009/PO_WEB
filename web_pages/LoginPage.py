#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on 2020-
@Author: GaoKang
Project description：
登陆页面元素定义和基本操作定义
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from web_pages.BasePage import BasePage


class LoginPage(BasePage):
    def __init__(self, driver, base_url, page_title):
        super().__init__(driver, base_url, page_title)
        self.user_loc = (By.ID, 'userName')
        self.passw_loc = (By.ID, 'password')
        self.login_submit_loc = (By.ID, 'logonBt')
        self.login_tip = (By.ID, 'logTip')
        self.switch_language_loc = (By.ID, 'language')
        self.about_show_loc = (By.ID, 'show-btn')
        self.about_close_loc = (By.XPATH, '/html/body/center/table/tbody/tr[5]/td/button')
        self.about_frame = (By.XPATH, '//*[@src="about.html"]')
        self.license_show_loc = (By.ID, 'licensetxt')
        self.copyright_loc = (By.ID, 'copyright')
        self.navigation_loc = (By.XPATH, '//*[@class="x-tab-strip-text icon_navigation"]')
        self.detail_siwitch = (By.ID, 'basic_SiwitchButtonId')

    def input_username(self, username):
        self.ele_send_keys(self.user_loc, username)

    def input_password(self, password):
        self.ele_send_keys(self.passw_loc, password)

    def login_submit(self):
        self.ele_click(self.login_submit_loc)

    def tab_txt(self, ele):
        return self.ele_text(ele)

    def switch_language(self):
        self.ele_click(self.switch_language_loc)

    def about_show(self):
        self.ele_click(self.about_show_loc)

    def about_close(self):
        # self.mouse_move_to(self.about_close_loc)
        iframe = self.find_element(*self.about_frame)
        self.switch_frame(iframe)
        self.ele_click(self.about_close_loc)

    def license_show(self):
        iframe = self.find_element(*self.about_frame)
        self.switch_frame(iframe)
        self.ele_click(self.license_show_loc)
        license_handle = self.driver.window_handles[-1]
        self.switch_window(license_handle)
        self.force_wait(1)

    def license_close(self):
        self.main_handle = self.driver.window_handles[0]
        self.driver.close()
        # print(self.main_handle)
        self.switch_window(str(self.main_handle))

    @property
    def ele_dict(self):
        dict_x = {'logtip_txt': self.login_tip, 'navigation_txt': self.navigation_loc,
                  'copyright_loc': self.copyright_loc, 'switch_language_loc': self.switch_language_loc
                  }
        return dict_x

    def login_just(self, username, password):
        self.open_url()
        self.input_username(username)
        self.input_password(password)
        self.login_submit()
        self.force_wait(2)


def main():
    """
    主函数
    """
    driver = webdriver.Chrome()
    base_url = 'http://120.0.60.7'
    page_title = '管理系统'
    login_web = LoginPage(driver, base_url, page_title)
    login_web.open_url()
    print(login_web.ele_text(login_web.copyright_loc))
    login_web.switch_language()
    print(login_web.ele_text(login_web.copyright_loc))

    login_web.about_show()
    login_web.force_wait(2)
    login_web.about_close()
    login_web.force_wait(2)

    login_web.about_show()
    login_web.force_wait(2)
    login_web.license_show()
    print(driver.window_handles)
    login_web.license_close()
    login_web.about_close()
    login_web.force_wait(2)
    login_web.login_submit()
    print(login_web.tab_txt(login_web.login_tip))
    login_web.input_username('admin')
    login_web.input_password('admin')
    login_web.login_submit()
    login_web.force_wait(2)
    driver.quit()


if __name__ == "__main__":
    main()
