#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on 2020-
@Author: GaoKang
Project description：
custom define hook function
"""

import os
import pytest
import utils
from utils import commlib
from selenium import webdriver
from web_pages.LoginPage import LoginPage


def pytest_addoption(parser):
    parser.addoption('--env',
                     action='store',
                     dest='environment',
                     default='rmd',
                     help='environment: rmd or macphy')


@pytest.fixture(scope="session")
def env(request):
    """
    get custom config info
    :param request: get environment rmd or macphy
    :return: config object
    """
    environment = request.config.getoption('environment')
    config_dir = 'rmd' if environment == 'rmd' else 'macphy'
    config_path = os.path.join(utils.CONFIGPATH, config_dir, 'global_config.ini')
    return commlib.Config(config_path)


@pytest.fixture(scope="session")
def base_info(env):
    global_config = env
    base_url = global_config.get_config_data('host', 'url')
    page_titie = global_config.get_config_data('init', 'page_title')
    web_driver = global_config.get_config_data('init', 'webdriver')
    print(f'base_info 的base_url是{base_url}!')
    if web_driver.upper() == 'FIREFOX':
        driver = webdriver.Firefox()
    elif web_driver.upper() == 'IE':
        driver = webdriver.Ie()
    else:
        driver = webdriver.Chrome()
    return driver, base_url, page_titie


@pytest.fixture(scope="class")
def init_login_info(env):
    global_config = env
    base_url = global_config.get_config_data('host', 'url')
    page_titie = global_config.get_config_data('init', 'page_title')
    web_driver = global_config.get_config_data('init', 'webdriver')
    username = global_config.get_config_data('superuser', 'username')
    password = global_config.get_config_data('superuser', 'password')
    print(f'init_login_info 的base_url是{base_url}!')
    if web_driver.upper() == 'FIREFOX':
        driver = webdriver.Firefox()
    elif web_driver.upper() == 'IE':
        driver = webdriver.Ie()
    else:
        driver = webdriver.Chrome()
    return driver, base_url, page_titie, username, password


@pytest.fixture(scope='class')
def login_web_class(init_login_info):
    driver, base_url, page_title, username, password = init_login_info
    login_page = LoginPage(driver, base_url, page_title)
    login_page.login_just(username, password)
    yield login_page.driver, login_page.base_url, login_page.page_title
    login_page.quit()


@pytest.fixture(scope='class')
def login_main_page(init_login_info):
    driver, base_url, page_title, username, password = init_login_info
    login_page = LoginPage(driver, base_url, page_title)
    login_page.login_just(username, password)
    login_page.ele_click(login_page.detail_siwitch)
    yield login_page.driver, login_page.base_url, login_page.page_title
    login_page.quit()


@pytest.fixture()
def login_web_func(init_login_info):
    driver, base_url, page_title, username, password = init_login_info
    login_page = LoginPage(driver, base_url, page_title)
    login_page.login_just(username, password)
    yield login_page.driver, login_page.base_url, login_page.page_title
    login_page.quit()


if __name__ == "__main__":
    print(utils.CONFIGPATH)
