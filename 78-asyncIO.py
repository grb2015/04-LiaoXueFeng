'''
异步IO
CPU的速度远远快于磁盘、网络等IO。
在一个线程中，CPU执行代码的速度极快，然而，一旦遇到IO操作，如读写文件、发送网络数据时，就需要等待IO操作完成，才能继续进行下一步操作。这种情况称为同步IO。
在IO操作的过程中，当前线程被挂起，而其他需要CPU执行的代码就无法被当前线程执行了。

因为一个IO操作就阻塞了当前线程，导致其他代码无法执行，所以我们必须使用多线程或者多进程来并发执行代码，为多个用户服务。每个用户都会分配一个线程，如果遇到IO导致线程被挂起，其他用户的线程不受影响。

多线程和多进程的模型虽然解决了并发问题，但是系统不能无上限地增加线程。由于系统切换线程的开销也很大，所以，一旦线程数量过多，CPU的时间就花在线程切换上了，真正运行代码的时间就少了，结果导致性能严重下降。

由于我们要解决的问题是CPU高速执行能力和IO设备的龟速严重不匹配，多线程和多进程只是解决这一问题的一种方法。

另一种解决IO问题的方法是异步IO。当代码需要执行一个耗时的IO操作时，它只发出IO指令，并不等待IO结果，然后就去执行其他代码了。一段时间后，当IO返回结果时，再通知CPU进行处理。
'''
'''
异步IO模型需要一个消息循环，在消息循环中，主线程不断地重复“读取消息-处理消息”这一过程：

loop = get_event_loop()
while True:
    event = loop.get_event()
    process_event(event)
'''
'''
asyncio是Python 3.4版本引入的标准库，直接内置了对异步IO的支持。

'''
##  asyncio的编程模型就是一个消息循环。
##　我们从asyncio模块中直接获取一个EventLoop的引用，然后把需要执行的协程扔到EventLoop中执行，就实现了异步IO。


import asyncio

@asyncio.coroutine  ## @asyncio.coroutine把一个generator标记为coroutine类型,这里用的是装饰器
def hello():
    print('hello world!')
    # 异步调用 asyncio.sleep()
    r = yield from asyncio.sleep(1)
    print('Hello again!')

if __name__!='__main__':

    loop = asyncio.get_event_loop() # 获取 EventLoop
    
    # 执行 coroutine(协程!)
    loop.run_until_complete(hello())

    loop.close()

'''
@asyncio.coroutine把一个generator标记为coroutine类型，然后，我们就把这个coroutine扔到EventLoop中执行。

hello()会首先打印出Hello world!，然后，yield from语法可以让我们方便地调用另一个generator。

由于asyncio.sleep()也是一个coroutine，所以线程不会等待asyncio.sleep()，而是直接中断并执行下一个消息循环。

当asyncio.sleep()返回时，线程就可以从yield from拿到返回值（此处是None），然后接着执行下一行语句。
'''

# 用Task封装两个coroutine试试：
import threading
import asyncio

@asyncio.coroutine
def hello2():
    print('Hello world! (%s)' % threading.currentThread())
    yield from asyncio.sleep(1)
    print('Hello again! (%s)' % threading.currentThread())

if __name__ != '__main__':
    loop2 = asyncio.get_event_loop()
    tasks = [hello2(),hello2()]
    loop2.run_until_complete(asyncio.wait(tasks))
    loop2.close()


#   结果：
#   Hello world! (<_MainThread(MainThread, started 140735195337472)>)
#   Hello world! (<_MainThread(MainThread, started 140735195337472)>)
#   (暂停约1秒)
#   Hello again! (<_MainThread(MainThread, started 140735195337472)>)
#   Hello again! (<_MainThread(MainThread, started 140735195337472)>)
#   解析：
#       第一个hello2()执行到sleep()的时候，它并没有等待，而是进入主循环去执行EventLoop去执行第二个hell2()任务了，然后第二个hello2()进入到sleep()
#   进行IO 操作。接着主消息中就没有要执行的任务了。他们就坐等各自的io返回。由于他们调用sleep的时间几乎一样的，所以io返回也几乎是一样的。所以
#   打印Hello again几乎是同时的。
# 由打印的当前线程名称可以看出，两个coroutine是由同一个线程并发执行的。
# 如果把asyncio.sleep()换成真正的IO操作，则多个coroutine就可以由一个线程并发执行。


# 我们用asyncio的异步网络连接来获取sina、sohu和163的网站首页：
import asyncio

@asyncio.coroutine
def wget(host):         ## 怎么驱动这个执行的?
    print('wget %s...' % host)
    connect = asyncio.open_connection(host,80)      ## 连接http(TCP连接请求)
    reader, writer = yield from connect             ## yield from语法，允许一个generator生成器将其部分操作委派给另一个生成器
                                                    ## 这里的reader,write我觉得还是外部send()进来的参数
    header = 'GET / HTTP/1.0\r\nHost:%s\r\n\r\n' % host
    writer.write(header.encode('utf-8'))            ## 发送http连接，这里的writer是上报的tcp连接后返回的
    yield from writer.drain()       ## 之类的drain是什么意思?
    while True:                                 ### 在一个while(1)读取服务器的回应
        line = yield from reader.readline()     ##  注意这里的reader是上面建立tcp连接后返回的
        if line == b'\r\n':     ## 只读取头部
            break
        print('%s header > %s' % (host, line.decode('utf-8').rstrip()))

    # Ignore the body, close the socket
    writer.close()  ##renbin.guo added 之前的fork作者好像网了这句
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = [wget(host) for host in ['www.sina.com.cn','www.sohu.com','www.163.com']]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


'''
asyncio提供了完善的异步IO支持；

异步操作需要在coroutine中通过yield from完成；

多个coroutine可以封装成一组Task然后并发执行。

'''
