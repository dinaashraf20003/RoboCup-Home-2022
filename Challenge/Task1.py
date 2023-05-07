#!/usr/bin/env python

"""
    partybot.py - Version 0.2 2019-03-30
    
    A party robot to serve guests and entertainment.
    
"""

import rospy
from std_msgs.msg import String
from sound_play.libsoundplay import SoundClient
from std_msgs.msg import Header
from opencv_apps.msg import RotatedRectStamped
from robot_vision_msgs.msg import BoundingBoxes
import sys
from subprocess import call
from geometry_msgs.msg import Twist
from math import radians
import os
from turtlebot_msgs.srv import SetFollowState
flag = 0
enable = 1
state = 0

class PartyBot:
    def __init__(self, script_path):
	self.flag = 0
	self.enable = 1
	self.state = 0
        rospy.init_node('Task1')

        rospy.on_shutdown(self.cleanup)
        
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
	self.soundhandle.say('Hello, I am PartyBot. What can I do for you?')
	#rospy.sleep(2)

        # Subscribe to the recognizer output and set the callback function
        #rospy.Subscriber('/lm_data', String, self.talkback)
	self.dance_arm = rospy.Publisher("dance_arm", String, queue_size=10)
        #habda
        self.arm = rospy.Publisher("arm", String, queue_size=10)
        self.navigation = rospy.Publisher("navigation", String, queue_size=10)
        self.drop = rospy.Publisher("drop", String, queue_size=10)
        self.navigation2 = rospy.Publisher("navigation2", String, queue_size=10)
        self.take_photo = rospy.Publisher("take_photo", String, queue_size=10)
	self.cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
	rospy.Subscriber('/result', String, self.talkback, queue_size=1)
	self.control_follow(0)
	#rospy.Subscriber('/lm_data', String, self.talkback)
    def callback(self, data):
	    #rospy.loginfo(rospy.get_time())
	    for i in data.bounding_boxes:
	    	#rospy.loginfo(i.Class)
		x = i.Class
		if (x == 'umbrella' or x == 'laptop' or x == 'laptopbag' or x == 'stopsign' or x == 'suitcase' or x == 'handbag' or x == 'bag') and self.flag == 0:
			self.soundhandle.playWave(self.wavepath + "/R2D2a.wav")
			#rospy.sleep(1)
			self.soundhandle.say("Bag Detected")
			#rospy.sleep(5)
			self.arm.publish('arm')
		        self.control_follow(0)
			self.flag = 1
			break
    def control_follow(self, msg):
        rospy.wait_for_service('/turtlebot_follower/change_state')
        change_state = rospy.ServiceProxy('/turtlebot_follower/change_state', SetFollowState)
        response = change_state(msg)

    def talkback(self, msg):
        # Print the recognized words on the screen
        #msg.data=msg.data.lower()
        rospy.loginfo(msg.data)
        
        # Speak the recognized words in the selected voice
        # self.soundhandle.say(msg.data, self.voice)
        # call('rosrun sound_play say.py "montreal"', shell=True)
        # rospy.sleep(1)
        #msg.data= msg.data.lower()

	if (msg.data.find('carry')>-1 or msg.data.find('bag')>-1 or msg.data.find('back')>-1 or msg.data.find('gary')>-1 or msg.data.find('daddy')>-1 or msg.data.find('caravan')>-1 or msg.data.find('carobel')>-1 or msg.data.find('teddy')>-1 or msg.data.find('bear')>-1) and self.enable == 1:
        	self.soundhandle.playWave(self.wavepath + "/R2D2a.wav")
        	#rospy.sleep(1)
		self.soundhandle.say("OKIE. Searching for Bag.")
		while self.flag == 0:
			rospy.Subscriber('yolo_ros/bounding_boxes', BoundingBoxes, 		self.callback,queue_size=1)
			#rospy.sleep(5)
                	self.control_follow(0)
		self.enable = 0	
	elif msg.data.find('follow')>-1:
		if self.state == 0:
			self.soundhandle.playWave(self.wavepath + "/R2D2a.wav")
			#rospy.sleep(1)
			self.soundhandle.say("OK. I will start follow you.")
			#rospy.sleep(5)
			self.state = 1
                self.control_follow(1)
	elif msg.data.find('stop')>-1 or msg.data.find('drop')>-1:
		if self.state == 1:
			rospy.loginfo("Stoppppppppppppppppppp")
			self.soundhandle.playWave(self.wavepath + "/R2D2a.wav")
			#rospy.sleep(1)
			self.soundhandle.say("OK. I will stop follow you.")
			#rospy.sleep(5)
			self.state = 0	
                	self.drop.publish('drop')
                self.control_follow(0)	
        elif msg.data.find('drop')>-1:
        	#self.soundhandle.playWave(self.wavepath + "/R2D2a.wav")
        	#rospy.sleep(1)		
                self.control_follow(0)
		self.soundhandle.say("You want me to drop your luggage? sure. let me do it")
		#rospy.sleep(5)
		
                self.drop.publish('drop')      	
		#self.soundhandle.playWave(self.wavepath + "/swtheme.wav", blocking=False)
	#else: self.soundhandle.say("Sorry, I cannot hear you clearly. Please say again.")
	else: rospy.sleep(3)
        
        # Uncomment to play one of the built-in sounds
        #rospy.sleep(2)
        #self.soundhandle.play(5)
        
        # Uncomment to play a wave file
        #rospy.sleep(2)
        #self.soundhandle.playWave(self.wavepath + "/R2D2a.wav")

    def cleanup(self):
        self.soundhandle.stopAll()
        rospy.loginfo("Shutting down partybot node...")
    

if __name__=="__main__":
    try:
        PartyBot(sys.path[0])
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Partybot node terminated.")
