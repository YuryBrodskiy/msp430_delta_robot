robot.end_effector = 18;            
robot.base = 40;            
robot.bicep_length = 90;
robot.forearm_length = 130;
robot.servo_step = 0.5;

theta1=25;
theta2=25;
theta3=25;
H = delta_calcForward(robot, theta1, theta2, theta3) 
H = delta_calcForward(robot, theta1-1, theta2+1, theta3+1) 
H = delta_calcForward(robot, theta1+1, theta2-1, theta3+1) 
H = delta_calcForward(robot, theta1+1, theta2+1, theta3-1) 
%q = delta_calcInverse(robot, H.x,H.y, H.z)
