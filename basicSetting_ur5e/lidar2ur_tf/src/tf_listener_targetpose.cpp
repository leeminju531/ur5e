#include <ros/ros.h>
#include <tf2_ros/transform_listener.h>
#include <geometry_msgs/TransformStamped.h>
#include <tf2/LinearMath/Quaternion.h>
#include "geometry_msgs/Pose2D.h"
#include "std_msgs/Byte.h"
#include <tf/transform_listener.h>


std_msgs::Byte bottleCount;
#define PI 3.141592
float RAD2DEG(float X){return X*180/PI;}		

int main(int argc,char** argv){

	ros::init(argc, argv, "ur_target_pose_publisher");
	ros::NodeHandle n;
	ros::Publisher targetPosePub = n.advertise<geometry_msgs::Pose2D>("tf/target_pose",10);
	
	geometry_msgs::Pose2D targetPose;


	tf2_ros::Buffer tfBuffer;
	tf2_ros::TransformListener tfListener(tfBuffer);
	ros::Rate rate(5.0);
	while(n.ok()){
		geometry_msgs::TransformStamped transformStamped;
		try{
			transformStamped = tfBuffer.lookupTransform("imaginary_base_link", "target_frame", 
 													ros::Time::now(),ros::Duration(1.0));
		}
		catch(tf2::TransformException &ex){
			ROS_WARN("%s",ex.what());
			ros::Duration(1.0).sleep();  // mean sec
			continue; // -> ★★★★★★ in case by doing 'continue', process restart line 36 (because of 'while')
		}

		targetPose.x = transformStamped.transform.translation.x;
		targetPose.y = transformStamped.transform.translation.y;

		tf::Quaternion quat_temp;
		double hole_r,hole_p,hole_y;
		tf::quaternionMsgToTF(transformStamped.transform.rotation,quat_temp);
		tf::Matrix3x3(quat_temp).getRPY(hole_r,hole_p,hole_y);
		printf("roll :%f || pitch :%f || yaw :%f\n",hole_r,hole_p,hole_y);

		if (hole_y < 0 )	hole_y = PI + hole_y;
		else if(hole_y>=0)	hole_y = hole_y - PI; 
		
		targetPose.theta = hole_y;

		
 // how to get theta;
		targetPosePub.publish(targetPose);
		printf("target pose x : %f | y : %f | theta : %f\n",targetPose.x,targetPose.y,RAD2DEG(targetPose.theta) );
		rate.sleep();
	}




	return 0;
}