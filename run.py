#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020-
@Author: GaoKang
Project description：
执行测试用例
"""

import sys
import os
import time
import utils
from utils import commlib

ALLURERESULTTPATH = utils.ALLURERESULT
ALLUREREPORTPATH = utils.ALLUREREPORT
HTMLREPORTTPATH = utils.HTMLREPORT
CASEPATH = utils.CASEPATH


def get_report_opt():
    para_list = sys.argv
    report_opt = None
    if len(para_list) > 1:
        report_opt = para_list[1]
    return report_opt


def start_run():
    """
    运行函数
    :return:
    """
    report_opt = get_report_opt()
    # allure_results_path = os.path.join(ALLURERESULTTPATH,  'result_'+time.strftime('%Y%m%d%H%M%S'))
    # allure_reports_path = os.path.join(ALLUREREPORTPATH, 'report'+time.strftime('%Y%m%d%H%M%S'))
    allure_report_name = os.path.join(ALLUREREPORTPATH,  'reports_'+time.strftime('%Y%m%d%H%M%S'))
    html_report_name = os.path.join(HTMLREPORTTPATH,  'reports_'+time.strftime('%Y%m%d%H%M%S') + '.html')
    allure_cmd_list = ['pytest {} --alluredir {} --clean-alluredir'.format(CASEPATH, ALLURERESULTTPATH),
                       'allure generate {} -o {}'.format(ALLURERESULTTPATH, allure_report_name)]
    html_cmd_list = ['pytest {} --html={} --self-contained-html'.format(CASEPATH, html_report_name)]
    # 'allure open {}'.format(allure_reports_path)
    demo_cmd_list = ['pytest -m demo {} --alluredir {} --clean-alluredir'.format(CASEPATH, ALLURERESULTTPATH),
                     'allure generate {} -o {}'.format(ALLURERESULTTPATH, allure_report_name)]
    if report_opt == 'html':
        exec_list = html_cmd_list
    elif report_opt == 'allure':
        exec_list = allure_cmd_list
    elif report_opt == 'demo':
        exec_list = demo_cmd_list
    else:
        exec_list = ['pytest {}'.format(CASEPATH)]
    commlib.excute_cmd_echo_out(exec_list)


def main():
    """
    运行函数
    """
    start_run()


if __name__ == "__main__":
    main()
