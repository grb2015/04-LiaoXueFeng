'''
aiohttp

asyncio可以实现单线程并发IO操作。如果仅用在客户端，发挥的威力不大。
如果把asyncio用在服务器端，例如Web服务器，由于HTTP连接就是IO操作，因此可以用单线程+coroutine实现多用户的高并发支持。

asyncio实现了TCP、UDP、SSL等协议，aiohttp则是基于asyncio实现的HTTP框架。
'''
'''
安装aiohttp：
pip install aiohttp
'''


##  aiohttp则是基于asyncio实现的HTTP框架,它更flask一样，解决如果要处理100个url怎么办的问题.
# 注意aiohttp的初始化函数init()也是一个coroutine，loop.create_server()则利用asyncio创建TCP服务。
import asyncio

from aiohttp import web

async def index(request):
    await asyncio.sleep(0.5)
    return web.Response(body=b'<h1>Index</h1>')

async def hello(request):
    await asyncio.sleep(0.5)
    text = '<h1>hello, %s!</h1>' % request.match_info['name']
    return web.Response(body=text.encode('utf-8'))

async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)     ## 指定 GET / 的http请求处理函数为index()
    app.router.add_route('GET', '/hello/{name}', hello) ## 指定GET  /hello/name   的http请求处理函数为 hello ()
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 8000)   ## 创建http服务器。使用的是aiohttp的功能
    print('Server started at http://127.0.0.1:8000...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()

