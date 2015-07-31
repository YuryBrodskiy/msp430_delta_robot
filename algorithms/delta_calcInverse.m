function result = delta_calcInverse(robot, x, y, z) 
  sqrt3  = sqrt(3.0);
  sin120 = sqrt3/2.0;
  cos120 = -0.5;
	result.q1 = delta_calcAngleYZ(robot,                   x,                 y, z);
	result.q2 = delta_calcAngleYZ(robot, x*cos120 + y*sin120, y*cos120-x*sin120, z);%  // rotate coords to +120 deg;
	result.q3 = delta_calcAngleYZ(robot, x*cos120 - y*sin120, y*cos120+x*sin120, z); % // rotate coords to -120 deg
 end
	  