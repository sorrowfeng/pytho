import pygame
import sys

#初始化Pygame
pygame.init()

size = width, height = 600, 400
speed = [-2, 1]
bg = (255, 255, 255)
#创建指定大小的窗口
screen = pygame.display.set_mode(size)
#设置窒口标题
pygame.display.set_caption("初次见面, 请大家多多关照！")
#加载图片
turtle = pygame.image.load("C:/Users/Administrator/Pictures/finger.png")
#获得图像的位置矩形
position = turtle.get_rect()

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    #移动图像
    position = position.move(speed)
    if position.left < 0 or position.right > width:
        #翻转图像
        turtle = pygame.transform.flip(turtle, True, False)
        #反方向移动
        speed[0] = -speed[0]
    if position.top < 0 or position.bottom > height: speed[1] = -speed[1]
    #填充背景
    screen.fill(bg)
    #更新图象
    screen.blit(turtle, position)
    #更新界面
    pygame.display.flip()
    #延迟10毫秒
    # pygame.time.delay(10)
    #设置帧率
    clock.tick(60)