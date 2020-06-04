import pyautogui, pygame, sys

pygame.init()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    print(pyautogui.position())
