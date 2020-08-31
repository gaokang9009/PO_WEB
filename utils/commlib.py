#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on 2020-
@Author: GaoKang
Project description：定义工具函数
"""

import utils
import os
import time
import configparser
import yaml
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart


class Config(object):
    """
    定义读取config目录的下配置文件类
    """
    def __init__(self, cfg_path):
        """
        定义构造函数
        :param cfg_path:配置文件路径
        """
        self.cfg_path = cfg_path
        self.config = configparser.ConfigParser()

    def get_config_data(self, section, key):
        """
        定义读取信息方法
        :param section:ini文件中的section
        :param key: ini文件中对应section下的key
        :return: 返回key对应的value
        """
        get_data = None
        if not self.config.read(self.cfg_path, encoding='utf-8-sig'):
            # 判断文件是否存在
            print('"{}" is not exists.'.format(self.cfg_path))
        else:
            try:
                get_data = self.config.get(section, key)
                # 读取config中ection下key对应的value值
            except Exception as e:
                print('"{}" file do not have the config which section is "{}" key is "{}", '
                      .format(self.cfg_path, section, key), e)
        return get_data

    def set_config_data(self, section, key, value):
        """
        定义写入信息方法
        :param section:ini文件中的section
        :param key: ini文件中对应section下的key
        :param value: ini文件中对应section下key对应的value
        :return: 返回写入是否成功
        """
        if section not in self.config.sections():
            self.config.add_section(section)
        try:
            self.config.set(section, key, value)
        except Exception as e:
            print('"{}" file add config failed, which section is "{}" key is "{}" value is {}, '
                  .format(self.cfg_path, section, key, value), e)
            return False
        else:
            with open(self.cfg_path, 'w', encoding='utf-8') as f:
                self.config.write(f)
            return True


def api_data(yaml_filename, key_x):
    """
    读取并返回yaml数据信息
    :param yaml_filename: 测试数据文件yaml的文件名
    :param key_x: yaml文件中一级key值
    :return: 返回用例名称的列表 和 测试数据与预期结果的列表元组
    """
    test_data_path = os.path.join(utils.DATAPATH, yaml_filename)
    case = []  # 测试用例名称
    data = []  # 请求对象
    expected = []  # 预期结果
    with open(test_data_path, 'r', encoding='UTF-8') as f:
        test_data = yaml.load(f.read(), Loader=yaml.SafeLoader)
    try:
        tests = test_data[key_x]
        for test_n in tests:
            case.append(test_n.get('case', ''))
            data.append(test_n.get('data', {}))
            expected.append(test_n.get('expected', {}))
        parameters = zip(case, data, expected)
    except Exception:
        raise KeyError(f'YAML文件{test_data_path},不存在key值->{key_x}')
    return case, parameters


def api_normal_data(yaml_filename, key_x):
    """
    读取并返回yaml简单数据信息
    :param yaml_filename: 测试数据文件yaml的文件名
    :param key_x: yaml文件中一级key值
    :return: 返回用例名称的列表 和 测试数据与预期结果的列表元组
    """
    test_data_path = os.path.join(utils.DATAPATH, yaml_filename)
    with open(test_data_path, 'r', encoding='UTF-8') as f:
        test_data = yaml.load(f.read(), Loader=yaml.SafeLoader)
    try:
        tests = test_data[key_x]
        case = tests[0].get('case', '')
        data = tests[0].get('data', {})
        expected = tests[0].get('expected', {})
    except Exception:
        raise KeyError(f'YAML文件{test_data_path},不存在key值->{key_x}')
    return case, data, expected


def excute_cmd_echo_out(cmd_list):
    """
    驱动Windows CMD执行命令
    :param cmd_list:所需执行的命令列表
    :return:None
    """
    cmd_result_path = os.path.join(utils.CMDRESULT, 'cmd_result.txt')
    with open(cmd_result_path, mode='w') as f:
        f.write('Result of CMD({}):\n\n'.format(time.strftime('%Y-%m-%d_%X')))
    for cmd in cmd_list:
        print(cmd)
        with open(cmd_result_path, mode='a') as f:
            f.write(cmd + '\n\n')
        with os.popen(cmd) as result:
            while True:
                result_echo = result.read()
                if result_echo:
                    print(result_echo)
                    with open(cmd_result_path, mode='a') as f:
                        f.write(result_echo + '\n\n')
                else:
                    break


def send_email(content_text, file_name):
    smtp = smtplib.SMTP(host='192.168.1.11')
    smtp.login(user='gaokangkang', password='gk40180')
    # 构建一封多组件的邮件
    msg = MIMEMultipart()
    msg['From'] = "<gaokangkang@dvt.dvt.com>"
    msg['To'] = "<gaokangkang@dvt.dvt.com>"
    msg['Subject'] = Header("web自动化测试报告", charset='utf-8')
    text_content = MIMEText('''Hi：
     测试已完成；概要信息如下
         {}
    
    CMD测试打印结果见附件；
    
    更详细的报告请查阅HTML或ALLURE系统报告；

                    谢谢！'''.format(content_text), _charset='utf-8')
    with open(file_name, 'rb') as f:
        f_msg = f.read()
    app = MIMEApplication(f_msg)
    app.add_header('content-disposition', 'attachment', filename=os.path.split(file_name)[1])
    msg.attach(text_content)
    msg.attach(app)
    smtp.send_message(msg=msg, from_addr="gaokangkang@dvt.dvt.com",
                      to_addrs=['gaokangkang@dvt.dvt.com'])
    smtp.quit()


def main():
    """
    测试函数
    """
    global_config_path = os.path.join(utils.CONFIGPATH, 'rmd', 'global_config.ini')
    config = Config(global_config_path)
    print(config.get_config_data('init', 'environment'))
    print(config.get_config_data('host1', 'url'))
    print(config.set_config_data('authentication', 'uid', 'gaokang'))
    print(config.set_config_data('hosta', 'url1', 'gaokang'))

    case, parameters = api_data('login_data.yaml')
    print(case)
    for para in parameters:
        print(para)


if __name__ == "__main__":
    main()
