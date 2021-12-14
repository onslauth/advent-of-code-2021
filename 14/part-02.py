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

def create_template_dict_and_counter( template ):
	comb    = { }
	counter = { }

	counter[ template[ 0 ] ] = 1

	for i in range( len( template ) - 1 ):

		a = template[ i ]
		b = template[ i + 1 ]

		if b in counter:
			counter[ b ] += 1
		else:
			counter[ b ] = 1

		key = a + b

		if key in comb:
			comb[ key ] += 1
		else:
			comb[ key ] = 1

	return comb, counter
	
def create_polymer( template, data, counter ):

	orig = template.copy( )

	for key in data:
		count = orig.pop( key, None )
		if count == None:
			continue

		if count == template[ key ]:
			template.pop( key )
		else:
			template[ key ] -= count

		value = data[ key ]
		if value in counter:
			counter[ value ] += count
		else:
			counter[ value ] = count

		left  = key[ 0 ] + value
		right = value + key[ 1 ]

		if left in template:
			template[ left ] += count
		else:
			template[ left ] = count

		if right in template:
			template[ right ] += count
		else:
			template[ right ] = count

if __name__ == "__main__":
	template, data = get_input( args[ "input" ] )
	print( "Template: {}".format( template ) )
	template, counter = create_template_dict_and_counter( template )
	print( template )
	print( counter )

	steps = 40
	for i in range( steps ):
		create_polymer( template, data, counter )

	first_key = list( counter.keys( ) )[ 0 ]
	min_value = counter[ first_key ]
	max_value = counter[ first_key ]

	for i in counter:
		if counter[ i ] > max_value:
			max_value = counter[ i ]

		if counter[ i ] < min_value:
			min_value = counter[ i ]

	print( "{} - {} = {}".format( max_value, min_value, max_value - min_value ) )


