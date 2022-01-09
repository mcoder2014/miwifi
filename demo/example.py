#!/usr/bin/python3

import Wifi.Mi
import Wifi.base


def main():
    mi = Wifi.Mi.Mi("config.ini")
    mi.Login()

    # 查看路由器状态
    status = mi.GetRouteStatus()
    print("Router status:", status)

    # 添加一个端口映射
    testConf = Wifi.base.PortForwardType()
    testConf.name = "test"
    testConf.srcport = "33"
    testConf.ftype = "1"
    testConf.proto = 1
    testConf.destport = "6996"
    testConf.destip = "192.168.31.10"
    mi.AddPortForward(testConf)

    # 添加一个端口范围映射
    testConf2 = Wifi.base.PortForwardType()
    testConf2.name = "test2"
    testConf2.ftype = "2"
    testConf2.proto = 1
    testConf2.destport = {}
    testConf2.destport["f"] = 63333
    testConf2.destport["t"] = 64444
    testConf2.destip = "192.168.31.10"
    mi.AddRangePortForward(testConf2)

    # 应用端口映射变化
    mi.ApplyPortForward()

    # 查询端口映射状态
    portForwardConf1 = mi.GetPortForward()
    # 查询端口范围映射状态
    portForwardConf2 = mi.GetPortForward(ftype=2)

    print("PortFord config:", portForwardConf1)
    print("RangePortFord config:", portForwardConf2)


if __name__ == "__main__":
    main()
