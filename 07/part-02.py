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

	m = int( max( data ) + 1 )
	n = int( min( data ) )

	index = np.arange( n, m )

	costs = np.zeros( [ m, ] )

	return index, costs

def calculate_shift_cost( index, data, costs ):
	
	for row in range( len( index ) ):
		val = index[ row ]

		for col in range( len( data ) ):

			j = data[ col ]
			high = max( val, j )
			low  = min( val, j )

			n = high - low

			diff = int( ( n * ( n + 1 ) ) / 2 )

			costs[ row ] += diff


if __name__ == "__main__":
	data = get_input( args[ "input" ] )

	index, costs = create_index_and_grid( data )

	calculate_shift_cost( index, data, costs )

	a = np.argmin( costs )
	print( a )
	print( int( costs[ a ] ) )
