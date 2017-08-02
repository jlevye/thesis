import os, csv, sys
import string
from ij import IJ
from ij.plugin.frame import RoiManager
from ij.gui import GenericDialog

#grab the default path, just in case
path = os.getcwd()

#Assumes that export_helper is found in the correct jar/libs folder
#just in case:
sys.path.append("/home/jen/Documents/School/GradSchool/Thesis/Code")
from export_helper import *

#Get the current image & the filename to save data as
imp = IJ.getImage()
filename = imp.title
im_name = filename.split(".")[0]

#Get the overlay for the current image, if there is one
#Make the overlay if there isn't, so we can fill it from the ROI manager
overlay = imp.getOverlay()
if overlay is None:
	overlay = ij.gui.Overlay()
	imp.setOverlay(overlay)

#Get the ROI manager and if it has things in it, add them to the overlay
ROIM = RoiManager()
if ROIM.getCount() > 0:
	rois = ROIM.getRoisAsArray() 
	for roi in rois:
		overlay.add(roi)

#Setting up parameters

#@int(label="Segment length cut-off",value=0) min_length 
#@int(label="Intersection threshold",value=1) thresh 

#Process with corrections for intersection
rangeEnd = overlay.size()
lines = []

for index in range(rangeEnd):
	roi = overlay.get(index)
	if roi.isLine():
		s = [roi.x1, roi.y1]
		t = [roi.x2, roi.y2]
		length = roi.getLength()
		width = roi.getStrokeWidth()
		newLine = LineSegment(s,t)
		newLine.length = length
		newLine.width = width
		lines.append(newLine)
		m = slope(s, t)
		b = intercept(s, m)

fullSegments = []

for line in lines:
	crosses = [l for l in lines if l is not line]
	newSegments = findSplits(line, crosses, thresh)
	for seg in newSegments:
		if seg.length > min_length:
			fullSegments.append(seg)

#print len(fullSegments)

newLayer = ij.gui.Overlay()

for line in fullSegments:
	toDraw = ij.gui.Line(line.s[0],line.s[1],line.t[0],line.t[1])
	toDraw.setStrokeWidth(line.width)
	toDraw.setStrokeColor(Color(0,255,0))
	newLayer.add(toDraw)

imp.setOverlay(newLayer)
newLayer.setLabelColor(Color(0,0,0))
newLayer.drawLabels(True)
imp.updateImage()

confirm = GenericDialog("Confirmation")
confirm.addMessage("Save revised ROIs and export data?")
confirm.showDialog()

if confirm.wasCanceled():
	confirmOK = False
elif confirm.wasOKed():
	confirmOK = True

#Only finish if OK is confirmed
if confirmOK:
	#So as to not have to re-write script later, change variable names
	overlay = newLayer

	#From each ROI get information needed, set up to work with analysis script
	x1 = []
	x2 = []
	y1 = []
	y2 = []
	width = []
	length = []

	for i in range(overlay.size()):
		roi = overlay.get(i)
		if roi.isLine():
			width.append(roi.getStrokeWidth())
			length.append(roi.getLength())
			x1.append(roi.x1)
			x2.append(roi.x2)
			y1.append(roi.y1)
			y2.append(roi.y2)
	
		
	##Get all the measurements etc needed
	#m = overlay.measure(imp)

	#array = overlay.toArray()
	#line_width = [roi.getStrokeWidth() for roi in array]

	#angle = m.getColumn(m.getColumnIndex("Angle"))

	#x = m.getColumn(m.getColumnIndex("BX"))
	#y = m.getColumn(m.getColumnIndex("BY"))
	#width = m.getColumn(m.getColumnIndex("Width"))
	#height = m.getColumn(m.getColumnIndex("Height"))
	#length = m.getColumn(m.getColumnIndex("Length"))

	#Write to file
	dataFileName = string.join([im_name, "csv"], ".")
	fullWriteFile = os.path.join(path, dataFileName)

	f = open(fullWriteFile, "wb")
	writer = csv.writer(f)
	#names = ["X","Y","Angle","Width","Height","LineWidth","Length"]
	names = ["x1","x2","y1","y2","Width","Length"]
	writer.writerow(names)

	for  i in range(len(x)):
		#row = [x[i], y[i], angle[i], width[i], height[i], line_width[i],length[i]]
		row = [x1[i], x2[i], y1[i], y2[i], width[i], length[i]]
		writer.writerow(row)

	f.close()
else:
	#Put the original overlay back
	imp.setOverlay(overlay)
	imp.updateImage()
	