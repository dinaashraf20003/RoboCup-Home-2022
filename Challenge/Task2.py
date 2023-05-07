#!/usr/bin/env python

"""
    partybot.py - Version 0.2 2019-03-30
    
    A party robot to serve guests and entertainment.
    
"""

import rospy
import actionlib
from actionlib_msgs.msg import *
from std_msgs.msg import String
from sound_play.libsoundplay import SoundClient
import sys
from subprocess import call
from geometry_msgs.msg import Twist
from math import radians
import math
import os
from turtlebot_msgs.srv import SetFollowState
import sys, select, termios, tty
from robot_vision_msgs.msg import HumanPoses
import time
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler

prev = 0
counter = 0
counterFlag = 0
flag = 0
centerx=0
centery=0
eyeL=0
eyeR=0
initialflag=0
flagOut=0
class PartyBot:
    def __init__(self, script_path):
	self.prev = 0
	self.counter = 0
	self.centerx=0
	self.centery=0
	self.counterFlag = 0
	self.eyeL=0
	self.eyeR=0
	self.flag = 0
	self.initialflag = 0
	self.flagOut=0
	initialpose=PoseWithCovarianceStamped()
	self.initialpose = initialpose	
        rospy.init_node('partybot')
        rospy.on_shutdown(self.cleanup)

   def
        
        # Set the default TTS voice to use
        # self.voice = rospy.get_param("~voice", "voice_don_diphone")
        
        # Set the wave file path if used
        self.wavepath = rospy.get_param("~wavepath", script_path + "/../sounds")
        
        # Create the sound client object
        #self.soundhandle = SoundClient()
        self.soundhandle = SoundClient(blocking=True)
        
        # Wait a moment to let the client connect to the sound_play server
        rospy.sleep(1)
        
        # Make sure any lingering sound_play processes are stopped.
        self.soundhandle.stopAll()
        
        # Announce that we are ready for input
        self.soundhandle.playWave(self.wavepath + "/R2D2a.wav")
        #rospy.sleep(1)
        # self.soundhandle.say("Ready")
        
        rospy.loginfo("Ready, waiting for commands...")
	self.soundhandle.say('Hello, I am TurtleBot. What can I do for you?')
	#rospy.sleep(2)

        # Subscribe to the recognizer output and set the callback function
        #rospy.Subscriber('/lm_data', String, self.talkback)
        #rospy.Subscriber('/result', String, self.talkback)
	self.pub = rospy.Publisher('~cmd_vel', Twist, queue_size=5)
	self.dance_arm = rospy.Publisher("dance_arm", String, queue_size=10)
        #habda
        self.arm = rospy.Publisher("arm", String, queue_size=10)
        self.navigation = rospy.Publisher("navigation", String, queue_size=10)
        self.drop = rospy.Publisher("drop", String, queue_size=10)
        self.navigation2 = rospy.Publisher("navigation2", String, queue_size=10)
        self.take_photo = rospy.Publisher("take_photo", String, queue_size=10)
	self.cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)	
	self.A_x = 1.1
	self.A_y = 1.24		
	rospy.Subscriber('/amcl_pose',PoseWithCovarianceStamped,self.callback)
	rospy.Subscriber('/openpose_ros/human_poses',HumanPoses,self.talkback)
	self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
	self.move_base.wait_for_server(rospy.Duration(120))

    def callback(self,msg):
	self.initialpose=msg
	if self.initialflag==0:
		rospy.loginfo("Entred")
		self.A_x = msg.pose.pose.position.x	
		self.A_y = msg.pose.pose.position.y
		rospy.loginfo(self.A_x)
		rospy.loginfo(self.A_y)		
		self.initialflag = 1
    def home(self,msg):
	rospy.loginfo("######################")
	rospy.loginfo(msg.pose.pose.position.x)
	rospy.loginfo(msg.pose.pose.position.y)
	locations = dict()

	# Location A
	A_theta = 0.04

	quaternion = quaternion_from_euler(0.0, 0.0, A_theta)
	locations['A'] = Pose(Point(self.A_x, self.A_y, 0.000), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

	'''self.initialpose.pose.pose.position.x=1.1157656908
	self.initialpose.pose.pose.position.y=1.24977564812
	self.initialpose.pose.pose.orientation.z=-0.999511309061
	self.initialpose.pose.pose.orientation.w=0.0312592875735	
	self.initialpose.pose.covariance=[0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06853892326654787]
	self.initialpose.header.frame_id="map"
	self.initialpose.header.seq=14
	self.initialpose.header.stamp.secs=1656169382
	self.initialpose.header.stamp.nsecs=572415853'''
	self.goal = MoveBaseGoal()
	waiting = 0
	self.goal.target_pose.header.frame_id = 'map'
	self.goal.target_pose.header.stamp = rospy.Time.now()
	while waiting != 1:
		rospy.sleep(2)
		self.goal.target_pose.pose = locations['A']
		self.move_base.send_goal(self.goal)
		#rospy.loginfo("brrrrr")
		
		waiting = self.move_base.wait_for_result(rospy.Duration(300))
		#rospy.loginfo(waiting)
    def control_follow(self, msg):
        rospy.wait_for_service('/turtlebot_follower/change_state')
        change_state = rospy.ServiceProxy('/turtlebot_follower/change_state', SetFollowState)
        response = change_state(msg)
    '''def forward(self,sec):
	timer = time.time()
	while time.time() - timer < sec:
		twist.linear.x = 0.2; twist.linear.y = 0; twist.linear.z = 0
		twist.angular.x = 0; twist.angular.y = 0; twist.angular.z =0
		self.cmd_vel.publish(twist)'''

	
    def talkback(self, msg):
        # Print the recognized words on the screen
        #msg.data=msg.data.lower()
	centerx = 0
	id1 = 0
	#rospy.loginfo(self.initialpose)
	if msg.poses[0].human_id == 0:
		if self.counter != 0:
			if abs(self.prev - msg.poses[0].Chest.x) > 50:
				mini = abs(self.prev - msg.poses[0].Chest.x)
				id1 = 0
				for i in range(0, len(msg.poses)):
					if abs(self.prev - msg.poses[i].Chest.x) < mini:
						mini = msg.poses[i].Chest.x
						id1 = i
		else:
			id1 = 0	
			self.counter = self.counter + 1
		centerx=msg.poses[id1].Chest.x
		centery=msg.poses[id1].Chest.y
		self.prev = centerx
		if centerx<250:
			#rospy.loginfo("L")
			twist = Twist()
			twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
			twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0.4
			self.counterFlag = 0
			self.cmd_vel.publish(twist)
		elif centerx>400:
			#rospy.loginfo("R")
			twist = Twist()
			twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
			twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = -0.4
			self.counterFlag = 0
			self.cmd_vel.publish(twist)
		else :
			#rospy.Subscriber('/camera/depth/points' ,PointCloud2,self.callback)
			#rospy.loginfo("F")
			twist = Twist()
			if centery<300:
				twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
				twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
				#rospy.loginfo("stop")
				self.cmd_vel.publish(twist)
				if self.counterFlag == 0:
					rospy.sleep(0.8)
					self.eyeL=msg.poses[id1].LEye.x
					self.eyeR=msg.poses[id1].REye.x
					#rospy.loginfo("Entering Turning Loop")
					if self.eyeL==-1 and self.eyeR==-1 and self.flag == 0:
						rospy.loginfo("Entered Turning Loop")
						timer = time.time()
						while time.time() - timer < 7:
							#rospy.loginfo("TURN")
							twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
							twist.angular.x = 0; twist.angular.y = 0; twist.angular.z =0.4
							self.cmd_vel.publish(twist)
						timer = time.time()
						while time.time() - timer < 3.5:
							twist.linear.x = 0.2; twist.linear.y = 0; twist.linear.z = 0
							twist.angular.x = 0; twist.angular.y = 0; twist.angular.z =0
							self.cmd_vel.publish(twist)
						timer = time.time()
						while time.time() - timer < 5:
							#rospy.loginfo("TURN")
							twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
							twist.angular.x = 0; twist.angular.y = 0; twist.angular.z =-0.4
							self.cmd_vel.publish(twist)
						timer = time.time()
						while time.time() - timer < 11:
							twist.linear.x = 0.2; twist.linear.y = 0; twist.linear.z = 0
							twist.angular.x = 0; twist.angular.y = 0; twist.angular.z =0
							self.cmd_vel.publish(twist)
						timer = time.time()
						while time.time() - timer < 7:
							#rospy.loginfo("TURN")
							twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
							twist.angular.x = 0; twist.angular.y = 0; twist.angular.z =-0.4
							self.cmd_vel.publish(twist)
						self.flag = 1
					
					if self.eyeL!=-1 and self.eyeR!=-1:
						rospy.loginfo("ay kalb")
						rospy.Subscriber('/amcl_pose',PoseWithCovarianceStamped,self.home)	
					self.counterFlag = 1
			elif self.eyeL!=-1 and self.eyeR!=-1 and self.flag==1:		
				rospy.Subscriber('/amcl_pose',PoseWithCovarianceStamped,self.home)
				rospy.loginfo("resetting flags")
				self.flag = 0
			else: 
				twist.linear.x = 0.2; twist.linear.y = 0; twist.linear.z = 0
				twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
				self.counterFlag = 0		
			self.cmd_vel.publish(twist)
			
	'''while 1:        
		twist = Twist()
		twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
		twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0.2
		self.cmd_vel.publish(twist)'''
	
	
        # Speak the recognized words in the selected voice
        # self.soundhandle.say(msg.data, self.voice)
        # call('rosrun sound_play say.py "montreal"', shell=True)
        # rospy.sleep(1)
        #msg.data= msg.data.lower()
	
    def cleanup(self):
        self.soundhandle.stopAll()
        rospy.loginfo("Shutting down partybot node...")

if __name__=="__main__":
    try:
        PartyBot(sys.path[0])
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Partybot node terminated.")
