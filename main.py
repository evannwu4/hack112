#adapted from: https://www.pyimagesearch.com/2015/09/21/opencv-track-object-movement/

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32,
    help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "yellow"
# ball in the HSV color space
yellowLower = (25,50,50)
yellowUpper = (32,255,255)

# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
pts = deque(maxlen=args["buffer"])
counter = 0
(dX, dY) = (0, 0)
direction = ""
yValues = []
avg = 0
avgList = []
avgAvgs = 0
xValues = []
xAvg = 0

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])

# keep looping
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
        break

    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=800)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "yellow", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, yellowLower, yellowUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    #res = cv2.bitwise_and(frame, frame, mask=mask)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    center1 = None

    # only proceed if at least one contour was found
    if len(cnts) > 10:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        cnts = sorted(cnts, key=cv2.contourArea)
        #c = max(cnts, key=cv2.contourArea)

        c = cnts[-1]

        d = cnts[-2]


        ((x, y), radius) = cv2.minEnclosingCircle(c)
        ((x1, y1), radius1) = cv2.minEnclosingCircle(d)
        M = cv2.moments(c)
        M1 = cv2.moments(d)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        center1 = (int(M1["m10"] / M1["m00"]), int(M1["m01"] / M1["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > 20:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            pts.appendleft(center)

        if radius1 > 20:
            cv2.circle(frame, (int(x1), int(y1)), int(radius1),
                (0, 255, 255), 2)
            cv2.circle(frame, center1, 5, (0, 0, 255), -1)
            pts.appendleft(center1)

    dY = int(x1-x)
    #average last 30 y (or x, hmmm) values for overall dY
    yValues.append(dY)


    length = len(yValues)
    negCount = 0

    if length > 30:
        for i in range(length-1, length-30, -1):
            avg += yValues[i]

    avg = avg/30
    #avg last 10 avgs for overall direction (east/right or west/left)

    avgList.append(avg)

    avgLength = len(avgList)
    if avgLength > 10:
        for i in range(avgLength-1, avgLength-10, -1):
            avgAvgs += avgList[i]
    avgAvgs = avgAvgs/10

    if avgAvgs >= -25 and avgAvgs <= 25:
        dirY = "None"
    elif avgAvgs > 25:
        dirY = "West/Left" #"North"
    else:
        dirY = "East/Right" #"South"

    #output direction: for pygame(?)
    control = avg//70

    
    dX = int(x1-x)
    xValues.append(dX)

    lengthX = len(xValues)
    if lengthX > 10:
        for i in range(lengthX-1, lengthX-11, -1):
            xAvg += xValues[i]
    xAvg = xAvg/10

    speed = abs(xAvg//100)

    # show the movement deltas and the direction of movement on
    # the frame
    #shows direction of movement
    cv2.putText(frame, "dY: {}".format(dY), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0,0,255), 3)
    cv2.putText(frame, "Avg dY: {}".format(avg), (10,60), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255,0,0), 3)
    cv2.putText(frame, "Direction: {}".format(dirY), (10,90), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (100,100,0), 3)
    cv2.putText(frame, "OutPut {}".format(control), (10,120), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0,200,0), 3)
    cv2.putText(frame, "X [Faulty] Speed) {}".format(speed), (10,150), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0,100,10), 3)
                                                
    # show the frame to our screen and increment the frame counter
    cv2.imshow("Frame", frame)
    #cv2.imshow("mask", mask)
    #cv2.imshow('res', res)
    key = cv2.waitKey(1) & 0xFF
    counter += 1

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
