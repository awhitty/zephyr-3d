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



if __name__ == "__main__":
	parser = ap.ArgumentParser()
	parser.add_argument('im')
	parser.add_argument('crossSections')
	args = parser.parse_args()

	crossSections = []

	with open(args.crossSections) as f:
		for line in f:
			crossSection = line.split()
			xMid = float(crossSection[0])
			yMid = float(crossSection[1])
			dist = float(crossSection[2])
			angle = float(crossSection[3])
			crossSections.append((xMid,yMid,dist,angle))
	curvatureSum = calculateCurvature(crossSections)
	print curvatureSum
