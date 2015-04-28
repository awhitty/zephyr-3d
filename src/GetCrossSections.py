import cv2, numpy as np
import argparse as ap
import math
import Queue
from sets import Set

currentAngle = 0

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
	global currentAngle
	queue = Queue.Queue()
	for angle in range(360):
		queue.put((math.radians(currentAngle + angle),0.1))
	while not queue.empty():
		ray = queue.get()
		row = x + math.sin(ray[0])*ray[1]
		col = y + math.cos(ray[0])*ray[1]
		if img[int(row)][int(col)][0] > 10:
			currentAngle = ray[0]
			return (int(row),int(col),ray[0])
		queue.put((ray[0], ray[1]+0.1))

def getOppositeEdge(point,nearestEdge,img):
	(x,y,angle) = nearestEdge
	x = point[0]
	y = point[1]
	angle += math.radians(180)
	dist = 1
	x += math.sin(angle)*dist
	y += math.cos(angle)*dist
	while x >= 0 and x < img.shape[0] and y >= 0 and y < img.shape[1]:
		if img[int(x)][int(y)][0] > 10:
			return (int(x),int(y),angle)
		x += math.sin(angle)*dist
		y += math.cos(angle)*dist
	# if point[0] == nearestEdge[0]:
	# 	slope = 1
	# else: 
	# 	slope = (point[1]-nearestEdge[1])/float(point[0]-nearestEdge[0])
	# signX = 1
	# signY = 1
	# if (point[0]-nearestEdge[0]) < 0: 
	# 	signX = -1
	# 	signY = -1
	# if (point[0]-nearestEdge[0]) == 0:
	# 	signX = 0
	# 	if (point[1]-nearestEdge[1]) < 0:
	# 		signY = -1
	# x = point[0] + signX
	# y = point[1] + slope*signY
	# while  x >= 0 and x < img.shape[0] and y >= 0 and y < img.shape[1]:
	# 	if img[int(x)][int(y)][0] > 10:
	# 		return (int(x),int(y),slope)
	# 	x += signX
	# 	y += slope*signY

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
		#img[midpointX][midpointY] = [255,255,255]
		dist = math.sqrt((nearestEdge[0] - oppositeEdge[0])**2 + (nearestEdge[1] - oppositeEdge[1])**2)
		crossSections.append((midpointX,midpointY,dist,oppositeEdge[2]))
	return crossSections

if __name__ == "__main__":
	parser = ap.ArgumentParser()
	parser.add_argument('im')
	parser.add_argument('centerPoints')
	args = parser.parse_args()

	img = cv2.imread(args.im)
	img2 = np.zeros((img.shape[0],img.shape[1],3), np.float32)
	img3 = np.zeros((img.shape[0],img.shape[1],3), np.float32)

	centerPoints = getCenterPoints(args.centerPoints)
	## Load images.
	crossSections = getCrossSections(img,centerPoints)
	f = open("crossSections.txt","w")
	# h,w = img.shape
	# vis2 = cv2.CreateMat(h, w, cv2.CV_32FC3)
	# vis0 = cv2.fromarray(img2)
	# cv2.CvtColor(vis0, vis2, cv2.CV_GRAY2BGR)

	for crossSection in crossSections:
		xMid = crossSection[0]
		yMid = crossSection[1]
		dist = crossSection[2]
		angle = crossSection[3]
		if dist < 2: continue
		f.write(str(crossSection[0]) + " " + str(crossSection[1]) + " " + str(crossSection[2]) + " " + str(crossSection[3]) + "\n")
		d = 0
		img3[xMid][yMid] = [255,255,255]
		x1 = 0
		y1 = 0
		x2 = 0
		y2 = 0
		while d < dist/2:
			d += 1
			x1 = xMid + math.sin(angle)*d
			y1 = yMid + math.cos(angle)*d
			x2 = xMid - math.sin(angle)*d
			y2 = yMid - math.cos(angle)*d
			# img2[xMid][yMid] = [255,255,255]
			img2[x1][y1] = [255,255,255]
			img2[x2][y2] = [255,255,255]
		img3[x1][y1] = [255,255,255]
		img3[x2][y2] = [255,255,255]
	cv2.imwrite("centerPoints1.jpg",img)
	cv2.imwrite("centerPoints2.jpg",img2)
	cv2.imwrite("centerPoints3.jpg",img3)





