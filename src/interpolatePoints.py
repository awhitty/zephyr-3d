import numpy as np
from scipy.ndimage import gaussian_filter1d

f = open("centerPoints1.txt","r")
xArr = []
yArr = []
zArr = []
for line in f:
	vals = line.split()
	xArr.append(vals[0])
	yArr.append(vals[1])
	zArr.append(vals[2])
t = np.linspace(0,1,len(xArr))
t2 = np.linspace(0,1,1000)

x2 = np.interp(t2,t,xArr)
y2 = np.interp(t2,t,yArr)
z2 = np.interp(t2,t,zArr)

sigma = 10
x3 = gaussian_filter1d(x2, sigma)
y3 = gaussian_filter1d(y2, sigma)
z3 = gaussian_filter1d(z2, sigma)

f2 = open("interpolatedPoints.txt","w")
for index in range(len(x3)):
	output = str(x3[index]) + " " + str(y3[index]) + " " + str(z3[index]) + "\n"
	f2.write(output)