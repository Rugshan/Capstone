# Imports
import cv2
import os
from datetime import datetime

from cv2 import destroyWindow

def save_photo():

    # Initialize Camera
    cam = cv2.VideoCapture(0) # Assign the correct camera index here.
    print('Camera On')

    # Get Date-Time
    now = datetime.now()
    file_name_path = now.strftime("./saved_images/%Y%m%d_%H%M%S.png")

    # Read Input
    result, image = cam.read()

    # Image Detected
    if result:
        
        print('Taking photo, say cheese!')

        # # Show Result (FrameName, Image)
        # cv2.imshow("Selfie", image)

        # Create Directory
        if not os.path.isdir('saved_images'):
                os.mkdir('saved_images')
        
        # Save Locally (Path, Image)
        cv2.imwrite(file_name_path, image)
        print('Saved image at: ' + file_name_path)

        # # Keyboard Interrupt
        # cv2.waitKey(0)
        # destroyWindow("Selfie")

    # Image Not Detected
    else:
        print('Error, image not detected.')

    cam.release()
    print('Camera Off')

save_photo()


