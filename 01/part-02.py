import argparse

ap = argparse.ArgumentParser( )
ap.add_argument( "-i", "--input", required = True, help = "Path to input file" )
args = vars( ap.parse_args( ) )


print( "Opening file: [{}]".format( args[ "input" ] ) )

i = 0
increased = 0
fp = open( args[ "input" ], "r" )
lines = fp.readlines( )

prev = None
curr = None

for i in range( len( lines ) - 2 ):
	try:
		curr = int( lines[ i ] ) + int( lines[ i + 1 ] ) + int( lines[ i + 2 ] )
	except Exception as e:
		print( "ERROR: {}".format( e ) )

	if prev != None:
		if prev < curr:
			increased += 1

	prev = curr

print( "increased: {}".format( increased ) )
