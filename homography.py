# following: https://blog.ekbana.com/skew-correction-using-corner-detectors-and-homography-fda345e42e65

import cv2
import numpy as np
import matplotlib.pyplot as plot

# test.png has more rounded top corners while test2.png has sharper corners
image = cv2.imread("test_images/test2.png")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
def get_destination_points(corners):
    """
        Approximate height and width of rectangle if it was unwarped

        args:
            corners = list
        
        return:
            list (the destination corners), int (height), int (width)
    """
    top_left = corners[0]
    top_right = corners[1]
    bottom_left = corners[2]
    bottom_right = corners[3]
    
    # distance formula for calculating widths, heights
    width1 = int(np.sqrt((top_right[0] - top_left[0])**2 + (top_right[1] - top_left[1])))
    width2 = int(np.sqrt((bottom_right[0] - bottom_left[0])**2 + (bottom_right[1] - bottom_left[1])**2))
    width = max(width1, width2)
    
    height1 = int(np.sqrt((top_right[0] - bottom_right[0])**2 + (top_right[1] - bottom_right[1])))
    height2 = int(np.sqrt((top_left[0] - bottom_left[0])**2 + (top_left[1] - bottom_left[1])))
    height = max(height1, height2)
    
    destination_corners = np.float32([(0,0), (width-1, 0), (0, height-1), (width-1, height-1)])
    
    print("\nThe destination points are:\n")
    for idx, corner in enumerate(destination_corners):
        char = chr(65 + idx) + "'"
        print(f"{char}:{corner}")

    print(f"\nThe approximated height and width of the original image is: \n({height},{width})")

    return destination_corners, height, width
    
    
def get_corners(image):
    """
        Using Shi-Tomasi algorithm for corner detection
    
        args:
            image = np.array
            
        return:
            list
    """
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    corners = cv2.goodFeaturesToTrack(gray, 4, 0.01, 100)
    corners = np.int0(corners)
    corners = sorted(np.concatenate(corners).tolist())
    print("\nThe corner points are...\n")
    
    img = image.copy()
    for idx, corner in enumerate(corners):
        x, y = corner
        cv2.circle(img, (x, y), 3, 255, -1)
        char = chr(65 + idx)
        print(f"{char}:{corner}")
        cv2.putText(img, char, tuple(corner), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
     
    plot.imshow(img)
    plot.title("corner detection: Shi-Tomasi")
    plot.show()
    
    get_destination_points(corners)
    
    return corners

#plot.imshow(image)
#plot.title("test image")
#plot.show()

get_corners(image)