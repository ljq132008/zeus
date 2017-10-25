#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/15 上午11:46
# @Author  : Liujiaqi
# @Site    : 
# @File    : crm_api_handler.py
# @Software: PyCharm

from agent_dao import AgentDao
from flask import current_app
from utils import Utils
from alarm_handler import Alarm
import logging
dao = AgentDao()

logger = logging.getLogger('logger01')


class AgentApiHandler:

    def __init__(self):
        pass

    @staticmethod
    def get_monitor_flag(parameters):
        parameters_dict = eval(parameters)
        current_app.logger.debug(str(parameters_dict))
        conf = dao.get_mysql_monitor_conf(parameters_dict['host_ip'])
        if conf:
            return conf
        else:
            current_app.logger("没有获取到服务器监控配置,需要先配置监控项")
            return None

    @staticmethod
    def push_slow_logs(parameters):
        parameters_dict = eval(parameters)
        current_app.logger.debug(parameters_dict)
        instance_id = int(parameters_dict['mysql_id'])
        for event in parameters_dict['data']:
            md5str = Utils.md5string(event['fingerprint'])
            if AgentApiHandler.handler_fingerprint(md5str, instance_id):
                # 已存在 直接写入slow log
                dao.update_printfinger_last_time(instance_id, md5str, event)
                dao.save_slow_log(instance_id, md5str, event)
            else:
                # 不存在 写入printfinger 写入slow log
                # 判断是否需要发送报警
                if Alarm.check_alarm_status(instance_id, 'slow_log'):
                    Alarm.alarm_slowlog_find_first(instance_id, event['sql'], event['schema'])
                    current_app.logger.info("mysql_id="+str(instance_id)+"实例发现新slow log并发送报警sql:"+str(event['sql'])+"schema:"+str(event['schema']))
                dao.save_printfinger(instance_id, md5str, event)
                dao.save_slow_log(instance_id, md5str, event)
        return '处理成功'

    @staticmethod
    def handler_fingerprint(md5str, instance_id):
        # 通过md5值查看sql是否在fingerprint表中，如果在 直接写入slowlog表 不存在 先写入 fingerprint表
        check_printfinger = dao.get_fingerprint(instance_id, md5str)
        if check_printfinger:
            # 已存在 处理数据并返回TRUE
            return True
        else:
            # 不存在
            return False

    @staticmethod
    def check_alarm_status(conn, instance_id):
        checkAlterDict = {}
        check_sql = 'select alter_slowlog from mysql_instances where id=' + str(instance_id)
        cursor = conn.cursor()
        cursor.execute(check_sql)
        result = cursor.findone()
        checkAlterDict['alter_slowlog'] = True #result[0][0]
        return checkAlterDict

    @staticmethod
    def push_performance_quota(parameters):
        parameters_dict = eval(parameters)
        current_app.logger.debug(parameters_dict)
        instance_id = int(parameters_dict['mysql_id'])
        logger.debug(type(parameters_dict['data']))
        if parameters_dict['data']:
            dao.save_performance_quota(instance_id, parameters_dict['data'])
        return '处理成功'