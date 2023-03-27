# pile3

Python utility for simple image operations

* File formats: PNG, TIF, ...


# Examples


## Resizing image

```
pile3.py image.png --resize 200,400 -o resized.png
```


Help
----

Command line `--help` dumps more instructions:

```
Usage: usage: pile3.PY img [img2 ...] options 

positional arguments:
  <filename> [<filename>]
                        Input image file

optional arguments:
  -h, --help            show this help message and exit
  -o <file>, --output_filename <file>
                        write resulting image to file
  -I <index>, --interpolation <index>
                        Interpolation method, 1=bilinear etc, see PIL manual.
  -Q <x1,y1,...,x8,y8>, --quad <x1,y1,...,x8,y8>
                        Transform area of four cornerpoints to rectangle.
  -g <gamma-value>, --gamma <gamma-value>
                        Gamma correction.
  -r <a:b,a:b,...>, --rescale <a:b,a:b,...>
                        Rescale intensities x = a+bx.
  -m <x,y>, --remap <x,y>
                        Map intensity x to y.
  -c <dx,dy,width,height>, --crop <dx,dy,width,height>
                        Crop image
  -s <width [,height]>, --size <width [,height]>
                        Resize image
  -p <imagefile>, --palette <imagefile>
                        Apply palette
  -a <aspect_ratio>, --aspect_ratio <aspect_ratio>
                        For deriving image HEIGHT from WIDTH.
  -A <x1,x2>, --alpha <x1,x2>
                        Create alpha channel (polynomial).
  -f <r,g,b>, --fill <r,g,b>
                        Fill with color.
  -M <r,g,b>, --mask <r,g,b>
                        Use alpha as mask to mix image with a color.
  -R <degrees>, --rotate <degrees>
                        Rotate image
  -C <report-format>, --compare <report-format>
                        Compare two images
  -v <level>, --verbose <level>
                        Print status messages to stdout

 Examples:

``` 