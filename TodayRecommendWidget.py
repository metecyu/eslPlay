#!/usr/bin/python
# -*- coding:utf-8 -*-
from PyQt4 import QtGui,QtCore,Qt
from PyQt4.QtDeclarative import QDeclarativeView
from PyQt4 import QtDeclarative
import sys

class ModelObject(object):    
    def __init__(self, picName,text=None):
        self.picName = picName
        self.text = text


class TodayRecommendWidget(QtGui.QMainWindow):
    '''今日推荐主界面'''
    def __init__(self, parent=None):
        super(TodayRecommendWidget, self).__init__()

        # self.view = QDeclarativeView()
        self.view = MyQDeclarativeView()
        self.view.setMouseTracking(True)
        ctxt = self.view.rootContext()
        self.currTime = 'master'
        ctxt.setContextProperty('currTime',self.currTime)

        self.view.setSource(QtCore.QUrl.fromLocalFile("ListView.qml"))
        # self.view.setStyleSheet("""border:1px solid red""")
        self.rootObject = self.view.rootObject()
        #self.rootObject.setProperty('globalWidth',1000)
        #self.rootObject.setProperty('globalHeight',180)
        # self.rootObject.sendClicked.connect(self.onClicked)

        #self.view2 = MyQDeclarativeView()
        #self.view2.setSource(QtCore.QUrl.fromLocalFile("todayRecommendBottom.qml"))
        # self.view2.setStyleSheet("""border:1px solid red""")

        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.addWidget(self.view)
        #self.mainLayout.addWidget(self.view2)
        self.mainLayout.setSpacing(0)
        # left top right bottom
        self.mainLayout.setContentsMargins(0,0,0,0)

        # 设置部件比例
        self.mainLayout.setStretch(0,5)
        self.mainLayout.setStretch(1,3)

        self.mainWidget = QtGui.QWidget()
        self.mainWidget.setMouseTracking(True)
        self.setStyleSheet("""
            QDeclarativeView
            {
                border-top:     0px solid #adadad;
                border-left:    0px solid #919191;
                border-right:   1px solid #919191;
                border-bottom:  0px solid #919191;
            }
            """)
        self.setCentralWidget(self.mainWidget)
        self.mainWidget.setLayout(self.mainLayout)

        # print self.size().height()/4

        # 使得QML窗口随父窗口大小改变而改变
        # ............令人无语的问题，加上自调整后会上下滚动
        # 试着在 ResizeEvent 重置吧
        self.view.setResizeMode(QDeclarativeView.SizeRootObjectToView)
        #self.view2.setResizeMode(QDeclarativeView.SizeRootObjectToView)





class MyQDeclarativeView(QDeclarativeView):
    def __init__(self, parent=None):
        super(MyQDeclarativeView, self).__init__()
        self.setMouseTracking(True)

    def enterEvent(self,event):
        self.setCursor(QtCore.Qt.ArrowCursor)

    # def mouseMoveEvent(self,event): 
    #     self.setCursor(QtCore.Qt.ArrowCursor)
    #     event.accept()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    testWidget = TodayRecommendWidget()
    testWidget.resize(600,400)
    testWidget.show()
    sys.exit(app.exec_())


