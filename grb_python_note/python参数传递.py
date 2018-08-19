# -*- coding: utf-8 -*-
# @Author: Teiei
# @Date:   2018-08-19 10:29:05
# @Last Modified by:   Teiei
# @Last Modified time: 2018-08-19 10:36:35

#参考：http://winterttr.me/2015/10/24/python-passing-arguments-as-value-or-reference/
#可变对象是传址，不可变对象传值


def test2(a):
	a = a+1  ## a是不可变对象，所以是传值,不会对原a起作用
def test3( a ):
    a[0] = 10 ## a为list,可变对象，所以传址，会对原来的a影响。这里是直接对a[0]这个地址进行的修改，所以结果会影响原来的
def test4(nums):
	nums = [0,0,0,0]  ## 注意这里，nums作为函数类类的一个局部变量，首先num 与nums都指向[1,2,3,4,5]的空间
	return nums       ## 然后这里又将nums指向了[0,0,0,0] 但是原来的num还是[1,2,3,4,5] 所以不变
if __name__ == '__main__':

	a = 2
	test2(a)
	print(a)
	print("-------------")

	lstFoo = [1,2,3,4]
	test3(lstFoo)
	print(lstFoo) #结果是[10]

	print('------------')
	num = [1,2,3,4,5]
	print(num)
