import dyna
import pygame
import time
 


pygame.init()
pygame.font.init() 
              
width, height = 64*10, 64*8
screen=pygame.display.set_mode((width, height))
screen.fill((255,255,255))


mot = dyna.motors()

speed = 200


while 1:

    for event in pygame.event.get():
        # check if the event is the X button 
        if event.type == pygame.QUIT:
            # if it is quit the game
            pygame.quit() 
            exit(0) 
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                mot.move(0,speed)
            elif event.key==pygame.K_LEFT:
                mot.move(3,speed)
            elif event.key==pygame.K_DOWN:
                mot.move(2,speed)
            elif event.key==pygame.K_RIGHT:
                mot.move(1,speed)            
            elif event.key==pygame.K_KP8:
                mot.move(0,-speed)
            elif event.key==pygame.K_KP2:
                mot.move(2,-speed)
            elif event.key==pygame.K_KP6:
                mot.move(1,-speed)
            elif event.key==pygame.K_KP4:
                mot.move(3,-speed)
            elif event.key==pygame.K_KP_PLUS:
                mot.move(4,-speed)
            elif event.key==pygame.K_KP_MINUS:
                mot.move(4,speed)
 
        if event.type == pygame.KEYUP:
            mot.stop_motors()



