import cv2, numpy as np
from matplotlib import pyplot as plt
import math
import argparse as ap
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from sets import Set

class TrackEdges():
	def __init__(self,edgeImage):
		self.image = edgeImage
		self.edgeSets = []
		self.edgePixels = Set()
		self.xMax = self.image.shape[0]
		self.yMax = self.image.shape[1]
		for row in range(self.xMax):
			for col in range(self.yMax):
				if self.image[int(row)][int(col)] > 10:
					self.edgePixels.add((row,col))

	def createEdgeSets(self):
		edges = self.edgePixels.copy()
		while len(edges) > 0:
			pixel = edges.pop()
			self.edgeSets.append(self.getEdgeSet(edges,pixel))

	def getEdgeSet(self,edges,pixel):
		edgePixels = []
		row = pixel[0]
		col = pixel[1]
		edgePixels.append(pixel)
		exhaustedSearch = False
		while not exhaustedSearch:
			if self.image[row-1][col-1] > 10 and (row-1,col-1) in edges:
				row -= 1
				col -= 1
				edges.discard((row,col))
				edgePixels.append((row,col))
			elif self.image[row-1][col] > 10 and (row-1,col) in edges:
				row -= 1
				edges.discard((row,col))
				edgePixels.append((row,col))
			elif self.image[row-1][col+1] > 10 and (row-1,col+1) in edges:
				row -= 1
				col += 1
				edges.discard((row,col))
				edgePixels.append((row,col))
			elif self.image[row][col-1] > 10 and (row,col-1) in edges:
				col -= 1
				edges.discard((row,col))
				edgePixels.append((row,col))
			elif self.image[row][col+1] > 10 and (row,col+1) in edges:
				col += 1
				edges.discard((row,col))
				edgePixels.append((row,col))
			elif self.image[row+1][col-1] > 10 and (row+1,col-1) in edges:
				row += 1
				col -= 1
				edges.discard((row,col))
				edgePixels.append((row,col))
			elif self.image[row+1][col] > 10 and (row+1,col) in edges:
				row += 1
				edges.discard((row,col))
				edgePixels.append((row,col))
			elif self.image[row+1][col+1] > 10 and (row+1,col+1) in edges:
				row += 1
				col += 1
				edges.discard((row,col))
				edgePixels.append((row,col))
			else: exhaustedSearch = True
		return edgePixels

	def orderEdgePixels(self):
		# edges
		# self.edgeSets = sorted(self.edgeSets, key=lambda edges: len(edges), reverse=True)
		# pairSet = Set()
		# firstPixel = self.egeSets[0][0]
		return self.edgeSets


	def distance(pixel1,pixel2):
		return math.sqrt((pixel1[0]-pixel2[0])**2 + (pixel1[1] - pixel2[1])**2)