#!/usr/bin/env python3

import rospy
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def movebase_client():

	client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
	client.wait_for_server()
	
	map_type = rospy.get_param('map_type', 'house')
	
	maps = dict()

	locations = dict()
	# locations['Exit'] = Pose(Point(1.081, 0.365, 0.000), Quaternion(0.000, 0.000, 0.000, 0.999))
	# locations['Top_right_room'] = Pose(Point(6.221, 0.633, 0.000), Quaternion(0.000, 0.000, -0.707, 0.707))
	# locations['Mid_left_room'] = Pose(Point(3.517, 4.541, 0.000), Quaternion(0.000, 0.000, 0.999, 0.000))
	# locations['Bottom_room'] = Pose(Point(-4.058, 3.444, 0.000), Quaternion(0.000, 0.000, 0.999, 0.000))
	# locations['Bottom_room_right'] = Pose(Point(-6.279, 2.025, 0.000), Quaternion(0.000, 0.000, -0.707, 0.707))
	
	locations['Exit'] = Pose(Point(1.081, 0.365, 0.000), Quaternion(0.000, 0.000, 0.000, 0.999))
	locations['Top_right_room'] = Pose(Point(8.707, -5.304, 0.000), Quaternion(0.000, 0.000, 0.862, 0.505))
	locations['Mid_left_room'] = Pose(Point(9.225, 3.097, 0.000), Quaternion(0.000, 0.000, 0.999, 0.021))  
	locations['Mid_inside_room'] = Pose(Point(3.762, 0.598, 0.000), Quaternion(0.000, 0.000, 0.732, 0.680))
	locations['central_room'] = Pose(Point(1.528, 3.150, 0.000), Quaternion(0.000, 0.000, -0.999, 0.029))
	locations['Bottom_room'] = Pose(Point(-3.456, 2.259, 0.000), Quaternion(0.000, 0.000, -0.697, 0.716))
	locations['Bottom_room_right'] = Pose(Point(-3.562, -4.2, 0.000), Quaternion(0.000, 0.000, 0.707, 0.707))
	locations['central_room2'] = Pose(Point(1.528, 3.150, 0.000), Quaternion(0.000, 0.000, -0.999, 0.029))
	locations['End'] = Pose(Point(-0.442, -0.076, 0.000), Quaternion(0.000, 0.000, -0.034, 0.999))

	maps['house'] = locations

	goal = MoveBaseGoal()
	goal.target_pose.header.frame_id = "map"
	goal.target_pose.header.stamp = rospy.Time.now()

	# Looping in goal location sequence
	for location in maps[map_type].keys():  
		
		goal = MoveBaseGoal()
		goal.target_pose.header.frame_id = "map"
		goal.target_pose.header.stamp = rospy.Time.now()
		
		goal.target_pose.pose = maps[map_type][location]

		client.send_goal(goal)
		wait = client.wait_for_result()
		if not wait:
		    rospy.logerr("Action server down")
		else:
		    print("Reached " + location + " Goal") 
	return 1

if __name__ == '__main__':
	try:
		rospy.init_node('movebaseClient')
		result = movebase_client()
		if result:
		    rospy.loginfo("All Goals executed")
	except rospy.ROSInterruptException:
		rospy.loginfo("Navigation DONE ")
