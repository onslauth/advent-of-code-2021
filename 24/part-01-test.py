
W = [ 9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9  ]

# Part 1 solution
#W = [ 3, 9, 4, 9, 4, 1, 9, 5, 7, 9, 9, 9, 7, 9 ]

# Part 2 solution
#W = [ 1, 3, 1, 6, 1, 1, 5, 1, 1, 3, 9, 6, 1, 7 ]

X = [ 13, 15, 15, 11, -7, 10, 10, -5, 15, -3, 0,  -5, -9, 0  ]
Y = [ 6,  7,  10, 2,  15, 8,  1,  10, 5,  3,  5,  11, 12, 10 ]
Z = [ 1,  1,  1,  1,  26, 1,  1,  26, 1,  26, 26, 26, 26, 26 ]

x = 0
y = 0
z = 0

for i in range( 14 ):
	w = W[ i ]

	x = z % 26
	x_rem = x
	z //= Z[ i ]
	x += X[ i ]

	mod_x = x

	if W[ i ] == x:
		x = 0
	else:
		x = 1

	if x == 0:
		z *= 1
	else:
		z *= 26

	if x == 1:
		addition = W[ i ] + Y[ i ]  
		z += addition

	print( "{:>2}: Z[ i ]: {:>2}, x_rem: {:>2}, X[ i ]: {:>2}, mod_x: {:>2}, W[ i ]: {:>2}, x: {:>2}, Y[ i ] + W[ i ]: {}, z: {:>2}".format( i, Z[ i ], x_rem, X[ i ], mod_x, W[ i ], x, addition, z ) )


print( "".join( [ str( x ) for x in W ] ) )
