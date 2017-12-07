# попиксельное сравнение - функция
import pyscreenshot as ImageGrab
import os
from time import clock, sleep
import time

x_pad = 0
y_pad = 0


def screenGrab():
    b1 = (x_pad + 1, y_pad + 1, x_pad + 64, y_pad + 48)
    im = ImageGrab.grab(b1)

    im.save(os.getcwd() + '\\Sna_pro_' + '.png', 'PNG')
    return im


def pix_to_pix(x, y, im1, im2):
    for i in range(0, x, 4):
        for k in range(0, y, 4):
            f_ = (i, k)
            p = im1.getpixel(f_)
            p2 = im2.getpixel(f_)
            if p == p2:
                print('x=', i, 'y=', k)
                if f_ == (x - 4, y - 4):
                    print('у картинок пикселы равны')
            else:
                print('пикселы не равны')
                break


if __name__ == "__main__":
    im1 = screenGrab()
    im2 = im1
    start1 = clock()
    pix_to_pix(64, 48, im1, im2)
    end1 = clock()
    # print(first_ten_even)
    print("Result (iterativ): выполняется за " + "\nФункция %1.10f секунд" % (end1 - start1))

    # f_ = (638, 478)
    # p=im1.getpixel(f_)
    # p2=im2.getpixel((638, 478))
    # if p==p2:
    #     print('пикселы равны')
    # else:
    #     print('пикселы не равны')