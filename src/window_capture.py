import numpy as np
import win32gui, win32ui, win32con
import cv2 as cv
import mss

class WindowCapture:

    # properties
    w = 0
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0


    # constructor
    def __init__(self, window_name=None):
        # find the handle for the window we want to capture.
        # if no window name is given, capture the entire screen
        if window_name is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception('Window not found: {}'.format(window_name))

        self.screen = mss.mss()
        self.is_desktop_window = (self.hwnd == win32gui.GetDesktopWindow())
        
        # Initialize properties that will be set in get_screenshot
        self.w = 0
        self.h = 0
        self.cropped_x = 0
        self.cropped_y = 0
        self.offset_x = 0
        self.offset_y = 0

    def get_screenshot(self):
        if not win32gui.IsWindow(self.hwnd):
            # print(f"Window {self.hwnd} is not a valid window.")
            return None
        if win32gui.IsIconic(self.hwnd):
            # print(f"Window {self.hwnd} is minimized.")
            return None

        # Get the window rectangle each time to update position
        window_rect = win32gui.GetWindowRect(self.hwnd)
        _full_w = window_rect[2] - window_rect[0]
        _full_h = window_rect[3] - window_rect[1]

        if self.is_desktop_window:
            border_pixels = 0
            titlebar_pixels = 0
        else:
            # Estimates for border and title bar
            border_pixels = 8
            titlebar_pixels = 30
        
        self.w = _full_w - (border_pixels * 2)
        self.h = _full_h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels
        
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

        # Ensure width and height are positive for mss
        self.w = max(1, self.w)
        self.h = max(1, self.h)

        mon = {"top": self.offset_y, "left": self.offset_x, "width": self.w, "height": self.h}
        
        try:
            sct_img = self.screen.grab(mon)
        except mss.exception.ScreenShotError as e:
            # print(f"MSS ScreenShotError: {e}. Mon: {mon}")
            return None
        
        # Convert to a NumPy array
        img = np.array(sct_img)
       
        return img

    # find the name of the window you're interested in.
    # once you have it, update window_capture()
    # https://stackoverflow.com/questions/55547940/how-to-get-a-list-of-the-name-of-every-open-window
    @staticmethod
    def list_window_names():
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)

    # translate a pixel position on a screenshot image to a pixel position on the screen.
    # pos = (x, y)
    # WARNING: if you move the window being captured after execution is started, this will
    # return incorrect coordinates, because the window position is only calculated in
    # the __init__ constructor.
    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)