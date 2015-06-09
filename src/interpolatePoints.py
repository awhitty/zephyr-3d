import numpy as np
from scipy.ndimage import gaussian_filter1d
import math

circularTrack = False
name = "Skyline"

# This script takes a list of temporally ordered car coordinates and interpolates and smooths these points
f = open(name + "CenterPoints.txt","r")
xTempArr = []
yTempArr = []
zTempArr = []
xArr = []
yArr = []
zArr = []
lastAngle = None
# read in coordinates
for line in f:
	vals = line.split()
	xTempArr.append(float(vals[0]))
	yTempArr.append(float(vals[1]))
	zTempArr.append(float(vals[2]))

t = np.linspace(0,1,len(xTempArr))
t2 = np.linspace(0,1,1000)

# If circular track, pad beginning and end to ensure the track meets at the transition
if circularTrack:
	xTempArr = np.interp(t2,t,xTempArr)
	yTempArr = np.interp(t2,t,yTempArr)
	zTempArr = np.interp(t2,t,zTempArr)

	for index in range(-5,len(xTempArr)):
		xArr.append(xTempArr[index])
		yArr.append(yTempArr[index])
		zArr.append(zTempArr[index])
	for index in range(6):
		xArr.append(xTempArr[index])
		yArr.append(yTempArr[index])
		zArr.append(zTempArr[index])
else:
	xArr = np.interp(t2,t,xTempArr)
	yArr = np.interp(t2,t,yTempArr)
	zArr = np.interp(t2,t,zTempArr)

# Use gaussian smoothing on all values
sigma = 5
x3 = gaussian_filter1d(xArr, sigma)
y3 = gaussian_filter1d(yArr, sigma)
z3 = gaussian_filter1d(zArr, sigma)


f2 = open(name + "InterpolatedCenterPoints.txt","w")
nums = range(len(x3))

# get rid of added padding if circular track
if circularTrack:
	nums = range(5,len(x3)-5)
for index in nums:
	output = str(xArr[index]) + " " + str(yArr[index]) + " " + str(z3[index]) + "\n"
	f2.write(output)