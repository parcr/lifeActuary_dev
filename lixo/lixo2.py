class P:

    def __init__(self, x):
        self.x = x

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x


p1 = P(42)
p2 = P(4711)
print(p1.get_x())

p1.set_x(47)
p1.set_x(p1.get_x() + p2.get_x())
print(p1.get_x())

p1.set_x(47)
p1.x = p1.x + p2.x
print(p1.x)
