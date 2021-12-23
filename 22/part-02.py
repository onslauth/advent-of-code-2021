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

		x_range[ 1 ] += 1
		y_range[ 1 ] += 1
		z_range[ 1 ] += 1

		#print( x_range, y_range, z_range ) 

		if state == "on":
			state = 1
		else:
			state = 0

		data.append( ( state, x_range, y_range, z_range ) )

	return data

def collate_points( steps ):
	x = [ ]
	y = [ ]
	z = [ ]

	for i in steps:
		print( i )

		x1, x2 = i[ 1 ]
		y1, y2 = i[ 2 ]
		z1, z2 = i[ 3 ]

		x.extend( [ x1, x2 ] )
		y.extend( [ y1, y2 ] )
		z.extend( [ z1, z2 ] )

	x = list( sorted( x ) )
	y = list( sorted( y ) )
	z = list( sorted( z ) )

	n = len( x )

	#grid = [ ]
	#for i in range( n ):
	#	x_axis = [ ]
	#	for j in range( n ):
	#		y_axis = [ ] 
	#		for k in range( n ):
	#			y_axis.append( 0 )

	#		x_axis.append( y_axis )
	#	grid.append( x_axis )

	grid = np.zeros( ( n, n, n ), dtype = np.uint8 )

	#print( grid )

	return grid, x, y, z

def run_steps( steps, grid, x, y, z ):

	for s in steps:
		state = s[ 0 ]

		x1, x2 = s[ 1 ]
		y1, y2 = s[ 2 ]
		z1, z2 = s[ 3 ]

		ix1 = x.index( x1 )
		ix2 = x.index( x2 )

		iy1 = y.index( y1 )
		iy2 = y.index( y2 )

		iz1 = z.index( z1 )
		iz2 = z.index( z2 )

		grid[ ix1:ix2, iy1:iy2, iz1:iz2 ] = state

		#for i in range( ix1, ix2 ):
		#	for j in range( iy1, iy2 ):
		#		for k in range( iz1, iz2 ):
		#			grid[ i ][ j ][ k ] = state


if __name__ == "__main__":
	steps = get_input( args[ "input" ] )
	
	grid, x, y, z = collate_points( steps )
	run_steps( steps, grid, x, y, z )

	n = len( x )

	sum_on = 0

	# This is really slow.
	for i in range( 0, n - 1 ):
		for j in range( 0, n - 1 ):
			for k in range( 0, n - 1 ):
				state = grid[ i ][ j ][ k ]
				if state == 0:
					continue

				sum_on += state * ( x[ i + 1 ] - x[ i ] ) * ( y[ j + 1 ] - y[ j ] ) * ( z[ k + 1 ] - z[ k ] )

	print( "sum_on: {}".format( sum_on ) )


	

