'''
我们来编写一个Dict类，这个类的行为和dict一致，但是可以通过属性来访问，用起来就像下面这样：
'''
class Dict(dict):
	"""docstring for Dict"""
	def __init__(self, **kw):       
		super().__init__(**kw)      ## 其实就是调用基类的init方法
	def __getattr__(self,key):
		try:
			return self[key]            # self就是一个dict 对象
		except KeyError:
			raise AttributeError(r"'Dict' object has no attribute '%s'" % key)
	def __setattr__(self,key,value):
		self[key]=value     ## self 指代的是新生成类的对象实例,它继承自dict .所以它也是有可以这样用的： dict[key]=value

d = Dict(a=1,b=2)
print(d['a'])
print(d.a)

# 为了编写单元测试，我们需要引入Python自带的unittest模块，编写mydict_test.py如下：
import unittest

class Test(unittest.TestCase):
	def test_init(self):
		d = Dict(a=1,b='test')
		self.assertEqual(d.a,1)
		self.assertEqual(d.b,'test')
		self.assertTrue(isinstance(d,dict))     ##用来测试d是不是一个dict对象的派生

	def test_key(self):         ## 测试__getattr__
		d = Dict()          ## ok  , 我新建了一个Dict对象d,现在我来测试它的方法
		d['key'] = 'value'  ## 先使用正常的dict的方法进行赋值。
		self.assertEqual(d.key,'value') ## 再使用Dict定义的方法,d.key ,即__getattr__方法，看它的结果是不是上面设置的值

	def test_attr(self):
		d = Dict()
		d.key = 'value'         ## 这里调用了Dict的__setattr__方法
		self.assertTrue('key' in d)  ##　先测试key是否设置进去了,使用的是dict中的标准操作key in d 来验证
		self.assertEqual(d['key'],'value')      ## 再测试设置的值对不对

	def test_keyerror(self):        ## 测试访问一个不存在的key,看会不会报错
		d = Dict()
		with self.assertRaises(KeyError):
			value = d['empty']      ## 访问一个不存在的Key

	def test_attrerror(self):       ## 跟上面的一样，都是测试访问一个不存在的Key,只不过访问的方式变成了自定义的__getattr__方法
		d = Dict()
		with self.assertRaises(AttributeError):     
			value = d.empty
	# 可以在单元测试中编写两个特殊的setUp()和tearDown()方法。
	# 这两个方法会分别在每调用一个测试方法的前后分别被执行。

	def setUp(self):
		print('setUp...')
	def tearDown(self):
		print('tearDown...')

'''
编写单元测试时，我们需要编写一个测试类，从unittest.TestCase继承。

以test开头的方法就是测试方法，不以test开头的方法不被认为是测试方法，测试的时候不会被执行。

对每一类测试都需要编写一个test_xxx()方法。由于unittest.TestCase提供了很多内置的条件判断，我们只需要调用这些方法就可以断言输出是否是我们所期望的。最常用的断言就是assertEqual()：

self.assertEqual(abs(-1), 1) # 断言函数返回的结果与1相等

另一种重要的断言就是期待抛出指定类型的Error，比如通过d['empty']访问不存在的key时，断言会抛出KeyError：

with self.assertRaises(KeyError):
    value = d['empty']

而通过d.empty访问不存在的key时，我们期待抛出AttributeError：

with self.assertRaises(AttributeError):
    value = d.empty
'''
unittest.main()

