import copy

#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########

AMPH_COST = { "A": 1, "B": 10, "C": 100, "D": 1000 }

TOP_ROW = [ "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E" ]

#A = [ "B", "D", "D", "A" ]
#B = [ "C", "C", "B", "D" ]
#C = [ "B", "B", "A", "C" ]
#D = [ "D", "A", "C", "A" ]

#####################
#.. . . . . . . . ..#
### D # B # C # C ###
  # D # C # B # A #
  # D # B # A # C #
  # D # A # B # A #
  #################

A = [ "D", "D", "D", "D" ]
B = [ "B", "C", "B", "A" ]
C = [ "C", "B", "A", "B" ]
D = [ "C", "A", "C", "A" ]

start = ( { "A": A, "B": B, "C": C, "D": D }, TOP_ROW )

CACHE = { }

def complete( bot ):
	for k, v in bot.items( ):
		for val in v:
			if val != k:
				return False

	return True

def print_state( state ):
	bot, top = state

	a_col = bot[ "A" ]
	b_col = bot[ "B" ]
	c_col = bot[ "C" ]
	d_col = bot[ "D" ]

	#print( "" )
	for t in top:
		print( "{} ".format( t ), end = "" )

	print( "" )

	for i in range( 4 ):
		a = a_col[ i ]
		b = b_col[ i ]
		c = c_col[ i ]
		d = d_col[ i ]

		print( "    {}   {}   {}   {}".format( a, b, c, d ) )

def make_key( state ):
	bot, top = state

	key = ( tuple( ( k, tuple( v ) ) for k, v in bot.items( ) ), tuple( top ) )
	return key

def col_index( key ):
	return { "A": 2, "B": 4, "C": 6, "D": 8 }[ key ]

def dest_col_index( col ):
	for i in reversed( range( 4 ) ):
		if col[ i ] == "E":
			return i

	return None
	
def check_bot_col( v, col ):
	for i in col:
		if i != v and i != "E":
			return False

	return True

def check_path_clear( top, start, end ):

	x1 = min( start, end ) + 1
	x2 = max( start, end )

	for i in range( x1, x2 ):
		if top[ i ] != "E":
			return False

	return True

def must_move_from_col( key, col ):
	for i in col:
		if i != key and i != "E":
			return True
	return False

def col_index_to_move( col ):
	for i, j in enumerate( col ):
		if j != "E":
			return i

	return None

def run( state ):
	bot, top = state

	print( "\nENTRY:" )
	print_state( state )

	if complete( bot ):
		return 0

	key = make_key( state )
	if key in CACHE:
		return CACHE[ key ]

	# Move from top row to column if possible
	
	# Loop over the top row
	for i, j in enumerate( top ):

		# Check if the value in top is in bot keys, i.e. "A", "B", "C", "D"
		if j in bot.keys( ) and check_bot_col( j, bot[ j ] ):
			if check_path_clear( top, i, col_index( j ) ):
				dest_index = dest_col_index( bot[ j ] )

				assert dest_index is not None

				print( "TOP:" )
				print_state( state )
				print( "  Moving from: {}( {} ) to col {}, {}".format( i, j, j, dest_index ) )

				distance = abs( col_index( j ) - i ) + dest_index + 1

				cost = AMPH_COST[ j ] * distance

				# Clear original top index because of second move in bottom for loop
				top[ i ] = "E"

				new_top = copy.deepcopy( top )
				new_top[ i ] = "E"

				new_bot = copy.deepcopy( bot )
				new_bot[ j ][ dest_index ] = j

				return cost + run( ( new_bot, new_top ) )

	# Move from column to top row
	new_cost = 1000000000
	print( "BEFORE BOT:" )
	print_state( ( bot, top ) )
	print( top )
	print( bot )
	for k, v in bot.items( ):

		col = v
		if not must_move_from_col( k, col ):
			continue

		# Index of column in top row
		ci = col_index( k )
		
		# Index of value to move from column if any
		src_index = col_index_to_move( col )
		if src_index is None:
			continue

		val_to_move = col[ src_index ]

		for dst_index in range( len( top ) ):
			if dst_index in [ 2, 4, 6, 8 ]:
				continue

			if top[ dst_index ] != "E":
				continue

			if check_path_clear( top, ci, dst_index ):
				print( "BOT:" )
				print( " Moving {} from col {}, {} to top {}".format( val_to_move, k, src_index, dst_index ) )
				print( top )
				print( bot )
				distance = abs( ci - dst_index ) + src_index + 1

				new_top = copy.deepcopy( top )
				assert new_top[ dst_index ] == "E"
				new_top[ dst_index ] = val_to_move

				new_bot = copy.deepcopy( bot )
				assert new_bot[ k ][ src_index ] == val_to_move
				new_bot[ k ][ src_index ] = "E"

				new_cost = min( new_cost, ( AMPH_COST[ val_to_move ] * distance ) + run( ( new_bot, new_top ) ) )
	
	CACHE[ key ] = new_cost
	print( "RETURNING\n\n" )

	return new_cost


val = run( start )
print( val )
