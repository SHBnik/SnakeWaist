import dyna
import pygame
import time
 


pygame.init()
pygame.font.init() 
              
width, height = 64*10, 64*8
screen=pygame.display.set_mode((width, height))
screen.fill((255,255,255))


mot = dyna.motors()

speed = 250
caps = False
freez_time = 3

while 1:

    for event in pygame.event.get():
        # check if the event is the X button 
        if event.type == pygame.QUIT:
            # if it is quit the game
            pygame.quit() 
            exit(0) 
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                mot.move(4,0,speed,speed,0)
                if caps: time.sleep(freez_time)
            elif event.key==pygame.K_DOWN:
                mot.move(4,speed,0,0,speed)
                if caps: time.sleep(freez_time)
            elif event.key==pygame.K_RIGHT:
                mot.move(4,speed,0,speed,0)
                if caps: time.sleep(freez_time)
            elif event.key==pygame.K_LEFT:
                mot.move(4,0,speed,0,speed)
                if caps: time.sleep(freez_time)            
            elif event.key==pygame.K_KP8:
                mot.move(4,0,-speed,-speed,0)
                if caps: time.sleep(freez_time)
            elif event.key==pygame.K_KP2:
                mot.move(4,-speed,0,0,-speed)
                if caps: time.sleep(freez_time)
            elif event.key==pygame.K_KP6:
                mot.move(4,-speed,0,-speed,0)
                if caps: time.sleep(freez_time)
            elif event.key==pygame.K_KP4:
                mot.move(4,0,-speed,0,-speed)
                if caps: time.sleep(freez_time)
            elif event.key==pygame.K_KP_PLUS:
                mot.move(4,-speed,-speed,-speed,-speed)
            elif event.key==pygame.K_KP_MINUS:
                mot.move(4,speed,speed,speed,speed)            
            elif event.key==pygame.K_CAPSLOCK:
                if caps == False: caps = True
                elif caps == True: caps = False
                        

            elif event.key==pygame.K_w:
                mot.move(4,-speed,speed,speed,-speed)
                if caps: time.sleep(freez_time)
            elif event.key==pygame.K_s:
                mot.move(4,speed,-speed,-speed,speed)
                if caps: time.sleep(freez_time)
            elif event.key==pygame.K_d:
                mot.move(4,speed,-speed,speed,-speed)
                if caps: time.sleep(freez_time)
            elif event.key==pygame.K_a:
                mot.move(4,-speed,speed,-speed,speed)
                if caps: time.sleep(freez_time) 

            elif event.key==pygame.K_SPACE:

                mot.move(4,0,100,100,0)
                time.sleep(4)
                mot.move(4,0,0,0,0)
                print("1")
                time.sleep(5)
                mot.move(4,0,100,0,200)
                time.sleep(4)
                mot.move(4,0,0,0,0)
                print("2")
                time.sleep(5) 
                mot.move(4,0,-100,0,-200)
                time.sleep(4)
                mot.move(4,0,0,0,0)
                print("3")
                time.sleep(5)
                mot.move(4,0,-100,-100,0)
                time.sleep(4)

                
 
        if event.type == pygame.KEYUP:
            mot.move(5,speed,speed,speed,speed)



