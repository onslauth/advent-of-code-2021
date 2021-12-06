import argparse
import numpy as np

ap = argparse.ArgumentParser( )
ap.add_argument( "-i", "--input", required = True, help = "Path to input file" )
args = vars( ap.parse_args( ) )

def get_input( filename ):
	fp = open( filename, "r" )

	bins = np.zeros( [ 9, ], dtype = np.uint )

	fish = None
	while True:
		line = fp.readline( ).rstrip( "\n" )

		if not line:
			break

		print( line )
		fish = np.fromstring( line, dtype = np.int, sep = "," )

	for i in fish:
		bins[ i ] += 1

	for i in range( len( bins ) ):
		print( "[{}]: {}".format( i, bins[ i ] ) )

	return bins

def increment_fish( fish ):
	for day in range( 1, 257 ):

		new_fish = fish[ 0 ]
		for i in range( 0, 8 ):
			fish[ i ] = fish[ i + 1 ]

		fish[ 6 ] += new_fish
		fish[ 8 ] = new_fish

if __name__ == "__main__":
	fish = get_input( args[ "input" ] )
	increment_fish( fish )

	total = int( np.sum( fish ) )
	print( "fish count: {}".format( total ) )


