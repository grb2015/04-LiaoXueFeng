'''
协程--Coroutine

协程的特点在于是一个线程执行，那和多线程比，协程有何优势？

最大的优势就是协程极高的执行效率。因为子程序切换不是线程切换，而是由程序自身控制，因此，没有线程切换的开销，和多线程比，线程数量越多，协程的性能优势就越明显。

第二大优势就是不需要多线程的锁机制，因为只有一个线程，也不存在同时写变量冲突，在协程中控制共享资源不加锁，只需要判断状态就好了，所以执行效率比多线程高很多。

因为协程是一个线程执行，那怎么利用多核CPU呢？最简单的方法是多进程+协程，既充分利用多核，又充分发挥协程的高效率，可获得极高的性能。
'''
'''
Python对协程的支持是通过generator实现的。

在generator中，我们不但可以通过for循环来迭代，还可以不断调用next()函数获取由yield语句返回的下一个值。

但是Python的yield不但可以返回一个值，它还可以接收调用者发出的参数。
'''

## 协程实现生产者-消费者的问题 .协程是通过生成器来实现的(生成器作参数)


def consumer():
    r = ''
    while True:
        n = yield r
        if not n:           ##这里是说，如果n为非0,则一直执行下去
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'

def produce(c):
    c.send(None)        ##启动生成器
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)       ## yield不仅可以返回结果，还可以接受参数。这里的n其实就是赋值给了上面consumer的n.
                            ## 而consumer中的yield r的值则通过c.send()函数返回给了produce的r
        print('[PRODUCER] Consumer return:%s...' % r)

## 执行开始
c = consumer()      ## consumer是一个生成器，它传递给了produce做参数!
produce(c)

'''
注意到consumer函数是一个generator，把一个consumer传入produce后：
1、首先调用c.send(None)启动生成器；
2、然后，一旦生产了东西，通过c.send(n)切换到consumer执行；
3、consumer通过yield拿到消息，处理，又通过yield把结果传回；
4、produce拿到consumer处理的结果，继续生产下一条消息；
5、produce决定不生产了，通过c.close()关闭consumer，整个过程结束。

整个流程无锁，由一个线程执行，produce和consumer协作完成任务，所以称为“协程”，而非线程的抢占式多任务。

最后套用Donald Knuth的一句话总结协程的特点：
“子程序就是协程的一种特例。”
'''















