#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on 2020-
@Author: GaoKang
Project description：
custom define hook function
"""

import os
import re
import time
import pytest
import utils
import allure
from _pytest import terminal
from utils import commlib
from selenium import webdriver
from web_pages.LoginPage import LoginPage


driver = None
failure_cases = os.path.join(utils.REPORTTPATH, "failure_cases")
result_statistics = {'all': 0, 'passed': 0, 'failed': 0, 'skipped': 0, 'xfail': 0, 'xpass': 0}


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
    global driver
    global_config = env
    base_url = global_config.get_config_data('host', 'url')
    page_titie = global_config.get_config_data('init', 'page_title')
    web_driver = global_config.get_config_data('init', 'webdriver')
    print(f'base_info 的 base_url是{base_url}!')
    if web_driver.upper() == 'FIREFOX':
        driver = webdriver.Firefox()
    elif web_driver.upper() == 'IE':
        driver = webdriver.Ie()
    else:
        driver = webdriver.Chrome()
    return driver, base_url, page_titie


@pytest.fixture(scope="class")
def init_login_info(env):
    global driver
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
    driver_x, base_url, page_title, username, password = init_login_info
    login_page = LoginPage(driver_x, base_url, page_title)
    login_page.login_just(username, password)
    yield login_page.driver, login_page.base_url, login_page.page_title
    login_page.quit()


@pytest.fixture(scope='class')
def login_main_page(init_login_info):
    driver_x, base_url, page_title, username, password = init_login_info
    login_page = LoginPage(driver_x, base_url, page_title)
    login_page.login_just(username, password)
    login_page.ele_click(login_page.detail_siwitch)
    yield login_page.driver, login_page.base_url, login_page.page_title
    login_page.quit()


@pytest.fixture()
def login_web_func(init_login_info):
    driver_x, base_url, page_title, username, password = init_login_info
    login_page = LoginPage(driver_x, base_url, page_title)
    login_page.login_just(username, password)
    yield login_page.driver, login_page.base_url, login_page.page_title
    login_page.quit()


class FailedCase:
    """
    记录失败case
    """
    skip = False


class ResultStatistics:
    """
    统计case结果
    """
    all = 0
    passed = 0
    failed = 0
    skipped = 0


@pytest.fixture(scope='session', autouse=True)
def generate_failure_cases_file():
    with open(failure_cases, mode='w') as f:
        f.write('Failure cases({}):\n\n'.format(time.strftime('%Y-%m-%d_%X')))


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    result_statistics = {'all': 0, 'passed': 0, 'failed': 0, 'skipped': 0, 'xfail': 0, 'xpass': 0}
    获取每个用例状态的钩子函数，对用例结果进行统计，并对于失败的用例进行记录和截图
    :param item: 测试用例
    :param call: 测试步骤
    :return: None
    """
    # 获取钩子方法的调用结果
    outcome = yield
    report = outcome.get_result()
    # 仅仅获取用例call执行结果是失败的情况,不包含 setup/teardown
    # if report.when == "call" and report.failed:
    global result_statistics
    if report.when == "setup":
        result_statistics['all'] += 1
        ResultStatistics.all += 1
        if report.outcome == 'skipped':
            result_statistics['skipped'] += 1
            with open(failure_cases, mode='a') as f:
                f.write(report.nodeid + ',result: call skipped! ' + "\n")
    if report.when == "call":
        if report.outcome == 'passed':
            result_statistics['passed'] += 1
        if "data" in item.fixturenames:
            extra = ",具体参数为:(%s)" % item.funcargs["data"]
        else:
            extra = ""
        if report.outcome == 'skipped':
            result_statistics['skipped'] += 1
            with open(failure_cases, mode='a') as f:
                f.write(report.nodeid + extra + ',result: call skipped! ' + "\n")
        if report.outcome == 'failed':
            result_statistics['failed'] += 1
            # 添加allure报告截图
            with allure.step('添加失败截图'):
                allure.attach(driver.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)
            with open(failure_cases, mode='a') as f:
                f.write(report.nodeid + extra + ',result: call failed! ' + "\n")
    # print(result_statistics)
    if report.when in ('call', 'setup') and report.outcome in ('failed', 'skipped'):
        # 当某个用例失败时(setup失败也算)或被跳过时，将这个用例的执行结果存储在 Failed 类中
        case_name = report.nodeid.split('::')[-1]
        if 'web登陆成功' not in case_name:
            case_name = re.sub(r'\[.*\]', '', report.nodeid.split('::')[-1])
        setattr(FailedCase, case_name, True)


# def pytest_terminal_summary(terminalreporter, existstatus, config):
#     """
#     调用结果统计
#     """
#     total = terminalreporter.stats
#     print("total:", terminalreporter._numcollected)
#     print('passed:', len(terminalreporter.stats.get('passed', [])))
#     print('failed:', len(terminalreporter.stats.get('failed', [])))
#     print('error:', len(terminalreporter.stats.get('error', [])))
#     print('skipped:', len(terminalreporter.stats.get('skipped', [])))
#     # terminalreporter._sessionstarttime 会话开始时间
#     duration = time.time() - terminalreporter._sessionstarttime
#     print('total times:', duration, 'seconds')


@pytest.fixture(scope='class')
def check_login_ok():
    """测试web能够正常登陆"""
    if getattr(FailedCase, 'test_login[用户名与密码匹配时测试web登陆成功]', False):
        pytest.skip('"test_login[用户名与密码匹配时测试web登陆成功]"执行失败或被跳过，web登陆失败，此用例跳过！')


if __name__ == "__main__":
    print(utils.CONFIGPATH)
