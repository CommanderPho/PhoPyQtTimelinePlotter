#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import traceback

import qtawesome as qta
from phopyqttimelineplotter.app.model import ToggleButtonModel
from lib import vlc
from PyQt5 import uic
from PyQt5.QtCore import QDir, QModelIndex, QSortFilterProxyModel, Qt, QTimer
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (
    QApplication,
    QDataWidgetMapper,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QWidget,
)

from phopyqttimelineplotter.GUI.Model.DataMovieLinkInfo import *

"""
The software displays/plays a video file with variable speed and navigation settings.
The software runs a timer, which calls both self.timer_handler() and self.update_ui().

self.update_ui():
    - Updates the slider_progress (playback slider) when the video plays
    - Updates the video labels

self.media_time_change_handler(...) is called on VLC's MediaPlayerTimeChanged event:
    -
"""


""" Classes belonging to the main media widget
lblVideoName
lblVideoSubtitle
dateTimeEdit
lblCurrentFrame
spinBoxCurrentFrame
lblTotalFrames
lblCurrentTime
lblTotalDuration
lblFileFPS
spinBoxFrameJumpMultiplier

btnSkipLeft
btnSkipRight
btnLeft
btnRight

button_play_pause
button_full_screen

button_speed_up
doubleSpinBoxPlaybackSpeed
button_slow_down

button_mark_start
button_mark_end

slider_progress

## DATA MODEL:
self.media_start_time = None
        self.media_end_time = None
        self.restart_needed = False
        self.timer_period = 100
        self.is_full_screen = False
        self.media_started_playing = False
        self.media_is_playing = False
        self.original_geometry = None
play_pause_model


"""


class VideoPlayerWidget(QWidget):
    """
    The main window class
    """

    SpeedBurstPlaybackRate = 16.0

    loaded_media_changed = pyqtSignal()  # Called when the loaded video is changed
    video_playback_position_updated = pyqtSignal(
        float
    )  # video_playback_position_updated:  called when the playback position of the video changes. Either due to playing, or after a user event
    video_playback_state_changed = (
        pyqtSignal()
    )  # video_playback_state_changed: called when play/pause state changes
    close_signal = pyqtSignal()  # Called when the window is closing.

    def __init__(self, parent=None):
        # super().__init__(self, parent)
        super().__init__(parent=parent)
        self.ui = uic.loadUi("GUI/Windows/VideoPlayer/VideoPlayerWidget.ui", self)

        # self.timestamp_filename = None
        self.video_filename = None
        self.media_start_time = None
        self.media_end_time = None
        self.restart_needed = False
        self.timer_period = 100
        self.is_full_screen = False
        self.media_started_playing = False
        self.media_is_playing = False
        self.original_geometry = None

        self.startDirectory = None

        self.vlc_instance = vlc.Instance()
        self.media_player = self.vlc_instance.media_player_new()
        self.is_display_initial_frame_playback = False

        self.is_speed_burst_mode_active = False
        self.speedBurstPlaybackRate = VideoPlayerWidget.SpeedBurstPlaybackRate
        # if sys.platform == "darwin":  # for MacOS
        #     self.ui.frame_video = QMacCocoaViewContainer(0)

        self.movieLink = None

        # self.closeEvent.connect(self.closeEvent)

        self.initUI()

    def initUI(self):

        # TODO: bind the signals and such to self.ui.timestampSidebarWidget
        # self.ui.timestampSidebarWidget.

        self.timer = QTimer(self)
        self.timer.setInterval(self.timer_period)
        self.timer.timeout.connect(self.update_ui)
        self.timer.timeout.connect(self.timer_handler)

        self.ui.frame_video.doubleClicked.connect(self.toggle_full_screen)
        self.ui.frame_video.wheel.connect(self.wheel_handler)

        # TODO: would send twice when the frame_video has focus.
        # self.keyPressEvent.connect(self.key_handler)
        self.ui.frame_video.keyPressed.connect(self.key_handler)

        # Set up Labels:
        # self.ui.lblVideoName.

        # self.displayed_video_title = bind("self.ui.lblVideoName", "text", str)
        self.ui.lblVideoName.setText(self.video_filename)
        self.ui.lblVideoSubtitle.setText("")
        self.ui.dateTimeEdit.setHidden(True)
        self.ui.lblCurrentFrame.setText("")
        self.ui.spinBoxCurrentFrame.setEnabled(False)
        self.ui.spinBoxCurrentFrame.setValue(1)
        self.ui.spinBoxCurrentFrame.valueChanged.connect(
            self.handle_frame_value_changed
        )
        self.ui.lblTotalFrames.setText("")

        self.ui.lblCurrentTime.setText("")
        self.ui.lblTotalDuration.setText("")

        self.ui.lblFileFPS.setText("")

        self.ui.spinBoxFrameJumpMultiplier.value = 1

        # Set up buttons

        # Set up directional buttons
        self.ui.btnSkipLeft.clicked.connect(self.skip_left_handler)
        self.ui.btnSkipRight.clicked.connect(self.skip_right_handler)
        self.ui.btnLeft.clicked.connect(self.step_left_handler)
        self.ui.btnRight.clicked.connect(self.step_right_handler)

        self.play_pause_model = ToggleButtonModel(None, self)
        self.play_pause_model.setStateMap(
            {
                True: {"text": "", "icon": qta.icon("fa.play", scale_factor=0.7)},
                False: {"text": "", "icon": qta.icon("fa.pause", scale_factor=0.7)},
            }
        )
        self.ui.button_play_pause.setModel(self.play_pause_model)
        self.ui.button_play_pause.clicked.connect(self.play_pause)

        self.ui.button_full_screen.setIcon(qta.icon("ei.fullscreen", scale_factor=0.6))
        self.ui.button_full_screen.setText("")
        self.ui.button_full_screen.clicked.connect(self.toggle_full_screen)

        # Playback Speed:
        self.ui.doubleSpinBoxPlaybackSpeed.value = 1.0
        self.ui.doubleSpinBoxPlaybackSpeed.valueChanged.connect(
            self.speed_changed_handler
        )

        self.ui.button_speed_up.clicked.connect(self.speed_up_handler)
        self.ui.button_speed_up.setIcon(
            qta.icon("fa.arrow-circle-o-up", scale_factor=0.8)
        )
        self.ui.button_speed_up.setText("")
        self.ui.button_slow_down.clicked.connect(self.slow_down_handler)
        self.ui.button_slow_down.setIcon(
            qta.icon("fa.arrow-circle-o-down", scale_factor=0.8)
        )
        self.ui.button_slow_down.setText("")

        # self.ui.button_mark_start.setIcon(
        #     qta.icon("fa.quote-left", scale_factor=0.7)
        # )
        # self.ui.button_mark_start.setText("")
        # self.ui.button_mark_end.setIcon(
        #     qta.icon("fa.quote-right", scale_factor=0.7)
        # )
        # self.ui.button_mark_end.setText("")
        # self.ui.button_add_entry.clicked.connect(self.add_entry)
        # self.ui.button_remove_entry.clicked.connect(self.remove_entry)

        # self.ui.button_mark_start.clicked.connect(
        #     lambda: self.set_mark(start_time=int(
        #         self.media_player.get_position() *
        #         self.media_player.get_media().get_duration()))
        # )
        # self.ui.button_mark_end.clicked.connect(
        #     lambda: self.set_mark(end_time=int(
        #         self.media_player.get_position() *
        #         self.media_player.get_media().get_duration()))
        # )

        self.ui.slider_progress.setTracking(False)
        self.ui.slider_progress.valueChanged.connect(self.set_media_position)

        # self.ui.slider_volume.valueChanged.connect(self.set_volume)
        # self.ui.entry_description.setReadOnly(True)

        # Mapper between the table and the entry detail
        # self.mapper = QDataWidgetMapper()
        # self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        # self.ui.button_save.clicked.connect(self.mapper.submit)

        # Set up default volume
        # self.set_volume(self.ui.slider_volume.value())

        self.vlc_events = self.media_player.event_manager()
        self.vlc_events.event_attach(
            vlc.EventType.MediaPlayerTimeChanged, self.media_time_change_handler
        )

        # Let our application handle mouse and key input instead of VLC
        self.media_player.video_set_mouse_input(False)
        self.media_player.video_set_key_input(False)

        self.timer.start()

        self.update_video_frame_overlay_text()

        self.ui.show()

    # Called when the window is closing.
    # def closeEvent(self, event):
    #     print("VideoPlayerWidget.closeEvent(...)")
    #     # print("VideoPlayerWidget.closeEvent({0})".format(str(event)))
    #     # self.on_close()
    #     # self.close()
    #     # event.accept()

    # def on_close(self):
    #     """ Perform on close stuff here """
    #     print("VideoPlayerWidget.on_close()!")
    #     # self.timer.stop() # Stop the timer
    #     # self.media_player.stop() # Stop the playing media
    #     # self.movieLink = None
    #     self.close_signal.emit()

    # Movie Link:
    def get_movie_link(self):
        return self.movieLink

    # Called when the UI slider position is updated via user-click
    def set_media_position(self, position):
        percentage = position / 10000.0
        self.media_player.set_position(percentage)
        absolute_position = percentage * self.media_player.get_media().get_duration()
        if absolute_position > self.media_end_time:
            self.media_end_time = -1

    # on_timeline_position_updated(...): called when the main timeline window updates the position. Results in programmatically setting the video playback position
    @pyqtSlot(float)
    def on_timeline_position_updated(self, new_video_percent_offset):
        print("on_timeline_position_updated({0})".format(str(new_video_percent_offset)))
        aPosition = (
            new_video_percent_offset * 10000.0
        )  # Not sure what this does, but it does the inverse of what's done in the start of the "set_media_position(...)" function to get the percentage
        self.set_media_position(aPosition)

        ### NOT YET IMPLEMENTED
        print("TODO: NOT YET IMPLEMENTED!!!!")

        # Or we could rely on the signals generated by the slider, which is how it normally works. Just set the slider's position and everything else should update.
        # TODO: the only provision is that it shouldn't re-emit a "video_playback_position_updated" signal to avoid a cycle
        # TODO: can I block a specific signal? like self.video_playback_position_updated.blockSignals(True)
        self.ui.slider_progress.blockSignals(True)
        self.ui.slider_progress.setValue(aPosition)
        self.ui.slider_progress.blockSignals(False)

    # self.update_ui(): called when the timer fires
    def update_ui(self):
        if self.media_player is None:
            return

        # Update the UI Slider to match the current video playback value
        self.ui.slider_progress.blockSignals(True)
        self.ui.slider_progress.setValue(self.media_player.get_position() * 10000.0)
        # print(self.media_player.get_position() * 10000)

        self.update_video_file_play_labels()

        self.ui.slider_progress.blockSignals(False)

        self.ui.doubleSpinBoxPlaybackSpeed.blockSignals(True)
        self.ui.doubleSpinBoxPlaybackSpeed.setValue(self.media_player.get_rate())
        self.ui.doubleSpinBoxPlaybackSpeed.blockSignals(False)

        currPos = self.media_player.get_position()
        self.video_playback_position_updated.emit(currPos)

        # When the video finishes
        if (
            self.media_started_playing
            and self.media_player.get_media().get_state() == vlc.State.Ended
        ):
            self.play_pause_model.setState(True)
            # Apparently we need to reset the media, otherwise the player
            # won't play at all
            self.media_player.set_media(self.media_player.get_media())
            # self.set_volume(self.ui.slider_volume.value())
            self.media_is_playing = False
            self.media_started_playing = False
            self.run()

    # Event Handlers:

    # self.timer_handler(): called when the timer fires
    def timer_handler(self):
        """
        This is a workaround, because for some reason we can't call set_time()
        inside the MediaPlayerTimeChanged handler (as the video just stops
        playing)
        """
        if self.restart_needed:
            self.media_player.set_time(self.media_start_time)
            self.restart_needed = False

    # Input Handelers:
    def key_handler(self, event):
        print("VideoPlayerWidget key handler: {0}".format(str(event.key())))
        if event.key() == Qt.Key_Escape and self.is_full_screen:
            self.toggle_full_screen()
        if event.key() == Qt.Key_F:
            self.toggle_full_screen()
        if event.key() == Qt.Key_Space:
            self.play_pause()
        if event.key() == Qt.Key_P:
            self.toggle_speed_burst()

    def wheel_handler(self, event):
        # self.modify_volume(1 if event.angleDelta().y() > 0 else -1)
        self.set_media_position(1 if event.angleDelta().y() > 0 else -1)

    def modify_volume(self, delta_percent):
        new_volume = self.media_player.audio_get_volume() + delta_percent
        if new_volume < 0:
            new_volume = 0
        elif new_volume > 40:
            new_volume = 40
        self.media_player.audio_set_volume(new_volume)
        # self.ui.slider_volume.setValue(self.media_player.audio_get_volume())

    def set_volume(self, new_volume):
        self.media_player.audio_set_volume(new_volume)

    def handle_frame_value_changed(self, newProposedFrame):
        # Tries to change the frame to the user provided one.
        ## TODO:
        print(newProposedFrame)

    # media_time_change_handler(...) is called on VLC's MediaPlayerTimeChanged event
    @vlc.callbackmethod
    def media_time_change_handler(self, _):
        # print('Time changed!')

        if not (self.media_player is None):
            currPos = self.media_player.get_position()
            self.video_playback_position_updated.emit(currPos)

        if self.is_display_initial_frame_playback:
            # self.is_display_initial_frame_playback: true to indicate that we're just trying to play the media long enough to get the first frame, so it's not a black square
            # Pause
            self.media_pause()
            self.is_display_initial_frame_playback = (
                False  # Set the variable to false so it quits pausing
            )

        if self.media_end_time == -1:
            return
        if self.media_player.get_time() > self.media_end_time:
            self.restart_needed = True

    # def update_slider_highlight(self):
    #     if self.ui.list_timestamp.selectionModel().hasSelection():
    #         selected_row = self.ui.list_timestamp.selectionModel(). \
    #             selectedRows()[0]
    #         self.media_start_time = self.ui.list_timestamp.model().data(
    #             selected_row.model().index(selected_row.row(), 0),
    #             Qt.UserRole
    #         )
    #         self.media_end_time = self.ui.list_timestamp.model().data(
    #             selected_row.model().index(selected_row.row(), 1),
    #             Qt.UserRole
    #         )
    #         duration = self.media_player.get_media().get_duration()
    #         self.media_end_time = self.media_end_time \
    #             if self.media_end_time != 0 else duration
    #         if self.media_start_time > self.media_end_time:
    #             raise ValueError("Start time cannot be later than end time")
    #         if self.media_start_time > duration:
    #             raise ValueError("Start time not within video duration")
    #         if self.media_end_time > duration:
    #             raise ValueError("End time not within video duration")
    #         slider_start_pos = (self.media_start_time / duration) * \
    #                            (self.ui.slider_progress.maximum() -
    #                             self.ui.slider_progress.minimum())
    #         slider_end_pos = (self.media_end_time / duration) * \
    #                          (self.ui.slider_progress.maximum() -
    #                           self.ui.slider_progress.minimum())
    #         self.ui.slider_progress.setHighlight(
    #             int(slider_start_pos), int(slider_end_pos)
    #         )

    #     else:
    #         self.media_start_time = 0
    #         self.media_end_time = -1

    def run(self):
        """
        Execute the loop
        """
        if self.video_filename is None:
            self._show_error("No video file chosen")
            return
        try:
            # self.update_slider_highlight()
            self.media_player.play()
            self.media_player.set_time(
                self.media_start_time
            )  # Looks like the media playback time is actually being set from the slider.
            self.media_started_playing = True
            self.media_is_playing = True
            self.play_pause_model.setState(False)
        except Exception as ex:
            self._show_error(str(ex))
            print(traceback.format_exc())

    # Toggles play/pause status:
    def play_pause(self):
        """Toggle play/pause status"""
        if not self.media_started_playing:
            self.run()
            return
        if self.media_is_playing:
            self.media_pause()
        else:
            self.media_play()

    # Plays the media:
    def media_play(self):
        if not self.media_started_playing:
            self.run()
            return
        if self.media_is_playing:
            return  # It's already playing, just return
        else:
            self.media_player.play()
            self.post_playback_state_changed_update()

    # Pauses the media:
    def media_pause(self):
        if not self.media_started_playing:
            self.run()
            return
        if self.media_is_playing:
            self.media_player.pause()
            self.post_playback_state_changed_update()
        else:
            return  # It's already paused, just return

    # Stops the media:
    def media_stop(self):
        if not self.media_started_playing:
            return  # It's already stopped, just return
        if self.media_is_playing:
            self.media_player.pause()

        self.media_player.stop()
        self.post_playback_state_changed_update()

    def post_playback_state_changed_update(self):
        # Called after the play, pause, stop state changed
        self.media_is_playing = not self.media_is_playing
        self.play_pause_model.setState(not self.media_is_playing)
        self.video_playback_state_changed.emit()

    # Updates the window title with the filename
    # TODO: doesn't work
    def update_window_title(self):
        print("update_window_title(): {0}".format(self.video_filename))
        if self.video_filename is None:
            # self.setWindowFilePath(None)
            self.setWindowTitle("Video Player: No Video")
            pass
        else:
            # self.setWindowFilePath(self.video_filename)
            self.setWindowTitle("Video Player: " + str(self.video_filename))
            pass

    # This updates the text that is overlayed over the top of the video frame. It serves to temporarily display changes in state, like play, pause, stop, skip, etc to provide feedback and notifications to the user.
    def update_video_frame_overlay_text(self):
        # TODO: should display the message for a few seconds, and then timeout and disappear
        self.ui.lblVideoStatusOverlay.setText("")

    # After a new media has been set, this function is called to start playing for a short bit to display the first few frames of the video
    def update_preview_frame(self):
        # Updates the frame displayed in the media player
        self.is_display_initial_frame_playback = True
        self.media_play()
        # Pause is called in the self.media_time_change_handler(...)

    # Info labels above the video that display the FPS/frame/time/etc info
    def update_video_file_play_labels(self):
        curr_total_fps = self.get_media_fps()
        curr_total_duration = self.media_player.get_length()
        totalNumFrames = self.get_media_total_num_frames()
        if totalNumFrames > 0:
            self.ui.lblTotalFrames.setText(str(totalNumFrames))
        else:
            self.ui.lblTotalFrames.setText("--")
        if curr_total_duration > 0:
            self.ui.lblTotalDuration.setText(
                str(curr_total_duration)
            )  # Gets duration in [ms]
        else:
            self.ui.lblTotalDuration.setText("--")

        # Changing Values: Dynamically updated each time the playhead changes
        curr_percent_complete = (
            self.media_player.get_position()
        )  # Current percent complete between 0.0 and 1.0

        if curr_percent_complete >= 0:
            self.ui.lblPlaybackPercent.setText("{:.4f}".format(curr_percent_complete))
        else:
            self.ui.lblPlaybackPercent.setText("--")

        curr_frame = int(round(curr_percent_complete * totalNumFrames))

        # Disable frame change on spinBox update to prevent infinite loop
        self.ui.spinBoxCurrentFrame.blockSignals(True)
        if curr_frame >= 0:
            self.ui.lblCurrentFrame.setText(str(curr_frame))
            # self.ui.spinBoxCurrentFrame.setValue(curr_frame)
            # self.ui.spinBoxCurrentFrame.setEnabled(True)
        else:
            self.ui.lblCurrentFrame.setText("--")
            # self.ui.spinBoxCurrentFrame.setEnabled(False)
            # self.ui.spinBoxCurrentFrame.setValue(1)

        # Re-enable signals from the frame spin box after update
        self.ui.spinBoxCurrentFrame.blockSignals(False)

        if self.media_player.get_time() >= 0:
            self.ui.lblCurrentTime.setText(
                str(self.media_player.get_time()) + "[ms]"
            )  # Gets time in [ms]
        else:
            self.ui.lblCurrentTime.setText("-- [ms]")  # Gets time in [ms]

    # Called only when the video file changes:
    def update_video_file_labels_on_file_change(self):
        if self.video_filename is None:
            self.ui.lblVideoName.setText("")
        else:
            self.ui.lblVideoName.setText(self.video_filename)
            # Only updated when the video file is changed:
            curr_total_fps = self.get_media_fps()
            self.ui.lblFileFPS.setText(str(curr_total_fps))

            curr_total_duration = self.media_player.get_length()
            totalNumFrames = self.get_media_total_num_frames()
            if totalNumFrames > 0:
                self.ui.lblTotalFrames.setText(str(totalNumFrames))
                self.ui.spinBoxCurrentFrame.setMaximum(totalNumFrames)
                self.ui.spinBoxCurrentFrame.setEnabled(True)
            else:
                self.ui.lblTotalFrames.setText("--")
                self.ui.spinBoxCurrentFrame.setEnabled(False)
                self.ui.spinBoxCurrentFrame.setMaximum(1)

            if curr_total_duration > 0:
                self.ui.lblTotalDuration.setText(
                    str(curr_total_duration)
                )  # Gets duration in [ms]
            else:
                self.ui.lblTotalDuration.setText("--")

            self.update_video_file_play_labels()

    # Media Information:
    def get_frame_multipler(self):
        return self.ui.spinBoxFrameJumpMultiplier.value

    def get_media_fps(self):
        return self.media_player.get_fps() or 30

    def get_milliseconds_per_frame(self):
        """Milliseconds per frame"""
        return int(1000 // self.get_media_fps())

    def get_media_total_num_frames(self):
        return int(self.media_player.get_length() * self.get_media_fps())

    # Playback Navigation (Left/Right) Handlers:
    def step_left_handler(self):
        print("step: left")
        self.seek_frames(-1 * self.get_frame_multipler())

    def skip_left_handler(self):
        print("skip: left")
        self.seek_frames(-10 * self.get_frame_multipler())

    def step_right_handler(self):
        print("step: right")
        self.seek_frames(1 * self.get_frame_multipler())

    def skip_right_handler(self):
        print("skip: right")
        self.seek_frames(10 * self.get_frame_multipler())

    # Other:
    def seek_frames(self, relativeFrameOffset):
        """Jump a certain number of frames forward or back"""
        if self.video_filename is None:
            self._show_error("No video file chosen")
            return
        # if self.media_end_time == -1:
        #     return

        curr_total_fps = self.get_media_fps()
        relativeSecondsOffset = (
            relativeFrameOffset / curr_total_fps
        )  # Desired offset in seconds
        curr_total_duration = self.media_player.get_length()
        relative_percent_offset = (
            relativeSecondsOffset / curr_total_duration
        )  # percent of the whole that we want to skip

        totalNumFrames = self.get_media_total_num_frames()

        try:
            didPauseMedia = False
            if self.media_is_playing:
                self.media_player.pause()
                didPauseMedia = True

            newPosition = self.media_player.get_position() + relative_percent_offset
            # newTime = int(self.media_player.get_time() + relativeFrameOffset)

            # self.update_slider_highlight()
            # self.media_player.set_time(newTime)
            self.media_player.set_position(newPosition)

            if didPauseMedia:
                self.media_player.play()
            # else:
            #     # Otherwise, the media was already paused, we need to very quickly play the media to update the frame with the new time, and then immediately pause it again.
            #     self.media_player.play()
            #     self.media_player.pause()
            self.media_player.next_frame()

            print("Setting media playback time to ", newPosition)
        except Exception as ex:
            self._show_error(str(ex))
            print(traceback.format_exc())

    def toggle_full_screen(self):
        if self.is_full_screen:
            # TODO Artifacts still happen some time when exiting full screen
            # in X11
            self.ui.frame_media.showNormal()
            self.ui.frame_media.restoreGeometry(self.original_geometry)
            self.ui.frame_media.setParent(self.ui.widget_central)
            self.ui.layout_main.addWidget(self.ui.frame_media, 2, 3, 3, 1)
            # self.ui.frame_media.ensurePolished()
        else:
            self.ui.frame_media.setParent(None)
            self.ui.frame_media.setWindowFlags(
                Qt.FramelessWindowHint | Qt.CustomizeWindowHint
            )
            self.original_geometry = self.ui.frame_media.saveGeometry()
            desktop = QApplication.desktop()
            rect = desktop.screenGeometry(desktop.screenNumber(QCursor.pos()))
            self.ui.frame_media.setGeometry(rect)
            self.ui.frame_media.showFullScreen()
            self.ui.frame_media.show()
        self.ui.frame_video.setFocus()
        self.is_full_screen = not self.is_full_screen

    # File Loading:

    def set_video_filename(self, filename):
        """
        Set the video filename
        """
        if not os.path.isfile(filename):
            self._show_error("ERROR: Cannot access video file " + filename)
            return

        # Close the previous file:
        self.media_stop()

        self.startDirectory = os.path.pardir
        self.video_filename = filename

        media = self.vlc_instance.media_new(self.video_filename)
        media.parse()
        if not media.get_duration():
            self._show_error("Cannot play this media file")
            self.media_player.set_media(None)
            self.video_filename = None
        else:
            self.media_player.set_media(media)

            # The media player has to be 'connected' to the QFrame (otherwise the
            # video would be displayed in it's own window). This is platform
            # specific, so we must give the ID of the QFrame (or similar object) to
            # vlc. Different platforms have different functions for this
            if sys.platform.startswith("linux"):  # for Linux using the X Server
                self.media_player.set_xwindow(self.ui.frame_video.winId())
            elif sys.platform == "win32":  # for Windows
                self.media_player.set_hwnd(self.ui.frame_video.winId())
            elif sys.platform == "darwin":  # for MacOS
                self.media_player.set_nsobject(self.ui.frame_video.winId())
            # self.ui.entry_video.setText(self.video_filename)
            self.update_window_title()
            self.update_video_file_labels_on_file_change()
            self.media_started_playing = False
            self.media_is_playing = False
            # self.set_volume(self.ui.slider_volume.value())
            self.play_pause_model.setState(True)
            self.update_preview_frame()

        self.loaded_media_changed.emit()

    def browse_video_handler(self):
        """
        Handler when the video browse button is clicked
        """
        tmp_name, _ = QFileDialog.getOpenFileName(
            self, "Choose Video file", self.startDirectory, "All Files (*)"
        )
        if not tmp_name:
            return
        self.set_video_filename(QDir.toNativeSeparators(tmp_name))

    def _show_error(self, message, title="Error"):
        QMessageBox.warning(self, title, message)

    # Playback Speed/Rate:
    def speed_changed_handler(self, val):
        # print(val)
        self.media_player.set_rate(val)
        # self.media_player.set_rate(self.ui.doubleSpinBoxPlaybackSpeed.value())
        # TODO: Fix playback speed. Print current playback rate (to a label or something, so the user can see).

    def speed_up_handler(self):
        self.modify_rate(0.1)

    def slow_down_handler(self):
        self.modify_rate(-0.1)

    def modify_rate(self, delta):
        new_rate = self.media_player.get_rate() + delta
        if new_rate < 0.2 or new_rate > 6.0:
            return
        self.media_player.set_rate(new_rate)

    # Speed Burst Features:
    def toggle_speed_burst(self):
        curr_is_speed_burst_enabled = self.is_speed_burst_mode_active
        updated_speed_burst_enabled = not curr_is_speed_burst_enabled
        if updated_speed_burst_enabled:
            self.engage_speed_burst()
        else:
            self.disengage_speed_burst()

    # Engages a temporary speed burst
    def engage_speed_burst(self):
        print("Speed burst enabled!")
        self.is_speed_burst_mode_active = True
        # Set the playback speed temporarily to the burst speed
        self.media_player.set_rate(self.speedBurstPlaybackRate)

        self.ui.toolButton_SpeedBurstEnabled.setEnabled(True)
        self.ui.doubleSpinBoxPlaybackSpeed.setEnabled(False)
        self.ui.button_slow_down.setEnabled(False)
        self.ui.button_speed_up.setEnabled(False)

    def disengage_speed_burst(self):
        print("Speed burst disabled!")
        self.is_speed_burst_mode_active = False
        # restore the user specified playback speed
        self.media_player.set_rate(self.ui.doubleSpinBoxPlaybackSpeed.value)

        self.ui.toolButton_SpeedBurstEnabled.setEnabled(False)
        self.ui.doubleSpinBoxPlaybackSpeed.setEnabled(True)
        self.ui.button_slow_down.setEnabled(True)
        self.ui.button_speed_up.setEnabled(True)
