import math, svgwrite

# Side Letters (Left, Right, Fore, Aft, Top, Bottom)
L, R, F, A, T, B = 1, 2, 3, 4, 5, 6

# notch offsets[horizontal|vertical][male|female][point#]
offsets = [ \
			[ \
				[ (0,0),(0,0),(1,0),(1,0),(0,0),(0,0) ], \
				[ (1,0),(1,0),(0,0),(0,0),(1,0),(1,0) ]  \
			], \
			[  \
				[ (0,0),(0,0),(0,1),(0,1),(0,0),(0,0) ], \
				[ (0,1),(0,1),(0,0),(0,0),(0,1),(0,1) ]  \
			] ]


class box_side:
	width = 0
	height = 0
	side = 0
	points = []

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
		self.points += [[0,0], [0,h], [w,h], [w,0], [0,0]]

		# add notch points in line with current sides
		self.points = [ [0,0,] ]*(5*4+1)
		p = self.points # temporary accessor

		# corners
		p[5*0] = [notch_thickness,		notch_thickness  ]
		p[5*1] = [notch_thickness,		h-notch_thickness]
		p[5*2] = [w-notch_thickness,	h-notch_thickness]
		p[5*3] = [w-notch_thickness,	notch_thickness  ]
		p[5*4] = [notch_thickness,		notch_thickness  ]

		# make last point reference to first point, so it loops around.
		p[-1] = p[0]

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
		print p
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
				p[5*s+point][0] += offsets[ds][notch_dir_list[s]][point][0]*notch_thickness*flip
				p[5*s+point][1] += offsets[ds][notch_dir_list[s]][point][1]*notch_thickness*flip

		#remove duplicated last point here

		print self.points, self.side
	#end __init__()

def main(argv=None):
	print "hello world"

	# Config variables
	m_xdepth 	 = 10.0
	m_ydepth 	 = 10.0
	m_zdepth 	 = 3.0
	m_thickness  = 1.0/8.0
	m_notchratio = 1.0/3.0
	make_roof	 = False

	# make sides
	Side_base =  box_side(m_xdepth, m_ydepth, B, m_thickness, m_notchratio, [0, 0, 0, 0])
	Side_left =  box_side(m_xdepth, m_zdepth, L, m_thickness, m_notchratio, [1, 0, 1, 1])
	Side_right = box_side(m_xdepth, m_zdepth, R, m_thickness, m_notchratio, [1, 0, 1, 1])

	Side_fore = box_side(m_ydepth, m_zdepth, F, m_thickness, m_notchratio, [0, 0, 0, 1])
	Side_aft =  box_side(m_ydepth, m_zdepth, A, m_thickness, m_notchratio, [0, 0, 0, 1])

	if make_roof == True:
		Side_top = box_side(m_ydepth, m_zdepth, T, m_thickness, m_notchratio, [1, 1, 1, 1])

	print Side_base.points

#actually run main
if __name__ == "__main__":
    main()