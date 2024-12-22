#!/usr/bin/python
import argparse
import re

def parse(args):
    try:
        with open(args.file, 'r', encoding='utf-8') as gcode:
            gcodes = gcode.readlines()
    except IOError as i:
        print(f"bad file: {i}")
        raise i

  #start the file
  #print "p3,100"
  #print "c"

    xmin = 100000
    xmax = 0
    ymin = 100000
    ymax = 0

    startCode = re.compile(r"^G([01])(?: X(\S+))?(?: Y(\S+))?(?: Z(\S+))?$")
    contCode = re.compile(r"^(?: X(\S+))?(?: Y(\S+))?(?: Z(\S+))?$")
    #p = re.compile("G([01])(?= Z(\S+))")
    
    lastX = 0  # Added initialization
    lastY = 0  # Added initialization
    
    for line in gcodes:
        s = startCode.match(line)
        c = contCode.match(line)
        gcode = 0
        if s:
            gcode = s.group(1)
            x = s.group(2)
            y = s.group(3)
            z = float(s.group(4))
            if z > 0:
                #don't draw
                print("d0")
            else:
                #draw
                print("d1")
        elif c: 
            try:
                x = float(c.group(1))
            except (TypeError, ValueError):
                x = lastX 
            try:
                y = float(c.group(2))
            except (TypeError, ValueError):
                y = lastY
            #z = float(c.group(3))
            #print(line)
            outx = x * args.scale + args.xoffset
            outy = args.ysub - y * args.scale + args.yoffset
            print("g%d,%d" % (outx, outy))
            lastX = x
            lastY = y
            if outx < xmin:
                xmin = outx 
            if outx > xmax:
                xmax = outx
            if outy < ymin:
                ymin = outy
            if outy > ymax:
                ymax = outy

    print("# xmin %f xmax %f" % (xmin, xmax))
    print("# ymin %f ymax %f" % (ymin, ymax))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="preprocesses ngc files for polargraph robot")
    parser.add_argument('--file',
        action='store', dest='file', 
        help="file to open")
    parser.add_argument('--scale',
        action='store', dest='scale', type=float, default=6.3,
        help="scale factor")
    parser.add_argument('--ysub',
        action='store', dest='ysub', type=int, default=1000,
        help="need to reflect y axis atm, this is what the y is subtracted from")
    parser.add_argument('--yoffset',
        action='store', dest='yoffset', type=int, default=500,
        help="how far to move the file on y axis")
    parser.add_argument('--xoffset',
        action='store', dest='xoffset', type=int, default=1000,
        help="how far to move the file on x axis")
    """
    parser.add_argument('--stoneCutLength',
        action='store', dest='stoneCutLength', type=int, default=280,
        help="mm long side of material to cut the stones from")
    parser.add_argument('--drawSizeLine',
        action='store_const', const=True, dest='drawSizeLine', default=False,
    """
    args = parser.parse_args()

    #set values, must be a better way of doing this
    parse(args)
