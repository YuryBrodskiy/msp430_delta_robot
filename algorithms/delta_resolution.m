function result = delta_resolution(robot, x0, y0, z0)

theta = delta_calcInverse(robot, x0, y0, z0);

delta_calcForward(robot, theta.q1, theta.q2, theta.q3);


loc = CombVec([-1 0 1],[-1 0 1],[-1 0 1]);

#loc = loc(:,abs(sum(loc))<1);

loc = loc * robot.servo_step;


for i = 1:size(loc,2)

  next_theta.q1 = theta.q1 + loc(1,i);
  next_theta.q2 = theta.q2 + loc(2,i);
  next_theta.q3 = theta.q3 + loc(3,i);

  next_pos(i) = delta_calcForward(robot, next_theta.q1, next_theta.q2, next_theta.q3);
  
  next_pos_vectors(:,i) = [next_pos(i).x; next_pos(i).y; next_pos(i).z];
  
  dpos(i) = sqrt( (next_pos(i).x-x0)^2 + (next_pos(i).y-y0)^2 + (next_pos(i).z-z0)^2 );
  
end

%{
plot3(next_pos_vectors(1,:),next_pos_vectors(2,:),next_pos_vectors(3,:),'r*')
axis([x0-2 x0+2 y0-2 y0+2 z0-2 z0+2])
axis equal
%}


# needs work, not the best metric for resolution.
result = mean(dpos);

end