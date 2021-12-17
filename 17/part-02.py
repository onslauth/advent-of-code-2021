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


def calculate_x_velocity( answer ):
	x = answer * 2
	required_answer = 1

	for i in range( 1, int( x / 2 ) ):
		if x % i != 0:
			continue

		y = -x / i
		if i + y == required_answer:
			return i

def calculate_min_x( x1, x2 ):
	options = [ ]
	for i in range( x1, x2 + 1 ):
		x = calculate_x_velocity( i )
		if x != None:
			options.append( x - 1 )

	print( options )

	x = list( sorted( options ) )[ 0 ]

	return x

def calculate_max_y( y1, y2 ):
	y1 = abs( y1 )
	y2 = abs( y2 )
	
	y_max = max( y1, y2 ) - 1

	return y_max

def brute_force( min_x, max_x, min_y, max_y, x1, x2, y1, y2 ):

	options = set( )

	x = min_x
	y = min_y

	x_velocity = min_x
	y_velocity = max_y

	print( "brute_force:" )
	print( "  x1: {}, x2: {}".format( x1, x2 ) )
	print( "  y1: {}, y2: {}".format( y1, y2 ) )

	for x_velocity in range( min_x, max_x + 1 ):
		for y_velocity in range( max_y, min_y - 1, -1 ):

			pos_x = 0
			pos_y = 0

			dx = x_velocity
			dy = y_velocity

			while pos_x <= x2 and pos_y >= y2:

				#print( "{},{} -> ".format( pos_x, pos_y ), end = "" )

				pos_x += dx
				pos_y += dy

				#print( "{},{}".format( pos_x, pos_y ) )
				#print( "  dx: {}, dy: {}".format( dx, dy ) )

				if x1 <= pos_x <= x2 and y2 <= pos_y <= y1:
					options.add( ( x_velocity, y_velocity ) )

				if dx > 0:
					dx -= 1

				dy -= 1

	print( "len( options ): {}".format( len( options ) ) )

	#for i in list( sorted( options ) ):
	#	print( i )

if __name__ == "__main__":
	data = get_input( args[ "input" ] )
	print( data )

	x1, x2, y1, y2 = parse_data( data )

	min_x = calculate_min_x( x1, x2 )
	print( min_x )

	max_x = x2

	min_y = min( y1, y2 )
	max_y = calculate_max_y( y1, y2 )

	print( "min_x: {}, max_x: {}".format( min_x, max_x ) )
	print( "min_y: {}, max_y: {}".format( min_y, max_y ) )

	brute_force( min_x, max_x, min_y, max_y, x1, x2, y2, y1 )
