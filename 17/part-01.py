import argparse
import numpy as np

import heapq

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

	data = None

	while True:
		line = fp.readline( ).rstrip( "\n" )

		if not line:
			break

		data = line

	return data

def parse_data( data ):
	left, right = data.split( ": " )

	left, right = right.split( ", " )

	x_values = left
	y_values = right

	left, right = x_values.split( "=" )
	x1, x2 = right.split( ".." )

	left, right = y_values.split( "=" )
	y1, y2 = right.split( ".." )

	return ( int( x1 ), int( x2 ), int( y1 ), int( y2 ) )

def calculate_max_height( y1, y2 ):
	# Because the velocity of y is always y - 1 for each step,
	# Any positive velocity will always return to 0 at some point before going negative
	# That means the largest step it can take after reaching 0 again will be the 
	# maximum depth of the target area - 1

	y1 = abs( y1 )
	y2 = abs( y2 )

	y_max = max( y1, y2 )
	y_max -= 1

	count = 0
	for i in range( y_max, 0, -1 ):
		count += i

	print( count )

if __name__ == "__main__":
	data = get_input( args[ "input" ] )
	print( data )

	x1, x2, y1, y2 = parse_data( data )
	calculate_max_height( y1, y2 )

