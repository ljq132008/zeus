#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/10/18 下午4:35
# @Author  : Liujiaqi
# @Site    : 
# @File    : alarm_dao.py
# @Software: PyCharm

from .model import MYSQL_INSTANCES, MYSQL_ALARM_CONF


class AlarmDao:

    def __init__(self):
        pass

    @staticmethod
    def get_mysql_instance(mysql_id):
        return MYSQL_INSTANCES.query.filter(MYSQL_INSTANCES.id == mysql_id).first()

    @staticmethod
    def get_mysql_alarm_conf(mysql_id, alarm_type):
        return MYSQL_ALARM_CONF.query.filter(MYSQL_ALARM_CONF.mysql_id == mysql_id and MYSQL_ALARM_CONF.alarm_type == alarm_type).first()

