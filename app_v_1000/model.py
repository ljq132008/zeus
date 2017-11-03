#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/27 下午1:46
# @Author  : Liujiaqi
# @Site    :
# @File    : model.py
# @Software: PyCharm
import flask_login
from passlib.apps import custom_app_context as pwd_context

from app import db


class CRM_USER(db.Model, flask_login.UserMixin):
    __tablename__ = 'crm_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128), default='')
    is_active = db.Column(db.Integer, default=0)
    last_login = db.Column(db.DateTime)
    is_staff = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime)
    group_id = db.Column(db.Integer, default=0)
    inception_role = db.Column(db.Integer, default=0)

    def __init__(self, user_name=None, email=None, password=None, is_active=1, last_login=None, is_staff=0, create_time=None, group_id=0, inception_role=0):
        self.user_name = user_name
        self.password = self.set_password(password)
        self.last_login = last_login
        self.email = email
        self.is_staff = is_staff
        self.is_active = is_active
        self.create_time = create_time
        self.group_id = group_id
        self.inception_role = inception_role

    def __repr__(self):
        return '<User %r>' % (self.username)

    @staticmethod
    def set_password(password):
         return pwd_context.encrypt(password)

    def check_password(self, password):
        return pwd_context.verify(password, self.password)

    def is_authenticated(self):
        pass

    def is_active(self):
        """Check the user whether pass the activation process."""
        if self.is_active == 1:
            return True
        else:
            return False

    def is_staff(self):
        if self.is_staff == 1:
            return True
        else:
            return False
    """
    def is_anonymous(self):
        #Check the user's login status whether is anonymous
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False
    """
    def get_id(self):
        # Get the user's uuid from database.
        return unicode(self.id)




class CRM_GROUP(db.Model):
    __tablename__ = 'crm_group'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    group_name = db.Column(db.String(50), unique=True)
    is_active = db.Column(db.Integer)

    def __init__(self, group_name=None, is_active=0):
        self.group_name = group_name
        self.is_active = is_active

    def __repr__(self):
        return '<Group %r>' % (self.group_name)


class CRM_ROLE(db.Model):
    __tablename__ = 'crm_role'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    role_name = db.Column(db.String(50), unique=True)
    is_active = db.Column(db.Integer)
    role_url = db.Column(db.String(200), unique=True)
    role_span = db.Column(db.String(200))

    def __init__(self, role_name=None,is_active=0,role_url=None,role_span=''):
        self.role_name = role_name
        self.role_url = role_url
        self.is_active = is_active
        self.role_span = role_span

    def __repr__(self):
        return '<ROLE %r>' % (self.role_name)

class CRM_GROUP_REF_ROLE(db.Model):
    __tablename__ = 'crm_group_ref_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g_id = db.Column(db.Integer)
    r_id = db.Column(db.Integer)
    is_active = db.Column(db.Integer)

    def __init__(self, r_id=0, g_id=0, is_active=0):
        self.r_id = r_id
        self.g_id = g_id
        self.is_active = is_active

class CRM_ROLE_NODE(db.Model):
    __tablename__ = 'crm_role_node'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    node_name = db.Column(db.String(128), unique=True)
    node_url = db.Column(db.String(128))
    role_id = db.Column(db.Integer)
    sort_id = db.Column(db.Integer)

    def __init__(self, node_name, node_url, role_id, sort_id):
        self.node_name = node_name
        self.node_url = node_url
        self.role_id = role_id
        self.sort_id = sort_id

    def __repr__(self):
        return '<NodeName %r>' % (self.node_name)

class MYSQL_INSTANCES(db.Model):
    __tablename__ = 'mysql_instances'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mysql_host = db.Column(db.String(32), default='localhost')
    mysql_port = db.Column(db.Integer, default=3306)
    mysql_comment = db.Column(db.String(128))
    manage_user = db.Column(db.String(128))
    manage_password = db.Column(db.String(256))
    is_master = db.Column(db.Integer, default=0)
    group_id = db.Column(db.Integer, default=0)
    master_id = db.Column(db.Integer, default=0)

    def __init__(self, mysql_host, mysql_port, mysql_comment, manage_user, manage_password, is_master, group_id, master_id):
        self.mysql_host = mysql_host
        self.mysql_port = mysql_port
        self.mysql_comment = mysql_comment
        self.manage_user = manage_user
        self.manage_password = manage_password
        self.is_master = is_master
        self.group_id = group_id
        self.master_id = master_id

    def __repr__(self):
        return '<mysql_comment %r>' % (str(self.mysql_host)+":"+str(self.mysql_port))


class MYSQL_MONITOR_CONF(db.Model):
    __tablename__ = 'mysql_monitor_conf'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mysql_id = db.Column(db.Integer, default=0)
    monitor_type = db.Column(db.String(32))
    monitor_status = db.Column(db.Integer, default=1)
    monitor_id = db.Column(db.Integer, default=0)

    def __init__(self, mysql_id, monitor_type, monitor_status):
        self.mysql_id = mysql_id
        self.monitor_type = monitor_type
        self.monitor_status = monitor_status

    def __repr__(self):
        return '<mysql_monitory_conf %r>' % self.monitor_type


class MYSQL_ALARM_CONF(db.Model):
    __tablename__ = 'mysql_alarm_conf'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mysql_id = db.Column(db.Integer, default=0)
    alarm_type = db.Column(db.String(32))
    alarm_status = db.Column(db.Integer, default=1)
    alarm_id = db.Column(db.Integer, default=0)

    def __init__(self, mysql_id, alarm_type, alarm_status):
        self.mysql_id = mysql_id
        self.alarm_type = alarm_type
        self.alarm_status = alarm_status

    def __repr__(self):
        return '<mysql_alarm_conf %r>' % self.alarm_type


class MYSQL_CLUSTER(db.Model):
    __tablename__ = 'mysql_group'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cluster_name = db.Column(db.String(128), unique=True)
    ha_type = db.Column(db.String(32), default=None)
    cluster_status = db.Column(db.String(32))
    master_write_status = db.Column(db.String(32), default='OK')
    master_read_status = db.Column(db.String(32), default='OK')
    status_check_time = db.Column(db.DateTime)

    def __init__(self, cluster_name, ha_type, cluster_status, master_write_status, master_read_status, status_check_time):
        self.cluster_name = cluster_name
        self.ha_type = ha_type
        self.cluster_status = cluster_status
        self.master_write_status = master_write_status
        self.master_read_status = master_read_status
        self.status_check_time = status_check_time

    def __repr__(self):
        return '<cluster_name %r>' % (self.group_name)

class MYSQL_PERFORMANCE_QUOTA(db.Model):
    __tablename__ = 'mysql_performance_quota'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    instance_id = db.Column(db.Integer)
    create_time = db.Column(db.DateTime)
    com_select = db.Column(db.Integer)
    com_delete = db.Column(db.Integer)
    questions = db.Column(db.Integer)
    com_insert = db.Column(db.Integer)
    com_commit = db.Column(db.Integer)
    com_rollback = db.Column(db.Integer)
    com_update = db.Column(db.Integer)
    qps = db.Column(db.Integer)
    tps = db.Column(db.Integer)
    threads_running = db.Column(db.Integer)
    threads_connected = db.Column(db.Integer)
    threads_created = db.Column(db.Integer)
    threads_cached = db.Column(db.Integer)
    bytes_received = db.Column(db.Integer)
    bytes_sent = db.Column(db.Integer)
    innodb_buffer_pool_read_requests = db.Column(db.Integer)
    innodb_buffer_pool_reads = db.Column(db.Integer)
    innodb_buffer_pool_pages_flushed = db.Column(db.Integer)
    innodb_data_reads = db.Column(db.Integer)
    innodb_data_writes = db.Column(db.Integer)
    innodb_data_read = db.Column(db.Integer)
    innodb_data_written = db.Column(db.Integer)
    innodb_os_log_fsyncs = db.Column(db.Integer)
    innodb_os_log_written = db.Column(db.Integer)
    innodb_buffer_pool_pages_data = db.Column(db.Integer)
    innodb_buffer_pool_pages_free = db.Column(db.Integer)
    innodb_buffer_pool_pages_dirty = db.Column(db.Integer)

    def __init__(self, instance_id, create_time, com_select, com_delete, questions, com_insert, com_commit, com_rollback, com_update, tps,
                 threads_running,threads_connected,threads_created,threads_cached,bytes_received,bytes_sent,innodb_buffer_pool_read_requests,
                 innodb_buffer_pool_reads,innodb_buffer_pool_pages_flushed,innodb_data_reads,innodb_data_writes,innodb_data_read,innodb_data_written,
                 innodb_os_log_fsyncs,innodb_os_log_written,innodb_buffer_pool_pages_data,innodb_buffer_pool_pages_free,innodb_buffer_pool_pages_dirty):
        self.instance_id = instance_id
        self.create_time = create_time
        self.com_select = com_select
        self.com_delete = com_delete
        self.questions = questions
        self.com_insert = com_insert
        self.com_commit = com_commit
        self.com_rollback = com_rollback
        self.com_update = com_update
        self.qps = questions
        self.tps = tps
        self.threads_running = threads_running
        self.threads_connected =threads_connected
        self.threads_created = threads_created
        self.threads_cached = threads_cached
        self.bytes_received = bytes_received
        self.bytes_sent = bytes_sent
        self.innodb_buffer_pool_read_requests = innodb_buffer_pool_read_requests
        self.innodb_buffer_pool_reads = innodb_buffer_pool_reads
        self.innodb_buffer_pool_pages_flushed = innodb_buffer_pool_pages_flushed
        self.innodb_data_reads = innodb_data_reads
        self.innodb_data_writes = innodb_data_writes
        self.innodb_data_read = innodb_data_read
        self.innodb_data_written = innodb_data_written
        self.innodb_os_log_fsyncs = innodb_os_log_fsyncs
        self.innodb_os_log_written = innodb_os_log_written
        self.innodb_buffer_pool_pages_data = innodb_buffer_pool_pages_data
        self.innodb_buffer_pool_pages_free = innodb_buffer_pool_pages_free
        self.innodb_buffer_pool_pages_dirty = innodb_buffer_pool_pages_dirty

class MYSQL_SLOW_LOG(db.Model):
    __tablename__ = 'mysql_slow_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    instance_id = db.Column(db.Integer)
    query_time = db.Column(db.DateTime)
    last_errno = db.Column(db.String(8))
    rows_examined = db.Column(db.Integer)
    rows_sent = db.Column(db.Integer)
    log_timestamp = db.Column(db.Integer)
    fingerprint_md5 = db.Column(db.String(32))
    bytes_sent = db.Column(db.Integer)
    lock_time = db.Column(db.String(32))
    killed = db.Column(db.Integer)
    cmd_user = db.Column(db.String(32))
    query_sql = db.Column(db.Text)
    cmd_ip = db.Column(db.String(32))
    query_date = db.Column(db.DateTime)
    cmd_schema = db.Column(db.String(32))

    def __init__(self, instance_id, query_time, last_errno, rows_examined, rows_sent, log_timestamp, fingerprint_md5, bytes_sent,
                 lock_time, killed, cmd_user, query_sql, cmd_ip, query_date, cmd_schema):
        self.instance_id = instance_id
        self.query_time = query_time
        self.last_errno = last_errno
        self.rows_examined = rows_examined
        self.rows_sent = rows_sent
        self.log_timestamp = log_timestamp
        self.fingerprint_md5 = fingerprint_md5
        self.bytes_sent = bytes_sent
        self.lock_time = lock_time
        self.killed = killed
        self.cmd_user = cmd_user
        self.query_sql = query_sql
        self.cmd_ip = cmd_ip
        self.query_date = query_date
        self.cmd_schema = cmd_schema

    def __repr__(self):
        return '<slow log instance_id %r>' % (self.instance_id)

class MYSQL_SLOW_QUERY_FINGERPRINT(db.Model):
    __tablename__ = 'mysql_slow_query_fingerprint'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    instance_id = db.Column(db.Integer)
    md5code = db.Column(db.String(32))
    sql_fingerprint = db.Column(db.Text)
    first_apper_time = db.Column(db.DateTime)
    last_apper_time = db.Column(db.DateTime)
    total_number = db.Column(db.Integer)
    status = db.Column(db.Integer, default=0)

    def __init__(self, instance_id, md5code, sql_fingerprint, first_apper_time, last_apper_time, total_number):
        self.instance_id = instance_id
        self.md5code = md5code
        self.sql_fingerprint = sql_fingerprint
        self.first_apper_time = first_apper_time
        self.last_apper_time = last_apper_time
        self.total_number = total_number

class INCEPTION_ROLE(db.Model):
    __tablename__ = 'inception_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(32))
    is_active = db.Column(db.Integer)

    def __init__(self, role_name, is_active):
        self.role_name = role_name
        self.is_active = is_active

class INCEPTION_USER_REF_CLUSTER(db.Model):
    __tablename__ = 'inception_user_ref_cluster'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    u_id = db.Column(db.Integer)
    # 集群id
    c_id = db.Column(db.Integer)

    def __init__(self, u_id, c_id):
        self.u_id = u_id
        self.c_id = c_id

