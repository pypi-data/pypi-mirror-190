# PyFITSRotate

## Description
A simple Python script to rotate FITS cube axes. It uses the [astropy](http://www.astropy.org/) package to read and write FITS files.

The default action is to rotate the spectral axis to be the first axis. This is useful for heavy IO operations on FITS cubes/

## Installation
From github:
```
pip install git+git://github.com/alecthomson/pyfitsrotate.git
```
From PyPI:
```
pip install pyfitsrotate
```

## Usage
```
❯ fitsrotate -h
usage: fitsrotate [-h] [-o [OUTFILE]] [-e EXT] [-s SWAP_AX] filename

Rotate a FITS file to put spectral axis first.

positional arguments:
  filename              Input filename.

optional arguments:
  -h, --help            show this help message and exit
  -o [OUTFILE], --outfile [OUTFILE]
                        Output filename. Defaults to input filename with .rot.fits extension.
  -e EXT, --ext EXT     Extension number. Defaults to 0.
  -s SWAP_AX, --swap-ax SWAP_AX
                        Axis to swap with spectral axis (numpy convention). Defaults to -1.
```
