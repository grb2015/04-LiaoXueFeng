
'''
我们先考虑如何定义一个User对象，然后把数据库表users和它关联起来。

yield 英文意思是生产，是 python 的关键字，在函数返回值时用来替换 return 产生一个值。yield 表达式只能用于定义生成器函数中，在函数外使用 yield 会导致 SyntaxError: 'yield' outside function 。
'''
'''
日期和时间用float类型存储在数据库中，而不是datetime类型，这么做的好处是不必关心数据库的时区以及时区转换问题，排序非常简单。
显示的时候，只需要做一个float到str的转换，也非常容易。
'''
import time,uuid
import asyncio
from orm import Model, StringField, IntegerField,BooleanField,FloatField,TextField,create_pool

##　day4
def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

###　有了ORM，我们就可以把Web App需要的3个表用Model表示出来
## 我们先考虑如何定义一个User对象，然后把数据库表users和它关联起来
## day 3  Model定义在orm中
class User(Model):      
    __table__ = 'users'     ## 这里是什么用法 ?__table__是其内置成员变量？

    # 在编写ORM时，给一个Field增加一个default参数可以让ORM自己填入缺省值，非常方便。　## day4 
    # 并且，缺省值可以作为函数对象传入，在调用save()时自动计算。
    #  StringField BooleanField FloatField代表数据类型，但是在哪里定义的呢?在orm中定义的！
    # 同样 ddl 在哪里定义的呢? ddl只是一个名称，携带参数来初始化类
    id = StringField(primary_key=True, default=next_id(),ddl='varchar(50)') ## day3只写了primary_key
    email = StringField(ddl='varchar(50)')      ## day4 added 
    passwd = StringField(ddl='varchar(50)')     ## day4 added 
    admin = BooleanField()                      ## day4 added
    name = StringField(ddl='varchar(50)')       ## day 3
    image = StringField(ddl='varchar(500)')     ## day4 added
    created_at = FloatField(default=time.time)  ## day4 added

## day4 added   博客的数据库
class Blog(Model):
    __table__ = 'blogs'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')        ##　用户id
    user_name = StringField(ddl='varchar(50)')      ##  用户名
    user_image = StringField(ddl='varchar(500)')    ##  用户照片
    name = StringField(ddl='varchar(50)')           ##  名字 ? 和user_name有何区别?
    summary = StringField(ddl='varchar(200)')       ##  摘要
    content = TextField()                           ##  内容
    created_at = FloatField(default=time.time)      ##  创建时间
## day4 added
class Comment(Model):       ## 用户评论的数据库
    __table__ = 'comments'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    blog_id = StringField(ddl='varchar(50)')        ## 博客名
    user_id = StringField(ddl='varchar(50)')        ## 用户id
    user_name = StringField(ddl='varchar(50)')      ## 用户名
    user_image = StringField(ddl='varchar(500)')    ## 用户照片
    content = TextField()                           ## 内容
    created_at = FloatField(default=time.time)      ##　创建时间      


def test(loop):
    yield from create_pool(loop=loop,user='basicblog',password='password',db='awesome')
    u = User(name='尉勇强',email='hellojue@foxmail.com',passwd = '12132',image='about:blank')
    yield from u.save()


# 测试代码
if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test(loop))
    loop.run_forever()