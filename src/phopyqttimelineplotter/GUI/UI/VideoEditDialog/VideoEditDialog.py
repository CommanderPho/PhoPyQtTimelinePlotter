import sys
from datetime import datetime, timedelta, timezone
from enum import Enum

import numpy as np
from phopyqttimelineplotter.app.database.DatabaseConnectionRef import (
    DatabaseConnectionRef,
    DatabasePendingItemsState,
)
from phopyqttimelineplotter.app.database.entry_models.Behaviors import Behavior, BehaviorGroup, CategoryColors
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
    QFileSystemModel,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSplitter,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QToolTip,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

from phopyqttimelineplotter.GUI.UI.AbstractDatabaseAccessingWidgets import (
    AbstractDatabaseAccessingDialog,
)
from phopyqttimelineplotter.GUI.UI.DialogComponents.AbstractDialogMixins import (
    BoxExperCohortAnimalIDsFrame_Mixin,
    DialogObjectIdentifier,
    ObjectSpecificDialogMixin,
)

# When you set a subtype, ensure that its parent is selected as the type
# When you select a type that's incompatible with the current subtype, probably change the subtype to the first of that type

"""
row_id      .id     array_index
1       1           0
2       2           1
3       3           2


The child (subtype) index that's being retrieved from the type's first child row id is wrong with the additional Noneitem. It needs to have 1 added to it.
"""


class VideoEditDialog(
    ObjectSpecificDialogMixin,
    BoxExperCohortAnimalIDsFrame_Mixin,
    AbstractDatabaseAccessingDialog,
):

    # This defines a signal called 'closed' that takes no arguments.
    on_cancel = pyqtSignal()

    # This defines a signal called 'closed' that takes no arguments.
    on_commit = pyqtSignal(datetime, datetime, int, int, int, int, bool)

    def __init__(self, database_connection, parent=None):
        super(VideoEditDialog, self).__init__(
            database_connection, parent
        )  # Call the inherited classes __init__ method
        self.ui = uic.loadUi(
            "GUI/UI/VideoEditDialog/VideoEditDialog.ui", self
        )  # Load the .ui file
        self.enable_none_selection = True  # if true, an "empty" item is added to the combobox dropdown lists which is selected by default
        self.reloadModelFromDatabase()
        self.initUI()
        self.show()  # Show the GUI

    def initUI(self):
        # self.ui.frame_StartEndDates.
        # self.ui.frame_TitleSubtitleBody
        self.ui.frame_TypeSubtype.setModel(self.behaviorGroups, self.behaviors, self)
        self.ui.frame_StartEndDates.set_editable(False)
        self.ui.frame_TitleSubtitleBody.set_editable(False)
        # self.ui.frame_BoxExperCohortAnimalIDs
        # self.ui.Frame_BoxExperCohorAnimalID
        return

    ## Data Model Functions:
    # Updates the member variables from the database
    # Note: if there are any pending changes, they will be persisted on this action
    def reloadModelFromDatabase(self):
        # Load the latest behaviors and colors data from the database
        self.behaviorGroups = (
            self.database_connection.load_behavior_groups_from_database()
        )
        self.behaviors = self.database_connection.load_behaviors_from_database()
        self.ui.frame_TypeSubtype.setModel(self.behaviorGroups, self.behaviors, self)

    def accept(self):
        print("accept:")
        # Emit the signal.
        behavioral_box_id, experiment_id, cohort_id, animal_id = self.get_id_values()
        final_bb_id, final_experiment_id, final_cohort_id, final_animal_id = (
            int(behavioral_box_id or -1),
            int(experiment_id or -1),
            int(cohort_id or -1),
            int(animal_id or -1),
        )
        self.on_commit.emit(
            self.get_start_date(),
            self.get_end_date(),
            final_bb_id,
            final_experiment_id,
            final_cohort_id,
            final_animal_id,
            self.get_is_original_video(),
        )
        super(VideoEditDialog, self).accept()

    def reject(self):
        print("reject:")
        self.on_cancel.emit()
        super(VideoEditDialog, self).reject()

    def set_type(self, type_id):
        self.ui.frame_TypeSubtype.set_type(type_id)

    def get_type(self):
        return self.ui.frame_TypeSubtype.get_type()

    def set_subtype(self, subtype_id):
        self.ui.frame_TypeSubtype.set_subtype(subtype_id)

    def get_subtype(self):
        return self.ui.frame_TypeSubtype.get_subtype()

    def set_start_date(self, startDate):
        self.ui.frame_StartEndDates.set_start_date(startDate)

    def set_end_date(self, endDate):
        self.ui.frame_StartEndDates.set_end_date(endDate)

    def get_start_date(self):
        return self.ui.frame_StartEndDates.get_start_date()

    def get_end_date(self):
        return self.ui.frame_StartEndDates.get_end_date()

    def get_dates(self):
        return (self.get_start_date(), self.get_end_date())

    def get_title(self):
        return self.ui.frame_TitleSubtitleBody.get_title()

    def get_subtitle(self):
        return self.ui.frame_TitleSubtitleBody.get_subtitle()

    def get_body(self):
        return self.ui.frame_TitleSubtitleBody.get_body()

    def set_title(self, updatedStr):
        self.ui.frame_TitleSubtitleBody.set_title(updatedStr)

    def set_subtitle(self, updatedStr):
        self.ui.frame_TitleSubtitleBody.set_subtitle(updatedStr)

    def set_body(self, updatedStr):
        self.ui.frame_TitleSubtitleBody.set_body(updatedStr)

    def get_is_original_video(self):
        return self.ui.checkBox_isOriginalVideo.isChecked()

    def set_is_original_video(self, is_original):
        self.ui.checkBox_isOriginalVideo.setChecked(is_original)
