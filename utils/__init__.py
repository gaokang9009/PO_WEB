#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on 2020-
@Author: GaoKang
Project description：
"""
import os

ROOTPATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
CONFIGPATH = os.path.join(ROOTPATH, 'config')
DATAPATH = os.path.join(ROOTPATH, 'web_datas')
PAGEPATH = os.path.join(ROOTPATH, 'web_pages')
CASEPATH = os.path.join(ROOTPATH, 'web_cases')
REPORTTPATH = os.path.join(ROOTPATH, 'report')
CMDRESULT = os.path.join(ROOTPATH, 'report', 'cmd_result')
SCREENSHOTPATH = os.path.join(ROOTPATH, 'report', 'screen_shot')
ALLUREREPORT = os.path.join(ROOTPATH, 'report', 'allure_report')
ALLURERESULT = os.path.join(ROOTPATH, 'report', 'allure_result')
HTMLREPORT = os.path.join(ROOTPATH, 'report', 'html_report')
JUNITRESULT = os.path.join(ROOTPATH, 'report', 'junit_result')
ALLUREENV = os.path.join(ROOTPATH, 'utils', 'environment.properties')
ALLURERESULTENV = os.path.join(ALLURERESULT, 'environment.properties')
