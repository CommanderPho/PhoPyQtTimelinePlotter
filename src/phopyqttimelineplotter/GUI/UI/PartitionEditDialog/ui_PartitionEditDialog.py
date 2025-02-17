# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\pho\repos\PhoPyQtTimelinePlotter\src\phopyqttimelineplotter\GUI\UI\PartitionEditDialog\PartitionEditDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PartitionEditDialog(object):
    def setupUi(self, PartitionEditDialog):
        PartitionEditDialog.setObjectName("PartitionEditDialog")
        PartitionEditDialog.resize(519, 436)
        self.verticalLayout = QtWidgets.QVBoxLayout(PartitionEditDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label = QtWidgets.QLabel(PartitionEditDialog)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.dateTimeEdit_Start = QtWidgets.QDateTimeEdit(PartitionEditDialog)
        self.dateTimeEdit_Start.setObjectName("dateTimeEdit_Start")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.dateTimeEdit_Start)
        self.label_2 = QtWidgets.QLabel(PartitionEditDialog)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.dateTimeEdit_End = QtWidgets.QDateTimeEdit(PartitionEditDialog)
        self.dateTimeEdit_End.setEnabled(True)
        self.dateTimeEdit_End.setObjectName("dateTimeEdit_End")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.dateTimeEdit_End)
        self.label_3 = QtWidgets.QLabel(PartitionEditDialog)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEdit_Title = QtWidgets.QLineEdit(PartitionEditDialog)
        self.lineEdit_Title.setClearButtonEnabled(True)
        self.lineEdit_Title.setObjectName("lineEdit_Title")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_Title)
        self.label_4 = QtWidgets.QLabel(PartitionEditDialog)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.lineEdit_Subtitle = QtWidgets.QLineEdit(PartitionEditDialog)
        self.lineEdit_Subtitle.setClearButtonEnabled(True)
        self.lineEdit_Subtitle.setObjectName("lineEdit_Subtitle")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_Subtitle)
        self.label_5 = QtWidgets.QLabel(PartitionEditDialog)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.textBrowser_Body = QtWidgets.QTextBrowser(PartitionEditDialog)
        self.textBrowser_Body.setReadOnly(False)
        self.textBrowser_Body.setObjectName("textBrowser_Body")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.textBrowser_Body)
        self.label_6 = QtWidgets.QLabel(PartitionEditDialog)
        self.label_6.setObjectName("label_6")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.comboBox_Type = QtWidgets.QComboBox(PartitionEditDialog)
        self.comboBox_Type.setObjectName("comboBox_Type")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.comboBox_Type)
        self.label_7 = QtWidgets.QLabel(PartitionEditDialog)
        self.label_7.setObjectName("label_7")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.comboBox_Subtype = QtWidgets.QComboBox(PartitionEditDialog)
        self.comboBox_Subtype.setObjectName("comboBox_Subtype")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.comboBox_Subtype)
        self.frame_BoxExperCohortAnimalIDs = DialogComponents_BoxExperCohortAnimalIDs(PartitionEditDialog)
        self.frame_BoxExperCohortAnimalIDs.setMinimumSize(QtCore.QSize(0, 100))
        self.frame_BoxExperCohortAnimalIDs.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_BoxExperCohortAnimalIDs.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_BoxExperCohortAnimalIDs.setObjectName("frame_BoxExperCohortAnimalIDs")
        self.formLayout_2.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.frame_BoxExperCohortAnimalIDs)
        self.verticalLayout.addLayout(self.formLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(PartitionEditDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(PartitionEditDialog)
        self.buttonBox.accepted.connect(PartitionEditDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(PartitionEditDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(PartitionEditDialog)

    def retranslateUi(self, PartitionEditDialog):
        _translate = QtCore.QCoreApplication.translate
        PartitionEditDialog.setWindowTitle(_translate("PartitionEditDialog", "Partition Edit Dialog"))
        self.label.setText(_translate("PartitionEditDialog", "startDate"))
        self.label_2.setText(_translate("PartitionEditDialog", "endDate"))
        self.label_3.setText(_translate("PartitionEditDialog", "Title"))
        self.lineEdit_Title.setText(_translate("PartitionEditDialog", "title"))
        self.lineEdit_Title.setPlaceholderText(_translate("PartitionEditDialog", "title"))
        self.label_4.setText(_translate("PartitionEditDialog", "Subtitle"))
        self.lineEdit_Subtitle.setText(_translate("PartitionEditDialog", "subtitle"))
        self.lineEdit_Subtitle.setPlaceholderText(_translate("PartitionEditDialog", "subtitle"))
        self.label_5.setText(_translate("PartitionEditDialog", "Body"))
        self.textBrowser_Body.setPlaceholderText(_translate("PartitionEditDialog", "body text"))
        self.label_6.setText(_translate("PartitionEditDialog", "Type"))
        self.label_7.setText(_translate("PartitionEditDialog", "Subtype"))
from GUI.UI.DialogComponents.DialogComponents_BoxExperCohortAnimalIDs import DialogComponents_BoxExperCohortAnimalIDs
