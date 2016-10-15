'''
Created on 2016. 5. 30.

@author: jongyeob
'''
from swpy.dataproc import data

#distance seoul to daejeon
seoul_coord = (126.9779692,37.566535)
daejeon_coord = (127.3845475,36.3504119)

radius_earth = 6371 #km
unit_distance = data.great_circle_distance(seoul_coord,daejeon_coord)

distance_seoul_to_daejeon = radius_earth * unit_distance
print "Distance Seoul to Daejeon [km] : ", distance_seoul_to_daejeon 


idw = data.IDWEstimator()

test_loc = [(10,20),(30,40),(15,20),(10,5)]
test_data = [ 1, 2, 3, 4 ]

idw.load(test_loc,test_data)

select_data = idw.select((10,20)) # Zero division
print "Interpolated data (zero division) : ",select_data

select_data = idw.select((10,21))
print "Interpolated data : ",select_data

