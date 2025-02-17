import math
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QEvent, QObject, QPoint, QRect, QSize, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QBrush, QColor, QFont, QFontMetrics, QPainter, QPen
from PyQt5.QtWidgets import (
    QFormLayout,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMenu,
    QMessageBox,
    QPushButton,
    QSplitter,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QToolTip,
    QVBoxLayout,
    QWidget,
)

# from phopyqttimelineplotter.GUI.Model.Events.PhoDurationEvent import *

# ThumbnailDrawingEventMixin.py

# INCLUDES:
# from phopyqttimelineplotter.GUI.Helpers.ThumbnailDrawingEventMixin import ThumbnailDrawingEventMixin


class ThumbnailDrawingEventMixin(object):
    """ThumbnailDrawingEventMixin: a mixin that draws thumbnail images on a timeline event
    Requires:
    self.desiredThumbnailSizeKey = "160"

    ## TODO: Doesn't work

    """

    def init_ThumbnailDrawingEventMixin(self):
        self.mainWidgetLayout = QGridLayout(self)

        self.desiredThumbnailSize = 40
        self.desiredThumbnailSizeKey = str(self.desiredThumbnailSize)
        self.max_num_horizontal_thumbnails = 5
        # A vertical box layout
        self.thumbnailsContainer = QWidget()
        self.thumbnailsLayout = QHBoxLayout()
        self.numThumbnailsHorizontal = self.get_num_thumbnails_horizontal()
        self.labels_array = []
        for index in range(0, self.max_num_horizontal_thumbnails):
            w = QLabel()
            # w.setPixmap(QtGui.QPixmap.fromImage(currThumbnailImage))
            self.labels_array.append(w)
            self.thumbnailsLayout.addWidget(w)

        self.thumbnailsContainer.setLayout(self.thumbnailsLayout)

        self.mainWidgetLayout.addWidget(self.thumbnailsContainer, 0, 0)

        # self.addWidget(self.thumbnailsContainer)

        # w.setPixmap(QtGui.QPixmap.fromImage(currThumbnailImage))

    def get_labels_array(self):
        return self.labels_array

    def get_num_thumbnails_horizontal(self):
        return math.floor(float(self.width()) / float(self.desiredThumbnailSize))

    @pyqtSlot(str, list)
    def on_thumbnails_loaded(self, filename, generated_thumbnails_list):
        print("on_thumbnails_loaded(...)")
        print(
            "thumbnail generation complete for [{0}]: {1} frames".format(
                str(filename), len(generated_thumbnails_list)
            )
        )
        # Iterate through the generated thumbnails and render them
        for (index, aVideoThumbnailObj) in enumerate(generated_thumbnails_list):
            currThumbsDict = aVideoThumbnailObj.get_thumbs_dict()
            # currThumbnailImage: should be a QImage
            currThumbnailImage = currThumbsDict[self.desiredThumbnailSizeKey]
            w = self.get_labels_array()[index]
            w.setPixmap(QtGui.QPixmap.fromImage(currThumbnailImage))
            # w.isHidden((index > self.get_num_thumbnails_horizontal()))

    pass
