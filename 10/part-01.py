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

	illegal_values = [ ]

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
					illegal_values.append( i )
					break

	return illegal_values

def calculate_values( illegal_values ):
	points = {
		")": 3,
		"]": 57,
		"}": 1197,
		">": 25137,
	}

	score = 0
	for i in illegal_values:
		score += points[ i ]

	print( score )

if __name__ == "__main__":
	data = get_input( args[ "input" ] )

	values = compare_opening_closing( data )
	calculate_values( values )




