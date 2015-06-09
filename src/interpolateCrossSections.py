import numpy as np
from scipy.ndimage import gaussian_filter1d
import math

name = "Skyline"
circularTrack = False

# In order to recognize that angle 0 is actually the same as angle 360, the angle may have
# to be modified so that interpolating can be applied on a cyclical scale. This function
# adds and subtracts multiples of pi to find the most probable angle that results in the
# least smoothing necessary
def modifyAngle(lastAngle, angle):
	angleOptions = []
	for coeff in range(-3,3):
		angleOptions.append(coeff*math.pi)
	modifiedAngle = angle + sorted(angleOptions, key=lambda angleMod: abs(lastAngle - (angle + angleMod)))[0]
	return modifiedAngle

# This script takes a list of ordered cross sections and interpolates and smooths the values
f = open(name + "CrossSections.txt","r")
xTempArr = []
yTempArr = []
distTempArr = []
angleTempArr = []
heightTempArr = []
xArr = []
yArr = []
distArr = []
angleArr = []
heightArr = []
lastAngle = None
# read in values
for line in f:
	vals = line.split()
	angle = float(vals[3])
	if lastAngle != None:
		angle = modifyAngle(lastAngle,angle)
	lastAngle = angle
	xTempArr.append(float(vals[0]))
	yTempArr.append(float(vals[1]))
	distTempArr.append(float(vals[2]))
	angleTempArr.append(angle)
	heightTempArr.append(float(vals[4]))
t = np.linspace(0,1,len(xTempArr))
t2 = np.linspace(0,1,1000)

# interpolate
xTempArr = np.interp(t2,t,xTempArr)
yTempArr = np.interp(t2,t,yTempArr)
distTempArr = np.interp(t2,t,distTempArr)
angleTempArr = np.interp(t2,t,angleTempArr)
heightTempArr = np.interp(t2,t,heightTempArr)

# if circular track use padding to ensure both ends meet
if circularTrack:
	for index in range(-5,len(xTempArr)):
		xArr.append(xTempArr[index])
		yArr.append(yTempArr[index])
		distArr.append(distTempArr[index])
		angleArr.append(angleTempArr[index])
		heightArr.append(heightTempArr[index])
	for index in range(6):
		xArr.append(xTempArr[index])
		yArr.append(yTempArr[index])
		distArr.append(distTempArr[index])
		angleArr.append(angleTempArr[index])
		heightArr.append(heightTempArr[index])
else:
	xArr = xTempArr
	yArr = yTempArr 
	distArr = distTempArr 
	angleArr = angleTempArr 
	heightArr = heightTempArr 

# smooth values
sigma = 2
x3 = gaussian_filter1d(xArr, sigma)
y3 = gaussian_filter1d(yArr, sigma)
z3 = gaussian_filter1d(distArr, sigma)
w3 = gaussian_filter1d(angleArr, sigma)
u3 = gaussian_filter1d(heightArr, sigma)


f2 = open(name + "InterpolatedCrossSections.txt","w")
nums = range(len(x3))
# if circular remove added padding
if circularTrack:
	nums = range(5,len(x3)-5)
for index in nums:
	output = str(x3[index]) + " " + str(y3[index]) + " " + str(z3[index]) +  " " + str(w3[index]) + " " + str(u3[index]) + "\n"
	f2.write(output)