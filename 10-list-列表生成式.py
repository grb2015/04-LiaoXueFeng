'''
列表生成式


列表生成式即List Comprehensions，是Python内置的非常简单却强大的可以用来创建list的生成式。
'''

## 1--- 生成 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]   
print(list(range(1,11)))


## 2----生成 [1, 4, 9, 16, 25, 36, 49, 64, 81, 100 ], 

## grb 方法1:使用循环
L = []
for x in range(1,11):
	L.append(x * x)
print(L)

## grb 方法2，使用列表生成式
L2 = [x * x for x in range(1, 11)]   ## 这里的 [x * x for x in range(1, 11)] 就是一个列表生产式,所以列表生产式就是这样写
print(L2)  

# for循环后面还可以加上if判断
## 3--- 生成[4, 16, 36, 64, 100] 偶数的平方
print([x * x for x in range(1,11) if x % 2 == 0])


# 使用两层循环，可以生成全排列
## 4---生成'ABC'和'XYZ'的全排列
print([m + n for m in 'ABC' for n in 'XYZ'])



# 运用列表生成式，可以写出非常简洁的代码。
# 5--- 例如，列出当前目录下的所有文件和目录名，可以通过一行代码实现：
import os
print([d for d in os.listdir('.')])


## 6---列表生成式也可以使用两个变量来生成list.  ['y=B', 'x=A', 'z=C']
            #更多个变量的for 循环一样 .  for循环其实可以同时使用两个甚至多个变量，比如dict的items()可以同时迭代key和value
            d = {'x': 'A', 'y': 'B', 'z': 'C' }
            for k,v in d.items():
	        print(k,'=',v)
# 列表生成式也可以使用两个变量来生成list
d = {'x':'A','y':'B','z':'C'}
print([k + '=' + v for k,v in d.items()])


# 7--- 把一个list中所有的字符串变成小写
L = ['Hello', 'World', 'IBM', 'Apple']
print([s.lower() for s in L])



# 习题
x = 'abs'
y = 123
print(isinstance(x,str))
print(isinstance(y,str))

L1 = ['Hello', 'World', 18, 'Apple', None]
print([s.lower() for s in L1 if isinstance(s,str) ])
