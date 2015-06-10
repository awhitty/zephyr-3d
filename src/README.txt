A manual of how our computer vision library works, along with documentation of the process.
This will include a step by step walkthrough of running the

	There are 10 python scripts included in the src folder, here we will detail each with how 
to run it as well as documenting design decisions and other information.

This System requires:
Python, Numpy, OpenCV, PIL, TKinter, argparse, MatPlotLib, and scipy


StitchTest.py
	This module is responsible for taking multiple images and combining them into a single image.
This module is responsible for creating a single image that can be used for edge detection of the
entire track at once, since it is not possible to get enough detail from a single aerial image.
The algorithm selects two image files in a specified folder and calculates key feature points 
using either the SURF or SIFT keypoint descriptors. Once these keypoints have been gathered, a 
homography is calculated which can then be used to convert the second image into the image coordinate
system of the first image, creating a new image of the two combined. This process is then repeated
with the merged image and a third image in the folder, and this process is repeated until all the 
images in the specified folder have been merged. 
	The command to run this script in terminal is: 

	python StitchTest.py <Path to Folder> <Name of Race Track> <optional -a SIFT or -a SURF>

This script assumes that the folder that has been specified consists of only jpg images following 
a naming convention <TrackName>1.jpg, <TrackName>2.jpg etc. Also assumes that there is significant 
overlap between image1 and image2, image2 and image3, etc. If there is not enough matching key 
feature points, the script will not produce the correct stitched image, or no image at all.


PickPoints.py
	This module allows you to simulate collection of car coordinates by clicking points on an image.
This was done to bypass the car system and instead move straight to the 3D reconstruction and 
optimization aspects of the project. The points will be stored in the order they are selected.
	The command to run this script in terminal is:

	python PickPoints.py <Image of Track> <Name of Race Track>

Assumes that the image of race track fits on single screen. If you have to scroll, the points will be
messed up, instead the image should be scaled using the SCALE variable in the script.


interpolatePoints.py
	Since we were simulating car coordinates, the points were fairly sparse and there were errors in
picking the points. To solve this problem we wrote this script to interpolate between the points and 
apply a gaussian smoothing algorithm to the points. By doing this we removed most of the noise 
introduced by human error.
	The command to run this script in terminal is:

	python interpolatePoints.py

This assumes that the points consist of an x,y,and z value, and interpolates/smooths all coordinates 
individually. Additionally, assumes that the point file follows the naming convention 
<TrackName>CenterPoints.txt or <TrackName>GPS.txt To change the input file name, change the variables
name and pointsType at the top of the script. This outputs a file of interpolated and smoothed points
and will be named <TrackName>Interpolated<PointsType>.txt


CombineGPS.py
	In order to get the height information (since we simulated car data) we pulled GPS height form the
internet. To combine this with the CenterPoint coordinates, we created this simple script to open a 
file of just the GPS information, the file of the Centerpoints, and outputs a new file of centerpoints
with the proper height associated with them. It assumes the output format of interpolatePoints, that
the files are named <TrackName>CenterPoints.txt or <TrackName>GPS.txt where <TrackName> is specified
by changing the name variable at the top of CombineGPS.py.
	The command to run this script in terminal is:

	python CombineGPS.py

Output will follow the naming convention <TrackName>Interpolated.txt


EdgeFinder.py
	This is the majority of the image processing portion of the project. This script is responsible
for identifying the track and pulling it out of the image to be used through the rest of the pipeline.
To identify the track, we originally used a canny edge detection algorithm, but it was inadequate to
accurately find the edges of the track. To solve this, we created and implemented a new algorithm we
call Radial Edge Detection. Using Center Points and radiating from these points, we can detect the edges
of the track much better than using a linear edge search such as canny edge detection. Once we have found 
these edges in the image, we incorporate the height data from the centerpoints to create a 3D model of 
the race track.
	The command to run this script in terminal is:

	python EdgeFinder.py <Image of Race Track> <Center Points file for Race Track> <Name of Race Track>

This script assumes centerpoints have an X, Y, and Z coordinate, and that the image, center points, 
and name all correspond to the same race track. It outputs an image of the race track all in white 
with a black background called <TrackName>EdgeImage.jpg to be used for calculating the cross sections 
as well as an xyz file named <TrackName>TrackPointsTest.xyz Which is used to make the 3D model for the iOS app.


GetCrossSections.py
	Once we have the 3D model of the race track, we move on to calculating the optimal driving line. To
Do this, we had to convert the image of the race track into a representation that can be used for the 
optimization algorithm. This script breaks down the race track into cross sections that include the center
point, width, angle, and height of the cross section. To do this, the car coordinates are used, and a radial
search is done to find the nearest edge (since the perpendicular bisector of the race track is the closest
point radially). Once this is found, we start a linear search from the same center point in the opposite 
direction to find the corresponding opposite edge, calculate the center point of that cross section, and 
output to a file.
	The command to run this script in terminal is:

	python GetCrossSections.py <Image of Race Track> <Center Points file for Race Track> <Name of Race Track>

This assumes the center points have an X, Y, and Z coordinate, and that the image, center points, and name
all correspond to the same race track. Outputs a file of the cross sections in order called 
<TrackName>CrossSections.txt as well as calling DisplayCrossSections.py as a visual sanity check and 
debugging tool (See DisplayCrossSections.py for more information).


interpolateCrossSections.py
	Identical to interpolatePoints.py except assumes that all cross sections have 5 components,
X midpoint, Y mindpoint, Width, Angle, and Height. (See interpolatePoints.py for more information)
	The command to run this script in terminal is:

	python interpolateCrossSections.py

This script assumes the output of a <TrackName>CrossSections.txt from GetCrossSections.py. Outputs
an interpolated and smoothed list of cross sections named <TrackName>InterpolatedCrossSections.txt


DisplayCrossSections.py
	This script is used mainly as a visual representation midway through the optimization pipeline
for debugging and checking in on the algorithm. Takes in a list of cross sections, center points, and
and image and outputs three images showing the cross sections overlayed on the image, just the cross
sections, and the edges and midpoints of the cross sections respectively. Additionally, this script
plots the edges of the race track in a continuous line resulting in only two lines in a 3D space
that are quick to render and quick to manipulate. This enables visual verification.
	The command to run this script in terminal is:

	python DisplayCrossSections <Image of Race Track> <Cross Sections File> <Center Points File>

This script assumes the previous outputs of Cross Sections and Center Points each have the proper number
of entries, and in the proper order. Outputs three image files: CrossSectionsOverlay.jpg, CrossSections.jpg,
and CrossSectionsSparse.jpg.


CalculateOptimalLine.py
	This script handles the optimization algorithm. After reading in the Cross Sections, this algorithm 
implements an A* heuristic random walk search algorithm to factor in expert knowledge about racing as well
as to avoid getting stuck in any local minima. The objective of this problem is to minimize curvature
of the track since the most time is lost in racing by turning and losing speed, so wider curves mean
faster time even if it also means a slightly farther distance. The algorithm works by calculating a given 
path by deciding what location in the given cross section it will be, with a constraint on not altering 
course too drastically from one cross section to another. Adiitionally, a probabilistic heuristic is used
to calculate the probability of positions in the next Cross Section given the current position. Once a 
position has been chosen for each Cross Section, the curvature is calculated. This is repeated 10,000 times
(tested as sufficient to reach convergence), and the best line is selected, smoothed, and returned. 10,000
iterations took approximately 3 minutes on our machine. 
	The command to run this script in terminal is:

	python CalculateOptimalLine.py <Race Track Image> <Cross Sections File> <Race Track Name>

This Script assumes proper interpolated and smoothed Cross Sections File. The Image is just used
to overlay the best line as a visual result, and is output as <TrackName>BestLine.jpg. Additionally,
This script outputs a file called <TrackName>BestLine.xyz which is the point cloud used to create the 3D
model of the optimal line in the iOS app.


STEPS TO RUN PIPELINE:
1. Put all images to be stitched together in single folder, following naming convention Track1, Track2, etc.
2. Call StitchTest.py to create panorama image
3. Call PickPoints.py on panorama image to get center points (or use car data)
4. Get GPS height information from internet (or use car data)
5. Call interpolatePoints.py on both center points and GPS
6. Call CombineGPS.py to get interpolated and smoothed simulated (or real) car data
7. Call EdgeFinder.py with center points (X,Y,Z) and panorama image
8. Call GetCrossSections.py on EdgeImage and center points (X,Y,Z)
9. Call interpolateCrossSections.py on cross sections
10. Call DisplayCrossSection.py on EdgeImage and interpolated and smoothed cross sections (optional, but used for visual check)
11. Call CalculateOptimalLine.py on CrossSections.jpg (for visual check) and cross sections
12. Use .xyz files to move model into app

If using real car data, you can skip steps 3 and 4, and just call interpolatePoints on just the single list of car coordinates for step 5