#!/usr/bin/python
"""
Python image processing based utility.
Enter 'pile3.py -help' for help.

Markus.Peura@fmi.fi
2006 - 2023 (c) Finnish Meteorological Institute
"""

#import Image
from PIL import Image
import os   # for environment variables 
import sys  # for command-line arguments
import math # for gamma correction
from argparse import ArgumentParser
import numpy as np

import logging
# logging.basicConfig(format='%(levelname)s\t %(name)s: %(message)s')
logging.basicConfig(format='%(levelname)s:\t %(message)s')


# os.environ["http_proxy"]="" #
parser = ArgumentParser(usage="usage: %(prog)s img [img2 ...] options ")

parser.add_argument("IMAGE", nargs='*', 
    help="Input image file",
    metavar="<filename> [<filename>]")


parser.add_argument("-o", "--output_filename", 
    dest="OUTPUT_FILENAME",
    help="write resulting image to file", 
    metavar="<file>")

#                  default="test.jpg",

parser.add_argument("-I", "--interpolation", 
    dest="INTERPOLATION",
    default=Image.ANTIALIAS,
    help="Interpolation method, 1=bilinear etc, see PIL manual. ", 
    metavar="<index>")

parser.add_argument("-Q", "--quad", 
    dest="QUAD",
    help="Transform area of four cornerpoints to rectangle.", 
    metavar="<x1,y1,...,x8,y8>")

parser.add_argument("-g", "--gamma", dest="GAMMA",
    help="Gamma correction.", 
    metavar="<gamma-value>")

parser.add_argument("-r", "--rescale", 
    dest="RESCALE",
    help="Rescale intensities x = a+bx.", 
    metavar="<a:b,a:b,...>")

parser.add_argument("-m", "--remap", 
    dest="REMAP",
    help="Map intensity x to y.", 
    metavar="<x,y>")

parser.add_argument("-c", "--crop", 
    dest="CROP",
    help="Crop image", 
    metavar="<dx,dy,width,height>")

parser.add_argument("-s", "--size", 
    dest="SIZE",
    help="Resize image", 
    metavar="<width [,height]>")


parser.add_argument("-p", "--palette", 
    dest="PALETTE",
    help="Apply palette", 
    metavar="<imagefile>")

# NEW
#parser.add_argument("-w", "--width", dest="WIDTH",
#                  help="Resize image width", metavar="width")

# NEW
parser.add_argument("-a", "--aspect_ratio", 
    dest="ASPECT_RATIO",
    default = 1.0,
    type = float,
    help="For deriving image HEIGHT from WIDTH.", 
    metavar="<aspect_ratio>")

parser.add_argument("-A", "--alpha", 
    dest="ALPHA",
    help="Create alpha channel (polynomial).", 
    metavar="<x1,x2>")

#parser.add_argument("-T", "--alphafile", dest="ALPHAFILE",
#                  help="Create alpha channel (polynomial).", metavar="<x1,x2>")

parser.add_argument("-f", "--fill", 
    dest="FILL",
    help="Fill with color.",
    metavar="<r,g,b>") 
    #type="int"

parser.add_argument("-M", "--mask", 
    dest="MASK",
    help="Use alpha as mask to mix image with a color.",
    metavar="<r,g,b>") 


parser.add_argument("-R", "--rotate", dest="ROTATE",
                  help="Rotate image", metavar="<degrees>")


parser.add_argument("-C", "--compare", 
    type=str,
    dest="COMPARE", 
    default="", 
    metavar="<report-format>",
    help="Compare two images")


# Change this...
parser.add_argument("-v", "--verbose", 
    type=str,
    dest="VERBOSE", 
    default="INFO", 
    metavar="<level>",
    help="Print status messages to stdout")
#                  action="store_false", dest="verbose", default=True,



if __name__ == '__main__':

    options = parser.parse_args()
    

    logger = logging.getLogger(__name__)
    logger.setLevel(30)

    if (options.VERBOSE):
        options.LOG_LEVEL = "DEBUG"
        #if (options.LOG_LEVEL):
        if hasattr(logging, options.VERBOSE):
            logger.setLevel(getattr(logging, options.VERBOSE))
        else:
            logger.setLevel(int(options.VERBOSE))
            
            logger.debug(options)   
            
            
            
    image_count = len(options.IMAGE)
            
    if image_count == 0:
        parser.print_help()
        print ("\n Examples:\n")
        print (" alpha.png --alpha 255,-1 --fill 255,128,0   # Creates orange image")
        exit

                
                
    # Global switch
    interpolation = int( options.INTERPOLATION )
                
    # Image list.
    Im = []
    
    # The bounding box of the first image loaded.
    Bbox=()

    # Load images, ensuring same size with the first image.
    for i in range( image_count ):
        logger.info('Loading image %s', options.IMAGE[i])
        if ((image_count < 3) and (i==0)) or options.COMPARE:
            Im.append( Image.open( options.IMAGE[i] ))
        else:
            Im.append( Image.open( options.IMAGE[i] ).convert('L') )
            #    Im.append( Image.open( args[i] ).split() )
        if Bbox == ():
            Bbox = Im[i].size 
        elif not options.COMPARE: # TODO: Resize only when needed
            Im[i] = Im[i].resize( Bbox, interpolation )

            
    if options.COMPARE:
        if (image_count != 2):
            logger.error('Comparing applicable for 2 images, but loaded %d', image_count)
            exit(1)
        data1 = np.array(Im[0])
        #logger.info(data1)
        data2 = np.array(Im[1])
        #logger.info(data2)
        if (data1.dtype != data2.dtype):
            logger.error('Mode: %s != %s', data1.dtype, data2.dtype)
            exit(2)
        if (data1.shape != data2.shape):
            logger.error('Size: %s != %s', data1.shape, data2.shape)
            exit(3)

        #Image.fromarray(data1).convert('L').save("array1.png")
        #Image.fromarray(data2).convert('L').save("array2.png")
        d  = (data1-data2)
        d_stddev = np.std(d)
        if (d_stddev == 0.0):
            logger.info('Diff.std: 0')
        elif (d_stddev < 1.0):
            logger.info('Diff.std: %d', d_stddev)
        elif (d_stddev < 10.0):
            logger.warn('Diff.std: %d', d_stddev)
        else:
            logger.error('Diff.std: %d', d_stddev)
            #exit(4)
            
        if (options.OUTPUT_FILENAME):
            im = Image.fromarray(d).convert('L')
        logger.debug("Test ended")

    #logger.warn("Test ended")


    GAMMA=()
    if options.GAMMA:
        GAMMA=options.GAMMA.split(",")
        for i in range( len(GAMMA) ):
            if i < image_count:
                
                g = float(GAMMA[i])
                
                # If negative, invert first.
                if (g < 0):
                    Im[i] = Im[i].point(lambda x: 255 - x)
                    
                # Then, apply gamma correction.
                g = abs(g)
                if (g != 1.0) and (g != 0.0):
                    logger.info('Gamma correcting image %d %s ',i, options.IMAGE[i])
                    Im[i] = Im[i].point(lambda x: 255.0*math.pow(x/255.0,1.0/g) )
                

    # todo: check with ALPHA
    RESCALE=()
    if options.RESCALE:
        RESCALE = options.RESCALE.split(",")
        for i in range( len(RESCALE) ):
            if i < image_count:

                r = RESCALE[i].split(":")
                a = float(r[0])
                b = float(r[1])

                if (a > 0) | (b != 1):
                    Im[i] = Im[i].point(lambda x: a + b*float(x))


    logger.info('image_count: %d', image_count)

    if image_count == 1:
        im = Im.pop().convert("RGBA")
        #im = Im[0]

    if (image_count == 2) and not options.COMPARE:
        # pick reference to alpha
        alpha = Im.pop()
        logger.info('adding alpha channel: %s', alpha)
        #    if options.verbose:
        #        print 'Read alpha ', alpha
        im = Im.pop().convert("RGB")
        im.putalpha(alpha)
        #    if options.verbose:
        #        print 'Composed RGBA image ', im

    if image_count == 3:
        im = Image.merge("RGB", Im )

    if image_count == 4:
        im  = Image.merge("RGBA", Im )


    REMAP = ()
    if options.REMAP:
        REMAP = options.REMAP.split(',')
        if (len(REMAP) == 2):
            x = int(REMAP[0])
            y = int(REMAP[1])
            im = im.point(lambda i: (i==x) * y + (i!=x)*i )
        

    if options.CROP:
        CROP = options.CROP.split(',')
        if ( CROP ):
            for i in range(len(CROP)):
                CROP[i] = int( CROP[i] )
                CROP[2] += CROP[0]
                CROP[3] += CROP[1]
                print (CROP)
                im = im.crop( CROP )
                # Can be further resized, see below.



    if options.SIZE:
        SIZE = options.SIZE.split(',')
        if (len(SIZE) == 2):
            SIZE = ( int(SIZE[0]), int(SIZE[1]) )
        else:
            SIZE = ( int(SIZE[0]), int(int(SIZE[0])*float(options.ASPECT_RATIO)) )
    else:
        SIZE = Bbox
    # Resizing is finally carried out in transform() or resize(), see below.


    if options.QUAD:
        QUAD = options.QUAD.split(',')
        if (QUAD):
            for i in range(len(QUAD)):
                QUAD[i] = int( QUAD[i] )
                # PIL 1.1.3 Limitation (take second best then):
            if interpolation == Image.ANTIALIAS:
                im = im.transform( SIZE, Image.QUAD, QUAD, Image.BICUBIC ) 
            else:
                im = im.transform( SIZE, Image.QUAD, QUAD, interpolation ) 
    else:
        if options.SIZE:
            im = im.resize( SIZE, interpolation ) 


    # Move up?
    if options.ROTATE:
        # Future extension (interpolation as a second argument)
        #    ROTATE = options.ROTATE.split(',')
        #if (options.ROTATE):
        angle = int( options.ROTATE )
        # Future extension     
        #        if len(ROTATE) == 2:
        #            interpolation = int(ROTATE[1])
        #        else:
        #            interpolation = Image.ANTIALIAS
        im = im.rotate( angle , interpolation )


    # See below
    if options.ALPHA:
        gray = im.convert('L')

    #gray = im.convert('L')

    # not sure if correct place here
    if options.PALETTE:
        palette = Image.open(options.PALETTE).convert("RGB")
        if (palette.size[0] > palette.size[1]):
            palette = palette.resize((256,1))
        else :
            palette = palette.resize((1,256))

        palette = list(palette.getdata())
        palette2 = []
        for i in range( len(palette) ):
            palette2.extend(palette[i])
        # NEW        
        im = im.convert('L')
        im.putpalette(palette2)

    # change later? NOtice im[0]
    ALPHA=()
    if options.ALPHA:
        ALPHA = options.ALPHA.split(',')
        a0 = float(ALPHA[0])
        a1 = float(ALPHA[1])
        #gray = im.convert('L')
        alpha = gray.point(lambda i: a0 + a1*i )
        im.putalpha(alpha)

    # See below
    if options.FILL:
        c = options.FILL.split(',')
        c = (int(c[0]),int(c[1]),int(c[2]))
        if im.size > 0:
            im.paste(c)
        if (alpha):
            im.putalpha(alpha)

    if options.MASK:
        c = options.MASK.split(',')
        #print col1
        base1 = Image.new('RGB', im.size, (int(c[0]),int(c[1]),int(c[2])))
        base2 = Image.new('RGB', im.size, (int(c[3]),int(c[4]),int(c[5])))
        im = Image.composite(base1,base2,im.convert('L'))
        #    im.composite(im,im,im)
    

    if options.OUTPUT_FILENAME:
        im.save(options.OUTPUT_FILENAME)





