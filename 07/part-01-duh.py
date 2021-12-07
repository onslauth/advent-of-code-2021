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

def calculate_cost( data, position ):
	cost = 0
	for i in data:
		cost += abs( i - position )

	return cost


if __name__ == "__main__":
	data = get_input( args[ "input" ] )

	median = np.median( data )
	print( median )

	cost = calculate_cost( data, median )
	print( int( cost ) )

