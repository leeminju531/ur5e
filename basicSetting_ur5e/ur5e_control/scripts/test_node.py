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

