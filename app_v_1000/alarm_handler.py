#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/10/17 上午11:07
# @Author  : Liujiaqi
# @Site    : 
# @File    : alarm_handler.py
# @Software: PyCharm

from utils import Utils
from DBUtilsTools import DBSingle
from app_v_1000.alarm_dao import AlarmDao
from flask import current_app
import MySQLdb
import logging
logger = logging.getLogger('logger01')


class Alarm:

    def __init__(self):
        pass

    @staticmethod
    def check_alarm_status(mysql_id, alarm_type):
        alarm = AlarmDao.get_mysql_alarm_conf(mysql_id, alarm_type)
        if alarm:
            if alarm.alarm_status:
                current_app.logger.info("mysql_id:"+str(mysql_id)+"实例发现告警项:"+str(alarm_type))
                return True
            else:
                current_app.logger.info("mysql_id:" + str(mysql_id) + "实例未发现告警项:" + str(alarm_type))
                return False
        else:
            current_app.logger.info("mysql_id:" + str(mysql_id) + "实例未发现告警项:" + str(alarm_type))
            return False

    @staticmethod
    def alarm_slowlog_find_first(instance_id, found_sql, schema):
        if schema == 'null':
            schema = 'mysql'

        a_mysql = AlarmDao.get_mysql_instance(instance_id)
        conn = DBSingle(a_mysql.mysql_host, int(a_mysql.mysql_port), a_mysql.manage_user, a_mysql.manage_password, schema).get_connection()
        # 获取sql的explain
        cursor = conn.cursor()
        cursor.execute('use ' + str(schema) + ';')
        result = None
        try:
            cursor.execute('explain ' + str(found_sql))
            result = cursor.fetchall()
        except MySQLdb.Error, e:
            logger.error("MySQL Error:%s" % str(e))

        td_str = '<tr>'
        if result:
            for item in result:
                tmp_str = ''
                for td in range(len(item)):
                    if not item[td]:
                        tmp_str = tmp_str + "<td>NULL</td>"
                    else:
                        tmp_str = tmp_str + "<td>" + str(item[td]) + "</td>"
                print "tmp_str=" + tmp_str
                td_str = td_str + tmp_str + "</tr>"
        html_string_head = """<html>
                                <body>
                                    <table border="1">
                                        <tr><th>id</td><th>select_type</th><th>table</th><th>type</th><th>possible_keys</th><th>key</th><th>key_len</th><th>ref</th><th>rows</th><th>Extra</th></tr>"""
        html_string_tail = '</table></body></html>'
        full_info_str = "mysql实例：" + str(a_mysql.mysql_host) + ":" + str(a_mysql.mysql_port) + "<br/> schema:" + str(schema) + "<br/>发现新慢SQL:" + str(found_sql) + "<br/>执行计划:<br/>" \
                        + html_string_head + str(td_str) + html_string_tail
        Utils.send_email(stmp_server='mail.we.com', from_addr='task_admin@we.com', password='M"Pp:0AeS05gK6ng', port=587, to_addr='liujiaqi@we.com', msgText=full_info_str)
