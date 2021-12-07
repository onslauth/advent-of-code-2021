import argparse
import numpy as np

np.set_printoptions( suppress = True )

ap = argparse.ArgumentParser( )
ap.add_argument( "-i", "--input", required = True, help = "Path to input file" )
args = vars( ap.parse_args( ) )

def get_input( filename ):
	fp = open( filename, "r" )

	data = None
	while True:
		line = fp.readline( ).rstrip( "\n" )

		if not line:
			break

		data = np.fromstring( line, sep = ",", dtype = np.uint )

	return data

def create_grid( data ):
	size = len( data )
	grid = np.zeros( [ size, size ] )

	return grid

def calculate_shift( index, grid ):

	size = len( index )

	for row in range( size ):
		val = index[ row ]
		for col in range( size ):
			j = index[ col ]

			high = max( j, val )
			low  = min( j, val )

			n = high - low

			grid[ row ][ col ] = n

def sum_rows( grid ):
	sum_grid = np.sum( grid, axis = 1 )
	return sum_grid

if __name__ == "__main__":
	data = get_input( args[ "input" ] )

	grid = create_grid( data )
	
	calculate_shift( data, grid )

	sum_grid = sum_rows( grid )
	a = np.argmin( sum_grid )

	print( "Position {} costs {}".format( data[ a ], int (sum_grid[ a ] ) ) )


