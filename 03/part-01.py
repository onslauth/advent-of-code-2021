import argparse
import numpy as np

ap = argparse.ArgumentParser( )
ap.add_argument( "-i", "--input", required = True, help = "Path to input file" )
args = vars( ap.parse_args( ) )


print( "Opening file: [{}]".format( args[ "input" ] ) )
fp = open( args[ "input" ], "r" )

data = [ ]

while True:
	line = fp.readline( ).rstrip( "\n" )

	if not line:
		print( "EOF" )
		break

	binary = [ int( x ) for x in line ]
	data.append( binary )

data = np.array( data )

count = np.apply_along_axis( np.bincount, 0, data ).argmax( axis = 0 )

binary_string = "".join( [ str( x ) for x in count ] )

gamma   = int( binary_string, 2 )
epsilon = ( ~gamma & 0xFFF )

print( "gamma:             {}".format( gamma ) )
print( "epsilon:           {}".format( epsilon ) )
print( "power consumption: {}".format( gamma * epsilon ) )
