import argparse

ap = argparse.ArgumentParser( )
ap.add_argument( "-i", "--input", required = True, help = "Path to input file" )
args = vars( ap.parse_args( ) )


print( "Opening file: [{}]".format( args[ "input" ] ) )
fp = open( args[ "input" ], "r" )

x = 0
y = 0

while True:
	line = fp.readline( ).rstrip( "\n" )

	if not line:
		print( "EOF" )
		break

	direction, shift = line.split( " " )
	shift = int( shift )

	if direction in [ "up" ]:
		y -= shift
	elif direction in [ "down" ]:
		y += shift
	elif direction in [ "forward" ]:
		x += shift

	print( "line: {}".format( line ) )

print( " x * y = {}".format( x * y ) )
