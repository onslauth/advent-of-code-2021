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

def split_word( string ):
	a = [ ]
	for i in list( string ):
		a.append( i )

	return a

def calculate_digits( line ):
	left  = line[ 0 ]
	right = line[ 1 ]

	top = None
	tl  = None
	tr  = None
	mid = None
	bl  = None
	br  = None
	bot = None

	digits = {
		0: None,
		1: split_word( [ x for x in left if len( x ) == 2 ][ 0 ] ),
		2: None,
		3: None,
		4: split_word( [ x for x in left if len( x ) == 4 ][ 0 ] ),
		5: None,
		6: None,
		7: split_word( [ x for x in left if len( x ) == 3 ][ 0 ] ),
		8: split_word( [ x for x in left if len( x ) == 7 ][ 0 ] ),
		9: None,
	}

	# Calculate top segment
	top = list( set( digits[ 7 ] ) -  set( digits[ 1 ] ) )

	# Top left and middle is 4 - 1
	top_left_and_middle = list( set( digits[ 4 ] ) - set( digits[ 1 ] ) )

	# Use 1 + 4 + 7 to calculate 9 and bot
	comb = list( set( digits[ 1 ] + digits[ 4 ] + digits[ 7 ] ) )

	six_sided_digits = [ x for x in left if len( x ) == 6 ] # [ 0, 6, 9 ]
	
	for i in six_sided_digits:
		rem = list( set( i ) - set( comb ) )
		if len( rem ) == 1:
			digits[ 9 ] = split_word( i )
			six_sided_digits = [ x for x in six_sided_digits if x != i ]
			bot = rem
			break


	# Calculate 3 and mid using 1 + top + bot
	five_sided_digits = [ x for x in left if len( x ) == 5 ] # [ 2, 3, 5 ]
	comb = list( set( digits[ 1 ] + top + bot ) )

	for i in five_sided_digits:
		rem = list( set( i ) - set( comb ) )
		if len( rem ) == 1:
			digits[ 3 ] = split_word( i )
			five_sided_digits = [ x for x in five_sided_digits if x != i ]
			mid = rem
			break


	# Calculate top left using 4 - 1 - mid
	tl = list( set( top_left_and_middle ) - set( mid ) )

	# Calculate 5 and bottom right using tl + top + mid + bot
	comb = list( set( tl + top + mid + bot ) )
	for i in five_sided_digits:
		rem = list( set( i ) - set( comb ) )
		if len( rem ) == 1:
			digits[ 5 ] = split_word( i )
			five_sided_digits = [ x for x in five_sided_digits if x != i ]
			br = rem
			break

	digits[ 2 ] = split_word( five_sided_digits[ 0 ] )

	# Calculate top right
	tr = list( set( digits[ 1 ] ) - set( br ) )

	# Calculate 6 and bottom left
	comb = list( set ( top + tl + mid + br + bot ) )
	for i in six_sided_digits:
		rem = list( set( i ) - set( comb ) )
		if len( rem ) == 1:
			digits[ 6 ] = split_word( i )
			bl = rem
			six_sided_digits = [ x for x in six_sided_digits if x != i ]
			break

	digits[ 0 ] = split_word( six_sided_digits[ 0 ] )

	string = ""
	for i in right:
		for j in digits:
			if set( i ) == set( digits[ j ] ):
				string += str( j )

	return string

def split_data( data ):
	parsed_data = [ ]
	for i in data:
		left, right = i.split( " | " )

		left =  left.split( " " )
		right = right.split( " " )

		parsed_data.append( [ left, right ] )

	return parsed_data

if __name__ == "__main__":
	data = get_input( args[ "input" ] )
	parsed_data = split_data( data )

	count = 0
	for i in parsed_data:
		count += int( calculate_digits( i ) )
	print( count )

