# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\pho\repos\PhoPyQtTimelinePlotter\src\phopyqttimelineplotter\GUI\UI\VideoTrackFilterEditWidget\VideoTrackFilterEditWidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_VideoTrackFilterEditWidget(object):
    def setupUi(self, VideoTrackFilterEditWidget):
        VideoTrackFilterEditWidget.setObjectName("VideoTrackFilterEditWidget")
        VideoTrackFilterEditWidget.resize(421, 328)
        self.gridLayout_2 = QtWidgets.QGridLayout(VideoTrackFilterEditWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(VideoTrackFilterEditWidget)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lblTrackID = QtWidgets.QLabel(VideoTrackFilterEditWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblTrackID.sizePolicy().hasHeightForWidth())
        self.lblTrackID.setSizePolicy(sizePolicy)
        self.lblTrackID.setObjectName("lblTrackID")
        self.gridLayout.addWidget(self.lblTrackID, 0, 1, 1, 2)
        self.label_3 = QtWidgets.QLabel(VideoTrackFilterEditWidget)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 2)
        self.lblTrackName = QtWidgets.QLabel(VideoTrackFilterEditWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblTrackName.sizePolicy().hasHeightForWidth())
        self.lblTrackName.setSizePolicy(sizePolicy)
        self.lblTrackName.setObjectName("lblTrackName")
        self.gridLayout.addWidget(self.lblTrackName, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.checkBox_isOriginalVideo = QtWidgets.QCheckBox(VideoTrackFilterEditWidget)
        self.checkBox_isOriginalVideo.setObjectName("checkBox_isOriginalVideo")
        self.verticalLayout.addWidget(self.checkBox_isOriginalVideo)
        self.checkBox_isTaggedVideo = QtWidgets.QCheckBox(VideoTrackFilterEditWidget)
        self.checkBox_isTaggedVideo.setObjectName("checkBox_isTaggedVideo")
        self.verticalLayout.addWidget(self.checkBox_isTaggedVideo)
        self.frame_BoxExperCohortAnimalIDs = DialogComponents_BoxExperCohortAnimalIDs(VideoTrackFilterEditWidget)
        self.frame_BoxExperCohortAnimalIDs.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_BoxExperCohortAnimalIDs.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_BoxExperCohortAnimalIDs.setObjectName("frame_BoxExperCohortAnimalIDs")
        self.verticalLayout.addWidget(self.frame_BoxExperCohortAnimalIDs)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(VideoTrackFilterEditWidget)
        QtCore.QMetaObject.connectSlotsByName(VideoTrackFilterEditWidget)

    def retranslateUi(self, VideoTrackFilterEditWidget):
        _translate = QtCore.QCoreApplication.translate
        VideoTrackFilterEditWidget.setWindowTitle(_translate("VideoTrackFilterEditWidget", "Form"))
        self.label.setText(_translate("VideoTrackFilterEditWidget", "Track ID:"))
        self.lblTrackID.setText(_translate("VideoTrackFilterEditWidget", "0000"))
        self.label_3.setText(_translate("VideoTrackFilterEditWidget", "Track Name:"))
        self.lblTrackName.setText(_translate("VideoTrackFilterEditWidget", "Name"))
        self.checkBox_isOriginalVideo.setText(_translate("VideoTrackFilterEditWidget", "is Original Video"))
        self.checkBox_isTaggedVideo.setText(_translate("VideoTrackFilterEditWidget", "is Tagged Video"))
from GUI.UI.DialogComponents.DialogComponents_BoxExperCohortAnimalIDs import DialogComponents_BoxExperCohortAnimalIDs
