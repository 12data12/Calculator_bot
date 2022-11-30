x = 0
y = 0
act = ''


def init(a, b, action):
    global x
    global y
    global act
    x = a
    y = b
    act = action


def do_it():
    if act == '+':
        return x + y
    if act == '-':
        return x - y
    if act == '*':
        return x * y
    if act == '/':
        try:
            return x / y
        except ZeroDivisionError:
            return 'Делить на ноль нельзя'
