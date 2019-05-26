import xml.etree.ElementTree as ET
import csv

# This code is not built to be failsafe if the input svg doesn't look like this example.
test_xml1 = """<?xml version="1.0" encoding="UTF-8"?>
<svg>   
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   width="420mm"
   height="297mm"
   viewBox="0 0 420 297"
   version="1.1"
   id="SVGRoot"
   inkscape:version="0.92.3 (2405546, 2018-03-11)"
   sodipodi:namedviewid="base"
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1.0"
     inkscape:pageopacity="0.0"
     inkscape:pageshadow="2"
     inkscape:zoom="1.979899"
     inkscape:cx="294.6746"
     inkscape:cy="916.53433"
     inkscape:document-units="mm"
     inkscape:current-layer="layer1"
     showgrid="false"
     inkscape:window-width="1920"
     inkscape:window-height="1009"
     inkscape:window-x="0"
     inkscape:window-y="34"
     inkscape:window-maximized="1"
    <g>
    <path
       style="fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:0.60854167;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
       d="M 39.530739,103.09394 39.389104,100.8705"
       id="path1484-2-9-5" />
    <path
       style="fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:0.39687499;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
       d="m 41.457449,35.668198 1.10522,-0.89766"
       id="path1588-0-9"
     />
    <path
       style="fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:0.39687499;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
       d="m 21.883309,48.352038 -1.06908,-0.93545"
       id="path1598-96-6"
    />
     </g>
   </svg>
"""

# massaged structure; ET doesn't seem to like some of the attributes in the root elements? Not sure. 
test_xml2 = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg>
  <g>
      <path
       style="opacity:1;fill:none;fill-opacity:1;stroke:#4cff3c;stroke-width:1.25;stroke-linecap:butt;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1"
       d="m 84.335936,65.773064 -5.338913,8.031993"
       id="path919"/>
    <path
       style="opacity:1;fill:none;fill-opacity:1;stroke:#4cff3c;stroke-width:0.15000001;stroke-linecap:butt;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1"
       d="m 98.604537,237.92941 -0.05906,0.0591 -0.165364,0.22443 -1.051248,0.48428 -1.133927,0.30711"
       id="path921"/>
    <path
       style="opacity:1;fill:none;fill-opacity:1;stroke:#4cff3c;stroke-width:0.2;stroke-linecap:butt;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1"
       d="m 90.478051,238.04752 1.145738,0.51972 1.417413,0.33073 1.393785,0.17717 0.968565,0.0827 0.791385,-0.1535"
       id="path923"/>
    <path
       style="opacity:1;fill:none;fill-opacity:1;stroke:#4cff3c;stroke-width:0.2;stroke-linecap:butt;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1"
       d="m 86.225818,234.48037 1.086681,1.19299 0.850447,0.81501 1.133928,0.87407 1.181177,0.68508"
       id="path925"/>
    <path
       style="opacity:1;fill:none;fill-opacity:1;stroke:#4cff3c;stroke-width:0.25;stroke-linecap:butt;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1"
       d="m 82.552362,226.77911 0.389786,1.50009 0.850448,2.16155 0.980377,1.73633 0.68508,1.26386 0.767765,1.03943"
       id="path927"/>
 </g>
</svg>
"""

root1 = ET.fromstring(test_xml2)
output = []   # Each command becomes a row of x & y pts in this list
oddballs = [] # List to save weird commands
movetos = []  # Input lines

# Find the attributes we want and save into a list
for x in root1.findall('g'):
   for path in x.findall('path'):  

        # Get 'width' data by turning 'style' attribute into a dict
        # This code chunk is overlong from testing, should fix.
        #style = path.attrib['style']
        #print style
        slist = (path.attrib['style']).split(";")
        tlist = []
        for s in slist:
            t = s.split(":")
            tlist.append(t)
        tdict = dict(tlist)
        
		# Combine extracted parts of path element into a line 
		# which is suitable for csv export:
        width = tdict['stroke-width']
        attrib1 = path.attrib['d']
        attrib2 = path.attrib['id']
        ldict = {'width': width, 'd': attrib1, 'id': attrib2}
        #print(ldict)
        movetos.append(ldict)

#for m in movetos:
#   print(m)                   

# Input: a list of dicts, each containing data from one path element
# Output: a list of lists where each index is in format: [x1, y1, x2, y2, width]
def process_movetos(movetos):
    o = []
    error_out = []
    is_error = False
    for path in movetos:		
        row = [] # Start a new csv export row

        # Process command element:
        dsplit = path['d'].split(" ")
        print(dsplit)
        for d in dsplit: # test for command characters
            check = check_element(d)
            if check == "error":
                error_out.append(d)
                # how to break out of inner loop?
            elif check == 
			elif check == "coordinates":
                coords = d.split(",") # need to error handle this
                x_coord = float(coords[0])
                y_coord = float(coords[1])

# def check_element_type()
#     input: an element of a d attribute
#     output: type of that element, either one of a list of command characters or a coordinate pair
def check_element_type(d):
    is_error = False
    if (len(d) == 1) and (d != "0"):
        if d == "m": pass #normal/relative mode, move on
        elif d == "M": pass #absolute mode
        elif d == "v":
            is_error = True
        elif d == "0": pass #weird numbers
        else:
            is_error = True
    elif (len(d) > 1):
            
            


    for m in movetos:
        pass
        row = [] # Start a new csv export row
        command = m['d']

        # Testing stuff:
        #for c in command.items():
         #  print(c)
           # Check that dictionary is correctly formed here
		# Any fail states to catch go here:
        if len(command) != 100:  
            pass
	        #oddballs.append(m)
        else:		
            # Get length of command string:
            command_len = len(command)

            # Get first endpoint:
            e1 = command[1].split(",")
            x1 = float(e1[0])
            y1 = float(e1[1])
            row = [x1,y1]
            print("Endpoint 1: (" + str(x1) + "," + str(y1) + ")")
        
            # Get 2nd set of coordinates:
            e2 = command[2].split(",")
            x2 = float(e2[0])
            y2 = float(e2[1])
        
            # Test command character:
            if command[0] == 'M':
                print("Endpoint 2: (" + str(x2) + "," + str(y2) + ")")
                row = row + [x2,y2,w]
                o.append(row)
        
            elif command[0] == 'm': # 2nd point is a relative, implicit 'lineto' command
                x3 = x1 + x2
                y3 = y1 + y2
                print("Move: (" + str(x2) + "," + str(y2) +")")
                print("Endpoint 2: (" + str(x3) + "," + str(y3) + ")")
            
                row = row + [x3,y3,w]
                o.append(row)

            else: # I don't know what this is
                #oddballs.append(command)
                print("Oddball: command")

    return o

# Run process and create output list:            
output = process_movetos(movetos)
#print
#for o in output:
#    print o     

############################################
# following is processing code when movetos did not contain dicts:
def process_movetos_old(movetos):
    o = []
    for m in movetos:
        row = []                # Start a new csv export row
        command = m
        # Testing stuff:

   
		# Any fail states to catch go here:
        if len(command) != 100:  
            pass
	        #oddballs.append(command)
            #print("Oddball: length")
        else:
            # Get the width value:
            w = float(command[3])
        
            # Get first endpoint:
            e1 = command[1].split(",")
            x1 = float(e1[0])
            y1 = float(e1[1])
            row = [x1,y1]
            print("Endpoint 1: (" + str(x1) + "," + str(y1) + ")")
        
            # Get 2nd set of coordinates:
            e2 = command[2].split(",")
            x2 = float(e2[0])
            y2 = float(e2[1])
        
            # Test command character:
            if command[0] == 'M':
                print("Endpoint 2: (" + str(x2) + "," + str(y2) + ")")
                row = row + [x2,y2,w]
                o.append(row)
        
            elif command[0] == 'm': # 2nd point is a relative, implicit 'lineto' command
                x3 = x1 + x2
                y3 = y1 + y2
                print("Move: (" + str(x2) + "," + str(y2) +")")
                print("Endpoint 2: (" + str(x3) + "," + str(y3) + ")")
            
                row = row + [x3,y3,w]
                o.append(row)

            else: # I don't know what this is
                #oddballs.append(command)
                print("Oddball: command")

    return o
    
##########################################
# Process command element:
        char1 = dsplit.pop(0)
        if char1 = "m":
            mode = "rel"
        elif char1 == "M":
            mode = "abs"
        else: #if ((char1 != "m") and (char1 != "M"))
            is_error = True
    
   
