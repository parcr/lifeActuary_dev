class P:

    def __init__(self, x):
        self.x = x

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        if x < 0:
            self.__x = 0
        elif x > 1000:
            self.__x = 1000
        else:
            self.__x = x


p1 = P(42)
p2 = P(4711)
print(p1.x)
print(p2.x)

p1.x = 47
p1.x = (p1.x + p2.x)
print(p1.x)

p1.__setattr__('x', 47)
p1.x = p1.x + p2.x
print(p1.x)
