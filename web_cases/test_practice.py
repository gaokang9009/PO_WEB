#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on 2020-
@Author: GaoKang
Project description：
测试LoginPage页面
"""

import pytest

user_data = [('admin', 1), ('pass', 2)]


@pytest.fixture(scope='function', params=user_data)
def login(request):
    return request.param[0], request.param[1]


def test_open_url(login):
    """测试web页面正常打开"""
    login_page, ele_dict = login
    print(login_page, ele_dict)


@pytest.mark.parametrize('admin, password', user_data)
def test_open_url1(admin, password):
    """测试web页面正常打开"""
    print(admin, password)


if __name__ == "__main__":
    pytest.main()
