from simulant.display.window import Window
from simulant.os import Shell


class Screen(Shell):
    # todo singleton
    windows = []  # todo: xdotool get all windows

    def __init__(self, number):
        self.number = number
        self.focus_window = [window for window in self.windows if window.is_focus][0]  # todo change focus

    def get_window(self, class_name):
        window = Window(class_name=class_name)
        self.window.append(window)
        return window

    @staticmethod
    def is_select():  # todo check xdotool
        return True

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.number}>"

    def __repr__(self):
        return self.__str__()
