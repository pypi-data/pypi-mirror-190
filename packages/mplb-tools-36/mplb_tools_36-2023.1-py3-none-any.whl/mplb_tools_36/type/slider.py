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

from matplotlib.widgets import Slider as slider_t
from mplb_tools_36.type.axes import axes_image_t, axes_t, ticker_t
from numpy import ndarray as array_t


STACK_SLIDER_WIDTH = "8%"
STACK_SLIDER_PADDING = 0.075


class stack_slider_t(slider_t):
    __slots__ = ("img", "mplb_img")

    img: array_t
    mplb_img: axes_image_t

    def __init__(
        self,
        slider_room: axes_t,
        img: array_t,
        mplb_img: axes_image_t,
        /,
        *args,
        **kwargs,
    ):
        """"""
        n_slices = img.shape[2]

        super().__init__(
            slider_room,
            args[0],
            0,
            n_slices - 1,
            valinit=0,
            valstep=1,
            *args[1:],
            **kwargs,
        )
        self.on_changed(self.ChangeDisplayedSlice)

        slider_room.set_xticks(())
        slider_room.set_yticks(tuple(range(n_slices)))
        slider_room.yaxis.set_minor_locator(ticker_t.AutoMinorLocator(2))
        tick_prms = {
            "axis": "y",
            "which": "major",
            "direction": "in",
            "left": False,
            "right": False,
            "pad": 0.03,
            "labelleft": True,
            "labelright": False,
            "labelsize": "xx-small",
            "labelcolor": "m",
        }
        slider_room.tick_params(**tick_prms)
        tick_prms["which"] = "minor"
        tick_prms["length"] = 4
        tick_prms["left"] = True
        tick_prms["right"] = True
        tick_prms["color"] = "m"
        tick_prms["labelleft"] = False
        slider_room.tick_params(**tick_prms)
        slider_room.set_navigate(True)  # Otherwise axes do not call format_coord
        slider_room.format_coord = lambda _, col: f"Switch to slice: {col:.0f}"

        self.img = img.copy()  # To avoid side effects
        self.mplb_img = mplb_img

    def ChangeDisplayedSlice(self, slider_value: float, /) -> None:
        """"""
        self.mplb_img.set_data(self.img[:, :, int(slider_value)])
        self.mplb_img.figure.canvas.draw_idle()
