# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\pho\repos\PhoPyQtTimelinePlotter\src\phopyqttimelineplotter\GUI\Windows\ImportCSVWindow\ImportCSVWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ImportCSVWindow(object):
    def setupUi(self, ImportCSVWindow):
        ImportCSVWindow.setObjectName("ImportCSVWindow")
        ImportCSVWindow.resize(805, 556)
        self.horizontalLayout = QtWidgets.QHBoxLayout(ImportCSVWindow)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_leftList = QtWidgets.QFrame(ImportCSVWindow)
        self.frame_leftList.setMinimumSize(QtCore.QSize(120, 0))
        self.frame_leftList.setBaseSize(QtCore.QSize(120, 0))
        self.frame_leftList.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_leftList.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_leftList.setObjectName("frame_leftList")
        self.horizontalLayout.addWidget(self.frame_leftList)
        self.frame_rightDetails = QtWidgets.QFrame(ImportCSVWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_rightDetails.sizePolicy().hasHeightForWidth())
        self.frame_rightDetails.setSizePolicy(sizePolicy)
        self.frame_rightDetails.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_rightDetails.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_rightDetails.setObjectName("frame_rightDetails")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_rightDetails)
        self.gridLayout.setObjectName("gridLayout")
        self.mainImportCSVWidget = ImportCSVWidget(self.frame_rightDetails)
        self.mainImportCSVWidget.setObjectName("mainImportCSVWidget")
        self.gridLayout.addWidget(self.mainImportCSVWidget, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.frame_rightDetails)

        self.retranslateUi(ImportCSVWindow)
        QtCore.QMetaObject.connectSlotsByName(ImportCSVWindow)

    def retranslateUi(self, ImportCSVWindow):
        _translate = QtCore.QCoreApplication.translate
        ImportCSVWindow.setWindowTitle(_translate("ImportCSVWindow", "Import CSV Window"))
from GUI.UI.ImportCSVWidget.ImportCSVWidget import ImportCSVWidget
