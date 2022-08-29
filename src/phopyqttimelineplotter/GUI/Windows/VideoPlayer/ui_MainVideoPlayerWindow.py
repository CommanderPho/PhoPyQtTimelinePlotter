# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\pho\repos\PhoPyQtTimelinePlotter\src\phopyqttimelineplotter\GUI\Windows\VideoPlayer\MainVideoPlayerWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainVideoPlayerWindow(object):
    def setupUi(self, MainVideoPlayerWindow):
        MainVideoPlayerWindow.setObjectName("MainVideoPlayerWindow")
        MainVideoPlayerWindow.resize(1005, 682)
        MainVideoPlayerWindow.setMinimumSize(QtCore.QSize(640, 480))
        self.widget_central = QtWidgets.QWidget(MainVideoPlayerWindow)
        self.widget_central.setObjectName("widget_central")
        self.layout_main = QtWidgets.QGridLayout(self.widget_central)
        self.layout_main.setContentsMargins(0, 8, 0, -1)
        self.layout_main.setObjectName("layout_main")
        self.widget_VideoTitleLayout = QtWidgets.QWidget(self.widget_central)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_VideoTitleLayout.sizePolicy().hasHeightForWidth())
        self.widget_VideoTitleLayout.setSizePolicy(sizePolicy)
        self.widget_VideoTitleLayout.setMinimumSize(QtCore.QSize(0, 33))
        self.widget_VideoTitleLayout.setMaximumSize(QtCore.QSize(16777215, 33))
        self.widget_VideoTitleLayout.setBaseSize(QtCore.QSize(0, 33))
        self.widget_VideoTitleLayout.setObjectName("widget_VideoTitleLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_VideoTitleLayout)
        self.horizontalLayout_3.setContentsMargins(-1, 9, -1, 4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lblVideoName = QtWidgets.QLabel(self.widget_VideoTitleLayout)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lblVideoName.setFont(font)
        self.lblVideoName.setObjectName("lblVideoName")
        self.horizontalLayout_3.addWidget(self.lblVideoName)
        self.lblVideoSubtitle = QtWidgets.QLabel(self.widget_VideoTitleLayout)
        self.lblVideoSubtitle.setObjectName("lblVideoSubtitle")
        self.horizontalLayout_3.addWidget(self.lblVideoSubtitle)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(self.widget_VideoTitleLayout)
        self.dateTimeEdit.setEnabled(True)
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.horizontalLayout_3.addWidget(self.dateTimeEdit)
        self.layout_main.addWidget(self.widget_VideoTitleLayout, 0, 0, 1, 1)
        self.widget_VideoInfoLayout = QtWidgets.QWidget(self.widget_central)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_VideoInfoLayout.sizePolicy().hasHeightForWidth())
        self.widget_VideoInfoLayout.setSizePolicy(sizePolicy)
        self.widget_VideoInfoLayout.setMinimumSize(QtCore.QSize(0, 41))
        self.widget_VideoInfoLayout.setMaximumSize(QtCore.QSize(16777215, 41))
        self.widget_VideoInfoLayout.setBaseSize(QtCore.QSize(0, 41))
        self.widget_VideoInfoLayout.setObjectName("widget_VideoInfoLayout")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.widget_VideoInfoLayout)
        self.horizontalLayout_7.setContentsMargins(-1, 2, -1, 0)
        self.horizontalLayout_7.setSpacing(6)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.groupBox_3 = QtWidgets.QGroupBox(self.widget_VideoInfoLayout)
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
        self.groupBox_2 = QtWidgets.QGroupBox(self.widget_VideoInfoLayout)
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
        self.groupBox = QtWidgets.QGroupBox(self.widget_VideoInfoLayout)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_4.setContentsMargins(-1, 2, -1, 2)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.spinBoxCurrentFrame = QtWidgets.QSpinBox(self.groupBox)
        self.spinBoxCurrentFrame.setEnabled(False)
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
        self.layout_main.addWidget(self.widget_VideoInfoLayout, 1, 0, 1, 1)
        self.frame_media = QtWidgets.QFrame(self.widget_central)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_media.sizePolicy().hasHeightForWidth())
        self.frame_media.setSizePolicy(sizePolicy)
        self.frame_media.setMinimumSize(QtCore.QSize(500, 300))
        self.frame_media.setBaseSize(QtCore.QSize(500, 300))
        self.frame_media.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_media.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_media.setLineWidth(0)
        self.frame_media.setObjectName("frame_media")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_media)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_videosWrapper = QtWidgets.QFrame(self.frame_media)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_videosWrapper.sizePolicy().hasHeightForWidth())
        self.frame_videosWrapper.setSizePolicy(sizePolicy)
        self.frame_videosWrapper.setMinimumSize(QtCore.QSize(0, 400))
        self.frame_videosWrapper.setBaseSize(QtCore.QSize(0, 400))
        self.frame_videosWrapper.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_videosWrapper.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_videosWrapper.setObjectName("frame_videosWrapper")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_videosWrapper)
        self.horizontalLayout_2.setContentsMargins(0, 4, 0, 4)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_previousFrames = QtWidgets.QFrame(self.frame_videosWrapper)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_previousFrames.sizePolicy().hasHeightForWidth())
        self.frame_previousFrames.setSizePolicy(sizePolicy)
        self.frame_previousFrames.setMinimumSize(QtCore.QSize(80, 0))
        self.frame_previousFrames.setBaseSize(QtCore.QSize(160, 0))
        self.frame_previousFrames.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_previousFrames.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_previousFrames.setObjectName("frame_previousFrames")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_previousFrames)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_PreviousFrame_0 = QtWidgets.QPushButton(self.frame_previousFrames)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_PreviousFrame_0.sizePolicy().hasHeightForWidth())
        self.btn_PreviousFrame_0.setSizePolicy(sizePolicy)
        self.btn_PreviousFrame_0.setMinimumSize(QtCore.QSize(160, 120))
        self.btn_PreviousFrame_0.setMaximumSize(QtCore.QSize(160, 16777215))
        self.btn_PreviousFrame_0.setBaseSize(QtCore.QSize(160, 120))
        self.btn_PreviousFrame_0.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btn_PreviousFrame_0.setText("")
        self.btn_PreviousFrame_0.setIconSize(QtCore.QSize(160, 120))
        self.btn_PreviousFrame_0.setFlat(True)
        self.btn_PreviousFrame_0.setObjectName("btn_PreviousFrame_0")
        self.verticalLayout.addWidget(self.btn_PreviousFrame_0)
        self.btn_PreviousFrame_1 = QtWidgets.QPushButton(self.frame_previousFrames)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_PreviousFrame_1.sizePolicy().hasHeightForWidth())
        self.btn_PreviousFrame_1.setSizePolicy(sizePolicy)
        self.btn_PreviousFrame_1.setMinimumSize(QtCore.QSize(160, 120))
        self.btn_PreviousFrame_1.setMaximumSize(QtCore.QSize(160, 120))
        self.btn_PreviousFrame_1.setBaseSize(QtCore.QSize(160, 120))
        self.btn_PreviousFrame_1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btn_PreviousFrame_1.setText("")
        self.btn_PreviousFrame_1.setIconSize(QtCore.QSize(160, 120))
        self.btn_PreviousFrame_1.setFlat(True)
        self.btn_PreviousFrame_1.setObjectName("btn_PreviousFrame_1")
        self.verticalLayout.addWidget(self.btn_PreviousFrame_1)
        self.btn_PreviousFrame_2 = QtWidgets.QPushButton(self.frame_previousFrames)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_PreviousFrame_2.sizePolicy().hasHeightForWidth())
        self.btn_PreviousFrame_2.setSizePolicy(sizePolicy)
        self.btn_PreviousFrame_2.setMinimumSize(QtCore.QSize(160, 120))
        self.btn_PreviousFrame_2.setMaximumSize(QtCore.QSize(160, 120))
        self.btn_PreviousFrame_2.setBaseSize(QtCore.QSize(160, 120))
        self.btn_PreviousFrame_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btn_PreviousFrame_2.setText("")
        self.btn_PreviousFrame_2.setIconSize(QtCore.QSize(160, 120))
        self.btn_PreviousFrame_2.setFlat(True)
        self.btn_PreviousFrame_2.setObjectName("btn_PreviousFrame_2")
        self.verticalLayout.addWidget(self.btn_PreviousFrame_2)
        self.horizontalLayout_2.addWidget(self.frame_previousFrames)
        self.frame_video = VideoFrame(self.frame_videosWrapper)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_video.sizePolicy().hasHeightForWidth())
        self.frame_video.setSizePolicy(sizePolicy)
        self.frame_video.setMinimumSize(QtCore.QSize(300, 300))
        self.frame_video.setBaseSize(QtCore.QSize(0, 300))
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
        self.lblVideoStatusOverlay.setStyleSheet("color: rgb(241, 241, 241);")
        self.lblVideoStatusOverlay.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.lblVideoStatusOverlay.setObjectName("lblVideoStatusOverlay")
        self.horizontalLayout_2.addWidget(self.frame_video)
        self.gridLayout.addWidget(self.frame_videosWrapper, 0, 0, 1, 1)
        self.frame_CurrentVideoPlaybackInformation = QtWidgets.QFrame(self.frame_media)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_CurrentVideoPlaybackInformation.sizePolicy().hasHeightForWidth())
        self.frame_CurrentVideoPlaybackInformation.setSizePolicy(sizePolicy)
        self.frame_CurrentVideoPlaybackInformation.setMinimumSize(QtCore.QSize(0, 34))
        self.frame_CurrentVideoPlaybackInformation.setMaximumSize(QtCore.QSize(16777215, 34))
        self.frame_CurrentVideoPlaybackInformation.setBaseSize(QtCore.QSize(0, 34))
        self.frame_CurrentVideoPlaybackInformation.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_CurrentVideoPlaybackInformation.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_CurrentVideoPlaybackInformation.setObjectName("frame_CurrentVideoPlaybackInformation")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_CurrentVideoPlaybackInformation)
        self.horizontalLayout.setContentsMargins(4, 0, 4, 0)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_PlaybackDuration = QtWidgets.QVBoxLayout()
        self.verticalLayout_PlaybackDuration.setSpacing(0)
        self.verticalLayout_PlaybackDuration.setObjectName("verticalLayout_PlaybackDuration")
        self.lblPlayheadRelativeDuration = QtWidgets.QLabel(self.frame_CurrentVideoPlaybackInformation)
        self.lblPlayheadRelativeDuration.setObjectName("lblPlayheadRelativeDuration")
        self.verticalLayout_PlaybackDuration.addWidget(self.lblPlayheadRelativeDuration)
        self.lblTotalVideoDuration = QtWidgets.QLabel(self.frame_CurrentVideoPlaybackInformation)
        self.lblTotalVideoDuration.setObjectName("lblTotalVideoDuration")
        self.verticalLayout_PlaybackDuration.addWidget(self.lblTotalVideoDuration)
        self.horizontalLayout.addLayout(self.verticalLayout_PlaybackDuration)
        self.verticalLayout_Frames = QtWidgets.QVBoxLayout()
        self.verticalLayout_Frames.setSpacing(0)
        self.verticalLayout_Frames.setObjectName("verticalLayout_Frames")
        self.lblPlayheadFrame = QtWidgets.QLabel(self.frame_CurrentVideoPlaybackInformation)
        self.lblPlayheadFrame.setObjectName("lblPlayheadFrame")
        self.verticalLayout_Frames.addWidget(self.lblPlayheadFrame)
        self.lblTotalVideoFrames = QtWidgets.QLabel(self.frame_CurrentVideoPlaybackInformation)
        self.lblTotalVideoFrames.setObjectName("lblTotalVideoFrames")
        self.verticalLayout_Frames.addWidget(self.lblTotalVideoFrames)
        self.horizontalLayout.addLayout(self.verticalLayout_Frames)
        self.btn_PlayheadDatetime = QtWidgets.QPushButton(self.frame_CurrentVideoPlaybackInformation)
        self.btn_PlayheadDatetime.setFlat(True)
        self.btn_PlayheadDatetime.setObjectName("btn_PlayheadDatetime")
        self.horizontalLayout.addWidget(self.btn_PlayheadDatetime)
        self.verticalLayout_Datetimes = QtWidgets.QVBoxLayout()
        self.verticalLayout_Datetimes.setSpacing(0)
        self.verticalLayout_Datetimes.setObjectName("verticalLayout_Datetimes")
        self.btn_VideoStartDatetime = QtWidgets.QPushButton(self.frame_CurrentVideoPlaybackInformation)
        self.btn_VideoStartDatetime.setMinimumSize(QtCore.QSize(0, 17))
        self.btn_VideoStartDatetime.setMaximumSize(QtCore.QSize(16777215, 17))
        self.btn_VideoStartDatetime.setBaseSize(QtCore.QSize(0, 17))
        self.btn_VideoStartDatetime.setFlat(True)
        self.btn_VideoStartDatetime.setObjectName("btn_VideoStartDatetime")
        self.verticalLayout_Datetimes.addWidget(self.btn_VideoStartDatetime)
        self.btn_VideoEndDatetime = QtWidgets.QPushButton(self.frame_CurrentVideoPlaybackInformation)
        self.btn_VideoEndDatetime.setMinimumSize(QtCore.QSize(0, 17))
        self.btn_VideoEndDatetime.setMaximumSize(QtCore.QSize(16777215, 17))
        self.btn_VideoEndDatetime.setBaseSize(QtCore.QSize(0, 17))
        self.btn_VideoEndDatetime.setFlat(True)
        self.btn_VideoEndDatetime.setObjectName("btn_VideoEndDatetime")
        self.verticalLayout_Datetimes.addWidget(self.btn_VideoEndDatetime)
        self.horizontalLayout.addLayout(self.verticalLayout_Datetimes)
        self.gridLayout.addWidget(self.frame_CurrentVideoPlaybackInformation, 1, 0, 1, 1)
        self.frame_media_control = QtWidgets.QFrame(self.frame_media)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_media_control.sizePolicy().hasHeightForWidth())
        self.frame_media_control.setSizePolicy(sizePolicy)
        self.frame_media_control.setMinimumSize(QtCore.QSize(0, 70))
        self.frame_media_control.setMaximumSize(QtCore.QSize(16777215, 70))
        self.frame_media_control.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_media_control.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_media_control.setLineWidth(0)
        self.frame_media_control.setObjectName("frame_media_control")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_media_control)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btnHelp = QtWidgets.QPushButton(self.frame_media_control)
        self.btnHelp.setObjectName("btnHelp")
        self.gridLayout_2.addWidget(self.btnHelp, 1, 19, 1, 1)
        self.btnSkipRight = QtWidgets.QToolButton(self.frame_media_control)
        self.btnSkipRight.setObjectName("btnSkipRight")
        self.gridLayout_2.addWidget(self.btnSkipRight, 1, 17, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 1, 10, 1, 1)
        self.btnSkipLeft = QtWidgets.QToolButton(self.frame_media_control)
        self.btnSkipLeft.setObjectName("btnSkipLeft")
        self.gridLayout_2.addWidget(self.btnSkipLeft, 1, 13, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 1, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 1, 12, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 1, 18, 1, 1)
        self.toolButton_SpeedBurstEnabled = QtWidgets.QToolButton(self.frame_media_control)
        self.toolButton_SpeedBurstEnabled.setEnabled(False)
        self.toolButton_SpeedBurstEnabled.setCheckable(True)
        self.toolButton_SpeedBurstEnabled.setChecked(True)
        self.toolButton_SpeedBurstEnabled.setObjectName("toolButton_SpeedBurstEnabled")
        self.gridLayout_2.addWidget(self.toolButton_SpeedBurstEnabled, 1, 4, 1, 1)
        self.btnRight = QtWidgets.QToolButton(self.frame_media_control)
        self.btnRight.setArrowType(QtCore.Qt.RightArrow)
        self.btnRight.setObjectName("btnRight")
        self.gridLayout_2.addWidget(self.btnRight, 1, 16, 1, 1)
        self.button_play_pause = ToggleButton(self.frame_media_control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_play_pause.sizePolicy().hasHeightForWidth())
        self.button_play_pause.setSizePolicy(sizePolicy)
        self.button_play_pause.setCheckable(False)
        self.button_play_pause.setObjectName("button_play_pause")
        self.gridLayout_2.addWidget(self.button_play_pause, 1, 0, 1, 1)
        self.button_slow_down = QtWidgets.QPushButton(self.frame_media_control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_slow_down.sizePolicy().hasHeightForWidth())
        self.button_slow_down.setSizePolicy(sizePolicy)
        self.button_slow_down.setObjectName("button_slow_down")
        self.gridLayout_2.addWidget(self.button_slow_down, 1, 2, 1, 1)
        self.slider_progress = HighlightedJumpSlider(self.frame_media_control)
        self.slider_progress.setMaximum(9999)
        self.slider_progress.setPageStep(1)
        self.slider_progress.setOrientation(QtCore.Qt.Horizontal)
        self.slider_progress.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.slider_progress.setObjectName("slider_progress")
        self.gridLayout_2.addWidget(self.slider_progress, 0, 0, 1, 20)
        self.button_mark_end = QtWidgets.QPushButton(self.frame_media_control)
        self.button_mark_end.setObjectName("button_mark_end")
        self.gridLayout_2.addWidget(self.button_mark_end, 1, 9, 1, 1)
        self.button_mark_start = QtWidgets.QPushButton(self.frame_media_control)
        self.button_mark_start.setObjectName("button_mark_start")
        self.gridLayout_2.addWidget(self.button_mark_start, 1, 8, 1, 1)
        self.doubleSpinBoxPlaybackSpeed = QtWidgets.QDoubleSpinBox(self.frame_media_control)
        self.doubleSpinBoxPlaybackSpeed.setMinimum(0.2)
        self.doubleSpinBoxPlaybackSpeed.setMaximum(6.0)
        self.doubleSpinBoxPlaybackSpeed.setProperty("value", 1.0)
        self.doubleSpinBoxPlaybackSpeed.setObjectName("doubleSpinBoxPlaybackSpeed")
        self.gridLayout_2.addWidget(self.doubleSpinBoxPlaybackSpeed, 1, 3, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem5, 1, 7, 1, 1)
        self.btnLeft = QtWidgets.QToolButton(self.frame_media_control)
        self.btnLeft.setArrowType(QtCore.Qt.LeftArrow)
        self.btnLeft.setObjectName("btnLeft")
        self.gridLayout_2.addWidget(self.btnLeft, 1, 14, 1, 1)
        self.button_speed_up = QtWidgets.QPushButton(self.frame_media_control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_speed_up.sizePolicy().hasHeightForWidth())
        self.button_speed_up.setSizePolicy(sizePolicy)
        self.button_speed_up.setObjectName("button_speed_up")
        self.gridLayout_2.addWidget(self.button_speed_up, 1, 5, 1, 1)
        self.spinBoxFrameJumpMultiplier = QtWidgets.QSpinBox(self.frame_media_control)
        self.spinBoxFrameJumpMultiplier.setFrame(True)
        self.spinBoxFrameJumpMultiplier.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.spinBoxFrameJumpMultiplier.setKeyboardTracking(False)
        self.spinBoxFrameJumpMultiplier.setMinimum(1)
        self.spinBoxFrameJumpMultiplier.setMaximum(50000)
        self.spinBoxFrameJumpMultiplier.setObjectName("spinBoxFrameJumpMultiplier")
        self.gridLayout_2.addWidget(self.spinBoxFrameJumpMultiplier, 1, 15, 1, 1)
        self.button_full_screen = QtWidgets.QPushButton(self.frame_media_control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_full_screen.sizePolicy().hasHeightForWidth())
        self.button_full_screen.setSizePolicy(sizePolicy)
        self.button_full_screen.setObjectName("button_full_screen")
        self.gridLayout_2.addWidget(self.button_full_screen, 1, 11, 1, 1)
        self.gridLayout.addWidget(self.frame_media_control, 2, 0, 1, 1)
        self.gridLayout.setRowStretch(0, 1)
        self.layout_main.addWidget(self.frame_media, 2, 0, 3, 1)
        self.layout_main.setRowStretch(2, 1)
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
        self.lblVideoStatusOverlay.setText(_translate("MainVideoPlayerWindow", "No Video"))
        self.lblPlayheadRelativeDuration.setText(_translate("MainVideoPlayerWindow", "00:00:00"))
        self.lblTotalVideoDuration.setText(_translate("MainVideoPlayerWindow", "00:00:00"))
        self.lblPlayheadFrame.setText(_translate("MainVideoPlayerWindow", "0"))
        self.lblTotalVideoFrames.setText(_translate("MainVideoPlayerWindow", "2600"))
        self.btn_PlayheadDatetime.setText(_translate("MainVideoPlayerWindow", "12/12/19 12:12:12 AM"))
        self.btn_VideoStartDatetime.setText(_translate("MainVideoPlayerWindow", "12/12/19 12:12:12 AM"))
        self.btn_VideoEndDatetime.setText(_translate("MainVideoPlayerWindow", "12/13/19 12:12:13 AM"))
        self.btnHelp.setText(_translate("MainVideoPlayerWindow", "Help"))
        self.btnSkipRight.setToolTip(_translate("MainVideoPlayerWindow", "Skip Frames Right"))
        self.btnSkipRight.setText(_translate("MainVideoPlayerWindow", "->"))
        self.btnSkipRight.setShortcut(_translate("MainVideoPlayerWindow", "Ctrl+Right"))
        self.btnSkipLeft.setToolTip(_translate("MainVideoPlayerWindow", "Skip Frames Left"))
        self.btnSkipLeft.setText(_translate("MainVideoPlayerWindow", "<-"))
        self.btnSkipLeft.setShortcut(_translate("MainVideoPlayerWindow", "Ctrl+Left"))
        self.toolButton_SpeedBurstEnabled.setStatusTip(_translate("MainVideoPlayerWindow", "Trigger speedburst with the hotkey"))
        self.toolButton_SpeedBurstEnabled.setWhatsThis(_translate("MainVideoPlayerWindow", "Trigger speedburst with the hotkey"))
        self.toolButton_SpeedBurstEnabled.setText(_translate("MainVideoPlayerWindow", "SpeedBurst"))
        self.btnRight.setToolTip(_translate("MainVideoPlayerWindow", "Step Frames Right"))
        self.btnRight.setText(_translate("MainVideoPlayerWindow", ">"))
        self.btnRight.setShortcut(_translate("MainVideoPlayerWindow", "Right"))
        self.button_play_pause.setToolTip(_translate("MainVideoPlayerWindow", "Toggle Play/Pause"))
        self.button_play_pause.setText(_translate("MainVideoPlayerWindow", "Play/Pause"))
        self.button_slow_down.setToolTip(_translate("MainVideoPlayerWindow", "Slow down the video"))
        self.button_slow_down.setText(_translate("MainVideoPlayerWindow", "Slow Down"))
        self.button_slow_down.setShortcut(_translate("MainVideoPlayerWindow", "Ctrl+S"))
        self.button_mark_end.setToolTip(_translate("MainVideoPlayerWindow", "Mark the end of the entry"))
        self.button_mark_end.setText(_translate("MainVideoPlayerWindow", "Mark End"))
        self.button_mark_start.setToolTip(_translate("MainVideoPlayerWindow", "Mark the start of the entry"))
        self.button_mark_start.setText(_translate("MainVideoPlayerWindow", "Mark Start"))
        self.btnLeft.setToolTip(_translate("MainVideoPlayerWindow", "Step Frames Left"))
        self.btnLeft.setText(_translate("MainVideoPlayerWindow", "<"))
        self.btnLeft.setShortcut(_translate("MainVideoPlayerWindow", "Left"))
        self.button_speed_up.setToolTip(_translate("MainVideoPlayerWindow", "Speed up the video"))
        self.button_speed_up.setText(_translate("MainVideoPlayerWindow", "Speed Up"))
        self.button_speed_up.setShortcut(_translate("MainVideoPlayerWindow", "Ctrl+="))
        self.spinBoxFrameJumpMultiplier.setToolTip(_translate("MainVideoPlayerWindow", "Jump Size"))
        self.button_full_screen.setToolTip(_translate("MainVideoPlayerWindow", "Set the video to full screen"))
        self.button_full_screen.setText(_translate("MainVideoPlayerWindow", "Full Screen"))
        self.actionExit.setText(_translate("MainVideoPlayerWindow", "Exit"))
        self.actionTest_Entry.setText(_translate("MainVideoPlayerWindow", "Test Entry"))
from GUI.Windows.VideoPlayer import HighlightedJumpSlider, ToggleButton, VideoFrame
