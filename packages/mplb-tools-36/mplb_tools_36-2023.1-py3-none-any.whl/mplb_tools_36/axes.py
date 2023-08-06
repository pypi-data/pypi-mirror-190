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

import copy
from fractions import Fraction as rational_t
from typing import Any, Callable, Dict, Sequence, Tuple, Optional, Union

import numpy as nmpy
from mplb_tools_36.type.axes import (
    AXES_SIDES,
    DEFAULT_AXIS_PROPS,
    DEFAULT_GRID_PROPS,
    MPLB_PRM_FROM_GRID_PROP,
    MPLB_PRM_FROM_TICK_PROP,
    XY_FROM_SIDE,
    axes_t,
    ticker_t,
)


o_float_h = Optional[float]
from_to_wo_scale_h = Tuple[o_float_h, o_float_h]
from_to_w_scale_h = Tuple[o_float_h, o_float_h, Optional[str]]
from_to_h = Union[from_to_wo_scale_h, from_to_w_scale_h]


def SetAxesDecorations(
    axes: axes_t,
    /,
    *,
    x_from_to: from_to_h = None,
    y_from_to: from_to_h = None,
    xbot_props: Dict[str, Any] = None,
    xtop_props: Dict[str, Any] = None,
    ylef_props: Dict[str, Any] = None,
    yrig_props: Dict[str, Any] = None,
    xgrid_props: Dict[str, Any] = None,
    ygrid_props: Dict[str, Any] = None,
) -> None:
    """
    The passed axes are the main axes in that they contain all the plotted materials. They are used to decorate the
    bottom and left spines. The top and right spines are decorated using auxiliary, empty axes "synchronized" with the
    main axes. Despite some significant efforts, no solutions were found with twin? axes or secondary_?axis, so the
    auxiliary axes are plain axes.
    To completely hide an axis (bottom, top, left, or right), pass None as its corresponding properties. Otherwise, the
    axis properties are passed in a dictionary (see below). At least the spine is then drawn. The optional decorations
    are the ticks, the tick labels, and the axis label.

    Note: only a few decoration possibilities have been tested.

    Unless otherwise stated, a property value of None below means "leave property as it is".
    Valid value properties are enumerated as comma-separated lists.
    x_from_to, y_from_to:
        None, Sequence[float, float] w/o scale, Sequence[float, float, str] w/ scale
        Any of the sequence values can be None.
    xbot_props, xtop_props, ylef_props, yrig_props:
        None=do not draw axis; Otherwise, dictionary with the following keys

        spine_color

        show_ticks: True, False
        tick_positions: None, Sequence[float,...]
        tick_direction: None, "in", "out", "inout"
        tick_length (in points): None, float
        tick_width (in points): None, float
        tick_color

        show_tick_labels: True, False
        tick_labels: None, Sequence[str,...]
        tick_label_formatter (mutually exclusive with "tick_labels"): None, "reversed", Callable[[float, Any], str]
        t2tl_distance (tick-to-tick-label, in points): None, float
        tick_label_size (in points or as a string): None, float, str
        tick_label_rotation
        tick_label_color

        show_axis_label: True, False
        axis_label: str
        axis_label_position: None, "end"
        axis_label_position_offset (in points): Tuple[float, float]
        axis_label_color
    xgrid_props, ygrid_props:
        None=do not draw grid; Otherwise, dictionary with the following keys
        which: None, "major", "minor", "both"
        width (in points): None, float
        style: valid Line2D line style specification
        alpha (in [0,1]): None, float
        color
    """
    # Since default values will be added to the property dictionaries, and to avoid side effects,
    # the passed dictionaries are first copied.
    if xbot_props is not None:
        xbot_props = xbot_props.copy()
    if xtop_props is not None:
        xtop_props = xtop_props.copy()
    if ylef_props is not None:
        ylef_props = ylef_props.copy()
    if yrig_props is not None:
        yrig_props = yrig_props.copy()

    if xgrid_props is not None:
        xgrid_props = xgrid_props.copy()
    if ygrid_props is not None:
        ygrid_props = ygrid_props.copy()

    # --- Property lists
    all_axes_props = (xbot_props, xtop_props, ylef_props, yrig_props)
    all_grid_props = (xgrid_props, ygrid_props)
    all_props = all_axes_props + all_grid_props
    all_defaults = 4 * (DEFAULT_AXIS_PROPS,) + 2 * (DEFAULT_GRID_PROPS,)

    # --- Defaults addition
    for props, defaults in zip(all_props, all_defaults):
        if props is not None:
            for key, value in defaults.items():
                if key not in props:
                    props[key] = value

    # --- Twin axes creation for fully independent bottom/top and left/right settings
    twin_axes = _NewTwinAxes(axes, (xtop_props, yrig_props))

    # --- Store properties
    axes.__mp36_axes_properties__ = twin_axes + tuple(
        copy.deepcopy(elm) for elm in all_props
    )

    # --- Set properties
    axes.figure.set_tight_layout(False)  # Necessary for drawing w/o warning
    _SetLimitsAndScales(axes, x_from_to, y_from_to)
    _HideAlmostAllDecorations(axes)
    for one_axes, side in zip(twin_axes, ("top", "right")):
        if one_axes is not None:
            _HideAlmostAllDecorations(one_axes, sides=(side,))
    _SetSpineColors(axes)
    _ReapplyAxesDecorations(axes)  # Necessary for saving w/o showing

    OnFigureResize = lambda _: _ReapplyAxesDecorations(axes)
    axes.figure.canvas.mpl_connect("resize_event", OnFigureResize)


def _NewTwinAxes(
    axes: axes_t,
    for_props: Tuple[Dict[str, Any], ...],
    /,
    *,
    send_to_back: bool = False,
) -> Tuple[axes_t, ...]:
    """
    Everything is made invisible, except the corresponding spine if appropriate (props is not None)
    """
    output = []

    figure = axes.figure
    position = axes.get_position(original=True)
    zorder = axes.get_zorder() - 1.0
    for props in for_props:
        if props is None:
            twin_axes = None
        else:
            twin_axes = figure.add_axes(position)
            twin_axes.patch.set_visible(False)
            if send_to_back:
                twin_axes.set_zorder(zorder)
                zorder -= 1.0
        output.append(twin_axes)

    return tuple(output)


def _SetLimitsAndScales(
    axes: axes_t,
    x_from_to: from_to_h,
    y_from_to: from_to_h,
    /,
) -> None:
    """
    Set main axes limits and scales
    """
    for from_to, set_lim, lim_names, set_scale in zip(
        (x_from_to, y_from_to),
        (axes.set_xlim, axes.set_ylim),
        (("left", "right"), ("bottom", "top")),
        (axes.set_xscale, axes.set_yscale),
    ):
        if from_to is not None:
            lim_prms = {lim_names[idx]: from_to[idx] for idx in (0, 1)}
            set_lim(**lim_prms)
            if (from_to.__len__() > 2) and (from_to[2] is not None):
                set_scale(from_to[2])


def _HideAlmostAllDecorations(axes: axes_t, /, *, sides: Sequence[str] = None) -> None:
    """
    Hide all decorations but appropriate spines
    """
    if sides is None:
        sides = []
        _, _, xbot_props, _, ylef_props, *_ = axes.__mp36_axes_properties__
        if xbot_props is not None:
            sides.append("bottom")
        if ylef_props is not None:
            sides.append("left")

    tick_params = {
        "axis": "both",
        "which": "both",
    }

    for looping_side in AXES_SIDES:
        axes.spines[looping_side].set_visible(looping_side in sides)
        tick_params[looping_side] = False
        tick_params["label" + looping_side] = False

    axes.tick_params(**tick_params)


def _SetSpineColors(axes: axes_t, /) -> None:
    """"""
    (
        twin_axes_for_xtop,
        twin_axes_for_yrig,
        xbot_props,
        xtop_props,
        ylef_props,
        yrig_props,
        *_,
    ) = axes.__mp36_axes_properties__
    all_axes_props = (xbot_props, xtop_props, ylef_props, yrig_props)

    # bottom, top, left, right
    all_axes = (axes, twin_axes_for_xtop, axes, twin_axes_for_yrig)

    # --- Spine colors
    for one_axes, props, side in zip(all_axes, all_axes_props, AXES_SIDES):
        if (props is not None) and (props["spine_color"] is not None):
            one_axes.spines[side].set_color(props["spine_color"])


def _ReapplyAxesDecorations(axes: axes_t, /) -> None:
    """"""
    _SynchronizeAxes(axes)
    _SetTickAndGridProperties(axes)
    _SetAdditionalTickProperties(axes)
    _SetAdditionalGridProperties(axes)


def _SynchronizeAxes(axes: axes_t, /) -> None:
    """"""
    (
        twin_axes_for_xtop,
        twin_axes_for_yrig,
        *_,
    ) = axes.__mp36_axes_properties__
    twin_axes = (twin_axes_for_xtop, twin_axes_for_yrig)

    for one_axes in twin_axes:
        if one_axes is None:
            continue

        # Invert (if required) before setting limits
        if axes.xaxis_inverted():
            one_axes.invert_xaxis()
        if axes.yaxis_inverted():
            one_axes.invert_yaxis()
        one_axes.xaxis.set_units(axes.xaxis.get_units())
        one_axes.yaxis.set_units(axes.yaxis.get_units())
        one_axes.set_xlim(*axes.get_xlim())
        one_axes.set_ylim(*axes.get_ylim())
        one_axes.set_xscale(axes.get_xscale())
        one_axes.set_yscale(axes.get_yscale())
        one_axes.set_position(axes.get_position(original=True))
        one_axes.set_aspect(axes.get_aspect())
        one_axes.set_box_aspect(axes.get_box_aspect())
        one_axes.set_adjustable(axes.get_adjustable())
        one_axes.set_anchor(axes.get_anchor())
        one_axes.set_autoscalex_on(axes.get_autoscalex_on())
        one_axes.set_autoscaley_on(axes.get_autoscaley_on())


def _SetTickAndGridProperties(axes: axes_t, /) -> None:
    """
    Ticks and grid properties through Axes.tick_params
    """
    (
        twin_axes_for_xtop,
        twin_axes_for_yrig,
        xbot_props,
        xtop_props,
        ylef_props,
        yrig_props,
        xgrid_props,
        ygrid_props,
    ) = axes.__mp36_axes_properties__

    # bottom, top, left, right
    all_axes = (axes, twin_axes_for_xtop, axes, twin_axes_for_yrig)

    all_axes_props = (xbot_props, xtop_props, ylef_props, yrig_props)
    all_grid_props = (xgrid_props, None, ygrid_props, None)

    for one_axes, props, grid_props, side in zip(
        all_axes,
        all_axes_props,
        all_grid_props,
        AXES_SIDES,
    ):
        if props is not None:
            # Unfortunately, the ""label" + side" property is not respected by a later call to set_label_text. Its
            # assignment is done anyway for... well no objective reason.
            major_tick_prms = {
                "axis": XY_FROM_SIDE[side],
                "which": "major",
                side: props["show_ticks"],
                "label" + side: props["show_tick_labels"],
            }
            for prop_name in MPLB_PRM_FROM_TICK_PROP.keys():
                if props[prop_name] is not None:
                    major_tick_prms[MPLB_PRM_FROM_TICK_PROP[prop_name]] = props[
                        prop_name
                    ]
            #
            if grid_props is not None:
                for prop_name in MPLB_PRM_FROM_GRID_PROP.keys():
                    if grid_props[prop_name] is not None:
                        major_tick_prms[
                            MPLB_PRM_FROM_GRID_PROP[prop_name]
                        ] = grid_props[prop_name]
            #
            one_axes.tick_params(**major_tick_prms)


def _SetAdditionalTickProperties(axes: axes_t, /) -> None:
    """
    Additional ticks properties not managed by Axes.tick_params
    """
    (
        twin_axes_for_xtop,
        twin_axes_for_yrig,
        xbot_props,
        xtop_props,
        ylef_props,
        yrig_props,
        *_,
    ) = axes.__mp36_axes_properties__

    all_axes_props = (xbot_props, xtop_props, ylef_props, yrig_props)

    if twin_axes_for_xtop is None:
        xaxis_top = None
    else:
        xaxis_top = twin_axes_for_xtop.xaxis
    if twin_axes_for_yrig is None:
        yaxis_rig = None
    else:
        yaxis_rig = twin_axes_for_yrig.yaxis
    for props, axis, get_lim, side in zip(
        all_axes_props,
        (axes.xaxis, xaxis_top, axes.yaxis, yaxis_rig),
        (axes.get_xlim, axes.get_xlim, axes.get_ylim, axes.get_ylim),
        AXES_SIDES,
    ):
        if props is None:
            continue
        #
        if props["show_ticks"] and (props["tick_positions"] is not None):
            axis.set_ticks(props["tick_positions"])
        if props["show_tick_labels"]:
            if props["tick_labels"] is not None:
                # If axis.set_ticks has not been called above, the following warning is issued:
                #     UserWarning: FixedFormatter should only be used together with FixedLocator
                axis.set_ticklabels(props["tick_labels"])
            elif props["tick_label_formatter"] is not None:
                if isinstance(props["tick_label_formatter"], Callable):
                    formatter = props["tick_label_formatter"]
                elif props["tick_label_formatter"] == "reversed":
                    formatter = lambda coord, _: f"{sum(get_lim()) - coord}"
                else:
                    raise ValueError(
                        f"{props['tick_label_formatter']}: Invalid tick label formatter"
                    )
                axis.set_major_formatter(ticker_t.FuncFormatter(formatter))
        if props["show_axis_label"] and props["axis_label"] is not None:
            if props["axis_label_color"] is None:
                color_prm = {}
            else:
                color_prm = {"color": props["axis_label_color"]}
            if props["axis_label_position"] is None:
                # Called to circumvent the non-respect of the ""label" + side" property set above with Axes.tick_params
                axis.set_label_position(side)
                axis.set_label_text(props["axis_label"], **color_prm)
            elif props["axis_label_position"] == "end":
                _SetAxisLabelAtEnd(
                    axes,
                    props["axis_label"],
                    side,
                    offset=props["axis_label_position_offset"],
                    **color_prm,
                )
            else:
                raise ValueError(
                    f"{props['axis_label_position']}: Invalid label position"
                )


def _SetAdditionalGridProperties(axes: axes_t, /) -> None:
    """
    Additional grid properties not managed by Axes.tick_params above
    """
    (
        *_,
        xgrid_props,
        ygrid_props,
    ) = axes.__mp36_axes_properties__

    # In fact, this should be done with Axes.tick_params
    for props, axis in zip((xgrid_props, ygrid_props), (axes.xaxis, axes.yaxis)):
        if (props is not None) and (props["which"] is not None):
            axis.grid(b=True, which=props["which"])


def _SetAxisLabelAtEnd(
    axes: axes_t,
    label: str,
    side: str,
    /,
    *,
    offset: Tuple[float, float] = None,
    **kwargs,
) -> None:
    """"""
    if offset is None:
        offset = (0.0, 0.0)

    if (side == "bottom") or (side == "top"):
        if side == "bottom":
            position = (1.0, 0.0)
        else:
            position = (1.0, 1.0)
        h_align = "left"
        v_align = "center_baseline"
    else:
        if side == "left":
            position = (0.0, 1.0)
        else:
            position = (1.0, 1.0)
        h_align = "center"
        v_align = "bottom"

    axes.annotate(
        label,
        xy=position,
        xytext=offset,
        ha=h_align,
        va=v_align,
        xycoords="axes fraction",
        textcoords="offset points",
        **kwargs,
    )


def AnglesAsFractionsOrMultiplesOfPi(
    *, min_factor: float = 0.0, max_factor: float = 2.0, n_angles: int = 4
) -> Tuple[str, ...]:
    #
    output = []

    factors = nmpy.linspace(min_factor, max_factor, num=n_angles)
    rational_factors = (rational_t(factor) for factor in factors)

    latex_pi = r"\pi"

    for factor in rational_factors:
        if factor == 0.0:
            angle_as_str = "0"
        elif factor == 1.0:
            angle_as_str = latex_pi
        elif factor.numerator == 1.0:
            angle_as_str = latex_pi + "/" + factor.denominator.__str__()
        elif factor.denominator == 1.0:
            angle_as_str = factor.numerator.__str__() + latex_pi
        else:
            angle_as_str = (
                factor.numerator.__str__()
                + latex_pi
                + "/"
                + factor.denominator.__str__()
            )

        output.append("$" + angle_as_str + "$")

    return tuple(output)


def RemoveColorbarFromAxes(axes: axes_t, /) -> None:
    """"""
    colorbar = axes.get_images()[0].colorbar
    if colorbar is not None:
        colorbar.remove()
