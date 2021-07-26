#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import geometry_msgs.msg
import time
import sys
import os

import tf
import math

x_offset = -0.00108
y_offset = 0.01289
z_offset = 0.02238

def read_position(data):
    global num,f
    x_pos = data.pose.position.x + x_offset
    y_pos = data.pose.position.y + y_offset
    z_pos = data.pose.position.z + z_offset
    (eu_roll, eu_pitch, eu_yaw) = tf.transformations.euler_from_quaternion(
        [data.pose.orientation.x,
         data.pose.orientation.y,
         data.pose.orientation.z,
         data.pose.orientation.w]
          )
    f.write(str(x_pos)+','+str(y_pos)+','+str(z_pos)+','+str(eu_roll)+','+str(eu_pitch)+','+str(eu_yaw)+'\n')
    # if num < 11:
    #     f.write(str(x_pos)+','+str(y_pos)+','+str(z_pos)+','+str(eu_roll)+','+str(eu_pitch)+','+str(eu_yaw)+'\n')
    #     num += 1

        # if num == 11:
        #     f.close()

def listen_to_aruco_single_node():
    global f
    try:
        rospy.init_node('Farzamsdick', anonymous=False)

        rospy.Subscriber("/aruco_single/pose", geometry_msgs.msg.PoseStamped, read_position)

        rospy.spin()
    except Exception as e: 
        f.close()





if __name__ == '__main__':
    num = 0
    filenname = sys.argv[1]
    f = open(filenname+".csv", "a")
    listen_to_aruco_single_node()