#include <ros/ros.h>
#include <tf2_ros/transform_broadcaster.h>
#include <tf2/LinearMath/Quaternion.h>
#include "sensor_msgs/LaserScan.h"
#include "geometry_msgs/Pose2D.h"

#define PI 3.141592


int main(int argc,char** argv){

	ros::init(argc, argv, "lidar_broadcaster");
	ros::NodeHandle n;

	//ros::Subscriber sub = n.subscribe("lidar/pose",10,tfcallback);
	
	geometry_msgs::TransformStamped transformStamped;
	tf2_ros::TransformBroadcaster tfb;
	transformStamped.header.stamp = ros::Time::now();

	transformStamped.header.frame_id = "laser_frame"; // ur base_link
	transformStamped.child_frame_id = "imaginary_base_link";
	transformStamped.transform.translation.x = 0.28707;
	transformStamped.transform.translation.y = -0.67003;
	transformStamped.transform.translation.z = 0.0;
	tf2::Quaternion q;
	q.setRPY(0,0,PI/2);
	transformStamped.transform.rotation.x = q.x();
	transformStamped.transform.rotation.y = q.y();
	transformStamped.transform.rotation.z = q.z();
	transformStamped.transform.rotation.w = q.w();

	ros::Rate rate(5.0);

	while(n.ok()){
		transformStamped.header.stamp = ros::Time::now();
		tfb.sendTransform(transformStamped);
		rate.sleep();
	}



	return 0;
}

