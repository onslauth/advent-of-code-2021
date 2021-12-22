import argparse
import functools

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

	lines = fp.read( ).rstrip( "\n" ).split( "\n" )

	player_1 = int( lines[ 0 ].split( ": " )[ 1 ] )
	player_2 = int( lines[ 1 ].split( ": " )[ 1 ] )

	return player_1, player_2

def get_position( pos, i, j, k ):
	pos += ( i + j + k )
	pos = ( ( pos - 1 ) % 10 ) + 1

	return pos

def calculate_combinations( ):
	return [ ( x, y, z ) for x in [ 1, 2, 3 ] for y in [ 1, 2, 3 ] for z in [ 1, 2, 3 ] ]

cache = { }

#@functools.lru_cache( maxsize = None )
def calculate_wins( p1_pos, p1_score, p2_pos, p2_score ):
	p1_wins = 0
	p2_wins = 0

	if ( p1_pos, p1_score, p2_pos, p2_score ) in cache:
		p1_wins, p2_wins = cache[ ( p1_pos, p1_score, p2_pos, p2_score ) ]
		return p1_wins, p2_wins

	for c in calculate_combinations( ):
		i, j, k = c

		pos = get_position( p1_pos, i, j, k )
		score = p1_score + pos

		if score >= 21:
			p1_wins += 1
		else:
			ret_p1_wins, ret_p2_wins = calculate_wins( p2_pos, p2_score, pos, score )

			p1_wins += ret_p2_wins
			p2_wins += ret_p1_wins

	cache[ ( p1_pos, p1_score, p2_pos, p2_score ) ] = [ p1_wins, p2_wins ]

	return p1_wins, p2_wins

if __name__ == "__main__":
	player_1, player_2 = get_input( args[ "input" ] )

	print( "player_1: {}".format( player_1 ) )
	print( "player_2: {}".format( player_2 ) )

	p1_wins, p2_wins = calculate_wins( player_1, 0, player_2, 0 )
	print( max( p1_wins, p2_wins ) )



