from common import *
from PyQt6.QtGui import *
import re

def editableColourStr(array):
    return '#%02X%02X%02X (%d)' % tuple(array)

NICE_STR_RE = re.compile('^#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})\s*(?:\((\d+)\))?$')
def colourFromNiceStr(thing):
    match = NICE_STR_RE.match(thing)
    try:
        if match:
            r,g,b,a = match.groups()
            return (int(r,16), int(g,16), int(b,16), int(a) if a is not None else 255)
    except:
        pass
    return None

class ColorDelegate(QtWidgets.QItemDelegate):
    '''new color picker, replaces typing in a hex code manually'''
    '''strangely also the only piece of code that uses super'''
    def __init__(self, parent=None):
        super(ColorDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        color = index.data(QtCore.Qt.ItemDataRole.DecorationRole)
        
        if color:
            rect = option.rect.adjusted(2, 2, -2, -2)
            painter.setBrush(QtGui.QBrush(color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRect(rect)
        text = index.data(QtCore.Qt.ItemDataRole.DisplayRole)
        if text:
            option.rect.adjust(rect.width() + 4, 0, 0, 0)
            super(ColorDelegate, self).paint(painter, option, index)

    def createEditor(self, parent, _option, index):
        color = index.data(QtCore.Qt.ItemDataRole.DecorationRole)
        dialog = QtWidgets.QColorDialog(parent)
        dialog.setCurrentColor(color)
        dialog.setOption(QtWidgets.QColorDialog.ColorDialogOption.DontUseNativeDialog, True)
        dialog.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            selected_color = dialog.currentColor()
            if selected_color.isValid():
                r, g, b, a = selected_color.getRgb()
                model = index.model()
                model.setData(index, '#%02X%02X%02X (%d)' % (r, g, b, a), QtCore.Qt.ItemDataRole.EditRole)
            return None
        return None

    def setEditorData(self, editor, index):
        color = index.data(QtCore.Qt.ItemDataRole.DecorationRole)
        if color:
            editor.setCurrentColor(color)

    def setModelData(self, editor, model, index):
        color = editor.currentColor()
        if color.isValid():
            r, g, b, a = color.getRgb()
            model.setData(index, '#%02X%02X%02X (%d)' % (r, g, b, a), QtCore.Qt.ItemDataRole.EditRole)

class KPWorldTableModel(QtCore.QAbstractTableModel):
    FIELDS = ('Name', 'World ID', 'Track ID',
            'FS Text 1', 'FS Text 2',
            'FS Hint 1', 'FS Hint 2',
            'HUD Text 1', 'HUD Text 2',
            'HUD Hue', 'HUD Saturation', 'HUD Lightness',
            'Title Level')

    def __init__(self, kpmap, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)

        self.currentMap = kpmap
        self.worlds = kpmap.worlds

    def columnCount(self, parent):
        return len(self.FIELDS)
    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Orientation.Horizontal:
            if role == QtCore.Qt.ItemDataRole.DisplayRole:
                return self.FIELDS[section]
        else:
            if role == QtCore.Qt.ItemDataRole.DisplayRole:
                return str(self.worlds[section].uniqueKey)

        return None

    def rowCount(self, parent):
        if parent.isValid():
            return 0
        else:
            return len(self.worlds)

    def data(self, index, role):
        if index.isValid():
            entry = self.worlds[index.row()]
            col = index.column()

            if role == QtCore.Qt.ItemDataRole.DisplayRole or role == QtCore.Qt.ItemDataRole.EditRole:
                if col == 0:
                    return entry.name
                elif col == 1:
                    return entry.worldID
                elif col == 2:
                    return entry.musicTrackID
                elif col == 3 or col == 4:
                    return editableColourStr(entry.fsTextColours[col - 3])
                elif col == 5 or col == 6:
                    return editableColourStr(entry.fsHintColours[col - 5])
                elif col == 7 or col == 8:
                    return editableColourStr(entry.hudTextColours[col - 7])
                elif col >= 9 and col <= 11:
                    return entry.hudHintTransform[col - 9]
                elif col == 12:
                    return entry.titleScreenID

            if role == QtCore.Qt.ItemDataRole.DecorationRole:
                if col == 3 or col == 4:
                    return QtGui.QColor(*entry.fsTextColours[col - 3])
                elif col == 5 or col == 6:
                    return QtGui.QColor(*entry.fsHintColours[col - 5])
                elif col == 7 or col == 8:
                    return QtGui.QColor(*entry.hudTextColours[col - 7])

        return None

    def flags(self, index):
        return QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEditable

    def setData(self, index, value, role):
        if index.isValid():
            if role == QtCore.Qt.ItemDataRole.EditRole:
                success = False

                entry = self.worlds[index.row()]
                col = index.column()

                if col == 0:
                    entry.name = str(value)
                    success = True
                elif col == 1:
                    entry.worldID = str(value)
                    success = True
                elif col == 2:
                    try:
                        v = int(value)
                        ok = True
                    except ValueError:
                        ok = False
                    if ok:
                        entry.musicTrackID = v
                        success = True
                elif col >= 3 and col <= 8:
                    newCol = colourFromNiceStr(str(value))
                    if newCol:
                        success = True
                        if col == 3:
                            entry.fsTextColours = (newCol, entry.fsTextColours[1])
                        elif col == 4:
                            entry.fsTextColours = (entry.fsTextColours[0], newCol)
                        elif col == 5:
                            entry.fsHintColours = (newCol, entry.fsHintColours[1])
                        elif col == 6:
                            entry.fsHintColours = (entry.fsHintColours[0], newCol)
                        elif col == 7:
                            entry.hudTextColours = (newCol, entry.hudTextColours[1])
                        elif col == 8:
                            entry.hudTextColours = (entry.hudTextColours[0], newCol)
                elif col >= 9 and col <= 11:
                    try:
                        v = int(value)
                        ok = True
                    except ValueError:
                        ok = False
                    if ok:
                        new = list(entry.hudHintTransform)
                        new[col - 9] = v
                        entry.hudHintTransform = new
                        success = True
                elif col == 12:
                    entry.titleScreenID = str(value)
                    success = True

                if success:
                    self.dataChanged.emit(index, index)
                return success

        return False


    def addEntryToEnd(self):
        self.beginInsertRows(QtCore.QModelIndex(), len(self.worlds), len(self.worlds))
        entry = KPWorldDef()
        entry.uniqueKey = self.currentMap.allocateWorldDefKey()
        self.worlds.append(entry)
        self.endInsertRows()

    def removeRows(self, row, count, parent):
        if not parent.isValid():
            if row >= 0 and (row + count) <= len(self.worlds):
                self.beginRemoveRows(parent, row, row+count-1)
                for i in range(count):
                    del self.worlds[row]
                self.endRemoveRows()



class KPWorldEditor(QtWidgets.QWidget):
    def __init__(self, kpmap, parent=None):
        QtWidgets.QWidget.__init__(self, parent, QtCore.Qt.WindowType.Window)
        self.setWindowTitle('World Editor - Koopatlas Marinara Edition')
        self.setWindowIcon(QIcon('Resources/Icon/Globe.png')) 
        self.resize(600, 200)

        self.dataView = QtWidgets.QTableView(self)

        self.addButton = QtWidgets.QPushButton('Add', self)
        self.removeButton = QtWidgets.QPushButton('Remove', self)

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.dataView, 0, 0, 1, 2)
        layout.addWidget(self.addButton, 1, 0, 1, 1)
        layout.addWidget(self.removeButton, 1, 1, 1, 1)

        self.model = KPWorldTableModel(kpmap, self)
        self.dataView.setModel(self.model)
        
        # Create an instance of the color delegate and set it for the color columns
        color_delegate = ColorDelegate(self.dataView)
        for col in range(3, 9):
            self.dataView.setItemDelegateForColumn(col, color_delegate)

        self.addButton.clicked.connect(self.model.addEntryToEnd)
        self.removeButton.clicked.connect(self.removeCurrentEntry)

    def removeCurrentEntry(self):
        what = self.dataView.selectionModel().currentIndex()
        if what.isValid():
            what = what.row()
            key = self.model.worlds[what].uniqueKey
            self.model.removeRows(what, 1, QtCore.QModelIndex())

