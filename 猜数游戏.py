import random
daan=random.randint(1,10)
print("猜数游戏")
temp=input("请输入一个数字:\n")
guess=int(temp)
while guess != daan :
    temp=input("猜错了，重新输入:\n")
    guess=int(temp)
    if guess > daan :
        print("大了")
    else:
        print("小了")
print("猜对了")
print("游戏结束")
