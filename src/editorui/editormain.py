from common import *
from math import floor, ceil

from .objects import *
from .doodads import *
from .paths import *
from settings import *

class KPMapScene(QtWidgets.QGraphicsScene):
    def __init__(self):
        QtWidgets.QGraphicsScene.__init__(self, 0, 0, 512*24, 512*24)

        # todo: handle selectionChanged
        # todo: look up why I used setItemIndexMethod(self.NoIndex) in Reggie

        self.currentLayer = None
        KP.mapScene = self
        self.playing = False
        self.timeLines = []
        self.ticker = QtCore.QTimeLine(100000)
        self.ticker.setLoopCount(0)
        set_curve_shape_compat(self.ticker, 4)
        self.ticker.setFrameRange(0,100000)
        self.ticker.valueChanged.connect(self.viewportUpdateProxy)
        self.ticker.setUpdateInterval(round(1000/60.0))
        
        self.grid = int(settings.config["Window"]["grid_type"])

        # create an item for everything in the map
        for layer in KP.map.layers:
            if isinstance(layer, KPTileLayer):
                for obj in layer.objects:
                    self.addItem(KPEditorObject(obj, layer))
            elif isinstance(layer, KPDoodadLayer):
                for obj in layer.objects:
                    self.addItem(KPEditorDoodad(obj, layer))
            elif isinstance(layer, KPPathLayer):
                for inLayer in KP.map.associateLayers:
                    for obj in inLayer.objects:
                        self.addItem(KPEditorObject(obj, inLayer))
                    for obj in inLayer.doodads:
                        self.addItem(KPEditorDoodad(obj, inLayer))

                for node in layer.nodes:
                    self.addItem(KPEditorNode(node))

                for path in layer.paths:
                    self.addItem(KPEditorPath(path))

            layer.setActivated(False)


    def playPause(self):
        if self.playing == False:
            self.playing = True
            self.views()[0].setViewportUpdateMode(QtWidgets.QGraphicsView.ViewportUpdateMode.MinimalViewportUpdate)
            self.ticker.start()

            for timeline in self.timeLines:
                timeline.start()
            self.views()[0].viewport().update()

        else:
            self.playing = False
            self.views()[0].setViewportUpdateMode(QtWidgets.QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
            self.ticker.stop()

            for timeline in self.timeLines:
                timeline.stop()
            self.views()[0].viewport().update()


    def viewportUpdateProxy(self):
        self.views()[0].viewport().update()

    def drawForeground(self, painter, rect):
        if self.grid == 0: return # 2 is unfinished but will be copied from Reggie next
        GridColor = QtGui.QColor.fromRgb(255,255,255,100) # if we add themes this is a var for that
        Zoom = KP.mainWindow.ZoomLevel
        drawLine = painter.drawLine
        if self.grid == 1:
            # NOTE: this is still the roadrunnerslop as it's the exact same in reggie
            if Zoom >= 4:
                startx = rect.x()
                startx -= (startx % 24)
                endx = startx + rect.width() + 24

                starty = rect.y()
                starty -= (starty % 24)
                endy = starty + rect.height() + 24

                painter.setPen(QtGui.QPen(GridColor, 1, Qt.PenStyle.DotLine))

                x = startx
                y1 = rect.top()
                y2 = rect.bottom()
                while x <= endx:
                    drawLine(QtCore.QLineF(x, starty, x, endy))
                    x += 24

                y = starty
                x1 = rect.left()
                x2 = rect.right()
                while y <= endy:
                    drawLine(QtCore.QLineF(startx, y, endx, y))
                    y += 24


            if Zoom >= 2:
                startx = rect.x()
                startx -= (startx % 96)
                endx = startx + rect.width() + 96

                starty = rect.y()
                starty -= (starty % 96)
                endy = starty + rect.height() + 96

                painter.setPen(QtGui.QPen(GridColor, 1, Qt.PenStyle.DashLine))

                x = startx
                y1 = rect.top()
                y2 = rect.bottom()
                while x <= endx:
                    drawLine(QtCore.QLineF(x, starty, x, endy))
                    x += 96

                y = starty
                x1 = rect.left()
                x2 = rect.right()
                while y <= endy:
                    drawLine(QtCore.QLineF(startx, y, endx, y))
                    y += 96


            startx = rect.x()
            startx -= (startx % 192)
            endx = startx + rect.width() + 192

            starty = rect.y()
            starty -= (starty % 192)
            endy = starty + rect.height() + 192

            painter.setPen(QtGui.QPen(GridColor, 2, Qt.PenStyle.DashLine))

            x = startx
            y1 = rect.top()
            y2 = rect.bottom()
            while x <= endx:
                drawLine(QtCore.QLineF(x, starty, x, endy))
                x += 192

            y = starty
            x1 = rect.left()
            x2 = rect.right()
            while y <= endy:
                drawLine(QtCore.QLineF(startx, y, endx, y))
                y += 192
        elif self.grid == 2:
            L = 0.2
            D = 0.1  # Change these values to change the checkerboard opacity

            Light = QtGui.QColor(GridColor)
            Dark = QtGui.QColor(GridColor)
            Light.setAlpha(int(Light.alpha() * L))
            Dark.setAlpha(int(Dark.alpha() * D))

            size = 24

            board = QtGui.QPixmap(8 * size, 8 * size)
            board.fill(QtGui.QColor(0, 0, 0, 0))
            p = QtGui.QPainter(board)
            p.setPen(QtCore.Qt.PenStyle.NoPen)

            p.setBrush(QtGui.QBrush(Light))
            for x, y in ((0, size), (size, 0)):
                p.drawRect(x + (4 * size), y, size, size)
                p.drawRect(x + (4 * size), y + (2 * size), size, size)
                p.drawRect(x + (6 * size), y, size, size)
                p.drawRect(x + (6 * size), y + (2 * size), size, size)

                p.drawRect(x, y + (4 * size), size, size)
                p.drawRect(x, y + (6 * size), size, size)
                p.drawRect(x + (2 * size), y + (4 * size), size, size)
                p.drawRect(x + (2 * size), y + (6 * size), size, size)

            p.setBrush(QtGui.QBrush(Dark))
            for x, y in ((0, 0), (size, size)):
                p.drawRect(x, y, size, size)
                p.drawRect(x, y + (2 * size), size, size)
                p.drawRect(x + (2 * size), y, size, size)
                p.drawRect(x + (2 * size), y + (2 * size), size, size)

                p.drawRect(x, y + (4 * size), size, size)
                p.drawRect(x, y + (6 * size), size, size)
                p.drawRect(x + (2 * size), y + (4 * size), size, size)
                p.drawRect(x + (2 * size), y + (6 * size), size, size)

                p.drawRect(x + (4 * size), y, size, size)
                p.drawRect(x + (4 * size), y + (2 * size), size, size)
                p.drawRect(x + (6 * size), y, size, size)
                p.drawRect(x + (6 * size), y + (2 * size), size, size)

                p.drawRect(x + (4 * size), y + (4 * size), size, size)
                p.drawRect(x + (4 * size), y + (6 * size), size, size)
                p.drawRect(x + (6 * size), y + (4 * size), size, size)
                p.drawRect(x + (6 * size), y + (6 * size), size, size)

            del p

            # Adjust the rectangle to align with the grid, so we don't have to
            # paint pixmaps on non-integer coordinates
            x, y, _, _ = rect.getRect()
            mod = board.width()
            rect.adjust(-(x % mod), -(y % mod), 0, 0)

            painter.drawTiledPixmap(rect, board)


    def drawBackground(self, painter, rect):
        #if 
        if KP.map.bgName == '/Maps/Water.brres' and settings.config["Window"]["water_lava_view"] == "True":
            painter.fillRect(rect, QtGui.QColor(11, 180, 249))
        elif KP.map.bgName == '/Maps/Lava.brres' and settings.config["Window"]["water_lava_view"] == "True":
            painter.fillRect(rect, QtGui.QColor(255, 63, 0))
        else:
            painter.fillRect(rect, QtGui.QColor(119, 136, 153))


        areaLeft, areaTop = rect.x(), rect.y()
        areaWidth, areaHeight = rect.width(), rect.height()
        areaRight, areaBottom = areaLeft+areaWidth, areaTop+areaHeight

        areaLeftT = floor(areaLeft / 24)
        areaTopT = floor(areaTop / 24)
        areaRightT = ceil(areaRight / 24)
        areaBottomT = ceil(areaBottom / 24)

        # compile a list of doodads
        visibleDoodadsByLayer = {}

        for obj in self.items(rect):
            if not isinstance(obj, KPEditorDoodad): continue

            layer = obj._layerRef()

            try:
                doodadList = visibleDoodadsByLayer[layer]
            except KeyError:
                doodadList = []
                visibleDoodadsByLayer[layer] = doodadList

            doodadList.append(obj)

        # now draw everything!
        for layer in reversed(KP.map.layers):
            if not layer.visible: continue

            if isinstance(layer, KPDoodadLayer):
                try:
                    toDraw = visibleDoodadsByLayer[layer]
                except KeyError:
                    continue

                for item in reversed(toDraw):

                    painter.save()

                    if self.playing == False:
                        painter.setWorldTransform(item.sceneTransform(), True)
                        painter.drawPixmap(item._boundingRect, item.pixmap, QtCore.QRectF(item.pixmap.rect()))

                    else:
                        self.animateDoodad(painter, item)
                    painter.restore()


            elif isinstance(layer, KPTileLayer):
                left, top = layer.cacheBasePos
                width, height = layer.cacheSize
                right, bottom = left+width, top+height

                if width == 0 and height == 0: continue

                if right < areaLeftT: continue
                if left > areaRightT: continue

                if bottom < areaTopT: continue
                if top > areaBottomT: continue

                # decide how much of the layer we'll actually draw
                drawLeft = int(max(areaLeftT, left))
                drawRight = int(min(areaRightT, right))

                drawTop = int(max(areaTopT, top))
                drawBottom = int(min(areaBottomT, bottom))

                srcY = drawTop - top
                destY = drawTop * 24

                baseSrcX = drawLeft - left
                baseDestX = drawLeft * 24

                rows = layer.cache
                tileset = KP.tileset(layer.tileset)
                tileList = tileset.tiles

                for y in range(drawTop, drawBottom):
                    srcX = baseSrcX
                    destX = baseDestX
                    row = rows[srcY]

                    for x in range(drawLeft, drawRight):
                        tile = row[srcX]
                        if tile != -1:
                            painter.drawPixmap(destX, destY, tileList[tile])

                        srcX += 1
                        destX += 24

                    srcY += 1
                    destY += 24


            elif isinstance(layer, KPPathLayer):
                for pnLayer in reversed(KP.mainWindow.pathNodeList.getLayers()):
                    if not pnLayer.visible: continue

                    # Render Tiles
                    left, top = pnLayer.cacheBasePos
                    width, height = pnLayer.cacheSize
                    right, bottom = left+width, top+height

                    if not (width == 0) or (height == 0) or (right < areaLeftT) or (left > areaRightT) or (bottom < areaTopT) or (top > areaBottomT):

                        drawLeft = int(max(areaLeftT, left))
                        drawRight = int(min(areaRightT, right))

                        drawTop = int(max(areaTopT, top))
                        drawBottom = int(min(areaBottomT, bottom))

                        srcY = drawTop - top
                        destY = drawTop * 24

                        baseSrcX = drawLeft - left
                        baseDestX = drawLeft * 24

                        rows = pnLayer.cache
                        tileset = KP.tileset(pnLayer.tileset)
                        tileList = tileset.tiles

                        for y in range(drawTop, drawBottom):
                            srcX = baseSrcX
                            destX = baseDestX
                            row = rows[srcY]

                            for x in range(drawLeft, drawRight):
                                tile = row[srcX]
                                if tile != -1:
                                    painter.drawPixmap(destX, destY, tileList[tile])

                                srcX += 1
                                destX += 24

                            srcY += 1
                            destY += 24

                    # Render Doodads
                    try:
                        toDraw = visibleDoodadsByLayer[pnLayer]
                    except KeyError:
                        continue

                    for item in reversed(toDraw):

                        painter.save()

                        if self.playing == False:
                            painter.setWorldTransform(item.sceneTransform(), True)
                            painter.drawPixmap(item._boundingRect, item.pixmap, QtCore.QRectF(item.pixmap.rect()))

                        else:
                            self.animateDoodad(painter, item)
                        painter.restore()


    def animateDoodad(self, painter, item):

        doodad = item._doodadRef()
        animations = doodad.animations

        transform = item.sceneTransform()
        posRect = QtCore.QRectF(item._boundingRect)

        # Anm indexes are Looping, Interpolation, Frame Len, Type, Start Value, End Value
        #
        # Anm Loops are Contiguous, Loop, Reversible Loop
        # Anm Interpolations are Linear, Sinusoidial, Cosinoidial
        # Anm Types are X Position, Y Position, Angle, X Scale, Y Scale, Opacity

        if len(animations) > 0:
            for anm, Timeline in zip(animations, doodad.timelines):

                Type = anm[3]

                modifier = Timeline.currentFrame()

                if Type == "X Position":
                    posRect.adjust(modifier, 0, modifier, 0)

                elif Type == "Y Position":
                    posRect.adjust(0, modifier, 0, modifier)

                elif Type == "Angle":
                    transform.rotate(modifier)

                elif Type == "X Scale":
                    posRect.setWidth(posRect.width()*modifier/100.0)

                elif Type == "Y Scale":
                    h = posRect.height()
                    posRect.setHeight(h*modifier/100.0)

                    new = h - posRect.height()
                    posRect.adjust(0, new, 0, new)

                elif Type == "Opacity":
                    painter.setOpacity(modifier/100.0)

        painter.setWorldTransform(transform, True)
        painter.drawPixmap(posRect, item.pixmap, QtCore.QRectF(item.pixmap.rect()))


    def setCurrentLayer(self, layer):
        if self.currentLayer is not None:
            self.currentLayer.setActivated(False)

        self.currentLayer = layer
        self.currentLayer.setActivated(True)


class KPEditorWidget(QtWidgets.QGraphicsView):
    def __init__(self, scene, parent=None):
        QtWidgets.QGraphicsView.__init__(self, scene, parent)

        self.setRenderHints(AntiAliasing)
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.grid = 0

        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
        self.setDragMode(QtWidgets.QGraphicsView.DragMode.RubberBandDrag)

        self.xScrollBar = QtWidgets.QScrollBar(QtCore.Qt.Orientation.Horizontal, parent)
        self.setHorizontalScrollBar(self.xScrollBar)

        self.yScrollBar = QtWidgets.QScrollBar(QtCore.Qt.Orientation.Vertical, parent)
        self.setVerticalScrollBar(self.yScrollBar)

        self.assignNewScene(scene)

    def drawForeground(self, painter, rect):

        QtWidgets.QGraphicsView.drawForeground(self, painter, rect)

        if self.grid:
            painter.setPen(Qt.GlobalColor.red)
            painter.setBrush(Qt.GlobalColor.transparent)

            c = rect.center()
            x = c.x()
            y = c.y()

            mx = 880.0
            my = 660.0

            m2x = 1180.0
            m2y = 660.0

            # mx = 1792.0
            # my = 1344.0
            newRect = QtCore.QRectF(x-(mx/2.0), y-(my/2.0), mx, my)
            painter.drawRect(newRect)

            newRect2 = QtCore.QRectF(x-(m2x/2.0), y-(m2y/2.0), m2x, m2y)
            painter.drawRect(newRect2)

            painter.drawLine(QtCore.QLineF(x, y-36, x, y+36))
            painter.drawLine(QtCore.QLineF(x-36, y, x+36, y))

            newRect3 = QtCore.QRectF(x-24, y-24, 48, 48)
            painter.drawRect(newRect3)


    def assignNewScene(self, scene):
        self.setScene(scene)
        self.centerOn(0,0)

        # set up stuff for painting
        self.objectToPaint = None
        self.objectIDToPaint = None
        self.doodadToPaint = None
        self.typeToPaint = None

        self._resetPaintVars()

    def _resetPaintVars(self):
        self.painting = None
        self.paintingItem = None
        self.paintBeginPosition = None

    def _tryToPaint(self, event):
        '''Called when a paint attempt is initiated'''

        layer = self.scene().currentLayer
        if not layer or not layer.visible: return

        if isinstance(layer, KPTileLayer):
            paint = self.objectToPaint
            if paint is None: return

            pos = event.position()
            clicked = self.mapToScene(int(pos.x()), int(pos.y()))
            x, y = clicked.x(), clicked.y()
            if x < 0: x = 0
            if y < 0: y = 0

            x = int(x / 24)
            y = int(y / 24)

            obj = KPObject()
            obj.position = (x,y)
            obj.size = (1,1)
            obj.tileset = layer.tileset
            obj.kind = self.objectIDToPaint
            obj.kindObj = paint
            obj.updateCache()
            layer.objects.append(obj)
            layer.updateCache()

            item = KPEditorObject(obj, layer)
            item.setAcceptHoverEvents(True)
            self.scene().addItem(item)

            self.painting = obj
            self.paintingItem = item
            self.paintBeginPosition = (x, y)

        elif isinstance(layer, KPDoodadLayer):
            paint = self.doodadToPaint
            if paint is None: return

            pos = event.position()
            clicked = self.mapToScene(int(pos.x()), int(pos.y()))
            x, y = clicked.x(), clicked.y()
            if x < 0: x = 0
            if y < 0: y = 0

            obj = KPDoodad()
            obj.position = [x,y]
            obj.source = paint
            obj.setDefaultSize()
            layer.objects.append(obj)

            item = KPEditorDoodad(obj, layer)
            item.setAcceptHoverEvents(True)
            self.scene().addItem(item)

            self.painting = obj
            self.paintingItem = item
            self.paintBeginPosition = (x, y)

        elif isinstance(layer, KPPathLayer):
            # decide what's under the mouse
            pos = event.position()
            clicked = self.mapToScene(int(pos.x()), int(pos.y()))
            x, y = clicked.x(), clicked.y()
            itemsUnder = self.scene().items(clicked)

            if event.modifiers() & Qt.KeyboardModifier.AltModifier:
                dialog = True
            else:
                dialog = False

            for item in itemsUnder:
                if isinstance(item, KPEditorNode):
                    # Paint a path to this node (if one is selected)
                    sourceItem, sourceNode = None, None
                    selected = self.scene().selectedItems()

                    for selItem in selected:
                        if isinstance(item, KPEditorNode) and selItem != item:
                            sourceItem = selItem
                            sourceNode = selItem._nodeRef()
                            break

                    if sourceItem is None: return

                    # Make sure that no path already exists between these nodes
                    destNode = item._nodeRef()

                    for pathToCheck in sourceNode.exits:
                        if pathToCheck._startNodeRef() == destNode:
                            return
                        if pathToCheck._endNodeRef() == destNode:
                            return

                    # No node can have more than four paths, because there are only
                    # four directions registered by a Wiimote DPad.

                    if len(sourceNode.exits) > 3:
                        return

                    if len(destNode.exits) > 3:
                        return

                    path = KPPath(sourceNode, destNode)
                    if not KP.mainWindow.pathNodeList.addLayer(path, dialog):
                        return

                    KP.map.pathLayer.paths.append(path)

                    item = KPEditorPath(path)
                    self.scene().addItem(item)

                    return

                elif isinstance(item, KPEditorPath):
                    # Split this path into two... at this point

                    origPath = item._pathRef()

                    node = KPNode()
                    node.position = (x - 12, y - 12)

                    if not KP.mainWindow.pathNodeList.addLayer(node, dialog):
                        return

                    KP.map.pathLayer.nodes.append(node)

                    # Start node => Original path => New node => New path => End node

                    endNode = origPath._endNodeRef()

                    origPath.setEnd(node)

                    nodeItem = KPEditorNode(node)
                    self.scene().addItem(nodeItem)

                    # TODO: fix this ugly bit of code
                    item._endNodeRef = weakref.ref(nodeItem)
                    item.updatePosition()

                    self.painting = node
                    self.paintingItem = item
                    self.paintBeginPosition = (x - 12, y - 12)

                    newPath = KPPath(node, endNode, origPath)
                    if not KP.mainWindow.pathNodeList.addLayer(newPath, dialog):
                        return
                    KP.map.pathLayer.paths.append(newPath)

                    pathItem = KPEditorPath(newPath)
                    self.scene().addItem(pathItem)

                    return

            # Paint a new node
            node = KPNode()
            node.position = (x - 12, y - 12)
            if not KP.mainWindow.pathNodeList.addLayer(node, dialog):
                return
            KP.map.pathLayer.nodes.append(node)

            item = KPEditorNode(node)
            self.scene().addItem(item)

            # Paint a path to this node (if one is selected)
            sourceItem, sourceNode = None, None
            selected = self.scene().selectedItems()

            for selItem in selected:
                if isinstance(selItem, KPEditorNode) and selItem != item:
                    sourceItem = selItem
                    sourceNode = selItem._nodeRef()
                    break

            # No node can have more than four paths, because there are only
            # four directions registered by a Wiimote DPad.

            if not sourceItem is None:
                if len(sourceNode.exits) > 3:
                    return

                # There, now you can draw paths easily in a row.
                path = KPPath(sourceNode, node)

                if not KP.mainWindow.pathNodeList.addLayer(path, dialog):
                    return

                KP.map.pathLayer.paths.append(path)

                pathItem = KPEditorPath(path)
                self.scene().addItem(pathItem)


            # Switch the selection to the recently drawn node, so you can keep on rolling.
            self.scene().clearSelection()
            item.setSelected(True)

            self.painting = node
            self.paintingItem = item
            self.paintBeginPosition = (x - 12, y - 12)

        elif isinstance(layer, KPPathTileLayer):
            if self.typeToPaint == 'object':
                paint = self.objectToPaint
                if paint is None: return

                pos = event.position()
                clicked = self.mapToScene(int(pos.x()), int(pos.y()))
                x, y = clicked.x(), clicked.y()
                if x < 0: x = 0
                if y < 0: y = 0

                x = int(x / 24)
                y = int(y / 24)

                obj = KPObject()
                obj.position = (x,y)
                obj.size = (1,1)
                obj.tileset = layer.tileset
                obj.kind = self.objectIDToPaint
                obj.kindObj = paint
                obj.updateCache()
                layer.objects.append(obj)
                layer.updateCache()

                item = KPEditorObject(obj, layer)
                self.scene().addItem(item)

                self.painting = obj
                self.paintingItem = item
                self.paintBeginPosition = (x, y)

            elif self.typeToPaint == 'doodad':

                paint = self.doodadToPaint
                if paint is None: return

                pos = event.position()
                clicked = self.mapToScene(int(pos.x()), int(pos.y()))
                x, y = clicked.x(), clicked.y()
                if x < 0: x = 0
                if y < 0: y = 0

                obj = KPDoodad()
                obj.position = [x,y]
                obj.source = paint
                obj.setDefaultSize()
                layer.doodads.append(obj)

                item = KPEditorDoodad(obj, layer)
                self.scene().addItem(item)

                self.painting = obj
                self.paintingItem = item
                self.paintBeginPosition = (x, y)


    def _movedWhilePainting(self, event):
        '''Called when the mouse is moved while painting something'''

        obj = self.painting
        item = self.paintingItem

        if isinstance(obj, KPObject):
            pos = event.position()
            clicked = self.mapToScene(int(pos.x()), int(pos.y()))
            x, y = clicked.x(), clicked.y()
            if x < 0: x = 0
            if y < 0: y = 0

            x = int(x / 24)
            y = int(y / 24)

            beginX, beginY = self.paintBeginPosition

            if x >= beginX:
                objX = beginX
                width = x - beginX + 1
            else:
                objX = x
                width = beginX - x + 1

            if y >= beginY:
                objY = beginY
                height = y - beginY + 1
            else:
                objY = y
                height = beginY - y + 1

            currentX, currentY = obj.position
            currentWidth, currentHeight = obj.size

            # update everything if changed
            changed = False

            if currentX != objX or currentY != objY:
                obj.position = (objX, objY)
                item._updatePosition()
                changed = True

            if currentWidth != width or currentHeight != height:
                obj.size = (width, height)
                obj.updateCache()
                item._updateSize()
                changed = True

            if not changed: return

            item._layerRef().updateCache()


    def mousePressEvent(self, event):

        if event.button() == QtCore.Qt.MouseButton.RightButton:
            self._tryToPaint(event)
            event.accept()

        elif event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if isinstance(self.scene().currentLayer, KPPathLayer):
                QtWidgets.QGraphicsView.mousePressEvent(self, event)
                return

            itemsUnder = self.scene().items(self.mapToScene(event.pos()), Qt.IntersectsItemShape, Qt.AscendingOrder)

            if itemsUnder:

                self.scene().clearSelection()

                kLayer = itemsUnder[0]._layerRef()
                if isinstance(kLayer, (KPPathTileLayer, KPPathLayer)):
                    QtWidgets.QGraphicsView.mousePressEvent(self, event)
                    return

                KP.mainWindow.handleSelectedLayerChanged(kLayer)
                index = KP.map.refLayer(kLayer)
                KP.mainWindow.layerList.selectLayer(index)

                itemsUnder[0].setSelected(True)

        else:
            QtWidgets.QGraphicsView.mousePressEvent(self, event)


    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.MouseButton.RightButton and self.painting:
            self._movedWhilePainting(event)
            event.accept()

        else:
            QtWidgets.QGraphicsView.mouseMoveEvent(self, event)


    def mouseReleaseEvent(self, event):
        QtWidgets.QGraphicsView.mouseReleaseEvent(self, event)
    #   try:
    #       self.scene().mouseGrabberItem().ungrabMouse()
    #   except:
    #       pass
        self.userClick.emit()


    def keyPressEvent(self, event):
        if event.key() == Key.Key_Delete or event.key() == Key.Key_Backspace:
            scene = self.scene()

            selection = scene.selectedItems()
            if len(selection) > 0:
                for obj in selection:
                    obj.setSelected(False)
                    obj.remove(True)
                scene.update()
                self.userClick.emit()
                self.update()
                return

        else:
            QtWidgets.QGraphicsView.keyPressEvent(self, event)

    userClick = QtCore.pyqtSignal()



