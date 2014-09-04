# This software is copyright 2014 by NU Solar
# Written September 1, 2014, Alexander Martin

import math, svgwrite, sys, getopt

# usage
usage = "box_maker.py [-h|-? (help)] [-i (dimensions are inner dimensions)] [-n|--notch_ratio= <notch-length-to-side-length ratio>] [-r (make a top for the box)] [-u (specify units)] x_depth y_depth vertical_depth material_thickness output_file"

# Side Letters (Left, Right, Fore, Aft, Top, Bottom)
L, R, F, A, T, B = range(6)


# notch offsets[horizontal|vertical][male|female][point#]
offsets = [ \
			[ \
				[ (-1,0),(-1,0),(0,0),(0,0),(-1,0),(-1,0) ], \
				[ (0,0),(0,0),(-1,0),(-1,0),(0,0),(0,0) ]  \
			], \
			[  \
				[ (0,-1),(0,-1),(0,0),(0,0),(0,-1),(0,-1) ], \
				[ (0,0),(0,0),(0,-1),(0,-1),(0,0),(0,0) ]  \
			] ]

offsets_outer = [ \
			[ \
				[ (0,0),(0,0),(1,0),(1,0),(0,0),(0,0) ], \
				[ (1,0),(1,0),(0,0),(0,0),(1,0),(1,0) ]  \
			], \
			[  \
				[ (0,0),(0,0),(0,1),(0,1),(0,0),(0,0) ], \
				[ (0,1),(0,1),(0,0),(0,0),(0,1),(0,1) ]  \
			] ]

# pixel-to-cm ratio
utp = {'px':1, 'cm':35.43307, 'mm':3.543307, 'in':90}

def main(argv=None):
	if argv == None:
		argv = sys.argv

	try:
		opts, argv = getopt.getopt(argv[1:],'h?in:ru:',['notch_ratio=','units=','help','inside_dim','roof'])
	except getopt.GetoptError as err:
		print str(err)
		print usage
		sys.exit(2)

	# Default config variables ######################################
	m_xdepth 	 = 10.0 											#
	m_ydepth 	 = 10.0 											#
	m_zdepth 	 = 5.0 												#
	m_thickness  = 0.2   											#
	m_notchratio = 1.0/3.0 											#
	make_roof	 = False 											#
	output		 = "box.svg" 										#
	units		 = 'cm'												#
	#################################################################

	# parse arguments
	try:
		m_xdepth 	= float(argv[0])
		m_ydepth 	= float(argv[1])
		m_zdepth 	= float(argv[2])
		m_thickness = float(argv[3])
		output   	= argv[4]
	except:
		print "Error parsing box dimensions. Check your arguments."
		print usage
		sys.exit(2)

	for opt, arg in opts:
		if opt in ('-h','-?','--help'):
			print "This program generates box layouts for Northwestern's Solar Car Team, NU Solar.\nThese layouts can be printed on any material cutter supporting svg vector input.\nAll inputs are currently in centimeters."
			print usage
			sys.exit(2)
			m_thickness = int(arg)
		elif opt in ('-n','--notch_ratio'):
			m_notchratio = int(arg)
		elif opt in ('-r','--roof'):
			make_roof = True
		elif opt in ('-u','--units'):
			units = arg
			if (units not in utp):
				print "Units not found in preset definitions."
				ratio = input("Provide ", arg, "-to-px ratio?\n-")
				utp[arg] = int(ratio)
		elif ('-i','--inside_dim') in opts: # if the dimensions given are inner dimensions, increase depths by the thickness of the material
			m_xdepth += m_thickness
			m_ydepth += m_thickness
			m_zdepth += m_thickness

	# adjust dimensions to be pixel dimensions
	m_xdepth_p 	  = utp[units]*m_xdepth
	m_ydepth_p 	  = utp[units]*m_ydepth
	m_zdepth_p 	  = utp[units]*m_zdepth
	m_thickness_p = utp[units]*m_thickness

	# make sides
	Side_base  =  boxSide(m_xdepth_p, m_ydepth_p, B, m_thickness_p, m_notchratio, [0, 0, 0, 0])
	Side_left  =  boxSide(m_ydepth_p, m_zdepth_p, L, m_thickness_p, m_notchratio, [1, 0, 1, 1])
	Side_right =  boxSide(m_ydepth_p, m_zdepth_p, R, m_thickness_p, m_notchratio, [1, 0, 1, 1])

	Side_fore  =  boxSide(m_xdepth_p, m_zdepth_p, F, m_thickness_p, m_notchratio, [0, 0, 0, 1])
	Side_aft   =  boxSide(m_xdepth_p, m_zdepth_p, A, m_thickness_p, m_notchratio, [0, 0, 0, 1])

	sides = [Side_base,Side_left,Side_right,Side_fore,Side_aft]

	if make_roof == True:
		Side_top = box_side(m_xdepth_p, m_ydepth_p, T, m_thickness_p, m_notchratio, [1, 1, 1, 1])
		sides.append(Side_top)

	# create svg drawing
	dwg_size = (str(max(m_xdepth+2*m_zdepth,2*m_xdepth)) + units, str(max(m_ydepth + 2*m_zdepth,2*m_ydepth)) + units)
	print "Drawing Size: ", dwg_size
	dwg = svgwrite.Drawing(filename = output,size=dwg_size)

	# add boxes to drawing
	for s in sides:
		box = dwg.polygon(points = [tuple(point) for point in s.points], fill = "none", stroke = "black", stroke_width = "0.01cm")
		dwg.add(box)
		s.SVG_object = box

	# transform boxes to preset positions (possibly add dynamic positioning later)
	Side_fore.SVG_object.translate(0,m_ydepth_p)
	Side_aft.SVG_object.translate (0,m_ydepth_p+m_zdepth_p)
	Side_left.SVG_object.rotate(-90,(m_ydepth_p,0))
	Side_left.SVG_object.translate(0,m_xdepth_p-m_ydepth_p)
	Side_right.SVG_object.rotate(-90,(m_ydepth_p,0))
	Side_right.SVG_object.translate(0,m_xdepth_p-m_ydepth_p+m_zdepth_p)
	if make_roof == True:
		Side_top.SVG_object.translate(m_xdepth_p,m_ydepth_p)

	# save the pdf
	dwg.save()

class boxSide:
	width = 0
	height = 0
	side = 0
	points = []
	SVG_object = None

	# init function
	# args: width, height, side_letter, 
	#		thickness of material, 
	#       ratio of notch length to total side length,
	#       list[4] defining whether a notch is female (1) or male (0). Clockwise from 0,0 (lower left corner)
	def __init__(self, w, h, side_letter, notch_thickness, notch_ratio, notch_dir_list):
		self.width = w
		self.height = h
		self.side = side_letter

		# initialize points (left, top, right, bottom)
		self.points = self.create_box_points(w, h, notch_thickness, notch_ratio, notch_dir_list)

		print self.points, self.side
	#end __init__()

	def create_box_points(self, w, h, thick, notch_ratio, notch_dir_list):
		p = [ [0,0,] ]*(5*4+1)

		# corners
		p[5*0] = [0,0]
		p[5*1] = [0,h]
		p[5*2] = [w,h]
		p[5*3] = [w,0]
		p[5*4] = p[0] # make last point reference to first point, so it loops around.

		# for each side, set notch points
		for s in range(4):
			base_x, base_y = p[5*s][0],				p[5*s][1]
			v_x,    v_y    = p[5*s+5][0] - base_x, 	p[5*s+5][1] - base_y
			inv_notch_ratio = (1-notch_ratio)/2

			p[5*s+1] = [base_x + v_x*inv_notch_ratio, 						base_y + v_y*inv_notch_ratio] 						# inset edge 1
			p[5*s+2] = p[5*s+1][:]
			p[5*s+4] = [base_x + v_x*(1-inv_notch_ratio), 					base_y + v_y*(1-inv_notch_ratio)] 					# inset edge 2
			p[5*s+3] = p[5*s+4][:]

		#notch points are now correct along the edges. We need to offset them in the perpendicular direction.
		for s in range(4):

			# set direction sign (for use with the offset vector)
			if (s == 0):
				ds = 0 # horizontal
				flip = -1 # offset in negative x
			elif (s == 1):
				ds = 1 # vertical
				flip = 1 # offset in positve y
			elif (s == 2):
				ds = 0 # horizontal
				flip = 1 # offset in positive x
			elif (s == 3):
				ds = 1 # vertical
				flip = -1 # offset in negative y

			# offset each point
			for point in range(6):
				p[5*s+point][0] += offsets[ds][notch_dir_list[s]][point][0]*thick*flip
				p[5*s+point][1] += offsets[ds][notch_dir_list[s]][point][1]*thick*flip

		#remove duplicated last point here
		del p[-1]

		return p
	#end create_box_points

#actually run main
if __name__ == "__main__":
    main()