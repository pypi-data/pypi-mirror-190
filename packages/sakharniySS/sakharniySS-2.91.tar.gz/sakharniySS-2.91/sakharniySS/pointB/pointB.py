class PointB:
    def __init__(self, x, y, z):
        self.Bx = x
        self.By = y
        self.Bz = z

    def print_point(self):
        print(f'X = {self.Bx}\nY = {self.By}\nZ = {self.Bz}')


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def print_point(self):
        print(f'X = {self.x}\nY = {self.y}')
