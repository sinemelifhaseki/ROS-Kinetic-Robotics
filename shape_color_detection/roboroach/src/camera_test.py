import rospy
import sys
from sensor_msgs.msg import Image, LaserScan
import matplotlib.pyplot as plt
import time
import numpy as np
import cv2
import base64
from geometry_msgs.msg import PoseStamped

print("**************************HELLO I AM ROBOROACH!**************************")
print("********************I WILL FIND THE COLOR AND SHAPE**********************")
print("What do you desire?")
user = raw_input()
colorname, shapename = user.split(" ")
print("Hmm, let's see if there is a " + colorname + " " + shapename)
font = cv2.FONT_HERSHEY_COMPLEX
prnt = 0

def displayImage(image):
    plt.imshow(image)
    plt.show()
    
def illcallyouback(data):
    global prnt
    h, w = data.height, data.width
    flag = 0
    frame = np.fromstring(data.data, dtype='>u1').reshape(h,w,3)[..., ::-1]
    frame = np.array(frame)
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    if colorname == "blue":
        l_h = 10
        l_s = 179
        l_v = 160
        u_h = 50
        u_s = 255
        u_v = 170
    elif colorname == "yellow":
        l_h = 0
        l_s = 130
        l_v = 227
        u_h = 180
        u_s = 255
        u_v = 255
    elif colorname == "green":
        l_h = 30
        l_s = 136
        l_v = 18
        u_h = 90
        u_s = 255
        u_v = 243
    elif colorname == "red":
        l_h = 93
        l_s = 13
        l_v = 164
        u_h = 180
        u_s = 255
        u_v = 243

    lower_red = np.array([l_h, l_s, l_v])
    upper_red = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel)

    # Contours detection
    if int(cv2.__version__[0]) > 3:
        # Opencv 4.x.x
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    else:
        # Opencv 3.x.x
        _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]

        if area > 400:
            cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)
            

            if len(approx) == 3:
                if shapename == "triangle":
                    flag = 1
                    string = 'Eureka! I have seen a '+ colorname+ ' triangle!'
                    prnt = 1
                    cv2.putText(frame, "Triangle", (x, y), font, 1, (0, 0, 0))
                    break
            elif len(approx) == 4:
                if shapename == "rectangle":
                    flag = 1
                    string = 'Eureka! I have seen a '+ colorname+ ' rectangle!'
                    prnt = 1
                    cv2.putText(frame, "Rectangle", (x, y), font, 1, (0, 0, 0))
                    break
            elif 5 < len(approx):
                if shapename == "circle":
                    flag = 1
                    string = 'Eureka! I have seen a '+ colorname+ ' circle!'
                    prnt = 1
                    cv2.putText(frame, "Circle", (x, y), font, 1, (0, 0, 0))
                    break
    
    #h, w = data.height, data.width
        
    cv2.imshow('Frame',frame[..., ::-1])
    if cv2.waitKey(25) & 0xFF == ord('q'):
        return

def laser_callback(data):
   print(data) 

def node():
    rospy.init_node('amble')
    rospy.Subscriber("/camera/rgb/image_raw", Image, illcallyouback, queue_size = 1000)
    pub = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size = 1000)
    rospy.sleep(5)

    goal1 = PoseStamped()
    goal1.header.frame_id = "map"
    goal1.header.stamp = rospy.Time.now()
    goal1.pose.position.x = 10.299451828
    goal1.pose.position.y = 6.46806716919
    goal1.pose.position.z = 0.0
    goal1.pose.orientation.w =0.718696551932
    goal1.pose.orientation.z = -0.695323857092
    pub.publish(goal1)
    rospy.sleep(23)

    goal = PoseStamped()
    goal.header.frame_id = "map"
    goal.header.stamp = rospy.Time.now()
    goal.pose.position.x = 9.75285053253
    goal.pose.position.y = 1.99568319321
    goal.pose.position.z = 0.0
    goal.pose.orientation.w = 1.0
    goal.pose.orientation.z = 0.0
    pub.publish(goal)
    rospy.sleep(20)


    goal2 = PoseStamped()
    goal2.header.frame_id = "map"
    goal2.header.stamp = rospy.Time.now()
    goal2.pose.position.x = 3.01921746254
    goal2.pose.position.y = 6.91606079102
    goal2.pose.position.z = 0.0
    goal2.pose.orientation.w = 0.640244253399
    goal2.pose.orientation.z = 0.768142859432
    pub.publish(goal2)
    rospy.sleep(17)

    goal5 = PoseStamped()
    goal5.header.frame_id = "map"
    goal5.header.stamp = rospy.Time.now()
    goal5.pose.position.x = 3.27724266052
    goal5.pose.position.y = 8.27506637573
    goal5.pose.position.z = 0.0
    goal5.pose.orientation.w = 0.814810943173
    goal5.pose.orientation.z = 0.579726769164
    pub.publish(goal5)
    rospy.sleep(4)

    if prnt:
        print('Eureka! I have seen a '+ colorname+ " "+shapename)
    else:
        print("Roboroach couldn't find any " + colorname +" "+ shapename+"s")
    rospy.spin()
    
if __name__ == '__main__':
    node()