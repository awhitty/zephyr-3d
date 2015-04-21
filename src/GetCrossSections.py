import cv2, numpy as np
import argparse as ap
import math
import Queue
from sets import Set

def getCenterPoints(centerPointsName):
	centerPoints = []
	seenPoints = Set()
	with open(centerPointsName) as f:
		for line in f:
			nums = line.split()
			if ((int(float(nums[0])),int(float(nums[1])))) in seenPoints: continue
			centerPoints.append((int(float(nums[0])),int(float(nums[1])),float(nums[2])))
			seenPoints.add(((int(float(nums[0])),int(float(nums[1])))))
			#centerPoints.append((int(float(nums[1])),int(float(nums[0]))))
	return centerPoints

def getNearestEdge(point,img):
	x = point[0]
	y = point[1]
	queue = Queue.Queue()
	for angle in range(360):
		queue.put((math.radians(angle),1))
	while not queue.empty():
		ray = queue.get()
		row = x + math.sin(ray[0])*ray[1]
		col = y + math.cos(ray[0])*ray[1]
		if img[int(row)][int(col)][0] > 10:
			return (int(row),int(col))
		queue.put((ray[0], ray[1]+1))

def getOppositeEdge(point,nearestEdge,img):
	if point[0] == nearestEdge[0]:
		slope = 1
	else: 
		slope = (point[1]-nearestEdge[1])/float(point[0]-nearestEdge[0])
	signX = 1
	signY = 1
	if (point[0]-nearestEdge[0]) < 0: 
		signX = -1
		signY = -1
	if (point[0]-nearestEdge[0]) == 0:
		signX = 0
		if (point[1]-nearestEdge[1]) < 0:
			signY = -1
	x = point[0] + signX
	y = point[1] + slope*signY
	while  x >= 0 and x < img.shape[0] and y >= 0 and y < img.shape[1]:
		if img[int(x)][int(y)][0] > 10:
			return (int(x),int(y),slope)
		x += signX
		y += slope*signY

def getCrossSections(img,centerPoints):
	crossSections = []
	index = -1
	for point in centerPoints:
		index += 1
		print index
		nearestEdge = getNearestEdge(point,img)
		oppositeEdge = getOppositeEdge(point,nearestEdge,img)
		if not oppositeEdge: continue
		midpointX = (nearestEdge[0] + oppositeEdge[0])/2
		midpointY = (nearestEdge[1] + oppositeEdge[1])/2
		img[midpointX][midpointY] = [255,255,255]
		dist = math.sqrt((nearestEdge[0] - oppositeEdge[0])**2 + (nearestEdge[1] - oppositeEdge[1])**2)
		crossSections.append((midpointX,midpointY,dist,oppositeEdge[2]))
	return crossSections

if __name__ == "__main__":
	parser = ap.ArgumentParser()
	parser.add_argument('im')
	parser.add_argument('centerPoints')
	args = parser.parse_args()

	centerPoints = getCenterPoints(args.centerPoints)
	## Load images.
	img = cv2.imread(args.im)
	crossSections = getCrossSections(img,centerPoints)
	cv2.imwrite("centerPoints.jpg",img)
	f = open("crossSections.txt","w")
	for crossSection in crossSections:
		f.write(str(crossSection[0]) + " " + str(crossSection[1]) + " " + str(crossSection[2]) + " " + str(crossSection[3]) + "\n")



