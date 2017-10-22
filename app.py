#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/15 上午11:46
# @Author  : Liujiaqi
# @Site    :
# @File    : app.py
# @Software: PyCharm
from flask import Flask
import flask_login
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = flask_login.LoginManager()


class FlaskApp:

    def __init__(self):
        pass

    @staticmethod
    def create_app():
        app = Flask(__name__)
        # flask SQLAlchemy 配置
        # jsonify
        app.config['JSON_AS_ASCII'] = False
        # json
        app.config['ensure_ascii'] = False
        app.config['SECRET_KEY'] = '123456'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123465@10.20.0.254:3306/zeus?charset=utf8mb4'
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123465@192.168.1.104:3306/zeus?charset=utf8'
        app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        # app.config['SQLALCHEMY_ECHO'] = True
        db.init_app(app)

        # flask login配置
        login_manager = flask_login.LoginManager()
        login_manager.init_app(app)
        login_manager.session_protection = 'strong'

        @login_manager.user_loader
        def load_user(user_id):
            from app_v_1000.model import CRM_USER
            return CRM_USER.query.get(int(user_id))

        from app_v_1000 import api as api_1_0_blueprint
        app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1000')

        return app

if __name__ == '__main__':
    flaskApp = FlaskApp.create_app()
    flaskApp.run(debug=True, host='0.0.0.0', port=5001)
