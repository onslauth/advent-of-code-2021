import argparse

ap = argparse.ArgumentParser( )
ap.add_argument( "-i", "--input", required = True, help = "Path to input file" )
args = vars( ap.parse_args( ) )


print( "Opening file: [{}]".format( args[ "input" ] ) )
fp = open( args[ "input" ], "r" )


depth = 0
aim   = 0
x = 0

while True:
	line = fp.readline( ).rstrip( "\n" )

	if not line:
		print( "EOF" )
		break

	direction, shift = line.split( " " )
	shift = int( shift )

	if direction in [ "up" ]:
		aim -= shift
	elif direction in [ "down" ]:
		aim += shift
	elif direction in [ "forward" ]:
		x += shift
		depth += ( aim * shift )

	print( "line: {}".format( line ) )

print( "  aim:   {}".format( aim ) )
print( "  depth: {}".format( depth ) )
print( "  x:     {}".format( x ) )

print( "  x * depth: {}".format( x * depth ) )
