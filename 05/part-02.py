import argparse
import numpy as np

ap = argparse.ArgumentParser( )
ap.add_argument( "-i", "--input", required = True, help = "Path to input file" )
args = vars( ap.parse_args( ) )

def get_input( filename ):
	fp = open( filename, "r" )

	max_x = 0
	max_y = 0

	coords = [ ]
	while True:
		line = fp.readline( ).rstrip( "\n" )

		if not line:
			break

		start, end = line.split( "->" )
		x1, y1     = map( int, start.split( "," ) )
		x2, y2     = map( int, end.split( "," ) )

		max_x = max( max_x, x1 )
		max_x = max( max_x, x2 )

		max_y = max( max_y, y1 )
		max_y = max( max_y, y2 )

		coords.append( [ [ x1, y1 ], [ x2, y2 ] ] )

	return coords, max_x + 1, max_y + 1

def create_grid( x, y ):
	grid = np.zeros( [ y, x ] )
	return grid

def mark_straight_line_on_grid( grid, x1, y1, x2, y2 ):
	if x1 == x2:
		t1 = min( y1, y2 )
		t2 = max( y1, y2 )
		y1 = t1
		y2 = t2

	elif y1 == y2:
		t1 = min( x1, x2 )
		t2 = max( x1, x2 )
		x1 = t1
		x2 = t2

	x2 += 1
	y2 += 1

	grid[ y1:y2, x1:x2 ] += 1

def mark_sloped_line_on_grid( grid, x1, y1, x2, y2 ):
	# Line equation: y = mx + b

	m = ( y1 - y2 ) / ( x1 - x2 )
	b = ( ( x1 * y2 ) - ( x2 * y1 ) ) / ( x1 - x2 )

	inc = 1
	if x2 < x1:
		inc = -1
		
	for i in range( x1, x2 + inc, inc ):
		y = int( ( m * i ) + b )
		grid[ y, i ] += 1

def populate_grid( grid, lines ):

	for i in lines:
		x1, y1 = i[ 0 ]
		x2, y2 = i[ 1 ]

		if x1 != x2 and y1 != y2:
			mark_sloped_line_on_grid( grid, x1, y1, x2, y2 )
		else:
			mark_straight_line_on_grid( grid, x1, y1, x2, y2 )


if __name__ == "__main__":
	line_equations, max_x, max_y = get_input( args[ "input" ] )

	print( "  limit: ( {}, {} )".format( max_x, max_y ) )

	grid = create_grid( max_x, max_y )
	populate_grid( grid, line_equations )
	print( grid )

	#b = np.where( grid > 1 )
	#print( b )
	#total = int( np.sum( grid[ b ] ) )
	#print( "total: {}".format( total ) )

	total = int( ( grid > 1 ).sum( ) )
	print( "total: {}".format( total ) )

