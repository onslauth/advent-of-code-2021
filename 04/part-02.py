import argparse
import numpy as np

ap = argparse.ArgumentParser( )
ap.add_argument( "-i", "--input", required = True, help = "Path to input file" )
args = vars( ap.parse_args( ) )

def read_input( filename ):
	print( "read_input:" )
	print( "  filename: {}".format( filename ) )

	fp = open( args[ "input" ], "r" )

	numbers_drawn = None
	index = 0

	boards = [ ]
	board = np.array( [ 5, 5 ], dtype = np.uint )
	row = -1

	values = ""

	board_id = 0

	while True:
		line = fp.readline( )

		if not line:
			break

		line = line.rstrip( "\n" )

		# Save the drawn numbers
		if index == 0:
			numbers_drawn = line
			index += 1
			continue
		
		# Check for blank lines
		if not line:
			continue

		values += line + " "
		row += 1

		if row == 4 and len( values ) > 0:
			board = Board( board_id, values )
			boards.append( board )

			board_id += 1
			board     = [ ]
			values    = ""
			row       = -1

	return numbers_drawn, boards

class Board:
	def __init__( self, board_id, values ):
		self.board_id = board_id
		self.board    = np.fromstring( values, sep = " " ).reshape( 5, 5 )
		self.guesses  = np.zeros( [ 5, 5 ], dtype = np.uint )
		self.rows     = np.zeros( 5 )
		self.cols     = np.zeros( 5 )

	def update_board( self, value ):
		location = np.where( self.board == value )

		if len( location[ 0 ] ) == 0:
			return

		row = location[ 0 ][ 0 ]
		col = location[ 1 ][ 0 ]

		self.guesses[ row ][ col ] = 1

		self.rows[ row ] += 1
		self.cols[ col ] += 1

	def check_bingo( self ):
		if 5 in self.rows:
			return True

		if 5 in self.cols:
			return True

		return False

if __name__ == "__main__":
	numbers, boards = read_input( args[ "input" ] )

	not_bingo = False
	numbers   = numbers.split( "," )
	current   = ""
	i         = 0

	winning_board = None
	previous_guesses = [ ]

	remaining_boards = len( boards )

	while not_bingo == False:
		value = int( numbers[ i ] )
		previous_guesses.append( value )
		current += "{} ".format( value )

		for j in boards:

			if j.check_bingo( ) == True:
				continue

			j.update_board( value )
			if j.check_bingo( ) == True:
				remaining_boards -= 1

				if remaining_boards == 1:
					not_bingo = True
					break


		i += 1

	last_board = None
	for j in boards:
		if j.check_bingo( ) == False:
			last_board = j
			break

	while last_board.check_bingo( ) == False:
		value = int( numbers[ i ] )
		previous_guesses.append( value )
		last_board.update_board( value )
		i += 1

	mask      = ~np.array( last_board.guesses, dtype = bool )
	remainder = last_board.board[ mask ]
	total     = np.sum( remainder )
	final_guess = previous_guesses[ -1 ]
	print( "total: {}".format( int( final_guess * total ) ) )



