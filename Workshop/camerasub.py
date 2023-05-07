#!/usr/bin/env python

'''
Copyright (c) 2016, Nadya Ampilogova
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

# Script for simulation
# Launch gazebo world prior to run this script

from __future__ import print_function
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import time
from opencv_apps.msg import RotatedRectStamped


class TakePhoto:
    def __init__(self):
        rospy.init_node('camerasub', anonymous=True)
        self.camera_sub = rospy.Subscriber("/camshift/track_box" , RotatedRectStamped , self.callback)
       

        rospy.spin()    
        

    def callback(self, data):
        #self.counter = 0
        self.pub = rospy.Publisher('input', String, queue_size=10)
        self.pos_x= data.rect.center.x
        self.pos_y= data.rect.center.y
        self.pub.publish("Left hand up")
        self.pub.publish("Right hand up")
        '''if self.pos_x > 300:
            self.pub.publish("Move Left")
            print("Move left")
        elif self.pos_x < 280:
            self.pub.publish("Move Right")
            print("Move right")
        elif self.pos_y > 290:
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
    
   