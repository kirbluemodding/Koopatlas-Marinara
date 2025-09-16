import sys
import os
import os.path

# this version of koopatlas uses PyQt6, and any other versions are currently unsupported.
# since i do plan on adding PyQt5 support again (and support for PyQt7+ in the future), i've left some random compat stuff here.
# HOWEVER, PyQt4 and below will not be supported due to their extreme age and the fact that they are no longer commonly used.

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

except (ImportError, NameError):
    errormsg = 'PyQt6 is not currently installed. Either wait a thousand years for PyQt5 support, or spend 3 seconds installing PyQt6.'
    raise Exception(errormsg)

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
