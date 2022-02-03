# following: https://blog.ekbana.com/skew-correction-using-corner-detectors-and-homography-fda345e42e65

import cv2
import numpy as np
import matplotlib.pyplot as plot

# test.png has more rounded top corners while test2.png has sharper corners
image = cv2.imread("test_images/buildingedit.png")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

SELECTED_CORNERS = []

def click(event):
    # TODO: show point clicked on image?
    SELECTED_CORNERS.append((event.x, event.y))
    
    # once 4 corners selected, close image
    if len(SELECTED_CORNERS) == 4:
        print(SELECTED_CORNERS)
        plot.close()

def collect_corners(image):
    height = image.shape[0]
    width = image.shape[1]
    
    fig, ax = plot.subplots()
    ax.imshow(image)
    
    ax.set_ylim([height, 0])
    ax.set_xlim([0, width])
    ax.set_title("select corners")
    
    cid = fig.canvas.mpl_connect('button_press_event', click)
    plot.show()
    
    
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
    width1 = int(np.sqrt((top_right[0] - top_left[0])**2 + (top_right[1] - top_left[1])**2))
    width2 = int(np.sqrt((bottom_right[0] - bottom_left[0])**2 + (bottom_right[1] - bottom_left[1])**2))
    width = max(width1, width2)
    
    height1 = int(np.sqrt((top_right[0] - bottom_right[0])**2 + (top_right[1] - bottom_right[1])**2))
    height2 = int(np.sqrt((top_left[0] - bottom_left[0])**2 + (top_left[1] - bottom_left[1])**2))
    height = max(height1, height2)
    
    destination_corners = np.float32([(0,0), (width-1, 0), (0, height-1), (width-1, height-1)])
    
    print("\nThe destination points are:\n")
    for idx, corner in enumerate(destination_corners):
        char = chr(65 + idx) + "'"
        print(f"{char}:{corner}")

    print(f"\nThe approximated height and width of the original image is: \n({height},{width})")

    return destination_corners, height, width
    
def unwarp(img, src, dst):
    """
        Unwarp an image
        
        args:
            img: np.array
            src: list
            dst: list
            
        return:
            np.array
    """
    height = img.shape[0]
    width = img.shape[1]
    
    matrix, _ = cv2.findHomography(src, dst, method=cv2.RANSAC, ransacReprojThreshold=3.0)
    print(f"\nThe homography matrix is: {matrix}\n")
    unwarped = cv2.warpPerspective(img, matrix, (width, height), flags=cv2.INTER_LINEAR)
    
    _, (ax1, ax2) = plot.subplots(1, 2)
    ax1.imshow(img)
    x = [src[0][0], src[2][0], src[3][0], src[1][0], src[0][0]]
    y = [src[0][1], src[2][1], src[3][1], src[1][1], src[0][1]]
    ax1.plot(x, y, color="yellow", linewidth=3)
    ax1.set_ylim([height, 0])
    ax1.set_xlim([0, width])
    ax1.set_title("targeted area in original image")
    ax2.imshow(unwarped)
    ax2.set_title("unwarped image")
    plot.show()
    
    return unwarped
    
def get_corners(image):
    """
        Using Shi-Tomasi algorithm for corner detection
    
        args:
            image = np.array
            
        return:
            list
    """
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    corners = cv2.goodFeaturesToTrack(gray, 4, 0.01, 10)
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
    
    dst_corners, h, w = get_destination_points(corners)
    
    unwarp(image, np.float32(corners), dst_corners)
    
    return corners

def apply_filter(image):
    """
        Create a 5 x 5 kernel and apply the filter to a grayscaled image
        The filter will blur the image
        
        args:
            image: np.array
            
        return:
            np.array
    """
    grayscale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    kernel = np.ones((5, 5), np.float32) / 15
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
    ret, thresh = cv2.threshold(filtered_img, 250, 255, cv2.THRESH_OTSU)
    plot.imshow(cv2.cvtColor(thresh, cv2.COLOR_BGR2RGB))
    plot.title("after applying Otsu threshold")
    plot.show()
    return thresh
    
def detect_contour(image, image_shape):
    """
        args:
            image: np.array
            image_shape: tuple
            
        return:
            np.array, list
    """
    canvas = np.zeros(image_shape, np.uint8)
    contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnt = sorted(contours, key=cv2.contourArea, reverse=True)[0]
    cv2.drawContours(canvas, cnt, -1, (0, 255, 255), 3)
    plot.title("largest contour")
    plot.imshow(canvas)
    plot.show()
    
    return canvas, cnt
    
def detect_corners_from_contour(canvas, contour, image):
    """
        detecting corner points from contours using cv2.approxPolyDP()
        
        args:
            canvas: np.array
            contour: list
            
        return:
            list
    """
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx_corners = cv2.approxPolyDP(contour, epsilon, True)
    cv2.drawContours(canvas, approx_corners, -1, (255, 255, 0), 10)
    approx_corners = [(438, 141), (1146, 54), (60, 884), (1565, 877)]#sorted(np.concatenate(approx_corners).tolist())
    print("\nThe corner points are ...\n")
    for index, corner in enumerate(approx_corners):
        char = chr(65 + index)
        print(f"{char}:{corner}")
        cv2.putText(canvas, char, tuple(corner), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    
    #approx_corners = [approx_corners[i] for i in [0, 2, 1, 3]]
    
    plot.imshow(canvas)
    plot.title("corner points")
    plot.show()
    
    return approx_corners
    
    
def better_skew_correction(image):
    filtered_image = apply_filter(image)
    threshold_image = apply_threshold(filtered_image)
    canvas, largest_contour = detect_contour(threshold_image, image.shape)
    corners = detect_corners_from_contour(canvas, largest_contour, image)
    destination_corners, height, width = get_destination_points(corners)
    #destination_corners = np.float32([(0,0), (image.shape[1]-1, 0), (0, image.shape[0]-1), (image.shape[1]-1, image.shape[0]-1)])
    unwarp(image, np.float32(corners), destination_corners)

#plot.imshow(image)
#plot.title("test image")
#plot.show()

#get_corners(image)

#better_skew_correction(image)

collect_corners(image)
