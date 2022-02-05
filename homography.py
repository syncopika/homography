import cv2
import numpy as np
import matplotlib.pyplot as plot
from matplotlib.patches import Circle
from tutorial import get_destination_points, unwarp

# test.png has more rounded top corners while test2.png has sharper corners
image = cv2.imread("test_images/building.png")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

SELECTED_CORNERS = []

class CornerSelectImage:
    def __init__(self, image):
        self.fig, self.ax = plot.subplots()
        self.selected_corners = []
        self.ax.imshow(image)
        #height = image.shape[0]
        #width = image.shape[1]
        #self.ax.set_ylim([height, 0])
        #self.ax.set_xlim([0, width])
        self.ax.set_title("select corners")
        self.fig.canvas.mpl_connect('button_press_event', self._click)
        plot.show()
        
    def _click(self, event):
        self.selected_corners.append((event.xdata, event.ydata))
        self.ax.add_patch(Circle((event.xdata, event.ydata), radius=10, color='red'))
        self.fig.canvas.draw()
        
        # once 4 corners selected, close image
        if len(self.selected_corners) == 4:
            plot.close()


def collect_corners(image):
    corner_picker = CornerSelectImage(image)
    corners = corner_picker.selected_corners
    # we want to allow the user to select the corners in any order they want
    # but we need the corners to be in a particular order when we use them!
    # top left, top right, bottom left, bottom right
    
    # sort by y coord first
    corners.sort(key=lambda x: x[1])
    
    # then sort by x coord, but split so that we sort the top coords separately from the bottom coords
    corners = sorted(corners[:2], key=lambda x: x[0]) + sorted(corners[2:], key=lambda x: x[0])
    
    return corners
    
    
def skew_correction(image):
    # the general idea is: get the corners of the original, warped image.
    # then figure out what the corners should be if the image was unwarped based on the warped image dimensions.
    # then create a matrix to transform the warped image to the unwarped one and apply it.
    # choosing the corners yourself is better than trying to use a contour I think
    corners = collect_corners(image)
    destination_corners, height, width = get_destination_points(corners)
    unwarp(image, np.float32(corners), destination_corners)


skew_correction(image)

