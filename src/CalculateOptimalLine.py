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

MAX_ITERS = 1
LAST_TURN = 0
EPSILON = 0.0
HEIGHT_SCALE = 5
name = ''

XYZPoints = []

def fillPoint(row,col,height,image):
	global XYZPoints
	for x in range(-2,3):
		for y in range(-2,3):
			XYZPoints.append((row+x,col+y,height))
			image[row + x][col+y][0] = 255
			image[row + x][col+y][1] = 255
			image[row + x][col+y][2] = 255

def calculateCurvature(linePoints):
	curvatureSum = 0
	lastChange = 1
	currentChange = 1
	lastAngle = 0
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
		if math.sin(angle) != 0:
			lastChange = currentChange
			currentChange = 1
			curvatureSum += 2*math.sin(angle)**2/(distXZ*(lastChange + currentChange))
		else:
			currentChange += 1
	return curvatureSum

def writeXYZ():
	f = open(name + 'BestLine.xyz', 'w')
	for point in XYZPoints:
		f.write(str(point[0]) + " "+ str(point[1]) + " " + str(point[2])+"\n")

def displayLine(line,im):
	for point in line:
		fillPoint(int(point[0]),int(point[1]),point[2],im)
		# im[int(point[0])][int(point[1])][0] = 0
		# im[int(point[0])][int(point[1])][1] = 0
		# im[int(point[0])][int(point[1])][2] = 0
	writeXYZ()
	cv2.imwrite(name + "BestLine.jpg",im)

def inTurn(angles):
	isInRightTurn = True
	for index in range(1,len(angles)):
		if angles[index] >= angles[index-1] - EPSILON: isInRightTurn = False
	isInLeftTurn = True
	for index in range(1,len(angles)):
		if angles[index] <= angles[index-1] + EPSILON: isInLeftTurn = False
	if isInRightTurn: return -1
	if isInLeftTurn: return 1
	return 0

def calculateWeights(crossSections,index,position):
	if index < 10 or index > len(crossSections)-11:
		return [.2,.6,.2]
	angles = []
	for delta in range(-10,11):
		angles.append(crossSections[index + delta][3])
	firstChange = inTurn(angles[0:10])#angles[3] - angles[0]
	secondChange = inTurn(angles[11:20])#angles[8] - angles[5]
	global LAST_TURN
	if inTurn(angles) != 0: LAST_TURN = position
	if firstChange > 0:
		if secondChange > 0:
			return [.2,.2,.6]
		elif secondChange < 0:
			return [.6,.2,.2]
		else:
			return [.6,.2,.2]
	elif firstChange < 0:
		if secondChange > 0:
			return [.2,.2,.6]
		elif secondChange < 0:
			return [.6,.2,.2]
		else:
			return [.2,.2,.6]
	else:
		if secondChange > 0:
			return [.2,.2,.6]
		elif secondChange < 0:
			return [.6,.2,.2]
		# elif LAST_TURN > 0:
		# 	return [.2,.2,.6]
		# elif LAST_TURN < 0:
		# 	return [.6,.2,.2]
		else:
			return [.2,.6,.2]

def calculateTestWeights(crossSections,index,position):
	if index < 10 or index > len(crossSections)-11:
		return [.2,.6,.2]
	angles = []
	for delta in range(-10,11):
		angles.append(crossSections[index + delta][3])
	firstChange = inTurn(angles[0:10])#angles[3] - angles[0]
	secondChange = inTurn(angles[11:20])#angles[8] - angles[5]
	global LAST_TURN
	if inTurn(angles) != 0: LAST_TURN = position
	if firstChange > 0:
		if secondChange > 0:
			return [0,0,1]
		elif secondChange < 0:
			return [1,0,0]
		else:
			return [1,0,0]
	elif firstChange < 0:
		if secondChange > 0:
			return [0,0,1]
		elif secondChange < 0:
			return [1,0,0]
		else:
			return [0,0,1]
	else:
		if secondChange > 0:
			return [0,0,1]
		elif secondChange < 0:
			return [1,0,0]
		# elif LAST_TURN > 0:
		# 	return [0,0,1]
		# elif LAST_TURN < 0:
		# 	return [1,0,0]
		else:
			return [0,1,0]


def smoothLine(line):
	bestLineX = []
	bestLineY = []
	bestLineZ = []
	for point in line:
		bestLineX.append(point[0])
		bestLineY.append(point[1])
		bestLineZ.append(point[2])
	sigma = 4
	x2 = gaussian_filter1d(bestLineX, sigma)
	y2 = gaussian_filter1d(bestLineY, sigma)
	z2 = bestLineZ#gaussian_filter1d(bestLineZ, sigma)
	smoothLine = []
	for index in range(len(x2)):
		smoothLine.append((x2[index],y2[index],z2[index]))
	return smoothLine

def calculateOptimal(crossSections,im):
	bestLine = []
	bestCurvature = float("inf")
	locationChange = [-1,0,1]
	for iteration in range(MAX_ITERS):
		# print iteration
		global LAST_TURN 
		LAST_TURN = 0
		line = []
		loc = 0#.5*crossSections[0][2]
		index = -1
		for crossSection in crossSections:
			index += 1
			weights = calculateTestWeights(crossSections,index,loc)
			loc += choice(locationChange,p=weights)
			loc = min(loc,.5*crossSection[2]-1)
			loc = max(loc,-.5*crossSection[2]+1)
			angle = crossSection[3]
			x = crossSection[0] + math.sin(angle)*loc
			y = crossSection[1] + math.cos(angle)*loc
			z = crossSection[4]*HEIGHT_SCALE
			line.append((x,y,z))
		curvature = calculateCurvature(line)
		if curvature < bestCurvature:
			bestLine = line
			bestCurvature = curvature
	print bestCurvature
	bestLine = smoothLine(bestLine)
	displayLine(bestLine,im)



if __name__ == "__main__":
	parser = ap.ArgumentParser()
	parser.add_argument('im')
	parser.add_argument('crossSections')
	parser.add_argument('name')
	args = parser.parse_args()

	img = cv2.imread(args.im)
	global name
	name = args.name
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
	calculateOptimal(crossSections,img)
