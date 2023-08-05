import re
from simulant.os import Shell


class Location(Shell):
    def __init__(self, window_id, x=None, y=None):
        self.window_id = window_id
        self._x = 0
        self._y = 0
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value


class Size(Shell):
    def __init__(self, window_id, width=None, height=None):
        self.window_id = window_id
        self._width = 0
        self._height = 0
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    def set(self, width, height):
        self.execute(f"xdotool windowsize {self.window_id} {width} {height}")


class Window(Shell):
    def __init__(self, class_name=None, location_x=None, location_y=None, width=None, height=None):
        if class_name is not None:
            self.id = self._id_by_class(class_name)
        self.focus()
        self.location = Location(self.id, location_x, location_y)
        self.size = Size(self.id, width, height)
        self._update_geometry()

    def is_focus(self):
        output = self.execute("xdotool getwindowfocus")
        return output == self.id

    def focus(self):
        self.execute(f"xdotool windowfocus {self.id}")

    def _id_by_class(self, class_name):
        return self.execute(f"xdotool search --classname --onlyvisible {class_name}")

    position_pattern = re.compile(r"^Position: (\d+),(\d+) \(screen: (\d+)\)$")
    geometry_pattern = re.compile(r"^Geometry: (\d+)x(\d+)$")

    def _update_geometry(self):
        output = self.execute(f"xdotool getwindowgeometry {self.id}")
        _, position, geometry = output.split('\n')
        position_result = re.search(self.position_pattern, position.strip())
        geometry_result = re.search(self.geometry_pattern, geometry.strip())
        self.screen = int(position_result.group(3))
        self.location.x = int(position_result.group(1))
        self.location.y = int(position_result.group(2))
        self.size.width = int(geometry_result.group(1))
        self.size.height = int(geometry_result.group(2))