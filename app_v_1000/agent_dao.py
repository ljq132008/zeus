#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/27 下午1:46
# @Author  : Liujiaqi
# @Site    : 
# @File    : agent_dao.py
# @Software: PyCharm

from .model import MYSQL_INSTANCES, MYSQL_MONITOR_CONF, MYSQL_SLOW_QUERY_FINGERPRINT, MYSQL_SLOW_LOG, MYSQL_PERFORMANCE_QUOTA
from app import db
from flask import current_app


class AgentDao:

    def __init__(self):
        pass

    @staticmethod
    def get_mysql_monitor_conf(host_ip):
        instances = MYSQL_INSTANCES.query.filter(MYSQL_INSTANCES.mysql_host == host_ip).all()

        conf_list = []
        if instances:
            for instance in instances:
                conf_dicts = {}
                conf_dicts['ip'] = instance.mysql_host
                conf_dicts['port'] = instance.mysql_port
                conf_dicts['user'] = instance.manage_user
                conf_dicts['password'] = instance.manage_password
                conf_dicts['id'] = instance.id

                conf = MYSQL_MONITOR_CONF.query.filter(MYSQL_MONITOR_CONF.mysql_id == instance.id).all()

                tmp_list = []
                if conf:
                    for conf in conf:
                        tmp_dict = {}
                        tmp_dict[conf.monitor_type] = conf.monitor_status
                        tmp_list.append(tmp_dict.copy())
                        conf_dicts['configs'] = tmp_list
                    conf_list.append(conf_dicts.copy())
                    current_app.logger.debug(conf_list)
                else:
                    conf_dicts['configs'] = tmp_list
                    conf_list.append(conf_dicts.copy())
        db.session.commit()
        return conf_list

    @staticmethod
    def get_fingerprint(instance_id, md5str):
        printfinger = MYSQL_SLOW_QUERY_FINGERPRINT.query.filter(MYSQL_SLOW_QUERY_FINGERPRINT.instance_id == instance_id, MYSQL_SLOW_QUERY_FINGERPRINT.md5code == md5str).first()
        db.session.commit()
        if printfinger:
            return True
        else:
            return False

    @staticmethod
    def save_slow_log(mysql_id, md5str, event):
        a_slow_log = MYSQL_SLOW_LOG(mysql_id, event['query_time'], event['last_error'], event['rows_examined'], event['rows_sent'],
                                    event['timestamp'], md5str, event['bytes_sent'],
                                    event['lock_time'], event['killed'], event['user'],
                                    event['sql'], event['ip'], event['time'],
                                    event['schema'])
        db.session.add(a_slow_log)
        db.session.commit()

    @staticmethod
    def save_printfinger(mysql_id, md5str, event):
        a_slow_log_printfinger = MYSQL_SLOW_QUERY_FINGERPRINT(mysql_id, md5str, event['fingerprint'], event['time'], event['time'], 1)
        db.session.add(a_slow_log_printfinger)
        db.session.commit()

    @staticmethod
    def update_printfinger_last_time(instance_id, md5str, event):
        printfinger = MYSQL_SLOW_QUERY_FINGERPRINT.query.filter(MYSQL_SLOW_QUERY_FINGERPRINT.instance_id == instance_id and MYSQL_SLOW_QUERY_FINGERPRINT.md5code == md5str).first()
        printfinger.last_apper_time = event['time']
        printfinger.total_number = printfinger.total_number + 1
        db.session.commit()

    @staticmethod
    def save_performance_quota(mysql_id,event):
        a_performance_quota = MYSQL_PERFORMANCE_QUOTA(mysql_id, event['create_time'], event['Com_select'], event['Com_delete'], event['Questions'], event['Com_insert'], event['Com_commit'],
                                                      event['Com_rollback'], event['Com_update'], event['Com_commit']+event['Com_rollback'])
        db.session.add(a_performance_quota)
        db.session.commit()
