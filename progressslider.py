# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import images
try:
	_fromUtf8 = QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

		
class progressSlider(QSlider):
	def __init__(self, orientation, parent=None):
		super(progressSlider, self).__init__(orientation, parent)

	def mousePressEvent(self, event):
		if self.topLevelWidget().mediaObject.state() != 2:
			return
		# harfWidth = self.width() / 2
		# posX = event.x()
		# chazhi = posX - harfWidth
		# print 'new... ', chazhi

		# chazhi = chazhi/30
		# posX = posX + chazhi
		posX = self.fixPosition( event.x(), self.width())

		new = QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), posX, self.width())
		#print ' event.x()... ', event.x()
		
		self.setValue(new)
		self.emit(SIGNAL('sliderMoved(int)'), new)

	def mouseMoveEvent(self, event):
		if self.topLevelWidget().mediaObject.state() != 2:
			return
		posX = self.fixPosition( event.x(), self.width())
		new = QStyle.sliderValueFromPosition(self.minimum(), self.maximum(),posX, self.width())
		self.setValue(new)
		self.emit(SIGNAL('sliderMoved(int)'), new)
	
	# mouse wheel 	
	def wheelEvent(self, event):
		if self.topLevelWidget().mediaObject.state() != 2:
			return
		modifier = QApplication.keyboardModifiers()
		max = self.maximum()
		min = self.minimum()
		if event.delta() >= 120:		
			new = self.value()+ max*0.03
			if new > max:
				new = max
			self.setValue(new)
			self.emit(SIGNAL('sliderMoved(int)'), new)
		elif event.delta() <= -120:			
			new = self.value()- max*0.03
			if new < min:
				new = min
			self.setValue(new)
			self.emit(SIGNAL('sliderMoved(int)'), new)
			
	def fixPosition(self,eventX,width):
		harfWidth = width / 2
		posX = eventX
		chazhi = posX - harfWidth
		# print 'new... ', chazhi

		chazhi = chazhi/15
		posX = posX + chazhi
		return posX