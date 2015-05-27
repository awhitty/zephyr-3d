import numpy as np
from scipy.ndimage import gaussian_filter1d
import math

def modifyAngle(lastAngle, angle):
	angleOptions = []
	for coeff in range(-3,3):
		angleOptions.append(coeff*math.pi)
	modifiedAngle = angle + sorted(angleOptions, key=lambda angleMod: abs(lastAngle - (angle + angleMod)))[0]
	return modifiedAngle

f = open("LagunaSecaCrossSections.txt","r")
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
for index in range(-5,len(xTempArr)):
	xArr.append(xTempArr[index])
	yArr.append(yTempArr[index])
	distArr.append(distTempArr[index])
	angleArr.append(angleTempArr[index])
	heightArr.append(heightTempArr[index])
for index in range(6)):
	xArr.append(xTempArr[index])
	yArr.append(yTempArr[index])
	distArr.append(distTempArr[index])
	angleArr.append(angleTempArr[index])
	heightArr.append(heightTempArr[index])
t = np.linspace(0,1,len(xArr))
t2 = np.linspace(0,1,1010)

x2 = np.interp(t2,t,xArr)
y2 = np.interp(t2,t,yArr)
z2 = np.interp(t2,t,distArr)
w2 = np.interp(t2,t,angleArr)
u2 = np.interp(t2,t,heightArr)

sigma = 2
x3 = gaussian_filter1d(x2, sigma)
y3 = gaussian_filter1d(y2, sigma)
z3 = gaussian_filter1d(z2, sigma)
w3 = gaussian_filter1d(w2, sigma)
u3 = gaussian_filter1d(u2, sigma)

# x3 = xArr
# y3 = yArr
# z3 = distArr
# w3 = angleArr


f2 = open("LagunaSecaInterpolatedCrossSections.txt","w")
for index in range(5,len(x3)-5):
	output = str(x3[index]) + " " + str(y3[index]) + " " + str(z3[index]) +  " " + str(w3[index]) + " " + str(u3[index]) + "\n"
	f2.write(output)