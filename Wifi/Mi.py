#!/usr/bin/python3
import time
import requests
from requests.adapters import HTTPAdapter
import random
from Crypto.Hash import SHA
import json
import re

from . import config, util, base, exception


class Mi:
    """
    Mi 小米 wifi 工具
    """

    def __init__(self, filepath):
        # 配置文件位置
        self.filepath = filepath
        self.hasLogin = False
        self.LoginTime = int(time.time_ns() / 1000)
        self.token = ""
        # 读取配置
        conf = config.Config()
        conf.Load(self.filepath)
        # 加载配置文件
        self.password = conf.password
        self.route_ip = conf.route_ip
        self.max_retries = conf.max_retries
        self.timeout = conf.timeout
        self.reqTimeout = conf.reqTimeout

    def checkLogin(self):
        if not self.hasLogin or util.getTimestamp() - self.LoginTime > self.timeout:
            self.Login()

    def Login(self):
        token = self.getToken()
        if len(token) != 0:
            self.token = token
            self.LoginTime = util.getTimestamp()
            self.hasLogin = True
            print("Login success! token=", token)
        else:
            raise exception.ReqError("Login failed!")

    def List(self):
        """
        ls 查看链接到 wifi 的设备列表
        :return:
        """
        self.checkLogin()
        s = self.getSession()
        url = self.getUrl('/api/misystem/devicelist')
        resp = s.get(url, timeout=self.reqTimeout)
        devices = json.loads(resp.content)
        return devices

    def GetNetThrough(self):
        self.checkLogin()
        s = self.getSession()
        url = self.getUrl('/api/xqnetwork/portforward?ftype=1')
        resp = s.get(url, timeout=self.reqTimeout)
        config = json.loads(resp.content)
        return config

    def AddNetThrough(self):
        self.checkLogin()
        pass

    def EnableNetThrough(self):
        self.checkLogin()
        pass

    # 模拟登陆获取token
    def getToken(self):
        # 创建请求对象
        s = self.getSession()
        route_url = 'http://' + self.route_ip

        # 获取nonce和mac_addr
        req = s.get(route_url + '/cgi-bin/luci/web', timeout=self.reqTimeout)
        key = re.findall(r'key: \'(.*)\',', req.text)[0]
        mac_addr = re.findall(r'deviceId = \'(.*)\';', req.text)[0]
        nonce = "0_" + mac_addr + "_" + str(int(time.time())) + "_" + str(random.randint(1000, 10000))
        # 第一次加密 对应CryptoJS.SHA1(pwd + this.key)
        password_encrypt1 = SHA.new()
        password_encrypt1.update((self.password + key).encode('utf-8'))
        # 第二次加密对应 CryptoJS.SHA1(this.nonce + CryptoJS.SHA1(pwd + this.key).toString()).toString();
        password_encrypt2 = SHA.new()
        password_encrypt2.update((nonce + password_encrypt1.hexdigest()).encode('utf-8'))
        hexpwd = password_encrypt2.hexdigest()

        data = {
            "logtype": 2,
            "nonce": nonce,
            "password": hexpwd,
            "username": "admin"
        }

        url = route_url + '/cgi-bin/luci/api/xqsystem/login'
        response = s.post(url=url, data=data, timeout=self.reqTimeout)
        res = json.loads(response.content)
        if res['code'] == 0:
            token = res['token']
            return token
        else:
            return ''

    def getUrl(self, service):
        # 定义根url
        route_url = 'http://' + self.route_ip
        url = route_url + '/cgi-bin/luci/;stok=' + self.token + service
        print("url:", url)
        return url

    def getSession(self):
        # 创建请求对象
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=self.max_retries))
        s.mount('https://', HTTPAdapter(max_retries=self.max_retries))
        return s

    def GetRouteStatus(self):
        self.checkLogin()
        s = self.getSession()
        url = self.getUrl('/api/misystem/status')
        req = s.get(url, timeout=self.reqTimeout)
        route_status = json.loads(req.content)
        mem_usage = route_status["mem"]["usage"]
        uptime = round(float(route_status["upTime"]) / 60.0 / 60.0 / 24.0, 2)
        cpu_load = route_status["cpu"]["load"]
        wan_downspeed = round(float(route_status["wan"]["downspeed"]) / 1024.0 / 1024.0, 2)
        wan_maxdownloadspeed = round(float(route_status["wan"]["maxdownloadspeed"]) / 1024.0 / 1024.0, 2)
        wan_upload = round(float(route_status["wan"]["upload"]) / 1024.0 / 1024.0, 2)
        wan_upspeed = round(float(route_status["wan"]["upspeed"]) / 1024.0 / 1024.0, 2)
        wan_maxuploadspeed = round(float(route_status["wan"]["maxuploadspeed"]) / 1024.0 / 1024.0, 2)
        wan_download = round(float(route_status["wan"]["download"]) / 1024.0 / 1024.0, 2)
        count = route_status["count"]["online"]
        status = {
            "mem_usage": mem_usage,
            "uptime": uptime,
            "cpu_load": cpu_load,
            "wan_download": wan_download,
            "wan_downspeed": wan_downspeed,
            "wan_maxdownloadspeed": wan_maxdownloadspeed,
            "wan_upload": wan_upload,
            "wan_upspeed": wan_upspeed,
            "wan_maxuploadspeed": wan_maxuploadspeed,
            "count": count
        }
        return status

    def GetPortForward(self, ftype=1):
        self.checkLogin()
        s = self.getSession()
        url = self.getUrl('/api/xqnetwork/portforward?ftype=' + str(ftype))
        req = s.get(url, timeout=self.reqTimeout)
        conf = json.loads(req.content)
        return conf

    def AddPortForward(self, conf=base.PortForwardType()):
        self.checkLogin()
        s = self.getSession()
        url = self.getUrl('/api/xqnetwork/add_redirect')
        resp = s.post(url, data={
            "name": conf.name,
            "proto": 1,
            "sport": conf.destport,
            "ip": conf.destip,
            "dport": conf.srcport
        })
        if resp.status_code != 200:
            raise exception.ReqError("eee")

    def AddRangePortForward(self, conf=base.PortForwardType()):
        self.checkLogin()
        s = self.getSession()
        url = self.getUrl('/api/xqnetwork/add_range_redirect')
        resp = s.post(url, data={
            "name": conf.name,
            "proto": 1,
            "ip": conf.destip,
            "fport": conf.destport["f"],
            "tport": conf.destport["t"]
        })
        if resp.status_code != 200:
            raise exception.ReqError("eee")

    def ApplyPortForward(self):
        self.checkLogin()
        s = self.getSession()
        url = self.getUrl('/api/xqnetwork/redirect_apply')
        resp = s.get(url, timeout=self.reqTimeout)
        if resp.status_code != 200:
            raise exception.ReqError("eee")
