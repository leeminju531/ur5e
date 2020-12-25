#!/usr/bin/env python


# monitor z = z - 0.8(table)
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import numpy as np
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
from tf.transformations import *
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Pose2D
from time import sleep

PI = 3.141592
table = 0.8
target_X = 0
target_Y = 0
target_TH = 0
subFlag = False

def updateTargetPose(data):
	global subFlag,target_X,target_Y,target_TH

	if subFlag == True:
		#print ("x : %f || y: %f \n",data.x,data.y)
		target_X = data.x 
		target_Y = data.y
		target_TH = data.theta
	else :
		target_X = 0
		target_Y = 0
		target_TH = 0

#initialize node
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial', anonymous=True)

#provides information such as the robot's kinematics, current joint states
robot = moveit_commander.RobotCommander()
#scene interface -> robot's internel understanding of the surrounding world
scene = moveit_commander.PlanningSceneInterface()

#this object is interface to a planning group
#this interface can be used to plan and execute motions
group_name = "manipulator"
move_group = moveit_commander.MoveGroupCommander(group_name)

#publisher for display in RVIZ
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=20)



# We can get the name of the reference frame for this robot:
planning_frame = move_group.get_planning_frame()
print "============ Reference frame: %s" % planning_frame

# We can also print the name of the end-effector link for this group:
eef_link = move_group.get_end_effector_link()
print "============ End effector: %s" % eef_link

# We can get a list of all the groups in the robot:
group_names = robot.get_group_names()
print "============ Robot Groups:", robot.get_group_names()

# Sometimes for debugging it is useful to print the entire state of the
# robot:
print "============ Printing robot state"
print robot.get_current_state()
print ""


rospy.Subscriber("tf/target_pose",Pose2D,updateTargetPose)




move_group.set_max_velocity_scaling_factor(0.05)
move_group.set_max_acceleration_scaling_factor(0.05)

def gripper_close():
	for i in range(100):
		gripperPub.publish(Int32(1))

def gripper_open():
	for i in range(100):
		gripperPub.publish(Int32(0))
	

# init posture : joint goal -> to avoid singularity 
def settingInitPosture():
	
	joint_goal = move_group.get_current_joint_values()
	joint_goal[0] = np.deg2rad(0)
	joint_goal[1] = np.deg2rad(-90)
	joint_goal[2] = np.deg2rad(0)
	joint_goal[3] = np.deg2rad(-90)
	joint_goal[4] = np.deg2rad(0)
	joint_goal[5] = np.deg2rad(0)
	joint = move_group.set_joint_value_target(joint_goal)
	plan = move_group.plan(joint)
	move_group.execute(plan, wait=True)
	move_group.stop()
	

	joint_goal = move_group.get_current_joint_values()
	joint_goal[0] = np.deg2rad(55)
	joint_goal[1] = np.deg2rad(-90)
	joint_goal[2] = np.deg2rad(0)
	joint_goal[3] = np.deg2rad(-90)
	joint_goal[4] = np.deg2rad(0)
	joint_goal[5] = np.deg2rad(0)
	joint = move_group.set_joint_value_target(joint_goal)
	plan = move_group.plan(joint)
	move_group.execute(plan, wait=True)
	move_group.stop()




def Down_catch_and_up_Bottle():
	####### setting target pose_goal x ,y ,z ######
	# this is fixed position !
	# end-effector location above bottle
	print("down and catch and up start !! ")
	
	pose_goal = move_group.get_current_pose()
	pose_goal.pose.position.x = -0.36877
	pose_goal.pose.position.y = -0.35616
	pose_goal.pose.position.z = table + 0.553
	quaternion = quaternion_from_euler( -PI , 0 ,PI/2)
	pose_goal.pose.orientation.x = quaternion[0]
	pose_goal.pose.orientation.y = quaternion[1]
	pose_goal.pose.orientation.z = quaternion[2]
	pose_goal.pose.orientation.w = quaternion[3]
	move_group.set_pose_target(pose_goal)
	plan = move_group.go(wait=True) ## real plan

	pose_goal = move_group.get_current_pose()
	pose_goal.pose.position.x = -0.36877
	pose_goal.pose.position.y = -0.35616
	pose_goal.pose.position.z = table + 0.453
	quaternion = quaternion_from_euler( -PI , 0 ,PI/2)
	pose_goal.pose.orientation.x = quaternion[0]
	pose_goal.pose.orientation.y = quaternion[1]
	pose_goal.pose.orientation.z = quaternion[2]
	pose_goal.pose.orientation.w = quaternion[3]
	move_group.set_pose_target(pose_goal)
	plan = move_group.go(wait=True) ## real plan

	# end-effector location  head to bottle
	pose_goal = move_group.get_current_pose()
	pose_goal.pose.position.x = -0.36877
	pose_goal.pose.position.y = -0.35616
	pose_goal.pose.position.z = table + 0.3906
	quaternion = quaternion_from_euler( -PI , 0 ,PI/2)
	pose_goal.pose.orientation.x = quaternion[0]
	pose_goal.pose.orientation.y = quaternion[1]
	pose_goal.pose.orientation.z = quaternion[2]
	pose_goal.pose.orientation.w = quaternion[3]
	move_group.set_pose_target(pose_goal)
	plan = move_group.go(wait=True) ## real plan

	#### glipper close ########
	print('glipper close')
	sleep(3)
	#gripper_close()



	pose_goal = move_group.get_current_pose()
	pose_goal.pose.position.x = -0.36877
	pose_goal.pose.position.y = -0.35616
	pose_goal.pose.position.z = table + 0.453
	quaternion = quaternion_from_euler( -PI , 0 ,PI/2)
	pose_goal.pose.orientation.x = quaternion[0]
	pose_goal.pose.orientation.y = quaternion[1]
	pose_goal.pose.orientation.z = quaternion[2]
	pose_goal.pose.orientation.w = quaternion[3]
	move_group.set_pose_target(pose_goal)
	plan = move_group.go(wait=True) ## real plan


	pose_goal = move_group.get_current_pose()
	pose_goal.pose.position.x = -0.36877
	pose_goal.pose.position.y = -0.35616
	pose_goal.pose.position.z = table + 0.552
	quaternion = quaternion_from_euler( -PI , 0 ,PI/2)
	pose_goal.pose.orientation.x = quaternion[0]
	pose_goal.pose.orientation.y = quaternion[1]
	pose_goal.pose.orientation.z = quaternion[2]
	pose_goal.pose.orientation.w = quaternion[3]
	move_group.set_pose_target(pose_goal)
	plan = move_group.go(wait=True) ## real plan
	



# the ur5e will wait in middle position
# until box is stable state 
def middlePos():
	print('end of grasp !!!, start of middle !')
	
	pose_goal = move_group.get_current_pose()
	pose_goal.pose.position.x = -0.36877
	pose_goal.pose.position.y = -0.35616
	pose_goal.pose.position.z = table + 0.552
	quaternion = quaternion_from_euler( -PI , 0 ,PI/2)
	pose_goal.pose.orientation.x = quaternion[0]
	pose_goal.pose.orientation.y = quaternion[1]
	pose_goal.pose.orientation.z = quaternion[2]
	pose_goal.pose.orientation.w = quaternion[3]
	move_group.set_pose_target(pose_goal)
	plan = move_group.go(wait=True) ## real plan

	pose_goal = move_group.get_current_pose()
	pose_goal.pose.position.x = -0.284
	pose_goal.pose.position.y = -0.4264
	pose_goal.pose.position.z = table + 0.552
	quaternion = quaternion_from_euler( -PI , 0 ,PI/2)
	pose_goal.pose.orientation.x = quaternion[0]
	pose_goal.pose.orientation.y = quaternion[1]
	pose_goal.pose.orientation.z = quaternion[2]
	pose_goal.pose.orientation.w = quaternion[3]
	move_group.set_pose_target(pose_goal)
	plan = move_group.go(wait=True) ## real plan

	pose_goal = move_group.get_current_pose()
	pose_goal.pose.position.x = -0.184
	pose_goal.pose.position.y = -0.4964
	pose_goal.pose.position.z = table + 0.552
	quaternion = quaternion_from_euler( -PI , 0 ,PI/2)
	pose_goal.pose.orientation.x = quaternion[0]
	pose_goal.pose.orientation.y = quaternion[1]
	pose_goal.pose.orientation.z = quaternion[2]
	pose_goal.pose.orientation.w = quaternion[3]
	move_group.set_pose_target(pose_goal)
	plan = move_group.go(wait=True) ## real plan

	pose_goal = move_group.get_current_pose()
	pose_goal.pose.position.x = -0.143
	pose_goal.pose.position.y = -0.541
	pose_goal.pose.position.z = table + 0.552
	quaternion = quaternion_from_euler( -PI , 0 ,PI/2)
	pose_goal.pose.orientation.x = quaternion[0]
	pose_goal.pose.orientation.y = quaternion[1]
	pose_goal.pose.orientation.z = quaternion[2]
	pose_goal.pose.orientation.w = quaternion[3]
	move_group.set_pose_target(pose_goal)
	plan = move_group.go(wait=True) ## real plan

	pose_goal = move_group.get_current_pose()
	pose_goal.pose.position.x = -0.043
	pose_goal.pose.position.y = -0.541
	pose_goal.pose.position.z = table + 0.552
	quaternion = quaternion_from_euler( -PI , 0 ,PI/2)
	pose_goal.pose.orientation.x = quaternion[0]
	pose_goal.pose.orientation.y = quaternion[1]
	pose_goal.pose.orientation.z = quaternion[2]
	pose_goal.pose.orientation.w = quaternion[3]
	move_group.set_pose_target(pose_goal)
	plan = move_group.go(wait=True) ## real plan
	
	pose_goal = move_group.get_current_pose()
	pose_goal.pose.position.x = 0.017
	pose_goal.pose.position.y = -0.541
	pose_goal.pose.position.z = table + 0.552
	quaternion = quaternion_from_euler( -PI , 0 ,PI/2)
	pose_goal.pose.orientation.x = quaternion[0]
	pose_goal.pose.orientation.y = quaternion[1]
	pose_goal.pose.orientation.z = quaternion[2]
	pose_goal.pose.orientation.w = quaternion[3]
	move_group.set_pose_target(pose_goal)

	plan = move_group.go(wait=True) ## real plan
	pose_goal = move_group.get_current_pose()
	pose_goal.pose.position.x = 0.117
	pose_goal.pose.position.y = -0.541
	pose_goal.pose.position.z = table + 0.552
	quaternion = quaternion_from_euler( -PI , 0 ,PI/2)
	pose_goal.pose.orientation.x = quaternion[0]
	pose_goal.pose.orientation.y = quaternion[1]
	pose_goal.pose.orientation.z = quaternion[2]
	pose_goal.pose.orientation.w = quaternion[3]
	move_group.set_pose_target(pose_goal)
	plan = move_group.go(wait=True) ## real plan

	pose_goal = move_group.get_current_pose()
	pose_goal.pose.position.x = 0.217
	pose_goal.pose.position.y = -0.541
	pose_goal.pose.position.z = table + 0.552
	quaternion = quaternion_from_euler( -PI , 0 ,PI/2)
	pose_goal.pose.orientation.x = quaternion[0]
	pose_goal.pose.orientation.y = quaternion[1]
	pose_goal.pose.orientation.z = quaternion[2]
	pose_goal.pose.orientation.w = quaternion[3]
	move_group.set_pose_target(pose_goal)
	plan = move_group.go(wait=True) ## real plan

	pose_goal = move_group.get_current_pose()
	pose_goal.pose.position.x = 0.317
	pose_goal.pose.position.y = -0.541
	pose_goal.pose.position.z = table + 0.552
	quaternion = quaternion_from_euler( -PI , 0 ,PI/2)
	pose_goal.pose.orientation.x = quaternion[0]
	pose_goal.pose.orientation.y = quaternion[1]
	pose_goal.pose.orientation.z = quaternion[2]
	pose_goal.pose.orientation.w = quaternion[3]
	move_group.set_pose_target(pose_goal)
	plan = move_group.go(wait=True) ## real plan
	
	pose_goal = move_group.get_current_pose()
	pose_goal.pose.position.x = 0.290
	pose_goal.pose.position.y = -0.441
	pose_goal.pose.position.z = table + 0.552
	quaternion = quaternion_from_euler( -PI , 0 ,PI/2)
	pose_goal.pose.orientation.x = quaternion[0]
	pose_goal.pose.orientation.y = quaternion[1]
	pose_goal.pose.orientation.z = quaternion[2]
	pose_goal.pose.orientation.w = quaternion[3]
	move_group.set_pose_target(pose_goal)
	plan = move_group.go(wait=True) ## real plan

	pose_goal = move_group.get_current_pose()
	pose_goal.pose.position.x = 0.276
	pose_goal.pose.position.y = -0.399
	pose_goal.pose.position.z = table + 0.552
	quaternion = quaternion_from_euler( -PI , 0 ,PI/2)
	pose_goal.pose.orientation.x = quaternion[0]
	pose_goal.pose.orientation.y = quaternion[1]
	pose_goal.pose.orientation.z = quaternion[2]
	pose_goal.pose.orientation.w = quaternion[3]
	move_group.set_pose_target(pose_goal)
	plan = move_group.go(wait=True) ## real plan



if __name__ == "__main__":
	rate = rospy.Rate(1) # 10hz
	print ("state ok ..! push any key to start")
	raw_input()
	

	# glipper open
	while(1):
		if subFlag == False:
			settingInitPosture()
			Down_catch_and_up_Bottle()
			middlePos()
			subFlag=True

		elif subFlag == True:
			print('end of middle , to target position !! ')
			print("X :",target_X ,"y :" ,target_Y,"th(deg) :",target_TH*180/3.14 )
		 	if (target_X != 0 and target_Y != 0 ):
		 		
		 		print("X :",target_X ,"y :" ,target_Y,"th(deg) :",target_TH*180/3.14 )
		 		

		 		pose_goal = move_group.get_current_pose()
		 		pose_goal.pose.position.x = target_X
		 		pose_goal.pose.position.y = target_Y
		 		pose_goal.pose.position.z = table + 0.452
		 		quaternion = quaternion_from_euler( -PI , 0 ,PI/2 + target_TH)
				pose_goal.pose.orientation.x = quaternion[0]
				pose_goal.pose.orientation.y = quaternion[1]
				pose_goal.pose.orientation.z = quaternion[2]
				pose_goal.pose.orientation.w = quaternion[3]
		 		move_group.set_pose_target(pose_goal)
		 		plan = move_group.go(wait=True) ## real plan

		 	

		 		pose_goal = move_group.get_current_pose()
		 		pose_goal.pose.position.x = target_X 
		 		pose_goal.pose.position.y = target_Y
		 		pose_goal.pose.position.z = table + 0.35
		 		quaternion = quaternion_from_euler( -PI , 0 ,PI/2 + target_TH)
				pose_goal.pose.orientation.x = quaternion[0]
				pose_goal.pose.orientation.y = quaternion[1]
				pose_goal.pose.orientation.z = quaternion[2]
				pose_goal.pose.orientation.w = quaternion[3]
		 		move_group.set_pose_target(pose_goal)
		 		plan = move_group.go(wait=True) ## real plan

		 		print("open glipper")
				#gripper_open()
				sleep(2)

		 		pose_goal = move_group.get_current_pose()
		 		pose_goal.pose.position.x = target_X
		 		pose_goal.pose.position.y = target_Y
		 		pose_goal.pose.position.z = table + 0.452
		 		quaternion = quaternion_from_euler( -PI , 0 ,PI/2 + target_TH)
				pose_goal.pose.orientation.x = quaternion[0]
				pose_goal.pose.orientation.y = quaternion[1]
				pose_goal.pose.orientation.z = quaternion[2]
				pose_goal.pose.orientation.w = quaternion[3]
		 		move_group.set_pose_target(pose_goal)
		 		plan = move_group.go(wait=True) ## real plan

		 		

		 		pose_goal = move_group.get_current_pose()
		 		pose_goal.pose.position.x = target_X - 0.3
		 		pose_goal.pose.position.y = target_Y - 0.2
		 		pose_goal.pose.position.z = table + 0.452
		 		quaternion = quaternion_from_euler( -PI , 0 ,PI/2 + target_TH)
				pose_goal.pose.orientation.x = quaternion[0]
				pose_goal.pose.orientation.y = quaternion[1]
				pose_goal.pose.orientation.z = quaternion[2]
				pose_goal.pose.orientation.w = quaternion[3]
		 		move_group.set_pose_target(pose_goal)
		 		plan = move_group.go(wait=True) ## real plan

		 		print("say good bye !")
		 		subFlag = False
		 		