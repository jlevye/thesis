import os, csv
import string
from ij import IJ
from ij.plugin.frame import RoiManager

#Get the current image & the filename to save data as
imp = IJ.getImage()
filename = imp.title
im_name = filename.split(".")[0]
path = os.getcwd()

#Get the overlay for the current image
overlay = imp.getOverlay()
rois = RoiManager(True)

#Make sure that any current ROIs have been added to the overlay we'll work with
if rois.getCount() > 0: 
	for roi in rois:
		overlay.add(roi)


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
		width.append(roi.getStrokeWidth()
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