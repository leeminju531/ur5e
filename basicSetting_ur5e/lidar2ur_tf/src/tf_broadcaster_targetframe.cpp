#include <ros/ros.h>
#include <tf2_ros/transform_broadcaster.h>
#include <tf2/LinearMath/Quaternion.h>
#include "std_msgs/Byte.h"

#define PI 3.141592

#define bottle_delta_x 0.0310
#define bottle_delta_y 0.0450

#define hardware_offset 0.0100

void tfcallback(const std_msgs::Byte msg){

	double x,y;
	int data = msg.data;

	switch(data){
		case 1:
			x = data*bottle_delta_x;
			y = bottle_delta_y;
			break;
		case 2:
			x = data*bottle_delta_x ;
			y = bottle_delta_y;
			break;
		case 3:
			x = data*bottle_delta_x ;
			y = bottle_delta_y;
			break;
		case 4:
			x = data*bottle_delta_x ;
			y = bottle_delta_y;
			break;
		case 5:
			x = data*bottle_delta_x ;
			y = bottle_delta_y;
			break;
		default :
			printf("subscribed data : %d so end! \n",msg.data);
			return;
	
	}	
	printf("out case subscribed data : %d\n",msg.data);
	printf("x : %f || y : %f \n",x,y);

	geometry_msgs::TransformStamped transformStamped;
	static tf2_ros::TransformBroadcaster tfb;
	transformStamped.header.stamp = ros::Time::now();

	transformStamped.header.frame_id = "box_frame"; // ur base_link
	transformStamped.child_frame_id = "target_frame";
	transformStamped.transform.translation.x = x;
	transformStamped.transform.translation.y = y;
	transformStamped.transform.translation.z = 0.2;
	tf2::Quaternion q;
	q.setRPY(0,0,0);
	transformStamped.transform.rotation.x = q.x();
	transformStamped.transform.rotation.y = q.y();
	transformStamped.transform.rotation.z = q.z();
	transformStamped.transform.rotation.w = q.w();
	
	tfb.sendTransform(transformStamped);
}

int main(int argc,char** argv){

	ros::init(argc, argv, "targetFrame_broadcaster");
	ros::NodeHandle n;
	ros::Rate rate(5.0);
	ros::Subscriber sub = n.subscribe("cam/bottle_location",10,tfcallback);
	// while(ros::ok()){
	// 	geometry_msgs::TransformStamped transformStamped;
	// 	static tf2_ros::TransformBroadcaster tfb;
	// 	transformStamped.header.stamp = ros::Time::now();

	// 	transformStamped.header.frame_id = "box_frame"; // ur base_link
	// 	transformStamped.child_frame_id = "target_frame";
	// 	transformStamped.transform.translation.x = bottle_delta_x;
	// 	transformStamped.transform.translation.y = bottle_delta_y;
	// 	transformStamped.transform.translation.z = 0.2;
	// 	tf2::Quaternion q;
	// 	q.setRPY(0,0,0);
	// 	transformStamped.transform.rotation.x = q.x();
	// 	transformStamped.transform.rotation.y = q.y();
	// 	transformStamped.transform.rotation.z = q.z();
	// 	transformStamped.transform.rotation.w = q.w();
		
	// 	tfb.sendTransform(transformStamped);
	// 	rate.sleep();
	// }
	

	ros::spin();
	return 0;
}

