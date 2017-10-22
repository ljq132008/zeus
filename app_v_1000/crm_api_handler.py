#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/15 上午11:46
# @Author  : Liujiaqi
# @Site    : 
# @File    : crm_api_handler.py
# @Software: PyCharm

from crm_dao import CRM_DAO
dao = CRM_DAO()

class CrmApiHandler():

    def crm_login(self,userName,password):
        user = dao.getUserByUserName(userName)
        if user:
            if user.user_name == userName and user.password == password:
                return user
            else:
                return None
        else:
            return None

    def crm_get_user_menu(self,user_id):
        return dao.getUserCommonContextById(user_id)

