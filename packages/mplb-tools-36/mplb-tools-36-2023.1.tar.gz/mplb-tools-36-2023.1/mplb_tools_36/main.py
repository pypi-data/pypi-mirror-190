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

# "By EricD" --- str-2-hex ---> 4279204572696344 --- log ---> 35.99254353973175 --- ~ ---> 36
# int(numpy.around(numpy.log(float("By EricD".encode("utf-8").hex()))))

import itertools as ittl
from typing import Any, List, Optional, Tuple, Union

import matplotlib.pyplot as pypl
import numpy as nmpy
import scipy.ndimage as spim
from mplb_tools_36.type.axes import (
    AUTO_GRID_THRESHOLD,
    NewDividerFor,
    axes_3d_t,
    axes_divider_t,
    axes_grid_h,
    axes_image_t,
    axes_t,
)
from mplb_tools_36.type.base import figure_t
from mplb_tools_36.type.colorbar import (
    COLORBAR_PADDING,
    COLORBAR_WIDTH,
    SOME_COLORMAPS,
    dynamic_colorbar_t,
)
from mplb_tools_36.type.slider import (
    STACK_SLIDER_PADDING,
    STACK_SLIDER_WIDTH,
    stack_slider_t,
)


array_t = nmpy.ndarray
boolean_t = nmpy.dtype("?")


def SimpleDisplay(
    *img_args,
    auto_grid: bool = False,
    mode: str = "interactive",
    return_axes: bool = False,
) -> Optional[
    Union[
        figure_t,
        Tuple[figure_t, Tuple[axes_t, ...] | axes_grid_h],
        Tuple[figure_t, ...],
        Tuple[Tuple[figure_t, ...], Tuple[Tuple[axes_t, ...] | axes_grid_h, ...]],
    ]
]:
    """
    img_args: img_arg or img_arg_1, img_arg_2...
    Each img_arg will give rise to a figure and can be:
    - a numpy array: the image will be displayed normally
    - a sequence of numpy arrays: the images will be displayed in a row, unless auto_grid is True or the number of
    arrays exceeds a threshold (constant AUTO_GRID_THRESHOLD in module)
    - a sequence of sequences of numpy arrays: the images will be displayed in grid. The sequences need not be of the
    same length. Sequences shorter than the longest one are completed with blank images.
    Any of the numpy arrays can in fact be replaced with None, in which case a blank space will be left, or with a
    dictionary for alternative plots, including 3-D. Such a dictionary must have the following key-value pairs:
    - "ndim": the dimension of the plot among 1, 2 or 3 (using numpy terminology)
    - "type": a plotting method of matplotlib.axes.Axes or mpl_toolkits.mplot3d.axes3d.Axes3D, e.g., bar or bar3d;
    - "data": a tuple of the elements to be plotted, passed as the first arguments to the "type" method;
    - "config": a dictionary of additional arguments to the "type" method, passed as keyword arguments.

    If a numpy array has a shape of (n_elms,), it will be plotted as a curve. If it has a shape of (n_rows, n_cols), it
    will be displayed as a grayscale image. If it has a depth of 3, it will be displayed as an RGB image. Otherwise, it
    will be displayed as stacked grayscale images with a slider allowing to navigate through the stack. This means that
    RGBA images will be treated as stacks too.

    auto_grid: If True, then a sequence of numpy arrays will be displayed in square grid.

    mode: "interactive", "display_only", "make_only"
    - interactive: figures are displayed and event loop blocks execution until all figures are closed
    - display_only: figures are displayed but event loop is not run (non-interactive display)
    - make_only: figures are built but not displayed (and event loop is not run)

    If a colorbar is shown above an image, then clicking on it allows to cycle through a predefined list of colormaps.

    Returned value: If "mode" is "interactive", the function returns None. Otherwise, it returns, at least, a tuple of
    the Matplotlib figures that were created. If "return_axes" is True, it also returns a tuple of axes grids, one grid
    per figure, where a grid is an n_rows-tuple of n_cols-tuples of axes, where any of the axes can actually be None if
    no plot was made at the corresponding grid position.
    """
    if return_axes and (mode == "interactive"):
        raise ValueError(
            f'{mode}: Invalid mode when axes should be returned; Expected_"display_only", "make_only"'
        )

    figures: List[figure_t] = []
    axes_grids: List[List[List[axes_t | None]]] = []
    auto_auto_grid = False

    for img_grid in img_args:
        # The tests below only apply to the first element (*)
        if _PlottableIsValid(img_grid):
            img_grid = ((img_grid,),)
        elif _PlottableIsValid(img_grid[0]):
            # FIXME: If img_grid is not iterable, the raised exception will not be informative enough
            n_imgs = img_grid.__len__()
            auto_auto_grid = n_imgs > AUTO_GRID_THRESHOLD
            if auto_grid or auto_auto_grid:
                n_cols = int(nmpy.ceil(nmpy.sqrt(n_imgs)).item())
                n_remaining = n_imgs % n_cols
                computed_grid = [
                    img_grid[idx : (idx + n_cols)]
                    for idx in range(0, n_imgs - n_cols + 1, n_cols)
                ]
                if n_remaining > 0:
                    computed_grid.append(img_grid[-n_remaining:])
                img_grid = computed_grid
            else:
                img_grid = (img_grid,)
        elif _PlottableIsValid(img_grid[0][0]):
            # FIXME: If img_grid[0] is not iterable, the raised exception will not be informative enough
            pass
        else:
            raise ValueError(f"{img_grid}: Invalid plottable")
        n_rows = img_grid.__len__()
        n_cols = max(row.__len__() for row in img_grid)

        # constrained_layout produces bad layouts (although it worked fine with matplotlib.pyplot.subplots in a 2-D only,
        # previous version).
        figure = pypl.figure(tight_layout=True)
        axes_grid: List[List[axes_t | None]] = [
            [None for _ in range(n_cols)] for _ in range(n_rows)
        ]
        a_idx = 1
        for row in range(n_rows):
            for col in range(img_grid[row].__len__()):
                img = img_grid[row][col]
                if img is not None:
                    if isinstance(img, dict):
                        if img["ndim"] in (1, 2):
                            projection = {}
                        elif img["ndim"] == 3:
                            projection = {"projection": axes_3d_t.name}
                        else:
                            raise ValueError(
                                f"{img['ndim']}: Invalid plot dimension for plot {row}x{col}"
                            )
                    elif isinstance(img, array_t):
                        if img.size > 0:
                            projection = {}
                        else:
                            projection = None
                    else:
                        # This case can happen since the tests above only apply to the first element (*)
                        raise ValueError(f"{img}: Invalid plottable")
                    if projection is not None:
                        axes = figure.add_subplot(
                            n_rows, n_cols, a_idx + col, **projection
                        )
                        axes_grid[row][col] = axes
            # Do not increment a_idx by 1 in each loop iteration above since the loop might be shorter than n_cols
            a_idx += n_cols

        figures.append(figure)
        axes_grids.append(axes_grid)

        for row in range(n_rows):
            for col in range(n_cols):
                axes: Optional[axes_t] = axes_grid[row][col]
                if axes is None:
                    continue

                img = img_grid[row][col]
                if isinstance(img, dict):
                    getattr(axes, img["type"])(*img["data"], **img["config"])
                else:
                    if img.ndim == 1:
                        axes.plot(img)
                        axes.set_xlim(left=0, right=img.__len__() - 1)
                    elif img.ndim in (2, 3):
                        type_is_boolean = nmpy.issubdtype(img.dtype, boolean_t)

                        if (img.ndim == 3) and (img.shape[2] == 3):
                            kwargs = {}
                            is_a_stack = False
                            img_to_show = img
                        else:
                            if type_is_boolean:
                                kwargs = {"cmap": "prism"}
                            else:
                                kwargs = {"cmap": SOME_COLORMAPS[0]}
                            is_a_stack = (img.ndim == 3) and (img.shape[2] != 3)
                            if is_a_stack:
                                img_to_show = img[:, :, 0]
                            else:
                                img_to_show = img

                        if type_is_boolean:
                            min_value = False
                            max_value = True
                        else:
                            # Currently, for image stacks, the dynamic and colorbar are global (i.e., fixed), as opposed to
                            # be local to the displayed slice (img_to_show). This might change.
                            min_value, max_value, *_ = spim.extrema(img)
                        mplb_img = axes.imshow(
                            img_to_show,
                            vmin=min_value,
                            vmax=max_value,
                            interpolation="nearest",
                            **kwargs,
                        )
                        axes.format_coord = _FormattedCoordinates

                        axes_divider = None
                        if type_is_boolean:
                            mplb_img.format_cursor_data = _FormattedBooleanValue
                        elif img_to_show.ndim == 2:
                            axes_divider = _AddColorbar(figure, axes, mplb_img)
                        if is_a_stack:
                            slider = _AddStackSlider(
                                figure, axes, axes_divider, mplb_img, img
                            )
                            # Keep a reference to slider so that it remains responsive (find another way eventually)
                            if hasattr(figure, "__mp36_slider_references__"):
                                figure.__mp36_slider_references__.append(slider)
                            else:
                                figure.__mp36_slider_references__ = [slider]
                    else:
                        _DisplayErrorImage(row, col, axes, img)

    if mode == "interactive":
        pypl.show(block=True)
        return None

    if mode == "display_only":
        pypl.show(block=False)
        for figure in figures:
            figure.canvas.draw()
    elif mode == "make_only":
        pass
    else:
        raise ValueError(f"{mode}: Invalid display mode")

    if return_axes:
        if auto_grid or auto_auto_grid:
            # Do not return a grid since the images were passed as a one-dimensional sequence
            axes_grids_frozen = tuple(
                tuple(ittl.chain.from_iterable(axes_grid)) for axes_grid in axes_grids
            )
        else:
            axes_grids_frozen = tuple(
                tuple(tuple(axes_row) for axes_row in axes_grid)
                for axes_grid in axes_grids
            )
    else:
        axes_grids_frozen = None
    if figures.__len__() > 1:
        if return_axes:
            return tuple(figures), axes_grids_frozen
        else:
            return tuple(figures)
    elif return_axes:
        return figures[0], axes_grids_frozen[0]
    else:
        return figures[0]


def _PlottableIsValid(plottable: Any, /) -> bool:
    """"""
    return (
        (plottable is None)
        or isinstance(plottable, array_t)
        or isinstance(plottable, dict)
    )


def _FormattedCoordinates(x_coord: float, y_coord: float, /) -> str:
    """"""
    row = int(y_coord + 0.5)
    col = int(x_coord + 0.5)

    return f"[{row},{col}]"


def _FormattedBooleanValue(value: Any, /) -> str:
    """"""
    return str(value)


def _AddColorbar(
    figure: figure_t, axes: axes_t, mplb_img: axes_image_t, /
) -> axes_divider_t:
    """
    Simplest way: colorbar = figure.colorbar(mplb_img, ax=axes)
    """
    axes_divider = NewDividerFor(axes)
    colorbar_room = axes_divider.new_vertical(size=COLORBAR_WIDTH, pad=COLORBAR_PADDING)
    _ = dynamic_colorbar_t(figure, colorbar_room, mplb_img, orientation="horizontal")

    return axes_divider


def _AddStackSlider(
    figure: figure_t,
    axes: axes_t,
    axes_divider: axes_divider_t,
    mplb_img: axes_image_t,
    img: array_t,
    /,
) -> stack_slider_t:
    """"""
    if axes_divider is None:
        axes_divider = NewDividerFor(axes)
        slider_room = axes_divider.new_horizontal(
            size=STACK_SLIDER_WIDTH, pad=STACK_SLIDER_PADDING
        )
        figure.add_axes(slider_room)
    else:
        slider_room = axes_divider.append_axes(
            "right", STACK_SLIDER_WIDTH, pad=STACK_SLIDER_PADDING
        )

    output = stack_slider_t(
        slider_room,
        img,
        mplb_img,
        "",
        dragging=False,
        orientation="vertical",
    )

    return output


def _DisableAxes(axes: axes_t, /) -> None:
    """"""
    axes.set_axis_off()
    axes.set_navigate(False)


def _DisplayErrorImage(row: int, col: int, axes: axes_t, img: array_t, /) -> None:
    """"""
    axes.matshow(nmpy.full((200, 200, 3), 255, dtype=nmpy.uint8))
    axes.text(
        0,
        150,
        f"Image {row}x{col}:\nDimension_{img.ndim}\nExpected_1, 2, 3",
        fontsize="xx-small",
        color="r",
    )
    _DisableAxes(axes)


# def _OnFigureResize(axes: axes_t, twin_axes: Tuple[axes_t, ...], /) -> None:
#     """"""
#     _SynchronizeAxes(axes, twin_axes)
#     _ReapplyAxesDecorations(axes, twin_axes)
