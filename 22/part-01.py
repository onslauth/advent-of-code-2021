import argparse
import sys
import numpy as np
import ast

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

	lines = fp.read( ).rstrip( "\n" ).split( "\n" )

	for i in lines:
		state, l = i.split( " " )
		x, y, z = l.split( "," )
		x_range = list( map( int, x.split( "=" )[ 1 ].split( ".." ) ) )
		y_range = list( map( int, y.split( "=" )[ 1 ].split( ".." ) ) )
		z_range = list( map( int, z.split( "=" )[ 1 ].split( ".." ) ) )

		#print( x_range, y_range, z_range ) 

		if state == "on":
			state = 1
		else:
			state = 0

		data.append( ( state, x_range, y_range, z_range ) )

	return data

def turn_on_cubes( data ):

	on_cubes = set( )

	for i in data:
		state = i[ 0 ]
		x1, x2 = i[ 1 ]
		y1, y2 = i[ 2 ]
		z1, z2 = i[ 3 ]

		if x1 < -50 or x2 > 50:
			continue

		if y1 < -50 or y2 > 50:
			continue

		if z1 < -50 or z2 > 50:
			continue

		cubes = [ ( x, y, z ) for x in range( x1, x2 + 1 ) for y in range( y1, y2 + 1 ) for z in range( z1, z2 + 1 ) ]
		print( i )

		for j in cubes:
			#print( "  {}".format( j ) )

			if state == 1:
				on_cubes.add( j )
			else:
				try:
					on_cubes.remove( j )
				except:
					pass

	print( len( on_cubes ) )

if __name__ == "__main__":
	data = get_input( args[ "input" ] )
	print( data )

	turn_on_cubes( data )

	

