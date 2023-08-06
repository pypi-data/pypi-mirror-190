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

from pathlib import Path as path_t
from typing import Callable, Tuple, Union

import numpy as nmpy
from matplotlib import image as mpim
from mplb_tools_36.type.axes import axes_t
from mplb_tools_36.type.base import figure_t


array_t = nmpy.ndarray

path_h = Union[str, path_t]


def PrepareAxesForSaving(axes: axes_t, /) -> None:
    """"""
    axes.set_axis_off()
    # axes.set_axis_on()
    # axes.spines["top"].set_visible(False)
    # axes.spines["right"].set_visible(False)
    #
    # # Removing x-or-y-tick labels (set_xticklabels(())) also prevents x-or-y-pointer-coordinate display!
    # # Make them the color of the background instead.
    # axes.tick_params(axis="both", labelcolor=axes.get_figure().get_facecolor())


def FigureContents(
    figure: figure_t,
    /,
    *,
    per_axes: bool = False,
    AutoCropped: Callable[..., array_t] = None,
) -> Union[array_t, Tuple[array_t, ...]]:
    """"""
    figure.canvas.draw()
    background_color = _FigureBackground(figure)

    # Also nmpy.around(figure.get_size_inches() * figure.dpi).astype(nmpy.uint64)
    width, height = figure.canvas.get_width_height()
    # figure.canvas.tostring_rgb() returns a [0, 255]-image
    output = nmpy.fromstring(figure.canvas.tostring_rgb(), dtype=nmpy.uint8)
    output = nmpy.reshape(output, (height, width, 3))

    if per_axes:
        output_per_axes = []
        for axes in figure.axes:
            positions = axes.get_position()
            positions = nmpy.array(
                (positions.xmin, positions.xmax, positions.ymin, positions.ymax),
                dtype=nmpy.float64,
            )
            positions *= (width, width, height, height)
            positions[2:] = height - positions[2:]
            positions = nmpy.around(positions).astype(nmpy.uint64)
            col_min, col_max_p1, row_max_p1, row_min = positions
            img = output[row_min:row_max_p1, col_min:col_max_p1, :]
            if AutoCropped is None:
                output_per_axes.append(img)
            else:
                output_per_axes.append(AutoCropped(img, value=background_color))
        output = tuple(output_per_axes)
    elif AutoCropped is not None:
        # Do not autocrop before otherwise, if per-axes, axes positions will get incorrect
        output = AutoCropped(output, value=background_color)

    return output


def SaveFigure(
    figure: figure_t, path: path_h, /, *, AutoCropped: Callable[..., array_t] = None
) -> None:
    """"""
    figure.canvas.draw()
    figure.savefig(path, bbox_inches="tight")

    if AutoCropped is not None:
        background_color = _FigureBackground(figure, mode="float01")
        img = mpim.imread(path)[:, :, :3]
        img = AutoCropped(img, value=background_color)
        mpim.imsave(path, img)


def _FigureBackground(
    figure: figure_t, /, *, mode: str = "uint8"
) -> Tuple[int, int, int]:
    """
    Uint8-based or [0,1]-float-based figure background color
    """
    # figure.get_facecolor() returns a [0.0, 1.0]-color
    output = figure.get_facecolor()[:3]  # Remove alpha component, if present
    if mode == "uint8":
        output = tuple(int(round(255.0 * value)) for value in output)
    elif mode == "float01":
        output = tuple(output)  # To make a copy
    else:
        raise ValueError

    return output
