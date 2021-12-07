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

def create_index_and_grid( data ):

	m = max( data )

	index = np.arange( m )
	cols  = len( data )

	grid = np.zeros( [ m, cols ] )

	return index, grid

def calculate_shift( index, data, grid ):
	
	for row in range( len( index ) ):
		val = index[ row ]

		for col in range( grid.shape[ 1 ] ):
			j = data[ col ]
			high = max( val, j )
			low  = min( val, j )

			n = high - low

			diff = int( ( n * ( n + 1 ) ) / 2 )

			grid[ row ][ col ] = diff


if __name__ == "__main__":
	data = get_input( args[ "input" ] )

	index, grid = create_index_and_grid( data )

	calculate_shift( index, data, grid )

	sum_grid = np.sum( grid, axis = 1 )
	a = np.argmin( sum_grid )
	print( a )
	print( int( sum_grid[ a ] ) )
