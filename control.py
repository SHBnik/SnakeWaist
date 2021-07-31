#!/usr/bin/env python
import dyna
import pygame
import time
import rospy
from std_msgs.msg import String
import geometry_msgs.msg
import time
import sys
import os

import tf
import math
import TXY as formula
from pid import pid

pygame.init()
pygame.font.init() 
              
width, height = 64*10, 64*8
screen=pygame.display.set_mode((width, height))
screen.fill((255,255,255))


mot = dyna.motors()
yaw_pid = pid(86.05,0.15,28)
# yaw_pid = pid(50,0.05,20)



speed = 250
caps = False
freez_time = 1
error_correction_time = 0.25 #1.4 mm

is_pid = False
yaw = 0

yaw_setpoint = -20










def read_position(data):
    global yaw
    (roll, eu_pitch, yaw) = tf.transformations.euler_from_quaternion(
        [data.pose.orientation.x,
         data.pose.orientation.y,
         data.pose.orientation.z,
         data.pose.orientation.w]
          )
    print(radtodeg(yaw))


def radtodeg(data):
    return data*57.2958








rospy.init_node('farzamsdick_controller', anonymous=False)

rospy.Subscriber("/aruco_single/pose", geometry_msgs.msg.PoseStamped, read_position)
pub = rospy.Publisher('chatter', String, queue_size=10)


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
                
            elif event.key==pygame.K_h:
                mot.home() 

            elif event.key==pygame.K_SPACE:
                if is_pid == False: is_pid = True
                elif is_pid == True: is_pid = False
                yaw_pid.resetI()


                
            elif event.key==pygame.K_RALT or event.key==pygame.K_LALT:
                mot.move(4,speed,-speed,speed,-speed)
                time.sleep(formula.t_yaw(yaw_setpoint))
                mot.move(4,0,0,0,0)

                
 
        if event.type == pygame.KEYUP:
            mot.move(5,0,0,0,0)

    if is_pid:
        pid_speed = yaw_pid.update_pid(yaw_setpoint,radtodeg(yaw))
        mot.move(4,pid_speed,-pid_speed,pid_speed,-pid_speed)
        