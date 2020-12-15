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
group_name = "mainpulator"
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

# We can get the joint values from the group and adjust some of the values:
joint_goal = move_group.get_current_joint_values()


joint_goal[0] = np.deg2rad(-121.16)
joint_goal[1] = np.deg2rad(-97.74)
joint_goal[2] = np.deg2rad(-119.09)
joint_goal[3] = np.deg2rad(-41.52)
joint_goal[4] = np.deg2rad(87.1)
joint_goal[5] = np.deg2rad(-36.09)


plan = move_group.plan(joint_goal)
move_group.execute(plan, wait=True)
move_group.stop()
# grasp vita

print ("grasp vita 500")

joint_goal[0] = np.deg2rad(-37.5)
joint_goal[1] = np.deg2rad(-92.74)
joint_goal[2] = np.deg2rad(-118.84)
joint_goal[3] = np.deg2rad(-54.97)
joint_goal[4] = np.deg2rad(86.95)
joint_goal[5] = np.deg2rad(-36.09)

