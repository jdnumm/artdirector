#!/usr/bin/env python

import argparse

from PIL import (
        Image,
        ImageFilter,
        ImageFile
    )

class ArtDirector(object):
    def __init__(self):
        pass

    def load(self, filename):
        self.image = Image.open(filename)
        return self

    def save(self, filename):
        self.image.save(filename, optimize=True, quality=85, progressive=False)
        return self

    def get_pil_image(self):
        return self.image

    def crop(self, size, focus=None, zoom=0.0, edge=3.0):

        src_width, src_height = self.image.size
        dst_width, dst_height = size

        center_x = src_width/2
        center_y = src_height/2

        src_ratio = float(src_width) / float(src_height)
        ratio = float(dst_width) / float(dst_height)

        if ratio < src_ratio:
            crop_height = src_height
            crop_width = crop_height * ratio
            x_offset = float(src_width - crop_width) / 2
            y_offset = 0
        else:
            crop_width = src_width
            crop_height = crop_width / ratio
            x_offset = 0
            y_offset = float(src_height - crop_height) / 2

        crop_height = crop_height-crop_height*zoom
        crop_width = crop_width-crop_width*zoom

        if focus:
            focus_x, focus_y = focus
            x_end = x_offset+crop_width
            # Move crop window to the right
            while focus_x >= x_offset+crop_width/edge and x_offset+crop_width < src_width :
                x_offset = x_offset+1
            # Move crop window to the left
            while focus_x <= x_offset+crop_width/edge and x_offset > 0:
                x_offset = x_offset-1
            # Move crop window down
            while focus_y >= y_offset+crop_height/edge and y_offset+crop_height <= src_height :
                y_offset = y_offset+1
            # Move crop window up
            while focus_y <= y_offset+crop_height/edge and y_offset > 0:
                y_offset = y_offset-1


        self.image = self.image.crop((int(x_offset), int(y_offset), int(x_offset)+int(crop_width), int(y_offset)+int(crop_height)))
        self.image = self.image.resize(size, Image.Resampling.LANCZOS)

        return self

    def filter_blur(self, radius=5):
        self.image = self.image.filter(ImageFilter.GaussianBlur(radius=radius))
        return self

    def filter_bw(self):
        self.image = self.image.convert('L')
        return self


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', metavar='INPUT_FILE', help='Input image')
    parser.add_argument('outputfile', metavar='OUTPUT_FILE', help='Output image')
    parser.add_argument('--width', dest='width', type=int, default=100, help='Crop width')
    parser.add_argument('--height', dest='height', type=int, default=100, help='Crop height')
    parser.add_argument('--focus-x', dest='focus_x', default=None, type=int, help='Focal point ')
    parser.add_argument('--focus-y', dest='focus_y', default=None, type=int, help='Focal point')
    parser.add_argument('--zoom', dest='zoom', type=float, default=0.0, help='Zoom between 0.0 - 1.0 (0.0. Default)')
    parser.add_argument('--edge', dest='edge', type=float, default=3.0, help='Edge (size/n) around the focal target area')
    return parser.parse_args()

def main():
    args = parse_arguments()
    ad = ArtDirector()
    ad.load(args.inputfile)
    if args.focus_x != None and args.focus_y != None:
        ad.crop([args.width, args.height], focus=[args.focus_x, args.focus_y], zoom=args.zoom, edge=args.edge)
    else:
        ad.crop([args.width, args.height], zoom=args.zoom, edge=args.edge)

    ad.save(args.outputfile)

if __name__ == '__main__':
    main()
