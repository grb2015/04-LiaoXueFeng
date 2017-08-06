#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## 用async 和 await代替yield from 

## 只需要做两点改动:
##1 . asyncio.coroutine替换为async；
##2.  把yield from替换为await。

import threading
import asyncio

async def hello():
    print('Hello world! (%s)' % threading.currentThread())
    await asyncio.sleep(1)
    print('Hello again! (%s)' % threading.currentThread())

loop = asyncio.get_event_loop()
tasks = [hello(), hello()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
