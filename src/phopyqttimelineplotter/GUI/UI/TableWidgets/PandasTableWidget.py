# coding: utf-8
import sys

import pandas as pd
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import (
    QAbstractTableModel,
    QDir,
    QEvent,
    QItemSelectionModel,
    QObject,
    QPersistentModelIndex,
    QPoint,
    QRect,
    QSize,
    Qt,
    QThreadPool,
    pyqtSignal,
    pyqtSlot,
)
from PyQt5.QtGui import QBrush, QColor, QFont, QIcon, QPainter, QPen
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QAction,
    QApplication,
    QFileDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QMenu,
    QMessageBox,
    QPushButton,
    QSplitter,
    QStackedWidget,
    QTableView,
    QTabWidget,
    QToolTip,
    QVBoxLayout,
    QWidget,
)

from phopyqttimelineplotter.GUI.Model.TableModels.PandasTableModel import (
    PandasTableModel,
)

## INCLUDES:
# from phopyqttimelineplotter.GUI.UI.TableWidgets.PandasTableWidget import PandasTableWidget


""" PandasTableWidget

"""


class PandasTableWidget(QWidget):

    # ActiveTableTabs = [Animal, Cohort, Experiment, BehavioralBox, Labjack]
    # ActiveTableTabStrings = ["Animal", "Cohort", "Experiment", "BehavioralBox", "Labjack"]

    # ActiveTableTabs = [FileParentFolder, Context, Subcontext, VideoFile]
    # ActiveTableTabStrings = ["FileParentFolder", "Context", "Subcontext", "VideoFile"]

    # ActiveTableTabs = [Animal, Cohort, Experiment, BehavioralBox, Labjack, VideoFile, TimestampedAnnotation]
    # ActiveTableTabStrings = ["Animal", "Cohort", "Experiment", "BehavioralBox", "Labjack", "VideoFile", "TimestampedAnnotation"]

    def __init__(self, table_models, parent=None):
        super().__init__(parent=parent)  # Call the inherited classes __init__ method

        self.activeActionTabIndex = 0
        self.models = table_models
        self.tables = []
        self.table_selection_models = []
        for (i, aTableModel) in enumerate(table_models):
            self.tables.append(None)
            self.table_selection_models.append(None)

        self.reloadModels()

        self.setMouseTracking(True)
        self.initUI()

    def get_table_models(self):
        return self.models

    def initUI(self):
        # mainQWidget = QWidget()
        mainLayout = QVBoxLayout()

        # Nested helper function to initialize the menu bar
        def initUI_initMenuBar(self):
            # self.ui.actionLoad.triggered.connect(self.handle_menu_load_event)
            # self.ui.actionSave.triggered.connect(self.handle_menu_save_event)
            # self.ui.actionRefresh.triggered.connect(self.handle_menu_refresh_event)
            pass

        desiredWindowWidth = 500
        self.resize(desiredWindowWidth, 800)
        self.setWindowTitle("DLC File Preview Window")

        # Setup the menubar
        initUI_initMenuBar(self)

        # Initialize tab screen
        self.tabs = QTabWidget()

        for (i, aTableModel) in enumerate(self.get_table_models()):
            currTabNameStr = aTableModel.get_model_display_name()

            exec("self.tab" + str(i) + "= QWidget() ")
            # self.tab1 = QWidget()
            exec("self.tabs.addTab(self.tab" + str(i) + ', "' + currTabNameStr + '")')
            # self.tabs.addTab(self.tab1,"Tab 1")
            exec("self.tab" + str(i) + ".layout = QVBoxLayout(self)")
            # self.tab1.layout = QVBoxLayout(self)

            self.tables[i] = QTableView(self)
            self.tables[i].setModel(self.models[i])
            self.tables[i].setSelectionBehavior(QAbstractItemView.SelectRows)
            self.tables[i].setContextMenuPolicy(Qt.CustomContextMenu)
            self.tables[i].customContextMenuRequested.connect(self.display_context_menu)
            self.tables[i].setSelectionMode(QAbstractItemView.SingleSelection)

            self.table_selection_models[i] = QItemSelectionModel(self.models[i])
            self.tables[i].setModel(self.table_selection_models[i].model())
            self.tables[i].setSelectionModel(self.table_selection_models[i])
            self.table_selection_models[i].selectionChanged.connect(
                self.update_current_record
            )

            exec("self.tab" + str(i) + ".layout.addWidget(self.tables[" + str(i) + "])")
            exec("self.tab" + str(i) + ".setLayout(self.tab" + str(i) + ".layout)")

            currBtnAddNewRecord = QPushButton("New", self)
            currBtnAddNewRecord.released.connect(self.handle_add_new_record_pressed)

            currBtnExportAllRecords = QPushButton("Export", self)
            currBtnExportAllRecords.released.connect(
                self.handle_export_all_records_pressed
            )

            exec("self.tab" + str(i) + ".layout.addWidget(currBtnAddNewRecord)")
            exec("self.tab" + str(i) + ".layout.addWidget(currBtnExportAllRecords)")

        self.tabs.resize(300, 200)

        mainLayout.addWidget(self.tabs)

        self.setLayout(mainLayout)

        for (aTableIndex, aTable) in enumerate(self.tables):
            aTable.resizeColumnsToContents()

    # Updates the member variables from the database
    # Note: if there are any pending changes, they will be persisted on this action
    def reloadModels(self):
        # self.model = []

        # for (i, tableRecordClass) in enumerate(self.get_table_models()):
        #     self.models[i] = self.database_connection.get_table_model(tableRecordClass)

        # self.model = self.database_connection.get_animal_table_model()
        # self.model = self.database_connection.get_table_model(FileParentFolder)
        # self.model = self.database_connection.get_table_model(VideoFile)
        # self.model = self.database_connection.get_table_model(BehavioralBox)
        pass

    def handle_add_new_record_pressed(self):
        print("handle_add_new_record_pressed(...)")
        self.create_new_record()
        # newRecord = BehavioralBox()
        # wasInsertSuccess = self.model.insertRecord(-1, newRecord)
        # if (wasInsertSuccess):
        #     print("insert success!")
        #     self.model.submitAll()
        # else:
        #     print("insert failed!")
        #     self.database_rollback()

        # print("done.")

    def handle_export_all_records_pressed(self):
        print("handle_export_all_records_pressed(...)")
        self.export_records()

    def display_context_menu(self, pos):
        curr_active_tab_index = self.get_active_tab_index()
        index = self.tables[curr_active_tab_index].indexAt(pos)

        self.menu = QMenu()

        # self.edit_action = self.menu.addAction("Edit")
        # self.edit_action.triggered.connect(self.edit_trial)

        self.duplicate_action = self.menu.addAction("Duplicate")
        self.duplicate_action.triggered.connect(self.duplicate_record)
        self.duplicate_action.setEnabled(False)

        self.delete_action = self.menu.addAction("Delete")
        self.delete_action.triggered.connect(self.delete_record)
        self.delete_action.setEnabled(False)

        table_viewport = self.tables[curr_active_tab_index].viewport()
        self.menu.popup(table_viewport.mapToGlobal(pos))

    def delete_record(self):
        ## TODO: unimplemented
        print("UNIMPLEMENTED!!!")
        curr_active_tab_index = self.get_active_tab_index()
        # # selected_row_index = self.table_selection_model.currentIndex().data(Qt.EditRole)
        # index_list = []
        # for model_index in self.tables[curr_active_tab_index].selectionModel().selectedRows():
        #     index = QPersistentModelIndex(model_index)
        #     index_list.append(index)

        # num_items_to_remove = len(index_list)
        # reply = QMessageBox.question(
        #     self, "Confirm", "Really delete the selected {0} records?".format(num_items_to_remove), QMessageBox.Yes, QMessageBox.No
        # )
        # if reply == QMessageBox.Yes:
        #     for index in index_list:
        #         self.current_record = self.models[curr_active_tab_index].record(index.row())
        #         self.database_connection.session.delete(self.current_record)
        #         # self.model.removeRow(index.row())

        #     # self.database_connection.session.commit()
        #     # self.model.refresh()

    def duplicate_record(self):
        ## TODO: unimplemented
        print("UNIMPLEMENTED!!!")
        curr_active_tab_index = self.get_active_tab_index()
        # index_list = []
        # for model_index in self.tables[curr_active_tab_index].selectionModel().selectedRows():
        #     index = QPersistentModelIndex(model_index)
        #     index_list.append(index)

        # num_items_to_remove = len(index_list)
        # selected_row_index = None
        # # Get only first item
        # if (num_items_to_remove > 0):
        #     print("duplicating!")
        #     selected_row_index = index_list[0]
        #     self.current_record = self.models[curr_active_tab_index].record(index.row())
        #     new = self.current_record.duplicate()
        #     self.database_connection.session.add(new)
        #     self.database_connection.session.commit()
        #     self.models[curr_active_tab_index].refresh()

        # else:
        #     print("selection empty!")
        #     return

        print("done.")

    def get_active_tab_index(self):
        return self.tabs.currentIndex()

    def create_new_record(self):
        self.activeActionTabIndex = self.get_active_tab_index()
        dialog = QInputDialog(self)
        dialog.setLabelText("Please enter the name for the new Record.")
        dialog.textValueSelected.connect(self.store_new_record)
        dialog.exec()

    def store_new_record(self, name):
        # self.currClass = PandasTableWidget.ActiveTableTabs[self.activeActionTabIndex]
        # self.currClassString = PandasTableWidget.ActiveTableTabStrings[self.activeActionTabIndex]

        # # rec = BehavioralBox()
        # rec = self.currClass()
        # rec.name = name

        # try:
        #     self.database_connection.save_to_database([rec], self.currClassString)

        # except IntegrityError as e:
        #     print("ERROR: Failed to commit changes! Rolling back", e)
        #     self.database_rollback()
        #     return
        # except Exception as e:
        #     print("Other exception! Trying to continue", e)
        #     self.database_rollback()
        #     return

        # print("storing new record")
        # self.models[self.activeActionTabIndex].refresh()
        pass

    def update_current_record(self, x, y):
        self.current_record = (
            self.table_selection_models[self.get_active_tab_index()]
            .currentIndex()
            .data(Qt.EditRole)
        )

    def export_records(self):
        print("export_records()...")
        self.activeActionTabIndex = self.get_active_tab_index()
        currModel = self.models[self.activeActionTabIndex]
        # currNumRows = currModel.rowCount()

        header_str = currModel.get_header_string()
        print(header_str)
        # separator_str = ', '
        # for irow in range(currModel.rowCount(None)):
        #     curr_row = []
        #     for icol in range(currModel.columnCount(None)):
        #         curr_cell = currModel.data(currModel.createIndex(irow, icol), Qt.DisplayRole)
        #         curr_row.append(curr_cell)

        #     # print all elems per row
        #     curr_row_str = separator_str.join([str(c) for c in curr_row])
        #     print(curr_row_str)
        pass
