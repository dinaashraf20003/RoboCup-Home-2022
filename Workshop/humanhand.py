#!/usr/bin/env python

import sys
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
import time
from robot_vision_msgs.msg import HumanPoses


class TakePhoto:
    def __init__(self):

        #global counter
        #counter += 1
        #if counter > 50:
        rospy.init_node('humanhand', anonymous=True)
        self.camera_sub = rospy.Subscriber("/openpose_ros/human_poses" , HumanPoses , self.callback)
        self.pub = rospy.Publisher('input', String, queue_size=10)

        rospy.spin()


    def callback(self, data):
        if data.poses[0].LWrist.y > data.poses[0].LEye.y:
            self.pub.publish("Left hand up")
            print("Left hand up")
        elif data.poses[0].RWrist.y > data.poses[0].REye.y:
            self.pub.publish("Right hand up")
            print("right hand up")
    

      
if __name__ == '__main__':
    TakePhoto()
   