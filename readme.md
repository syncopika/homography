# homography    
learning about homography and fixing skewed images with OpenCV and matplotlib    
    
## motivation:    
I was looking at some buildings in London via Google Maps for some inspiration for buildings to model in Blender and while looking at them from the perspective of the Google car camera thought it would awesome if I could take a snapshot of the buildings and somehow create some automation to construct at least the face of them in 3D.    
    
The first step in doing so I thought would be to correct the perspective of the building images taken from Google Maps. With this code, the perspective correction isn't perfect but it does seem to work as it should (see example below).    
    
!(test_images/building.png)[original, skewed image] !(unwarped_image.png)[corrected image]    
    
This code allows a user to select 4 points that enclose the area of an image they wish to perform perspective correction on.    
    
## how to run:    
I recommend using miniconda. With miniconda installed you can run the following (assuming in the directory of this repo):    
```
> conda create --name homography opencv numpy matplotlib    
> conda activate homography    
> python homography.py    
```   
   
## example usage:    
!(example_usage.gif)[example usage gif]    
    
## next steps:    
Now we can get a mostly perspective-corrected image. With this image, I guess the next step would be to figure out how to create a 3D representation of it in Blender (just the face of the building of course). Is that particularly useful though? I dunno, maybe? But it would be neat I think. :)    
    