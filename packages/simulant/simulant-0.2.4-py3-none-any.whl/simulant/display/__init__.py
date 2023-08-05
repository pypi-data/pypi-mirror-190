from Xlib import display as disp
from Xlib import X
from PIL import Image


def display_handler(f):
    def wrapper(*args):
        try:
            return f(*args)
        finally:
            args[0]._dsp.close()

    return wrapper


class Display:
    @property
    def dsp(self):
        self._dsp = disp.Display()
        return self._dsp

    @property
    @display_handler
    def width(self):
        scr = self.dsp.screen()
        width = scr.width_in_pixels
        return width

    @property
    @display_handler
    def height(self):
        scr = self.dsp.screen()
        height = scr.height_in_pixels
        return height

    @display_handler
    def screenshot(self, width=None, height=None):
        image = None
        scr = self.dsp.screen()
        width = width if width else scr.width_in_pixels
        height = height if height else scr.height_in_pixels
        root = scr.root
        raw = root.get_image(0, 0, width, height, X.ZPixmap, 0xffffffff)
        image = Image.frombytes("RGB", (width, height), raw.data, "raw", "BGRX")
        return image
