# 1 - Import library
import pygame

import time
 
# 2 - Initialize the game
pygame.init()
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
 
width, height = 64*10, 64*8
screen=pygame.display.set_mode((width, height))

 
# 4 - keep looping through
while 1:
 
    # 5 - clear the screen before drawing it again
    screen.fill((255,255,255))
 
    # 7 - update the screen
    pygame.display.flip()
    # 8 - loop through the events
    for event in pygame.event.get():
        # check if the event is the X button 
        if event.type == pygame.QUIT:
            # if it is quit the game
            pygame.quit() 
            exit(0) 
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                keys[0]=True
            elif event.key==K_LEFT:
                keys[1]=True
            elif event.key==K_DOWN:
                keys[2]=True
            elif event.key==K_RIGHT:
                keys[3]=True
            time.sleep(0.1)
 
        if event.type == pygame.KEYUP:
            if event.key==pygame.K_UP:
                keys[0]=False
            elif event.key==pygame.K_LEFT:
                keys[1]=False
            elif event.key==pygame.K_DOWN:
                keys[2]=False
            elif event.key==pygame.K_RIGHT:
                keys[3]=False
