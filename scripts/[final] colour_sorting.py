#!/usr/bin/env python

import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
colour = " "
colour_det = " "
count = 0
count1 = 0

class Ball_detect:

    def unsubscribe(self):
        print("unsubcribe")
        self.image_sub.unregister()

    def red_ball(self):
        self.unsubscribe()
        print("red ball")
        global colour,count
        colour = "red"
        count = 1

    def yellow_ball(self):
        self.unsubscribe()
        print("yellow ball")
        global colour,count
        colour = "yellow"
        count = 1

    def blue_ball(self):
        self.unsubscribe()
        print("blue ball")
        global colour,count
        colour = "blue"
        count = 1

    def green_ball(self):
        self.unsubscribe()
        print("green ball")
        global colour,count
        colour = "green"
        count = 1

    def none_ball(self):
        self.unsubscribe()
        print("none")

    def forward(self):
        loop = 0
        while loop < 25:
            self.twist.linear.x = 0.1 #move forward
            self.twist.angular.z = 0.0
            self.cmd_vel_pub.publish(self.twist)
            rospy.sleep(0.1)
            loop += 1

    def ball_callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        # Convert BGR to HSV
        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

        # Define the range of the object's color in HSV
        lower_red = np.array([0, 50, 50])
        upper_red = np.array([10, 255, 255])
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])
        lower_blue = np.array([78, 158, 124])
        upper_blue = np.array([138, 255, 255])
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([70, 255, 255])

        # Threshold the image to get only the pixels in the range
        red_mask = cv2.inRange(hsv, lower_red, upper_red)
        yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
        green_mask = cv2.inRange(hsv, lower_green, upper_green)

        #Calculate the centroid of the object
        M1 = cv2.moments(red_mask)
        M2 = cv2.moments(yellow_mask)
        M3 = cv2.moments(blue_mask)
        M4 = cv2.moments(green_mask)

        if M1['m00'] > 0:
            cx = int(M1['m10']/M1['m00'])
            cy = int(M1['m01']/M1['m00'])
            cv2.circle(cv_image, (cx, cy), 20, (0, 0, 255), -1)
            #Adjust the robot's velocity based on the centroid's position
            self.forward()
            self.red_ball()
            cv2.imshow("Image window", cv_image)
            cv2.waitKey(0)

        elif M2['m00'] > 0:
            cx = int(M2['m10']/M2['m00'])
            cy = int(M2['m01']/M2['m00'])
            cv2.circle(cv_image, (cx, cy), 20, (0, 255, 255), -1)
            self.forward()
            self.yellow_ball()
            cv2.imshow("Image window", cv_image)
            cv2.waitKey(1)

        elif M4['m00'] > 0:
            cx = int(M4['m10']/M4['m00'])
            cy = int(M4['m01']/M4['m00'])
            cv2.circle(cv_image, (cx, cy), 20, (0, 255, 0), -1)
            self.forward()
            self.green_ball()
            cv2.imshow("Image window", cv_image)
            cv2.waitKey(1)

        elif M3['m00'] > 0:
            cx = int(M3['m10']/M3['m00'])
            cy = int(M3['m01']/M3['m00'])
            cv2.circle(cv_image, (cx, cy), 20, (255, 0, 0), -1)
            self.forward()
            self.blue_ball()
            cv2.imshow("Image window", cv_image)
            cv2.waitKey(1)

        else:
            self.none_ball()
            cv2.imshow("Image window", cv_image)
            cv2.waitKey(0)



class location_detect:

    def unsubscribe(self):
        print("unsubcribe")
        self.image_sub.unregister()

    def location(self):
        self.unsubscribe()
        if colour == colour_det:
            if percentage_pixels > 0.45:
                print("majority colour", percentage_pixels)
                self.move3() 
                global count1
                count1 = 2
                rospy.sleep(1)
            else:
                print("not majority colour", percentage_pixels)
                self.move2()    
        else:
            self.move2()

    def move1(self):
        self.unsubscribe()
        self.twist.linear.x = 0.0
        self.twist.angular.z = 0.2
        self.cmd_vel_pub.publish(self.twist)
        rospy.sleep(0.1)

    def move2(self):
        self.unsubscribe()
        self.twist.linear.x = 0.1
        self.twist.angular.z = 0.00
        self.cmd_vel_pub.publish(self.twist)
        rospy.sleep(0.1)

    def move3(self):
        self.unsubscribe()
        self.twist.linear.x = 0.2
        self.twist.angular.z = 0.0
        self.cmd_vel_pub.publish(self.twist)
        rospy.sleep(0.3)

    def image_callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        # Convert BGR to HSV
        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

        # Define the range of the object's color in HSV
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([179, 255, 30])
        lower_red = np.array([0, 50, 50])
        upper_red = np.array([10, 255, 255])
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])
        lower_blue = np.array([78, 158, 124])
        upper_blue = np.array([138, 255, 255])
        lower_green = np.array([50, 100, 100])
        upper_green = np.array([70, 255, 255])

        # Threshold the image to get only the pixels in the range
        mask = cv2.inRange(hsv, lower_black, upper_black)
        red_mask = cv2.inRange(hsv, lower_red, upper_red)
        yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
        green_mask = cv2.inRange(hsv, lower_green, upper_green)

        # Calculate numbers of pixels
        global total_pixels, red_pixels, percentage_pixels
        total_pixels = cv_image.shape[0] * cv_image.shape[1]
        red_pixels = cv2.countNonZero(red_mask)
        yellow_pixels = cv2.countNonZero(yellow_mask)
        blue_pixels = cv2.countNonZero(blue_mask)
        green_pixels = cv2.countNonZero(green_mask)

        #Calculate the centroid of the object
        global colour_det
        M = cv2.moments(mask)
        M1 = cv2.moments(red_mask)
        M2 = cv2.moments(yellow_mask)
        M3 = cv2.moments(blue_mask)
        M4 = cv2.moments(green_mask)

        if M['m00'] > 0:
            #robot make a turn if detect black colour
            self.move1()

        elif M1['m00'] > 0:
           colour_det = "red"
           print ("red detected!")
           percentage_pixels = (red_pixels / float(total_pixels))
           self.location()

        elif M2['m00'] > 0:
           colour_det = "yellow"
           print ("yellow detected!")
           percentage_pixels = (yellow_pixels / float(total_pixels))
           self.location()

        elif M4['m00'] > 0:
           colour_det = "green"
           print ("green detected!")
           percentage_pixels = (green_pixels / float(total_pixels))
           self.location()

        elif M3['m00'] > 0:
           colour_det = "blue"
           percentage_pixels = (blue_pixels / float(total_pixels))
           self.location()

        else:
            #Robot move straight if not detect black colour
            self.move2()

def detect(self):
    while count == 0:
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/usb_cam/image_raw", Image, self.ball_callback)
        self.cmd_vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        self.twist = Twist()
        rospy.sleep(10)
        if rospy.is_shutdown():
            global count1
            count1 = 2
            break

def find(self):
    while count == 1 and count1 != 2:
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/usb_cam/image_raw", Image, self.image_callback)
        self.cmd_vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        self.twist = Twist()
        rospy.sleep(0.3)
        if rospy.is_shutdown():
            break

if __name__ == '__main__':
    rospy.init_node('object_follower')
    follower = Ball_detect()
    road = location_detect()
    detect(follower)
    find(road)
    
