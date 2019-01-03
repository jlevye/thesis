from ij import IJ

def slope(s,t):
	if t[0]-s[0] == 0:
		m = None
	else:
		m = float((t[1]-s[1]))/float((t[0]-s[0]))
	return m

imp = IJ.getImage()
select = imp.getRoi()
s = [select.x1, select.y1]
t = [select.x2, select.y2]

m = slope(s,t)
print m


