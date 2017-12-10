def rotatePoint(centerPoint,point,angle): 
"""Rotates a point around another centerPoint. Angle is in degrees. Rotation is counter-clockwise""" 
angle = math.radians(angle) 
temp_point = point[0]-centerPoint[0] , point[1]-centerPoint[1] 
temp_point = ( temp_point[0]*math.cos(angle)-temp_point[1]*math.sin(angle) , temp_point[0]*math.sin(angle)+temp_point[1]*math.cos(angle)) 
temp_point = temp_point[0]+centerPoint[0] , temp_point[1]+centerPoint[1] 
return temp_point 
