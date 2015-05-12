import numpy as np
from scipy.ndimage import gaussian_filter1d
import math

f1 = open("ArastraderoInterpolatedCenterPoints.txt","r")
f2 = open("ArastraderoInterpolatedGPS.txt","r")
f3 = open("ArastraderoInterpolated.txt","w")

lines = []

for line in f1:
	vals = line.split()
	lines.append(str(vals[0]) + " " + str(vals[1]) + " ")

lineNum = 0
for line in f2:
	vals = line.split()
	lines[lineNum] += str((float(vals[2]) - 93.4562888001)/4)
	lineNum += 1

for line in lines:
	f3.write(line+"\n")

# f = open("ArastraderoCenterPoints1.txt","r")
# xArr = []
# yArr = []
# zArr = []
# lastAngle = None
# for line in f:
# 	vals = line.split()
# 	xArr.append(float(vals[0]))
# 	yArr.append(float(vals[1]))
# 	zArr.append(float(vals[2]))
# t = np.linspace(0,1,len(xArr))
# t2 = np.linspace(0,1,1000)

# x2 = np.interp(t2,t,xArr)
# y2 = np.interp(t2,t,yArr)
# z2 = np.interp(t2,t,zArr)

# sigma = 2
# x3 = gaussian_filter1d(x2, sigma)
# y3 = gaussian_filter1d(y2, sigma)
# z3 = gaussian_filter1d(z2, sigma)

# # x3 = xArr
# # y3 = yArr
# # z3 = distArr
# # w3 = angleArr


# f2 = open("ArastraderoInterpolatedCenterPoints.txt","w")
# for index in range(len(x3)):
# 	output = str(x3[index]) + " " + str(y3[index]) + " " + str(z3[index]) + "\n"
# 	f2.write(output)