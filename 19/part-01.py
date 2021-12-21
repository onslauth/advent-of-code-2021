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

	sensors = [ ]

	lines = fp.read( ).rstrip( "\n" )

	group = lines.split( "\n\n" )
	for i in group:
		data = i.split( "\n" )

		name = data[ 0 ]

		coords = [ ]

		for j in data[ 1: ]:
			x, y, z = j.split( "," )
			coords.append( [ int( x ), int( y ), int( z ) ] )

		coords = np.array( coords )

		s = {
			"name":   name,
			"coords": coords,
		}
		sensors.append( s )

	return sensors

def calculate_line_length( pt1, pt2 ):
	x1, y1, z1 = pt1
	x2, y2, z2 = pt2

	x = ( x2 - x1 )**2
	y = ( y2 - y1 )**2
	z = ( z2 - z1 )**2

	return np.sqrt( x + y + z )

def calculate_line_lengths_for_sensor( s ):

	coords = s[ "coords" ]

	lines = { }
	points = { }

	for i in range( len( coords ) - 1 ):
		x1, y1, z1 = coords[ i ]
		pt1 = ( x1, y1, z1 )

		for j in coords[ i+1: ]:
			x2, y2, z2 = j
			pt2 = ( x2, y2, z2 )
			
			length = calculate_line_length( pt1, pt2 )
			lines[ length ] = ( pt1, pt2 )
			points[ ( pt1, pt2 ) ] = length

	s[ "lines" ]  = lines
	s[ "points" ] = points

def calculate_sensor( s ):
	calculate_line_lengths_for_sensor( s )

def find_two_lines_common_point( s1, lines ):
	print( "\nfind_two_lines_common_point:" )
	points = [ ]
	for i in lines:
		p = s1[ "lines" ][ i ]
		points.append( p )

	pt1, pt2 = points[ 0 ]
	print( pt1, pt2 )

	pt3 = None
	pt4 = None

	for i in points[ 1: ]:
		pt3, pt4 = i

		if pt1 in [ pt3, pt4 ]:
			break

		if pt2 in [ pt3, pt4 ]:
			break

	print( "  pt1: {}, pt2: {}".format( pt1, pt2 ) )
	print( "  pt3: {}, pt4: {}".format( pt3, pt4 ) )

	length_1 = s1[ "points" ][ ( pt1, pt2 ) ]
	length_2 = s1[ "points" ][ ( pt3, pt4 ) ]

	return length_1, length_2

def get_length( s1, pt1, pt2 ):
	if ( pt1, pt2 ) in s1[ "points" ]:
		return s1[ "points" ][ ( pt1, pt2 ) ]
	else:
		return s1[ "points" ][ ( pt2, pt1 ) ]

def get_common_point( s1, length_1, length_2 ):
	pt1, pt2 = s1[ "lines" ][ length_1 ]
	pt3, pt4 = s1[ "lines" ][ length_2 ]

	common = None
	other  = None
	if pt1 == pt3:
		common = pt1
		other  = pt2
		
	if pt1 == pt4:
		common = pt1
		other  = pt2

	if pt2 == pt3:
		common = pt2
		other  = pt1

	if pt2 == pt4:
		common = pt2
		other  = pt1

	print( "\nget_common_point:" )
	print( "  length_1: {}".format( length_1 ) )
	print( "  length_2: {}".format( length_2 ) )
	print( "  {}, {}".format( pt1, pt2 ) )
	print( "  {}, {}".format( pt3, pt4 ) )

	print( "  {}, {} -> {}".format( common, other, get_length( s1, common, other ) ) )

	print( "  common: {}, other: {}".format( common, other ) )

	return common, other

def check_axis_positions( r1, r2 ):
	print( "\ncheck_axis_positions:" )

	swap = [ 0, 1, 2 ]

	if r1[ 0 ] == r2[ 1 ]:
		swap[ 0 ] = 1
	elif r1[ 0 ] == r2[ 2 ]:
		swap[ 0 ] = 2

	if r1[ 1 ] == r2[ 0 ]:
		swap[ 1 ] = 0
	elif r1[ 1 ] == r2[ 2 ]:
		swap[ 1 ] = 2

	if r1[ 2 ] == r2[ 0 ]:
		swap[ 2 ] = 0
	elif r1[ 2 ] == r2[ 1 ]:
		swap[ 2 ] = 1

	return swap

def check_axis_direction( swap, r1, r2 ):
	print( "\ncheck_axis_direction:" )
	rx1 = r1[ 0 ]
	ry1 = r1[ 1 ]
	rz1 = r1[ 2 ]

	rx2 = r2[ swap[ 0 ] ]
	ry2 = r2[ swap[ 1 ] ]
	rz2 = r2[ swap[ 2 ] ] 

	inv = [ 1, 1, 1 ]

	print( "  x: {}, {}".format( rx1, rx2 ) )
	print( "  y: {}, {}".format( ry1, ry2 ) )
	print( "  z: {}, {}".format( rz1, rz2 ) )

	if rx1 == -rx2:
		inv[ 0 ] = -1

	if ry1 == -ry2:
		inv[ 1 ] = -1

	if rz1 == -rz2:
		inv[ 2 ] = -1

	return inv

def swap_and_invert_axes( s1, swap, inv ):
	print( "\nswap_and_invert_axes:" )
	print( "  swap: {}".format( swap ) )
	print( "  inv:  {}".format( inv ) )

	x = s1[ "coords" ][ :, swap[ 0 ] ].copy( )
	y = s1[ "coords" ][ :, swap[ 1 ] ].copy( )
	z = s1[ "coords" ][ :, swap[ 2 ] ].copy( )

	x *= inv[ 0 ]
	y *= inv[ 1 ]
	z *= inv[ 2 ]

	s1[ "coords" ][ :,0 ] = x
	s1[ "coords" ][ :,1 ] = y
	s1[ "coords" ][ :,2 ] = z

def convert_points_to_relative( s1, pos ):
	x = pos[ 0 ]
	y = pos[ 1 ]
	z = pos[ 2 ]

	s1[ "coords" ][ :,0 ] += x
	s1[ "coords" ][ :,1 ] += y
	s1[ "coords" ][ :,2 ] += z

def check_and_adjust_axis( s1, s2, length_1, length_2 ):
	print( "\ncheck_and_adjust_axis:" )

	s1_common_pt, s1_other_pt = get_common_point( s1, length_1, length_2 )
	s2_common_pt, s2_other_pt = get_common_point( s2, length_1, length_2 )

	print( "  s1:" )
	print( "    {}, {}".format( s1_common_pt, s1_other_pt ) )
	print( "  s2:" )
	print( "    {}, {}".format( s2_common_pt, s2_other_pt ) )
	
	rx1 = s1_common_pt[ 0 ] - s1_other_pt[ 0 ]
	ry1 = s1_common_pt[ 1 ] - s1_other_pt[ 1 ]
	rz1 = s1_common_pt[ 2 ] - s1_other_pt[ 2 ]

	rx2 = s2_common_pt[ 0 ] - s2_other_pt[ 0 ]
	ry2 = s2_common_pt[ 1 ] - s2_other_pt[ 1 ]
	rz2 = s2_common_pt[ 2 ] - s2_other_pt[ 2 ]

	print( "  rx1: {}, ry1: {}, rz1: {}".format( rx1, ry1, rz1 ) )
	print( "  rx2: {}, ry2: {}, rz2: {}".format( rx2, ry2, rz2 ) )

	swap = check_axis_positions( ( abs( rx1 ), abs( ry1 ), abs( rz1 ) ), ( ( abs( rx2 ), abs( ry2 ), abs( rz2 ) ) ) )
	print( "  swap: {}".format( swap ) )

	inv = check_axis_direction( swap, ( rx1, ry1, rz1 ), ( rx2, ry2, rz2 ) )
	print( "  inv: {}".format( inv ) )

	x1 = s1_common_pt[ 0 ]
	y1 = s1_common_pt[ 1 ]
	z1 = s1_common_pt[ 2 ]

	x2 = s2_common_pt[ swap[ 0 ] ]
	y2 = s2_common_pt[ swap[ 1 ] ]
	z2 = s2_common_pt[ swap[ 2 ] ]

	print( x1, y1, z1 )
	print( x2, y2, z2 ) 

	x = x1 - ( inv[ 0 ] * x2 )
	y = y1 - ( inv[ 1 ] * y2 ) 
	z = z1 - ( inv[ 2 ] * z2 )
	pos = ( x, y, z )

	x2 *= inv[ 0 ]
	y2 *= inv[ 1 ]
	z2 *= inv[ 2 ]
	print( x2 + x, y2 + y, z2 + z )
	print( "  pos: {}, {}, {}".format( x, y, z ) )

	#print_sensor( s1 )

	#print( "\nBEFORE SWAP & INV" )
	#print_sensor( s2 )
	
	swap_and_invert_axes( s2, swap, inv )
	#print( "\nAFTER SWAP & INV" )
	#print_sensor( s2 )

	convert_points_to_relative( s2, pos )
	#print( "\nAFTER CONVERSION TO RELATIVE" )
	#print_sensor( s1 )
	#print_sensor( s2 )
	#print_sensors_common_coords( s1, s2 )

	s2[ "relative" ] = pos
	#print_sensor( s2, debug = "full" )
	calculate_sensor( s2 )
	#print_sensor( s2, debug = "full" )

def check_intersect( s1, s2 ):
	print( "\ncheck_intersect:" )
	print( "  s1: {}, s2: {}".format( s1[ "name" ], s2[ "name" ] ) )

	s1_lines = set( s1[ "lines" ] )
	s2_lines = set( s2[ "lines" ] )

	intersecting_lines = sorted( s1_lines.intersection( s2_lines ) )
	print( "  number similar lines: {}".format( len( intersecting_lines ) ) )

	if len( intersecting_lines ) < 12:
		return

	length_1, length_2 = find_two_lines_common_point( s1, intersecting_lines )

	check_and_adjust_axis( s1, s2, length_1, length_2 )

def print_sensor( s, debug = "short" ):
	print( "{}".format( s[ "name" ] ) )
	print( "  coords:" )
	for i in s[ "coords" ][ s[ "coords" ][ :,0 ].argsort( ) ]:
		x, y, z = i
		print( "    {:>6}, {:>6}, {:>6}".format( x, y, z ) )

	if debug == "short":
		return

	print( "  lines:" )
	for i in sorted( s[ "lines" ] ):
		value = s[ "lines" ][ i ]
		print( "    {:<40} -> {}".format( str( value ), i ) )

def print_sensors_common_coords( s1, s2 ):
	print( "COMMON COORDS: {} & {}".format( s1[ "name" ], s2[ "name" ] ) )

	common = [ ]
	for i in s1[ "coords" ]:
		for j in s2[ "coords" ]:
			x1, y1, z1 = i
			x2, y2, z2 = j

			if x1 == x2 and y1 == y2 and z1 == z2:
				common.append( j )

	print( "  coords:" )
	for i in common:
		x, y, z = i
		print( "    {:>6}, {:>6}, {:>6}".format( x, y, z ) )

	

if __name__ == "__main__":
	sensors = get_input( args[ "input" ] )

	for i in sensors:
		calculate_sensor( i )

	print_sensor( sensors[ 0 ] )

	sensors[ 0 ][ "relative" ] = ( 0, 0, 0 )

	known_sensors   = [ ]
	unknown_sensors = [ ]
	known_sensors.append( sensors[ 0 ] )

	for i in sensors[ 1: ]:
		unknown_sensors.append( i )

	while True:
		print( "\n\nLOOP:" )
		
		print( "\nKNOWN SENSORS:" )
		for i in known_sensors:
			print( "  {}".format( i[ "name" ] ) )

		print( "\nUNKNOWN SENSORS:" )
		for i in unknown_sensors:
			print( "  {}".format( i[ "name" ] ) )

		print( "  len( unknown_sensors ): {}".format( len( unknown_sensors ) ) )
		if len( unknown_sensors ) == 0:
			break

		s2 = unknown_sensors.pop( 0 )
		print( "  selecting sensor s2: {}".format( s2[ "name" ] ) )

		for i in range( len( known_sensors ) ):
			s1 = known_sensors[ i ]
			check_intersect( s1, s2 )

			if "relative" in s2:
				known_sensors.append( s2 )
				break

		if not "relative" in s2:
			unknown_sensors.append( s2 )

	beacons = set( )
	for i in known_sensors:
		for j in i[ "coords" ]:
			x, y, z = j
			beacons.add( ( x, y, z )  )

	print( "\n\nNumber of beacons: {}".format( len( beacons ) ) )


