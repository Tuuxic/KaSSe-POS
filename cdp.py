PORT = "/dev/ttyS3"

dev = open(PORT, "w")

EMPTY = "                  "

top_buffer = EMPTY
bottom_buffer = EMPTY


def left(text):
    while len(text) < 20:
        text += " "
    return text


def center(text):
    while len(text) < 20:
        if len(text) % 2 == 0:
            text = " " + text
        else:
            text += " "
    return text


def right(text):
    while len(text) < 20:
        text = " " + text
    return text


def merge(a, b):
    a = list(a)
    b = list(b)
    if len(a) > len(b):
        for i in range(len(b)):
            if a[i] == " ":
                a[i] = b[i]
        return "".join(a)
    else:
        for i in range(len(a)):
            if b[i] == " ":
                b[i] = a[i]
        return "".join(b)


def show(top, bottom):
    if top is None:
        top = EMPTY
    if bottom is None:
        bottom = EMPTY
    top = center(top)[:20]
    bottom = center(bottom)[:20]
    dev.write(("\f" + top + bottom + "\n"))
