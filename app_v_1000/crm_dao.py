#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/19 下午3:14
# @Author  : Liujiaqi
# @Site    : 
# @File    : crm_dao.py
# @Software: PyCharm

from .model import CRM_USER, CRM_ROLE_NODE, CRM_GROUP_REF_ROLE, CRM_ROLE
from app import db


class CRM_DAO():

    def getUserById(self, user_id):
        return CRM_USER.query.filter(CRM_USER.id == user_id).first()

    def getUserByUserName(self, userName):
        return CRM_USER.query.filter(CRM_USER.user_name == userName).first()

    def addUser(self, userName, userEmail):
        # 判断用户名和邮箱是否存在，如果存在返回错误相应的错误信息
        # TODO

        user = CRM_USER(user_name='admin_test', email='admin_test@we.com', password='admin', is_active='1',
                        last_login='2017-09-21 00:00:00', is_staff=1, create_time='2017-09-21 00:00:00', group_id=1,
                        inception_role=0)

        db.session.add(user)
        db.session.commit()

    def getUserCommonContextById(self,user_id):
        #获取user对象
        user = self.getUserById(user_id)
        contextList = []
        if user:
            #sqlchemy
            menuObject = CRM_ROLE.query.join(CRM_GROUP_REF_ROLE,CRM_GROUP_REF_ROLE.r_id == CRM_ROLE.id).filter(CRM_GROUP_REF_ROLE.g_id == user.group_id).all()
            if menuObject:
                for menu in menuObject:
                    menuDict = {}
                    menuDict['menuName'] = menu.role_name
                    menuDict['menuUrl'] = menu.role_url
                    menuDict['menuSpan'] = menu.role_span
                    treeNodeList = []
                    treeNode = self.getMenuTreeNode(menu.id)
                    if treeNode:
                        for node in treeNode:
                            treeNodeList.append({'nodeName':node.node_name,'nodeUrl':node.node_url})
                    menuDict['treeNode'] = treeNodeList
                    contextList.append(menuDict.copy())
        return contextList

    def getMenuTreeNode(self,role_id):
        nodes = CRM_ROLE_NODE.query.filter(CRM_ROLE_NODE.role_id == role_id).all()
        return nodes