import argparse
import sys
import numpy as np
import ast

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

def roll_dice( dice ):
	moves = 0

	for i in range( 3 ):
		dice += 1
		if dice > 100:
			dice = 1

		moves += dice

	return dice, moves

def play_game( p1_pos, p2_pos ):
	dice = 0
	rolls = 0

	p1_score, p2_score = 0, 0

	turn = 0
	while p1_score < 1000 and p2_score < 1000:
		print( "\nturn: {}".format( turn + 1 ) )

		rolls += 3

		dice, moves = roll_dice( dice )

		print( " = {}".format( moves ) )
		print( "  dice: {}".format( dice ) )


		if turn % 2 == 0:
			print( "  Player 1 turn:" )

			p1_pos += moves
			p1_pos = ( ( p1_pos - 1 ) % 10 ) + 1

			p1_score += p1_pos

		else:
			print( "  Player 2 turn:" )

			p2_pos += moves
			p2_pos = ( ( p2_pos - 1 ) % 10 ) + 1

			p2_score += p2_pos

		print( "    p1_pos: {}, p1_score: {}".format( p1_pos, p1_score ) )
		print( "    p2_pos: {}, p2_score: {}".format( p2_pos, p2_score ) )
	
		turn = ( turn + 1 ) % 2 

	print( "Number rolls: {}".format( rolls ) )
	print( "Player 1 score: {}".format( p1_score ) )
	print( "Player 2 score: {}".format( p2_score ) )

	if p1_score > p2_score:
		print( rolls * p2_score )
	else:
		print( rolls * p1_score )



if __name__ == "__main__":
	player_1, player_2 = get_input( args[ "input" ] )

	print( "player_1: {}".format( player_1 ) )
	print( "player_2: {}".format( player_2 ) )

	play_game( player_1, player_2 )



