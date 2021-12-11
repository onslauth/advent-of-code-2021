import numpy as np
import cv2

o = cv2.imread( "octo-square.png" )

for i in range( 0, 10 ):

	b = o.astype( np.uint16 )
	b[ b > 0 ] += ( i * 5 )
	o = b.clip( 0, 255 ).astype( np.uint8 )

	cv2.imshow( "IMage", o )
	cv2.waitKey( 0 )






