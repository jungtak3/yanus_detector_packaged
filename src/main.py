import cv2 as cv
import numpy as np
import os
import time
import pygame

try:
    from .window_capture import WindowCapture
except ImportError:
    from window_capture import WindowCapture

def main():
    # Define asset paths relative to the project root
    if __name__ == "__main__":
        # If run as a script, the assets are in the parent directory
        assets_dir = os.path.join(os.path.dirname(__file__), '..', 'assets')
    else:
        # If imported as a module, assets are relative to the package root
        assets_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')

    image_dir = os.path.join(assets_dir, 'images')
    sound_dir = os.path.join(assets_dir, 'sounds')

    # Initialize pygame mixer for sound playback
    pygame.mixer.init()

    # Load the target image to search for
    yanus_image_path = os.path.join(image_dir, 'yanus5_768.jpg')
    yanus_image = cv.imread(yanus_image_path, cv.IMREAD_UNCHANGED)

    if yanus_image is None or yanus_image.size == 0:
        print(f"Error: Could not load or read image {yanus_image_path}. Please ensure it's a valid image file.")
        exit()

    # Ensure yanus_image is grayscale and 8-bit for template matching
    if len(yanus_image.shape) == 3:
        yanus_image = cv.cvtColor(yanus_image, cv.COLOR_BGR2GRAY)
    yanus_image = np.array(yanus_image, dtype=np.uint8)
    print(f"Yanus image dimensions: {yanus_image.shape}")

    # Load the sound file
    yanus_sound_path = os.path.join(sound_dir, '야누스_5초.mp3') 
    yanus_sound = pygame.mixer.Sound(yanus_sound_path)

    # Load the portal image to search for
    portal_image_path = os.path.join(image_dir, 'portal_768.JPG')
    portal_image = cv.imread(portal_image_path, cv.IMREAD_UNCHANGED)

    if portal_image is None or portal_image.size == 0:
        print(f"Error: Could not load or read image {portal_image_path}. Please ensure it's a valid image file.")
        exit()

    # Ensure portal_image is grayscale and 8-bit for template matching
    if len(portal_image.shape) == 3:
        portal_image = cv.cvtColor(portal_image, cv.COLOR_BGR2GRAY)
    portal_image = np.array(portal_image, dtype=np.uint8)
    print(f"Portal image dimensions: {portal_image.shape}")

    # Load the portal sound file
    portal_sound_path = os.path.join(sound_dir, '아이유_포탈.mp3')
    portal_sound = pygame.mixer.Sound(portal_sound_path)

    # initialize the WindowCapture class
    wincap = WindowCapture('MapleStory')
    # wincap = WindowCapture(None) # For capturing the entire screen

    # Create the display window once
    WINDOW_TITLE = 'Screen Capture Feed'
    cv.namedWindow(WINDOW_TITLE, cv.WINDOW_NORMAL)

    loop_time = time.time()
    while(True):
        # get an updated image of the game
        screenshot = wincap.get_screenshot()

        current_frame_time = time.time()

        if screenshot is not None:
            # Calculate FPS based on successful frames
            fps = 1 / (current_frame_time - loop_time)
            loop_time = current_frame_time

            # Convert screenshot to grayscale for template matching
            screenshot_gray = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)

            # Perform image detection
            result = cv.matchTemplate(screenshot_gray, yanus_image, cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

            print(f"Max correlation value: {max_val}")

            threshold = 0.8
            if max_val >= threshold:
                # Image found, play sound
                if not pygame.mixer.get_busy():
                    yanus_sound.play()
                
                # Draw a rectangle around the detected image
                img_w = yanus_image.shape[1]
                img_h = yanus_image.shape[0]
                top_left = max_loc
                bottom_right = (top_left[0] + img_w, top_left[1] + img_h)
                cv.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)
                cv.putText(screenshot, 'Yanus Found!', (top_left[0], top_left[1] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


                # Draw a rectangle around the detected image
                img_w = yanus_image.shape[1]
                img_h = yanus_image.shape[0]
                top_left = max_loc
                bottom_right = (top_left[0] + img_w, top_left[1] + img_h)
                cv.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)
                cv.putText(screenshot, 'Yanus Found!', (top_left[0], top_left[1] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Perform portal image detection
            result_portal = cv.matchTemplate(screenshot_gray, portal_image, cv.TM_CCOEFF_NORMED)
            min_val_portal, max_val_portal, min_loc_portal, max_loc_portal = cv.minMaxLoc(result_portal)

            print(f"Max correlation value (Portal): {max_val_portal}")

            threshold_portal = 0.6
            if max_val_portal >= threshold_portal:
                # Portal image found, play sound and sleep
                if not pygame.mixer.get_busy():
                    portal_sound.play()
                    time.sleep(10) # Sleep for 10 seconds after playing the sound
                
                # Draw a rectangle around the detected portal image
                portal_img_w = portal_image.shape[1]
                portal_img_h = portal_image.shape[0]
                portal_top_left = max_loc_portal
                portal_bottom_right = (portal_top_left[0] + portal_img_w, portal_top_left[1] + portal_img_h)
                cv.rectangle(screenshot, portal_top_left, portal_bottom_right, (255, 0, 0), 2) # Red rectangle for portal
                cv.putText(screenshot, 'Portal Found!', (portal_top_left[0], portal_top_left[1] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)


            cv.putText(screenshot, f'FPS: {fps:.2f}', (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv.imshow(WINDOW_TITLE, screenshot)
        else:
            pass
            
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break

    print('Done.')

if __name__ == "__main__":
    main()
