#ROBOROACH 2019
This is a project developed by team ROBOROACH for Robotics couse in Istanbul Technical University.
The robot starts in a room with a wall decorated with colorful shapes (e.g. blue rectangle, red circle, etc.). After taking the desired color-shape tuple as input from end user, robot first finds the wall while avoiding obstacles and following the path, and when it reaches the wall it finds and contours the desired colored shape.
You can see this whole process in the live camera frame, along with rViz's camera section.
Video of the project can be watched from:
https://drive.google.com/open?id=1fhuHtVg1gRs3PutSzMOAPYa2sgTHJGDW


For running this project:
#copy project dir to your working dir
roboroach -> catkin_ws/src

#copy models to the default path
shapewall -> ~/.gazebo/models

#run catkin make
catkin_make

#start the project with gazebo and rviz
roslaunch roboroach robo.launch

#run camera app in src/ dir
cd src
python camera_test.py

#check both the terminal and live frame feed
