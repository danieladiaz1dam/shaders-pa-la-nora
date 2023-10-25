input = "color 255 0 255 255"

def func(msg):
    shader = msg[0]
    (r, g, b, a) = ([int(x)/255 for x in msg[1:]])
    print(shader, r, g, b, a)

func(input.split(" "))