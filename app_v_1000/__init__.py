#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/19 下午3:10
# @Author  : Liujiaqi
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm

from flask import Blueprint
api = Blueprint('api',__name__)
from . import view