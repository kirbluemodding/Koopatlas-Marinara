import sys
import os
import os.path

# compatibility slop for PyQt6/PyQt5
# PyQt4 support has been removed due to how outdated it is, and the fact that i don't know of any other tools for NSMBW that use it (basically there's no reason to use it or have it installed without PyQt5 or PyQt6)
# is there probably a better way to set this up and probably keep PyQt4 compatibility? probably, but do i care? no

PYQT6 = False

try:
    # try PyQt6 first
    from PyQt6 import QtCore, QtGui, QtWidgets
    QtCore.QString = str
    PYQT6 = True

    # some enum families
    ItemDataRole   = QtCore.Qt.ItemDataRole
    Alignment      = QtCore.Qt.AlignmentFlag
    Orientation    = QtCore.Qt.Orientation
    ItemFlag       = QtCore.Qt.ItemFlag
    DockWidgetArea = QtCore.Qt.DockWidgetArea
    DockFeatures   = QtWidgets.QDockWidget.DockWidgetFeature
    ToolButtonStyle= QtCore.Qt.ToolButtonStyle
    ToolButtonMode = QtWidgets.QToolButton.ToolButtonPopupMode
    SizePolicy     = QtWidgets.QSizePolicy.Policy
    ViewportUpdate = QtWidgets.QGraphicsView.ViewportUpdateMode
    DragMode       = QtWidgets.QGraphicsView.DragMode
    DragDropMode   = QtWidgets.QAbstractItemView.DragDropMode
    SelectionMode  = QtWidgets.QAbstractItemView.SelectionMode
    Movement       = QtWidgets.QListView.Movement
    LayoutMode     = QtWidgets.QListView.LayoutMode
    ViewMode       = QtWidgets.QListView.ViewMode
    Key            = QtCore.Qt.Key
    MouseButton    = QtCore.Qt.MouseButton
    KeyboardMod    = QtCore.Qt.KeyboardModifier
    CheckState     = QtCore.Qt.CheckState
    GlobalColor    = QtCore.Qt.GlobalColor
    IteratorFlag   = QtWidgets.QTreeWidgetItemIterator.IteratorFlag
    GraphicsItemFlag = QtWidgets.QGraphicsItem.GraphicsItemFlag

    EasingType = QtCore.QEasingCurve.Type

    # two cool singletons. wait does that make them doubletons now?
    AntiAliasing = QtGui.QPainter.RenderHint.Antialiasing
    Format_ARGB32 = QtGui.QImage.Format.Format_ARGB32

    # keyboard shortcuts
    Copy      = QtGui.QKeySequence.StandardKey.Copy
    Paste     = QtGui.QKeySequence.StandardKey.Paste
    SelectAll = QtGui.QKeySequence.StandardKey.SelectAll
    ZoomIn    = QtGui.QKeySequence.StandardKey.ZoomIn
    ZoomOut   = QtGui.QKeySequence.StandardKey.ZoomOut

    def add_action_compat(menu_or_toolbar, text, slot=None, shortcut=None, parent=None):
        action = QtGui.QAction(text, parent or menu_or_toolbar)
        if shortcut is not None:
            action.setShortcut(QtGui.QKeySequence(shortcut))
        if slot is not None:
            action.triggered.connect(slot)
        menu_or_toolbar.addAction(action)
        return action

    def app_exec(app):
        return app.exec()

    def make_qkeyseq(standard):
        return QtGui.QKeySequence(standard)

except ImportError:
    # fallback to the lame and inferior PyQt5
    from PyQt5 import QtCore, QtGui, QtWidgets
    QtCore.QString = str

    # some MORE enum families, even though PyQt5 has them flat let's just do this for consistency's sake
    ItemDataRole   = QtCore.Qt
    Alignment      = QtCore.Qt
    Orientation    = QtCore.Qt
    ItemFlag       = QtCore.Qt
    DockWidgetArea = QtCore.Qt
    DockFeatures   = QtCore.Qt
    ToolButtonStyle= QtCore.Qt
    ToolButtonMode = QtWidgets.QToolButton
    SizePolicy     = QtWidgets.QSizePolicy
    ViewportUpdate = QtWidgets.QGraphicsView
    DragMode       = QtWidgets.QGraphicsView
    DragDropMode   = QtWidgets.QAbstractItemView
    SelectionMode  = QtWidgets.QAbstractItemView
    Movement       = QtWidgets.QListView
    LayoutMode     = QtWidgets.QListView
    ViewMode       = QtWidgets.QListView
    Key            = QtCore.Qt
    MouseButton    = QtCore.Qt
    KeyboardMod    = QtCore.Qt
    CheckState     = QtCore.Qt
    GlobalColor    = QtCore.Qt
    IteratorFlag   = QtWidgets.QTreeWidgetItemIterator
    GraphicsItemFlag = QtWidgets.QGraphicsItem

    EasingType = QtCore.QEasingCurve

    # the doubletons
    AntiAliasing = QtGui.QPainter.Antialiasing
    Format_ARGB32 = QtGui.QImage.Format_ARGB32

    # keyboard shortcuts
    Copy      = QtGui.QKeySequence.Copy
    Paste     = QtGui.QKeySequence.Paste
    SelectAll = QtGui.QKeySequence.SelectAll
    ZoomIn    = QtGui.QKeySequence.ZoomIn
    ZoomOut   = QtGui.QKeySequence.ZoomOut

    def add_action_compat(menu_or_toolbar, text, slot=None, shortcut=None, parent=None):
        if slot is not None and shortcut is not None:
            return menu_or_toolbar.addAction(text, slot, shortcut)
        elif slot is not None:
            return menu_or_toolbar.addAction(text, slot)
        elif shortcut is not None:
            return menu_or_toolbar.addAction(text, shortcut)
        else:
            return menu_or_toolbar.addAction(text)

    def app_exec(app):
        return app.exec_()

Qt = QtCore.Qt
QtCompatVersion = QtCore.QT_VERSION

# easing curve compatibility
CURVE_SHAPE_TO_EASING = {
    0: EasingType.InQuad,     # EaseInCurve
    1: EasingType.OutQuad,    # EaseOutCurve
    2: EasingType.InOutSine,  # EaseInOutCurve
    3: EasingType.Linear,     # LinearCurve
    4: EasingType.InOutSine,  # SineCurve
}

def set_curve_shape_compat(timeline, shape):
    if isinstance(shape, int):
        etype = CURVE_SHAPE_TO_EASING.get(shape, EasingType.InOutSine)
    else:
        etype = shape
    timeline.setEasingCurve(QtCore.QEasingCurve(etype))

from main import KP
from tileset import *
from mapdata import *
