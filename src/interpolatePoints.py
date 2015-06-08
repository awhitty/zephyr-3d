import numpy as np
from scipy.ndimage import gaussian_filter1d
import math

f = open("SkylineCenterPoints.txt","r")
xTempArr = []
yTempArr = []
zTempArr = []
xArr = []
yArr = []
zArr = []
lastAngle = None
for line in f:
	vals = line.split()
	xTempArr.append(float(vals[0]))
	yTempArr.append(float(vals[1]))
	zTempArr.append(float(vals[2]))

t = np.linspace(0,1,len(xTempArr))
t2 = np.linspace(0,1,1000)

xArr = np.interp(t2,t,xTempArr)
yArr = np.interp(t2,t,yTempArr)
zArr = np.interp(t2,t,zTempArr)

# xTempArr = np.interp(t2,t,xTempArr)
# yTempArr = np.interp(t2,t,yTempArr)
# zTempArr = np.interp(t2,t,zTempArr)
# 
# for index in range(-5,len(xTempArr)):
# 	xArr.append(xTempArr[index])
# 	yArr.append(yTempArr[index])
# 	zArr.append(zTempArr[index])
# for index in range(6):
# 	xArr.append(xTempArr[index])
# 	yArr.append(yTempArr[index])
# 	zArr.append(zTempArr[index])

sigma = 5
x3 = gaussian_filter1d(xArr, sigma)
y3 = gaussian_filter1d(yArr, sigma)
z3 = gaussian_filter1d(zArr, sigma)

# x3 = xArr
# y3 = yArr
# z3 = distArr
# w3 = angleArr


f2 = open("SkylineInterpolatedCenterPoints.txt","w")
for index in range(len(x3)):
	output = str(xArr[index]) + " " + str(yArr[index]) + " " + str(z3[index]) + "\n"
	f2.write(output)