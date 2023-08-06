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

from typing import Any, Callable, Dict, Final, Tuple, Union

import numpy as nmpy
from matplotlib import cm as clmp
from matplotlib import tri as mptr


array_t = nmpy.ndarray

number_h: Final = Union[int, float]
plot_config_h: Final = Dict[str, Any]


def XYHeightConfig(
    height,
    x_coords: Union[Tuple[number_h, number_h], array_t] = None,
    y_coords: Union[Tuple[number_h, number_h], array_t] = None,
    /,
    **kwargs,
) -> plot_config_h:
    """
    If x_coords (y_coords) is None, row (col) coordinates are generated instead
    """
    x_coords = _ArrayFromCoords(x_coords, height.shape[0])
    y_coords = _ArrayFromCoords(y_coords, height.shape[1])
    grid_x_coords, grid_y_coords = nmpy.meshgrid(x_coords, y_coords, indexing="ij")

    if kwargs.__len__() > 0:
        config = kwargs
    else:
        config = {"cmap": clmp.plasma}

    output = {
        "ndim": 3,
        "type": "plot_surface",
        "data": (grid_x_coords, grid_y_coords, height),
        "config": config,
    }

    return output


def _ArrayFromCoords(
    coords: Union[Tuple[number_h, number_h], array_t], n_elements: int, /
) -> array_t:
    """"""
    if coords is None:
        output = tuple(range(n_elements))
    elif isinstance(coords, tuple):
        if coords.__len__() == 2:
            output = nmpy.linspace(*coords, num=n_elements)
        else:
            raise ValueError(
                f"{coords.__len__()}: Invalid coordinate tuple length; Expected_2"
            )
    elif isinstance(coords, array_t):
        if coords.shape == (n_elements,):
            output = coords
        else:
            raise ValueError(
                f"{coords.shape}: Invalid coordinate array shape; Expected_{(n_elements,)}"
            )
    else:
        raise ValueError(
            f"{type(coords)}: Invalid coordinate type; Expected_None, 2-tuple of numbers, numpy ndarray"
        )

    return output


def ParametricSurfaceConfig(
    params_u: array_t,
    params_v: array_t,
    XCoords: Callable[[array_t, array_t], array_t],
    YCoords: Callable[[array_t, array_t], array_t],
    ZCoords: Callable[[array_t, array_t], array_t],
    /,
    **kwargs,
) -> plot_config_h:
    """"""
    if kwargs.__len__() > 0:
        config = kwargs
    else:
        config = {"cmap": clmp.plasma}

    grid_params_u, grid_params_v = nmpy.meshgrid(params_u, params_v)
    all_params_u = grid_params_u.flatten()
    all_params_v = grid_params_v.flatten()
    triangulation = mptr.Triangulation(all_params_u, all_params_v)
    config["triangles"] = triangulation.triangles

    x_coords = XCoords(all_params_u, all_params_v)
    y_coords = YCoords(all_params_u, all_params_v)
    z_coords = ZCoords(all_params_u, all_params_v)

    output = {
        "ndim": 3,
        "type": "plot_trisurf",
        "data": (x_coords, y_coords, z_coords),
        "config": config,
    }

    return output
