"""
created (translated to pyqt) by Aleksandr Korabelnikov (nesoriti@yandex.ru)
origin was written in c++ by Aleksey Osipov (aliks-os@yandex.ru)
wiki: https://wiki.qt.io/Widget-moveable-and-resizeable

distributed without any warranty. Code bellow can contains mistakes taken from c++ version and/or created by my own
"""

import sys
from enum import Enum, IntFlag, IntEnum

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QPoint, pyqtSignal, QRect, QSize, QMargins, Q_FLAGS
from PyQt5.QtGui import QColor, QCursor, QPainterPath, QBrush
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMenu, QLabel, QMainWindow


"""
"T"/"B": Top/Bottom
"L"/"R": Left/Right
"""

class ResizableContainerMode(IntEnum):
    NONE = 0,
    MOVE = 1,
    RESIZETL = 2,
    RESIZET = 4,
    RESIZETR = 8,
    RESIZER = 16,
    RESIZEBR = 32,
    RESIZEB = 64,
    RESIZEBL = 128,
    RESIZEL = 256

    # Note Margins are QMargins(int left, int top, int right, int bottom)

    def get_highlight_rect(self, parent_rect, border_handle_size_diff):
        const_corner_rect_size = QSize(10, 10)
        currRect = QRect(QPoint(0, 0), const_corner_rect_size)
        
        if (self == ResizableContainerMode.RESIZETL):
            currPoint = parent_rect.topLeft()
            currRect.moveTopLeft(currPoint)
        elif (self == ResizableContainerMode.RESIZETR):
            currPoint = parent_rect.topRight()
            currRect.moveTopRight(currPoint)
        elif (self == ResizableContainerMode.RESIZEBR):
            currPoint = parent_rect.bottomRight()
            currRect.moveBottomRight(currPoint)
        elif (self == ResizableContainerMode.RESIZEBL):
            currPoint = parent_rect.bottomLeft()
            currRect.moveBottomLeft(currPoint)
        elif (self == ResizableContainerMode.RESIZET):
            # currPoint = parent_rect.top()
            # currRect = QRect(currPoint, const_corner_rect_size))
            currMargins = QMargins(0,border_handle_size_diff,0,0)
            contents_rect = parent_rect.marginsRemoved(currMargins)
            currRect.setLeft(parent_rect.left())
            currRect.setRight(parent_rect.right())
            currRect.setTop(parent_rect.top())
            currRect.setBottom(contents_rect.top())
            # currRect.setHeight(border_handle_size_diff)
        elif (self == ResizableContainerMode.RESIZER):
            # currPoint = parent_rect.top()
            # currRect = QRect(currPoint, const_corner_rect_size))
            currMargins = QMargins(0,0,border_handle_size_diff,0)
            contents_rect = parent_rect.marginsRemoved(currMargins)
            currRect.setLeft(contents_rect.right())
            currRect.setRight(parent_rect.right())
            currRect.setTop(parent_rect.top())
            currRect.setBottom(parent_rect.bottom())
            # currRect.setHeight(border_handle_size_diff)
        elif (self == ResizableContainerMode.RESIZEB):
            # currPoint = parent_rect.top()
            # currRect = QRect(currPoint, const_corner_rect_size))
            currMargins = QMargins(0,0,0,border_handle_size_diff)
            contents_rect = parent_rect.marginsRemoved(currMargins)
            currRect.setLeft(parent_rect.left())
            currRect.setRight(parent_rect.right())
            # currRect.setTop(parent_rect.bottom()+border_handle_size_diff)
            currRect.setTop(contents_rect.bottom())
            currRect.setBottom(parent_rect.bottom())
            # currRect.setHeight(border_handle_size_diff)
        elif (self == ResizableContainerMode.RESIZEL):
            # currPoint = parent_rect.top()
            # currRect = QRect(currPoint, const_corner_rect_size))
            currMargins = QMargins(border_handle_size_diff,0,0,0)
            contents_rect = parent_rect.marginsRemoved(currMargins)
            currRect.setLeft(parent_rect.left())
            currRect.setRight(contents_rect.left())
            currRect.setTop(parent_rect.top())
            currRect.setBottom(parent_rect.bottom())
            # currRect.setHeight(border_handle_size_diff)
        else:
            currRect = None

        return currRect

    def get_mode_cursor(self):
        if (self == ResizableContainerMode.RESIZETL):
            return QCursor(QtCore.Qt.SizeFDiagCursor)
        elif (self == ResizableContainerMode.RESIZETR):
            return QCursor(QtCore.Qt.SizeBDiagCursor)
        elif (self == ResizableContainerMode.RESIZEBR):
            return QCursor(QtCore.Qt.SizeFDiagCursor)
        elif (self == ResizableContainerMode.RESIZEBL):
            return QCursor(QtCore.Qt.SizeBDiagCursor)
        elif (self == ResizableContainerMode.RESIZET):
            return QCursor(QtCore.Qt.SizeVerCursor)
        elif (self == ResizableContainerMode.RESIZER):
            return QCursor(QtCore.Qt.SizeHorCursor)
        elif (self == ResizableContainerMode.RESIZEB):
            return QCursor(QtCore.Qt.SizeVerCursor)
        elif (self == ResizableContainerMode.RESIZEL):
            return QCursor(QtCore.Qt.SizeHorCursor)
        elif (self == ResizableContainerMode.MOVE):
            return QCursor(QtCore.Qt.SizeAllCursor)
        else:
            return QCursor(QtCore.Qt.ArrowCursor)


    # QtCore.Q_DECLARE_FLAGS(ResizableContainerOptions, ResizableContainerOption)
# Q_FLAGS(ResizableContainerMode)
    # QtCore.Q_DECLARE_OPERATORS_FOR_FLAGS(ResizableContainerMode.ResizableContainerOptions)
# class ResizableContainerOption:
#     Enable_Move = int(ResizableContainerMode.MOVE)
#     EnableResize_Corner_TL = int(ResizableContainerMode.RESIZETL)
#     EnableResize_Corner_TR = int(ResizableContainerMode.RESIZETR)
#     EnableResize_Corner_BR = int(ResizableContainerMode.RESIZEBR)
#     EnableResize_Corner_BL = int(ResizableContainerMode.RESIZEBL)
#     EnableResize_Edge_Top = int(ResizableContainerMode.RESIZET)
#     EnableResize_Edge_Right = int(ResizableContainerMode.RESIZER)
#     EnableResize_Edge_Bottom = int(ResizableContainerMode.RESIZEB)
#     EnableResize_Edge_Left = int(ResizableContainerMode.RESIZEL)



class ResizableContainerWidgetMixin(object):

    mode = ResizableContainerMode.NONE
    position = None
    inFocus = pyqtSignal(bool)
    outFocus = pyqtSignal(bool)
    newGeometry = pyqtSignal(QRect)

    def init_resizable(self, parent):
        self.setVisible(True)
        self.setAutoFillBackground(False)
        self.setMouseTracking(True)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setFocus()
        # self.move(p)

        # self.vLayout = QVBoxLayout(self)
        # self.setChildWidget(cWidget)

        self.m_infocus = True
        self.m_isEditing = True
        self.installEventFilter(parent)

    def focusInEvent(self, a0: QtGui.QFocusEvent):
        self.m_infocus = True
        p = self.parentWidget()
        p.installEventFilter(self)
        p.repaint()
        self.inFocus.emit(True)

    def focusOutEvent(self, a0: QtGui.QFocusEvent):
        if not self.m_isEditing:
            return
        if self.m_showMenu:
            return
        self.mode = ResizableContainerMode.NONE
        self.outFocus.emit(False)
        self.m_infocus = False

    # It seems most of the magic is being done here. This function sets the cursor shape (whether it's a "resizing" handle or a mouse) and sets the "mode" variable to indicate which mode it's currently in.,
    def setCursorShape(self, e_pos: QPoint):
        self.border_handle_size_diff = 3
        # Left - Bottom

        if (((e_pos.y() > self.y() + self.height() - self.border_handle_size_diff) and # Bottom
            (e_pos.x() < self.x() + self.border_handle_size_diff)) or # Left
        # Right-Bottom
        ((e_pos.y() > self.y() + self.height() - self.border_handle_size_diff) and # Bottom
        (e_pos.x() > self.x() + self.width() - self.border_handle_size_diff)) or # Right
        # Left-Top
        ((e_pos.y() < self.y() + self.border_handle_size_diff) and # Top
        (e_pos.x() < self.x() + self.border_handle_size_diff)) or # Left
        # Right-Top
        (e_pos.y() < self.y() + self.border_handle_size_diff) and # Top
        (e_pos.x() > self.x() + self.width() - self.border_handle_size_diff)): # Right
            # Left - Bottom
            if ((e_pos.y() > self.y() + self.height() - self.border_handle_size_diff) and # Bottom
            (e_pos.x() < self.x()
                + self.border_handle_size_diff)): # Left
                self.mode = ResizableContainerMode.RESIZEBL
                self.setCursor(QCursor(QtCore.Qt.SizeBDiagCursor))
                # Right - Bottom
            if ((e_pos.y() > self.y() + self.height() - self.border_handle_size_diff) and # Bottom
            (e_pos.x() > self.x() + self.width() - self.border_handle_size_diff)): # Right
                self.mode = ResizableContainerMode.RESIZEBR
                self.setCursor(QCursor(QtCore.Qt.SizeFDiagCursor))
            # Left - Top
            if ((e_pos.y() < self.y() + self.border_handle_size_diff) and # Top
            (e_pos.x() < self.x() + self.border_handle_size_diff)): # Left
                self.mode = ResizableContainerMode.RESIZETL
                self.setCursor(QCursor(QtCore.Qt.SizeFDiagCursor))
            # Right - Top
            if ((e_pos.y() < self.y() + self.border_handle_size_diff) and # Top
            (e_pos.x() > self.x() + self.width() - self.border_handle_size_diff)): # Right
                self.mode = ResizableContainerMode.RESIZETR
                self.setCursor(QCursor(QtCore.Qt.SizeBDiagCursor))
        # check cursor horizontal position
        elif ((e_pos.x() < self.x() + self.border_handle_size_diff) or # Left
            (e_pos.x() > self.x() + self.width() - self.border_handle_size_diff)): # Right
            if e_pos.x() < self.x() + self.border_handle_size_diff: # Left
                self.setCursor(QCursor(QtCore.Qt.SizeHorCursor))
                self.mode = ResizableContainerMode.RESIZEL
            else: # Right
                self.setCursor(QCursor(QtCore.Qt.SizeHorCursor))
                self.mode = ResizableContainerMode.RESIZER
        # check cursor vertical position
        elif ((e_pos.y() > self.y() + self.height() - self.border_handle_size_diff) or # Bottom
            (e_pos.y() < self.y() + self.border_handle_size_diff)): # Top
            if e_pos.y() < self.y() + self.border_handle_size_diff: # Top
                self.setCursor(QCursor(QtCore.Qt.SizeVerCursor))
                self.mode = ResizableContainerMode.RESIZET
            else: # Bottom
                self.setCursor(QCursor(QtCore.Qt.SizeVerCursor))
                self.mode = ResizableContainerMode.RESIZEB
        else:
            self.setCursor(QCursor(QtCore.Qt. ArrowCursor))
            self.mode = ResizableContainerMode.MOVE


    def resizableContainer_keyPressEvent(self, e: QtGui.QKeyEvent):
        if not self.m_isEditing: return
        if e.key() == QtCore.Qt.Key_Delete:
            self.deleteLater()
        # Moving container with arrows
        if QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:
            newPos = QPoint(self.x(), self.y())
            if e.key() == QtCore.Qt.Key_Up:
                newPos.setY(newPos.y() - 1)
            if e.key() == QtCore.Qt.Key_Down:
                newPos.setY(newPos.y() + 1)
            if e.key() == QtCore.Qt.Key_Left:
                newPos.setX(newPos.x() - 1)
            if e.key() == QtCore.Qt.Key_Right:
                newPos.setX(newPos.x() + 1)
            self.move(newPos)

        if QApplication.keyboardModifiers() == QtCore.Qt.ShiftModifier:
            if e.key() == QtCore.Qt.Key_Up:
                self.resize(self.width(), self.height() - 1)
            if e.key() == QtCore.Qt.Key_Down:
                self.resize(self.width(), self.height() + 1)
            if e.key() == QtCore.Qt.Key_Left:
                self.resize(self.width() - 1, self.height())
            if e.key() == QtCore.Qt.Key_Right:
                self.resize(self.width() + 1, self.height())
        self.newGeometry.emit(self.geometry())


    def resizableContainer_mousePressEvent(self, e: QtGui.QMouseEvent):
        self.position = QPoint(e.globalX() - self.geometry().x(), e.globalY() - self.geometry().y())
        if not self.m_isEditing:
            return False
        if not self.m_infocus:
            return False
        if not e.buttons() and QtCore.Qt.LeftButton:
            self.setCursorShape(e.pos())
            return False
        return True


    def resizableContainer_mouseMoveEvent(self, e: QtGui.QMouseEvent):
        if not self.m_isEditing:
            return
        if not self.m_infocus:
            return
        if not e.buttons() and QtCore.Qt.LeftButton:
            p = QPoint(e.x() + self.geometry().x(), e.y() + self.geometry().y())
            self.setCursorShape(p)
            return

        if (self.mode == ResizableContainerMode.MOVE or self.mode == ResizableContainerMode.NONE) and e.buttons() and QtCore.Qt.LeftButton:
            toMove = e.globalPos() - self.position
            if toMove.x() < 0:return
            if toMove.y() < 0:return
            if toMove.x() > self.parentWidget().width() - self.width(): return
            self.move(toMove)
            self.newGeometry.emit(self.geometry())
            self.parentWidget().repaint()
            return
        if (self.mode != ResizableContainerMode.MOVE) and e.buttons() and QtCore.Qt.LeftButton:
            if self.mode == ResizableContainerMode.RESIZETL: # Left - Top
                newwidth = e.globalX() - self.position.x() - self.geometry().x()
                newheight = e.globalY() - self.position.y() - self.geometry().y()
                toMove = e.globalPos() - self.position
                self.resize(self.geometry().width() - newwidth, self.geometry().height() - newheight)
                self.move(toMove.x(), toMove.y())
            elif self.mode == ResizableContainerMode.RESIZETR: # Right - Top
                newheight = e.globalY() - self.position.y() - self.geometry().y()
                toMove = e.globalPos() - self.position
                self.resize(e.x(), self.geometry().height() - newheight)
                self.move(self.x(), toMove.y())
            elif self.mode== ResizableContainerMode.RESIZEBL: # Left - Bottom
                newwidth = e.globalX() - self.position.x() - self.geometry().x()
                toMove = e.globalPos() - self.position
                self.resize(self.geometry().width() - newwidth, e.y())
                self.move(toMove.x(), self.y())
            elif self.mode == ResizableContainerMode.RESIZEB: # Bottom
                self.resize(self.width(), e.y())
            elif self.mode == ResizableContainerMode.RESIZEL: # Left
                newwidth = e.globalX() - self.position.x() - self.geometry().x()
                toMove = e.globalPos() - self.position
                self.resize(self.geometry().width() - newwidth, self.height())
                self.move(toMove.x(), self.y())
            elif self.mode == ResizableContainerMode.RESIZET:# Top
                newheight = e.globalY() - self.position.y() - self.geometry().y()
                toMove = e.globalPos() - self.position
                self.resize(self.width(), self.geometry().height() - newheight)
                self.move(self.x(), toMove.y())
            elif self.mode == ResizableContainerMode.RESIZER: # Right
                self.resize(e.x(), self.height())
            elif self.mode == ResizableContainerMode.RESIZEBR:# Right - Bottom
                self.resize(e.x(), e.y())
            self.parentWidget().repaint()
        self.newGeometry.emit(self.geometry())


"""
TContainer: a freely resizable container widget that embeds its main contents in a frame that allows the user to resize (by producing handles at the edges of the widget), drag, etc
- TODO: need to add a "ModeMask" like variable that disables certain resizing actions (like resizing from any of the corners, in a certain dimension, etc).
    - If it detects a mode that isn't permitted in the mask, it returns self.mode = None
"""
class TContainer(QWidget):
    
    class ResizableContainerOption(IntFlag):
        NONE = 0,
        MOVE = 1,
        RESIZETL = 2,
        RESIZET = 4,
        RESIZETR = 8,
        RESIZER = 16,
        RESIZEBR = 32,
        RESIZEB = 64,
        RESIZEBL = 128,
        RESIZEL = 256

    """ allow to move and resize by user"""
    menu = None
    mode = ResizableContainerMode.NONE
    # (ResizableContainerOption.RESIZEL | ResizableContainerOption.RESIZER)

    # QFlags()
    position = None
    inFocus = pyqtSignal(bool)
    outFocus = pyqtSignal(bool)
    newGeometry = pyqtSignal(QRect)

    def __init__(self, parent, selectable_regions, editable_regions, p, cWidget):
        super().__init__(parent=parent)
        # self.border_handle_size_diff: how many pixels you have to grab the edges
        self.border_handle_size_diff = 3
        self.hoverEdgeRectColor = QColor(100,255,0,200)
        # self.enabled_options = TContainer.ResizableContainerOption(TContainer.ResizableContainerOption.RESIZEL.value)
        self.read_only_options = selectable_regions
        self.enabled_options = editable_regions
        
        self.menu = QMenu(parent=self, title='menu')
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setVisible(True)
        self.setAutoFillBackground(False)
        self.setMouseTracking(True)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setFocus()
        self.move(p)

        self.vLayout = QVBoxLayout(self)
        self.setChildWidget(cWidget)

        self.m_infocus = True
        self.m_showMenu = False
        self.m_isEditing = True
        self.installEventFilter(parent)

    def try_set_mode(self, proposed_mode):
        # print("try_set_mode[{0}]({1}): current_options: {2} ({3})".format(str(proposed_mode), str(proposed_mode.value), str(self.enabled_options), str(self.enabled_options.value)))
        if proposed_mode == ResizableContainerMode.NONE:
            # print("None mode is always enabled!")
            self.mode = proposed_mode
            return True

        if (proposed_mode.value & self.read_only_options.value):
        # if (proposed_mode.value in self.enabled_options):
            # print("Mode is enabled!")
            self.mode = proposed_mode
            return True
        else:
            # print("enabled_options doesn't contain the proposed mode: {0}".format(proposed_mode))
            return False
        
        return

    # get_can_edit_current_mode(): returns True if the current mode can be edited (it isn't read only)
    def get_can_edit_current_mode(self):
        if (self.mode.value & self.enabled_options.value):
            return True
        else:
            return False

    def focusInEvent(self, a0: QtGui.QFocusEvent):
        self.m_infocus = True
        p = self.parentWidget()
        p.installEventFilter(self)
        p.repaint()
        self.inFocus.emit(True)

    def focusOutEvent(self, a0: QtGui.QFocusEvent):
        if not self.m_isEditing:
            return
        if self.m_showMenu:
            return
        self.mode = ResizableContainerMode.NONE
        self.outFocus.emit(False)
        self.m_infocus = False

    # It seems most of the magic is being done here. This function sets the cursor shape (whether it's a "resizing" handle or a mouse) and sets the "mode" variable to indicate which mode it's currently in.,
    def setCursorShape(self, e_pos: QPoint):
        self.border_handle_size_diff = 3
        didModeChange = False
        # Check corners
        # Left - Bottom
        if (((e_pos.y() > self.y() + self.height() - self.border_handle_size_diff) and # Bottom
            (e_pos.x() < self.x() + self.border_handle_size_diff)) or # Left
        # Right-Bottom
        ((e_pos.y() > self.y() + self.height() - self.border_handle_size_diff) and # Bottom
        (e_pos.x() > self.x() + self.width() - self.border_handle_size_diff)) or # Right
        # Left-Top
        ((e_pos.y() < self.y() + self.border_handle_size_diff) and # Top
        (e_pos.x() < self.x() + self.border_handle_size_diff)) or # Left
        # Right-Top
        (e_pos.y() < self.y() + self.border_handle_size_diff) and # Top
        (e_pos.x() > self.x() + self.width() - self.border_handle_size_diff)): # Right
            # Left - Bottom
            if ((e_pos.y() > self.y() + self.height() - self.border_handle_size_diff) and # Bottom
            (e_pos.x() < self.x()
                + self.border_handle_size_diff)): # Left
                didModeChange = self.try_set_mode(ResizableContainerMode.RESIZEBL)
                # Right - Bottom
            if ((e_pos.y() > self.y() + self.height() - self.border_handle_size_diff) and # Bottom
            (e_pos.x() > self.x() + self.width() - self.border_handle_size_diff)): # Right
                didModeChange = self.try_set_mode(ResizableContainerMode.RESIZEBR)
            # Left - Top
            if ((e_pos.y() < self.y() + self.border_handle_size_diff) and # Top
            (e_pos.x() < self.x() + self.border_handle_size_diff)): # Left
                didModeChange = self.try_set_mode(ResizableContainerMode.RESIZETL)
            # Right - Top
            if ((e_pos.y() < self.y() + self.border_handle_size_diff) and # Top
            (e_pos.x() > self.x() + self.width() - self.border_handle_size_diff)): # Right
                didModeChange = self.try_set_mode(ResizableContainerMode.RESIZETR)

        # if we're ignoring the corners, try the edges
        
        # check cursor horizontal position (check left and right edges)
        if ((not didModeChange) and (e_pos.x() < self.x() + self.border_handle_size_diff) or # Left
            (e_pos.x() > self.x() + self.width() - self.border_handle_size_diff)): # Right
            if e_pos.x() < self.x() + self.border_handle_size_diff: # Left
                didModeChange = self.try_set_mode(ResizableContainerMode.RESIZEL)
            else: # Right
                didModeChange = self.try_set_mode(ResizableContainerMode.RESIZER)

        # check cursor vertical position (check top and bottom edges)
        if ((not didModeChange) and (e_pos.y() > self.y() + self.height() - self.border_handle_size_diff) or # Bottom
            (e_pos.y() < self.y() + self.border_handle_size_diff)): # Top
            if e_pos.y() < self.y() + self.border_handle_size_diff: # Top
                didModeChange = self.try_set_mode(ResizableContainerMode.RESIZET)
            else: # Bottom
                didModeChange = self.try_set_mode(ResizableContainerMode.RESIZEB)
        
        # Otherwise we're not hovering any corners or edges. Check and see if we're moving
        if (not didModeChange):
            didModeChange = self.try_set_mode(ResizableContainerMode.MOVE)
            if (not didModeChange):
                # if we don't allow MOVE mode, set to NONE mode
                didModeChange = self.try_set_mode(ResizableContainerMode.NONE)

        # Finally update the cursor
        if didModeChange:
            self.setCursor(self.mode.get_mode_cursor())

    def setChildWidget(self, cWidget):
        if cWidget:
            self.childWidget = cWidget
            self.childWidget.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
            self.childWidget.setParent(self)
            self.childWidget.releaseMouse()
            self.vLayout.addWidget(cWidget)
            self.vLayout.setContentsMargins(0,0,0,0)

    def popupShow(self, pt: QPoint):
        if self.menu.isEmpty:
            return
        global_ = self.mapToGlobal(pt)
        self.m_showMenu = True
        self.menu.exec(global_)
        self.m_showMenu = False

    def paintEvent(self, e: QtGui.QPaintEvent):
        painter = QtGui.QPainter(self)
        color = (r, g, b, a) = (255, 0, 0, 16)
        painter.fillRect(e.rect(), QColor(r, g, b, a))

        rect = e.rect()
        rect.adjust(0,0,-1,-1)

        if self.m_infocus:
            painter.setPen(QColor(r, g, b))
            painter.drawRect(rect)

        # Draw highlighted edges:
        currHighlightRect = self.mode.get_highlight_rect(rect, self.border_handle_size_diff)
        if currHighlightRect is not None:
            painter.setPen(self.hoverEdgeRectColor)
            painter.drawRect(currHighlightRect)


    def mousePressEvent(self, e: QtGui.QMouseEvent):
        self.position = QPoint(e.globalX() - self.geometry().x(), e.globalY() - self.geometry().y())
        if not self.m_isEditing:
            return
        if not self.m_infocus:
            return
        if not e.buttons() and QtCore.Qt.LeftButton:
            self.setCursorShape(e.pos())
            return
        if e.button() == QtCore.Qt.RightButton:
            self.popupShow(e.pos())
            e.accept()

    def keyPressEvent(self, e: QtGui.QKeyEvent):
        if not self.m_isEditing: return
        if e.key() == QtCore.Qt.Key_Delete:
            self.deleteLater()
        # Moving container with arrows
        if QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:
            newPos = QPoint(self.x(), self.y())
            if e.key() == QtCore.Qt.Key_Up:
                newPos.setY(newPos.y() - 1)
            if e.key() == QtCore.Qt.Key_Down:
                newPos.setY(newPos.y() + 1)
            if e.key() == QtCore.Qt.Key_Left:
                newPos.setX(newPos.x() - 1)
            if e.key() == QtCore.Qt.Key_Right:
                newPos.setX(newPos.x() + 1)
            self.move(newPos)

        if QApplication.keyboardModifiers() == QtCore.Qt.ShiftModifier:
            if e.key() == QtCore.Qt.Key_Up:
                self.resize(self.width(), self.height() - 1)
            if e.key() == QtCore.Qt.Key_Down:
                self.resize(self.width(), self.height() + 1)
            if e.key() == QtCore.Qt.Key_Left:
                self.resize(self.width() - 1, self.height())
            if e.key() == QtCore.Qt.Key_Right:
                self.resize(self.width() + 1, self.height())
        self.newGeometry.emit(self.geometry())

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent):
        QWidget.mouseReleaseEvent(self, e)

    def mouseMoveEvent(self, e: QtGui.QMouseEvent):
        QWidget.mouseMoveEvent(self, e)
        if not self.m_isEditing:
            return
        if not self.m_infocus:
            return
        if not e.buttons() and QtCore.Qt.LeftButton:
            p = QPoint(e.x() + self.geometry().x(), e.y() + self.geometry().y())
            self.setCursorShape(p)
            self.update()

            return

        if (self.mode == ResizableContainerMode.MOVE) and e.buttons() and QtCore.Qt.LeftButton:
            canEdit = self.get_can_edit_current_mode()
            if canEdit:
                toMove = e.globalPos() - self.position
                if toMove.x() < 0:return
                if toMove.y() < 0:return
                if toMove.x() > self.parentWidget().width() - self.width(): return
                self.move(toMove)
                self.newGeometry.emit(self.geometry())
                self.parentWidget().repaint()

            return

        if (self.mode != ResizableContainerMode.MOVE) and e.buttons() and QtCore.Qt.LeftButton:
            canEdit = self.get_can_edit_current_mode()
            if canEdit:
                if self.mode == ResizableContainerMode.RESIZETL: # Left - Top
                    newwidth = e.globalX() - self.position.x() - self.geometry().x()
                    newheight = e.globalY() - self.position.y() - self.geometry().y()
                    toMove = e.globalPos() - self.position
                    self.resize(self.geometry().width() - newwidth, self.geometry().height() - newheight)
                    self.move(toMove.x(), toMove.y())
                elif self.mode == ResizableContainerMode.RESIZETR: # Right - Top
                    newheight = e.globalY() - self.position.y() - self.geometry().y()
                    toMove = e.globalPos() - self.position
                    self.resize(e.x(), self.geometry().height() - newheight)
                    self.move(self.x(), toMove.y())
                elif self.mode== ResizableContainerMode.RESIZEBL: # Left - Bottom
                    newwidth = e.globalX() - self.position.x() - self.geometry().x()
                    toMove = e.globalPos() - self.position
                    self.resize(self.geometry().width() - newwidth, e.y())
                    self.move(toMove.x(), self.y())
                elif self.mode == ResizableContainerMode.RESIZEB: # Bottom
                    self.resize(self.width(), e.y())
                elif self.mode == ResizableContainerMode.RESIZEL: # Left
                    newwidth = e.globalX() - self.position.x() - self.geometry().x()
                    toMove = e.globalPos() - self.position
                    self.resize(self.geometry().width() - newwidth, self.height())
                    self.move(toMove.x(), self.y())
                elif self.mode == ResizableContainerMode.RESIZET:# Top
                    newheight = e.globalY() - self.position.y() - self.geometry().y()
                    toMove = e.globalPos() - self.position
                    self.resize(self.width(), self.geometry().height() - newheight)
                    self.move(self.x(), toMove.y())
                elif self.mode == ResizableContainerMode.RESIZER: # Right
                    self.resize(e.x(), self.height())
                elif self.mode == ResizableContainerMode.RESIZEBR:# Right - Bottom
                    self.resize(e.x(), e.y())
            else:
                print("Can't edit current mode! It's read only!")

            self.parentWidget().repaint()
        self.newGeometry.emit(self.geometry())



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # self.showMaximized()
        lab1 = QLabel("Label1")
        lab2 = QLabel("Label2")
        currReadOnlyOptions = (TContainer.ResizableContainerOption.NONE | TContainer.ResizableContainerOption.RESIZEL | TContainer.ResizableContainerOption.RESIZER)
        currEditableOptions = (TContainer.ResizableContainerOption.NONE | TContainer.ResizableContainerOption.RESIZER)

        con1 = TContainer(self, currReadOnlyOptions, currEditableOptions, QPoint(10,10), lab1)
        
        # con1 = TContainer(self, (TContainer.ResizableContainerOption.NONE | TContainer.ResizableContainerOption.RESIZEL | TContainer.ResizableContainerOption.RESIZER), QPoint(10,10), lab1)
        # con1.mode = ResizableContainerMode.RESIZER
        currReadOnlyOptions = (TContainer.ResizableContainerOption.NONE | TContainer.ResizableContainerOption.MOVE | TContainer.ResizableContainerOption.RESIZEL | TContainer.ResizableContainerOption.RESIZER)
        currEditableOptions = (TContainer.ResizableContainerOption.NONE | TContainer.ResizableContainerOption.RESIZEL | TContainer.ResizableContainerOption.RESIZER)
        con2 = TContainer(self, currReadOnlyOptions, currEditableOptions, QPoint(20,50), lab2)
        # con2.mode = ResizableContainerMode.NONE
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())