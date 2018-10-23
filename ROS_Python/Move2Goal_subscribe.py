#!/usr/bin/env python
import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion
from std_msgs.msg import String

class GoToPose():

    def __init__(self):
        #node cycle rate (10 hz)
        self.loop_rate = rospy.Rate(10)
        self.posX =None
        self.posY =None
        self.goal_sent = False
        rospy.wait_for_message('xyPosition',Point)
        rospy.Subscriber ('xyPosition', Point, self.callback)
        rospy.on_shutdown(self.shutdown)
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        rospy.loginfo("Wait for the action server to come up")
        # Allow up to 5 seconds for the action server to come up
        self.move_base.wait_for_server(rospy.Duration(5))


    
        msg=rospy.wait_for_message('xyPosition',Point)
        self.posX =msg.x
        self.posY=msg.y


    def callback (self,message):
        print "pose callback"
        self.posX= message.x
        self.posY= message.y
        #rospy.loginfo("In callback function")
        #position = pose_message
        #print ('x = %f' %self.posX)
        #print ('y = %f' %self.posY)
        rospy.loginfo("X="+ str(self.posX))
        rospy.loginfo("Y="+ str(self.posY))
        
    def goto(self):
        # Send a goal
        #rospy.loginfo("Called the function goto")
        
        self.goal_sent = True
        goal = MoveBaseGoal()
        
        goal.target_pose.header.frame_id = 'base_link'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position= Point (self.posX,self.posY,0.00)  #(pos['x'], pos['y'], 0.000)
        goal.target_pose.pose.orientation=Quaternion (0,0,0,1)#(quat['r1'], quat['r2'], quat['r3'], quat['w'])
	    
        # Start moving
        self.move_base.send_goal(goal)
        #rospy.loginfo("Send goal pose values")
        #rospy.loginfo("x:")

        success = self.move_base.wait_for_result(rospy.Duration(60))# Allow TurtleBot up to 60 seconds to complete task
        state = self.move_base.get_state()
        result = False

        if success and state == GoalStatus.SUCCEEDED:
            # We made it!
            result = True
        else:
            self.move_base.cancel_goal()

        self.goal_sent = False
        return result
        self.loop_rate.sleep()

    def shutdown(self):
        if self.goal_sent:
            self.move_base.cancel_goal()
        rospy.loginfo("Stop")
        rospy.sleep(1)
    
    


if __name__ == '__main__':
    try:
        rospy.init_node('nav_test', anonymous=True)
        navigator = GoToPose()
        # Subscribing the Positon of turtlebot 
                
        # Customize the following values so they are appropriate for your location    
        #position = {'x': 0.1, 'y' : 0.2}
        #quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'w' : 1.000}
        #rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
        success= navigator.goto()
        #success = navigator.goto(position, quaternion)
        if success:
            rospy.loginfo("Hooray, reached the desired pose")
        else:
            rospy.loginfo("The base failed to reach the desired pose")

        # Sleep to give the last log messages time to be sent
        rospy.sleep(1)

    except rospy.ROSInterruptException:
        rospy.loginfo("Ctrl-C caught. Quitting")