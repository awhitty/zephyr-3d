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
		self.includedPixels = Set()
		self.xMax = self.image.shape[0]
		self.yMax = self.image.shape[1]
		for row in range(self.xMax):
			for col in range(self.yMax):
				if self.image[int(row)][int(col)] > 10:
					self.edgePixels.add((row,col))

	def isValid(self,row,col):
		for x in range(-11,11):
			for y in range(-11,11):
				if (row + x, col + y) in self.includedPixels: 
					return False
		return (row,col) in self.edgePixels

	def createEdgeSets(self):
		edges = self.edgePixels.copy()
		while len(edges) > 0:
			pixel = edges.pop()
			if self.isValid(pixel[0],pixel[1]): 
				self.edgeSets.append(self.getEdgeSet(edges,pixel))

	def isValid(self,row,col):
		for x in range(-11,11):
			for y in range(-11,11):
				if (row + x, col + y) in self.includedPixels: 
					return False
		return (row,col) in self.edgePixels

	def getEdgeSetWithoutOverlap(self,edges,pixel):
		edgePixels = []
		row = pixel[0]
		col = pixel[1]
		edgePixels.append(pixel)
		exhaustedSearch = False
		direction = 0
		while not exhaustedSearch:
			leftDir = direction + 90
			leftX = row + round(math.cos(math.radians(leftDir)))
			leftY = col + round(math.sin(math.radians(leftDir)))
			if not self.isValid(leftX,leftY):
				exhaustedSearch = True
				for angle in range(-45,135,45):
					newDir = direction - angle
					newX = row + round(math.cos(math.radians(newDir)))
					newY = col + round(math.sin(math.radians(newDir)))
					if self.isValid(newX,newY):
						direction = newDir
						row = newX
						col = newY
						self.edgePixels.discard((row,col))
						edgePixels.append((row,col))
						exhaustedSearch = False
						break
			else:
				frontDir = direction
				frontX = row + round(math.cos(math.radians(frontDir)))
				frontY = col + round(math.sin(math.radians(frontDir)))
				if self.isValid(frontX,frontY):
					row = frontX
					col = frontY
				else:
					direction -= 45

		for pixel in edgePixels:
			self.includedPixels.add(pixel)
		return edgePixels

	def getEdgeSet(self,edges,pixel):
		edgePixels = []
		row = pixel[0]
		row = min(row, self.image.shape[0]-2)
		row = max(row,1)
		col = pixel[1]
		col = min(col, self.image.shape[1]-2)
		col = max(col,1)
		edgePixels.append(pixel)
		exhaustedSearch = False
		direction = 0
		while not exhaustedSearch and row < self.image.shape[0]-1 and col < self.image.shape[1]-1:
			if self.image[row-1][col-1] > 1 and (row-1,col-1) in self.edgePixels:
				row -= 1
				col -= 1
				self.edgePixels.discard((row,col))
				edgePixels.append((row,col))
			elif self.image[row-1][col] > 1 and (row-1,col) in self.edgePixels:
				row -= 1
				self.edgePixels.discard((row,col))
				edgePixels.append((row,col))
			elif self.image[row-1][col+1] > 1 and (row-1,col+1) in self.edgePixels:
				row -= 1
				col += 1
				self.edgePixels.discard((row,col))
				edgePixels.append((row,col))
			elif self.image[row][col+1] > 1 and (row,col+1) in self.edgePixels:
				col += 1
				self.edgePixels.discard((row,col))
				edgePixels.append((row,col))
			elif self.image[row+1][col+1] > 1 and (row+1,col+1) in self.edgePixels:
				row += 1
				col += 1
				self.edgePixels.discard((row,col))
				edgePixels.append((row,col))
			elif self.image[row+1][col] > 1 and (row+1,col) in self.edgePixels:
				row += 1
				self.edgePixels.discard((row,col))
				edgePixels.append((row,col))
			elif self.image[row+1][col-1] > 1 and (row+1,col-1) in self.edgePixels:
				row += 1
				col -= 1
				self.edgePixels.discard((row,col))
				edgePixels.append((row,col))
			elif self.image[row][col-1] > 1 and (row,col-1) in self.edgePixels:
				col -= 1
				self.edgePixels.discard((row,col))
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