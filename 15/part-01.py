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

	data = [ ]

	while True:
		line = fp.readline( ).rstrip( "\n" )

		if not line:
			break

		row = split_word( line )

		data.append( row )

	return np.array( data, dtype = np.uint8 )

def walk_maze( grid ):
	x = 0
	y = 0

	dest = ( grid.shape[ 0 ] - 1, grid.shape[ 1 ] - 1 )
	visited = np.zeros( ( grid.shape[ 0 ], grid.shape[ 1 ] ) )

	# heapq sorts by first element in tuple
	paths = [ ( 0, x, y ) ]

	heapq.heapify( paths )

	while True:
		value = heapq.heappop( paths )
		count, x, y = value

		if visited[ y ][ x ] == 1:
			continue

		if ( x, y ) == dest:
			return count

		visited[ y ][ x ] = 1

		up = ( x, y - 1 )
		down = ( x, y + 1 )
		left = ( x - 1, y )
		right = ( x + 1, y )

		for i, j in [ up, down, left, right ]:
			if 0 <= i < grid.shape[ 1 ] and 0 <= j < grid.shape[ 0 ]:

				if visited[ j ][ i ]:
					continue

				next_value = grid[ j ][ i ]

				heapq.heappush( paths, ( count + next_value, i, j ) )


if __name__ == "__main__":
	grid = get_input( args[ "input" ] )
	print( grid )
	print( grid.shape )

	value = walk_maze( grid )
	print( value )
