import argparse
import sys
import numpy as np
import ast
import copy

class Node:
	def __init__( self, parent = None, left = None, right = None ):
		self.parent = parent
		self.left   = left
		self.right  = right

	def __repr__( self ):
		string = "["
		if isinstance( self.left, Node ):
			string += repr( self.left )
		else:
			string += "{}".format( self.left )

		string += ","

		if isinstance( self.right, Node ):
			string += repr( self.right )
		else:
			string += "{}".format( self.right ) 

		string += "]"

		return string

	def depth( self ):
		if self.parent is None:
			return 0
		else:
			return 1 + self.parent.depth( )

	def max_depth( self ):
		a = 0
		b = 0
		if isinstance( self.left, Node ):
			a = self.left.max_depth( )
		else:
			b = self.depth( )

		if isinstance( self.right, Node ):
			b = self.right.max_depth( )
		else:
			b = self.depth( )

		return max( a, b )

	def add( self, node ):
		n = Node( )
		n.left   = self.left
		n.right  = self.right
		n.parent = self

		if isinstance( self.left, Node ):
			n.left.parent  = n

		if isinstance( self.right, Node ):
			n.right.parent = n

		node.parent = self

		self.left  = n
		self.right = node

	def need_explode( self ):
		return self.max_depth( ) >= 4

	def need_split( self ):
		
		if isinstance( self.left, Node ):
			a = self.left.need_split( )
		else:
			a = self.left > 9

		if isinstance( self.right, Node ):
			b = self.right.need_split( )
		else:
			b = self.right > 9

		return a or b

	def check_level( self ):
		if isinstance( self.left, Node ):
			a = self.left.check_level( )

		if isinstance( self.right, Node ):
			b = self.right.check_level( )

		#print( "l: {}, r: {}, d: {}".format( self.left, self.right, self.depth( ) ) )

		if self.depth( ) >= 4:
			self.explode( )
			return True

		return a or b

	def check_split( self ):
		if isinstance( self.left, Node ):
			a = self.left.check_split( )
		else:
			if self.left > 9:
				self.split( self.left )
				

		if isinstance( self.right, Node ):
			self.right.check_split( )
		else:
			if self.right > 9:
				self.split( self.right )

	def is_left( self ):
		return self.parent.left == self

	def is_right( self ):
		return self.parent.right == self

	def is_root( self ):
		return self.parent == None

	def explode( self ):
		if isinstance( self.left, Node ) and isinstance( self.right, Node ):
			return

		if self.parent is None:
			return

		#print( "\n\nExploding node: {}".format( self ) )
		#print( "  left: {}, right: {}".format( self.left, self.right ) )

		left_val  = self.left
		right_val = self.right

		nparent = self.parent

		# Go up parent until parent is a right branch of we hit the top of the tree
		# Once we find a right branch, take the left child, then walk down right side till we hit a number

		#print( "  searching for right node..." )
		n = self
		while True:

			if n.is_root( ):
				#print( "    n is root, breaking" )
				break

			if n.is_left( ):
				n = n.parent
				continue

			else:
				#print( "    found right node: {}".format( n ) )
				parent  = n.parent
				sibling = parent.left

				#print( "    parent: {}, sibling: {}".format( parent, sibling ) )

				if isinstance( sibling, int ):
					#print( "      sibling is int, s: {}, p: {}".format( sibling, parent ) )
					parent.left += left_val

				else:
					n = parent.left
					while isinstance( n.right, Node ):
						n = n.right

					#print( "      found n: {}".format( n ) )

					n.right += left_val
					#print( "        n: {}".format( n ) )

				break


		#print( "  searching for left node..." )
		n = self
		#print( "    n: {}, is_left: {}".format( n, n.is_left( ) ) )
		while True:

			if n.is_root( ):
				#print( "    n is root, breaking" )
				break

			#print( "  n: {}, is_left: {}, is_right: {}".format( n, n.is_left( ), n.is_right( ) ) )

			if n.is_right( ):
				n = n.parent
				continue

			else:
				#print( "  found left node: {}".format( n ) )
				parent  = n.parent
				sibling = parent.right

				#print( "    parent: {}, sibling: {}".format( parent, sibling ) )

				if isinstance( sibling, int ):
					#print( "      sibling is int, s: {}, p: {}".format( sibling, parent ) )
					parent.right += right_val

				else:
					n = parent.right
					while isinstance( n.left, Node ):
						n = n.left

					#print( "      found n: {}".format( n ) )

					n.left += right_val
					#print( "        n: {}".format( n ) )

				break



		if self.is_left( ):
			self.parent.left = 0
		else:
			self.parent.right = 0

		#print( nparent )

		n = self
		while not n.is_root( ):
			n = n.parent

		#print( n )

		#print( "" )


	def split( self, value ):

		#print( "\n\nSPLITTING: {}".format( self ) )

		a = int( np.floor( value / 2 ) )
		b = int( np.ceil( value / 2 ) )

		if value == self.left:
			self.left = Node( parent = self, left = a, right = b )
		elif value == self.right:
			self.right = Node( parent = self, left = a, right = b )

		n = self
		while not n.is_root( ):
			n = n.parent

		#print( n )

		#print( "" )


ap = argparse.ArgumentParser( )
ap.add_argument( "-i", "--input", required = True, help = "Path to input file" )
args = vars( ap.parse_args( ) )

def split_word( string ):
	a = [ ]
	for i in list( string ):
		a.append( i )
	return a

def create_node( data, parent ):
	if type( data ) != list:
		return data

	n = Node( )
	n.parent = parent
	n.left = create_node( data[ 0 ], n )
	n.right = create_node( data[ 1 ], n )

	return n

def create_tree( line ):
	a = ast.literal_eval( line )

	t = Node( )

	t.left  = create_node( a[ 0 ], t )
	t.right = create_node( a[ 1 ], t )

	return t

def get_input( filename ):
	fp = open( filename, "r" )

	data = [ ]


	while True:
		line = fp.readline( ).rstrip( "\n" )

		if not line:
			break

		data.append( create_tree( line ) )

	return data

def check_explode( node ):
	if isinstance( node, Node ):
		check_explode( node.left )
		#print( node )
		#print( node.depth( ) )
		#print( "" )
		if node.depth( ) >= 4:
			node.explode( )
			return True
		check_explode( node.right )

	return False

def check_split( node ):

	if isinstance( node, Node ):
		left = check_split( node.left )
		if left == True:
			return True


		if isinstance( node.left, int ):
			if node.left >= 10:
				node.split( node.left )
				return True

		if isinstance( node.right, int ):
			if node.right >= 10:
				node.split( node.right )
				return True

		right = check_split( node.right )
		if right == True:
			return True

	return False

def calc_magnitude( node ):
	left = 0
	right = 0

	if isinstance( node.left, Node ):
		left = calc_magnitude( node.left ) * 3
	else:
		left = node.left * 3

	if isinstance( node.right, Node  ):
		right = calc_magnitude( node.right ) * 2
	else:
		right = node.right * 2

	return left + right


if __name__ == "__main__":
	data = get_input( args[ "input" ] )

	values = [ ]

	for i in range( len( data ) - 1 ):
		first = data[ i ]

		for second in data[ i + 1: ]:

			print( "  first:  {}".format( first ) )
			print( "  second: {}".format( second ) ) 

			f1 = copy.deepcopy( first )
			f2 = copy.deepcopy( first )

			s1 = copy.deepcopy( second )
			s2 = copy.deepcopy( second )

			f1.add( s1 )
			while True:
				if check_explode( f1 ):
					continue
				if check_split( f1 ):
					continue

				break

			s2.add( f2 )
			while True:
				if check_explode( s2 ):
					continue
				if check_split( s2 ):
					continue

				break

			m1 = calc_magnitude( f1 )
			m2 = calc_magnitude( s2 )

			print( "m1: {}".format( m1 ) )
			print( "m2: {}".format( m2 ) )

			values.append( m1 )
			values.append( m2 )

			print( "" )

	print( values )
	max_value = values[ 0 ]
	for i in values:
		if i > max_value:
			max_value = i

	print( max_value )


		

			


