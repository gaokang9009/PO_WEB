#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on 2020-
@Author: GaoKang
Project description：
测试MenuPage页面
"""

import pytest
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


class TestMenu(object):
    # def test_menu(self, menu_page):
    #     """测试web menu中各模块能够打开和关闭"""
    #     Menu, ele_dict, menus = menu_page
    #     # for menu in menus:
    #     for menu in ele_dict['eles']():
    #         menux = menu.find_element(*Menu.menu_loc_name)
    #         Menu.open_tab(menu)
    #         print(f'打开"{menux.text}"模块页面')
    #         Menu.force_wait(3)
    #         if menux.text == '设备快照':
    #             continue
    #         assert menux.text == Menu.ele_text(Menu.menu_tab_loc),
    #         f'打开menu模块，预期标题为{menux.text}，实际标题为{Menu.ele_text(Menu.menu_tab_loc)}'
    #         Menu.close_tab()
    #         print(f'关闭"{menux.text}"模块页面')

    @pytest.mark.parametrize('data', menudata_datas, ids=menudata_ids)
    def test_menu(self, menu_page, data):
        """测试web menu中各模块能够打开和关闭"""
        Menu, ele_dict, menus = menu_page
        ele = menus[data]
        menux = ele.find_element(*Menu.menu_loc_name)
        Menu.open_tab(ele)
        Menu.force_wait(3)
        assert menux.text == Menu.ele_text(Menu.menu_tab_loc), f'打开menu模块，预期标题为{menux.text}，实际标题为{Menu.ele_text(Menu.menu_tab_loc)}'
        Menu.close_tab()


if __name__ == "__main__":
    pytest.main()
