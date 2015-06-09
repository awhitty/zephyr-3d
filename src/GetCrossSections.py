import cv2, numpy as np
import argparse as ap
import math
import Queue
from sets import Set
import DisplayCrossSections

currentAngle = 0
name = ''

# Given a filename consisting of a list of center points, read them and store them in a list
def getCenterPoints(centerPointsName):
	centerPoints = []
	seenPoints = Set()
	with open(centerPointsName) as f:
		for line in f:
			nums = line.split()
			x = int(float(nums[1]))
			y = int(float(nums[0])) 
			if ((x,y)) in seenPoints: continue
			centerPoints.append((x,y,float(nums[2])))
			seenPoints.add(((x,y)))
	return centerPoints

# Given a center point, searches for the nearest edge in the edge image by expanding radially 
# with an ever increasing radius
def getNearestEdge(point,img):
	x = point[0]
	y = point[1]
	global currentAngle
	queue = Queue.Queue()
	for angle in range(360):
		queue.put((math.radians(currentAngle + angle),0.1))
	while not queue.empty():
		ray = queue.get()
		row = x + math.sin(ray[0])*ray[1]
		col = y + math.cos(ray[0])*ray[1]
		if row >= 0 and row < img.shape[0] and col >= 0 and col < img.shape[1]:
			if img[int(row)][int(col)][0] < 10:
				currentAngle = ray[0]
				return (int(row),int(col),ray[0])
			queue.put((ray[0], ray[1]+0.1))

# Normalizes angle to be between -pi and +pi
def normalizeAngle(angle):
	while angle >= 2*math.pi:
		angle -= 2*math.pi
	return angle

# Given a center point and the nearest edge to that point, search linearly
# in the opposite direction until it finds the corresponding edge on the 
# other side of the track.
def getOppositeEdge(point,nearestEdge,img):
	(x,y,angle) = nearestEdge
	x = point[0]
	y = point[1]
	angle += math.radians(180)
	dist = .5
	x += math.sin(angle)*dist
	y += math.cos(angle)*dist
	while x >= 0 and x < img.shape[0] and y >= 0 and y < img.shape[1]:
		if img[int(x)][int(y)][0] < 10:
			return (int(x),int(y),normalizeAngle(angle))
		x += math.sin(angle)*dist
		y += math.cos(angle)*dist

# Given a list of center points in an image of edges, for each point finds
# the nearest edge and the corresponding opposite edge. Stores a cross crossSection
# as the coordinates of the midpoint of the cross section, the length (dist) of the 
# cross section, the angle of the cross section, and the height of the cross section
# in that order. Returns a list of cross sections
def getCrossSections(img,centerPoints):
	crossSections = []
	index = -1
	previousDist = None
	for point in centerPoints:
		index += 1
		print index
		nearestEdge = getNearestEdge(point,img)
		if not nearestEdge: continue
		oppositeEdge = getOppositeEdge(point,nearestEdge,img)
		if not oppositeEdge: continue
		midpointX = (nearestEdge[0] + oppositeEdge[0])/2
		midpointY = (nearestEdge[1] + oppositeEdge[1])/2
		#img[midpointX][midpointY] = [255,255,255]
		dist = math.sqrt((nearestEdge[0] - oppositeEdge[0])**2 + (nearestEdge[1] - oppositeEdge[1])**2)
		if previousDist != None and dist > 1.5*previousDist: continue
		previousDist = dist
		crossSections.append((midpointX,midpointY,dist,oppositeEdge[2], point[2]))
	return crossSections
	
# This script is called to translate an edge image in which the track is filled in white
# into cross section representation which our algorithm uses to calculate the optimal line
if __name__ == "__main__":
	parser = ap.ArgumentParser()
	parser.add_argument('im')
	parser.add_argument('centerPoints')
	parser.add_argument('name')

	args = parser.parse_args()

	global name
	name = args.name
	img = cv2.imread(args.im)

	centerPoints = getCenterPoints(args.centerPoints)
	## Load images.
	crossSections = getCrossSections(img,centerPoints)

	DisplayCrossSections.displayCrossSections(crossSections,img,name + "CrossSections.txt")





