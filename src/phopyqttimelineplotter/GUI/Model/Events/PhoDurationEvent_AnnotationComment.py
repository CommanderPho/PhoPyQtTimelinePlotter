# PhoEvent.py
# Contains the different shapes to draw and what they represent (instantaneous events, intervals, etc)
# https://www.e-education.psu.edu/geog489/node/2301
# https://wiki.python.org/moin/PyQt/Making%20non-clickable%20widgets%20clickable

import sys
from datetime import datetime, timedelta, timezone

import numpy as np
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QEvent, QObject, QPoint, QRect, QSize, Qt, pyqtSignal
from PyQt5.QtGui import (
    QBrush,
    QColor,
    QFont,
    QFontMetrics,
    QPainter,
    QPainterPath,
    QPen,
    QPolygon,
    QRegion,
)
from PyQt5.QtWidgets import (
    QFormLayout,
    QFrame,
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
)

from phopyqttimelineplotter.GUI.Model.Events.PhoDurationEvent import *
from phopyqttimelineplotter.GUI.Model.Events.PhoEvent import *
from phopyqttimelineplotter.GUI.UI.TrianglePainter import *


class PhoDurationEvent_AnnotationComment(PhoDurationEvent):
    InstantaneousEventDuration = timedelta(minutes=30)
    RectCornerRounding = 2
    ColorBase = QColor(51, 255, 102, PhoEvent.DefaultOpacity)  # Teal
    ColorEmph = QColor(31, 200, 62, PhoEvent.DefaultOpacity)  # Green
    ColorActive = QColor(255, 102, 51, PhoEvent.DefaultOpacity)  # Orange

    ColorNibHandleActive = QColor(255, 102, 51, PhoEvent.DefaultOpacity)  # Orange

    ColorBorderBase = QColor("#e0e0e0")  # Whiteish
    ColorBorderActive = QColor(255, 222, 122)  # Yellowish

    MainTextFont = QFont("SansSerif", 12)
    SecondaryTextFont = QFont("SansSerif", 10)
    BodyTextFont = QFont("SansSerif", 8)

    NibTriangleHeight = 10.0
    NibTriangleWidth = 10.0

    LeftNibPainter = TrianglePainter(TriangleDrawOption_Horizontal.LeftApex)
    RightNibPainter = TrianglePainter(TriangleDrawOption_Horizontal.RightApex)

    # This defines a signal called 'on_edit' that takes no arguments
    on_edit_by_dragging_handle_start = pyqtSignal(int, int)
    on_edit_by_dragging_handle_end = pyqtSignal(int, int)

    def __init__(
        self,
        startTime=datetime.now(),
        endTime=None,
        name="",
        title="",
        subtitle="",
        color=QColor(31, 200, 62, PhoEvent.DefaultOpacity),
        extended_data=dict(),
        parent=None,
    ):
        super(PhoDurationEvent_AnnotationComment, self).__init__(
            startTime, endTime, name, color, extended_data, parent=parent
        )
        self.title = title
        self.subtitle = subtitle

        self.finalEventRect = QRect()
        self.start_poly = None
        self.start_poly_is_active = False

        self.end_poly = None
        self.end_poly_is_active = False

        self._drag_position = None

        # Can I get a double click effect?

    # overrides:
    def set_state_selected(self):
        super().set_state_selected()

    def set_state_deselected(self):
        super().set_state_deselected()
        self.start_poly_is_active = False
        self.end_poly_is_active = False

    def set_state_emphasized(self):
        super().set_state_emphasized()

    def set_state_deemphasized(self):
        super().set_state_deemphasized()

    # Direct override for menu items
    def buildMenu(self):
        self.menu = QMenu()
        self.info_action = self.menu.addAction("Get Info")
        self.modify_action = self.menu.addAction("Modify Comment...")
        self.delete_action = self.menu.addAction("Delete...")
        return self.menu

    def showMenu(self, pos):
        print("PhoDurationEvent_AnnotationComment.showMenu(pos: {0})".format(str(pos)))
        curr_child_index = self.get_track_index()

        self.menu = self.buildMenu()
        action = self.menu.exec(self.mapToGlobal(pos))
        if action == self.info_action:
            print("PhoDurationEvent_AnnotationComment: Get Info action!")
            self.on_info.emit(curr_child_index)
        elif action == self.modify_action:
            print("PhoDurationEvent_AnnotationComment: Modify Comment action!")
            self.on_edit.emit(curr_child_index)
        elif action == self.delete_action:
            print("PhoDurationEvent_AnnotationComment: Delete action!")
            self.on_delete.emit(curr_child_index)
        else:
            print("PhoDurationEvent_AnnotationComment: Unknown menu option!!")

        # self.menu.hide()
        # self.menu = None
        # self.menu.close()

    def on_button_clicked(self, event):
        # self.set_state_selected()
        print(
            "PhoDurationEvent_AnnotationComment.on_button_clicked({0})".format(
                str(event)
            )
        )
        if self.start_poly:
            currPoint = event.pos()
            self.start_poly_is_active = self.start_poly.containsPoint(
                currPoint, Qt.OddEvenFill
            )
        else:
            self.start_poly_is_active = False

        if self.end_poly:
            currPoint = event.pos()
            self.end_poly_is_active = self.end_poly.containsPoint(
                currPoint, Qt.OddEvenFill
            )
        else:
            self.end_poly_is_active = False

        # Only allow one active at a time
        if self.start_poly_is_active:
            startPos = self.finalEventRect.x()
            self._drag_position = startPos
            self.on_edit_by_dragging_handle_start.emit(
                self.get_track_index(), self._drag_position
            )
        elif self.end_poly_is_active:
            startPos = (
                self.finalEventRect.x() + self.finalEventRect.width()
            ) - PhoDurationEvent_AnnotationComment.NibTriangleWidth
            self._drag_position = startPos
            self.on_edit_by_dragging_handle_end.emit(
                self.get_track_index(), self._drag_position
            )
        else:
            self._drag_position = None

        self.update()

    def on_button_released(self, event):
        print(
            "PhoDurationEvent_AnnotationComment.on_button_released({0})".format(
                str(event)
            )
        )
        self.set_state_deselected()

        if not (self._drag_position is None):
            changeInX = 0.0
            print(self._drag_position)
            # Only allow one active at a time
            if self.start_poly_is_active:
                startPos = self.finalEventRect.x()
                changeInX = startPos - self._drag_position
                print("Change in X: {0}".format(changeInX))
                self.on_edit_by_dragging_handle_start.emit(
                    self.get_track_index(), self._drag_position
                )
                self.start_poly_is_active = False

            elif self.end_poly_is_active:
                startPos = (
                    self.finalEventRect.x() + self.finalEventRect.width()
                ) - PhoDurationEvent_AnnotationComment.NibTriangleWidth
                changeInX = startPos - self._drag_position
                print("Change in X: {0}".format(changeInX))
                self.on_edit_by_dragging_handle_end.emit(
                    self.get_track_index(), self._drag_position
                )
                self.end_poly_is_active = False
            else:
                pass

        # TODO: use the delta to compute the change

        # Clear drag position
        self._drag_position = None
        self.start_poly_is_active = False
        self.end_poly_is_active = False

        if event.button() == Qt.LeftButton:
            print(
                "PhoDurationEvent_AnnotationComment.on_button_released(...): Left click"
            )
        elif event.button() == Qt.RightButton:
            print(
                "PhoDurationEvent_AnnotationComment.on_button_released(...): Right click"
            )
            currPos = self.finalEventRect.topLeft()
            self.showMenu(currPos)
        elif event.button() == Qt.MiddleButton:
            print(
                "PhoDurationEvent_AnnotationComment.on_button_released(...): Middle click"
            )
        else:
            print(
                "PhoDurationEvent_AnnotationComment.on_button_released(...): Unknown click event!"
            )

        self.update()

    def mouseMoveEvent(self, e):
        print("PhoDurationEvent_AnnotationComment.mouseMoveEvent({0})".format(str(e)))

        # p = QPoint(e.x() + self.geometry().x(), e.y() + self.geometry().y())

        p = QPoint(e.x() + self.geometry().x(), e.y() + self.geometry().y())

        # self.updateEdgeAndCornerContainerActivePosition(e.pos(), True)
        # self.updateEdgeAndCornerContainerActivePosition(e.globalPos(), True)
        self.updateEdgeAndCornerContainerActivePosition(p, True)

        # If drag active, move the stop.
        if not (self._drag_position is None):
            self._drag_position = e.x()
            # Only allow one active at a time
            if self.start_poly_is_active:
                self.on_edit_by_dragging_handle_start.emit(
                    self.get_track_index(), self._drag_position
                )
            elif self.end_poly_is_active:
                self.on_edit_by_dragging_handle_end.emit(
                    self.get_track_index(), self._drag_position
                )
            else:
                pass

            self.update()

        # Call the default implementation to allow passing the events through. Doesn't make much sense in the main window
        QWidget.mouseMoveEvent(self, event)

    def on_key_pressed(self, event):
        gey = event.key()
        self.func = (None, None)
        if gey == Qt.Key_M:
            print("PhoDurationEvent_AnnotationComment: Key 'm' pressed!")
        elif gey == Qt.Key_Right:
            print(
                "PhoDurationEvent_AnnotationComment: Right key pressed!, call drawFundBlock()"
            )
            # self.func = (self.drawFundBlock, {})
            self.mModified = True

    # def reset_triangles(self):
    #     self.start_poly_is_active = False
    #     self.end_poly_is_active = False
    #     self.update()

    # "pass": specifies that we're leaving this method "virtual" or intensionally empty to be overriden by a subclass.
    def paint(
        self,
        painter,
        totalStartTime,
        totalEndTime,
        totalDuration,
        totalParentCanvasRect,
    ):
        # "total*" refers to the parent frame in which this event is to be drawn
        # totalStartTime, totalEndTime, totalDuration, totalParentCanvasRect
        parentOffsetRect = self.compute_parent_offset_rect(
            totalStartTime,
            totalEndTime,
            totalDuration,
            totalParentCanvasRect.width(),
            totalParentCanvasRect.height(),
        )
        x = parentOffsetRect.x() + totalParentCanvasRect.x()
        y = parentOffsetRect.y() + totalParentCanvasRect.y()
        width = parentOffsetRect.width()
        height = parentOffsetRect.height()

        self.finalEventRect = QRect(x, y, width, height)
        # painter.setPen( QtGui.QPen( Qt.darkBlue, 2, join=Qt.MiterJoin ) )

        # Construct the nibs:
        halfNibOffset = PhoDurationEvent_AnnotationComment.NibTriangleWidth / 2.0

        # Offset the rect by the nibs
        body_y = y + PhoDurationEvent_AnnotationComment.NibTriangleHeight
        body_height = height - PhoDurationEvent_AnnotationComment.NibTriangleHeight
        bodyRect = QRect(x, body_y, width, body_height)

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)

        if self.is_deemphasized:
            activeColor = Qt.lightGray
        else:
            # de-emphasized overrides emphasized status
            if self.is_emphasized:
                activeColor = PhoDurationEvent_AnnotationComment.ColorEmph
            else:
                activeColor = self.color

        if self.is_active:
            painter.setPen(
                QtGui.QPen(
                    PhoDurationEvent_AnnotationComment.ColorBorderActive,
                    2.0,
                    join=Qt.MiterJoin,
                )
            )
            painter.setBrush(
                QBrush(PhoDurationEvent_AnnotationComment.ColorActive, Qt.SolidPattern)
            )
        else:
            painter.setPen(
                QtGui.QPen(
                    PhoDurationEvent_AnnotationComment.ColorBorderBase,
                    0.8,
                    join=Qt.MiterJoin,
                )
            )
            painter.setBrush(QBrush(activeColor, Qt.SolidPattern))

        # Draw start triangle nib
        startPos = x
        self.start_poly = PhoDurationEvent_AnnotationComment.LeftNibPainter.get_poly(
            startPos,
            PhoDurationEvent_AnnotationComment.NibTriangleHeight,
            PhoDurationEvent_AnnotationComment.NibTriangleWidth,
        )
        self.start_poly_region = QRegion(self.start_poly)

        self.body_region = QRegion(x, body_y, width, body_height)

        if self.is_instantaneous_event():
            # Instantaneous type event
            # painter.setPen(Qt.NoPen)
            if self.is_emphasized:
                penWidth = 1.0
            else:
                penWidth = 0.2

            ## NOTE: Apparently for events as small as the instantaneous events (with a width of 2) the "Brush" or "fill" doesn't matter, only the stroke does.
            painter.setPen(QtGui.QPen(activeColor, penWidth, join=Qt.MiterJoin))
            painter.drawRect(x, body_y, width, body_height)

            # Draw Nib:
            if self.start_poly_is_active:
                painter.setPen(
                    QtGui.QPen(
                        PhoDurationEvent_AnnotationComment.ColorBorderActive,
                        1.0,
                        join=Qt.MiterJoin,
                    )
                )
                painter.setBrush(
                    QBrush(
                        PhoDurationEvent_AnnotationComment.ColorNibHandleActive,
                        Qt.SolidPattern,
                    )
                )
            else:
                painter.setPen(
                    QtGui.QPen(
                        PhoDurationEvent_AnnotationComment.ColorBorderBase,
                        penWidth,
                        join=Qt.MiterJoin,
                    )
                )
                painter.setBrush(QBrush(activeColor, Qt.SolidPattern))

            self.final_region_mask = self.body_region.united(self.start_poly_region)
            painter.setClipRegion(self.final_region_mask)

            painter.drawPolygon(self.start_poly)
        else:
            # Normal duration event (like for videos)
            painter.drawRoundedRect(
                x,
                body_y,
                width,
                body_height,
                PhoDurationEvent_AnnotationComment.RectCornerRounding,
                PhoDurationEvent_AnnotationComment.RectCornerRounding,
            )

            startPos = (x + width) - PhoDurationEvent_AnnotationComment.NibTriangleWidth
            self.end_poly = PhoDurationEvent_AnnotationComment.RightNibPainter.get_poly(
                startPos,
                PhoDurationEvent_AnnotationComment.NibTriangleHeight,
                PhoDurationEvent_AnnotationComment.NibTriangleWidth,
            )
            self.end_poly_region = QRegion(self.end_poly)

            self.final_region_mask = self.body_region.united(
                self.start_poly_region
            ).united(self.end_poly_region)
            painter.setClipRegion(self.final_region_mask)

            # If it's not an instantaneous event, draw the label
            self.titleHeight = self.precompute_text_height(
                PhoDurationEvent_AnnotationComment.MainTextFont
            )
            self.titleLabelRect = QRect(x, body_y, width, self.titleHeight)
            self.subtitleHeight = self.precompute_text_height(
                PhoDurationEvent_AnnotationComment.SecondaryTextFont
            )
            self.subtitleLabelRect = QRect(
                x, (body_y + self.titleHeight), width, self.subtitleHeight
            )
            self.bodyTextLabelRect = QRect(
                x,
                self.subtitleLabelRect.bottom(),
                width,
                (bodyRect.height() - (self.titleHeight + self.subtitleHeight)),
            )
            # PhoDurationEvent_AnnotationComment.BodyTextFont

            # painter.drawText(bodyRect, Qt.AlignTop|Qt.AlignHCenter, self.title)
            # painter.drawText(bodyRect, Qt.AlignHCenter|Qt.AlignCenter, self.subtitle)
            # painter.drawText(bodyRect, Qt.AlignBottom|Qt.AlignHCenter, self.name)

            painter.setFont(PhoDurationEvent_AnnotationComment.MainTextFont)
            painter.drawText(self.titleLabelRect, Qt.AlignCenter, self.title)
            painter.setFont(PhoDurationEvent_AnnotationComment.SecondaryTextFont)
            painter.drawText(self.subtitleLabelRect, Qt.AlignCenter, self.subtitle)
            painter.setFont(PhoDurationEvent_AnnotationComment.BodyTextFont)
            painter.drawText(self.bodyTextLabelRect, Qt.AlignCenter, self.name)

            # Draw Nibs:
            self.hoveredEdgeAndCorners = EdgeAndCornerContainerComponent.NONE

            if self.start_poly_is_active:
                painter.setPen(
                    QtGui.QPen(
                        PhoDurationEvent_AnnotationComment.ColorBorderActive,
                        1.0,
                        join=Qt.MiterJoin,
                    )
                )
                painter.setBrush(
                    QBrush(
                        PhoDurationEvent_AnnotationComment.ColorNibHandleActive,
                        Qt.SolidPattern,
                    )
                )
                self.hoveredEdgeAndCorners = EdgeAndCornerContainerComponent.Edge_Left
            else:
                painter.setPen(
                    QtGui.QPen(
                        PhoDurationEvent_AnnotationComment.ColorBorderBase,
                        0.8,
                        join=Qt.MiterJoin,
                    )
                )
                painter.setBrush(QBrush(activeColor, Qt.SolidPattern))

            painter.drawPolygon(self.start_poly)

            if self.end_poly_is_active:
                painter.setPen(
                    QtGui.QPen(
                        PhoDurationEvent_AnnotationComment.ColorBorderActive,
                        1.0,
                        join=Qt.MiterJoin,
                    )
                )
                painter.setBrush(
                    QBrush(
                        PhoDurationEvent_AnnotationComment.ColorNibHandleActive,
                        Qt.SolidPattern,
                    )
                )
                self.hoveredEdgeAndCorners = EdgeAndCornerContainerComponent.Edge_Right
            else:
                painter.setPen(
                    QtGui.QPen(
                        PhoDurationEvent_AnnotationComment.ColorBorderBase,
                        0.8,
                        join=Qt.MiterJoin,
                    )
                )
                painter.setBrush(QBrush(activeColor, Qt.SolidPattern))

            painter.drawPolygon(self.end_poly)

        self.paintEvent_EdgeAndCornerContainerViewMixin(painter, self.finalEventRect)

        painter.restore()

        self.setMask(self.final_region_mask)
        return self.finalEventRect

    ## GUI CLASS
