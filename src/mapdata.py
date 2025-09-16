from common import *
import weakref
import mapfile

TILE_SIZE = (24,24)
MAP_SIZE_IN_TILES = (512,512)
MAP_SIZE = (MAP_SIZE_IN_TILES[0] * TILE_SIZE[0], MAP_SIZE_IN_TILES[1] * TILE_SIZE[1])

@mapfile.dumpable('layer')
class KPLayer(object):
    dump_attribs = ('name', '_visible')

    def __repr__(self):
        return "<KPLayer %r>" % self.name

    def __init__(self):
        self.name = ''
        self._visible = True

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        if self._visible == value:
            return
        self._visible = value

        self._visibilityChanged(value)

    def _visibilityChanged(self, value):
        pass

    def setActivated(self, value, listToUse=None):
        # return

        flag1 = QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
        flag2 = QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable

        if listToUse is None:
            listToUse = self.objects

        for obj in listToUse:
            item = obj.qtItem
            if item:
                item.setFlag(flag1, value)
                item.setFlag(flag2, value)
                item.setAcceptHoverEvents(value)


@mapfile.dumpable('object')
class KPObject(object):
    dump_attribs = ('position', 'size', 'tileset', 'kind')

    def _load(self, mapObj, src):
        self.kindObj = KP.tileset(self.tileset).objects[self.kind]
        self.updateCache()

    def __init__(self):
        self.position = (0,0)
        self.size = (1,1)
        self.kind = 0
        self.kindObj = None
        self.cache = []
        self.tileset = None
        self.qtItem = None

    def updateCache(self):
        self.cache = self.kindObj.render(self.size)

    def __deepcopy__(self, memo):
        return mapfile.load(mapfile.dump(self))


@mapfile.dumpable('tile_layer')
class KPTileLayer(KPLayer):
    dump_attribs = KPLayer.dump_attribs + ('tileset', 'objects')

    def _load(self, mapObj, src):
        self.updateCache()

    def __repr__(self):
        return "<KPTileLayer %r with %r>" % (self.name, self.tileset)

    def __init__(self):
        KPLayer.__init__(self)
        self.tileset = ''
        self.objects = []
        self.cache = ['DUMMY_FLAG']
        self.updateCache()

        self.icon = KP.icon('LayerTile')

    def _visibilityChanged(self, value):
        for obj in self.objects:
            item = obj.qtItem
            if item:
                item.setVisible(value)

    def updateCache(self):
        if len(self.objects) == 0:
            if len(self.cache) != 0:
                self.cache = []
                self.cacheBasePos = (0,0)
                self.cacheSize = (0,0)
            return

        x1, x2 = MAP_SIZE_IN_TILES[0] - 1, 0
        y1, y2 = MAP_SIZE_IN_TILES[1] - 1, 0

        for obj in self.objects:
            x, y = obj.position
            w, h = obj.size
            right, bottom = (x+w-1), (y+h-1)

            if x < x1:
                x1 = x
            if y < y1:
                y1 = y
            if right > x2:
                x2 = right
            if bottom > y2:
                y2 = bottom


        # create the cache
        # I was going to just resize it, but setting every tile to -1
        # in Python would probably be slower than creating a new one ...
        size = (x2 - x1 + 1, y2 - y1 + 1)
        width, height = size

        cache = [[-1 for i in range(width)] for j in range(height)]
        self.cache = cache

        self.cacheBasePos = (x1, y1)
        self.cacheSize = size

        # now generate the thing
        for obj in self.objects:
            oX, oY = obj.position
            baseX = oX - x1
            y = oY - y1

            for row in obj.cache:
                destRow = cache[y]
                x = baseX
                for tile in row:
                    destRow[x] = tile
                    x += 1
                y += 1


@mapfile.dumpable('associate_layer')
class KPPathTileLayer(KPLayer):
    dump_attribs = KPLayer.dump_attribs + ('tileset', 'objects', 'doodads', 'folder')

    def _dump(self, mapObj, dest):
        if isinstance(self.associate, KPNode):
            dest['associatedRef'] = ('node', mapObj.refNode(self.associate))
        else:
            dest['associatedRef'] = ('path', mapObj.refPath(self.associate))

    def _load(self, mapObj, src):
        assocType, assocID = src['associatedRef']

        if assocType == 'path':
            self.associate = mapObj.derefPath(assocID)
        else:
            self.associate = mapObj.derefNode(assocID)

        self.updateCache()

    def __repr__(self):
        return "<KPPathTileLayer with %r connected to %r>" % (self.tileset, self.associate)

    def __init__(self, pathnode=None):
        KPLayer.__init__(self)

        self.cache = ['DUMMY_FLAG']

        self.tileset = ''
        self.objects = []
        self.doodads = []
        self.associate = pathnode
        self.folder = ''

        if pathnode is None:
            return

        self.updateCache()

    def _visibilityChanged(self, value):
        for obj in self.objects:
            item = obj.qtItem
            if item:
                item.setVisible(value)

        for obj in self.doodads:
            item = obj.qtItem
            if item:
                item.setVisible(value)

    def setActivated(self, value, listToUse=None):
        # return

        flag1 = QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
        flag2 = QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable

        if listToUse is None:
            listToUse = self.objects + self.doodads

        for obj in listToUse:
            item = obj.qtItem
            if item:
                item.setFlag(flag1, value)
                item.setFlag(flag2, value)

    def updateCache(self):
        if len(self.objects) == 0:
            if len(self.cache) != 0:
                self.cache = []
                self.cacheBasePos = (0,0)
                self.cacheSize = (0,0)
            return

        # oh gosh, how did someone get a KPDoodad into self.objects (2021-08-05)
        remove = []
        for obj in self.objects:
            if not isinstance(obj, KPObject):
                remove.append(obj)
        for obj in remove:
            self.objects.remove(obj)
        remove = []
        for dood in self.doodads:
            if not isinstance(obj, KPDoodad):
                remove.append(dood)
        for dood in remove:
            self.doodads.remove(dood)

        x1, x2 = MAP_SIZE_IN_TILES[0] - 1, 0
        y1, y2 = MAP_SIZE_IN_TILES[1] - 1, 0

        for obj in self.objects:
            x, y = obj.position
            w, h = obj.size
            right, bottom = (x+w-1), (y+h-1)

            if x < x1:
                x1 = x
            if y < y1:
                y1 = y
            if right > x2:
                x2 = right
            if bottom > y2:
                y2 = bottom


        # create the cache
        # I was going to just resize it, but setting every tile to -1
        # in Python would probably be slower than creating a new one ...
        size = (x2 - x1 + 1, y2 - y1 + 1)
        width, height = size

        cache = [[-1 for i in range(width)] for j in range(height)]
        self.cache = cache

        self.cacheBasePos = (x1, y1)
        self.cacheSize = size

        # now generate the thing
        for obj in self.objects:
            oX, oY = obj.position
            baseX = oX - x1
            y = oY - y1

            for row in obj.cache:
                destRow = cache[y]
                x = baseX
                for tile in row:
                    destRow[x] = tile
                    x += 1
                y += 1

    def setTileset(self, tileset):
        self.tileset = tileset

        tsObjects = KP.tileset(tileset).objects

        for obj in self.objects:
            obj.tileset = tileset
            obj.kindObj = tsObjects[obj.kind]
            obj.updateCache()

        self.updateCache()


@mapfile.dumpable('doodad')
class KPDoodad(object):
    dump_attribs = ('position', 'size', 'angle', 'animations')

    def _dump(self, mapObj, dest):
        dest['sourceRef'] = mapObj.refDoodad(self.source)

    def _load(self, mapObj, src):
        self.source = mapObj.derefDoodad(src['sourceRef'])

    def __init__(self):
        self.position = [0,0]
        self.size = [0,0]
        self.angle = 0
        self.source = None
        self.animations = []
        self.timelines = None

    def setDefaultSize(self):
        pixmap = self.source[1]
        self.size = [pixmap.width(), pixmap.height()]

    class doodadTimeLine(QtCore.QTimeLine):
        def __init__(self):
            QtCore.QTimeLine.__init__(self)

            self.delayTimer = QtCore.QTimer()
            self.delayTimer.timeout.connect(self.startTimeline)
            self.delayTimer.setSingleShot(True)

            self.offsetTimer = QtCore.QTimer()
            self.offsetTimer.timeout.connect(self.startTimeline)
            self.offsetTimer.setSingleShot(True)

            self.reversible = False
            self.reversed = False

        def restartDelay(self):

            if self.reversible:
                if not self.reversed:
                    self.reversed = True
                    self.toggleDirection()
                    self.startTimeline()
                    return
                else:
                    self.toggleDirection()
                    self.reversed = False

            self.delayTimer.start()

        def start(self):

            self.offsetTimer.start()

        def startTimeline(self):
            if QtCore.QTimeLine.state(self) == 0:
                QtCore.QTimeLine.start(self)
            else:
                QtCore.QTimeLine.stop(self)
                QtCore.QTimeLine.start(self)


    def cleanUpAnimations(self):
        myTimelines = self.timelines
        if myTimelines is None: return

        timelineList = KP.mapScene.timeLines

        for timeline in myTimelines:
            try:
                timelineList.remove(timeline)
            except ValueError:
                pass

        self.timelines = None

    def setupAnimations(self):
        self.cleanUpAnimations()

        timelineList = KP.mapScene.timeLines
        myTimelines = []

        for anim in self.animations:
            if len(anim) == 6:
                anim.extend([0,0])

            if len(anim) == 7:
                anim.extend([0])

            Loop, Curve, Frames, Type, StartVal, EndVal, Delay, DelayOffset = anim

            Timeline = self.doodadTimeLine()

            # Interpolate the correct modifier
            if Curve == "Linear":
                set_curve_shape_compat(Timeline, 3)
            elif Curve == "Sinusoidial":
                set_curve_shape_compat(Timeline, 4)
            elif Curve == "Cosinoidial":
                set_curve_shape_compat(Timeline, 5)
            Timeline.setFrameRange(round(StartVal), round(EndVal))

            if Loop == "Contiguous":
                Timeline.setLoopCount(1)
            elif Loop == "Loop":
                Timeline.setLoopCount(1)
                Timeline.finished.connect(Timeline.restartDelay)
            elif Loop == "Reversible Loop":
                Timeline.setLoopCount(1)
                Timeline.reversible = True
                Timeline.finished.connect(Timeline.restartDelay)

            # Setup the Delay Timer and Duration
            # Wii goes at 60 frames per second
            Timeline.delayTimer.setInterval(round(Delay/60.0*1000))
            Timeline.offsetTimer.setInterval(round(DelayOffset/60.0*1000))
            Timeline.setDuration(round(Frames/60.0*1000))

            timelineList.append(Timeline)
            myTimelines.append(Timeline)

        self.timelines = myTimelines

    def isRGBA8(self):
        # TODO: this is obviously a huge hack! Replace this with a system that actually
        # lets the user choose the texture format for each doodad.
        return self.source[0].startswith('Cloud') or self.source[0].startswith('Tiling_Cloud')


@mapfile.dumpable('doodad_layer')
class KPDoodadLayer(KPLayer):
    dump_attribs = KPLayer.dump_attribs + ('objects',)

    def __repr__(self):
        return "<KPDoodadLayer %r>" % self.name

    def __init__(self):
        KPLayer.__init__(self)
        self.objects = []

        self.icon = KP.icon('LayerObjects')

    def _visibilityChanged(self, value):
        for obj in self.objects:
            item = obj.qtItem
            if item:
                item.setVisible(value)


@mapfile.dumpable('node')
class KPNode(object):
    dump_attribs = (
            'position', 'actions', 'level', 'hasSecret', 'mapChange',
            'transition', 'mapID', 'foreignID', 'worldDefID')

    def _dump(self, mapObj, dest):
        dest['exitIDs'] = list(map(mapObj.refPath, self.exits))

    def _load(self, mapObj, src):
        self.exitIDs = src['exitIDs']
        # The exits array will be created by KPPathLayer._load after the
        # paths have all been created.

    def __init__(self):
        self.position = (0,0)
        self.actions = []
        self.exits = []
        self.level = None
        self.hasSecret = False
        self.mapChange = None
        self.transition = 0
        self.mapID = None
        self.foreignID = None
        self.worldDefID = None

    def isStop(self):
        return True if (self.level or self.mapChange or len(self.exits) != 2) else False


@mapfile.dumpable('path')
class KPPath(object):
    dump_attribs = ('unlockSpec', 'animation', 'movementSpeed')

    def _dump(self, mapObj, dest):
        dest['startNodeLink'] = mapObj.refNode(self._startNodeRef())
        dest['endNodeLink'] = mapObj.refNode(self._endNodeRef())
        # dest['linkedLayer'] = mapObj.refLayer(self.linkedLayer)

    def _load(self, mapObj, src):
        self._startNodeRef = weakref.ref(mapObj.derefNode(src['startNodeLink']))
        self._endNodeRef = weakref.ref(mapObj.derefNode(src['endNodeLink']))
        # self.linkedLayer = mapObj.derefLayer(src['linkedLayer'])

    def __init__(self, startNode=None, endNode=None, cloneFrom=None):
        # this is placed before the null ctor in case we load an old
        # kpmap that didn't have unlockSpec
        self.unlockSpec = None  # always unlocked, by default

        if startNode is None and endNode is None:
            # null ctor, ignore this
            # we're probably loaded from a file, so trust
            # that everything is correct ... _load will set it all up
            return

        self._startNodeRef = weakref.ref(startNode)
        self._endNodeRef = weakref.ref(endNode)

        startNode.exits.append(self)
        endNode.exits.append(self)

        if cloneFrom is None:
            self.animation = 0
        else:
            self.animation = cloneFrom.animation

        self.movementSpeed = 1.0
        # self.linkedLayer = None


    def setStart(self, newStart):
        currentStart = self._startNodeRef()
        if currentStart is not None:
            currentStart.exits.remove(self)

        newStart.exits.append(self)
        self._startNodeRef = weakref.ref(newStart)

    def setEnd(self, newEnd):
        currentEnd = self._endNodeRef()
        if currentEnd is not None:
            currentEnd.exits.remove(self)

        newEnd.exits.append(self)
        self._endNodeRef = weakref.ref(newEnd)


@mapfile.dumpable('path_layer')
class KPPathLayer(KPLayer):
    dump_attribs = KPLayer.dump_attribs + ('nodes', 'paths')

    def _load(self, mapObj, src):
        for node in self.nodes:
            node.exits = list(map(mapObj.derefPath, node.exitIDs))
            del node.exitIDs

    def __repr__(self):
        return "<KPPathLayer %r>" % self.name

    def __init__(self):
        KPLayer.__init__(self)
        self.nodes = []
        self.paths = []

        self.icon = KP.icon('LayerPath')

    def _visibilityChanged(self, value):
        for objList in (self.nodes, self.paths):
            for obj in objList:
                item = obj.qtItem
                if item:
                    item.setVisible(value)

    def setActivated(self, value):
        # return
        KPLayer.setActivated(self, value, self.nodes)

        flag = QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
        for path in self.paths:
            item = path.qtItem
            if item:
                item.setFlag(flag, value)


@mapfile.dumpable('world_definition')
class KPWorldDef(object):
    dump_attribs = ('uniqueKey', 'name', 'worldID', 'fsHintColours', 'fsTextColours', 'hudHintTransform', 'hudTextColours', 'musicTrackID', 'titleScreenID')

    def __init__(self):
        self.uniqueKey = -1
        self.name = 'Untitled World'
        self.worldID = '0'

        self.fsHintColours = ((0,0,0,255),(0,0,0,255))
        self.fsTextColours = ((255,255,255,255),(255,255,255,255))

        self.hudHintTransform = (0,0,0)
        self.hudTextColours = ((255,255,255,255),(255,255,255,255))

        self.musicTrackID = 0
        self.titleScreenID = '01-40'


@mapfile.dumpable('map_root')
class KPMap(object):
    dump_attribs = ('layers', 'associateLayers', 'nextLayerNumber', 'doodadDefinitions', 'worlds', 'bgName')

    def _preload(self, src):
        # we need this early so we can use the deref methods!
        for layer in self.layers:
            if isinstance(layer, KPPathLayer):
                self.pathLayer = layer

    def _load(self, mapObj, source):
        self.layerModel.list = self.layers
        self.doodadModel.list = self.doodadDefinitions

        if 'version' in source:
            self.version = source['version']
        else:
            self.version = 1

        self.deleteNullDoodads()

    def _dump(self, mapObj, dest):
        dest['version'] = self.version

    def save(self):
        path = self.filePath
        if path is None:
            raise "No path was specified for this map"

        KP.mainWindow.pathNodeList.setLayerFolders()
        self.associateLayers = KP.mainWindow.pathNodeList.getLayers()

        import mapfile
        dumped = mapfile.dump(self)
        with open(path, 'wb') as file:
            file.write(dumped)

    def export(self, path):
        from exporter import KPMapExporter
        exp = KPMapExporter(self)
        data = exp.build()
        with open(path, 'wb') as file:
            file.write(data)

    def __init__(self):
        self.version = 2

        self.filePath = None

        self.nextLayerNumber = 1

        self.pathLayer = self._createPathLayer()
        self.layers = [self.pathLayer]
        self.associateLayers = []
        self.layerModel = KPMap.LayerModel(self.layers)

        self.doodadDefinitions = []
        self.doodadModel = KPMap.DoodadModel(self.doodadDefinitions)

        self.worlds = []
        self.nextWorldKey = 1

        self.bgName = '/Maps/Water.brres'

    def allocateWorldDefKey(self):
        key = self.nextWorldKey
        self.nextWorldKey += 1
        return key

    def deleteNullDoodads(self):
        """Some maps have doodad definitions with null pixmaps. These
        cause errors when exporting, so we detect and delete them upon
        map load"""

        # Remove doodads referencing definitions with null pixmaps
        for L in self.layers:
            if isinstance(L, KPDoodadLayer):
                i = 0
                while i < len(L.objects):
                    doodad = L.objects[i]
                    if doodad.source[1].isNull():
                        print('WARNING: Deleting doodad referencing null definition: ' + doodad.source[0])
                        L.objects.pop(i)
                    else:
                        i += 1

        # And the bad doodad definitions themselves
        i = 0
        while i < len(self.doodadDefinitions):
            doodadDef = self.doodadDefinitions[i]
            if doodadDef[1].isNull():
                print('WARNING: Deleting null doodad definition: ' + doodadDef[0])
                self.doodadDefinitions.pop(i)
            else:
                i += 1

    # LAYERS
    class LayerModel(QtCore.QAbstractListModel):
        def __init__(self, layerList):
            QtCore.QAbstractListModel.__init__(self)
            self.list = layerList


        def headerData(self, section, orientation, role = ItemDataRole.DisplayRole):
            return 'Layer'

        def rowCount(self, parent):
            return len(self.list)

        def data(self, index, role = ItemDataRole.DisplayRole):
            try:
                if index.isValid():
                    layer = self.list[index.row()]

                    if (role == ItemDataRole.DisplayRole or role == ItemDataRole.EditRole):
                        return layer.name
                    elif role == ItemDataRole.DecorationRole:
                        return layer.icon
                    elif role == ItemDataRole.CheckStateRole:
                        return (CheckState.Checked if layer.visible else CheckState.Unchecked)

            except IndexError:
                pass

            return None

        def flags(self, index):
            if not index.isValid():
                return Qt.ItemFlag.ItemIsEnabled

            return Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsUserCheckable \
                    | QtCore.QAbstractListModel.flags(self, index)

        def setData(self, index, value, role = ItemDataRole.EditRole):
            if index.isValid():
                layer = self.list[index.row()]

                # enforce uniqueness for layer names
                usedLayerNames = {L.name for L in self.list}

                if role == ItemDataRole.EditRole:
                    value = str(value)
                    if len(value) > 0 and value not in usedLayerNames:
                        layer.name = value
                        self.dataChanged.emit(index, index)
                        return True

                elif role == ItemDataRole.CheckStateRole:
                    layer.visible = value
                    self.dataChanged.emit(index, index)
                    return True

            return False

    def _createPathLayer(self):
        layer = KPPathLayer()
        layer.name = 'Paths'
        return layer

    def createNewTileLayer(self, tilesetName):
        layer = KPTileLayer()
        layer.name = "Tilemap - Layer %d" % self.nextLayerNumber
        self.nextLayerNumber += 1
        layer.tileset = tilesetName
        return layer

    def createNewDoodadLayer(self):
        layer = KPDoodadLayer()
        layer.name = "Doodads - Layer %d" % self.nextLayerNumber
        self.nextLayerNumber += 1
        return layer

    def appendLayer(self, layer):
        return self.insertLayer(len(self.layers), layer)

    def insertLayer(self, index, layer):
        self.layerModel.beginInsertRows(QtCore.QModelIndex(), index, index)
        self.layers.insert(index, layer)
        self.layerModel.endInsertRows()
        return index

    def moveLayer(self, fromIndex, toIndex):
        if fromIndex == toIndex:
            return
        if fromIndex < 0 or toIndex < 0:
            return
        if fromIndex >= len(self.layers) or toIndex > len(self.layers):
            return
        if fromIndex == toIndex-1:
            return

        self.layerModel.beginMoveRows(
                QtCore.QModelIndex(), fromIndex, fromIndex,
                QtCore.QModelIndex(), toIndex)

        toMove = self.layers[fromIndex]
        newIndex = ((toIndex > fromIndex) and (toIndex - 1)) or toIndex

        del self.layers[fromIndex]
        self.layers.insert(newIndex, toMove)

        self.layerModel.endMoveRows()

        return newIndex

    def removeLayer(self, layer):
        if layer not in self.layers:
            return

        index = self.layers.index(layer)
        self.layerModel.beginRemoveRows(QtCore.QModelIndex(), index, index)
        del self.layers[index]
        self.layerModel.endRemoveRows()


    # DOODADS
    class DoodadModel(QtCore.QAbstractListModel):
        def __init__(self, doodadList):
            QtCore.QAbstractListModel.__init__(self)
            self.list = doodadList


        def headerData(self, section, orientation, role = ItemDataRole.DisplayRole):
            return 'Doodad'

        def rowCount(self, parent):
            return len(self.list)

        def data(self, index, role = ItemDataRole.DisplayRole):
            try:
                if index.isValid():
                    doodad = self.list[index.row()]

                    if role == ItemDataRole.DecorationRole:
                        return QtGui.QIcon(doodad[1])
                    elif role == ItemDataRole.ToolTipRole:
                        return doodad[0]
                    elif role == ItemDataRole.DisplayRole:
                        return doodad[0]

            except IndexError:
                pass

            return None

        def flags(self, index):
            if not index.isValid():
                return Qt.ItemIsEnabled
            return QtCore.QAbstractListModel.flags(self, index)

    def addDoodad(self, title, image):
        doodad = (title, image)

        index = len(self.doodadDefinitions)
        self.doodadModel.beginInsertRows(QtCore.QModelIndex(), index, index)
        self.doodadDefinitions.append(doodad)
        self.doodadModel.endInsertRows()

        return doodad

    def removeDoodad(self, doodad):
        if doodad not in self.doodadDefinitions:
            raise ValueError

        index = self.doodadDefinitions.index(doodad)
        self.doodadModel.beginRemoveRows(QtCore.QModelIndex(), index, index)
        del self.doodadDefinitions[index]
        self.doodadModel.endRemoveRows()


    # REFERENCES
    def refDoodad(self, doodad):
        return -1 if (doodad is None) else self.doodadDefinitions.index(doodad)
    def derefDoodad(self, ref):
        return self.doodadDefinitions[ref] if (ref >= 0) else None

    def refLayer(self, layer):
        return -1 if (layer is None) else self.layers.index(layer)
    def derefLayer(self, ref):
        return self.layers[ref] if (ref >= 0) else None

    def refPath(self, path):
        return -1 if (path is None) else self.pathLayer.paths.index(path)
    def derefPath(self, ref):
        return self.pathLayer.paths[ref] if (ref >= 0) else None

    def refNode(self, node):
        return -1 if (node is None) else self.pathLayer.nodes.index(node)
    def derefNode(self, ref):
        return self.pathLayer.nodes[ref] if (ref >= 0) else None


