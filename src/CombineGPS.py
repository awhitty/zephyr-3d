import numpy as np
from scipy.ndimage import gaussian_filter1d
import math

# Since we don't have car data, we have simulated data from manually picking
# points on an image and getting gps elevation data. This combines the two
# data sets so that they are in one file

f1 = open("SkylineInterpolatedCenterPoints.txt","r")
f2 = open("SkylineInterpolatedGPS.txt","r")
f3 = open("SkylineInterpolated.txt","w")

lines = []

for line in f1:
	vals = line.split()
	lines.append(str(vals[0]) + " " + str(vals[1]) + " ")

lineNum = 0
for line in f2:
	vals = line.split()
	lines[lineNum] += str((float(vals[2]) - 263))
	lineNum += 1

for line in lines:
	f3.write(line+"\n")