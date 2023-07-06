# -*- coding: utf-8 -*-
"""
Importer for MeteoSwiss radar composites in metranet format.

This importer is the same as the original importer in pysteps, but it uses
py-radlib to read the files.
"""

# Import the needed libraries
import numpy as np

try:
    import radlib

    RADLIB_IMPORTED = True
except ImportError:
    RADLIB_IMPORTED = False

from pysteps.decorators import postprocess_import
from pysteps.exceptions import MissingOptionalDependency


# Function importer_mch_metranet_radlib_xxx to import 8-bit-format
# files from the MeteoSwiss


@postprocess_import()
def import_mch_metranet_radlib(filename, product, unit, accutime, **kwargs):
    """
    Import a 8-bit bin radar reflectivity composite from the MeteoSwiss
    archive.

    Parameters
    ----------
    filename: str
        Name of the file to import.
    product: {"AQC", "CPC", "RZC", "AZC"}
        The name of the MeteoSwiss QPE product.\n
        Currently supported prducts:

        +------+----------------------------+
        | Name |          Product           |
        +======+============================+
        | AQC  |     Acquire                |
        +------+----------------------------+
        | CPC  |     CombiPrecip            |
        +------+----------------------------+
        | RZC  |     Precip                 |
        +------+----------------------------+
        | AZC  |     RZC accumulation       |
        +------+----------------------------+

    unit: {"mm/h", "mm", "dBZ"}
        the physical unit of the data
    accutime: float
        the accumulation time in minutes of the data

    {extra_kwargs_doc}

    Returns
    -------

    out: tuple
        A three-element tuple containing the precipitation field in mm/h imported
        from a MeteoSwiss gif file and the associated quality field and metadata.
        The quality field is currently set to None.
    """
    if not RADLIB_IMPORTED:
        raise MissingOptionalDependency(
            "py-radlib package needed for importing MeteoSwiss "
            "radar composites but it is not installed"
        )

    ret = radlib.read_file(filename, physic_value=True, verbose=False)
    precip = ret.data

    geodata = _import_mch_geodata()

    # read metranet
    metadata = geodata
    metadata["institution"] = "MeteoSwiss"
    metadata["accutime"] = accutime
    metadata["unit"] = unit
    metadata["transform"] = None
    metadata["zerovalue"] = np.nanmin(precip)
    metadata["threshold"] = _get_threshold_value(precip)
    metadata["zr_a"] = 316.0
    metadata["zr_b"] = 1.5

    return precip, None, metadata


def _import_mch_geodata():
    """
    Swiss radar domain CCS4
    These are all hard-coded because the georeferencing is missing from the gif files.
    """

    geodata = {}

    # LV03 Swiss projection definition in Proj4
    projdef = ""
    projdef += "+proj=somerc "
    projdef += " +lon_0=7.43958333333333"
    projdef += " +lat_0=46.9524055555556"
    projdef += " +k_0=1"
    projdef += " +x_0=600000"
    projdef += " +y_0=200000"
    projdef += " +ellps=bessel"
    projdef += " +towgs84=674.374,15.056,405.346,0,0,0,0"
    projdef += " +units=m"
    projdef += " +no_defs"
    geodata["projection"] = projdef

    geodata["x1"] = 255000.0
    geodata["y1"] = -160000.0
    geodata["x2"] = 965000.0
    geodata["y2"] = 480000.0

    geodata["xpixelsize"] = 1000.0
    geodata["ypixelsize"] = 1000.0
    geodata["cartesian_unit"] = "m"
    geodata["yorigin"] = "upper"

    return geodata


def _get_threshold_value(precip):
    """
    Get the the rain/no rain threshold with the same unit, transformation and
    accutime of the data.
    If all the values are NaNs, the returned value is `np.nan`.
    Otherwise, np.min(precip[precip > precip.min()]) is returned.

    Returns
    -------
    threshold: float
    """
    valid_mask = np.isfinite(precip)
    if valid_mask.any():
        _precip = precip[valid_mask]
        min_precip = _precip.min()
        above_min_mask = _precip > min_precip
        if above_min_mask.any():
            return np.min(_precip[above_min_mask])
        else:
            return min_precip
    else:
        return np.nan
