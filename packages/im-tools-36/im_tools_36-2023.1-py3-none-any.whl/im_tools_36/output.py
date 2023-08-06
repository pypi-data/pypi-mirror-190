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

import imageio as imio
import numpy as nmpy
from im_tools_36.path import path_h


array_t = nmpy.ndarray


def SaveImage8(image: array_t, path: path_h, /, *, w_scaling: bool = True) -> None:
    """
    8: For 8 bits
    """
    image = image.astype(nmpy.float64, copy=False)
    if w_scaling:
        img_min = nmpy.min(image)
        img_max = nmpy.max(image)
        if img_max > img_min:
            image = (255.0 / (img_max - img_min)) * (image - img_min)
        else:
            # Avoid -= in case it really is inplace (since copy=False was used above)
            image = image - img_min
    image = nmpy.around(image).astype(nmpy.uint8)

    imio.imwrite(path, image)
