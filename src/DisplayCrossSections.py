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
import EdgeFinder


xArr1 = []
yArr1 = []
zArr1 = []
xArr2 = []
yArr2 = []
zArr2 = []

# Since height is not scaled in picture, this is used to translate height in meters to height in voxels
HEIGHT_SCALE = 1.04

# Used mainly for debugging, this function superimposes the cross sections over the image they are taken from,
# prints out just the cross sections over a black background, and prints our the edges and center points
def displayCrossSections(crossSections, img, name):
	img2 = np.zeros((img.shape[0],img.shape[1],3), np.float32)
	img3 = np.zeros((img.shape[0],img.shape[1],3), np.float32)

	f = open(name,"w")

	for crossSection in crossSections:
		xMid = crossSection[0]
		yMid = crossSection[1]
		dist = crossSection[2]
		angle = crossSection[3]
		if dist < 2: continue
		f.write(str(crossSection[0]) + " " + str(crossSection[1]) + " " + str(crossSection[2]) + " " + str(crossSection[3]) + " " + str(crossSection[4]) + "\n")
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
			img2[x1][y1] = [255,0,0]
			img2[x2][y2] = [0,255,0]
			img[x1][y1] = [255,0,0]
			img[x2][y2] = [0,255,0]
		img3[x1][y1] = [255,255,255]
		img3[x2][y2] = [255,255,255]
		xArr1.append(x1)
		xArr2.append(x2)
		yArr1.append(y1)
		yArr2.append(y2)
	cv2.imwrite("CrossSectionsOverlay.jpg",img)
	cv2.imwrite("CrossSections.jpg",img2)
	cv2.imwrite("CrossSectionsSparse.jpg",img3)

# Plots a 3d representation of the track based on the cross section edges. This is a very sparse model
# that only includes two lines, one for each edge of the track, so it renders very quickly and is easily 
# interacted with
def plotTrack(crossSections,centerPoints):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	for index in range(len(xArr1)):
		zArr1.append(EdgeFinder.getHeight(xArr1[index],yArr1[index],centerPoints)*HEIGHT_SCALE)
		zArr2.append(EdgeFinder.getHeight(xArr2[index],yArr2[index],centerPoints)*HEIGHT_SCALE)	
	t = np.linspace(0, 1, len(zArr1))
	t2 = np.linspace(0, 1, len(zArr1))

	x12 = np.interp(t2, t, xArr1)
	y12 = np.interp(t2, t, yArr1)
	z12 = np.interp(t2, t, zArr1)
	x22 = np.interp(t2, t, xArr2)
	y22 = np.interp(t2, t, yArr2)
	z22 = np.interp(t2, t, zArr2)
	sigma = 2
	x13 = gaussian_filter1d(x12, sigma)
	y13 = gaussian_filter1d(y12, sigma)
	z13 = gaussian_filter1d(z12, sigma)
	x23 = gaussian_filter1d(x22, sigma)
	y23 = gaussian_filter1d(y22, sigma)
	z23 = gaussian_filter1d(z22, sigma)
	ax.plot(z13,y13,x13,color = 'b')
	ax.plot(z23,y23,x23,color = 'b')
	plt.show()

# This entire script is used mainly for debugging and visualizing the cross sections to make
# that everything is as it should be. Outputs multiple images as visual representation
if __name__ == "__main__":
	parser = ap.ArgumentParser()
	parser.add_argument('im')
	parser.add_argument('crossSections')
	parser.add_argument('centerPoints')
	args = parser.parse_args()

	centerPoints = EdgeFinder.getCenterPoints(args.centerPoints)
	img = cv2.imread(args.im)

	crossSections = []

	with open(args.crossSections) as f:
		for line in f:
			crossSection = line.split()
			xMid = float(crossSection[0])
			yMid = float(crossSection[1])
			dist = float(crossSection[2])
			angle = float(crossSection[3])
			height = float(crossSection[4])
			crossSections.append((xMid,yMid,dist,angle,height))
	displayCrossSections(crossSections,img,"interpolatedCrossSections1.txt")
	plotTrack(crossSections,centerPoints)


