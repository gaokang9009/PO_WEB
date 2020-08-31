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
import re
# from conftest import result_statistics, ResultStatistics
import utils
from utils import commlib

ALLURERESULTTPATH = utils.ALLURERESULT
ALLUREREPORTPATH = utils.ALLUREREPORT
HTMLREPORTTPATH = utils.HTMLREPORT
CASEPATH = utils.CASEPATH
JUNITRESULTPATH = utils.JUNITRESULT
ALLUREENVPATH = utils.ALLUREENV
ALLURERESULTENVPATH = utils.ALLURERESULTENV
cmd_result_path = os.path.join(utils.CMDRESULT, 'cmd_result.txt')


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
    print('执行策略为"{}"'.format(report_opt))
    # allure_results_path = os.path.join(ALLURERESULTTPATH,  'result_'+time.strftime('%Y%m%d%H%M%S'))
    allure_report_name = os.path.join(ALLUREREPORTPATH,  'reports_'+time.strftime('%Y%m%d%H%M%S'))
    html_report_name = os.path.join(HTMLREPORTTPATH,  'reports_'+time.strftime('%Y%m%d%H%M%S') + '.html')
    junit_report_name = os.path.join(JUNITRESULTPATH,  'results.xml')
    allure_cmd_list = ['pytest {} --alluredir {} --clean-alluredir'.format(CASEPATH, ALLURERESULTTPATH),
                       'copy {} {}'.format(ALLUREENVPATH, ALLURERESULTENVPATH),
                       'allure generate {} -o {}'.format(ALLURERESULTTPATH, allure_report_name)]
    # 'allure open {}'.format(allure_report_name)
    html_cmd_list = ['pytest {} --html={} --self-contained-html'.format(CASEPATH, html_report_name)]
    junit_cmd_list = ['pytest -m demo {} --junitxml={}'.format(CASEPATH, junit_report_name)]
    demo_cmd_list = ['pytest -m demo {} --alluredir {} --clean-alluredir'.format(CASEPATH, ALLURERESULTTPATH),
                     'copy {} {}'.format(ALLUREENVPATH, ALLURERESULTENVPATH),
                     'allure generate {} -o {}'.format(ALLURERESULTTPATH, allure_report_name)]
    if report_opt == 'html':
        exec_list = html_cmd_list
    elif report_opt == 'allure':
        exec_list = allure_cmd_list
    elif report_opt == 'junit':
        exec_list = junit_cmd_list
    elif report_opt == 'demo':
        exec_list = demo_cmd_list
    else:
        exec_list = ['pytest {}'.format(CASEPATH)]
    commlib.excute_cmd_echo_out(exec_list)
    # print(f"my test result is: all num {result_statistics.get('all')},passed num {result_statistics.get('passed')},"
    #       f"skipped num {result_statistics.get('skipped')},failed num {result_statistics.get('failed')}")
    # print('class all:::: ', ResultStatistics.all)
    with open(cmd_result_path, encoding='gbk') as f:
        all_info = f.read()
        try:
            result = re.search(r'=\s(\d[^=]*)', all_info).group(1)
        except Exception as e:
            result = 'Do not get result info,please check result from report;'
            print(e)
    commlib.send_email(result, cmd_result_path)
    print('cmd_line result:::: ', result)


def main():
    """
    运行函数
    """
    start_run()


if __name__ == "__main__":
    main()
