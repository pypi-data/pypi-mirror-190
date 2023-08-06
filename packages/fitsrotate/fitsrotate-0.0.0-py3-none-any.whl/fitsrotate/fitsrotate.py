#!/usr/bin env python3
# -*- coding: utf-8 -*-
"""Rotate a FITS file to put spectral axis first."""
from typing import Union

from astropy.io import fits
from astropy.wcs import WCS
import numpy as np
import dask.array as da

def fits_to_numpy(naxis: int, fits_idx: int) -> int:
    """Convert FITS axis index to numpy axis index.

    Args:
        naxis (int): Number of axis.
        fits_idx (int): FITS axis index.

    Returns:
        int: Numpy axis index.

    """

    return np.arange(naxis-1, -1, -1)[fits_idx]

def rotate_hdu(
    data: Union[np.ndarray, da.Array],
    header: fits.Header,
    wcs: WCS,
    swap_ax: int = -1,
) -> fits.PrimaryHDU:
    """Rotate FITS HDU to put spectral axis first.

    Args:
        data (np.ndarray): Data array.
        header (fits.Header): Header.
        wcs (WCS): WCS.

    Returns:
        fits.ImageHDU: Rotated FITS HDU.
    """
    # Find spectral axis
    spec_axis = wcs.wcs.spec
    print(f"Spectral axis is {spec_axis} in FITS convention.")
    spec_axis_idx = fits_to_numpy(wcs.naxis, spec_axis)
    print(f"Spectral axis is {spec_axis_idx} in numpy convention.")

    data_swap = data.swapaxes(spec_axis_idx, swap_ax)
    wcs_swap = wcs.swapaxes(spec_axis_idx, swap_ax)
    header_swap = header.copy()
    wcs_head = wcs_swap.to_header()
    for key, value in wcs_head.items():
        header_swap[key] = value

    return fits.PrimaryHDU(data=data_swap, header=header_swap)

def main(
    filename: str,
    outfile: Union[str, None] = None,
    ext: int = 0,
    swap_ax: int = -1,
):
    """Rotate FITS file to put spectral axis first.

    Args:
        filename (str): Input filename.
        outfile (str, optional): Output filename. Defaults to None.
        ext (int, optional): Extension number. Defaults to 0.
    """
    print(f"Reading {filename}...")
    with fits.open(filename, memmap=True, mode="denywrite") as hdulist:
        print(f"Using extension {ext}...")
        hdu = hdulist[ext]
        header = hdu.header
        wcs = WCS(header)
        data = da.from_array(hdu.data)

        print("Rotating...")
        hdu_rot = rotate_hdu(data, header, wcs)

        if outfile is None:
            outfile = filename.replace(".fits", ".rot.fits")

        print(f"Writing rotated file to {outfile}...")

        hdulist[ext] = hdu_rot
        hdulist.writeto(outfile, overwrite=True)

    print("Done!")

def cli():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("filename", help="Input filename.")
    parser.add_argument(
        "-o",
        "--outfile",
        nargs="?",
        default=None,
        help="Output filename. Defaults to input filename with .rot.fits extension.",
    )
    parser.add_argument(
        "-e",
        "--ext",
        type=int,
        default=0,
        help="Extension number. Defaults to 0.",
    )
    parser.add_argument(
        "-s",
        "--swap-ax",
        type=int,
        default=-1,
        help="Axis to swap with spectral axis (numpy convention). Defaults to -1.",
    )
    args = parser.parse_args()
    main(
        filename=args.filename,
        outfile=args.outfile,
        ext=args.ext,
        swap_ax=args.swap_ax,
    )

if __name__ == "__main__":
    cli()