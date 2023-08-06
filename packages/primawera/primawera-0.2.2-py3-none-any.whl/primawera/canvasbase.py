from functools import partial
from typing import Optional, Dict, List, Union

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QAction
from numpy.typing import ArrayLike

import primawera.lut as lut
from primawera.filters import linear_contrast, gamma_correction
from primawera.previewwindow import PreviewDialog


class CanvasBase(QWidget):
    menus_changed_signal = pyqtSignal()

    def __init__(self, data: ArrayLike, mode: str,
                 desktop_height: int, desktop_width: int,
                 filters: Optional[Dict[str, bool]] = None,
                 filters_options: Optional[Dict[str, int]] = None, *args,
                 **kwargs) -> None:
        super(CanvasBase, self).__init__(*args, **kwargs)
        self.data = data
        self.filters = filters
        self.filters_options = filters_options
        self.lut = None
        self.mode = mode
        # This may change, for example when applying LUTs.
        self.mode_visualisation = mode
        self.preview_dialog_value = 0

        self.axes_orientation = (0, 1, 2)
        self.desktop_height = desktop_height
        self.desktop_width = desktop_width
        if self.mode == "":
            raise RuntimeError("Empty mode encountered")

    def _init_interface(self):
        self.main_layout = QVBoxLayout()
        self.view_layout = QGridLayout()
        self.coordinates_label = QLabel("Please click on the image")
        self.main_layout.addWidget(self.coordinates_label, stretch=0)

    def _create_actions(self):
        self.no_filter_action = QAction("None")
        self.logarithm_stretch_action = QAction("Logarithm stretch.")
        self.linear_stretch_action = QAction("Linear stretch.")
        self.linear_contrast_action = QAction("Linear contrast.")
        self.gamma_correction_action = QAction("Gamma correction.")
        self.lut_actions = []
        self.lut_actions.append(("None", QAction("None")))
        for lut_name in lut.LUTS.keys():
            self.lut_actions.append((lut_name, QAction(lut_name)))

    def _connect_actions(self):
        self.no_filter_action.triggered.connect(self._no_filter)
        self.logarithm_stretch_action.triggered.connect(
            self._logarithm_stretch)
        self.linear_stretch_action.triggered.connect(self._linear_stretch)
        self.linear_contrast_action.triggered.connect(self._linear_contrast)
        self.gamma_correction_action.triggered.connect(self._gamma_correction)
        for lut_name, lut_action in self.lut_actions:
            lut_action.triggered.connect(partial(self._apply_lut, lut_name))

    def _set_actions_checkable(self) -> None:
        for action in self.get_actions():
            action.setCheckable(True)

    def _no_filter(self):
        self.filters.clear()
        self._redraw(self._process_data())
        self.current_filter_name = "No filter"

    def _linear_stretch(self):
        self.filters = {"linear_stretch": True}

        self._redraw(self._process_data())
        self.current_filter_name = "Linearly stretched"

    def _logarithm_stretch(self):
        self.filters = {"logarithm_stretch": True}
        self._redraw(self._process_data())
        self.current_filter_name = "Logarithmically stretched."

    def _linear_contrast(self):
        dialog = PreviewDialog(self.data, [("Factor", int, 100, 0, 1)],
                               self.mode, linear_contrast)
        dialog.return_signal.connect(self.preview_dialog_slot)
        ret = dialog.exec()
        if ret == 0:
            return
        factor = self.preview_dialog_value
        self.filters = {"linear_contrast": True}
        self.filters_options = {"factor": float(factor)}
        self._redraw(self._process_data())
        self.current_filter_name = "Linearly adjusted contrast"

    def _gamma_correction(self):
        dialog = PreviewDialog(self.data, [("Factor", float, 2.0, 0.0, 0.1)],
                               self.mode, gamma_correction)
        dialog.return_signal.connect(self.preview_dialog_slot)
        ret = dialog.exec()
        if ret == 0:
            return
        factor = self.preview_dialog_value
        self.filters = {"gamma_correction": True}
        self.filters_options = {"factor": factor}
        self._redraw(self._process_data())
        self.current_filter_name = "Gamma corrected"

    def _apply_lut(self, name):
        if name == "None":
            self.mode_visualisation = self.mode
            self.lut = None
        else:
            self.lut = lut.get_lut(name)
        self._redraw(self._process_data())

    def _redraw(self, new_data):
        raise NotImplementedError("CanvasBase should not be directly created!")

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key_Plus:
            self._increase_zoom_level()
        elif event.key() == QtCore.Qt.Key_Minus:
            self._decrease_zoom_level()
        else:
            event.ignore()

    def _increase_zoom_level(self):
        raise NotImplementedError("CanvasBase should not be directly created!")

    def _decrease_zoom_level(self):
        raise NotImplementedError("CanvasBase should not be directly created!")

    def get_filters(self):
        raise NotImplementedError("CanvasBase should not be directly created!")

    def get_luts(self):
        raise NotImplementedError("CanvasBase should not be directly created!")

    def get_actions(self):
        raise NotImplementedError("CanvasBase should not be directly created!")

    def get_menus(self):
        raise NotImplementedError("CanvasBase should not be directly created!")

    def _process_data(self):
        raise NotImplementedError("CanvasBase should not be directly created!")

    def update_desktop_size(self, width: int, height: int) -> None:
        # TODO: this does not affect anything.
        self.desktop_width = width
        self.desktop_height = height

    @pyqtSlot(list)
    def preview_dialog_slot(self, data: List[Union[int, float]]) -> None:
        self.preview_dialog_value = data[0]
