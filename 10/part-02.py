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

	return np.array( data )

def compare_opening_closing( lines ):

	opening_brackets = [ "(", "[", "{", "<" ]
	closing_brackets = {
		")": "(", 
		"]": "[",
		"}": "{",
		">": "<",
	}

	legal_lines = [ ]

	for l in lines:
		opening = [ ]

		for i in l:
			if i in opening_brackets:
				opening.append( i )
				continue

			if i in closing_brackets:
				last = opening.pop( )
				value = closing_brackets[ i ]

				if last != value:
					opening = [ ]
					break

		if len( opening ) > 0:
			legal_lines.append( [ "".join( l ), opening ] )
			#print( "{} - {}".format( "".join( l ), opening ) )

	return legal_lines

def calculate_autocomplete_count( lines ):

	opening_brackets = {
		"(": 1,
		"[": 2,
		"{": 3,
		"<": 4,
	}

	scores = [ ]

	for l in lines:
		lines, opening = l
		count = 0

		for i in reversed( opening ):
			value = opening_brackets[ i ]
			count *= 5
			count += value

		scores.append( count )

	l = len( scores )

	mid = int( np.floor( l / 2 ) )

	sorted_scores = sorted( scores )
	print( sorted_scores[ mid ] )


if __name__ == "__main__":
	data = get_input( args[ "input" ] )

	values = compare_opening_closing( data )
	calculate_autocomplete_count( values )




