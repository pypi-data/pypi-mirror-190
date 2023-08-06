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
from im_tools_36.shape import AutoCropped
from mplb_tools_36.axes import SetAxesDecorations
from mplb_tools_36.in_out import SaveFigure


figure_1, axes = pypl.subplots()
axes.plot(range(0, 5), 50 * nmpy.random.rand(5), "y--")
xbot_props = {
    "spine_color": "b",
    "tick_positions": (0, 1, 2),
    "tick_direction": "inout",
    "tick_length": 10,
    "tick_width": 3,
    "tick_color": "m",
    "tick_labels": ("A", "B", "C"),
    "tick_label_rotation": 45,
    "tick_label_color": "g",
    "axis_label": "letter",
    "axis_label_position": "end",
    "axis_label_position_offset": (5, 0),
    "axis_label_color": "r",
}
xtop_props = {
    "spine_color": "g",
    "tick_positions": (0, 1, 2),
    "tick_direction": "in",
    "tick_labels": ("A", "B", "C"),
    "axis_label": "letter top",
    "axis_label_position": "end",
    "axis_label_position_offset": (5, 0),
}
ylef_props = {
    "show_ticks": False,
    "tick_positions": (0, 1.5, 2.5),
    "tick_labels": ("1", "2", "3"),
    "axis_label": "number",
}
ygrid_props = {"which": "both"}
SetAxesDecorations(
    axes,
    x_from_to=(0, 4),
    y_from_to=(0, None),
    xbot_props=xbot_props,
    xtop_props=xtop_props,
    ylef_props=ylef_props,
    ygrid_props=ygrid_props,
)

figure_2, axes = pypl.subplots()
axes.imshow(nmpy.random.rand(200, 300), cmap="gray")
xbot_props = {
    "spine_color": "b",
    "tick_direction": "inout",
    "tick_length": 10,
    "tick_width": 3,
    "tick_color": "m",
    "tick_label_rotation": 45,
    "tick_label_color": "g",
    "axis_label": "number x",
    "axis_label_position": "end",
    "axis_label_position_offset": (5, 0),
    "axis_label_color": "r",
}
ylef_props = {
    "show_ticks": False,
    "tick_label_formatter": "reversed",
    "axis_label": "number y",
}
SetAxesDecorations(
    axes,
    xbot_props=xbot_props,
    ylef_props=ylef_props,
    ygrid_props=ygrid_props,
)

figure_3, axes = pypl.subplots()
axes.imshow(nmpy.random.rand(200, 300), cmap="gray")
xbot_props = {
    "spine_color": "b",
    "tick_direction": "inout",
    "tick_length": 10,
    "tick_width": 3,
    "tick_color": "m",
    "tick_label_rotation": 45,
    "tick_label_color": "g",
    "axis_label": "number x",
    "axis_label_position": "end",
    "axis_label_position_offset": (5, 0),
    "axis_label_color": "r",
}
yrig_props = {
    "show_ticks": False,
    "tick_label_formatter": "reversed",
    "tick_label_color": "b",
    "axis_label": "number y",
    "axis_label_color": "b",
}
SetAxesDecorations(
    axes,
    xbot_props=xbot_props,
    yrig_props=yrig_props,
    ygrid_props=ygrid_props,
)

figures = (figure_1, figure_2, figure_3)
paths = (f"figure_{idx+1}.png" for idx in range(figures.__len__()))
for figure, path in zip(figures, paths):
    SaveFigure(figure, path, AutoCropped=AutoCropped)

pypl.show()
