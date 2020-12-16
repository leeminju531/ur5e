#include <ros/ros.h>
#include <tf2_ros/transform_listener.h>
#include <geometry_msgs/TransformStamped.h>
#include <tf2/LinearMath/Quaternion.h>
#include "geometry_msgs/Pose2D.h"
#include "std_msgs/Byte.h"

std_msgs::Byte bottleCount;

int main(int argc,char** argv){

	ros::init(argc, argv, "ur_target_pose_publisher");
	ros::NodeHandle n;
	ros::Publisher targetPosePub = n.advertise<geometry_msgs::Pose2D>("tf/target_pose",10);
	
	geometry_msgs::Pose2D targetPose;


	tf2_ros::Buffer tfBuffer;
	tf2_ros::TransformListener tfListener(tfBuffer);
	ros::Rate rate(10.0);
	while(n.ok()){
		geometry_msgs::TransformStamped transformStamped;
		try{
			transformStamped = tfBuffer.lookupTransform("real_base_link", "target_frame", 
 													ros::Time::now(),ros::Duration(1.0));
		}
		catch(tf2::TransformException &ex){
			ROS_WARN("%s",ex.what());
			ros::Duration(1.0).sleep();  // mean sec
			continue; // -> ★★★★★★ in case by doing 'continue', process restart line 36 (because of 'while')
		}

		targetPose.x = transformStamped.transform.translation.x;
		targetPose.y = transformStamped.transform.translation.y;
 // how to get theta;
		targetPosePub.publish(targetPose);
	}




	return 0;
}