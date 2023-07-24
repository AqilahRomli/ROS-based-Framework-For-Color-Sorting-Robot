#!/usr/bin/env python

import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
var = 0

def none_ball():
    print("unsubcribe_cam")
    rospy.sleep(2)
    image_sub.unregister()

def image_callback(data):
    try:
        cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
        print(e)

    # Convert BGR to HSV
    hsv_image= cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

    # Define the range of the object's color in HSV
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    lower_blue = np.array([110, 50, 50])
    upper_blue = np.array([130, 255, 255])
    lower_green = np.array([50, 50, 50])
    upper_green = np.array([70, 255, 255])
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([179, 255, 30])

    # Threshold the HSV image to get only specified colors
    mask = cv2.inRange(hsv_image, lower_black, upper_black)
    red_mask = cv2.inRange(hsv_image, lower_red, upper_red)
    yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
    blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)
    green_mask = cv2.inRange(hsv_image, lower_green, upper_green)

    # Calculate the centroid of the object
    M = cv2.moments(mask)
    M1 = cv2.moments(red_mask)
    M2 = cv2.moments(yellow_mask)
    M3 = cv2.moments(blue_mask)
    M4 = cv2.moments(green_mask)

    if M['m00'] > 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv2.circle(cv_image, (cx, cy), 20, (0, 255, 255), -1)
        print("black")

    elif M1['m00'] > 0:
        cx = int(M1['m10']/M1['m00'])
        cy = int(M1['m01']/M1['m00'])
        cv2.circle(cv_image, (cx, cy), 20, (0, 0, 255), -1)
        print("red")
        #none_ball()
    elif M2['m00'] > 0:
        cx = int(M2['m10']/M2['m00'])
        cy = int(M2['m01']/M2['m00'])
        cv2.circle(cv_image, (cx, cy), 20, (0, 255, 255), -1)
        print("yellow")
        #none_ball()
    elif M3['m00'] > 0:
        cx = int(M3['m10']/M3['m00'])
        cy = int(M3['m01']/M3['m00'])
        cv2.circle(cv_image, (cx, cy), 20, (255, 0, 0), -1)
        print("blue")
        #none_ball()
    elif M4['m00'] > 0:
        cx = int(M4['m10']/M4['m00'])
        cy = int(M4['m01']/M4['m00'])
        cv2.circle(cv_image, (cx, cy), 20, (0, 255, 0), -1)
        print("green")
        #none_ball()
    else:
        print("none")

    cv2.imshow("Image window", cv_image)
    cv2.waitKey(1)

if __name__ == '__main__':
    rospy.init_node('object_follower')
    while not rospy.is_shutdown():
        bridge = CvBridge()
        image_sub = rospy.Subscriber("/usb_cam/image_raw", Image, image_callback)
        cmd_vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        twist = Twist()
        rospy.sleep(10)


