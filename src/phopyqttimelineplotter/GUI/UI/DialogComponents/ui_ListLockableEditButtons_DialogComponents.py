# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\pho\repos\PhoPyQtTimelinePlotter\src\phopyqttimelineplotter\GUI\UI\DialogComponents\ListLockableEditButtons_DialogComponents.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame_TypeSubtype(object):
    def setupUi(self, Frame_TypeSubtype):
        Frame_TypeSubtype.setObjectName("Frame_TypeSubtype")
        Frame_TypeSubtype.resize(94, 19)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Frame_TypeSubtype.sizePolicy().hasHeightForWidth())
        Frame_TypeSubtype.setSizePolicy(sizePolicy)
        Frame_TypeSubtype.setMinimumSize(QtCore.QSize(70, 19))
        Frame_TypeSubtype.setMaximumSize(QtCore.QSize(16777215, 22))
        Frame_TypeSubtype.setBaseSize(QtCore.QSize(70, 19))
        self.horizontalLayout = QtWidgets.QHBoxLayout(Frame_TypeSubtype)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnAdd = QtWidgets.QToolButton(Frame_TypeSubtype)
        self.btnAdd.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/fugue/plus"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAdd.setIcon(icon)
        self.btnAdd.setObjectName("btnAdd")
        self.horizontalLayout.addWidget(self.btnAdd)
        self.btnMinus = QtWidgets.QToolButton(Frame_TypeSubtype)
        self.btnMinus.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/fugue/minus"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnMinus.setIcon(icon1)
        self.btnMinus.setObjectName("btnMinus")
        self.horizontalLayout.addWidget(self.btnMinus)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnToggleLocked = QtWidgets.QToolButton(Frame_TypeSubtype)
        self.btnToggleLocked.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/fugue/lock-locked"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(":/fugue/lock-unlocked"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.btnToggleLocked.setIcon(icon2)
        self.btnToggleLocked.setCheckable(True)
        self.btnToggleLocked.setChecked(False)
        self.btnToggleLocked.setObjectName("btnToggleLocked")
        self.horizontalLayout.addWidget(self.btnToggleLocked)

        self.retranslateUi(Frame_TypeSubtype)
        QtCore.QMetaObject.connectSlotsByName(Frame_TypeSubtype)

    def retranslateUi(self, Frame_TypeSubtype):
        _translate = QtCore.QCoreApplication.translate
        Frame_TypeSubtype.setWindowTitle(_translate("Frame_TypeSubtype", "ListLockableEditButtons_DialogComponents"))
        self.btnAdd.setToolTip(_translate("Frame_TypeSubtype", "Add Record"))
        self.btnMinus.setToolTip(_translate("Frame_TypeSubtype", "Remove Selected Record"))
        self.btnToggleLocked.setToolTip(_translate("Frame_TypeSubtype", "Re-lock to prevent editing"))
import PhoPyQtTimelinePlotterResourceFile_rc
