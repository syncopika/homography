import cv2
import os
import json
import numpy as np
import matplotlib.pyplot as plot

def apply_filter(image):
    """
        Create a 5 x 5 kernel and apply the filter to a grayscaled image
        The filter will blur the image
        
        args:
            image: np.array
            
        return:
            np.array
    """
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    grayscale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    kernel = np.ones((5, 5), np.float32) / 30
    filtered = cv2.filter2D(grayscale, -1, kernel)
    plot.imshow(cv2.cvtColor(filtered, cv2.COLOR_BGR2RGB))
    plot.title("filtered image")
    plot.show()
    
    return filtered

def apply_threshold(filtered_img):
    """
        Apply Otsu threshold
        
        args:
            filtered_img: np.array
            
        return:
            np.array
    """
    ret, thresh = cv2.threshold(filtered_img, 254, 255, cv2.THRESH_OTSU)
    plot.imshow(cv2.cvtColor(thresh, cv2.COLOR_BGR2RGB))
    plot.title("after applying Otsu threshold")
    plot.show()
    return thresh    
    
def output_contour_json(contours):
    # https://stackoverflow.com/questions/32606743/how-to-access-opencv-contour-point-indexes-in-python
    coords = {}
    contour_coords = []
    contour_edges = []
    
    # this counter will help keep continuity when adding edge info
    # as we go through each separate contour since that info 
    # is supposed to use coordinate indexes
    curr_coord_count = 0
    
    for c in contours:
        # still confused a bit about how the contour data is organized...
        # it feels like there's an extra list depth?
        for idx, contour in enumerate(c):
            for coord in contour:
                # gotta add z coord for 3d (e.g. use in blender)
                contour_coords.append([int(coord[0]), int(coord[1]), 0])
                
                # also create edges by specifying the index of vertices that make an edge
                if idx < len(c) - 1:
                    contour_edges.append([curr_coord_count, curr_coord_count+1])
                
                curr_coord_count += 1
            
    coords["coords"] = contour_coords
    coords["edges"] = contour_edges
    
    with open("contours.json", "w") as f:
        json.dump(coords, f, indent=2)
    
def detect_contour(image, image_shape):
    """
        args:
            image: np.array
            image_shape: tuple
            
        return:
            np.array, list
    """
    canvas = np.zeros(image_shape, np.uint8)

    # https://docs.opencv.org/3.4/d9/d8b/tutorial_py_contours_hierarchy.html
    # https://stackoverflow.com/questions/30212713/get-coordinates-of-contours-in-opencv/30214930
    # explore with using RETR_EXTERNAL as well!
    contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    # the exact num of contours to collect will probably vary depending on image
    cnt = sorted(contours, key=cv2.contourArea, reverse=True)[0:8]
    
    output_contour_json(cnt)

    cv2.drawContours(canvas, cnt, -1, (0, 255, 255), 3)
    plot.title("contours")
    plot.imshow(canvas)
    plot.show()
    
    return canvas, cnt


image = cv2.imread("unwarped_image.png")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

filtered_image = apply_filter(image)
threshold_image = apply_threshold(filtered_image)
detect_contour(threshold_image, image.shape)
