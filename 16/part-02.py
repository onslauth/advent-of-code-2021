import argparse
import numpy as np

import heapq

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

	data = None

	while True:
		line = fp.readline( ).rstrip( "\n" )

		if not line:
			break

		data = line

	return data

def convert_to_bits( data ):

	string = ""

	for i in data:

		hex_value = i
		int_value = int( i, base = 16 )
		bin_value = bin( int_value )

		#print( "{} -> {}".format( i, str( bin_value )[ 2: ].zfill( 4 ) ) )

		string += str( bin_value )[ 2: ].zfill( 4 )

	return string

def parse_literal_packet( bit_string ):
	print( "\nparse_literal_packet:" )

	start = 6
	end   = start + 5
	print( bit_string[ start: ] )

	number_string = ""
	number        = None

	while True:
		number = bit_string[ start:end ]
		#print( "  n: {}".format( number ) )

		number_string += number[ 1: ]

		if number[ 0 ] == "0":
			break

		start += 5
		end   = start + 5

	number = int( number_string, base = 2 )

	length = end
	#print( "  number: {}".format( number ) )
	#print( "  length: {}".format( length ) )

	#print( bit_string[ length: ] )

	print( "  l: {}, n: {}".format( length, number ) )
	print( "" )

	return length, number

def parse_operator_sub_data( bit_string ):
	data = [ ]
	i = 0
	while i < len( bit_string ):
		p, v, t = get_packet_type( bit_string[ i: ] )

		print( "    p: {}, v: {}, t: {}".format( p, v, t ) )

		if p == "literal":
			size, number = parse_literal_packet( bit_string[ i: ] )
			print( "      n: {}".format( number ) )
			data.append( ( "l", v, t, number ) )
			i += size

		else:
			size, ret_data = parse_operator_packet( bit_string[ i: ] )
			data += [ ( "o", v, t, ret_data ) ]
			print( "      r: {}".format( ret_data ) )
			i += size

	return data

def parse_operator_packet( bit_string ):
	print( "\nparse_operator_packet:" )

	length_id = bit_string[ 6 ]
	start = 7

	sub_data = [ ]

	print( "  {}".format( bit_string ) )
	print( "  l_id: {}".format( length_id ) )

	data_size = 0
	if length_id == "0":
		data_size = 15
	else:
		data_size = 11

	end = start + data_size

	sub_packet_length = bit_string[ start:end ]

	if length_id == "0":
		sub_packet_size = int( sub_packet_length, base = 2 )
		data_start = end
		data_end   = end + sub_packet_size

		sub_packet_size   = int( sub_packet_length, base = 2  )
		print( "  sub_packet_length: {} -> {}".format( sub_packet_length, sub_packet_size ) )

		data = bit_string[ data_start:data_end ]
		print( "  data: {}".format( data ) )

		ret_data = parse_operator_sub_data( data )
		sub_data += ret_data

		length = data_end

	else:
		packet_count = int( sub_packet_length, base = 2 )
		print( "  packet_count: {}".format( packet_count ) )

		i = end
		packet_index = 0
		while packet_index < packet_count:
			p, v, t = get_packet_type( bit_string[ i: ] )

			if p == "literal":
				size, number = parse_literal_packet( bit_string[ i: ] )
				sub_data.append( ( "l", v, t, number ) )
				i += size
			else:
				size, ret_data = parse_operator_packet( bit_string[ i: ] )
				sub_data += [ ( "o", v, t, ret_data ) ]
				i += size

			packet_index += 1

		length = i

	print( "  sub_data: {}".format( sub_data ) )
	return length, sub_data

def get_packet_type( bit_string ):
	v_start = 0
	v_end   = v_start + 3

	t_start = v_end
	t_end   = t_start + 3

	version = bit_string[ v_start:v_end ]
	ptype   = bit_string[ t_start:t_end ]

	packet = None

	if ptype == "100":
		packet = "literal"
	else:
		packet = "operator"

	return packet, version, ptype

def calculate_version_count( data ):
	count = 0
	for i in data:
		if i[ 0 ] == "l":
			print( "lit: {}".format( int( i[ 1 ], base = 2 ) ) )
			count += int( i[ 1 ], base = 2 )

		if i[ 0 ] == "o":
			count += int( i[ 1 ], base = 2 )
			print( "op:  {}".format( i[ 3 ] ) )
			count += calculate_version_count( i[ 3 ] )

	return count

def calculate_value( data, index = 0 ):

	# 0: o | l
	# 1: version
	# 2: type
	# 3: number | array

	ret_values = [ ]

	count = 0
	print( "data: {}".format( data ) )

	for i in data[ 3 ]:
		print( i )
		if i[ 0 ] == "l":
			ret_values.append( i[ 3 ] )

		elif i[ 0 ] == "o":
			ret_values.append( calculate_value( i ) )

	operand = int( data[ 2 ], base = 2 )

	print( "  op: {}".format( operand ) )
	print( "  ret: {}".format( ret_values ) )
	
	# sum
	if operand == 0:
		for i in ret_values:
			count += i

	# product
	elif operand == 1:
		count = 1
		for i in ret_values:
			count *= i

	# minimum
	elif operand == 2:
		count = ret_values[ 0 ]
		for i in ret_values:
			if i < count:
				count = i

	# maximum
	elif operand == 3:
		count = ret_values[ 0 ]
		for i in ret_values:
			if i > count:
				count = i

	# greater than
	elif operand == 5:
		if ret_values[ 0 ] > ret_values[ 1 ]:
			count = 1
		else:
			count = 0

	# less than
	elif operand == 6:
		if ret_values[ 0 ] < ret_values[ 1 ]:
			count = 1
		else:
			count = 0

	elif operand == 7:
		if ret_values[ 0 ] == ret_values[ 1 ]:
			count = 1
		else:
			count = 0

	print( "  count: {}".format( count ) )
	return count

def parse_string( bit_string ):

	# 0 -> 2: Packet version
	# 3 -> 5: Packet type

	index = 0
	length_bits = len( bit_string )

	ret_data = [ ]

	while index < length_bits:
		print( bit_string[ index: ] )
		if int( bit_string[ index: ], base = 2 ) == 0:
			break

		p, v, t = get_packet_type( bit_string[ index: ] )
		print( "p: {}, v: {}, t: {}".format( p, v, t ) )

		if p == "literal":
			size, number = parse_literal_packet( bit_string[ index: ] )
			ret_data.append( ( "l", v, t, number ) )
			index += size

		else:
			size, data = parse_operator_packet( bit_string[ index: ] )
			ret_data.append( ( "o", v, t, data ) )
			index += size

	#print( calculate_version_count( ret_data ) )
	print( "\n\ncalculating:" )
	print( calculate_value( ret_data[ 0 ] ) )

if __name__ == "__main__":
	data = get_input( args[ "input" ] )
	print( data )

	bit_string = convert_to_bits( data )

	parse_string( bit_string )
