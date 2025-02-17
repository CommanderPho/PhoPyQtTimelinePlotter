# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\pho\repos\PhoPyQtTimelinePlotter\src\phopyqttimelineplotter\GUI\UI\ReferenceMarkViewer\ReferenceMarkViewer.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ReferenceMarkViewer(object):
    def setupUi(self, ReferenceMarkViewer):
        ReferenceMarkViewer.setObjectName("ReferenceMarkViewer")
        ReferenceMarkViewer.resize(400, 300)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(ReferenceMarkViewer)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(ReferenceMarkViewer)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.toolButton_RemoveReferenceMark = QtWidgets.QToolButton(self.frame)
        self.toolButton_RemoveReferenceMark.setEnabled(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/fugue/fugue/icons-shadowless/bookmark--minus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_RemoveReferenceMark.setIcon(icon)
        self.toolButton_RemoveReferenceMark.setObjectName("toolButton_RemoveReferenceMark")
        self.horizontalLayout.addWidget(self.toolButton_RemoveReferenceMark)
        self.toolButton_CreateReferenceMark = QtWidgets.QToolButton(self.frame)
        self.toolButton_CreateReferenceMark.setEnabled(False)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/fugue/fugue/icons-shadowless/bookmark--plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_CreateReferenceMark.setIcon(icon1)
        self.toolButton_CreateReferenceMark.setObjectName("toolButton_CreateReferenceMark")
        self.horizontalLayout.addWidget(self.toolButton_CreateReferenceMark)
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.toolButton_CreateAnnotation = QtWidgets.QToolButton(self.frame)
        self.toolButton_CreateAnnotation.setEnabled(False)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/diagona/diagona/icons/16/027.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_CreateAnnotation.setIcon(icon2)
        self.toolButton_CreateAnnotation.setObjectName("toolButton_CreateAnnotation")
        self.horizontalLayout.addWidget(self.toolButton_CreateAnnotation)
        self.line_2 = QtWidgets.QFrame(self.frame)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.toolButton_AlignLeft = QtWidgets.QToolButton(self.frame)
        self.toolButton_AlignLeft.setEnabled(False)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/fugue/fugue/icons-shadowless/application-dock-180.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_AlignLeft.setIcon(icon3)
        self.toolButton_AlignLeft.setObjectName("toolButton_AlignLeft")
        self.horizontalLayout.addWidget(self.toolButton_AlignLeft)
        self.toolButton_AlignRight = QtWidgets.QToolButton(self.frame)
        self.toolButton_AlignRight.setEnabled(False)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/fugue/fugue/icons-shadowless/application-dock.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_AlignRight.setIcon(icon4)
        self.toolButton_AlignRight.setObjectName("toolButton_AlignRight")
        self.horizontalLayout.addWidget(self.toolButton_AlignRight)
        self.toolButton_3 = QtWidgets.QToolButton(self.frame)
        self.toolButton_3.setEnabled(False)
        self.toolButton_3.setObjectName("toolButton_3")
        self.horizontalLayout.addWidget(self.toolButton_3)
        self.toolButton_4 = QtWidgets.QToolButton(self.frame)
        self.toolButton_4.setEnabled(False)
        self.toolButton_4.setObjectName("toolButton_4")
        self.horizontalLayout.addWidget(self.toolButton_4)
        self.verticalLayout_2.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(ReferenceMarkViewer)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.frame_2)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.verticalLayout.addWidget(self.tableWidget)
        self.verticalLayout_2.addWidget(self.frame_2)

        self.retranslateUi(ReferenceMarkViewer)
        QtCore.QMetaObject.connectSlotsByName(ReferenceMarkViewer)

    def retranslateUi(self, ReferenceMarkViewer):
        _translate = QtCore.QCoreApplication.translate
        ReferenceMarkViewer.setWindowTitle(_translate("ReferenceMarkViewer", "Form"))
        self.label.setText(_translate("ReferenceMarkViewer", "Active Reference Markers"))
        self.toolButton_RemoveReferenceMark.setText(_translate("ReferenceMarkViewer", "..."))
        self.toolButton_CreateReferenceMark.setText(_translate("ReferenceMarkViewer", "..."))
        self.toolButton_CreateAnnotation.setToolTip(_translate("ReferenceMarkViewer", "Create comment from selection"))
        self.toolButton_CreateAnnotation.setStatusTip(_translate("ReferenceMarkViewer", "Create comment from selection"))
        self.toolButton_CreateAnnotation.setText(_translate("ReferenceMarkViewer", "..."))
        self.toolButton_AlignLeft.setText(_translate("ReferenceMarkViewer", "..."))
        self.toolButton_AlignRight.setText(_translate("ReferenceMarkViewer", "..."))
        self.toolButton_3.setText(_translate("ReferenceMarkViewer", "..."))
        self.toolButton_4.setText(_translate("ReferenceMarkViewer", "..."))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("ReferenceMarkViewer", "id"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("ReferenceMarkViewer", "name"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("ReferenceMarkViewer", "datetime"))
import PhoPyQtTimelinePlotterResourceFile_rc
