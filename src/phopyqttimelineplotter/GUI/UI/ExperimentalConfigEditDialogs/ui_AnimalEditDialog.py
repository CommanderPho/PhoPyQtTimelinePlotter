# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\pho\repos\PhoPyQtTimelinePlotter\src\phopyqttimelineplotter\GUI\UI\ExperimentalConfigEditDialogs\AnimalEditDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AnimalEditDialog(object):
    def setupUi(self, AnimalEditDialog):
        AnimalEditDialog.setObjectName("AnimalEditDialog")
        AnimalEditDialog.resize(519, 457)
        self.verticalLayout = QtWidgets.QVBoxLayout(AnimalEditDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_3 = QtWidgets.QLabel(AnimalEditDialog)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEdit_Name = QtWidgets.QLineEdit(AnimalEditDialog)
        self.lineEdit_Name.setClearButtonEnabled(True)
        self.lineEdit_Name.setObjectName("lineEdit_Name")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_Name)
        self.label = QtWidgets.QLabel(AnimalEditDialog)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.dateTimeEdit_Birth = QtWidgets.QDateTimeEdit(AnimalEditDialog)
        self.dateTimeEdit_Birth.setObjectName("dateTimeEdit_Birth")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.dateTimeEdit_Birth)
        self.label_2 = QtWidgets.QLabel(AnimalEditDialog)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.dateTimeEdit_Receive = QtWidgets.QDateTimeEdit(AnimalEditDialog)
        self.dateTimeEdit_Receive.setEnabled(True)
        self.dateTimeEdit_Receive.setObjectName("dateTimeEdit_Receive")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.dateTimeEdit_Receive)
        self.deathDateLabel = QtWidgets.QLabel(AnimalEditDialog)
        self.deathDateLabel.setObjectName("deathDateLabel")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.deathDateLabel)
        self.dateTimeEdit_Death = QtWidgets.QDateTimeEdit(AnimalEditDialog)
        self.dateTimeEdit_Death.setEnabled(True)
        self.dateTimeEdit_Death.setObjectName("dateTimeEdit_Death")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.dateTimeEdit_Death)
        self.label_5 = QtWidgets.QLabel(AnimalEditDialog)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.textBrowser_Notes = QtWidgets.QTextBrowser(AnimalEditDialog)
        self.textBrowser_Notes.setReadOnly(False)
        self.textBrowser_Notes.setObjectName("textBrowser_Notes")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.textBrowser_Notes)
        self.verticalLayout.addLayout(self.formLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(AnimalEditDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AnimalEditDialog)
        self.buttonBox.accepted.connect(AnimalEditDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(AnimalEditDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(AnimalEditDialog)

    def retranslateUi(self, AnimalEditDialog):
        _translate = QtCore.QCoreApplication.translate
        AnimalEditDialog.setWindowTitle(_translate("AnimalEditDialog", "Animal Edit Dialog"))
        self.label_3.setText(_translate("AnimalEditDialog", "Name"))
        self.lineEdit_Name.setText(_translate("AnimalEditDialog", "animal"))
        self.lineEdit_Name.setPlaceholderText(_translate("AnimalEditDialog", "title"))
        self.label.setText(_translate("AnimalEditDialog", "birthDate"))
        self.label_2.setText(_translate("AnimalEditDialog", "receiveDate"))
        self.deathDateLabel.setText(_translate("AnimalEditDialog", "deathDate"))
        self.label_5.setText(_translate("AnimalEditDialog", "Notes"))
        self.textBrowser_Notes.setPlaceholderText(_translate("AnimalEditDialog", "body text"))
