import argparse

ap = argparse.ArgumentParser( )
ap.add_argument( "-i", "--input", required = True, help = "Path to input file" )
args = vars( ap.parse_args( ) )


print( "Opening file: [{}]".format( args[ "input" ] ) )

i = 0
increased = 0
fp = open( args[ "input" ], "r" )

prev = None
curr = None

while True:
	line = fp.readline( ).rstrip( "\n" )


	if not line:
		print( "[EOF]" )
		break


	try:
		curr = int( line )
	except Exception as e:
		print( "ERROR: {}".format( e ) )
		break

	i += 1
	
	if prev != None:
		if prev < curr:
			print( "[LINE {:04}: {} ( increased )".format( i, line ) )
			increased += 1

		else:
			print( "[LINE {:04}: {} ( decreased )".format( i, line ) )

	prev = curr

print( "Increased: {}".format( increased ) )

