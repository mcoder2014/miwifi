#!/usr/bin/python3
import time


def getTimestamp():
    return int(time.time_ns() / 1000)
