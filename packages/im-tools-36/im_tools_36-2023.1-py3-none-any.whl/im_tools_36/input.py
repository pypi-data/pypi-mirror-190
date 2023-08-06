# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2019)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import importlib as mprt
import itertools as ittl
from types import ModuleType as module_t
from typing import Sequence, Tuple

import imageio as mgio
import numpy as nmpy
from im_tools_36.path import path_h, path_t


def _Module(name: str, /) -> module_t | None:
    """"""
    try:
        output = mprt.import_module(name)
    except ModuleNotFoundError:
        output = None

    return output


aics = _Module("aicsimageio")
mrci = _Module("mrc")
skio = _Module("skimage.io")
tiff = _Module("tifffile")


array_t = nmpy.ndarray


def _WithAICS(path: str, /) -> array_t:
    """
    Arrangement: TCZYX
    """
    return aics.AICSImage(path).data


def _WithMRC(path: str, /) -> array_t:
    """
    If output.ndim == 5, probably time x channel x Z x Y x X, while sequences are:
        time x channel   x (Z=1 x)             Y x X.
    So one gets:
        time x channel=1 x Z=actual channels x Y x X. Then, use: output[:, 0, :, :]
    numpy.array: Because the returned value seems to be a read-only memory map
    """
    return nmpy.array(mrci.imread(path))


READING_MODULE = {
    "aicsimageio": aics,
    "imageio": mgio,
    "mrc": mrci,
    "scikit-image": skio,
    "skimage": skio,
    "tifffile": tiff,
}
READING_FUNCTION = {
    aics: _WithAICS,
    mgio: mgio.v3.imread,
    mrci: _WithMRC,
    skio: skio.imread,
    tiff: tiff.imread,
    None: None,
}


def ImageVolumeOrSequence(
    path: path_h,
    /,
    *,
    with_module: str = None,
    should_squeeze: bool = True,
    expected_dim: int = None,
    expected_shape: Sequence[int | None] = None,
) -> array_t | Tuple[str, ...]:
    """"""
    # Potential outputs
    image = None
    issues = []

    if isinstance(path, str):
        path_str = path
        path_lib = path_t(path)
    else:
        path_str = str(path)
        path_lib = path
    if (expected_dim is None) and (expected_shape is not None):
        expected_dim = expected_shape.__len__()

    if with_module is None:
        reading_functions = [READING_FUNCTION[mgio], READING_FUNCTION[skio]]

        img_format = path_lib.suffix[1:].lower()
        if img_format in ("tif", "tiff"):
            reading_functions.append(READING_FUNCTION[aics])
            reading_functions.append(READING_FUNCTION[tiff])
        elif img_format in ("dv", "mrc"):
            if img_format == "dv":
                reading_functions.append(READING_FUNCTION[aics])
            reading_functions.append(READING_FUNCTION[mrci])
        elif img_format in ("czi", "lif", "nd2"):
            reading_functions.append(READING_FUNCTION[aics])
    elif with_module in READING_MODULE:
        reading_functions = [READING_FUNCTION[READING_MODULE[with_module]]]
    else:
        return (
            f"{with_module}: Invalid module. Expected={str(tuple(READING_MODULE.keys()))[1:-1]}",
        )

    for Read in reversed(reading_functions):
        if Read is None:
            continue

        try:
            image = Read(path_str)
            break
        except Exception as exception:
            issues.append(str(exception))

    if image is None:
        return tuple(issues)

    if should_squeeze:
        image = nmpy.squeeze(image)

    if (expected_dim is not None) and (image.ndim != expected_dim):
        return (
            f"{image.ndim}: Invalid dimension (shape={image.shape}). Expected={expected_dim}",
        )
    if expected_shape is None:
        return image

    shape = image.shape
    if _ShapesMatch(shape, expected_shape):
        return image

    shape_as_array = nmpy.array(shape)
    for order in ittl.permutations(range(image.ndim)):
        if _ShapesMatch(shape_as_array[nmpy.array(order)], expected_shape):
            return nmpy.moveaxis(image, order, range(image.ndim))

    return (
        f"{shape}: Invalid shape. Expected={tuple(expected_shape)}, or a permutation of it",
    )


def _ShapesMatch(
    actual: Tuple[int, ...] | array_t, expected: Sequence[int | None], /
) -> bool:
    """"""
    return all((_ctl == _xpt) or (_xpt is None) for _ctl, _xpt in zip(actual, expected))
