#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on 2020-
@Author: GaoKang
Project description：
自定义断言
"""

import allure

# class WebAssert(object):
@allure.step('检测相应元素的文本信息正确')
def check_ele_info(cur_page, ele_dict, expect, assert_type='in', assert_tip=None):
    label_ele = ele_dict[expect['labelname']]
    label_str = cur_page.tab_txt(label_ele)
    expect_str = expect['labelstr']
    if not assert_tip:
        if assert_type == 'equal':
            assert_tip = f'预期元素的text为"{expect_str}"，实际为"{label_str}"'
        else:
            assert_tip = f'预期元素的text--"{expect_str}"中存在字符--"{label_str}"'
    if assert_type == 'equal':
        assert expect_str == label_str, assert_tip
    else:
        assert expect_str in label_str, assert_tip


def main():
    """
    主函数
    """

    pass


if __name__ == "__main__":
    main()
