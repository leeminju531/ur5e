#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int32
from std_msgs.msg import Byte
import cv2 as cv
import numpy as np

cnt = 0
cap = cv.VideoCapture(2)

#print "Press spacebar to shot"

def counter():
	vita = rospy.Publisher('cam/bottle_location', Byte, queue_size=10)
	rospy.init_node('counter', anonymous=True)
	rate = rospy.Rate(100)
	while not rospy.is_shutdown():
		ret, img_color = cap.read()

		roi_color = img_color[162:339, 264:520]

		img_hsv = cv.cvtColor(roi_color, cv.COLOR_BGR2HSV)
		img_mask = cv.inRange(img_hsv, (12, 160, 50), (24, 220, 220))
		kernel = np.ones((4, 4), np.uint8)
		img_mask = cv.morphologyEx(img_mask, cv.MORPH_DILATE, kernel, iterations=2)

		cnt = 0
		num0fLabels, img_label, stats, centroids = cv.connectedComponentsWithStats(img_mask)
		for idx in range(1, num0fLabels):
			x, y, width, height, area = stats[idx]
			if area > 500:
				cnt+=1
        			cv.rectangle(roi_color, (x, y), (x + width, y + height), (0, 255, 0), 2)
				cv.putText(roi_color, str(cnt), (x,y), 0, 1, (0, 255, 0), 2)

		cv.rectangle(img_color, (520, 162), (264, 339), (0, 255, 0), 2)
		cv.rectangle(img_color, (520, 192), (428, 312), (0, 0, 255), 2)
		roi_color2 = img_color[192:312, 428:520]
		img_hsv2 = cv.cvtColor(roi_color2, cv.COLOR_BGR2HSV)
		img_mask2 = cv.inRange(img_hsv2, (12, 160, 50), (24, 220, 220))
		kernel = np.ones((4, 4), np.uint8)
		img_mask2 = cv.morphologyEx(img_mask2, cv.MORPH_DILATE, kernel, iterations=2)
	    
		trash = cv.countNonZero(img_mask2)
		
		cv.imshow('0', img_color)
		cv.imshow('1', img_mask)

		if cv.waitKey(1) & 0xff == 27:
			break

		if cnt%2 == 1:
			cnt = 0
		elif cnt < 7:
			if trash > 400:
				cnt = 0
			else:
				cnt = (cnt + 2)/2
		else:
			cnt = (cnt + 2)/2

		print cnt
		cnt = 2
		vita.publish(cnt)
		rate.sleep()

if __name__ == '__main__':
	try:
		counter()
	except rospy.ROSInterruptException:
		pass