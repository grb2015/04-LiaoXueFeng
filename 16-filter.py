'''
Python内建的filter()函数用于过滤序列。

和map()类似，filter()也接收一个函数和一个序列。

和map()不同的时，filter()把传入的函数依次作用于每个元素，然后根据返回值是True还是False决定保留还是丢弃该元素。

filter()函数返回的是一个Iterator，也就是一个惰性序列，所以要强迫filter()完成计算结果，需要用list()函数获得所有结果并返回list。
'''
# 1--- 在一个list中，删掉偶数，只保留奇数
def is_odd(n):
	return n % 2 == 1

print(list(filter(is_odd,[1,2,3,4,5,6,7,8,9])))


# 2-- 把一个序列中的空字符串删掉
def not_empty(s):
	return s and s.strip()
print(not_empty(None))
print(list(filter(not_empty, ['A','B',None,'C',' '])))


## 3--- 求所有的素数

## 生成器，用于生成一个无穷的奇数数列 3,5,7...
def odd_iter():
	n = 1
	while True:
		n = n + 2
		yield n

##  判断一个数是不是,判断传入的参数是否能被给定的n整除。若不能，则返回true
def not_divisible(n):
	return lambda x : x % n > 0

## 生成器 
def primes():
	yield 2         ##  primes第一次返回2 
	it = odd_iter() ##  it=[3,5,7,9,...] 

	while True:
		n = next(it) ##     返回it的下一个值,第一次返回3
		yield n     ## 将n返回 
		it = filter(not_divisible(n), it) # 构造新序列it,这里在原来的[3,5,7,...]中过滤掉所有能被3整除的。

for n in primes():     ##返回前1000个素数
	if n < 1000:
		print(n)
	else:
		break

## 练习 

def is_palindrome(n):
	s = str(n)
	s1 = s[::-1]
	return s == s1
    
output = filter(is_palindrome, range(1, 1000))
print(list(output))
