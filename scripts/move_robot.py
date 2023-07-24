#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
colour = " "

class robotmove:

    def __init__(self):
        self.cmd_vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
        self.twist = Twist()
        
    def stop(self):
        rate = rospy.Rate(10)
        #duration = 2
        #start_time = rospy.Time.now().to_sec()
        #while rospy.Time.now().to_sec() - start_time < duration and not rospy.is_shutdown():
        self.twist.linear.x = 0.0 #stop
        self.twist.angular.z = 0.0
        self.cmd_vel_pub.publish(self.twist)
        rate.sleep()

    def straight(self):
        rate = rospy.Rate(10)
        duration = 3
        start_time = rospy.Time.now().to_sec()
        while rospy.Time.now().to_sec() - start_time < duration and not rospy.is_shutdown():
            self.twist.linear.x = 0.05 #move forward
            self.twist.angular.z = 0.0
            self.cmd_vel_pub.publish(self.twist)
            rate.sleep()
        
    def reverse(self):
        rate = rospy.Rate(10)
        duration = 1
        start_time = rospy.Time.now().to_sec()
        while rospy.Time.now().to_sec() - start_time < duration and not rospy.is_shutdown():
            self.twist.linear.x = -0.05 #move forward
            self.twist.angular.z = 0.0
            self.cmd_vel_pub.publish(self.twist)
            rate.sleep()

    def right(self):
        duration = 7
        start_time = rospy.Time.now().to_sec()
        while rospy.Time.now().to_sec() - start_time < duration and not rospy.is_shutdown():
            self.twist.linear.x = 0.0
            self.twist.angular.z = -0.2
            self.cmd_vel_pub.publish(self.twist)

    def move(self):
        if colour == "red":
            self.straight()
            self.twist.linear.x = 0.0
            self.twist.angular.z = 0.0
            self.cmd_vel_pub.publish(self.twist)
            rospy.sleep(1)
        if colour == "blue":
            self.reverse()
            self.twist.linear.x = 0.0
            self.twist.angular.z = 0.0
            self.cmd_vel_pub.publish(self.twist)
            rospy.sleep(1)
        else:
            self.straight()
            #self.stop()
            rospy.sleep(1)
            self.right()
            #self.stop()
            rospy.sleep(1)
            self.straight()
            #self.stop()
            rospy.sleep(1)
            self.reverse()
            #self.stop()
            rospy.sleep(1)

if __name__ == '__main__':
    try:
        rospy.init_node('robot_move')
        robot = robotmove()
        robot.move()
    except rospy.ROSInterruptException:
        pass



