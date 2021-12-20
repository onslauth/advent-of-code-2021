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


	while True:
		line = fp.readline( )

		if len( line ) == 1:
			continue

		if not line:
			break

		data.append( line.rstrip( "\n" ) )

	lookup = data[ 0 ]
	grid   = data[ 1: ]

	return lookup, grid

def make_grid_from_string( data ):
	rows = [ ]
	for i in data:
		rows.append( np.fromstring( ",".join( i.replace( "#", "1" ).replace( ".", "0" ) ), sep = ",", dtype = np.uint8 ) )

	grid = np.array( rows )
	return grid

def bin_to_dec( kernel ):
	k = kernel.flatten( )
	v = k.dot( 2**np.arange( k.size )[ ::-1 ] )
	return v

def print_grid( grid ):
	return
	for i in grid:
		for j in i:
			if j == 0:
				print( ".", end = "" )
			else:
				print( "#", end = "" )
		print( "" )


def process_image( grid, lookup, fill_value = 0 ):

	h, w = grid.shape
	pad = 2

	ph = h + ( 2 * pad )
	pw = w + ( 2 * pad )

	padded = np.zeros( ( ph, pw ), dtype = np.uint8 )
	padded[ : ] = fill_value

	padded[ pad: ph - pad, pad:pw - pad ] = grid
	print_grid( padded )

	nh = h + pad
	nw = w + pad

	new_image = np.zeros( ( nh, nw ), dtype = np.uint8 )
	print_grid( new_image )

	for i in range( ph - 2 ):
		for j in range( pw - 2):
			kernel = padded[ i:i+3, j:j+3 ]
			#print( kernel )
			key = bin_to_dec( kernel.flatten( ) )
			value = lookup[ key ]

			if value == "#":
				new_image[ i, j ] = 1

	print_grid( new_image )
	return new_image

if __name__ == "__main__":
	lookup, data = get_input( args[ "input" ] )
	grid = make_grid_from_string( data )

	for i in range( 50 ):
		grid = process_image( grid, lookup, fill_value = i % 2 )

	print( len( grid[ grid > 0 ] ) )






