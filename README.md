# Art directed Image cropping

Art direction sets a focal point and can be used when you need multiple copies of the same Image but also in in different proportions.

## Installation

    pip3 install artdirection

## Usage

Use it as a command-line tool:


```
$ artdirector --help
usage: artdirector [-h] [--width WIDTH] [--height HEIGHT] [--focus-x FOCUS_X] [--focus-y FOCUS_Y] [--zoom ZOOM]
                      INPUT_FILE OUTPUT_FILE

positional arguments:
  INPUT_FILE         Input image
  OUTPUT_FILE        Output image

options:
  -h, --help         show this help message and exit
  --width WIDTH      Crop width
  --height HEIGHT    Crop height
  --focus-x FOCUS_X  Crop height
  --focus-y FOCUS_Y  Crop height
  --zoom ZOOM        Crop height
```

Processing an image:

```
artdirector --width 300 --height 300 input.jpg output.jpg
```

Or use it as a module


```
from artdirector import ArtDirector

ad = ArtDirector()
ad.load('input.jpg')
ad.crop([400, 400], focus=[600, 300], zoom=0.3)
ad.output('input.jpg')
```
