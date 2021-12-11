import argparse
import numpy as np

np.set_printoptions( suppress = True )

ap = argparse.ArgumentParser( )
ap.add_argument( "-i", "--input", required = True, help = "Path to input file" )
args = vars( ap.parse_args( ) )

def split_word( string ):
	a = [ ]
	for i in list( string ):
		a.append( i )

	return a

def get_input( filename ):
	fp = open( filename, "r" )

	data = [ ]
	while True:
		line = fp.readline( ).rstrip( "\n" )

		if not line:
			break

		data.append( split_word( line ) )

	return np.array( data, dtype = np.uint )

def get_adjacent( grid, x, y ):
	#print( "increment_adjacent:" )
	#print( "  x: {}".format( x ) )
	#print( "  y: {}".format( y ) )

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
	#print( "  ad: {}".format( adjacent_coords ) )

	return adjacent_coords

def increment_adjacent( grid, points ):
	for i in points:
		y, x = i
		if grid[ y, x ] == 0:
			continue

		grid[ y, x ] += 1

	return grid

def count_flashes( grid ):
	step      = 0
	count     = 0
	all_flash = False

	while all_flash == False:

		step += 1
		grid += 1

		#print( "\n\nSTEP: {}".format( step ) )
		#print( grid )

		while len( np.argwhere( grid >= 10 ) ) > 0:
			count += 1
			charged_octos = np.argwhere( grid >= 10 )

			y, x = charged_octos[ 0 ]
			#print( "\nflash: ( {}, {} )".format( x, y ) )
			closest = get_adjacent( grid, x, y )

			grid[ y, x ] = 0 
			increment_adjacent( grid, closest )
			#print( "" )
			#print( grid )

		if np.all( grid == 0 ):
			all_flash = True
			print( "ALL FLASH: {}".format( step ) )

	print( count )

if __name__ == "__main__":
	grid = get_input( args[ "input" ] )
	print( grid )

	count_flashes( grid )




