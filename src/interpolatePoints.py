import numpy as np
from scipy.ndimage import gaussian_filter1d
import math

f1 = open("LagunaSecaInterpolatedCenterPoints.txt","r")
f2 = open("LagunaSecaInterpolatedGPS.txt","r")
f3 = open("LagunaSecaInterpolated.txt","w")

lines = []

for line in f1:
	vals = line.split()
	lines.append(str(vals[0]) + " " + str(vals[1]) + " ")

lineNum = 0
for line in f2:
	vals = line.split()
	lines[lineNum] += str((float(vals[2]) - 220))
	lineNum += 1

for line in lines:
	f3.write(line+"\n")

# f = open("LagunaSecaGPS.txt","r")
# xTempArr = []
# yTempArr = []
# zTempArr = []
# xArr = []
# yArr = []
# zArr = []
# lastAngle = None
# for line in f:
# 	vals = line.split()
# 	xTempArr.append(float(vals[0]))
# 	yTempArr.append(float(vals[1]))
# 	zTempArr.append(float(vals[2]))

# t = np.linspace(0,1,len(xTempArr))
# t2 = np.linspace(0,1,1000)

# xTempArr = np.interp(t2,t,xTempArr)
# yTempArr = np.interp(t2,t,yTempArr)
# zTempArr = np.interp(t2,t,zTempArr)

# for index in range(-5,len(xTempArr)):
# 	xArr.append(xTempArr[index])
# 	yArr.append(yTempArr[index])
# 	zArr.append(zTempArr[index])
# for index in range(6):
# 	xArr.append(xTempArr[index])
# 	yArr.append(yTempArr[index])
# 	zArr.append(zTempArr[index])

# sigma = 5
# x3 = gaussian_filter1d(xArr, sigma)
# y3 = gaussian_filter1d(yArr, sigma)
# z3 = gaussian_filter1d(zArr, sigma)

# # x3 = xArr
# # y3 = yArr
# # z3 = distArr
# # w3 = angleArr


# f2 = open("LagunaSecaInterpolatedGPS.txt","w")
# for index in range(5,len(x3)-5):
# 	output = str(x3[index]) + " " + str(y3[index]) + " " + str(z3[index]) + "\n"
# 	f2.write(output)