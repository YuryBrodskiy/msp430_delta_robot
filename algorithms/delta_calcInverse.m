function result = delta_calcInverse(x0, y0, z0) 
status = delta_calcAngleYZ(x0, y0, z0);
theta1 = 0;
theta2 = 0;
theta3 = 0;
  
  if(status(0) == 0) 
    theta1=status(1);
    status = delta_calcAngleYZ(x0*cos120 + y0*sin120, y0*cos120-x0*sin120, z0, theta2);  // rotate coords to +120 deg
  end
  if(status(0) == 0) {
    theta2=status(1);
    status = delta_calcAngleYZ(x0*cos120 - y0*sin120, y0*cos120+x0*sin120, z0, theta3);  // rotate coords to -120 deg
end
  
  theta3=status(1);

  result = [status(0), theta1,theta2,theta3 );
  end
	  
function result = delta_calcAngleYZ(x0, y0, z0) 
     y1 = -0.5 * 0.57735 * f; % f/2 * tg 30
     y0 -= 0.5 * 0.57735 * e;  % shift center to edge
		   % z = a + b*y
    var a = (x0*x0 + y0*y0 + z0*z0 +rf*rf - re*re - y1*y1)/(2.0*z0);
    var b = (y1-y0)/z0;

    // discriminant
    var d = -(a+b*y1)*(a+b*y1)+rf*(b*b*rf+rf); 
    if (d < 0) return Array(1,0); // non-existing povar.  return error, theta

    var yj = (y1 - a*b - Math.sqrt(d))/(b*b + 1); // choosing outer povar
    var zj = a + b*yj;
    theta = Math.atan(-zj/(y1 - yj)) * 180.0/pi + ((yj>y1)?180.0:0.0);

    return Array(0,theta);  // return error, theta
end