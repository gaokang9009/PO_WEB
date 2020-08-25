#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on 2020-
@Author: GaoKang
Project description：
测试LoginPage页面
"""

import allure
import pytest
from utils import commlib
from utils.web_assert import *
from web_pages.LoginPage import LoginPage

login_ids, login_datas = commlib.api_data('login_data.yaml', 'login_data')
switch_language_ids, switch_language_datas = commlib.api_data('login_data.yaml', 'switch_language_data')
open_url_ids, open_url_datas = commlib.api_data('login_data.yaml', 'open_url_data')


@pytest.fixture(scope='class')
def login_page(base_info):
    driver, base_url, page_title = base_info
    loginpage = LoginPage(driver, base_url, page_title)
    yield loginpage, loginpage.ele_dict
    driver.quit()


@pytest.fixture(autouse=True)
def forcewait(login_page):
    login_page, ele_dict = login_page
    login_page.force_wait(2)


class TestLogin(object):

    @allure.feature("登录页面")
    @allure.story("web网页成功打开")
    @pytest.mark.parametrize('case, data, expect', open_url_datas, ids=open_url_ids)
    def test_open_url(self, login_page, case, data, expect):
        """测试web页面正常打开"""
        login_page, ele_dict = login_page
        # login_page.open_url()
        with allure.step("step1：打开web网页"):
            login_page.open(login_page.base_url)
            login_page.force_wait(5)
        with allure.step("step2：获取网页标题"):
            web_title = login_page.driver.title
        with allure.step("step1：验证预期标题与实际网页标题相同"):
            assert login_page.page_title in web_title, f"打开网页失败 {login_page.base_url}," \
                f"期望page_title为'{login_page.page_title}'，实际page_title为'{web_title}'"

    @allure.feature("登录页面")
    @allure.story("关于web链接成功打开与关闭")
    def test_about_web(self, login_page):
        """测试web登陆页面中关于web系统正常开关"""
        login_page, ele_dict = login_page
        with allure.step("step1：点击关于web链接"):
            login_page.about_show()
        with allure.step("step2：验证关于web信息框被打开"):
            assert login_page.find_element(*login_page.about_frame) is not None, 'about信息框未被成功打开'
        with allure.step("step3：关闭关于web窗口"):
            login_page.about_close()
        with allure.step("step4：验证关于web信息框被关闭"):
            assert login_page.find_element(*login_page.login_submit_loc) is not None, 'about信息框未被成功关闭'

    @allure.feature("登录页面")
    @allure.story("用户许可协议链接成功打开与关闭")
    def test_user_license(self, login_page):
        """测试web登陆页面用户许可协议正常开关"""
        login_page, ele_dict = login_page
        with allure.step("step1：点击关于web链接"):
            login_page.about_show()
            login_page.force_wait(1)
        with allure.step("step2：点击用户许可协议链接"):
            login_page.license_show()
        with allure.step("step3：验证用户许可协议标题与预期一致"):
            assert '用户许可协议' in login_page.driver.title, f'预期用户许可协议页面title为"用户许可协议"，实际title为{login_page.driver.title}'
        with allure.step("step4：关闭用户许可协议page"):
            login_page.license_close()
            login_page.force_wait(1)
        with allure.step("step5：关闭关于web窗口"):
            login_page.about_close()

    # @pytest.mark.parametrize('case, data, expect', switch_language_datas, ids=switch_language_ids)
    # def test_switch_language(self, login_page, case, data, expect):
    #     """测试web页面中英文正常切换"""
    #     login_page, ele_dict = login_page
    #     click_ele = ele_dict[data['click']]
    #     login_page.ele_click(click_ele)
    #     login_page.force_wait(1)
    #     label_ele = ele_dict[expect['labelname']]
    #     label_str = login_page.tab_txt(label_ele)
    #     expect_str = expect['labelstr']
    #     assert expect_str in label_str, f'验证copyright {label_str}中存在{expect_str}'

    @allure.feature("登录页面")
    @allure.story("web语言进行切换")
    @pytest.mark.parametrize('case, data, expect', switch_language_datas, ids=switch_language_ids)
    def test_switch_language(self, login_page, case, data, expect):
        """测试web页面中英文正常切换"""
        login_page, ele_dict = login_page
        click_ele = ele_dict[data['click']]
        with allure.step("step1：点击语言切换按钮"):
            login_page.ele_click(click_ele)
            login_page.force_wait(1)
        with allure.step("step2：验证页面语言符合预期"):
            check_ele_info(login_page, ele_dict, expect, assert_type='in', assert_tip=None)

    @allure.feature("登录页面")
    @allure.story("web登陆测试")
    @pytest.mark.parametrize('case, data, expect', login_datas, ids=login_ids)
    def test_login(self, login_page, case, data, expect):
        """测试web登陆页面用户登陆"""
        login_page, ele_dict = login_page
        with allure.step("step1：获取测试的用户名和密码"):
            username = data['username']
            password = data['password']
        with allure.step("step2：输入用户名"):
            if username:
                login_page.input_username(username)
            else:
                login_page.find_element(*login_page.user_loc).clear()
        with allure.step("step3：输入密码"):
            if password:
                login_page.input_password(password)
            else:
                login_page.find_element(*login_page.passw_loc).clear()
        with allure.step("step4：点击登陆按钮"):
            login_page.login_submit()
        # label_ele = ele_dict[expect['labelname']]
        # label_str = login_page.tab_txt(label_ele)
        # expect_str = expect['labelstr']
        # assert label_str == expect_str, f'预期登陆时提示为{expect_str}，实际提示为{label_str}'
        with allure.step("step5：验证登陆结果符合预期"):
            check_ele_info(login_page, ele_dict, expect, assert_type='equal', assert_tip=None)


if __name__ == "__main__":
    pytest.main()
