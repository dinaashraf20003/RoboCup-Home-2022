#!/usr/bin/env python

"""
    arm.py - move robot arm according to predefined gestures

"""

import rospy
from numpy import interp
from cv_bridge import CvBridge
import math
import numpy as np
from std_msgs.msg import Float64
from std_msgs.msg import String
from sensor_msgs.msg import Image
from opencv_apps.msg import RotatedRectStamped

class Loop:
    def __init__(self):
	self.camx = 0
	self.camy = 0
	self.camz = 0
        rospy.on_shutdown(self.cleanup)
        rospy.Subscriber('/arm', String, self.callback)

	# publish command message to joints/servos of arm
    	self.joint1 = rospy.Publisher('/waist_controller/command',Float64)
	self.joint2 = rospy.Publisher('/shoulder_controller/command',Float64)
    	self.joint3 = rospy.Publisher('/elbow_controller/command',Float64)
    	self.joint4 = rospy.Publisher('/wrist_controller/command',Float64)
	self.joint5 = rospy.Publisher('/hand_controller/command',Float64)
	self.pos1 = Float64()
    	self.pos2 = Float64()
    	self.pos3 = Float64()
    	self.pos4 = Float64()
    	self.pos5 = Float64()
	
	'''self.x=30
	self.y=0
	self.z=0
	self.L=math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
	self.theta1= math.atan(self.y/self.x)	
	self.theta2= 2*np.arccos(self.L/21.0)
	self.theta3= np.arccos((self.L*self.L-220.5)/-220.5)
	
	rospy.loginfo(self.theta1)
	rospy.loginfo(self.theta2)
	rospy.loginfo(self.theta3)'''
	# Initial gesture of robot arm
	self.pos1 = 0.5
	self.pos2 = 0.0
        #self.pos2 = 0.0
	self.pos3 = 0.0	
	self.pos4 = 0.0
	self.pos5 = 0.0
	self.joint1.publish(self.pos1)
	self.joint2.publish(self.pos2)
	self.joint3.publish(self.pos3)
	self.joint4.publish(self.pos4)
	self.joint5.publish(self.pos5)
	#self.callback()
    def imgback(self, msg):
	self.camx = msg.rect.center.x
	self.camy = msg.rect.center.y
    def imageback(self, msg):
	bridge = CvBridge()
	data = bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
	self.camz = data[int(self.camx / 1.35416667)][int(self.camy / 1.35416667)]
    def callback(self, msg):
        #print msg.data
        if msg.data == "arm":       
		while not rospy.is_shutdown():
			rospy.Subscriber('/camshift/track_box', RotatedRectStamped, self.imgback)
			rospy.Subscriber('/camera/depth_registered/image_raw',Image , self.imageback)		
			#x -> self.camx
			#y -> self.camy
			#z -> self.camz	
			self.x = interp(self.camx, [0, 650], [1.5, -1.5])
			self.y = interp(self.camy, [0, 450], [29.0, 0.0])
			self.z = interp(self.camy, [0, 2], [0.0, 29.0])
			if self.z == 0.0:
				self.phi = math.pi / 2
			else:
				self.phi = math.atan(self.y/self.z)
			self.theta = -1 * math.acos((self.z*self.z + self.y*self.y - 10.5*10.5 - 18.5*18.5) / (2.0*10.5*18.5))
			self.alpha = self.phi + math.atan(18.5 * math.sin(self.theta) / (10.5 + 18.5 * math.cos(self.theta)))
			self.shoulder = self.alpha
			self.elbow  = self.theta
			'''if self.x >= 325:
				self.x = self.x - 325
				self.x = self.x / (216 + 2/3)
				self.x = self.x * -1
			else:
				self.x = self.x / (216.0 + 2.0/3.0)
				self.x = 1.5 - self.x'''
			rospy.loginfo(self.x)
			#self.pos1 = -1.0
			self.pos1 = self.x
			#self.pos2 = -0.215
			self.pos2 = math.pi/2 - (self.shoulder)
			self.pos3 = (self.elbow) 	
			self.pos4 = 0.0
			self.pos5 = 0.5
			self.joint1.publish(self.pos1)
			self.joint2.publish(self.pos2)
			self.joint3.publish(self.pos3)
			self.joint4.publish(self.pos4)
			self.joint5.publish(self.pos5)
			rospy.sleep(2)
			'''
			# gesture 2
			#self.pos1 = -1.0
			self.pos1 = 0.0
			#self.pos2 = 0.24
			self.pos2 = 0.0
			self.pos3 = 0.639
			self.pos4 = -1.0
			self.pos5 = 0.0
			self.joint1.publish(self.pos1)
			self.joint2.publish(self.pos2)
			self.joint3.publish(self.pos3)
			self.joint4.publish(self.pos4)
			self.joint5.publish(self.pos5)
			rospy.sleep(3)
			
			#hand 
			#self.pos1 = -1.0
			self.pos1 = 0.0
			#self.pos2 = 0.24
			self.pos2 = 0.0
			self.pos3 = 0.639
			self.pos4 = 0.5
			self.pos5 = 0.5
			self.joint1.publish(self.pos1)
			self.joint2.publish(self.pos2)
			self.joint3.publish(self.pos3)
			self.joint4.publish(self.pos4)
			self.joint5.publish(self.pos5)
			rospy.sleep(3)
			#hand open
			#self.pos1 = -1.0
			self.pos1 = 0.0
			#self.pos2 = 0.24
			self.pos2 = 0.0
			self.pos3 = 0.639
			self.pos4 = 0.5
			self.pos5 = 0.0
			self.joint1.publish(self.pos1)
			self.joint2.publish(self.pos2)
			self.joint3.publish(self.pos3)
			self.joint4.publish(self.pos4)
			self.joint5.publish(self.pos5)
			rospy.sleep(3)
			#rospy.sleep(5)
			#hand close 
			#self.pos1 = -1.0
			self.pos1 = 0.0
			#self.pos2 = 0.24
			self.pos2 = 0.0
			self.pos3 = 0.639
			self.pos4 = 0.5
			self.pos5 = 0.8
			self.joint1.publish(self.pos1)
			self.joint2.publish(self.pos2)
			self.joint3.publish(self.pos3)
			self.joint4.publish(self.pos4)
			self.joint5.publish(self.pos5)
			rospy.sleep(3)
			
			# gesture 1
			#self.pos1 = -1.0
			self.pos1 = 0.0
			#self.pos2 = -0.215
			self.pos2 = 0.0
			self.pos3 = 1.508
			self.pos4 = 0.496
			self.pos5 = 0.8
			self.joint1.publish(self.pos1)
			self.joint2.publish(self.pos2)
			self.joint3.publish(self.pos3)
			self.joint4.publish(self.pos4)
			self.joint5.publish(self.pos5)
			rospy.sleep(2)

			# initial gesture
			#self.pos1 = -0.5
			self.pos1 = 0.0
			self.pos2 = -1.86
			#self.pos2 = 0.0
			self.pos3 = 2.44
			self.pos4 = 0.5
			self.pos5 = 0.8
			self.joint1.publish(self.pos1)
			self.joint2.publish(self.pos2)
			self.joint3.publish(self.pos3)
			self.joint4.publish(self.pos4)
			self.joint5.publish(self.pos5)
			rospy.sleep(3)'''
			break
		     
    def cleanup(self):
        rospy.loginfo("Shutting down robot arm....")
if __name__=="__main__":
   rospy.init_node('arm')
   try:
       Loop()
       rospy.spin()
   except rospy.ROSInterruptException:
       pass

