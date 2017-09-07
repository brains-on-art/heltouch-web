import numpy as np
import cv2
import os


def process_img(imgfile):
    path = os.path.abspath(imgfile)
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    #print(image)

    mask = threshold(im)
    g,r,p = detect_points(image)
    dist = calculate_distance(r,p)
    
    return dist

green_filter = np.array([[30, 100, 150],
                         [50, 200, 255]])

purple_filter = np.array([[120, 50, 150],
                          [140, 255, 255]])

red_filter = np.array([[155, 60, 140],
                       [180, 255, 255]])
kernel = np.ones((3,3),np.uint8)

def threshold(im):
    im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    mask = np.zeros_like(im)
    mask[:,:,0] = cv2.inRange(im, 
                          green_filter[0], 
                          green_filter[1])
    mask[:,:,0] = cv2.dilate(mask[:,:,0], kernel)

    mask[:,:,1] = cv2.inRange(im, 
                          red_filter[0], 
                          red_filter[1])
    mask[:,:,1] = cv2.dilate(mask[:,:,1], kernel)

    mask[:,:,2] = cv2.inRange(im, 
                          purple_filter[0], 
                          purple_filter[1])
    mask[:,:,2] = cv2.dilate(mask[:,:,2], kernel)
    
    return mask

params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 0;
params.maxThreshold = 11;

# Filter by Area.
params.filterByArea = True
params.minArea = 400
params.maxArea = 1500
     
# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.5
params.maxCircularity = 1.0
     
# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.3
params.maxConvexity = 1.0
     
# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.5


#kernel = np.ones((3,3),np.uint8)
#reverse_mask = cv2.dilate(reverse_mask, kernel)
detector = cv2.SimpleBlobDetector_create(params)

def kpts_to_xy(keypoints):
    return np.array([[x.pt[0],x.pt[1]] for x in keypoints]) / [3280, 2464]

def get_corners(keypoints):
    coords = kpts_to_xy(keypoints)
    sorted_coords = np.full((4,2), np.nan)
    for (x,y) in coords:
        if x < 0.5 and y < 0.5:
            sorted_coords[0] = [x,y]
        elif x >= 0.5 and y < 0.5:
            sorted_coords[1] = [x,y]
        elif x >= 0.5 and y >= 0.5:
            sorted_coords[2] = [x,y]
        elif x < 0.5 and y >= 0.5:
            sorted_coords[3] = [x,y]
    return sorted_coords
    
def augment(x):
    return np.hstack([x, np.ones((x.shape[0],1))])

def get_transform(corner_keypoints):
    a = augment(get_corners(corner_keypoints))
    b = np.array([[0.0, 0.0, 1.0],
                  [1.0, 0.0, 1.0],
                  [1.0, 1.0, 1.0],
                  [0.0, 1.0, 1.0]])
    mask = ~np.isnan(a)[:,0]
    x,res,rank,s = np.linalg.lstsq(a[mask], b[mask])
    return x

def transform(keypoints, x):
    return np.matmul(augment(kpts_to_xy(keypoints)), x)[:,:2]

def detect_points(mask):
    kp = detector.detect(255-mask[:,:,0])
    x = get_transform(kp)
    
    green = transform(kp, x)
    
    kp = detector.detect(255-mask[:,:,1])
    red = transform(kp, x)
    
    kp = detector.detect(255-mask[:,:,2])
    purple = transform(kp, x)
    
    return green, red, purple

red_init = np.load('red_init.npy')
purple_init = np.load('purple_init.npy')

def calculate_distance(red, purple):
    dist = np.full((20, 28), np.nan)
    
    red_dist = cdist(red, red_init[:,:2])
    red_ind = red_init[red_dist.argmin(axis=0), 2:4].astype(int)
    red_dist = red_dist.min(axis=0)
    
    dist[red_ind[:,0], red_ind[:,1]] = red_dist
    
    purple_dist = cdist(purple, purple_init[:,:2])
    purple_ind = purple_init[purple_dist.argmin(axis=0), 2:4].astype(int)
    purple_dist = purple_dist.min(axis=0)
    
    dist[purple_ind[:,0], purple_ind[:,1]] = purple_dist
    
    return dist

