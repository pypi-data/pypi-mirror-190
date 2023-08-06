# -*- coding: utf-8 -*-

import os
import re

from .file import get_file_line


def is_ip(str):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(str):
        return True
    else:
        return False


# 判断数据是否在数据里面
def is_res(type, str):
    for item in get_file_line(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res', type + '.data')):
        if item in str:
            return item

    return False
