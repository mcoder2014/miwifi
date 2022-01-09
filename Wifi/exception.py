#!/usr/bin/python3


class ConfigError(RuntimeError):
    def __init__(self, arg):
        self.args = arg


class ReqError(RuntimeError):
    def __init__(self, arg):
        self.args = arg
