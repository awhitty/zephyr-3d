import cv2, numpy as np
import argparse as ap
import math


def displayCrossSections(crossSections, img, name):
	img2 = np.zeros((img.shape[0],img.shape[1],3), np.float32)
	img3 = np.zeros((img.shape[0],img.shape[1],3), np.float32)

	f = open(name,"w")

	for crossSection in crossSections:
		xMid = crossSection[0]
		yMid = crossSection[1]
		dist = crossSection[2]
		angle = crossSection[3]
		if dist < 2: continue
		f.write(str(crossSection[0]) + " " + str(crossSection[1]) + " " + str(crossSection[2]) + " " + str(crossSection[3]) + "\n")
		d = 0
		img3[xMid][yMid] = [255,255,255]
		x1 = 0
		y1 = 0
		x2 = 0
		y2 = 0
		while d < dist/2:
			d += 1
			x1 = xMid + math.sin(angle)*d
			y1 = yMid + math.cos(angle)*d
			x2 = xMid - math.sin(angle)*d
			y2 = yMid - math.cos(angle)*d
			# img2[xMid][yMid] = [255,255,255]
			img2[x1][y1] = [255,0,0]
			img2[x2][y2] = [0,255,0]
			img[x1][y1] = [255,0,0]
			img[x2][y2] = [0,255,0]
		img3[x1][y1] = [255,255,255]
		img3[x2][y2] = [255,255,255]
	cv2.imwrite("centerPoints.jpg",img)
	cv2.imwrite("centerPoints2.jpg",img2)
	cv2.imwrite("centerPoints3.jpg",img3)



if __name__ == "__main__":
	parser = ap.ArgumentParser()
	parser.add_argument('im')
	parser.add_argument('crossSections')
	args = parser.parse_args()

	img = cv2.imread(args.im)

	crossSections = []

	with open(args.crossSections) as f:
		for line in f:
			crossSection = line.split()
			xMid = float(crossSection[0])
			yMid = float(crossSection[1])
			dist = float(crossSection[2])
			angle = float(crossSection[3])
			crossSections.append((xMid,yMid,dist,angle))
	displayCrossSections(crossSections,img,"interpolatedCrossSections1.txt")

