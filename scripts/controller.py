#!/usr/bin/env python

import rospy
import tf
import time
from time import sleep
from std_msgs.msg import Float64

FL_JOINT_CMD='/spot/leg_fl_joint_position_controller/command'
FR_JOINT_CMD='/spot/leg_fr_joint_position_controller/command'
RL_JOINT_CMD='/spot/leg_rl_joint_position_controller/command'
RR_JOINT_CMD='/spot/leg_rr_joint_position_controller/command'

class SpotController():
 
    def __init__(self):
	rospy.loginfo('Class constructor TailgateAnimate')

        self.leg_angles = {'fl':0, 'fr':0, 'rl':0, 'rr':0}

        self.fl_joint_pub = rospy.Publisher(FL_JOINT_CMD, Float64, queue_size=1)
        self.fr_joint_pub = rospy.Publisher(FR_JOINT_CMD, Float64, queue_size=1)
        self.rl_joint_pub = rospy.Publisher(RL_JOINT_CMD, Float64, queue_size=1)
        self.rr_joint_pub = rospy.Publisher(RR_JOINT_CMD, Float64, queue_size=1)
	self.leg_pubs = { 'fl':self.fl_joint_pub, 
			  'fr':self.fr_joint_pub, 
			  'rl':self.rl_joint_pub, 
			  'rr':self.rr_joint_pub } 

    def move(self, leg_type, rad):
        self.leg_pubs[leg_type].publish(rad) 
	self.leg_angles[leg_type] = rad

    def home(self):
        for leg in self.leg_pubs:
	    self.leg_pubs[leg].publish(0)
	    self.leg_angles[leg] = 0

    def forward(self):
        self.move('fl',-0.7)
	self.move('rr',-0.7)
        self.move('rl',0)
        self.move('fr',0)
	sleep(1.5)
	self.home()
	sleep(1.5)
        self.move('fr',-0.7)
	self.move('rl',-0.7)
        self.move('rr',0)
        self.move('fl',0)
	sleep(1.5)
	self.home()
	sleep(1.5)


#        self.move('fl',0.5)
#        self.move('rl',-0.5)
#	self.move('fr',0.5)
#        self.move('rr',-0.5)
#	sleep(1)




if __name__ == '__main__':
    rospy.init_node('spot_controller', log_level=rospy.DEBUG)
    sc = SpotController()
    while not rospy.is_shutdown():
	sc.forward()
	#sc.home()

