#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on 2020-
@Author: GaoKang
Project description：
测试NavigationPage页面
"""

import allure
# from pytest import assume
from pytest_assume.plugin import assume
import pytest
from utils import commlib
from web_pages.NavigationPage import NavigationPage

navidata_ids, navidata_datas = commlib.api_data('navigation_data.yaml', 'navidata')
navigation_switch_ids, navigation_switch_datas = commlib.api_data('navigation_data.yaml', 'navi_switchdata')


@pytest.fixture(scope='class')
def navigation_page(login_web_class):
    driver, base_url, page_titie = login_web_class
    navigationpage = NavigationPage(driver, base_url, page_titie)
    yield navigationpage, navigationpage.ele_dict


@pytest.fixture(autouse=True)
def forcewait(navigation_page):
    navigationpage, dict_x = navigation_page
    navigationpage.force_wait(1)


@pytest.mark.usefixtures('check_login_ok')
class TestNavigation(object):

    @allure.feature("导航页面")
    @allure.story("各功能页面成功打开")
    @allure.severity("normal")
    @pytest.mark.parametrize('case, data, expect', navidata_datas, ids=navidata_ids)
    def test_navigation_tab(self, navigation_page, case, data, expect):
        """测试web导航页面中各模块能够打开和关闭"""
        navigation_page, ele_dict = navigation_page
        move_ele = ele_dict[data['move']]
        click_ele = ele_dict[data['click']]
        label_ele = ele_dict[expect['labelname']]
        label_str = expect['labelstr']
        with allure.step(f"step1：打开{label_str}页面"):
            navigation_page.open_tab(move_ele, click_ele)
        navigation_page.force_wait(3)
        label_now_str = navigation_page.tab_txt(label_ele)
        with allure.step("step2：验证打开的table标题文本信息与预期一致"):
            with assume:
                assert label_now_str == label_str, f'打开导航中模块，预期标题为{label_str}，实际标题为{label_now_str}'
        with allure.step(f"step3：关闭{label_str}页面"):
            navigation_page.close_tab()

    @pytest.mark.demo
    @allure.feature("导航页面")
    @allure.story("导航页面中高级菜单切换")
    @allure.severity("blocker")
    @pytest.mark.parametrize('case, data, expect', navigation_switch_datas, ids=navigation_switch_ids)
    def test_navigation_switch(self, navigation_page, case, data, expect):
        """测试web导航页面中高级菜单切换"""
        navigation_page, ele_dict = navigation_page
        click_ele = ele_dict[data['click']]
        label_ele = ele_dict[expect['labelname']]
        label_str = expect['labelstr']
        with allure.step(f"step1：点击菜单切换按钮"):
            navigation_page.ele_click(click_ele)
        navigation_page.force_wait(2)
        with allure.step(f"step2：获取切换后页面元素特征字符"):
            label_now_str = navigation_page.tab_txt(label_ele)
        with allure.step(f"step3：验证切换后元素字符与预期一致"):
            assert label_now_str == label_str, f'基本与高级菜单切换，预期元素text为{label_str}，实际元素text为{label_now_str}'


if __name__ == "__main__":
    pytest.main()
