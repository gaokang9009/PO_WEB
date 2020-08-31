#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on 2020-
@Author: GaoKang
Project description：
测试LoginPage页面
"""

import pytest
from conftest import FailedCase

user_data = [('admin', 1), ('pass', 2)]


@pytest.fixture(scope='function', params=user_data)
def login(request):
    return request.param[0], request.param[1]


# def test_open_url(login):
#     """测试web页面正常打开"""
#     login_page, ele_dict = login
#     print(login_page, ele_dict)
#
#
# @pytest.mark.parametrize('admin, password', user_data)
# def test_open_url1(admin, password):
#     """测试web页面正常打开"""
#     print(admin, password)


class TestDemoA:

    def test_A_001(self):
        # 断言失败
        assert 0

    def test_A_002(self):
        # 从 Failed 获取 test_A_001 的执行结果
        if getattr(FailedCase, 'test_A_001', False):
            pytest.skip('test_A_001 执行失败或被跳过，此用例跳过！')

    def test_A_003(self):
        if getattr(FailedCase, 'test_A_002', False):
            pytest.skip('test_A_002 执行失败或被跳过，此用例跳过！')
        pass


if __name__ == "__main__":
    pytest.main()
