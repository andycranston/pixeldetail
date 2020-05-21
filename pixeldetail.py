#! /usr/bin/python3
#
# @(!--#) @(#) pixeldetail.py, version 007, 21-may-2020
#
# create a detailed version of a BMP/PNG/JPG file
#
# uses the Pillow library
#
#   pip install -U Pillow
#

#
# imports
#

import sys
import os
import argparse
from PIL import Image

##################################################################################

DEFAULT_MAGNIFY_WIDE = 48
DEFAULT_MAGNIFY_TALL = 48

MINIMUM_MAGNIFY_WIDE = 23
MINIMUM_MAGNIFY_TALL = 33

PADDING_WIDE = 4
PADDING_TALL = 4
PADDING_NEWLINE = 10

LINE_COLOUR = (128, 128, 128)

ALLOWABLE_FILE_EXTENSIONS = [ 'bmp', 'jpg', 'png' ]

DETAIL_EXTENSION = 'detail'

BACKGROUND = 128

##################################################################################

def charmap2vectorarray(charmap):
    varray = []
    
    linenum = 0
    for line in charmap:
        cnum = 0
        for c in line:
            if c == '#':
                varray.append((cnum, linenum))
            cnum += 1
        linenum += 1
    
    return varray

##################################################################################

def generatedigits():
    digits = {}
    
    digits['0'] = charmap2vectorarray([' ### ',
                                       '#   #',   
                                       '#   #',   
                                       '#   #',   
                                       '#   #',   
                                       '#   #',   
                                       ' ### '])

    digits['1'] = charmap2vectorarray(['  #  ',
                                       ' ##  ',   
                                       '# #  ',   
                                       '  #  ',   
                                       '  #  ',   
                                       '  #  ',   
                                       '#####'])
                                       
    digits['2'] = charmap2vectorarray([' ####',
                                       '#   #',   
                                       '    #',   
                                       ' ### ',   
                                       '#  ',   
                                       '#  ',   
                                       '#####'])
                                       
    digits['3'] = charmap2vectorarray(['#####',
                                       '    #',   
                                       '    #',   
                                       ' ###',   
                                       '    #',   
                                       '    #',   
                                       '#####'])
                                       
    digits['4'] = charmap2vectorarray(['   # ',
                                       '  ## ',   
                                       ' # # ',   
                                       '#  # ',   
                                       '#####',   
                                       '   # ',   
                                       '   # '])
                                       
    digits['5'] = charmap2vectorarray(['#####',
                                       '#    ',   
                                       '#    ',   
                                       '#### ',   
                                       '    #',   
                                       '    #',   
                                       '#### '])
                                       
    digits['6'] = charmap2vectorarray(['#####',
                                       '#    ',   
                                       '#    ',   
                                       '#####',   
                                       '#   #',   
                                       '#   #',   
                                       '#####'])
                                       
    digits['7'] = charmap2vectorarray(['#####',
                                       '    #',   
                                       '   # ',   
                                       '  #  ',   
                                       '  #  ',   
                                       '  #  ',   
                                       '  #  '])
                                       
    digits['8'] = charmap2vectorarray([' ### ',
                                       '#   #',   
                                       '#   #',   
                                       ' ### ',   
                                       '#   #',   
                                       '#   #',   
                                       ' ### '])
                                       
    digits['9'] = charmap2vectorarray(['#####',
                                       '#   #',   
                                       '#   #',   
                                       '#####',   
                                       '    #',   
                                       '    #',   
                                       '#####'])
                                       
    return digits
    
##################################################################################

def main():
    global progname
    
    parser = argparse.ArgumentParser()
        
    parser.add_argument('--wide',   help='width of detailed pixel box', type=int, default=DEFAULT_MAGNIFY_WIDE)
    parser.add_argument('--tall',   help='height of detailed pixel box', type=int, default=DEFAULT_MAGNIFY_TALL)
    parser.add_argument('filename', help='file name of BMP/PNG file')
    
    args = parser.parse_args()
    
    magnify_wide = args.wide
    
    if magnify_wide < MINIMUM_MAGNIFY_WIDE:
        print('{}: --wide command line argument too small - minimum value is {}'.format(progname, MINIMUM_MAGNIFY_WIDE), file=sys.stderr)
        return 1
    
    magnify_tall = args.tall
    
    if magnify_tall < MINIMUM_MAGNIFY_TALL:
        print('{}: --tall command line argument too small - minimum value is {}'.format(progname, MINIMUM_MAGNIFY_TALL), file=sys.stderr)
        return 1
    
    filename = args.filename
    
    if len(filename) < 5:
        print('{}: filename "{}" is too short'.format(progname, filename), file=sys.stderr)
        return 1
    
    fileextension = None
    for ft in ALLOWABLE_FILE_EXTENSIONS:
        if filename.lower().endswith('.' + ft):
            fileextension = ft
            break        
        
    if fileextension == None:
        print('{}: filename "{}" has an unsupported file type'.format(progname, filename), file=sys.stderr)
        return 1
    
    # read in image
    print('Reading image file "{}"'.format(filename))
    
    try:
        im = Image.open(filename)
    except FileNotFoundError:
        print('{}: cannot open filename "{}" for reading'.format(progname, filename), file=sys.stderr)
        return 1
    
    # create new image
    wide = (im.size[0] * (magnify_wide + 1)) + 1
    tall = (im.size[1] * (magnify_tall + 1)) + 1

    print('Creating new image of {} pixels'.format(wide * tall))
    
    detail = Image.new('RGB', (wide , tall), BACKGROUND)

    # copy the image
    print('Copying pixels to new image')
    
    for w in range(0, im.size[0]):
        for t in range(0, im.size[1]):
            pixel = im.getpixel((w, t))
            
            for ww in range(0, magnify_wide):
                for tt in range(0, magnify_tall):
                    detail.putpixel( ( (w * (magnify_wide + 1)) + ww + 1, (t * (magnify_tall + 1)) + tt + 1 ), pixel)
                    
    # draw horizontal lines
    print('Drawing horizontal separator lines')
    for w in range(0, wide):
        for t in range(0, tall + 1, magnify_tall + 1):
            detail.putpixel((w, t), LINE_COLOUR)
            
    # draw vertical lines
    print('Drawing vertical separator lines')
    for t in range(0, tall):
        for w in range(0, wide + 1, magnify_wide + 1):
            detail.putpixel((w, t), LINE_COLOUR)

    # copy in RGB values
    print('Putting RGB values into each pixel box')
    
    digits = generatedigits()

    for w in range(0, im.size[0]):
        for t in range(0, im.size[1]):
            pixel = im.getpixel((w, t))
            
            if ((pixel[0] + pixel[1] + pixel[2]) // 3) < 128:
                textcolour = (255, 255, 255)
            else:
                textcolour = (0, 0, 0)
            
            if (pixel != (0,0,0)) and (pixel != (255,255,255)):
                pcount = 0
                
                # if a greyscale colour reduce to one pixel
                if (pixel[0] == pixel[1]) and (pixel[1] == pixel[2]):
                    pixel = [pixel[0]]
                
                for p in pixel:
                    pstring = '{:03d}'.format(p)
    
                    wpos = (w * (magnify_wide + 1)) + PADDING_WIDE
                    tpos = (t * (magnify_tall + 1)) + PADDING_TALL + (pcount * PADDING_NEWLINE)
                    
                    for c in pstring:
                        for wt in digits[c]:
                            detail.putpixel((wpos + wt[0], tpos + wt[1]), textcolour)
                        wpos += 6
                        
                    pcount += 1
            
    im.close()
    
    detailfilename = filename[:-(len(fileextension)+1)] + '-' + DETAIL_EXTENSION + '.' + fileextension
    
    # save file
    print('Saving new image to file "{}"'.format(detailfilename))
    
    detail.save(detailfilename)

    print('Done')
    
    return 0

##################################################################################

progname = os.path.basename(sys.argv[0])

sys.exit(main())

# end of file
