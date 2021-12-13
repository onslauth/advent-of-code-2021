import argparse
import numpy as np

ap = argparse.ArgumentParser( )
ap.add_argument( "-i", "--input", required = True, help = "Path to input file" )
args = vars( ap.parse_args( ) )

def get_input( filename ):
	fp = open( filename, "r" )

	data_01 = [ ]
	data_02 = [ ]

	x_max = 0
	y_max = 0

	data = data_01
	while True:
		line = fp.readline( )

		if len( line ) == 1:
			data = data_02
			continue

		if not line:
			break

		data.append( line.rstrip( "\n" ).split( "," ) )

	return data_01, data_02

def create_grid( data ):
	x_max = 0
	y_max = 0

	for i in data:
		x, y = i
		x = int( x )
		y = int( y )
		if x > x_max:
			x_max = x

		if y > y_max:
			y_max = y

	grid = np.zeros( [ y_max + 1, x_max + 1 ], dtype = np.uint8 )

	for i in data:
		x, y = i
		x = int( x )
		y = int( y )
		grid[ y, x ] = 1

	return grid

def fold_grid( grid, x = None, y = None ):
	if x == None and y == None:
		print( "No fold specified" )
		return

	if y != None:
		y = y + 1
		top_slice = grid[ 0:y - 1 ]
		bot_slice = np.flip( grid[ y:grid.shape[ 0 ] ], axis = 0 )

		grid = top_slice + bot_slice

	if x != None:
		x = x + 1
		left_slice  = grid[ :, 0:x - 1 ]
		right_slice = np.flip( grid[ :, x:grid.shape[ 1 ] ], axis = 1 )

		grid = left_slice + right_slice

	return grid



if __name__ == "__main__":
	data, instructions = get_input( args[ "input" ] )
	grid = create_grid( data )
	print( grid.shape  )

	grid = fold_grid( grid, x = 655 )	
