def jiecheng(x):
	result = x
	for i in range(1,x):
		result *= i
		
	return result

number = int(input('输入一个正整数：\n'))
result = jiecheng(number)
print('%d 的阶乘是 %d' % (number,result))
