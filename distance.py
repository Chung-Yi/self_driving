# import the necessary packages
from imutils import paths
import numpy as np
import imutils
import cv2
from darkflow.net.build import TFNet
import time

options = {
    'model': 'cfg/tiny-yolo-voc-3c.cfg',
    'load': 1000,
    'threshold': 0.2
}

tfnet = TFNet(options)
colors = [tuple(255 * np.random.rand(3)) for _ in range(10)]

def find_marker(image):
	# convert the image to grayscale, blur it, and detect edges
	#print(image)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(gray, 35, 125)
    #cv2.imshow("image", image)



	# find the contours in the edged image and keep the largest one;
	# we'll assume that this is our piece of paper in the image
	cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	#print(cnts)
	#print(cv2.contourArea)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	c = max(cnts, key = cv2.contourArea)
	#print(c)

	# compute the bounding box of the of the paper region and return it
	return cv2.minAreaRect(c)

def distance_to_camera(knownWidth, focalLength, perWidth):
	# compute and return the distance from the maker to the camera
	return (knownWidth * focalLength) / perWidth

# initialize the known distance from the camera to the object, which
# in this case is 24 inches
KNOWN_DISTANCE = 24.0

# initialize the known object width, which in this case, the piece of
# paper is 12 inches wide
KNOWN_WIDTH = 11.0

# load the furst image that contains an object that is KNOWN TO BE 2 feet
# from our camera, then find the paper marker in the image, and initialize
# the focal length
video_capture = cv2.VideoCapture(0)
i = 1
while True:
    stime = time.time()
    ret, frame = video_capture.read()
    if ret:
        results = tfnet.return_predict(frame)
        for color, result in zip(colors,results):
            # print(result)
            tl = (result['topleft']['x'], result['topleft']['y'])
            br = (result['bottomright']['x'], result['bottomright']['y'])
            frame = cv2.rectangle(frame, tl, br, color, 5)
            #Get the detected object in the image
            frame1 = frame[result['topleft']['y']:result['bottomright']['y'],result['topleft']['x']:result['bottomright']['x']]
            # cv2.imshow('cropped',frame1)
            marker = find_marker(frame1)
            # print(marker)
            if i == 1:
                first_dis = marker[1][0]
                focalLength = (first_dis * KNOWN_DISTANCE) / KNOWN_WIDTH
                print("Got FocalLength")
                inches = distance_to_camera(KNOWN_WIDTH, focalLength, first_dis)
                i += 1
            else:
                other_dis = marker[1][0]
                inches = distance_to_camera(KNOWN_WIDTH, focalLength, other_dis)
            # print(label)
            print(inches)
            cv2.putText(frame, "%.2fft" % (inches / 12),(frame.shape[1] - 200, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,2.0, (0, 255, 0), 3)
    cv2.imshow("image", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
