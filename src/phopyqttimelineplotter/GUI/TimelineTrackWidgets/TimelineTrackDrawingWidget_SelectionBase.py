# EventTrackDrawingWidget.py
# Contains EventTrackDrawingWidget which draws several PhoEvent objects as rectangles or lines within a single track.

import sys
from datetime import datetime, timedelta, timezone

import numpy as np
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QEvent, QObject, QPoint, QRect, QSize, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PyQt5.QtWidgets import (
    QComboBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMenu,
    QMessageBox,
    QPushButton,
    QSplitter,
    QToolTip,
    QVBoxLayout,
)

from phopyqttimelineplotter.GUI.TimelineTrackWidgets.TimelineTrackDrawingWidgetBase import (
    ItemSelectionOptions,
    TimelineTrackDrawingWidgetBase,
)

## IMPORT:
# from phopyqttimelineplotter.GUI.TimelineTrackWidgets.TimelineTrackDrawingWidget_SelectionBase import TimelineTrackDrawingWidget_SelectionBase

#  "A Base with selections"
#
class TimelineTrackDrawingWidget_SelectionBase(TimelineTrackDrawingWidgetBase):
    default_shouldDismissSelectionUponMouseButtonRelease = False
    default_itemSelectionMode = ItemSelectionOptions.SingleSelection
    default_itemHoverMode = ItemSelectionOptions.SingleSelection

    default_TrackTitleFont = QFont("Helvetica", 22)
    default_TrackTitlePen = QPen(Qt.gray)

    def __init__(
        self,
        trackID,
        totalStartTime,
        totalEndTime,
        durationObjects,
        database_connection,
        parent=None,
        wantsKeyboardEvents=True,
        wantsMouseEvents=True,
    ):
        super(TimelineTrackDrawingWidget_SelectionBase, self).__init__(
            trackID,
            totalStartTime,
            totalEndTime,
            database_connection=database_connection,
            parent=parent,
            wantsKeyboardEvents=wantsKeyboardEvents,
            wantsMouseEvents=wantsMouseEvents,
        )
        self.reloadModelFromDatabase()
        self.durationRecords = []
        self.durationObjects = durationObjects
        self.eventRect = np.repeat(QRect(0, 0, 0, 0), len(durationObjects))

        # Hovered Object
        self.hovered_object_index = None
        self.hovered_object = None
        self.hovered_object_rect = None
        self.hovered_duration_object_indicies = []

        # Selected Object
        self.selected_duration_object_indicies = []
        self.shouldDismissSelectionUponMouseButtonRelease = (
            TimelineTrackDrawingWidget_SelectionBase.default_shouldDismissSelectionUponMouseButtonRelease
        )
        self.itemSelectionMode = (
            TimelineTrackDrawingWidget_SelectionBase.default_itemSelectionMode
        )
        self.itemHoverMode = (
            TimelineTrackDrawingWidget_SelectionBase.default_itemHoverMode
        )

    def reset_hovered(self):
        self.hovered_object_index = None
        self.hovered_object = None
        self.hovered_object_rect = None
        self.hovered_duration_object_indicies = []

    def reset_selected(self):
        self.selected_duration_object_indicies = []

    # Called to reset the hover/selection whenever the data is reloaded
    def reset_on_reload(self):
        self.reset_hovered()
        self.reset_selected()

    # Returns the currently selected partition index or None if none are selected
    def get_selected_event_indicies(self):
        return self.selected_duration_object_indicies

    # Returns the currently selected partition object or None if none are selected
    def get_selected_duration_objects(self):
        prevSelectedItemIndicies = self.get_selected_event_indicies()
        return [
            self.durationObjects[anObjIndex] for anObjIndex in prevSelectedItemIndicies
        ]

    # Find the next event
    def find_next_event(self, following_datetime):
        for (index, obj) in enumerate(self.durationObjects):
            if obj.startTime > following_datetime:
                return (index, obj)
        return None  # If there is no next event, return None

    # Find the previous event
    def find_previous_event(self, preceeding_datetime):
        best_found_candidate_index = None
        best_found_candidate_object = None

        for (index, obj) in enumerate(self.durationObjects):
            if obj.endTime < preceeding_datetime:
                best_found_candidate_index = index
                best_found_candidate_object = obj
            else:
                # otherwise if the object's endTime is later than our desired preceeding_datetime, we have our candidate to return
                break

        if (best_found_candidate_index is None) and (
            best_found_candidate_object is None
        ):
            return None
        else:
            return (best_found_candidate_index, best_found_candidate_object)

    # Returns the currently selected partition index or None if none are selected
    def get_selected_event_index(self):
        if len(self.selected_duration_object_indicies) > 0:
            # Deselect previously selected item
            prevSelectedItemIndex = self.selected_duration_object_indicies[0]
            if not (prevSelectedItemIndex is None):
                return prevSelectedItemIndex
            else:
                return None
        else:
            return None

    # Returns the currently selected partition object or None if none are selected
    def get_selected_duration_obj(self):
        prevSelectedItemIndex = self.get_selected_event_index()
        if not (prevSelectedItemIndex is None):
            prevSelectedDurationObj = self.durationObjects[prevSelectedItemIndex]
            if prevSelectedDurationObj:
                return prevSelectedDurationObj
            else:
                return None
        else:
            return None

    # Returns the index of the child object that the (x, y) point falls within, or None if it doesn't fall within an event.
    def find_child_object(self, event_x, event_y):
        clicked_object_index = None
        for (index, aRect) in enumerate(self.eventRect):
            if aRect.contains(event_x, event_y):
                clicked_object_index = index
                break
        return clicked_object_index

    def deselect_all(self):
        # print("deselect_all()")
        while len(self.selected_duration_object_indicies) > 0:
            prevSelectedItemIndex = self.selected_duration_object_indicies[0]
            self.selected_duration_object_indicies.remove(prevSelectedItemIndex)
            self.durationObjects[prevSelectedItemIndex].set_state_deselected()

    def select(self, new_selection_index):
        # Select the object
        if self.selected_duration_object_indicies.__contains__(new_selection_index):
            # Already contains the object.
            return False
        else:
            # If in single selection mode, be sure to deselect any previous selections before selecting a new one.
            if self.itemSelectionMode is ItemSelectionOptions.SingleSelection:
                self.deselect_all()
            # Doesn't already contain the object
            self.selected_duration_object_indicies.append(new_selection_index)
            self.durationObjects[new_selection_index].set_state_selected()
            return True

    def deselect(self, selection_index):
        # Select the object
        if self.selected_duration_object_indicies.__contains__(selection_index):
            # Already contains the object.
            self.selected_duration_object_indicies.remove(selection_index)
            self.durationObjects[selection_index].set_state_deselected()
            return True
        else:
            return False

    def deemphasize_all(self):
        while len(self.hovered_duration_object_indicies) > 0:
            prevSelectedItemIndex = self.hovered_duration_object_indicies[0]
            self.hovered_duration_object_indicies.remove(prevSelectedItemIndex)
            self.durationObjects[prevSelectedItemIndex].set_state_deemphasized()

    def emphasize(self, new_emph_index):
        # Select the object
        if self.hovered_duration_object_indicies.__contains__(new_emph_index):
            # Already contains the object.
            return False
        else:
            # If in single selection mode, be sure to deselect any previous selections before selecting a new one.
            if self.itemHoverMode is ItemSelectionOptions.SingleSelection:
                self.deemphasize_all()
            # Doesn't already contain the object
            self.hovered_duration_object_indicies.append(new_emph_index)
            self.durationObjects[new_emph_index].set_state_emphasized()
            return True

    def deemphasize(self, emph_index):
        # Select the object
        if self.hovered_duration_object_indicies.__contains__(emph_index):
            # Already contains the object.
            self.hovered_duration_object_indicies.remove(emph_index)
            self.durationObjects[emph_index].set_state_deemphasized()
            return True
        else:
            return False

    def clear_hover(self):
        QToolTip.hideText()
        self.hovered_object_index = None
        self.hovered_object = None
        self.hovered_object_rect = None
        self.deemphasize_all()

    def on_button_clicked(self, event):
        newlySelectedObjectIndex = self.find_child_object(event.x(), event.y())

        if event.button() == Qt.LeftButton:
            print("SelectionBase Track on_button_released(...): Left click")
            if newlySelectedObjectIndex is None:
                self.deselect_all()
                self.selected_duration_object_indicies = []  # Empty all the objects
                self.selection_changed.emit(self.trackID, -1)
            else:
                # Select the object
                didSelectionChange = self.select(newlySelectedObjectIndex)
                if not didSelectionChange:
                    # Already contains the object.
                    return
                else:
                    # Doesn't already contain the object
                    self.durationObjects[newlySelectedObjectIndex].on_button_clicked(
                        event
                    )
                    self.update()
                    self.selection_changed.emit(self.trackID, newlySelectedObjectIndex)

        elif event.button() == Qt.RightButton:
            print("SelectionBase Track on_button_released(...): Right click")

        elif event.button() == Qt.MiddleButton:
            print("SelectionBase Track on_button_released(...): Middle click")

        else:
            print("SelectionBase Track on_button_released(...): Unknown click event!")

    def on_button_released(self, event):
        # Check if we want to dismiss the selection when the mouse button is released (requiring the user to hold down the button to see the results)
        needs_update = False
        # print("on_button_released({0},{1})".format(event.x(), event.y()))
        newlySelectedObjectIndex = self.find_child_object(event.x(), event.y())

        if event.button() == Qt.LeftButton:
            print("SelectionBase Track on_button_released(...): Left click")
            if newlySelectedObjectIndex is None:
                if self.shouldDismissSelectionUponMouseButtonRelease:
                    self.deselect_all()
                    self.selection_changed.emit(self.trackID, -1)  # Deselect
                # No Durations to create
                return
            else:
                if self.shouldDismissSelectionUponMouseButtonRelease:
                    didSelectionChange = self.deselect(newlySelectedObjectIndex)
                    if not didSelectionChange:
                        # Already contains the object.
                        return
                    else:
                        # Doesn't already contain the object
                        print(
                            "DEBUG: on_button_released({0}): call 1 (left_click) for hovered_object".format(
                                str(event)
                            )
                        )
                        self.durationObjects[
                            newlySelectedObjectIndex
                        ].on_button_released(event)
                        self.selection_changed.emit(
                            self.trackID, newlySelectedObjectIndex
                        )  # TODO: do we need to do this?
                        needs_update = True

        elif event.button() == Qt.RightButton:
            print("SelectionBase Track on_button_released(...): Right click")
            # The menu is called twice because we check both the selected and the hoverred item, of which an event can be both.
            prevHoveredObj = self.hovered_object
            if prevHoveredObj is not None:
                print(
                    "DEBUG: on_button_released({0}): call 1 (right_click) for hovered_object".format(
                        str(event)
                    )
                )
                prevHoveredObj.on_button_released(event)
            else:
                print(
                    "SelectionBase Track on_button_released(...): No valid hoverred object"
                )

            prevSelectedPartitionObj = self.get_selected_duration_obj()
            if prevSelectedPartitionObj is not None:
                is_same_object = False
                # make sure the selected object isn't the same as the hoverred object
                if prevHoveredObj is not None:
                    is_same_object = (
                        prevSelectedPartitionObj.get_track_index()
                        == prevHoveredObj.get_track_index()
                    )
                else:
                    # If the object is None, there's no chance that it was already called
                    is_same_object = False

                if not is_same_object:
                    prevSelectedPartitionObj.on_button_released(event)
                    print(
                        "DEBUG: on_button_released({0}): call 2 (right_click) for get_selected_duration_obj()".format(
                            str(event)
                        )
                    )

            else:
                print(
                    "SelectionBase Track on_button_released(...): No valid selection object"
                )

        elif event.button() == Qt.MiddleButton:
            print("SelectionBase Track on_button_released(...): Middle click")

        else:
            print("SelectionBase Track on_button_released(...): Unknown click event!")

        if needs_update:
            self.update()

    def on_mouse_moved(self, event):
        # print("TimelineTrackDrawingWidget_SelectionBase: mouse move!")
        needs_update = False

        if not self.underMouse():
            self.clear_hover()
            self.hover_changed.emit(self.trackID, -1)
            needs_update = True
        else:
            self.hovered_object_index = self.find_child_object(event.x(), event.y())
            if self.hovered_object_index is None:
                # No object hovered
                self.clear_hover()
                self.hover_changed.emit(self.trackID, -1)
                needs_update = True
            else:
                self.hovered_object = self.durationObjects[self.hovered_object_index]
                self.emphasize(self.hovered_object_index)
                self.hovered_object_rect = self.eventRect[self.hovered_object_index]
                # text = "event: {0}\nstart_time: {1}\nend_time: {2}\nduration: {3}".format(self.hovered_object.name, self.hovered_object.startTime, self.hovered_object.endTime, self.hovered_object.computeDuration())
                # QToolTip.showText(event.globalPos(), text, self, self.hovered_object_rect)
                needs_update = True
                self.hover_changed.emit(self.trackID, self.hovered_object_index)

        # Update if needed
        if needs_update:
            self.update()

        super().on_mouse_moved(event)

    def enterEvent(self, QEvent):
        # here the code for mouse hover
        # print("TimelineTrackDrawingWidget_SelectionBase.enterEvent(...): track_id: {0}".format(self.trackID))
        return super().enterEvent(QEvent)

    def leaveEvent(self, QEvent):
        # here the code for mouse leave
        # print("TimelineTrackDrawingWidget_SelectionBase.leaveEvent(...): track_id: {0}".format(self.trackID))
        self.clear_hover()
        return super().leaveEvent(QEvent)
