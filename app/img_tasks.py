import numpy as np
import cv2
import os


def read_img_detect_circles(imgfile):
    path = os.path.abspath(imgfile)
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    #print(image)

    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.minThreshold = 0;
    params.maxThreshold = 11;

    # Filter by Area.
    params.filterByArea = True
    params.minArea = 300

    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.3
    params.maxCircularity = 1.0

    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.3
    params.maxConvexity = 1.0

    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.5

    detector = cv2.SimpleBlobDetector_create(params)


    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_image,
                       np.array([172-30, 115-50, 0]),
                       np.array([172+30, 115+50, 255]))
    reverse_mask = 255-mask
    #kernel = np.ones((3,3),np.uint8)
    #reverse_mask = cv2.dilate(reverse_mask, kernel)

    points = detector.detect(reverse_mask)
    # print(points)
    return points
