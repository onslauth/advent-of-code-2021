import argparse
import numpy as np

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

	template = split_word( fp.readline( ).rstrip( "\n" ) )
	data = {
	}

	while True:
		line = fp.readline( )

		if len( line ) == 1:
			continue

		if not line:
			break

		left, right = line.rstrip( "\n" ).split( " -> " )

		data[ left ] = right

	return template, data

def create_polymer( template, data, steps ):

	new  = template
	orig = new.copy( )

	for i in range( steps ):
		orig = new.copy( )
		new  = [ ]

		size = len( orig )
		#print( "\nSTEP: {}".format( i ) )

		new += [ orig[ 0 ] ]

		for j in range( size - 1 ):
			key   = orig[ j ] + orig[ j + 1 ]
			value = data[ key ]

			#print( "{} -> {}".format( key, value ) )

			new += [ value, key[ 1 ] ]
		#print( new )

	unique, counts = np.unique( new, return_counts = True )

	max_key = 0
	min_key = 0
	for i in range( len( unique ) ):
		if counts[ i ] > counts[ max_key ]:
			max_key = i
		if counts[ i ] < counts[ min_key ]:
			min_key = i
		print( "{} -> {}".format( unique[ i ], counts[ i ] ) )

	max_value = counts[ max_key ]
	min_value = counts[ min_key ]
	print( "{} - {} = {}".format( max_value, min_value, max_value - min_value ) )

if __name__ == "__main__":
	template, data = get_input( args[ "input" ] )
	print( "Template: {}".format( template ) )
	print( data )

	steps = 10

	create_polymer( template, data, steps )
