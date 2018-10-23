#!/usr/bin/env python
import rospy
from tf.transformations import euler_from_quaternion
#import tf2_ros
import tf
import numpy as np

if __name__ == '__main__':
    rospy.init_node('tf_listener')
    listener = tf.TransformListener()
    now=rospy.Time.now()
    while not rospy.is_shutdown():
        try:
            listener.waitForTransform("/base_link","/map",rospy.Time(0),rospy.Duration(5))
            (trans,rot) = listener.lookupTransform('/map', '/base_link', rospy.Time(0))
            print ("trans:"+str(trans))
            print("rot:"+str(rot))
            print("***************")
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            rospy.loginfo("No transform")
            rate.sleep()
            continue