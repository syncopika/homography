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
    coords = []
    for c in contours:
        for contour in c:
            for coord in contour:
                #print(f"x:{coord[0]}, y:{coord[1]}")
                
                # gotta add z coord for 3d (e.g. use in blender)
                coords.append([int(coord[0]), int(coord[1]), 0])
                
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
    # explore with using RETR_EXTERNAL as well!
    contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnt = sorted(contours, key=cv2.contourArea, reverse=True)[0:5]
    
    output_contour_json(cnt)
    #print(cnt) # TODO: what does each contour value represent
    # https://docs.opencv.org/3.4/d9/d8b/tutorial_py_contours_hierarchy.html
    # https://stackoverflow.com/questions/30212713/get-coordinates-of-contours-in-opencv/30214930
    cv2.drawContours(canvas, cnt, -1, (0, 255, 255), 3)
    plot.title("contours")
    plot.imshow(canvas)
    plot.show()
    
    return canvas, cnt

# test.png has more rounded top corners while test2.png has sharper corners
image = cv2.imread("test_images/buildingedit.png")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

filtered_image = apply_filter(image)
threshold_image = apply_threshold(filtered_image)
detect_contour(threshold_image, image.shape)
