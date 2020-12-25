#!/usr/bin/env python
import rospy
import os
from std_msgs.msg import Int32

from dynamixel_sdk import * 
# Control table address is different in Dynamixel model
ADDR_PRO_TORQUE_ENABLE = 64
ADDR_PRO_GOAL_POSITION = 116
ADDR_PRO_PRESENT_POSITION = 132

# Protocol version
PROTOCOL_VERSION = 2.0

# Default setting
DXL_ID1 = 1
DXL_ID2 = 2
BAUDRATE = 57600
print ("zz")
DEVICENAME = '/dev/ttyUSB1'
print ("zss")
TORQUE_ENABLE = 1
TORQUE_DISABLE = 0
DXL_MOVING_STATUS_THRESHOLD = 10
DXL_MINIMUM_POSITION_VALUE1 = 1254
DXL_MAXIMUM_POSITION_VALUE1 = 1529
DXL_MINIMUM_POSITION_VALUE2 = 1270
DXL_MAXIMUM_POSITION_VALUE2 = 1549

index = 0
dxl_goal_position1 = [DXL_MINIMUM_POSITION_VALUE1, DXL_MAXIMUM_POSITION_VALUE1]
dxl_goal_position2 = [DXL_MINIMUM_POSITION_VALUE2, DXL_MAXIMUM_POSITION_VALUE2]

# Initialize PortHandler instance
portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)
if portHandler.openPort():
	print("Succeeded to open the port")
if portHandler.setBaudRate(BAUDRATE):
	print("Succeeded to change the baudrate")

# Enable Dynamixel Torque
dxl_comm_result1, dxl_error1 = packetHandler.write1ByteTxRx(portHandler, DXL_ID1, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
dxl_comm_result2, dxl_error2 = packetHandler.write1ByteTxRx(portHandler, DXL_ID2, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)

def couter_callback(data):
	print data
	if data == Int32(1):
		print('close')
		index = 1
	else:
		print('open')
		index = 0
	dxl_comm_result1, dxl_error1 = packetHandler.write4ByteTxRx(portHandler, DXL_ID1, ADDR_PRO_GOAL_POSITION, dxl_goal_position1[index])
	dxl_comm_result2, dxl_error2 = packetHandler.write4ByteTxRx(portHandler, DXL_ID2, ADDR_PRO_GOAL_POSITION, dxl_goal_position2[index])

def listener():
	global index
	rospy.init_node('listener', anonymous = True)
	rospy.Subscriber("gripper", Int32, couter_callback)
	rospy.spin()

if __name__ == '__main__':
	listener()
	

	# Disable Dynamixel Torque
	dxl_comm_result1, dxl_error1 = packetHandler.write1ByteTxRx(portHandler, DXL_ID1, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
	dxl_comm_result2, dxl_error2 = packetHandler.write1ByteTxRx(portHandler, DXL_ID2, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
	# Close port
	portHandler.closePort()