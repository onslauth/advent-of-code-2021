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
		#data.append( line )

	return np.array( data, dtype = np.uint )

def calculate_low_points( grid, mask ):
	height = grid.shape[ 0 ]
	width  = grid.shape[ 1 ]

	total = 0

	for row in range( height ):
		for col in range( width ):

			if row == 0:
				top = None
			else:
				top = grid[ row - 1 ][ col ]

			if row == height - 1:
				bot = None
			else:
				bot = grid[ row + 1 ][ col ]

			if col == 0:
				left = None
			else:
				left = grid[ row ][ col - 1 ]

			if col == width - 1:
				right = None
			else:
				right = grid[ row ][ col + 1 ]

			adjacent = [ left, top, right, bot ]
			surrounding_values = [ x for x in adjacent if x != None ]

			pos = grid[ row ][ col ]

			if all( pos < x for x in surrounding_values ):
				mask[ row ][ col ] = 1
				total += ( pos + 1 )

	return int( total ), mask

def scan_surround( grid, x, y ):

	height = grid.shape[ 0 ] - 1
	width  = grid.shape[ 1 ] - 1

	left  = x - 1
	right = x + 1
	up    = y - 1
	down  = y + 1

	if y == 0:
		up = None
	else:
		up = [ y - 1, x ]

	if y == height:
		down = None
	else:
		down = [ y + 1, x ]

	if x == 0:
		left = None
	else:
		left = [ y, x - 1 ]

	if x == width:
		right = None
	else:
		right = [ y, x + 1 ]

	points = [ x for x in [ left, up, right, down ] if x != None ]
	return points

def calculate_basin( grid, mask ):
	basins = [ ]

	starting_points = np.argwhere( mask == 1 )

	#print( starting_points )

	index = 0
	for i in starting_points:
		y, x = i

		points    = [ i ]
		locations = { }

		while len( points ) > 0:
			y, x = points.pop( )
			pt = ( y, x )

			if pt in locations:
				continue

			if grid[ y ][ x ] == 9:
				continue

			locations[ pt ] = 1

			new_points = scan_surround( grid, x, y )

			points += new_points

		basins.append( len( locations ) )

	sorted_basins = np.sort( basins )
	total = sorted_basins[ -1 ] * sorted_basins[ -2 ] * sorted_basins[ -3 ]
	return total

if __name__ == "__main__":
	grid = get_input( args[ "input" ] )

	mask = np.zeros( grid.shape )
	value, mask = calculate_low_points( grid, mask )

	value = calculate_basin( grid, mask )
	print( value )
