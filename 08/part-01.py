import argparse
import numpy as np

np.set_printoptions( suppress = True )

ap = argparse.ArgumentParser( )
ap.add_argument( "-i", "--input", required = True, help = "Path to input file" )
args = vars( ap.parse_args( ) )

def get_input( filename ):
	fp = open( filename, "r" )

	data = [ ]
	while True:
		line = fp.readline( ).rstrip( "\n" )

		if not line:
			break

		data.append( line )

	return data

def count_unique_digits( data ):
	values = [ ]
	count = 0

	for i in data:
		left, right = i.split( " | " )
		digits = right.split( " " )
		#values += digits
		for j in digits:
			if len( j ) in [ 2, 3, 4, 7 ]:
				count += 1

	#print( values )
	print( count )

if __name__ == "__main__":
	data = get_input( args[ "input" ] )
	count_unique_digits( data )

