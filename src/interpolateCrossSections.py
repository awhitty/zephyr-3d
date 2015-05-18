import numpy as np
from scipy.ndimage import gaussian_filter1d
import math

def modifyAngle(lastAngle, angle):
	angleOptions = []
	for coeff in range(-3,3):
		angleOptions.append(coeff*math.pi)
	modifiedAngle = angle + sorted(angleOptions, key=lambda angleMod: abs(lastAngle - (angle + angleMod)))[0]
	return modifiedAngle

f = open("crossSectionsFinal.txt","r")
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
		# if shouldSwitch(lastAngle,angle):
		# 	print "switched1"
		# 	angle = (angle + math.pi)%(2*math.pi)
		# elif abs(lastAngle - angle - math.pi) < abs(lastAngle - angle):
		# 	print "switched2"
		# 	angle += math.pi
	lastAngle = angle
	xArr.append(float(vals[0]))
	yArr.append(float(vals[1]))
	distArr.append(float(vals[2]))
	angleArr.append(angle)
	heightArr.append(float(vals[4]))
t = np.linspace(0,1,len(xArr))
t2 = np.linspace(0,1,1000)

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


f2 = open("interpolatedCrossSections.txt","w")
for index in range(len(x3)):
	output = str(x3[index]) + " " + str(y3[index]) + " " + str(z3[index]) +  " " + str(w3[index]) + " " + str(u3[index]) + "\n"
	f2.write(output)