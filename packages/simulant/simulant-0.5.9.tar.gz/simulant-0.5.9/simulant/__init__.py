import subprocess
import sys

from .display import Display
from .keyboard import Keyboard
from .keyboard.key import Keys
from .mouse import Mouse

__all__ = ['sm', 'keys']

keys = Keys()


class Simulant:
    def __init__(self):
        self.os = sys.platform
        self.keyboard = Keyboard()
        self.display = Display()
        self.mouse = Mouse()

    @staticmethod
    def get_clipboard():
        return subprocess.check_output(["xclip", "-o"]).decode('utf-8')

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"<Simulant: {self.os}>"


sm = Simulant()
