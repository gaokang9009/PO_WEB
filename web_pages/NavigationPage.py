#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on 2020-
@Author: GaoKang
Project description：
导航页面元素定义和基本操作定义
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from web_pages.BasePage import BasePage
from web_pages.LoginPage import LoginPage


class NavigationPage(BasePage):

    def __init__(self, driver, base_url, page_title):
        super().__init__(driver, base_url, page_title)
        self.detail_SiwitchButton = (By.ID, 'basic_SiwitchButtonId')
        self.basic_SiwitchButton = (By.XPATH, '//*[@id="ext-gen26"]')

        self.base_loc = (By.ID, 'baseConfigId')
        self.base_tab_loc = (By.XPATH, '//*[@class="x-tab-strip-text icon_devBaseConfig"]')

        self.network_loc = (By.ID, 'networkManagementId')
        self.DHCPRelay_loc = (By.XPATH, '//*[@id="basic_networkManagement_sub"]/button[1]')
        self.DHCPRelay_tab_loc = (By.XPATH, '//*[@class="x-tab-strip-text icon-dhcpRelay"]')
        self.VLAN_loc = (By.XPATH, '//*[@id="basic_networkManagement_sub"]/button[2]')
        self.VLAN_tab_loc = (By.XPATH, '//*[@class="x-tab-strip-text icon-vlan"]')
        self.StaticRoute_loc = (By.XPATH, '//*[@id="basic_networkManagement_sub"]/button[3]')
        self.StaticRoute_tab_loc = (By.XPATH, '//*[@class="x-tab-strip-text icon-staticRoute"]')
        self.LPDHCP_loc = (By.XPATH, '//*[@id="basic_networkManagement_sub"]/button[4]')
        self.LPDHCP_tab_loc = (By.XPATH, '//*[@class="x-tab-strip-text icon-config"]')
        self.Mcast_loc = (By.XPATH, '//*[@id="basic_networkManagement_sub"]/button[5]')
        self.Mcast_tab_loc = (By.XPATH, '//*[@class="x-tab-strip-text icon-config"]')

        self.RF_loc = (By.ID, 'basic_rfInformation')
        self.RfStatus_loc = (By.XPATH, '//*[@id="basic_rfInformation_sub"]/button[1]')
        self.RfStatus_tab_loc = (By.XPATH, '//*[@class="x-tab-strip-text icon-channelMonitor"]')
        self.specGroup_loc = (By.XPATH, '//*[@id="basic_rfInformation_sub"]/button[2]')
        self.specGroup_tab_loc = (By.XPATH, '//*[@class="x-tab-strip-text icon-config"]')
        self.USChannel_loc = (By.XPATH, '//*[@id="basic_rfInformation_sub"]/button[3]')
        self.USChannel_tab_loc = (By.XPATH, '//*[@class="x-tab-strip-text icon-upChannel"]')
        self.DSChannel_loc = (By.XPATH, '//*[@id="basic_rfInformation_sub"]/button[4]')
        self.DSChannel_tab_loc = (By.XPATH, '//*[@class="x-tab-strip-text icon-downChannel"]')

        self.TerminalDev_loc = (By.ID, 'TerminalDevMgmtId')
        self.CMCPEList_loc = (By.XPATH, '//*[@id="basic_TerminalDevMgmt_sub"]/button[1]')
        self.CMCPEList_tab_loc = (By.XPATH, '//*[@class="x-tab-strip-text icon-cm"]')
        self.CMList_loc = (By.XPATH, '//*[@id="basic_TerminalDevMgmt_sub"]/button[2]')
        self.CMList_tab_loc = (By.XPATH, '//*[@class="x-tab-strip-text icon-remoteQuery"]')

        self.logView_loc = (By.ID, 'logViewId')
        self.logView_tab_loc = (By.XPATH, '//*[@class="x-tab-strip-text icon-logShow"]')

        self.tab_close_loc = (By.XPATH, '//*[@class="x-tab-strip x-tab-strip-top"]/li[3]/*[@class="x-tab-strip-close"]')

    def open_tab(self, ele_class, ele):
        self.move_to_ele(ele_class)
        self.force_wait(1)
        self.ele_click(ele)
        self.force_wait(1)

    def close_tab(self):
        self.ele_click(self.tab_close_loc)

    def tab_txt(self, ele):
        return self.ele_text(ele)

    @property
    def ele_dict(self):
        dict_x = {'base_loc': self.base_loc, 'base_tab_loc': self.base_tab_loc, 'network_loc': self.network_loc,
                  'DHCPRelay_loc': self.DHCPRelay_loc, 'DHCPRelay_tab_loc': self.DHCPRelay_tab_loc,
                  'VLAN_loc': self.VLAN_loc, 'VLAN_tab_loc': self.VLAN_tab_loc,
                  'StaticRoute_loc': self.StaticRoute_loc, 'StaticRoute_tab_loc': self.StaticRoute_tab_loc,
                  'LPDHCP_loc': self.LPDHCP_loc, 'LPDHCP_tab_loc': self.LPDHCP_tab_loc, 'Mcast_loc': self.Mcast_loc,
                  'Mcast_tab_loc': self.Mcast_tab_loc, 'RF_loc': self.RF_loc, 'RfStatus_loc': self.RfStatus_loc,
                  'RfStatus_tab_loc': self.RfStatus_tab_loc, 'specGroup_loc': self.specGroup_loc,
                  'specGroup_tab_loc': self.specGroup_tab_loc, 'USChannel_loc': self.USChannel_loc,
                  'USChannel_tab_loc': self.USChannel_tab_loc, 'DSChannel_loc': self.DSChannel_loc,
                  'DSChannel_tab_loc': self.DSChannel_tab_loc, 'TerminalDev_loc': self.TerminalDev_loc,
                  'CMCPEList_loc': self.CMCPEList_loc, 'CMCPEList_tab_loc': self.CMCPEList_tab_loc,
                  'CMList_loc': self.CMList_loc, 'CMList_tab_loc': self.CMList_tab_loc,
                  'logView_loc': self.logView_loc, 'logView_tab_loc': self.logView_tab_loc,
                  'detail_SiwitchButton':self.detail_SiwitchButton, 'basic_SiwitchButton':self.basic_SiwitchButton,
                  }
        return dict_x


def main():
    """
    主函数
    """
    driver = webdriver.Chrome()
    base_url = 'http://120.0.60.7'
    page_title = '管理系统'
    login_web = LoginPage(driver, base_url, page_title)
    login_web.open_url()
    login_web.input_username('admin')
    login_web.input_password('admin')
    login_web.login_submit()
    login_web.force_wait(2)

    Navigation = NavigationPage(driver, base_url, page_title)

    Navigation.open_tab(Navigation.base_loc, Navigation.base_loc)
    print(Navigation.tab_txt(Navigation.base_tab_loc))
    Navigation.close_tab()

    Navigation.open_tab(Navigation.network_loc, Navigation.DHCPRelay_loc)
    print(Navigation.tab_txt(Navigation.DHCPRelay_tab_loc))
    Navigation.close_tab()

    Navigation.open_tab(Navigation.network_loc, Navigation.VLAN_loc)
    print(Navigation.tab_txt(Navigation.VLAN_tab_loc))
    Navigation.close_tab()

    Navigation.force_wait(2)
    driver.quit()


if __name__ == "__main__":
    main()
