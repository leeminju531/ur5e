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



def callback(data):
	print ("x : %f || y: %f \n",data.x,data.y)




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

rospy.Subscriber("tf/target_pose", Pose2D, callback)

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

raw_input() 

pose_goal = move_group.get_current_pose()
print pose_goal
print "pose getting"














# grasp vita
raw_input() 
joint_goal = move_group.get_current_joint_values()


joint_goal[0] = np.deg2rad(-120.86)
joint_goal[1] = np.deg2rad(-104.15)
joint_goal[2] = np.deg2rad(-114.03)
joint_goal[3] = np.deg2rad(-51.83)
joint_goal[4] = np.deg2rad(87.10)
joint_goal[5] = np.deg2rad(-36.09)

move_group.execute(plan, wait=True)
move_group.stop()



raw_input() 
# waiting until stable state

joint_goal[0] = np.deg2rad(-57.03)
joint_goal[1] = np.deg2rad(-116.88)
joint_goal[2] = np.deg2rad(-85.53)
joint_goal[3] = np.deg2rad(-67.78)
joint_goal[4] = np.deg2rad(86.27)
joint_goal[5] = np.deg2rad(-0.15)

move_group.execute(plan, wait=True)
move_group.stop()

raw_input()

# target pose x ,y , theta setting 
# by subscribe tf listener


pose_goal = move_group.get_current_pose()
pose_goal.pose.position.z -=0.1
move_group.set_pose_target(pose_goal)
print "pose setting"

raw_input()







plan = move_group.go(wait=True)
move_group.stop()
