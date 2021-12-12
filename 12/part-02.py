import argparse
import numpy as np

np.set_printoptions( suppress = True )

ap = argparse.ArgumentParser( )
ap.add_argument( "-i", "--input", required = True, help = "Path to input file" )
args = vars( ap.parse_args( ) )

def get_input( filename ):
	fp = open( filename, "r" )

	data = [ ]
	while True:
		line = fp.readline( ).rstrip( "\n" )

		if not line:
			break

		data.append( line )

	return data

def parse_nodes( data ):
	nodes = { }

	for i in data:
		cave_01, cave_02 = i.split( "-" )	

		print( "  {} -> {}".format( cave_01, cave_02 ) )

		if cave_01 not in nodes:
			nodes[ cave_01 ] = [ ]

		if cave_02 not in nodes:
			nodes[ cave_02 ] = [ ]

		if cave_02 not in nodes[ cave_01 ]:
			nodes[ cave_01 ].append( cave_02 )

		if cave_01 not in nodes[ cave_02 ]:
			nodes[ cave_02 ].append( cave_01 )

	return nodes

def is_small_cave( string ):
	return string.islower( )

def small_cave_limit_reached( node, path, index ):
	small_caves = [ ]

	for i in path:
		if i == "start" or i == "end":
			continue

		if i.isupper( ):
			continue

		small_caves.append( i )

	unique, counts = np.unique( small_caves, return_counts = True )

	#space = " " * index * 2
	#print( "{}unqiue: {}".format( space, unique ) )
	#print( "{}counts: {}".format( space, counts ) )

	# Check if cave counts exceed 2
	if len( counts[ counts > 2 ] ) > 0:
		return True

	# Check only one cave has a count of two after adding node
	if len( counts[ counts == 2 ] ) > 1:
		return True
	
	return False

def traverse( index, nodes, node, paths, path ):
	#space = " " * index * 2
	#print( "" )
	#print( "{}node: {}".format( space, node ) )
	#print( "{}path: {}".format( space, path ) )
	#print( "{}{} -> opts: {}".format( space, node, sorted( nodes[ node ] ) ) )
	for i in sorted( nodes[ node ] ):

		if i == "start":
			continue

		#print( "{}i: {}".format( space, i ) )

		if is_small_cave( i ):

			if small_cave_limit_reached( i, path, index ):
				#print( "{}LIMIT REACHED".format( space ) )
				continue

		if i == "end":
			p = path.copy( )
			p.append( "end" )
			paths.append( p )
			continue

		p = path.copy( )
		p.append( i )

		traverse( index + 1, nodes, i, paths, p )
		

def calculate_paths( nodes ):
	paths = [ ]
	path  = [ "start" ]

	index = 0

	traverse( index, nodes, "start", paths, path )

	for i in paths:
		print( i )

	print( "count: {}".format( len( paths ) ) )

if __name__ == "__main__":
	data = get_input( args[ "input" ] )
	print( data )

	nodes = parse_nodes( data )

	for i in nodes:
		print( "{}".format( i ) )
		print( "  {}".format( list( sorted( nodes[ i ] ) ) ) )

	calculate_paths( nodes )
