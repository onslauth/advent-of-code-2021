import cv2
import glob

#fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', 'V')
fourcc = cv2.VideoWriter_fourcc( *"MP4V" )
(h, w) = cv2.imread(glob.glob("./images/*.jpg")[0]).shape[:2]

print( h, w )

fps = 10

out = cv2.VideoWriter('video.mp4', fourcc, fps, (w, h), isColor=True)

for img in sorted(glob.glob("./images/*.jpg")):
    img = cv2.imread(img)
    img = cv2.resize(img, (w, h))
    out.write(img)

out.release()
