import cv2, numpy as np
from matplotlib import pyplot as plt
import math
import argparse as ap
from scipy.ndimage import gaussian_filter1d
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import TrackEdges
from sets import Set

xPoints = []
yPoints = []
zPoints = []

def getCenterPoints(centerPointsName):
	centerPoints = []
	seenPoints = Set()
	with open(centerPointsName) as f:
		for line in f:
			nums = line.split()
			x = int(float(nums[0]))
			y = int(float(nums[1])) 
			if ((x,y)) in seenPoints: continue
			centerPoints.append((x,y,float(nums[2])))
			seenPoints.add(((x,y)))
			#centerPoints.append((y,x))
	return centerPoints

def getHeight(x,y,centerPoints):
	minDist = float("inf")
	secondDist = float("inf")
	minHeight = 0
	secondHeight = 0
	for point in centerPoints:
		dist = math.sqrt((point[0]-x)**2 + (point[1]-y)**2)
		if dist < minDist:
			secondDist = minDist
			secondHeight = minHeight
			minHeight = point[2]
			minDist = dist
		elif dist < secondDist:
			secondHeight = point[2]
			secondDist = dist
	height = secondHeight*(1  - (1/(1 + (minDist/secondDist)**4))) + minHeight*(1/(1 + (minDist/secondDist)**4))
	return minHeight

def createOrdered3D(centerPoints,edgeSets):
	f = open('ArastraderoTrackPointsTest.xyz', 'w')
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	for edgeSet in edgeSets:
		xArr = []
		yArr = []
		zArr = []
		for point in edgeSet:
			xArr.append(point[0])
			yArr.append(point[1])
			height = getHeight(point[0],point[1],centerPoints)
			zArr.append(height)
			f.write(str(point[0]) + " "+ str(point[1]) + " " + str(height*10)+"\n")
		t = np.linspace(0, 1, len(zArr))
		t2 = np.linspace(0, 1, len(zArr))

		x2 = np.interp(t2, t, xArr)
		y2 = np.interp(t2, t, yArr)
		z2 = np.interp(t2, t, zArr)
		sigma = 10
		x3 = gaussian_filter1d(x2, sigma)
		y3 = gaussian_filter1d(y2, sigma)
		z3 = gaussian_filter1d(z2, sigma)
		ax.plot(xArr,yArr,zArr,color = 'b')
	plt.show()

def createScatter3D(centerPoints,edgeSets):
	f = open('ArastraderoTrackPointsTest.xyz', 'w')
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	for edgeSet in edgeSets:
		xArr = []
		yArr = []
		zArr = []
		for point in edgeSet:
			xArr.append(point[0])
			yArr.append(point[1])
			height = getHeight(point[0],point[1],centerPoints)
			zArr.append(height)
			f.write(str(point[0]) + " "+ str(point[1]) + " " + str(height*10)+"\n")
		ax.scatter(xArr,yArr,zArr,color = 'b')
	plt.show()


def create3D(centerPoints):
	for index in range(len(xPoints)):
		zPoints.append(getHeight(xPoints[index],yPoints[index],centerPoints))
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.scatter(xPoints,yPoints,zPoints)
	for index in range(len(xPoints)):
		x = xPoints[index]
		y = yPoints[index]
		z = zPoints[index]
		ax.plot([x,x],[y,y],[z,0], color = 'b')

	plt.show()

def fillPoint(row,col,image):
	row = min(row,image.shape[0]-6)
	col = min(col,image.shape[1]-6)
	xPoints.append(row)
	yPoints.append(col)
	image[row][col] = 255
	for x in range(-1,2):
		for y in range(-1,2):
			image[row + x][col+y] = 255

def checkRay(point,edgeImage,image,angle):
	xMax = image.shape[0]
	yMax = image.shape[1]
	x = point[0]
	y = point[1]
	x+=math.sin(angle)
	y+=math.cos(angle)
	while x > 0 and x < xMax and y > 0 and y < yMax:
		#fillPoint(int(x),int(y),edgeImage)
		if image[int(x)][int(y)] > 10:
			fillPoint(int(x),int(y),edgeImage)
			return
		x+=math.sin(angle)
		y+=math.cos(angle)

def radialEdgeDetection(point,edgeImage,image):
	# check0(point,edgeImage,image)
	# check45(point,edgeImage,image)
	# check90(point,edgeImage,image)
	# check135(point,edgeImage,image)
	# check180(point,edgeImage,image)
	# check225(point,edgeImage,image)
	# check270(point,edgeImage,image)
	# check315(point,edgeImage,image)
	for angle in range(0,360,1):
		checkRay(point,edgeImage,image,math.radians(angle))

def getEdges(image, centerPoints):
	edgeImage = np.zeros(image.shape)
	for point in centerPoints:
		radialEdgeDetection(point,edgeImage,image)
		# fillPoint(point[0],point[1],image)
	return edgeImage


if __name__ == "__main__":
	parser = ap.ArgumentParser()
	parser.add_argument('im')
	parser.add_argument('centerPoints')

	args = parser.parse_args()
	centerPoints = getCenterPoints(args.centerPoints)
	## Load images.
	img = cv2.imread(args.im)
	blur = cv2.GaussianBlur(img,(3,3),0)
	edges = cv2.Canny(blur,150,150)
	edges = cv2.Canny(edges,200,200)
	edges = cv2.GaussianBlur(edges,(5,5),0)
	radialEdges = getEdges(edges,centerPoints)
	radialEdges = cv2.GaussianBlur(radialEdges,(3,3),0)
	for row in range(radialEdges.shape[0]):
		for col in range(radialEdges.shape[1]):
			if radialEdges[row][col] > 1: radialEdges[row][col] = 255
	#radialEdges = cv2.GaussianBlur(radialEdges,(5,5),0)
	cv2.imwrite("ArastraderoEdgeImage.jpg",radialEdges)

	plt.subplot(121),plt.imshow(img,cmap = 'gray')
	plt.title('Original Image'), plt.xticks([]), plt.yticks([])
	# # plt.subplot(122),plt.imshow(edges,cmap = 'gray')
	# # plt.title('Blur Image'), plt.xticks([]), plt.yticks([])
	plt.subplot(122),plt.imshow(radialEdges,cmap = 'gray')
	plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

	plt.show()
	trackEdges = TrackEdges.TrackEdges(radialEdges)
	trackEdges.createEdgeSets()
	edgeSets = trackEdges.orderEdgePixels()
	createScatter3D(centerPoints,edgeSets)
	#createOrdered3D(centerPoints,edgeSets)