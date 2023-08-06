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

from typing import Final

from mplb_tools_36.type.axes import axes_image_t, axes_t
from mplb_tools_36.type.base import figure_t, mouse_event_t


COLORBAR_WIDTH = "6%"
COLORBAR_PADDING = 0.1


SOME_COLORMAPS: Final = (
    "gray",
    # --- "Perceptually Uniform Sequential" (Matplotlib terminology)
    "cividis",
    "inferno",
    "magma",
    "plasma",
    "viridis",
    # --- "Sequential (2)" (Matplotlib terminology)
    "afmhot",
    "autumn",
    "bone",
    "cool",
    "copper",
    "gist_heat",
    "hot",
    "pink",
    "spring",
    "summer",
    "winter",
    "Wistia",
)
COLORBAR_AXES_FORMAT: Final = {
    "axis": "x",
    "which": "both",
    "top": True,
    "bottom": False,
    "length": 2,
    "color": "gray",
    "pad": 0.01,
    "labeltop": True,
    "labelbottom": False,
    "labelsize": "xx-small",
    "labelcolor": "gray",
}
COLORBAR_NAME_FORMAT: Final = {
    "fontsize": "xx-small",
    "color": "gray",
}


class dynamic_colorbar_t:
    __slots__ = ("reference", "mplb_img", "cmap_idx")

    reference: axes_t
    mplb_img: axes_image_t
    cmap_idx: int

    def __init__(
        self,
        figure: figure_t,
        colorbar_room: axes_t,
        mplb_img: axes_image_t,
        /,
        *args,
        **kwargs,
    ):
        """"""
        colorbar_room.set_picker(True)
        # Changing "pick" for one axes appears to, somehow, change it for any axes instance. For that reason,
        # "ChangeColormap" has to check the event "inaxes" property before proceeding (*)
        colorbar_room.pick = self.ChangeColormap

        figure.add_axes(colorbar_room)
        _ = figure.colorbar(mplb_img, cax=colorbar_room, *args, **kwargs)

        self.reference = colorbar_room
        self.mplb_img = mplb_img
        self.cmap_idx = 0

        self.AdjustDecorations()

    def AdjustDecorations(self) -> None:
        """"""
        title = f"{SOME_COLORMAPS[self.cmap_idx]} ({self.cmap_idx+1}/{SOME_COLORMAPS.__len__()})"
        self.reference.tick_params(**COLORBAR_AXES_FORMAT)
        self.reference.set_title(title, fontdict=COLORBAR_NAME_FORMAT, y=0.0, pad=-6)

    def ChangeColormap(self, event: mouse_event_t, /) -> None:
        """"""
        # See note in "__init__" about changing the "pick" property of axes regarding this test (*)
        if event.inaxes is self.reference:
            if event.key == "alt":
                step = -1
            else:
                step = 1
            self.cmap_idx = (self.cmap_idx + step) % SOME_COLORMAPS.__len__()
            self.mplb_img.set_cmap(SOME_COLORMAPS[self.cmap_idx])
            self.AdjustDecorations()
            self.mplb_img.figure.canvas.draw_idle()
