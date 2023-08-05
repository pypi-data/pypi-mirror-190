import requests
from flask import current_app,request
from .util import jsonres

app = current_app()

host = request.host

class CoreController:
    # @self.app.route("/xyadmin/")
    def xyadmin():
        url = "https://uiadmin.net/xyadmin/?version=1.3.0"
        res = requests.get(url)
        return res.text

    # @app.route("/xyadmin/api")
    def xyadmin_api():
        # 返回json数据的方法
        data = {
            "code": 200,
            "msg": "success",
            "data": {
                "framework": "flask",
                "stype": "应用",
                "name": "uiadmin",
                "api": {
                    "apiLogin": "/v1/admin/user/login",
                    "apiConfig": "/v1/site/info",
                    "apiBase": host + "/api",
                    "apiUserInfo": "/v1/admin/user/info",
                    "apiAdmin": "/v1/admin/index/index",
                    "apiMenuTrees": "/v1/admin/menu/trees"
                },
                "lang": "python",
                "title": app.config['UIADMIN_SITE_TITLE'],
                "domainRoot": host,
                "siteInfo": {
                    "title": app.config['UIADMIN_SITE_TITLE']
                },
                "version": app.config['UIADMIN_SYTE_VERSION'],
                "config": {
                    "useVerify": "",
                    # "headerRightToolbar": [
                    #         {
                    #             "type": "url",
                    #             "title": "接口文档",
                    #             "class": "xyicon xyicon-map",
                    #             "url": "/doc.html"
                    #         }
                    # ]
                }
            }
        }
        return jsonres(data)
    
    @app.route("/api/v1/admin/user/login", methods=["post"])
    def admin_login():
        # 返回json数据的方法
        data = {
            "code": 200,
            "msg": "登录成功",
            "data": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI",
                "userInfo": {
                    "id": 1,
                    "nickname": "admin",
                    "username": "admin",
                    "avatar": "",
                    "roles": "",
                    "status": 1,
                    "authorities": ["ROLE_SUPER_ADMIN"]
                }
            }
        }
        return jsonres(data)
    
    @app.route("/api/v1/admin/index/index")
    def admin_index():
        data = {
            "code": 200,
            "msg": "success",
            "data": {
                "dataList": [
                    {
                            "type": "count",
                            "content": [
                                {
                                    "item": {
                                        "bgColor": "#2db7f5",
                                        "icon": "ivu-icon ivu-icon-md-contacts",
                                        "title": ""
                                    },
                                    "current": {
                                        "suffix": "",
                                        "value": "0"
                                    },
                                    "content": {
                                        "value": "注册用户"
                                    }
                                },
                                {
                                    "item": {
                                        "bgColor": "#19be6b",
                                        "icon": "ivu-icon ivu-icon-md-person-add",
                                        "title": ""
                                    },
                                    "current": {
                                        "suffix": "",
                                        "value": "0"
                                    },
                                    "content": {
                                        "value": "今日新增"
                                    }
                                },
                                {
                                    "item": {
                                        "bgColor": "#ff9900",
                                        "icon": "ivu-icon ivu-icon-md-clock",
                                        "title": ""
                                    },
                                    "current": {
                                        "suffix": "",
                                        "value": "0"
                                    },
                                    "content": {
                                        "value": "总消费"
                                    }
                                },
                                {
                                    "item": {
                                        "bgColor": "#ed4014",
                                        "icon": "ivu-icon ivu-icon-ios-paper-plane",
                                        "title": ""
                                    },
                                    "current": {
                                        "suffix": "",
                                        "value": "0"
                                    },
                                    "content": {
                                        "value": "今日消费"
                                    }
                                }
                            ],
                            "span": 24
                    },
                    {
                            "type": "card",
                            "title": "系统信息",
                            "content": [
                                {
                                    "type": "text",
                                    "title": "服务器IP",
                                    "value": ""
                                },
                                {
                                    "type": "text",
                                    "title": "WEB服务器",
                                    "value": ""
                                },
                                {
                                    "type": "text",
                                    "title": "JDK版本",
                                    "value": ""
                                },
                                {
                                    "type": "text",
                                    "title": "服务器时间",
                                    "value": ""
                                },
                                {
                                    "type": "text",
                                    "title": "官方网站",
                                    "value": "https://jiangruyi.com(ijry@qq.com)"
                                }
                            ],
                            "span": 12
                    },
                    {
                            "type": "card",
                            "title": "项目信息",
                            "content": [
                                {
                                    "type": "text",
                                    "title": "项目名称",
                                    "value": ""
                                },
                                {
                                    "type": "text",
                                    "title": "项目口号",
                                    "value": ""
                                },
                                {
                                    "type": "text",
                                    "title": "项目简介",
                                    "value": ""
                                },
                                {
                                    "type": "text",
                                    "title": "ICP备案号",
                                    "value": ""
                                }
                            ],
                            "span": 12
                    }
                ]
            }
        }
        return jsonres(data)
 