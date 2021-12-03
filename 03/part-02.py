import argparse
import numpy as np
import sys

np.set_printoptions( threshold = sys.maxsize )

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

size = len( data[ 0 ] )

o2_values  = np.copy( data )
co2_values = np.copy( data )
o2_answer  = None
co2_answer = None

current_o2_filter = ""
current_co2_filter = ""

for i in range( size ):

	if o2_answer is None:
		j = np.bincount( o2_values[ :,i ] )
		if j[ 0 ] == j[ 1 ]:
			j = 1
		else:
			j = j.argmax( )
		current_o2_filter += str( j )

		o2_values = o2_values[ o2_values[ :,i ] == j ]

		if len( o2_values ) == 1:
			o2_answer = o2_values[ 0 ]

	if co2_answer is None:
		j = np.bincount( co2_values[ :,i ] )
		j = j.argmin( )
		current_co2_filter += str( j )

		co2_values = co2_values[ co2_values[ :,i ] == j ]

		if len( co2_values ) == 1:
			co2_answer = co2_values[ 0 ]

	if o2_answer is not None and co2_answer is not None:
		break

print( "o2_answer:  {}".format( o2_answer ) )
print( "co2_answer: {}".format( co2_answer ) )

string = "".join( [ str( x ) for x in o2_answer ] )
oxygen_generator_rating = int( string, 2 )

string = "".join( [ str( x ) for x in co2_answer ] )
co2_scrubber_rating = int( string, 2 )

life_support_rating = oxygen_generator_rating * co2_scrubber_rating
print( "Life support rating: {}".format( life_support_rating ) )
