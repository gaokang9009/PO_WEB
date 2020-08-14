#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on 2020-
@Author: GaoKang
Project description：
测试LoginPage页面
"""

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

    @pytest.mark.parametrize('case, data, expect', open_url_datas, ids=open_url_ids)
    def test_open_url(self, login_page, case, data, expect):
        """测试web页面正常打开"""
        login_page, ele_dict = login_page
        # login_page.open_url()
        login_page.open(login_page.base_url)
        login_page.force_wait(5)
        assert login_page.page_title in login_page.driver.title, f"打开网页失败 {login_page.base_url}," \
            f"期望page_title为'{login_page.page_title}'，实际page_title为'{login_page.driver.title}'"

    def test_about_web(self, login_page):
        """测试web登陆页面中关于web系统正常开关"""
        login_page, ele_dict = login_page
        login_page.about_show()
        assert login_page.find_element(*login_page.about_frame) is not None, '验证about信息框存在'
        login_page.about_close()
        assert login_page.find_element(*login_page.login_submit_loc) is not None, '验证about信息框不存在'

    def test_user_license(self, login_page):
        """测试web登陆页面用户许可协议正常开关"""
        login_page, ele_dict = login_page
        login_page.about_show()
        login_page.license_show()
        assert '用户许可协议' in login_page.driver.title, f'验证用户许可协议页面被打开，新页面title实际为{login_page.driver.title}'
        login_page.license_close()
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

    @pytest.mark.parametrize('case, data, expect', switch_language_datas, ids=switch_language_ids)
    def test_switch_language(self, login_page, case, data, expect):
        """测试web页面中英文正常切换"""
        login_page, ele_dict = login_page
        click_ele = ele_dict[data['click']]
        login_page.ele_click(click_ele)
        login_page.force_wait(1)
        check_ele_info(login_page, ele_dict, expect, assert_type='in', assert_tip=None)

    @pytest.mark.parametrize('case, data, expect', login_datas, ids=login_ids)
    def test_login(self, login_page, case, data, expect):
        """测试web登陆页面用户登陆"""
        login_page, ele_dict = login_page
        username = data['username']
        password = data['password']
        if username:
            login_page.input_username(username)
        else:
            login_page.find_element(*login_page.user_loc).clear()
        if password:
            login_page.input_password(password)
        else:
            login_page.find_element(*login_page.passw_loc).clear()
        login_page.login_submit()
        # label_ele = ele_dict[expect['labelname']]
        # label_str = login_page.tab_txt(label_ele)
        # expect_str = expect['labelstr']
        # assert label_str == expect_str, f'预期登陆时提示为{expect_str}，实际提示为{label_str}'
        check_ele_info(login_page, ele_dict, expect, assert_type='equal', assert_tip=None)


if __name__ == "__main__":
    pytest.main()
