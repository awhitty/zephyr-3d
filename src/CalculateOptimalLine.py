import cv2, numpy as np
from numpy.random import choice
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

MAX_ITERS = 1000

def calculateCurvature(linePoints):
	curvatureSum = 0
	for index in range(len(linePoints)-2):
		x = linePoints[index]
		y = linePoints[index+1]
		z = linePoints[index+2]
		xy = [x[0] - y[0], x[1] - y[1]]
		zy = [z[0] - y[0], z[1] - y[1]]
		xz = [x[0] - z[0], x[1] - z[1]]
		distXY = math.sqrt(xy[0]**2 + xy[1]**2)
		distZY = math.sqrt(zy[0]**2 + zy[1]**2)
		distXZ = math.sqrt(xz[0]**2 + xz[1]**2)
		xy[0] /= distXY
		xy[1] /= distXY
		zy[0] /= distZY
		zy[1] /= distZY
		angle = math.acos(xy[0]*zy[0] + xy[1]*zy[1])
		curvatureSum += 2*math.sin(angle)/distXZ
	return curvatureSum

def displayLine(line,im):
	for point in line:
		im[int(point[0])][int(point[1])][0] = 0
		im[int(point[0])][int(point[1])][1] = 0
		im[int(point[0])][int(point[1])][2] = 0
	cv2.imwrite("bestLine.jpg",im)


def calculateOptimal(crossSections,im):
	bestLine = []
	bestCurvature = float("inf")
	locationChange = [-0.1,0,0.1]
	for iteration in range(MAX_ITERS):
		line = []
		loc = 0
		for crossSection in crossSections:
			weights = [.3,.4,.3]
			loc += choice(locationChange,p=weights)
			loc = min(loc,.5*crossSection[2])
			loc = max(loc,-.5*crossSection[2])
			angle = crossSection[3]
			x = crossSection[0] + math.sin(angle)*loc
			y = crossSection[1] + math.cos(angle)*dist
			line.append((x,y))
		curvature = calculateCurvature(line)
		if curvature < bestCurvature:
			bestLine = line
			bestCurvature = curvature
	print bestCurvature
	displayLine(bestLine,im)



if __name__ == "__main__":
	parser = ap.ArgumentParser()
	parser.add_argument('im')
	parser.add_argument('crossSections')
	args = parser.parse_args()

	img = cv2.imread(args.im)
	crossSections = []

	with open(args.crossSections) as f:
		for line in f:
			crossSection = line.split()
			xMid = float(crossSection[0])
			yMid = float(crossSection[1])
			dist = float(crossSection[2])
			angle = float(crossSection[3])
			crossSections.append((xMid,yMid,dist,angle))
	calculateOptimal(crossSections,img)
