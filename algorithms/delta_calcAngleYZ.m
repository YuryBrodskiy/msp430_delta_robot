function result = delta_calcAngleYZ(robot, x0, y0, z0) 
%robot struct short rename and check for all fields
  e = robot.end_effector;            
  f = robot.base ;   
  rf = robot.bicep_length;
  re = robot.forearm_length;

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
		  yj = (y1 - a*b - sqrt(d))/(b*b + 1); % choosing outer povar
		  zj = a + b*yj;
      if (yj>y1)
        tmp= 180.0;
      else
        tmp = 0.0;
      end
		  result = atan(-zj/(y1 - yj)) * 180.0/pi + (tmp);
    end	
end
