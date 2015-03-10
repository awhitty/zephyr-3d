import cv2, numpy as np
from matplotlib import pyplot as plt
import math
import argparse as ap

xMax = 0
yMax = 0

def getCenterPoints():
	centerPoints = []
	with open("centerPoints.txt") as f:
		for line in f:
			nums = line.split()
			centerPoints.append((int(float(nums[0])),int(float(nums[1]))))
	return centerPoints
def fillPoint(row,col,image):
	for x in range(-1,1):
		for y in range(-1,1):
			image[row + x][col+y] = 255

def check0(point,edgeImage,image):
	x = point[0]
	y = point[1]
	while y < yMax:
		y+=1
		if image[x][y] > 1:
			fillPoint(x,y,edgeImage)
			return

def check45(point,edgeImage,image):
	x = point[0]
	y = point[1]
	while x > 0 and y < yMax:
		x-=1
		y+=1
		if image[x][y] > 1:
			fillPoint(x,y,edgeImage)
			return

def check90(point,edgeImage,image):
	x = point[0]
	y = point[1]
	while x > 0:
		x-=1
		if image[x][y] > 1:
			fillPoint(x,y,edgeImage)
			return

def check135(point,edgeImage,image):
	x = point[0]
	y = point[1]
	while x > 0 and y > 0:
		x-=1
		y-=1
		if image[x][y] > 1:
			fillPoint(x,y,edgeImage)
			return

def check180(point,edgeImage,image):
	x = point[0]
	y = point[1]
	while y > 0:
		y-=1
		if image[x][y] > 1:
			fillPoint(x,y,edgeImage)
			return

def check225(point,edgeImage,image):
	x = point[0]
	y = point[1]
	while x < xMax and y > 0:
		x+=1
		y-=1
		if image[x][y] > 1:
			fillPoint(x,y,edgeImage)
			return

def check270(point,edgeImage,image):
	x = point[0]
	y = point[1]
	while x < xMax:
		x+=1
		if image[x][y] > 1:
			fillPoint(x,y,edgeImage)
			return

def check315(point,edgeImage,image):
	x = point[0]
	y = point[1]
	while x < xMax and y < yMax:
		x+=1
		y+=1
		if image[x][y] > 1:
			fillPoint(x,y,edgeImage)
			return


def radialEdgeDetection(point,edgeImage,image):
	check0(point,edgeImage,image)
	check45(point,edgeImage,image)
	check90(point,edgeImage,image)
	check135(point,edgeImage,image)
	check180(point,edgeImage,image)
	check225(point,edgeImage,image)
	check270(point,edgeImage,image)
	check315(point,edgeImage,image)

def getEdges(image, centerPoints):
	xMax = image.shape[0]
	yMax = image.shape[1]
	edgeImage = np.zeros(image.shape)
	for point in centerPoints:
		radialEdgeDetection(point,edgeImage,image)
		fillPoint(point[0],point[1],image)
	return edgeImage


if __name__ == "__main__":
	parser = ap.ArgumentParser()
	parser.add_argument('im')

	args = parser.parse_args()
	centerPoints = getCenterPoints()
	## Load images.
	img = cv2.imread(args.im)
	blur = cv2.GaussianBlur(img,(3,3),0)
	edges = cv2.Canny(img,150,150)
	edgesBlur = cv2.GaussianBlur(edges,(1,1),0)
	edges = cv2.Canny(edgesBlur,50,150)
	edges = cv2.GaussianBlur(edges,(9,9),0)
	radialEdges = getEdges(edges,centerPoints)

	plt.subplot(121),plt.imshow(edges,cmap = 'gray')
	plt.title('Original Image'), plt.xticks([]), plt.yticks([])
	plt.subplot(122),plt.imshow(radialEdges,cmap = 'gray')
	plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

	plt.show()