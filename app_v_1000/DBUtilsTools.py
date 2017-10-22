#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/26 上午12:01
# @Author  : Liujiaqi
# @Site    : 
# @File    : DBUtilsTools.py
# @Software: PyCharm


import MySQLdb
import logging
logger = logging.getLogger('logger01')


class DBSingle:

    def __init__(self, host, port, user, password, db_name='mysql'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db_name = db_name

    def get_connection(self):
        conn = None
        try:
            conn = MySQLdb.connect(host=self.host, port=int(self.port), user=self.user, passwd=self.password)
            return conn
        except MySQLdb.Warning, w:
            logger.warning("MySQL Warning:%s" % str(w))
            return conn
        except MySQLdb.Error, e:
            logger.error("MySQL Warning:%s" % str(e))
            return conn

