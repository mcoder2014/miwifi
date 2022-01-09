# miwifi

小米路由器可以通过「小米 Wifi app」和「web 管理后台页面」进行控制，但部分功能仅在「web 管理后台页面」中支持，「小米 Wifi app」不支持。所以参考现有的一些解决方案，做了个简易的 python 工具来方便自己使用。

本项目参考了[miwifi-exporter](https://github.com/bboysoulcn/miwifi-exporter) 的部分代码，主要解决路由器登录问题。

## 进展

- 2021.01.10 支持了查询端口映射、新增单个端口映射、新增范围端口映射、应用端口映射变更功能。

# 参考

1. [miwifi-exporter](https://github.com/bboysoulcn/miwifi-exporter)