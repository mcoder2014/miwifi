#!/usr/bin/python3


class PortForwardType:
    def __init__(self):
        # 配置名称
        self.name = "config name"
        # 内网机器的 IP
        self.destip = "192.168.31.160"
        # 内网机器需要映射的 port
        self.destport = "22"
        self.ftype = 1
        self.proto = 1
        # 外网看懂的 port
        self.srcport = 40022


# class PortForwardType2:
#     def __init__(self):
#         self.name = "config name"
#         self.ftype = 2
#         self.destip = "192.168.31.160"
#         self.proto = 1
#         self.srcport = dict(f=60000, t=61000)
