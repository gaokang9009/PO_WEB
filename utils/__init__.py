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
SCREENSHOTPATH = os.path.join(ROOTPATH, 'report', 'screen_shot')
ALLUREREPORT = os.path.join(ROOTPATH, 'report', 'allure_report')
ALLURERESULT = os.path.join(ROOTPATH, 'report', 'allure_result')
HTMLREPORT = os.path.join(ROOTPATH, 'report', 'html_report')
