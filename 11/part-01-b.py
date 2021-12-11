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

		print( "\n\nSTEP: {}".format( i ) )
		print( grid )

		while len( np.argwhere( grid >= 10 ) ) > 0:
			charged_octos = np.argwhere( grid >= 10 )
			count += len( charged_octos )

			all_adjacent = [ ]
			for j in charged_octos:
				y, x = j
				all_adjacent += get_adjacent( grid, x, y )
				grid[ y, x ] = 0

			print( "  all_adjacent: {}".format( all_adjacent ) )

			increment_adjacent( grid, all_adjacent )
			print( "" )
			print( grid )

	print( count )

if __name__ == "__main__":
	grid = get_input( args[ "input" ] )
	print( grid )

	steps = 100
	count_flashes( grid, steps )




