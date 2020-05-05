import numpy as np

def get_iter(c:complex, thresh:int =4, max_steps:int =25) -> int:
    # Z_(n) = (Z_(n-1))^2 + c
    # Z_(0) = c
    z=c
    i=1
    while i<max_steps and (z*z.conjugate()).real<thresh:
        z=z*z +c
        i+=1
    return i

def plotter(n, thresh, max_steps=25):
    mapper = lambda x,y: (4*(x-n//2)/n, 4*(y-n//2)/n)
    img=np.full((n,n), 255)
    x_lower = 0
    x_upper = 5*n//8
    y_lower = 2*n//10
    y_upper = 8*n//10
    for x in range(x_lower, x_upper):
        for y in range(y_lower, y_upper):
            it = get_iter(complex(*mapper(x,y)), thresh=thresh, max_steps=max_steps)
            img[y][x] = 255 - it
    return img[y_lower:y_upper, x_lower:x_upper]


def show(n, thresh, max_steps):
    img = plotter(n, thresh, max_steps)
    density = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'.  "
    s = ""
    density_mapper = lambda d: int(d*((len(density)/255)))
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            pixel=img[y][x]
            s += density[density_mapper(pixel)] * 2
        s += "\n"
    print(s)

show(n=90, thresh=4, max_steps=255)