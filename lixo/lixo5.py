class P:

    def __init__(self, x, y):
        self.set_x(x)
        self.y = y

    @property
    def x(self):
        return self.__x

    def set_x(self, x):
        if x < 0:
            self.__x = 0
        elif x > 1000:
            self.__x = 1000
        else:
            self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, z):
        self.__y = -z

    def sum(self):
        print(self.x + self.y)


p = P(2, 3)
p.sum()

try:
    p.x = 678
except AttributeError as ae:
    print(f"PCR message {ae} for {p.x}")

p.x = 45
