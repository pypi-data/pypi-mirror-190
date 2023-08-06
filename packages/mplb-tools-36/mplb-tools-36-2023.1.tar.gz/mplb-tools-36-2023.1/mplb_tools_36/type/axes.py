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

from typing import Final, Tuple

import matplotlib.ticker as ticker_t
from matplotlib.image import AxesImage as axes_image_t
from matplotlib.pyplot import Axes as axes_t
from mpl_toolkits.axes_grid1.axes_divider import AxesDivider as axes_divider_t
from mpl_toolkits.axes_grid1 import make_axes_locatable as NewDividerFor
from mpl_toolkits.mplot3d.axes3d import Axes3D as axes_3d_t


axes_grid_h = Tuple[Tuple[axes_t | None, ...], ...]


AUTO_GRID_THRESHOLD = 6


AXES_SIDES: Final = ("bottom", "top", "left", "right")
XY_FROM_SIDE: Final = {"bottom": "x", "top": "x", "left": "y", "right": "y"}

DEFAULT_AXIS_PROPS: Final = {
    # --- Spines
    "spine_color": None,
    # --- Ticks
    "show_ticks": True,
    "tick_positions": None,
    "tick_direction": None,
    "tick_length": None,
    "tick_width": None,
    "tick_color": None,
    # --- Tick labels
    "show_tick_labels": True,
    "tick_labels": None,
    "tick_label_formatter": None,
    "t2tl_distance": None,
    "tick_label_size": None,
    "tick_label_rotation": None,
    "tick_label_color": None,
    # --- Axis label
    "show_axis_label": True,
    "axis_label": None,
    "axis_label_position": None,
    "axis_label_position_offset": None,
    "axis_label_color": None,
}
DEFAULT_GRID_PROPS: Final = {
    "which": None,
    "width": None,
    "style": None,
    "alpha": None,
    "color": None,
}

# Some tick property names and their translation into Axes.tick_params arguments
MPLB_PRM_FROM_TICK_PROP: Final = {
    # --- Ticks
    "tick_direction": "direction",
    "tick_length": "length",
    "tick_width": "width",
    "tick_color": "color",
    # --- Tick labels
    "t2tl_distance": "pad",  # t2tl=Tick-to-Tick label
    "tick_label_size": "labelsize",
    "tick_label_rotation": "labelrotation",
    "tick_label_color": "labelcolor",
}
# Some grid property names and their translation into Axes.tick_params arguments
MPLB_PRM_FROM_GRID_PROP: Final = {
    "width": "grid_linewidth",
    "style": "grid_linestyle",
    "alpha": "grid_alpha",
    "color": "grid_color",
}
