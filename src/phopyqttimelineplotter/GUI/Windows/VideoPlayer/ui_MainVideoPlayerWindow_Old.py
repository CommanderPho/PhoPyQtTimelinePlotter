# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\pho\repos\PhoPyQtTimelinePlotter\src\phopyqttimelineplotter\GUI\Windows\VideoPlayer\MainVideoPlayerWindow_Old.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainVideoPlayerWindow(object):
    def setupUi(self, MainVideoPlayerWindow):
        MainVideoPlayerWindow.setObjectName("MainVideoPlayerWindow")
        MainVideoPlayerWindow.resize(1388, 664)
        MainVideoPlayerWindow.setMinimumSize(QtCore.QSize(1024, 480))
        self.widget_central = QtWidgets.QWidget(MainVideoPlayerWindow)
        self.widget_central.setObjectName("widget_central")
        self.layout_main = QtWidgets.QGridLayout(self.widget_central)
        self.layout_main.setObjectName("layout_main")
        self.entry_video = QtWidgets.QLineEdit(self.widget_central)
        self.entry_video.setAutoFillBackground(False)
        self.entry_video.setReadOnly(True)
        self.entry_video.setObjectName("entry_video")
        self.layout_main.addWidget(self.entry_video, 1, 1, 1, 1)
        self.list_timestamp = TimestampTableView(self.widget_central)
        self.list_timestamp.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.list_timestamp.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.list_timestamp.setAlternatingRowColors(True)
        self.list_timestamp.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.list_timestamp.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.list_timestamp.setObjectName("list_timestamp")
        self.list_timestamp.horizontalHeader().setHighlightSections(False)
        self.list_timestamp.horizontalHeader().setStretchLastSection(True)
        self.list_timestamp.verticalHeader().setHighlightSections(False)
        self.layout_main.addWidget(self.list_timestamp, 2, 0, 1, 4)
        self.button_video_browse = QtWidgets.QPushButton(self.widget_central)
        self.button_video_browse.setObjectName("button_video_browse")
        self.layout_main.addWidget(self.button_video_browse, 1, 3, 1, 1)
        self.frame_media = QtWidgets.QFrame(self.widget_central)
        self.frame_media.setMinimumSize(QtCore.QSize(500, 0))
        self.frame_media.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_media.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_media.setLineWidth(0)
        self.frame_media.setObjectName("frame_media")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_media)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.media_layout = QtWidgets.QVBoxLayout()
        self.media_layout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.media_layout.setObjectName("media_layout")
        self.frame_video = VideoFrame(self.frame_media)
        self.frame_video.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_video.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.frame_video.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_video.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_video.setLineWidth(0)
        self.frame_video.setObjectName("frame_video")
        self.lblVideoStatusOverlay = QtWidgets.QLabel(self.frame_video)
        self.lblVideoStatusOverlay.setGeometry(QtCore.QRect(0, 0, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.lblVideoStatusOverlay.setFont(font)
        self.lblVideoStatusOverlay.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.lblVideoStatusOverlay.setObjectName("lblVideoStatusOverlay")
        self.media_layout.addWidget(self.frame_video)
        self.frame_media_control = QtWidgets.QFrame(self.frame_media)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_media_control.sizePolicy().hasHeightForWidth())
        self.frame_media_control.setSizePolicy(sizePolicy)
        self.frame_media_control.setMaximumSize(QtCore.QSize(16777215, 70))
        self.frame_media_control.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_media_control.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_media_control.setLineWidth(0)
        self.frame_media_control.setObjectName("frame_media_control")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_media_control)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.button_slow_down = QtWidgets.QPushButton(self.frame_media_control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_slow_down.sizePolicy().hasHeightForWidth())
        self.button_slow_down.setSizePolicy(sizePolicy)
        self.button_slow_down.setObjectName("button_slow_down")
        self.gridLayout_2.addWidget(self.button_slow_down, 1, 2, 1, 1)
        self.button_speed_up = QtWidgets.QPushButton(self.frame_media_control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_speed_up.sizePolicy().hasHeightForWidth())
        self.button_speed_up.setSizePolicy(sizePolicy)
        self.button_speed_up.setObjectName("button_speed_up")
        self.gridLayout_2.addWidget(self.button_speed_up, 1, 5, 1, 1)
        self.button_full_screen = QtWidgets.QPushButton(self.frame_media_control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_full_screen.sizePolicy().hasHeightForWidth())
        self.button_full_screen.setSizePolicy(sizePolicy)
        self.button_full_screen.setObjectName("button_full_screen")
        self.gridLayout_2.addWidget(self.button_full_screen, 1, 11, 1, 1)
        self.doubleSpinBoxPlaybackSpeed = QtWidgets.QDoubleSpinBox(self.frame_media_control)
        self.doubleSpinBoxPlaybackSpeed.setMinimum(0.2)
        self.doubleSpinBoxPlaybackSpeed.setMaximum(6.0)
        self.doubleSpinBoxPlaybackSpeed.setProperty("value", 1.0)
        self.doubleSpinBoxPlaybackSpeed.setObjectName("doubleSpinBoxPlaybackSpeed")
        self.gridLayout_2.addWidget(self.doubleSpinBoxPlaybackSpeed, 1, 3, 1, 1)
        self.button_play_pause = ToggleButton(self.frame_media_control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_play_pause.sizePolicy().hasHeightForWidth())
        self.button_play_pause.setSizePolicy(sizePolicy)
        self.button_play_pause.setCheckable(False)
        self.button_play_pause.setObjectName("button_play_pause")
        self.gridLayout_2.addWidget(self.button_play_pause, 1, 0, 1, 1)
        self.spinBoxFrameJumpMultiplier = QtWidgets.QSpinBox(self.frame_media_control)
        self.spinBoxFrameJumpMultiplier.setMinimum(1)
        self.spinBoxFrameJumpMultiplier.setMaximum(1000)
        self.spinBoxFrameJumpMultiplier.setObjectName("spinBoxFrameJumpMultiplier")
        self.gridLayout_2.addWidget(self.spinBoxFrameJumpMultiplier, 1, 15, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 12, 1, 1)
        self.button_mark_end = QtWidgets.QPushButton(self.frame_media_control)
        self.button_mark_end.setObjectName("button_mark_end")
        self.gridLayout_2.addWidget(self.button_mark_end, 1, 9, 1, 1)
        self.btnHelp = QtWidgets.QPushButton(self.frame_media_control)
        self.btnHelp.setObjectName("btnHelp")
        self.gridLayout_2.addWidget(self.btnHelp, 1, 19, 1, 1)
        self.btnRight = QtWidgets.QToolButton(self.frame_media_control)
        self.btnRight.setArrowType(QtCore.Qt.RightArrow)
        self.btnRight.setObjectName("btnRight")
        self.gridLayout_2.addWidget(self.btnRight, 1, 16, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 1, 18, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 1, 1, 1, 1)
        self.btnSkipLeft = QtWidgets.QToolButton(self.frame_media_control)
        self.btnSkipLeft.setObjectName("btnSkipLeft")
        self.gridLayout_2.addWidget(self.btnSkipLeft, 1, 13, 1, 1)
        self.slider_progress = HighlightedJumpSlider(self.frame_media_control)
        self.slider_progress.setMaximum(9999)
        self.slider_progress.setPageStep(1)
        self.slider_progress.setOrientation(QtCore.Qt.Horizontal)
        self.slider_progress.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.slider_progress.setObjectName("slider_progress")
        self.gridLayout_2.addWidget(self.slider_progress, 0, 0, 1, 20)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 1, 10, 1, 1)
        self.btnLeft = QtWidgets.QToolButton(self.frame_media_control)
        self.btnLeft.setArrowType(QtCore.Qt.LeftArrow)
        self.btnLeft.setObjectName("btnLeft")
        self.gridLayout_2.addWidget(self.btnLeft, 1, 14, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 1, 7, 1, 1)
        self.button_mark_start = QtWidgets.QPushButton(self.frame_media_control)
        self.button_mark_start.setObjectName("button_mark_start")
        self.gridLayout_2.addWidget(self.button_mark_start, 1, 8, 1, 1)
        self.btnSkipRight = QtWidgets.QToolButton(self.frame_media_control)
        self.btnSkipRight.setObjectName("btnSkipRight")
        self.gridLayout_2.addWidget(self.btnSkipRight, 1, 17, 1, 1)
        self.toolButton_SpeedBurstEnabled = QtWidgets.QToolButton(self.frame_media_control)
        self.toolButton_SpeedBurstEnabled.setEnabled(False)
        self.toolButton_SpeedBurstEnabled.setCheckable(True)
        self.toolButton_SpeedBurstEnabled.setChecked(True)
        self.toolButton_SpeedBurstEnabled.setObjectName("toolButton_SpeedBurstEnabled")
        self.gridLayout_2.addWidget(self.toolButton_SpeedBurstEnabled, 1, 4, 1, 1)
        self.media_layout.addWidget(self.frame_media_control)
        self.gridLayout.addLayout(self.media_layout, 1, 0, 1, 1)
        self.layout_main.addWidget(self.frame_media, 2, 5, 3, 1)
        self.frame_timestamp_detail = QtWidgets.QFrame(self.widget_central)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_timestamp_detail.sizePolicy().hasHeightForWidth())
        self.frame_timestamp_detail.setSizePolicy(sizePolicy)
        self.frame_timestamp_detail.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame_timestamp_detail.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_timestamp_detail.setObjectName("frame_timestamp_detail")
        self.formLayout = QtWidgets.QFormLayout(self.frame_timestamp_detail)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setObjectName("formLayout")
        self.label_start_time = QtWidgets.QLabel(self.frame_timestamp_detail)
        self.label_start_time.setObjectName("label_start_time")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_start_time)
        self.entry_start_time = QtWidgets.QLineEdit(self.frame_timestamp_detail)
        self.entry_start_time.setEnabled(True)
        self.entry_start_time.setAutoFillBackground(False)
        self.entry_start_time.setReadOnly(True)
        self.entry_start_time.setObjectName("entry_start_time")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.entry_start_time)
        self.label_end_time = QtWidgets.QLabel(self.frame_timestamp_detail)
        self.label_end_time.setObjectName("label_end_time")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_end_time)
        self.entry_end_time = QtWidgets.QLineEdit(self.frame_timestamp_detail)
        self.entry_end_time.setEnabled(True)
        self.entry_end_time.setAutoFillBackground(False)
        self.entry_end_time.setReadOnly(True)
        self.entry_end_time.setObjectName("entry_end_time")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.entry_end_time)
        self.label_description = QtWidgets.QLabel(self.frame_timestamp_detail)
        self.label_description.setObjectName("label_description")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_description)
        self.entry_description = PlainTextEdit(self.frame_timestamp_detail)
        self.entry_description.setEnabled(True)
        self.entry_description.setMaximumSize(QtCore.QSize(16777215, 75))
        self.entry_description.setAutoFillBackground(False)
        self.entry_description.setObjectName("entry_description")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.entry_description)
        self.frame = QtWidgets.QFrame(self.frame_timestamp_detail)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setLineWidth(0)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_add_entry = QtWidgets.QPushButton(self.frame)
        self.button_add_entry.setObjectName("button_add_entry")
        self.horizontalLayout.addWidget(self.button_add_entry)
        self.button_remove_entry = QtWidgets.QPushButton(self.frame)
        self.button_remove_entry.setEnabled(False)
        self.button_remove_entry.setObjectName("button_remove_entry")
        self.horizontalLayout.addWidget(self.button_remove_entry)
        self.button_save = QtWidgets.QPushButton(self.frame)
        self.button_save.setEnabled(False)
        self.button_save.setObjectName("button_save")
        self.horizontalLayout.addWidget(self.button_save)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.button_run = QtWidgets.QPushButton(self.frame)
        self.button_run.setObjectName("button_run")
        self.horizontalLayout.addWidget(self.button_run)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.frame)
        self.layout_main.addWidget(self.frame_timestamp_detail, 3, 0, 1, 4)
        self.button_timestamp_browse = QtWidgets.QPushButton(self.widget_central)
        self.button_timestamp_browse.setObjectName("button_timestamp_browse")
        self.layout_main.addWidget(self.button_timestamp_browse, 0, 3, 1, 1)
        self.entry_timestamp = QtWidgets.QLineEdit(self.widget_central)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.entry_timestamp.sizePolicy().hasHeightForWidth())
        self.entry_timestamp.setSizePolicy(sizePolicy)
        self.entry_timestamp.setAutoFillBackground(False)
        self.entry_timestamp.setStyleSheet("")
        self.entry_timestamp.setReadOnly(True)
        self.entry_timestamp.setObjectName("entry_timestamp")
        self.layout_main.addWidget(self.entry_timestamp, 0, 1, 1, 1)
        self.button_timestamp_create = QtWidgets.QPushButton(self.widget_central)
        self.button_timestamp_create.setObjectName("button_timestamp_create")
        self.layout_main.addWidget(self.button_timestamp_create, 0, 4, 1, 1)
        self.label_video = QtWidgets.QLabel(self.widget_central)
        self.label_video.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_video.setObjectName("label_video")
        self.layout_main.addWidget(self.label_video, 1, 0, 1, 1)
        self.label_timestamp = QtWidgets.QLabel(self.widget_central)
        self.label_timestamp.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_timestamp.setObjectName("label_timestamp")
        self.layout_main.addWidget(self.label_timestamp, 0, 0, 1, 1)
        self.widget = QtWidgets.QWidget(self.widget_central)
        self.widget.setObjectName("widget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_3.setContentsMargins(-1, 9, -1, 4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lblVideoName = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lblVideoName.setFont(font)
        self.lblVideoName.setObjectName("lblVideoName")
        self.horizontalLayout_3.addWidget(self.lblVideoName)
        self.lblVideoSubtitle = QtWidgets.QLabel(self.widget)
        self.lblVideoSubtitle.setObjectName("lblVideoSubtitle")
        self.horizontalLayout_3.addWidget(self.lblVideoSubtitle)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem6)
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(self.widget)
        self.dateTimeEdit.setEnabled(True)
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.horizontalLayout_3.addWidget(self.dateTimeEdit)
        self.layout_main.addWidget(self.widget, 0, 5, 1, 1)
        self.widget_2 = QtWidgets.QWidget(self.widget_central)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_7.setContentsMargins(-1, 2, -1, 0)
        self.horizontalLayout_7.setSpacing(6)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.groupBox_3 = QtWidgets.QGroupBox(self.widget_2)
        self.groupBox_3.setEnabled(True)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_6.setContentsMargins(-1, 2, -1, 2)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_2 = QtWidgets.QLabel(self.groupBox_3)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_6.addWidget(self.label_2)
        self.lblFileFPS = QtWidgets.QLabel(self.groupBox_3)
        self.lblFileFPS.setObjectName("lblFileFPS")
        self.horizontalLayout_6.addWidget(self.lblFileFPS)
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_6.addWidget(self.label_3)
        self.lblPlaybackPercent = QtWidgets.QLabel(self.groupBox_3)
        self.lblPlaybackPercent.setObjectName("lblPlaybackPercent")
        self.horizontalLayout_6.addWidget(self.lblPlaybackPercent)
        self.horizontalLayout_7.addWidget(self.groupBox_3)
        self.groupBox_2 = QtWidgets.QGroupBox(self.widget_2)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_5.setContentsMargins(-1, 2, -1, 2)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lblCurrentTime = QtWidgets.QLabel(self.groupBox_2)
        self.lblCurrentTime.setObjectName("lblCurrentTime")
        self.horizontalLayout_5.addWidget(self.lblCurrentTime)
        self.lblTotalDuration = QtWidgets.QLabel(self.groupBox_2)
        self.lblTotalDuration.setObjectName("lblTotalDuration")
        self.horizontalLayout_5.addWidget(self.lblTotalDuration)
        self.horizontalLayout_7.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(self.widget_2)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_4.setContentsMargins(-1, 2, -1, 2)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.spinBoxCurrentFrame = QtWidgets.QSpinBox(self.groupBox)
        self.spinBoxCurrentFrame.setEnabled(True)
        self.spinBoxCurrentFrame.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.spinBoxCurrentFrame.setMinimum(1)
        self.spinBoxCurrentFrame.setMaximum(10000)
        self.spinBoxCurrentFrame.setProperty("value", 1)
        self.spinBoxCurrentFrame.setObjectName("spinBoxCurrentFrame")
        self.horizontalLayout_4.addWidget(self.spinBoxCurrentFrame)
        self.lblCurrentFrame = QtWidgets.QLabel(self.groupBox)
        self.lblCurrentFrame.setEnabled(False)
        self.lblCurrentFrame.setObjectName("lblCurrentFrame")
        self.horizontalLayout_4.addWidget(self.lblCurrentFrame)
        self.lblTotalFrames = QtWidgets.QLabel(self.groupBox)
        self.lblTotalFrames.setObjectName("lblTotalFrames")
        self.horizontalLayout_4.addWidget(self.lblTotalFrames)
        self.horizontalLayout_7.addWidget(self.groupBox)
        self.layout_main.addWidget(self.widget_2, 1, 5, 1, 1)
        MainVideoPlayerWindow.setCentralWidget(self.widget_central)
        self.actionExit = QtWidgets.QAction(MainVideoPlayerWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionTest_Entry = QtWidgets.QAction(MainVideoPlayerWindow)
        self.actionTest_Entry.setObjectName("actionTest_Entry")

        self.retranslateUi(MainVideoPlayerWindow)
        QtCore.QMetaObject.connectSlotsByName(MainVideoPlayerWindow)

    def retranslateUi(self, MainVideoPlayerWindow):
        _translate = QtCore.QCoreApplication.translate
        MainVideoPlayerWindow.setWindowTitle(_translate("MainVideoPlayerWindow", "Video Player"))
        self.button_video_browse.setText(_translate("MainVideoPlayerWindow", "Browse"))
        self.lblVideoStatusOverlay.setText(_translate("MainVideoPlayerWindow", "No Video"))
        self.button_slow_down.setToolTip(_translate("MainVideoPlayerWindow", "Slow down the video"))
        self.button_slow_down.setText(_translate("MainVideoPlayerWindow", "Slow Down"))
        self.button_speed_up.setToolTip(_translate("MainVideoPlayerWindow", "Speed up the video"))
        self.button_speed_up.setText(_translate("MainVideoPlayerWindow", "Speed Up"))
        self.button_full_screen.setToolTip(_translate("MainVideoPlayerWindow", "Set the video to full screen"))
        self.button_full_screen.setText(_translate("MainVideoPlayerWindow", "Full Screen"))
        self.button_play_pause.setToolTip(_translate("MainVideoPlayerWindow", "Toggle Play/Pause"))
        self.button_play_pause.setText(_translate("MainVideoPlayerWindow", "Play/Pause"))
        self.button_mark_end.setToolTip(_translate("MainVideoPlayerWindow", "Mark the end of the entry"))
        self.button_mark_end.setText(_translate("MainVideoPlayerWindow", "Mark End"))
        self.btnHelp.setText(_translate("MainVideoPlayerWindow", "Help"))
        self.btnRight.setToolTip(_translate("MainVideoPlayerWindow", "Step Frames Right"))
        self.btnRight.setText(_translate("MainVideoPlayerWindow", ">"))
        self.btnRight.setShortcut(_translate("MainVideoPlayerWindow", "Right"))
        self.btnSkipLeft.setToolTip(_translate("MainVideoPlayerWindow", "Skip Frames Left"))
        self.btnSkipLeft.setText(_translate("MainVideoPlayerWindow", "<-"))
        self.btnSkipLeft.setShortcut(_translate("MainVideoPlayerWindow", "Ctrl+Left"))
        self.btnLeft.setToolTip(_translate("MainVideoPlayerWindow", "Step Frames Left"))
        self.btnLeft.setText(_translate("MainVideoPlayerWindow", "<"))
        self.btnLeft.setShortcut(_translate("MainVideoPlayerWindow", "Left"))
        self.button_mark_start.setToolTip(_translate("MainVideoPlayerWindow", "Mark the start of the entry"))
        self.button_mark_start.setText(_translate("MainVideoPlayerWindow", "Mark Start"))
        self.btnSkipRight.setToolTip(_translate("MainVideoPlayerWindow", "Skip Frames Right"))
        self.btnSkipRight.setText(_translate("MainVideoPlayerWindow", "->"))
        self.btnSkipRight.setShortcut(_translate("MainVideoPlayerWindow", "Ctrl+Right"))
        self.toolButton_SpeedBurstEnabled.setStatusTip(_translate("MainVideoPlayerWindow", "Trigger speedburst with the hotkey"))
        self.toolButton_SpeedBurstEnabled.setWhatsThis(_translate("MainVideoPlayerWindow", "Trigger speedburst with the hotkey"))
        self.toolButton_SpeedBurstEnabled.setText(_translate("MainVideoPlayerWindow", "SpeedBurst"))
        self.label_start_time.setText(_translate("MainVideoPlayerWindow", "Start Time"))
        self.label_end_time.setText(_translate("MainVideoPlayerWindow", "End Time"))
        self.label_description.setText(_translate("MainVideoPlayerWindow", "Description"))
        self.button_add_entry.setText(_translate("MainVideoPlayerWindow", "Add Entry"))
        self.button_remove_entry.setText(_translate("MainVideoPlayerWindow", "Remove Entry"))
        self.button_save.setText(_translate("MainVideoPlayerWindow", "Save"))
        self.button_run.setText(_translate("MainVideoPlayerWindow", "Run"))
        self.button_timestamp_browse.setText(_translate("MainVideoPlayerWindow", "Browse"))
        self.button_timestamp_create.setText(_translate("MainVideoPlayerWindow", "Create"))
        self.label_video.setText(_translate("MainVideoPlayerWindow", "Video File"))
        self.label_timestamp.setText(_translate("MainVideoPlayerWindow", "Timestamp File"))
        self.lblVideoName.setText(_translate("MainVideoPlayerWindow", "VideoName"))
        self.lblVideoSubtitle.setText(_translate("MainVideoPlayerWindow", "Subtitle"))
        self.groupBox_3.setTitle(_translate("MainVideoPlayerWindow", "Other"))
        self.label_2.setText(_translate("MainVideoPlayerWindow", "FPS:"))
        self.lblFileFPS.setText(_translate("MainVideoPlayerWindow", "--"))
        self.label_3.setText(_translate("MainVideoPlayerWindow", "Playback Percent:"))
        self.lblPlaybackPercent.setText(_translate("MainVideoPlayerWindow", "--"))
        self.groupBox_2.setTitle(_translate("MainVideoPlayerWindow", "Playback Time"))
        self.lblCurrentTime.setText(_translate("MainVideoPlayerWindow", "--"))
        self.lblTotalDuration.setText(_translate("MainVideoPlayerWindow", "--"))
        self.groupBox.setTitle(_translate("MainVideoPlayerWindow", "Video Frames"))
        self.lblCurrentFrame.setText(_translate("MainVideoPlayerWindow", "--"))
        self.lblTotalFrames.setText(_translate("MainVideoPlayerWindow", "--"))
        self.actionExit.setText(_translate("MainVideoPlayerWindow", "Exit"))
        self.actionTest_Entry.setText(_translate("MainVideoPlayerWindow", "Test Entry"))
from GUI.Windows.VideoPlayer import HighlightedJumpSlider, PlainTextEdit, TimestampTableView, ToggleButton, VideoFrame
