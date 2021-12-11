import numpy as np
import cv2
import imutils
import random

### Part 01 solution

def split_word( string ):
	a = [ ]
	for i in list( string ):
		a.append( i )

	return a

def get_input( ):
	fp = open( "../input.txt", "r" )

	data = [ ]
	while True:
		line = fp.readline( ).rstrip( "\n" )

		if not line:
			break

		data.append( split_word( line ) )
	
	return np.array( data, dtype = np.uint )

def get_adjacent( grid, x, y ):
	height = grid.shape[ 0 ] - 1
	width  = grid.shape[ 1 ] - 1

	adjacent_coords = [ ]

	tl = ( y - 1, x - 1 )
	tp = ( y - 1, x )
	tr = ( y - 1, x + 1 )
	lt = ( y, x - 1 )
	rt = ( y, x + 1 )
	bl = ( y + 1, x - 1 )
	bt = ( y + 1, x )
	br = ( y + 1, x + 1 )

	if x == 0:
		tl = None
		lt = None
		bl = None
	if x == width:
		tr = None
		rt = None
		br = None
	if y == 0:
		tl = None
		tp = None
		tr = None
	if y == height:
		bl = None
		bt = None
		br = None

	adjacent_coords = [ x for x in [ tl, tp, tr, lt, rt, bl, bt, br ] if x != None ]

	return adjacent_coords

def increment_adjacent( grid, points ):
	for i in points:
		y, x = i
		if grid[ y, x ] == 0:
			continue

		grid[ y, x ] += 1

	return grid

def count_flashes( grid, steps ):
	count = 0

	for i in range( 0, steps ):

		grid += 1

		#print( grid )

		while len( np.argwhere( grid >= 10 ) ) > 0:
			count += 1
			charged_octos = np.argwhere( grid >= 10 )

			y, x = charged_octos[ 0 ]
			closest = get_adjacent( grid, x, y )

			grid[ y, x ] = 0 
			increment_adjacent( grid, closest )

### END Part 01 solution


def get_octo( ):
	octo = cv2.imread( "./octo-square.png" )
	return octo

def create_grid( width, height, color ):
	image = np.zeros( [ height, width, 3 ], dtype = np.uint8 )
	image[ :,: ] = color

	return image

def create_octo_img( img, info, cell, debug = False ):
	rotation   = info[ "rotation" ]
	direction  = info[ "direction" ]
	count      = info[ "count" ]
	#brightness = int( info[ "cell" ] ) * 10
	brightness = int( cell ) * 20

	if debug == True:
		print( info )
		print( "  cell: {}".format( cell ) )
		print( "  brightness: {}".format( brightness ) )

	rotation += ( direction * 5 )
	count += 5
	if count >= 25:
		direction *= -1
		count = 0

	info[ "rotation" ]  = rotation
	info[ "direction" ] = direction
	info[ "count" ]     = count

	o = imutils.rotate( img, rotation )

	b = o.astype( np.uint16 )
	b[ b > 0 ] += brightness
	o = b.clip( 0, 255 ).astype( np.uint8 )

	return o

def create_octo_grid( width, data ):
	octo_dict = [ ]

	for i in range( 0, width * 10, width ):
		for j in range( 0, width * 10, width ):
			rotation = random.randint( 0, 360 )
			direction = 1 if random.randint( 0, 1 ) == 0 else -1
			count = random.randint( 0, 25 )

			#brightness = random.randint( 0, 10 )

			y = int( j / 50 )
			x = int( i / 50 )

			#if x == 0 and y == 0:
			#	print( "  ( {}, {} ) -> {}".format( y, x, data[ y ][ x ] ) )

			info = {
				"y":           i,
				"x":           j,
				"rotation":    rotation,
				"direction":   direction,
				"count":       count,
				"cell":        data[ y ][ x ],
			}

			octo_dict.append( info )

	return octo_dict

def animate_octo_grid( octo_img, octo_dict, octo_grid, width ):

	diff = int( ( width -  octo_img.shape[ 0 ] ) / 2 )

	grid = create_grid( 10 * width, 10 * width, ( 0, 0, 0 ) )

	debug = False

	for i in octo_dict:
		x = i[ "x" ]
		y = i[ "y" ]

		if x == 0 and y == 0:
			debug = False
		else:
			debug = False

		cell = octo_grid[ int( y / 50 ) ][ int( x / 50 ) ]

		o = create_octo_img( octo_img, i, cell, debug = debug )
		grid[ y + diff:y + width - diff, x + diff: x + width - diff ] = o

	return grid

def create_video( octo_img, octo_dict, width ):
	images = [ ]
	for i in range( 0, 200 ):
		image = animate_octo_grid( octo_img, octo_dict, width )
		images.append( image )


	vid_size = ( width * 10, width * 10 )
	fourcc  = cv2.VideoWriter_fourcc( *"MP4V" )
	fps = 25

	video = cv2.VideoWriter( "vis.mp4", fourcc, fps, vid_size, isColor = True )
	
	for i, j in enumerate( images ):
		video.write( j )

	video.release( )

def write_video( images, width ):

	vid_size = ( width * 10, width * 10 )
	fourcc   = cv2.VideoWriter_fourcc( *"MP4V" )
	fps      = 25

	video = cv2.VideoWriter( "vis.mp4", fourcc, fps, vid_size, isColor = True )
	for i in images:
		video.write( i )

	video.release( )

def add_flashes_to_image( image, flashes ):

	for i in flashes:
		x      = int( ( i[ "x" ] * 50 ) + 25 )
		y      = int( ( i[ "y" ] * 50 ) + 25 )
		radius = i[ "size" ]

		if radius < 50:
			cv2.circle( image, ( x, y ), radius + 6,  ( 120, 120, 120 ), 3 )
			cv2.circle( image, ( x, y ), radius + 3,  ( 204, 204, 204 ), 2 )
			cv2.circle( image, ( x, y ), radius, ( 255, 255, 255 ), 3 )
			if radius - 2 > 0:
				cv2.circle( image, ( x, y ), radius - 2, ( 200, 200, 200 ), 2 )

	return image

def create_video_period( octo_img, octo_dict, octo_grid, flashes, width, step ):
	images = [ ]

	fps = 25

	font       = cv2.FONT_HERSHEY_SIMPLEX
	pos        = ( 15, 15 )
	font_scale = 0.5
	font_color = ( 255, 255, 255 )
	thickness  = 1
	linetype   = 2

	for i in range( 0, fps ):
		image = animate_octo_grid( octo_img, octo_dict, octo_grid, width )
		image = add_flashes_to_image( image, flashes )
		cv2.putText( image,
			     "Step: {}".format( step ),
			     pos,
			     font,
			     font_scale,
			     font_color,
			     thickness,
			     linetype )

		images.append( image )

		for j in flashes:
			j[ "size" ] += 5

	return images

def perform_step( octo_img, octo_dict, octo_grid, width ):
	steps = 10
	count = 0

	images = [ ]

	flashes = [ ]

	for i in range( 0, steps ):

		#print( "\n\nSTEP: {}".format( i ) )

		octo_grid += 1
		flashes = [ ]

		while len( np.argwhere( octo_grid >= 10 ) ) > 0:
			charged_octos = np.argwhere( octo_grid >= 10 )
			count += len( charged_octos )


			all_adjacent = [ ]
			for j in charged_octos:
				y, x = j
				all_adjacent += get_adjacent( octo_grid, x, y )
				octo_grid[ y, x ] = 0

				flash = {
					"x":    x,
					"y":    y,
					"size": 0,
				}

				flashes.append( flash )

			increment_adjacent( octo_grid, all_adjacent )
			#print( "  octo_grid[ 0 ][ 0 ]: {}".format( octo_grid[ 0 ][ 0 ] ) )

			images += create_video_period( octo_img, octo_dict, octo_grid, flashes, width, i )

			flashes = [ x for x in flashes if x[ "size" ] < 50 ]

	write_video( images, width )

	print( "count: {}".format( count ) )

if __name__ == "__main__":

	data = get_input( )

	width = 50
	octo = get_octo( )
	small = imutils.resize( octo, width = width - 10 )

	octo_dict = create_octo_grid( width, data )
	perform_step( small, octo_dict, data, width )

	#create_video( small, octo_dict, width )

