#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/10/17 上午10:44
# @Author  : Liujiaqi
# @Site    : 
# @File    : utils.py
# @Software: PyCharm
import hashlib


class Utils:
    def __init__(self):
        pass

    @staticmethod
    def md5string(a_string):
        m2 = hashlib.md5()
        m2.update(a_string)
        return m2.hexdigest()

    @staticmethod
    def send_email(stmp_server='mail.we.com', from_addr='task_admin@we.com', password='M"Pp:0AeS05gK6ng', port=587, to_addr='liujiaqi@we.com', msgText=''):

        def _format_addr(s):
            name, addr = parseaddr(s)
            return formataddr((Header(name, 'utf-8').encode(), addr.encode('utf-8') if isinstance(addr, unicode) else addr))

        import smtplib
        from email.header import Header
        from email.mime.text import MIMEText
        from email.utils import parseaddr, formataddr

        msg = MIMEText(msgText, 'html', 'utf-8')
        msg['From'] = _format_addr(from_addr)
        msg['To'] = _format_addr(to_addr)
        msg['Subject'] = Header(u'ip:port新增慢查询', 'utf-8').encode()

        # SMTP协议默认端口是25 加密端口587
        server = smtplib.SMTP(stmp_server, port)
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        print msg.as_string()
        server.quit()
