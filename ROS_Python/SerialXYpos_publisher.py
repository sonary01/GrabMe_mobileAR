#!/usr/bin/env python
#import roslib; roslib.load_manifest('numpy_tutorials') 

import rospy
from std_msgs.msg import Float32
import serial
from geometry_msgs.msg import Point

ser = serial.Serial('/dev/ttyUSB0', 9600)

def poseRecieve():
    count = 0
    position_message = Point()
    rospy.init_node('serialReader',anonymous= True)
    pub = rospy.Publisher('xyPosition', Point, queue_size =2)
    rate= rospy.Rate(10)
    
    while True:
        if not rospy.is_shutdown():
            if ser.inWaiting():
                data= ser.readline()
                #data= ser.read(1)
                count = count+1
                if count == 1:
                    #print("count:")
                    #print(count)
                    #print(data)

                    # The unity coordinates uses LH system. So,inversing the X values,
                    # Unity is LHS system, so Unity x = -y coordinate in robot system
                    # Unity y = x coordinate of robot 
                    position_message.y = -(float(data))
                elif count ==2:
                    #print("count:")
                    #print(count)
                    #print(data)
                    position_message.x = float(data)    
                    print("poseX="+ str(position_message.x))
                    print("poseY="+ str(position_message.y))
                    #rospy.sleep(1)
                    pub.publish(position_message)
                    count=0  
            #else:
                #
                # print( "no data available")
        else:
            break
if __name__ == '__main__':
  try:
    
    poseRecieve()
  except rospy.ROSInterruptException:
    pass
