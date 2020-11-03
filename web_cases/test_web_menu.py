#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on 2020-
@Author: GaoKang
Project description：
测试MenuPage页面
"""

import allure
# from pytest import assume
from pytest_assume.plugin import assume
import pytest
import allure
from utils import commlib
from web_pages.MenuPage import MenuPage

menudata_id, menudata_data, menudata_expect = commlib.api_normal_data('menu_data.yaml', 'menudata')
menudata_ids = []
for menu in menudata_id.split(','):
    if menu == '设备快照':
        continue
    id_name = f'打开和关闭"{menu}"页面'
    menudata_ids.append(id_name)
menudata_datas = list(range(1, len(menudata_ids)+1))


@pytest.fixture(scope='class')
def menu_page(login_main_page):
    driver, base_url, page_titie = login_main_page
    menu_page = MenuPage(driver, base_url, page_titie)
    menus = menu_page.find_elements(*menu_page.menus_loc)
    yield menu_page, menu_page.ele_dict, menus


@pytest.mark.usefixtures('check_login_ok')
class TestMenu(object):

    @allure.feature("功能菜单页面")
    @allure.story("各功能页面成功打开")
    @allure.severity("normal")
    @pytest.mark.parametrize('data', menudata_datas, ids=menudata_ids)
    def test_menu(self, menu_page, data):
        """测试web menu中各模块能够打开和关闭"""
        menu, ele_dict, menus = menu_page
        ele = menus[data]
        menu_x = ele.find_element(*menu.menu_loc_name)
        with allure.step(f"step1：打开{menu_x.text}页面"):
            menu.open_tab(ele)
        menu.force_wait(3)
        with allure.step('step2：验证打开的table标题文本信息与预期一致'):
            with assume:
                assert menu_x.text == menu.ele_text(menu.menu_tab_loc), f'打开menu模块,预期标题为{menu_x.text},' \
                    f'实际标题为{menu.ele_text(menu.menu_tab_loc)}'
        with allure.step(f"step3：关闭{menu_x.text}页面"):
            menu.close_tab()


if __name__ == "__main__":
    pytest.main()
