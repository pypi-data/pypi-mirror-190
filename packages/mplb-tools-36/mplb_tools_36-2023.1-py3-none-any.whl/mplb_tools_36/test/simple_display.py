# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2020)
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

import matplotlib.pyplot as pypl
import numpy as nmpy
import skimage.data as sidt
from mplb_tools_36.config import ParametricSurfaceConfig, XYHeightConfig
from mplb_tools_36.main import SimpleDisplay


img_curve = nmpy.random.randint(10, size=100)
img_bool = sidt.checkerboard().astype(nmpy.bool_)
img_bool_stack = nmpy.dstack(
    tuple(nmpy.roll(img_bool, shift, axis=1) for shift in range(0, 25, 5))
)
img_gray = sidt.moon()
img_rgb = sidt.colorwheel()
img_rgba = sidt.logo()
img_4d = nmpy.empty((2, 2, 2, 2))

x_coords = nmpy.arange(-5.0, 5.0, 0.25)
y_coords = nmpy.arange(-5.0, 5.0, 0.25)
grid_x_coords, grid_y_coords = nmpy.meshgrid(x_coords, y_coords)
norms = nmpy.sqrt(grid_x_coords**2 + grid_y_coords**2)
height = nmpy.sin(norms)
xyheight = XYHeightConfig(height)

param_u = nmpy.linspace(0.0, 2.0 * nmpy.pi)
param_v = nmpy.linspace(-0.5, 0.5, num=10)
XCoords = lambda prm_u, prm_v: (1.0 + 0.5 * prm_v * nmpy.cos(prm_u / 2.0)) * nmpy.cos(
    prm_u
)
YCoords = lambda prm_u, prm_v: (1.0 + 0.5 * prm_v * nmpy.cos(prm_u / 2.0)) * nmpy.sin(
    prm_u
)
ZCoords = lambda prm_u, prm_v: 0.5 * prm_v * nmpy.sin(prm_u / 2.0)
prm_surf = ParametricSurfaceConfig(
    param_u,
    param_v,
    XCoords,
    YCoords,
    ZCoords,
)

e_idx = 1

examples = SimpleDisplay(img_gray, img_rgb, mode="make_only")
examples[0].suptitle(f"{e_idx}: Separate (Gray)")
examples[1].suptitle(f"{e_idx}: Separate (Color)")
e_idx += 1

examples = SimpleDisplay(
    (img_bool_stack, img_gray, img_rgb),
    (img_bool, img_curve, img_rgba),
    mode="make_only",
)
examples[0].suptitle(f"{e_idx}: Together (Boolean Stack, Gray, Color)")
examples[1].suptitle(f"{e_idx}: Together (Boolean, Curve, RGBA Stack)")
e_idx += 1

examples = SimpleDisplay(
    ((img_gray, None, img_rgb), (img_gray, img_4d, img_rgb, img_rgba)),
    mode="make_only",
)
examples.suptitle(
    f"{e_idx}: Grid ((Gray, <blank>, Color, <blank>), (Gray, <invalid>, Color, RGBA Stack))"
)
e_idx += 1

examples = SimpleDisplay(
    (img_gray, None, img_rgb, img_gray, img_4d, img_rgb, img_rgba, xyheight, prm_surf),
    auto_grid=True,
    mode="make_only",
)
examples.suptitle(
    f"{e_idx}: Autogrid (Gray, <blank>, Color, Gray, <invalid>, Color, RGBA Stack, XYHeight, PSurf)"
)
e_idx += 1

pypl.show()
