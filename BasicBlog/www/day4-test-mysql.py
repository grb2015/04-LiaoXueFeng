## renbin.guo added 2017/08/30
## 使用python语句来插入数据库数据。
## 运行提示create_pool缺少loop参数
import orm
from models import User, Blog, Comment

def test():
    yield from orm.create_pool(user='www-data', password='www-data', database='awesome')

    u = User(name='Test', email='test@example.com', passwd='1234567890', image='about:blank')

    yield from u.save()

for x in test():
    pass
