
clear all

robot.end_effector = 18;            
robot.base = 40;            
robot.bicep_length = 75;
robot.forearm_length = 100;
robot.servo_step = 0.2;

effector_pos.x = 50;
effector_pos.y = 50;
effector_pos.z = -140;

# contour plots are a bit unstable (win10+octave 4)
range = -100:10:100;

[X,Y] = meshgrid(range,range);

for i = 1:size(X,1)
  for j = 1:size(X,2)
 
    Z(i,j) = delta_resolution(robot, X(i,j), Y(i,j), effector_pos.z);
 
  end
end

Z(isnan(Z))=5;

contour(X,Y,Z,0.3:0.02:1.3)

axis equal