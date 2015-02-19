import cv2, numpy as np
from matplotlib import pyplot as plt
import math
import argparse as ap

if __name__ == "__main__":
	parser = ap.ArgumentParser()
	parser.add_argument('im')

	args = parser.parse_args()
	## Load images.
	img = cv2.imread(args.im)
	blur = cv2.GaussianBlur(img,(3,3),0)
	edges = cv2.Canny(img,150,150)
	edgesBlur = cv2.GaussianBlur(edges,(1,1),0)
	edges = cv2.Canny(edgesBlur,50,150)
	edges = cv2.GaussianBlur(edges,(9,9),0)

	plt.subplot(121),plt.imshow(edgesBlur,cmap = 'gray')
	plt.title('Original Image'), plt.xticks([]), plt.yticks([])
	plt.subplot(122),plt.imshow(edges,cmap = 'gray')
	plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

	plt.show()