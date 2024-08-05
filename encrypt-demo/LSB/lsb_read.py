#! -*-conding: UTF-8 -*-
# @公众号: 海哥python

from PIL import Image


def mod(x, y):
    return x % y


def extract_text(img_path):
    im = Image.open(img_path)

    width = im.size[0]
    height = im.size[1]
    key = ""
    binstr = ""

    for h in range(height):
        for w in range(width):
            pixel = im.getpixel((w, h))
            a = pixel[0]
            b = pixel[1]
            c = pixel[2]

            binstr += str(mod(a, 2))
            if len(binstr) == 8:
                char = chr(int(binstr, 2))
                if char == '\x00':
                    return key
                key += char
                binstr = ""

            binstr += str(mod(b, 2))
            if len(binstr) == 8:
                char = chr(int(binstr, 2))
                if char == '\x00':
                    return key
                key += char
                binstr = ""

            binstr += str(mod(c, 2))
            if len(binstr) == 8:
                char = chr(int(binstr, 2))
                if char == '\x00':
                    return key
                key += char
                binstr = ""

    return key


if __name__ == '__main__':
    extracted_text = extract_text("fat2.png")
    print("Extracted text:", extracted_text)

