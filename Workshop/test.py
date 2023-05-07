#!/usr/bin/env python

import sys
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
import time
from opencv_apps.msg import RotatedRectStamped
class TakePhoto:
    def __init__(self):
        rospy.init_node('test', anonymous=True)
        self.camera_sub = rospy.Subscriber("/camshift/track_box" , RotatedRectStamped , self.callback)
        self.pub = rospy.Publisher('input', String, queue_size=10)

        rospy.spin()


    def callback(self, data):
        # if data.poses[0].LWrist.y > data.poses[0].LEye.y:
        #     self.pub.publish("Left hand up")
        #     print("Left hand up")
        # elif data.poses[0].RWrist.y > data.poses[0].REye.y:
        #     self.pub.publish("Right hand up")
        #     print("right hand up")
        self.pos_x= data.rect.center.x
        self.pos_y= data.rect.center.y
        if self.pos_x > 300:
            self.pub.publish("Move Left")
            print("Move left")
        elif self.pos_x < 280:
            self.pub.publish("Move Right")
            print("Move right")
        '''elif self.pos_y > 290:
            self.pub.publish("Move Upwards")
            print("Move upwards")
        elif self.pos_y < 270:
            print("Move downwards")
            self.pub.publish("Move downwards") 
        else:
            print("centered")
            self.pub.publish("You are centered")'''
    

      
if __name__ == '__main__':
    TakePhoto()
   