import win32gui
import win32api
import win32con
import numpy as np
from time import sleep
from win32gui import GetWindowRect

class Control():
    def __init__(self, handle):
        self.handle = handle

        def get_window_location():
            rect = GetWindowRect(self.handle)
            x = rect[0]
            y = rect[1]

            return x, y

        self.window_location = get_window_location()
    
    def click(self, x, y):
        lParam = win32api.MAKELONG(x, y)
        win32gui.SendMessage(self.handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam) 
        win32gui.SendMessage(self.handle, win32con.WM_LBUTTONUP, 0, lParam)
        sleep(0.1)

    def drag(self, x1, y1, x2, y2):
        lParam1 = win32api.MAKELONG(x1, y1)
        lParam2 = win32api.MAKELONG(x2, y2)
        win32gui.SendMessage(self.handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam1)
        delta = np.array([x2-x1, y2-y1])
        len = np.linalg.norm(delta)
        step_size = 20
        delta = (delta/len) * step_size
        for i in range(int(len / step_size)):
            pos = (delta * i + np.array([x1, y1])).astype(int)
            pos = win32api.MAKELONG(pos[0], pos[1])
            win32gui.SendMessage(self.handle, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, pos)
            sleep(0.04)
        win32gui.SendMessage(self.handle, win32con.WM_LBUTTONUP, 0, lParam2)
        sleep(0.1)

    def scroll(self, distance, x, y, control=False, shift=False):
        if shift and control:
            print("Error: can't hold down shift and control")
            return
        button = 0
        if control:
            button = win32con.MK_CONTROL
        elif shift:
            button = win32con.MK_SHIFT
        wParam = win32api.MAKELONG(button, 120*np.sign(distance))
        x += self.window_location[0]
        y += self.window_location[1]
        lParam = win32api.MAKELONG(x, y)
        for i in range(abs(distance)):
            win32gui.SendMessage(self.handle, win32con.WM_MOUSEWHEEL, wParam, lParam)
            sleep(.3)

    def keydown(self, key):
        if type(key) == type('a'):
            win32gui.SendMessage(self.handle, win32con.WM_KEYDOWN, ord(key), 0)
        else:
            print("Error: input not a key")

    def keyup(self, key):
        if type(key) == type('a'):
            win32gui.SendMessage(self.handle, win32con.WM_UP, ord(key), 0)
        else:
            print("Error: input not a key")