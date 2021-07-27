#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import geometry_msgs.msg
import time
import sys
import os

import tf
import math

x_offset = -0.00136
y_offset = 0.01389
z_offset = 0.2211

x_pos = 0
y_pos = 0

def read_position(data):
    global num,f,x_pos,y_pos
    x_pos = data.pose.position.x - x_offset
    y_pos = data.pose.position.y - y_offset
    z_pos = data.pose.position.z - z_offset
    (eu_roll, eu_pitch, eu_yaw) = tf.transformations.euler_from_quaternion(
        [data.pose.orientation.x,
         data.pose.orientation.y,
         data.pose.orientation.z,
         data.pose.orientation.w]
          )

    print(eu_roll * 180/math.pi, eu_pitch* 180/math.pi, eu_yaw* 180/math.pi)
    # if num < 11:
    #     f.write(str(x_pos)+','+str(y_pos)+','+str(z_pos)+','+str(eu_roll)+','+str(eu_pitch)+','+str(eu_yaw)+'\n')
    #     num += 1

        # if num == 11:
        #     f.close()


def now(data):
    
    f.write(data.data+','+str(x_pos)+','+str(y_pos)+'\n')

def listen_to_aruco_single_node():
    global f
    try:
        rospy.init_node('Farzamsdick', anonymous=False)

        rospy.Subscriber("/aruco_single/pose", geometry_msgs.msg.PoseStamped, read_position)
        rospy.Subscriber('chatter', String, now)

        rospy.spin()
    except Exception as e: 
        f.close()





if __name__ == '__main__':
    num = 0
    filenname = sys.argv[1]
    f = open(filenname+".csv", "a")
    listen_to_aruco_single_node()