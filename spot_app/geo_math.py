import math

# earth_radius = 3960.0  # for miles
earth_radius = 6371.0  # for kms
degrees_to_radians = math.pi/180.0
radians_to_degrees = 180.0/math.pi

def change_in_latitude(distance):
	"Given a distance north, return the change in latitude."
	return (distance/earth_radius)*radians_to_degrees

def change_in_longitude(latitude, distance):
	"Given a latitude and a distance west, return the change in longitude."
	# Find the radius of a circle around the earth at given latitude.
	r = earth_radius*math.cos(latitude*degrees_to_radians)
	return (distance/r)*radians_to_degrees

def bounding_box(latitude, longitude, distance):
	lat_change = change_in_latitude(distance)
	lat_max = latitude + lat_change
	lat_min = latitude - lat_change
	lon_change = change_in_longitude(latitude, distance)
	lon_max = longitude + lon_change
	lon_min = longitude - lon_change
	return (lon_max, lon_min, lat_max, lat_min)