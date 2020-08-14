#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on 2020-
@Author: GaoKang
Project description：
just practice
"""

import os
import utils
from utils import commlib
import traceback


ids, test_datas = commlib.api_data('demo.yaml', 'aaa')


def main():
    """
    主函数
    """
    print(ids)
    print(list(test_datas))
    try:
        assert 1 == 2, 'gaokang'
    except:
        print(traceback.format_exc())
        # print('s')


if __name__ == "__main__":
    main()
