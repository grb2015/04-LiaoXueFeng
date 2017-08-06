## 之前用WSGI写的http服务器可以正常工作，但是有个问题，它如何处理不同的url，比如如何处理100个不同的URL ?
## 
# 一个最简单的想法是从environ变量里取出HTTP请求的信息，然后逐个判断：

# def application(environ, start_response):
#    method = environ['REQUEST_METHOD']
#    path = environ['PATH_INFO']
#    if method=='GET' and path=='/':            # 处理第一种url:  GET / 
#        return handle_home(environ, start_response)
#    if method=='POST' and path='/signin':      # 处理第二种url:   POST  /signin    
#        return handle_signin(environ, start_response)
#       ...
#                                               # 处理第100中url：


# 这样写的代码肯定无法维护了
# 我们想用一个函数处理一个URL，至于URL到函数的映射，就交给Web来做。(所以web框架可以帮我们实现 从url到函数的映射)

'''
使用Web框架-Flask

我们需要在WSGI接口之上能进一步抽象，让我们专注于用一个函数处理一个URL，至于URL到函数的映射，就交给Web框架来做。
'''
'''
先用pip安装Flask：
$ pip install flask
'''
'''
然后写一个app.py，处理3个URL，分别是：
1、GET /：首页，返回Home；
2、GET /signin：登录页，显示登录表单；
3、POST /signin：处理登录表单，显示登录结果。

注意噢，同一个URL/signin分别有GET和POST两种请求，映射到两个处理函数中。
'''
'''
Flask通过Python的装饰器在内部自动地把URL和函数给关联起来
'''
from flask import Flask
from flask import request

app = Flask(__name__)

## 处理第一种url    GET  /      or  POST  /
@app.route('/',methods=['GET','POST'])
def home():
    return '<h1>Home</h1>'

## 处理第2种url    GET  /signin
@app.route('/signin',methods=['GET'])
def signin_form():
    return '''<form action='/signin' method='post'>
              <p><input name='username'></p>
              <p><input name='password' type='password'></p>
              <p><button type='submit'>Sign In</button></p>'''

## 处理第3种url    POST  /signin
@app.route('/signin',methods=['POST'])
def signin():
    # 需要从request对象读取表单内容：
    if request.form['username']=='admin' and request.form['password']=='password':
        return '<h3>Hello,admin..</h3>'
    return '<h3>bad username or password</h3>'


# 开始执行程序
if __name__ == '__main__':
    print(app)
    app.run()       ##  运行python，Flask自带的Server在端口5000上监听.我们写的只是处理http的逻辑

'''
运行python，Flask自带的Server在端口5000上监听：

$ python app.py 
 * Running on http://127.0.0.1:5000/
'''
'''
除了Flask，常见的Python Web框架还有：
1、Django：全能型Web框架；
2、web.py：一个小巧的Web框架；
3、Bottle：和Flask类似的Web框架；
4、Tornado：Facebook的开源异步Web框架。

当然了，因为开发Python的Web框架也不是什么难事，我们后面也会讲到开发Web框架的内容。
'''
