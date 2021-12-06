import argparse
import numpy as np

ap = argparse.ArgumentParser( )
ap.add_argument( "-i", "--input", required = True, help = "Path to input file" )
args = vars( ap.parse_args( ) )

def get_input( filename ):
	fp = open( filename, "r" )

	fish = None
	while True:
		line = fp.readline( ).rstrip( "\n" )

		if not line:
			break

		print( line )
		fish = list( map( int, line.split( "," ) ) )

	return fish

def increment_fish( fish ):
	for day in range( 1, 81 ):
		print( "day: {}".format( day ) )
		
		for i in range( len( fish ) ):
			if fish[ i ] == 0:
				fish[ i ] = 6
				fish.append( 8 )

			else:
				fish[ i ] -= 1

if __name__ == "__main__":
	fish = get_input( args[ "input" ] )

	print( "Start value: {}".format( len( fish ) ) )
	increment_fish( fish )

	print( "Fish count:  {}".format( len( fish ) ) )

