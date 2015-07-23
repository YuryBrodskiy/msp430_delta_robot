function result = delta_calcInverse(robot, x0, y0, z0) 
	status = delta_calcAngleYZ(robot, x0, y0, z0);
	result.theta1 = delta_calcAngleYZ(robot, x0, y0, z0);
	result.theta2 = delta_calcAngleYZ(robot, x0*cos120 + y0*sin120, y0*cos120-x0*sin120, z0, theta2);%  // rotate coords to +120 deg;
	result.theta3 = delta_calcAngleYZ(robot, x0*cos120 - y0*sin120, y0*cos120+x0*sin120, z0, theta3); % // rotate coords to -120 deg
 end
	  
function result = delta_calcAngleYZ(robot, x0, y0, z0) 
	y1 = -0.5 * 0.57735 * f; % f/2 * tg 30
    y0 -= 0.5 * 0.57735 * e;  % shift center to edge
		   % z = a + b*y
    a = (x0*x0 + y0*y0 + z0*z0 +rf*rf - re*re - y1*y1)/(2.0*z0);
    b = (y1-y0)/z0;

    %// discriminant
    d = -(a+b*y1)*(a+b*y1)+rf*(b*b*rf+rf); 
    if d < 0 
		result = NaN;%  non-existing povar.  return error, theta
	else
		yj = (y1 - a*b - sqrt(d))/(b*b + 1); // choosing outer povar
		zj = a + b*yj;
		result = atan(-zj/(y1 - yj)) * 180.0/pi + ((yj>y1)?180.0:0.0);
    end	
end
