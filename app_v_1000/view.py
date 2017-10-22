#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/21 上午11:49
# @Author  : Liujiaqi
# @Site    : 
# @File    : view.py
# @Software: PyCharm
from crm_dao import CRM_DAO
from flask import request, jsonify, current_app
from crm_api_handler import CrmApiHandler
from agent_api_handler import AgentApiHandler
from flask_login import login_required,login_user,current_user,logout_user
from . import api

dao = CRM_DAO()
handler = CrmApiHandler()
agentHandler = AgentApiHandler()


@api.route('/login', methods=['POST'])
def login_in():
    fun_name = request.form.get('funName')
    parameters = request.form.get('parameters')

    if (not fun_name) or (not parameters):
        return jsonify({'statusCode': 400, 'message': '参数错误'})
    else:
        # 参数正常传入相应处理函数进一步验证
        if fun_name == 'login':
            parameters_dict = eval(parameters)
            username = parameters_dict['username']
            password = parameters_dict['password']
            if (not username) or (not password):
                return jsonify({'statusCode': 400, 'message': '用户名或密码不能为空'})
            else:
                user = handler.crm_login(username, password)
                if user:
                    login_user(user)
                    return jsonify({'statusCode': 200, 'message': '登录成功'})
                else:
                    return jsonify({'statusCode': 401, 'message': '登录失败'})

        else:
            return jsonify({'statusCode': 400, 'message': '登录标识参数错误'})


@api.route('/logout', methods=['POST'])
@login_required
def logout():
    print current_user.user_name
    logout_user()
    return jsonify({'statusCode': 200, 'message': '用户登出成功'})


# 用户权限相关的 api 控制器
@api.route('/crm', methods=['POST','GET'])
@login_required
def crm_controller():
    # 解析post表单2个参数 funName 、 parameters
    fun_name = request.form.get('funName')
    parameters = request.form.get('parameters')

    if (not fun_name) or (not parameters):
        return jsonify({'statusCode': 400, 'message': '参数错误'})
    else:
        if fun_name == 'getMenu':
            resp_data = handler.crm_get_user_menu(current_user.id)
            return jsonify(resp_data)
        elif fun_name == 'addUser':
            handler.crm_add_user(parameters)
        else:
            pass


@api.route('/agent', methods=['POST', 'GET'])
def agent_controller():
    # 解析post表单2个参数 funName,parameters
    fun_name = request.form.get('funName')
    parameters = request.form.get('parameters')
    current_app.logger.debug(parameters)
    current_app.logger.debug(fun_name)
    if (not fun_name) or (not parameters):
        return jsonify({'statusCode': 400, 'message': '参数错误'})
    else:
        if fun_name == 'getMonitorConf':
            return jsonify(agentHandler.get_monitor_flag(parameters))
        if fun_name == 'pushSlowLogs':
            return jsonify(agentHandler.push_slow_logs(parameters))

