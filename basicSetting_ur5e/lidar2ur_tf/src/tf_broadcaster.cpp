#include <ros/ros.h>
#include <tf2_ros/transform_broadcaster.h>
#include <tf2/LinearMath/Quaternion.h>
#include "sensor_msgs/LaserScan.h"
#include "geometry_msgs/Pose2D.h"

#define PI 3.141592
#define X 0
#define Y 1
#define TH 2

 // lidar has noise so frame msg can unstable so filter
float great_fast[3]{};
float fast[3]{};
float cur[3]{};




void updateCur(float x,float y, float th){
	cur[X] = x;
	cur[Y] = y;
	cur[TH] = th;
}
void updateFast(){
	great_fast[X] = fast[X];
	great_fast[Y] = fast[Y];
	great_fast[TH] = fast[TH]; 

	fast[X] = cur[X];
	fast[Y] = cur[Y];
	fast[TH] = cur[TH];
}

void filterFast(){
	//not yet updated
	if(great_fast[X] == 0 && great_fast[Y] == 0 &&  great_fast[Y] == 0)	return;

	float cur_great_distance = sqrt ( pow(cur[X]- great_fast[X],2) + pow(cur[Y]- great_fast[Y],2) );
	float cur_fast_distance = sqrt ( pow(cur[X]- fast[X],2) + pow(cur[Y]- fast[Y],2) );

	//fast noisy case
	if ( abs(cur_great_distance - cur_fast_distance) > 0.2 ){
		
		printf(" noisy case");
		fast[X] = cur[X];
		fast[Y] = cur[Y];
		fast[TH] = cur[TH];
	}

}



void tfcallback(const geometry_msgs::Pose2D msg){
	printf("callback start\n");

	updateCur(msg.x,msg.y,msg.theta);
	filterFast();
	geometry_msgs::TransformStamped transformStamped;
	static tf2_ros::TransformBroadcaster tfb;
	transformStamped.header.stamp = ros::Time::now();

	transformStamped.header.frame_id = "laser_frame";
	transformStamped.child_frame_id = "box_frame";
	transformStamped.transform.translation.x = great_fast[X];
	transformStamped.transform.translation.y = great_fast[Y];
	transformStamped.transform.translation.z = 0.0;
	tf2::Quaternion q;
	q.setRPY(0,0,great_fast[TH]+PI);
	transformStamped.transform.rotation.x = q.x();
	transformStamped.transform.rotation.y = q.y();
	transformStamped.transform.rotation.z = q.z();
	transformStamped.transform.rotation.w = q.w();
	
	tfb.sendTransform(transformStamped);
	printf("sending\n");
	updateFast();
	
}

int main(int argc,char** argv){

	ros::init(argc, argv, "box_broadcaster");
	ros::NodeHandle n;

	ros::Subscriber sub = n.subscribe("lidar/pose",10,tfcallback);
	ros::spin();
	return 0;
}



