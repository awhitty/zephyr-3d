import cv2, numpy as np
from matplotlib import pyplot as plt
import math
import argparse as ap


def getCenterPoints(centerPointsName):
	centerPoints = []
	with open(centerPointsName) as f:
		for line in f:
			nums = line.split()
			centerPoints.append((int(float(nums[0])),int(float(nums[1]))))
	return centerPoints
def fillPoint(row,col,image):
	for x in range(-1,1):
		for y in range(-1,1):
			image[row + x][col+y] = 255

def checkRay(point,edgeImage,image,angle):
	xMax = image.shape[0]
	yMax = image.shape[1]
	x = point[0]
	y = point[1]
	x+=math.sin(angle)
	y+=math.cos(angle)
	while x > 0 and x < xMax and y > 0 and y < yMax:
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
	for angle in range(0,360,5):
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
	radialEdges = cv2.GaussianBlur(radialEdges,(7,7),0)

	plt.subplot(121),plt.imshow(img,cmap = 'gray')
	plt.title('Original Image'), plt.xticks([]), plt.yticks([])
	# plt.subplot(122),plt.imshow(edges,cmap = 'gray')
	# plt.title('Blur Image'), plt.xticks([]), plt.yticks([])
	plt.subplot(122),plt.imshow(radialEdges,cmap = 'gray')
	plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

	plt.show()