'''
Created on 05.06.2015

@author: jrenken
'''
from PyQt4.QtCore import QObject, pyqtSlot, QTimer, pyqtSignal
from qgis.core import QgsPoint, QgsCoordinateTransform, QgsCoordinateReferenceSystem
from position_marker import PositionMarker
# from qgis.core import 


class MobileItem(QObject):
    '''
    A Mobile Item that reveives its position from a dataprovider and is displayed on the canvas
    Could be everything liek vehicles or simple beacons
    '''

    mobileItemCount = 0

    newPosition = pyqtSignal(float, QgsPoint, float, float)
    newAttitude = pyqtSignal(float, float, float)   # heading, pitch, roll
    timeout = pyqtSignal()

    def __init__(self, iface, params={}, parent=None):
        '''
        Constructor
        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        :param params: A dictionary defining all the properties of the mobile item
        :type params: dictionary
        :param parent: Parent object for the new item. Defaults None.
        :type parent: QObject
        '''
        super(MobileItem, self).__init__(parent)

        self.iface = iface
        self.canvas = iface.mapCanvas()
        MobileItem.mobileItemCount += 1
        self.name = params.setdefault('Name', 'MobileItem_' + str(MobileItem.mobileItemCount))
        self.marker = PositionMarker(self.canvas, params)
        self.marker.setToolTip(self.name)
        self.dataProvider = params.get('provider', dict())
        self.messageFilter = dict()
        self.extData = dict()
        self.coordinates = None
        self.position = None
        self.lastFix = 0.0
        self.crsXform = QgsCoordinateTransform()
        self.crsXform.setSourceCrs(QgsCoordinateReferenceSystem(4326))
        self.onCrsChange()
        self.canvas.scaleChanged.connect(self.onScaleChange)
        self.canvas.mapRenderer().destinationSrsChanged.connect(self.onCrsChange)
        self.timer = QTimer(self);
        self.timer.timeout.connect(self.timeout)
        self.timeoutTime = int(params.get('timeout', 3000))
        self.enabled = True

    def __del__(self):
        print "Bye", self.name
        
    def removeFromCanvas(self):
        self.marker.removeFromCanvas()
#         self.marker.deleteTrack()
#         self.canvas.scene().removeItem(self.marker)
#         self.deleteLater()
    
    def properties(self):
        d = {'Name' : self.name, 
             'timeout': self.timeoutTime,
             'enabled': self.enabled,
             'provider' : self.dataProvider}
        d.update(self.marker.properties())
        return d

    def subscribePositionProvider(self, provider, filterId=None):
        provider.newDataReceived.connect(self.processNewData)
        if filterId != None:
            self.messageFilter[provider.name] = filterId
        elif provider.name in self.messageFilter.keys():
            del self.messageFilter[provider.name]

    def unsubscribePositionProvider(self, provider):
        try:
            provider.newDataReceived.disconnect(self.processData)
            del self.messageFilter[provider.name]
        except:
            pass

    @pyqtSlot(dict)
    def processNewData(self, data):
        if not self.enabled:
            return
        try:
            name = data['name']
            if name in self.messageFilter.keys():
                if data['id'] != self.messageFilter[name]:
                    return
        except:
            pass
        self.extData.update(data)
            
        if 'lat' in data and 'lon' in data:
            self.position = QgsPoint(data['lon'], data['lat'])
            self.coordinates = self.crsXform.transform(self.position)
            self.marker.newCoords(self.coordinates)
            if 'time' in data:
                self.lastFix = data['time']
            self.newPosition.emit(self.lastFix, self.position, data.get('depth', 0.0), data.get('altitude', -9999.9))
            self.timer.start(self.timeoutTime)
                
                
        if 'heading' in data:
            self.newAttitude.emit(data['heading'], data.get('pitch', 0.0), data.get('roll', 0.0))
            self.marker.newHeading(data['heading'])

    @pyqtSlot(float)
    def onScaleChange(self, scale):
        self.marker.updateSize()

    @pyqtSlot()
    def onCrsChange(self):
        crsDst = self.canvas.mapRenderer().destinationCrs()
        print 'CRS changed', crsDst.ellipsoidAcronym (), crsDst.srsid()
        self.crsXform.setDestCRS(crsDst)
        self.marker.updateSize()

    @pyqtSlot(bool)
    def setEnabled(self, enabled):
        self.enabled = enabled
        self.marker.setVisible(self.enabled)
        self.marker.resetPosition()
        if self.enabled:
            self.timer.start(self.timeoutTime)
        else:
            self.timer.stop()
            
    @pyqtSlot()
    def deleteTrack(self):
        self.marker.deleteTrack()

    @pyqtSlot()
    def centerOnMap(self):
        if self.coordinates is not None:
            self.canvas.setCenter(self.coordinates)
            self.canvas.refresh()
        
