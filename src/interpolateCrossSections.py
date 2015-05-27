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
t = np.linspace(0,1,len(xTempArr))
t2 = np.linspace(0,1,1000)

xTempArr = np.interp(t2,t,xTempArr)
yTempArr = np.interp(t2,t,yTempArr)
distTempArr = np.interp(t2,t,distTempArr)
angleTempArr = np.interp(t2,t,angleTempArr)
heightTempArr = np.interp(t2,t,heightTempArr)


# for index in range(-5,len(xTempArr)):
# 	xArr.append(xTempArr[index])
# 	yArr.append(yTempArr[index])
# 	distArr.append(distTempArr[index])
# 	angleArr.append(angleTempArr[index])
# 	heightArr.append(heightTempArr[index])
# for index in range(6):
# 	xArr.append(xTempArr[index])
# 	yArr.append(yTempArr[index])
# 	distArr.append(distTempArr[index])
# 	angleArr.append(angleTempArr[index])
# 	heightArr.append(heightTempArr[index])

sigma = 2
x3 = gaussian_filter1d(xTempArr, sigma)
y3 = gaussian_filter1d(yTempArr, sigma)
z3 = gaussian_filter1d(distTempArr, sigma)
w3 = gaussian_filter1d(angleTempArr, sigma)
u3 = gaussian_filter1d(heightTempArr, sigma)

# x3 = xArr
# y3 = yArr
# z3 = distArr
# w3 = angleArr


f2 = open("LagunaSecaInterpolatedCrossSections.txt","w")
for index in range(5,len(x3)-5):
	output = str(x3[index]) + " " + str(y3[index]) + " " + str(z3[index]) +  " " + str(w3[index]) + " " + str(u3[index]) + "\n"
	f2.write(output)