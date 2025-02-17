import sys
from datetime import datetime, timedelta, timezone
from enum import Enum

import numpy as np
from orangecanvas.gui.dock import CollapsibleDockWidget
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import (
    QDir,
    QEvent,
    QObject,
    QPoint,
    QRect,
    QSize,
    Qt,
    pyqtSignal,
    pyqtSlot,
)
from PyQt5.QtGui import QBrush, QColor, QFont, QIcon, QPainter, QPen, QStandardItem
from PyQt5.QtWidgets import (
    QApplication,
    QDockWidget,
    QFileSystemModel,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSplitter,
    QStackedWidget,
    QStyle,
    QTableWidget,
    QTableWidgetItem,
    QToolTip,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

from phopyqttimelineplotter.GUI.Model.TrackConfigs.AbstractTrackConfigs import *
from phopyqttimelineplotter.GUI.Model.TrackConfigs.VideoTrackConfig import *
from phopyqttimelineplotter.GUI.Model.TrackType import TrackConfigMixin, TrackType

# from phopyqttimelineplotter.GUI.UI.TimelineHeaderWidget.TimelineHeaderWidget import TimelineHeaderWidget

# _ContentsExpanded
# TimelineHeaderWidget_ContentsExpanded.ui
# TimelineHeaderWidget_ContentsCollapsed.ui


class TimelineHeaderWidget_ContentsCollapsed(QWidget):
    def __init__(self, parent=None):
        super(TimelineHeaderWidget_ContentsCollapsed, self).__init__(
            parent=parent
        )  # Call the inherited classes __init__ method
        self.ui = uic.loadUi(
            "GUI/UI/TimelineHeaderWidget/TimelineHeaderWidget_ContentsCollapsed.ui",
            self,
        )  # Load the .ui file
        self.initUI()
        self.show()  # Show the GUI

    def initUI(self):
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)


class TimelineHeaderWidget_ContentsExpanded(QWidget):
    def __init__(self, parent=None):
        super(TimelineHeaderWidget_ContentsExpanded, self).__init__(
            parent=parent
        )  # Call the inherited classes __init__ method
        self.ui = uic.loadUi(
            "GUI/UI/TimelineHeaderWidget/TimelineHeaderWidget_ContentsExpanded.ui", self
        )  # Load the .ui file
        self.initUI()
        self.show()  # Show the GUI

    def initUI(self):
        self.ui.lblTitle.setText(self.parent().track_name)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.ui.frame_TopButtons.setHidden(False)

        self.ui.btnToggleCollapse.setIcon(
            self.style().standardIcon(QStyle.SP_TitleBarShadeButton)
        )
        self.ui.btnToggleCollapse.setText("")
        self.ui.btnToggleCollapse.clicked.connect(self.parent().on_collapse_pressed)

        self.ui.btnOptions.setIcon(
            self.style().standardIcon(QStyle.SP_FileDialogDetailedView)
        )
        self.ui.btnOptions.setText("")
        self.ui.btnOptions.clicked.connect(self.parent().on_options_pressed)

        self.ui.btnRefresh.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        self.ui.btnRefresh.setText("")
        self.ui.btnRefresh.clicked.connect(self.parent().on_reload_pressed)

    def get_title(self):
        return self.ui.lblTitle.text()

    def get_body(self):
        return self.ui.textBrowser_Main.toPlainText()

    def set_title(self, updatedStr):
        self.ui.lblTitle.setText(updatedStr)

    def set_body(self, updatedStr):
        return self.ui.textBrowser_Main.setPlainText(updatedStr)


class TimelineHeaderWidget(TrackConfigMixin, QFrame):

    toggleCollapsed = pyqtSignal(int, bool)
    showOptions = pyqtSignal(int)
    refresh = pyqtSignal(int)

    def __init__(self, track_config, parent=None):
        super(TimelineHeaderWidget, self).__init__(
            parent=parent
        )  # Call the inherited classes __init__ method
        self.ui = uic.loadUi(
            "GUI/UI/TimelineHeaderWidget/TimelineHeaderWidget.ui", self
        )  # Load the .ui file
        self.track_config = track_config
        self.track_id = track_config.get_track_id()
        self.track_name = track_config.get_track_title()

        # self.enableDynamicLabelUpdating: if True, automatically updates the labels from the config. Otherwise relies on the manually set labels
        self.enableDynamicLabelUpdating = True

        # self.setAutoFillBackground(False)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)

        self.timelineHeaderWidget_ContentsCollapsed = (
            TimelineHeaderWidget_ContentsCollapsed(self)
        )
        self.timelineHeaderWidget_ContentsExpanded = (
            TimelineHeaderWidget_ContentsExpanded(self)
        )

        self.timelineHeaderWidget_ContentsExpanded.set_title(
            self.track_config.get_track_title()
        )
        self.timelineHeaderWidget_ContentsExpanded.set_body(
            self.track_config.get_track_extended_description()
        )

        self.initUI()
        self.show()  # Show the GUI

    def initUI(self):

        self.ui.dockWidget_Main = CollapsibleDockWidget(parent=self)
        self.ui.dockWidget_Main.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.ui.dockWidget_Main.setFeatures(
            self.ui.dockWidget_Main.features() | QDockWidget.DockWidgetVerticalTitleBar
        )
        self.ui.dockWidget_Main.setWindowTitle(self.track_name)
        self.layout().addWidget(self.ui.dockWidget_Main)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.ui.dockWidget_Main.setCollapsedWidget(
            self.timelineHeaderWidget_ContentsCollapsed
        )
        self.ui.dockWidget_Main.setExpandedWidget(
            self.timelineHeaderWidget_ContentsExpanded
        )

        return

    # TrackConfigMixin override
    def get_track_config(self):
        return self.track_config

    def update_from_config(self):
        self.track_id = self.track_config.get_track_id()
        self.track_name = self.track_config.get_track_title()
        self.set_title(self.track_config.get_track_title())
        self.set_body(self.track_config.get_track_extended_description())

    def get_config(self):
        return self.track_config

    def set_config(self, newConfig):
        self.track_config = newConfig
        if self.enableDynamicLabelUpdating:
            self.update_labels_dynamically()

    def get_title(self):
        return self.ui.lblTitle.text()

    def get_body(self):
        return self.ui.textBrowser_Main.toPlainText()

    def set_title(self, updatedStr):
        self.track_config.track_name = updatedStr
        self.timelineHeaderWidget_ContentsExpanded.set_title(updatedStr)
        self.ui.dockWidget_Main.setWindowTitle(updatedStr)

    def set_body(self, updatedStr):
        self.track_config.trackExtendedDescription = updatedStr
        return self.timelineHeaderWidget_ContentsExpanded.set_body(updatedStr)

    # update_labels_dynamically(): updates the labels dynamically from the active filter
    def update_labels_dynamically(self):
        self.track_config.update_labels_dynamically()
        self.update_from_config()
        return

    def on_collapse_pressed(self):
        print("on_collapse_pressed(...)")
        self.toggleCollapsed.emit(self.track_id, False)

    def on_options_pressed(self):
        print("on_options_pressed(...)")
        self.showOptions.emit(self.track_id)

    def on_reload_pressed(self):
        print("on_reload_pressed(...)")
        self.refresh.emit(self.track_id)

    def perform_collapse(self):
        # self.dockWidgetContents.setHidden(True)
        self.ui.dockWidget_Main.hide()

    def perform_expand(self):
        self.dockWidgetContents.setHidden(False)
