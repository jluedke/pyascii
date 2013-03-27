#!/usr/bin/env python
import optparse
import time;
from PIL import Image

def convert_to_ascii(image, ascii_map=['.', '*', '#']):
    ascii_output = ''
    for y in range(0,image.size[1]):
        for x in range(0,image.size[0]):
            pixel = image.getpixel((x,y))
            level = int((pixel[0] + pixel[1] + pixel[2])/3)
            value = ((float(level)/255)*len(ascii_map)+.5)-1
            ascii_output += ascii_map[int(value)]
            # print pixel, level, value
        ascii_output += "\n";
    print ascii_output,

# TODO ther is a bug where if you put in an odd offset it will crash or 
# produce messed up results
def convert_to_ascii_2(image, ascii_map=['.', '*', '#']):
    ascii_output = ''
    pixels = image.tostring()
    print image.size
    for y in range(0,image.size[1]):
        for x in range(0,image.size[0]):
            offset = (x+y*image.size[1])*3
            pixel = pixels[offset:offset+3]
            level = (ord(pixel[0]) + ord(pixel[1]) + ord(pixel[2]))/3
            value = ((float(level)/255)*len(ascii_map)+.5)-1
            ascii_output += ascii_map[int(value)]
            # print pixel, level, value
        ascii_output += "\n";
    print ascii_output,


if __name__ == '__main__':
    usage = "usage: %prog [options] <image>"
    parser = optparse.OptionParser(usage=usage)

    parser.add_option('-w', '--width', metavar='STRING', type='int',
        help='specify the output width to use')

    parser.add_option('-H', '--height', metavar='STRING', type='int',
        help='specify the output height to use')

    parser.add_option('-m', '--ascii_map', metavar='STRING', type='string',
        help='character map used to map colors to')

    (options, args) = parser.parse_args()

    for image_name in args:
        image = Image.open(image_name)

        width = None
        height = None

        if options.width:
            width = options.width
        elif not options.width and options.height:
            width = int(float(options.height)/image.size[1]*image.size[0]*2)
        else:
            width = 72
            
        if options.height:
            height = options.height
        else:
            # scale based on image width
            height = int(image.size[1]*((float(width)/image.size[0])/2))
        ascii_map = [
            '.', ',', ';', '!', '|',
            '\'', ' ', '^', '~', '*', 
            'a', 'O', '0', '%', '#']
        if options.ascii_map:
            ascii_map = options.ascii_map[:]

        print width, height
        image = image.resize((int(width), int(height)))

        start = time.time()
        convert_to_ascii_2(image, ascii_map)
        print time.time() - start

   
