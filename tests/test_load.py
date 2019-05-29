from spaghetti import load, register

@register
class Composite:
    def __init__(self, a, b):
        self.a = a
        self.b = b(-3, 2)

    def __call__(self, x):
        return self.b(self.a(x))

@register
class Linear:
    def __init__(self, w, b):
        self.w = w
        self.b = b

    def __call__(self, x):
        return self.w * x + self.b

if __name__ == "__main__":
    m = load("assets/test.yaml")
    print(m(2))
