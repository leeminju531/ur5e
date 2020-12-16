#include <ros/ros.h>
#include "std_msgs/Byte.h"
#include <iostream>
using namespace std;

int main(int argc,char** argv){

	ros::init(argc, argv, "temp_cam_node");
	ros::NodeHandle n;
	ros::Publisher targetPosePub = n.advertise<std_msgs::Byte>("cam/bottle_location",10);
	std_msgs::Byte location;
	ros::Rate rate(10.0);
	while(n.ok()){
		cin >> location.data;
		location.data-=48;
		printf("cam/bottle_location published %d\n",location.data);
		targetPosePub.publish(location);
		rate.sleep();
		ros::spinOnce();

	}

	
}
