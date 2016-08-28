#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
from PyQt4 import QtGui,QtCore,Qt
from PyQt4.QtDeclarative import QDeclarativeView

from mutagen.mp3 import MP3     # mutagen v1.30: https://bitbucket.org/lazka/mutagen/downloads
import sip, sys, random, ConfigParser, images, re, chardet, locale, codecs

from PyQt4.phonon import Phonon
from controlBar import *

defaultcode = 'utf-8'


#from PyQt4.phonon import Phonon
'''  
    Esl player 
    gui refer to (Xiami For Linux Project)  
'''
class MainWindow(QtGui.QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__()
        # mp3播放器
        self.mediaObject = Phonon.MediaObject(self)   #实例化一个媒体对象
        self.mediaObject.setTickInterval(10) # set this value If you want to signal tick(qint64) Event
        self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)   #实例化音频输出
        Phonon.createPath(self.mediaObject, self.audioOutput)   #将上面的媒体对象作为音频来源并对接到音频输出
        #self.mediaObject.stateChanged.connect(self.handleStateChanged)  #播放状态改变触发事件
        #self.clicked.connect(self.handleButton) #单击按钮事件

        self.setWindowIcon(QtGui.QIcon('default_user.ico'))
        self.setWindowTitle(u'Xiami For Linux')
        # 自适应窗口宽度
        # self.cellWidget.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.content_splitter = QtGui.QSplitter()
        # self.content_splitter.setSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        self.content_splitter.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        self.content_splitter.setOrientation(QtCore.Qt.Horizontal)
        self.content_splitter.setHandleWidth(1)
        self.content_splitter.setStyleSheet("QSplitter.handle{background:lightgray}")

        self.titlebar = titleBar(master=self)
        self.titlebar.resize(700, 52)
        self.titlebar.setMinimumSize(700,52)
        self.titlebar.setMaximumHeight(52)
        self.titlebar.title_label.setText(u" "*20+u'ESL Player')

        self.ControlBar = controlBar(master=self)
        self.ControlBar.resize(700, 60)
        self.ControlBar.setMinimumSize(700,60)
        self.ControlBar.setMaximumHeight(60)

        # 容纳主部件的widget
        self.contentWidget = QtGui.QMainWindow()
        self.contentWidget.setContentsMargins(0,0,0,0)

        # 旧 content_splitter 替代品
        self.content_layout = QtGui.QHBoxLayout()
        self.content_layout.setSpacing(0)

        # 主部件添加位置
        self.content_layout.addWidget(self.contentWidget)
        # 旧 content_splitter 替代品
        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.addWidget(self.titlebar)
        self.main_layout.addLayout(self.content_layout)
        self.main_layout.addWidget(self.ControlBar)     
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(10,7,10,7)

        # 窗口属性
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        self.LeftButtonPreesed = 0

        self.widget = MyQWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(self.main_layout)
        # self.widget.setFixedSize(700,650)
        self.widget.setObjectName('main')
        self.setObjectName('main')

        # 功能性功能开始
        self.titlebar.min_button.clicked.connect(self.hideIt)
        self.titlebar.max_button.clicked.connect(self.MaxAndNormal)
        self.titlebar.close_button.clicked.connect(self.closeIt)
        
        # 无焦点触发mouseMoveEvent
        self.setMouseTracking(True)
        self.widget.setMouseTracking(True)

        self.desktop = QtGui.QApplication.desktop()
        self.animationEndFlag = 1

        # 双屏居中
        self.resize(700,650)
        self.center(1)      

         # 打开文件
        self.openFile(u'167.mp3')       





    def changeCentralWidget(self):
        self.contentWidget.setCentralWidget(self.beCentralWidget)   

    # open media file ,    
    def openFile(self,fileName):       
        self.audioFile = AudioFile(fileName)
        self.ControlBar.songTimeLabel.setText('00:00')
        self.ControlBar.songTotalTimeLabel.setText(self.audioFile.time)

        path =   self.audioFile.filePath
        if path:
            self.mediaObject.setCurrentSource(Phonon.MediaSource(path))  #把这个文件放到当前的播放队列的第一个位置（这个位置不是我们看到的列表里面的位置，而是播放位置）
            # self.master.mediaObject.play()  #开始播放
        self.ControlBar.initSlider()
        



    '''
        window handle (min,max, close)
    '''    
    def closeIt(self):
        self.animation = QtCore.QPropertyAnimation(self,"windowOpacity")
        self.animation.finished.connect(QtCore.QCoreApplication.instance().quit)
        self.animation.setDuration(300)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

    def hideIt(self):
        self.animation = QtCore.QPropertyAnimation(self,"windowOpacity")
        self.animation.finished.connect(self.showMinimized2)
        self.animation.setDuration(300)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

    def MaxAndNormal(self):
        '''最大化与正常大小间切换函数'''
        if self.showNormal3():
            self.showFullScreen3()


    '''
       move the windows with mouse 
       need with mousePressEvent, mouseReleaseEvent,leaveEvent
    ''' 
    def mouseMoveEvent(self,event):
        if event.buttons() == QtCore.Qt.LeftButton:            
            # print event.globalPos(),self.dragPosition,self.pos().x()+self.size().width(),self.pos().y()+self.size().height()
            # print self.dragPosition.x(),self.dragPosition.y()
            if self.dragPosition.x() < 12:
                if self.dragPosition.y() < 12:
                    # print "左上"
                    x = event.globalPos().x()-self.globalPositon.x()
                    y = event.globalPos().y()-self.globalPositon.y()  
                    self.setGeometry(self.oldGeometry.x()+x,self.oldGeometry.y()+y,self.oldGeometry.width()-x,self.oldGeometry.height()-y)                                                         
                elif self.oldSize.height() - self.dragPosition.y() < 12:
                    x = event.globalPos().x()-self.globalPositon.x()
                    y = event.globalPos().y()-self.globalPositon.y()
                    self.setGeometry(self.oldGeometry.x(),self.oldGeometry.y(),self.oldGeometry.width(),self.oldGeometry.height()+y)                     
                    self.setGeometry(self.oldGeometry.x()+x,self.oldGeometry.y(),self.oldGeometry.width()-x,self.oldGeometry.height()+y)                     
                    # print "左下"
                else:
                    num = event.globalPos().x()-self.globalPositon.x()
                    self.setGeometry(self.oldGeometry.x()+num,self.oldGeometry.y(),self.oldGeometry.width()-num,self.oldGeometry.height())                    
                    # print "左"
            elif self.oldSize.width() - self.dragPosition.x() < 12:
                if self.dragPosition.y() < 12:
                    x = event.globalPos().x()-self.globalPositon.x()
                    y = event.globalPos().y()-self.globalPositon.y()
                    self.setGeometry(self.oldGeometry.x(),self.oldGeometry.y()+y,self.oldGeometry.width()+x,self.oldGeometry.height()-y)
                    # print "右上"
                elif self.oldSize.height() - self.dragPosition.y() < 12:
                    x = event.globalPos().x()-self.globalPositon.x()
                    y = event.globalPos().y()-self.globalPositon.y()
                    self.setGeometry(self.oldGeometry.x(),self.oldGeometry.y(),self.oldGeometry.width()+x,self.oldGeometry.height()+y)
                    # print "右下"
                else:
                    num = event.globalPos().x()-self.globalPositon.x()
                    self.setGeometry(self.oldGeometry.x(),self.oldGeometry.y(),self.oldGeometry.width()+num,self.oldGeometry.height())
                    # print "右"
            else:
                if self.dragPosition.y() < 12:
                    num = event.globalPos().y()-self.globalPositon.y()
                    self.setGeometry(self.oldGeometry.x(),self.oldGeometry.y()+num,self.oldGeometry.width(),self.oldGeometry.height()-num)                      
                    # print "上"
                elif self.oldSize.height() - self.dragPosition.y() < 12:
                    num = event.globalPos().y()-self.globalPositon.y()
                    self.setGeometry(self.oldGeometry.x(),self.oldGeometry.y(),self.oldGeometry.width(),self.oldGeometry.height()+num)           
                    # print "下"          
                else:
                    # print "中"
                    self.move(event.globalPos() - self.dragPosition)                
            # event.accept()

        self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
        self.oldSize = self.size()
        if self.dragPosition.x() < 12:
            if self.dragPosition.y() < 12:
                self.setCursor(QtCore.Qt.SizeFDiagCursor)                                                      
            elif self.oldSize.height() - self.dragPosition.y() < 12:
                self.setCursor(QtCore.Qt.SizeBDiagCursor)
            else:
                self.setCursor(QtCore.Qt.SizeHorCursor)
        elif self.oldSize.width() - self.dragPosition.x() < 12:
            if self.dragPosition.y() < 12:
                self.setCursor(QtCore.Qt.SizeBDiagCursor)
            elif self.oldSize.height() - self.dragPosition.y() < 12:
                self.setCursor(QtCore.Qt.SizeFDiagCursor)       
            else:
                self.setCursor(QtCore.Qt.SizeHorCursor)
        else:
            if self.dragPosition.y() < 12:                     
                self.setCursor(QtCore.Qt.SizeVerCursor)
            elif self.oldSize.height() - self.dragPosition.y() < 12:          
                self.setCursor(QtCore.Qt.SizeVerCursor)
            else:
                self.setCursor(QtCore.Qt.ArrowCursor)

        if self.isFullScreen():
            #                           left top right bottom
            self.main_layout.setContentsMargins(10,7,10,7)
            self.animation = QtCore.QPropertyAnimation(self,"geometry")
            self.animation.setDuration(160)
            self.animation.setEndValue(self.normalGeometry2)
            self.animation.setStartValue(self.desktop.availableGeometry(self.desktop.screenNumber(self.widget)))
            self.animation.finished.connect(self.showNormal2)
            self.animationEndFlag = 0
            self.animation.start()
            # event.accept()
        else:
            # 缩放动画停止前不允许窗口拖动
            if self.animationEndFlag:
                self.normalGeometry2 = self.geometry()
                if event.buttons() == QtCore.Qt.LeftButton:
                    if self.LeftButtonPreesed:
                        self.move(event.globalPos() - self.dragPosition)

        event.ignore()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            # QtGui.QApplication.postEvent(self, QtCore.QEvent(174))
            self.globalPositon = event.globalPos()
            self.oldGeometry = self.geometry()
            self.oldSize = self.size()
            self.LeftButtonPreesed = 1
            # event.accept()
        if event.button() == QtCore.Qt.MidButton:
            self.hideIt()
            # event.accept()

    def mouseReleaseEvent(self,event):
        self.LeftButtonPreesed = 0

    def leaveEvent(self,event):
        self.setCursor(QtCore.Qt.ArrowCursor)

    # F11全屏切换
    def keyPressEvent(self,event):        
        if event.key()==QtCore.Qt.Key_F11:
            self.MaxAndNormal()    



    def showNormal2(self):
        self.showNormal()
        self.animationEndFlag = 1 # 动画停止

    def showNormal3(self):
        if self.isFullScreen():
            self.main_layout.setContentsMargins(10,7,10,7)
            self.animation = QtCore.QPropertyAnimation(self,"geometry")
            self.animation.setDuration(180)
            self.animation.setEndValue(self.normalGeometry2)
            self.animation.setStartValue(self.desktop.availableGeometry(self.desktop.screenNumber(self.widget)))
            self.animation.finished.connect(self.showNormal2)
            self.animationEndFlag = 0
            self.animation.start()
            return 0
        return 1

    def showFullScreen2(self):
        self.animationEndFlag = 1 # 动画停止
        self.showFullScreen()

    def showFullScreen3(self):
        if not self.isFullScreen():
            self.main_layout.setContentsMargins(0,0,0,0)
            self.animation = QtCore.QPropertyAnimation(self,"geometry")
            self.animation.setDuration(180)
            self.animation.setStartValue(self.geometry())
            self.animation.setEndValue(self.desktop.availableGeometry(self.desktop.screenNumber(self.widget)))
            self.animation.finished.connect(self.showFullScreen2)
            self.animationEndFlag = 0
            self.animation.start()

    def showMinimized2(self):
        self.setWindowOpacity(1)
        self.showMinimized()

    # 居中 - 多屏居中支持
    def center(self,screenNum=0):
        
        screen = self.desktop.availableGeometry(screenNum)
        size = self.geometry()
        self.normalGeometry2 = QtCore.QRect((screen.width()-size.width())/2+screen.left(),
                         (screen.height()-size.height())/2,
                         size.width(),size.height())
        self.setGeometry((screen.width()-size.width())/2+screen.left(),
                         (screen.height()-size.height())/2,
                         size.width(),size.height())

    # ??
    def paintEvent(self,event):
        # 窗口阴影
        # print 'paintEvent...'
        p = QtGui.QPainter(self)
        p.drawPixmap(0, 0, self.rect().width(), self.rect().height(), QtGui.QPixmap('img/mainwindow/main_shadow2.png'))

    # ??
    def showEvent(self,event):
        print 'showEvent...'
        self.animation = QtCore.QPropertyAnimation(self,"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()   


class MyQWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MyQWidget, self).__init__()
        self.setMouseTracking(True)

    def mouseMoveEvent(self,event): 
        event.ignore()


class titleBar(QtGui.QMainWindow):
    def __init__(self,master,parent=None):
        super(titleBar,self).__init__()
        self.master = master
        # self.setMouseTracking(True)

        self.title_label = QtGui.QLabel()
        self.title_label.setStyleSheet("color:black")
        self.title_label.setText(u"虾米音乐")
        self.title_label.setText(u"Xiami For Linux Project")

        self.font = QtGui.QFont()
        self.font.setPixelSize(20)   # 设置字号32,以像素为单位
        self.font.setFamily("SimSun")# 设置字体，宋体
        self.font.setFamily(u"微软雅黑")
        # self.font.setWeight(20)     # 设置字型,不加粗
        self.font.setBold(True)
        self.font.setItalic(False)   # 设置字型,不倾斜
        self.font.setUnderline(False)# 设置字型,无下划线

        self.title_label.setFont(self.font)

        self.close_button = QtGui.QPushButton()
        self.min_button   = QtGui.QPushButton()
        self.max_button   = QtGui.QPushButton()

        self.close_button.setIcon(QtGui.QIcon("img/orange.png"))
        self.min_button.setIcon(QtGui.QIcon("img/green.png"))
        self.max_button.setIcon(QtGui.QIcon("img/blue.png"))        

        self.close_button.setFixedSize(15,15)
        self.min_button.setFixedSize(15,15)
        self.max_button.setFixedSize(15,15)

        self.close_button.setStyleSheet(""" 
                                    background:transparent;
                                    """)
        self.min_button.setStyleSheet(""" 
                                    background:transparent;
                                    """)
        self.max_button.setStyleSheet(""" 
                                    background:transparent;
                                    """)
        self.title_label.setStyleSheet(""" 
                                    background:transparent;
                                    color:rgba(70,70,70,255);
                                    """)


        '''
        border-radius可以同时设置1到4个值。
        如果设置1个值，表示4个圆角都使用这个值。
        如果设置两个值，表示左上角和右下角使用第一个值，右上角和左下角使用第二个值。
        如果设置三个值，表示左上角使用第一个值，右上角和左下角使用第二个值，右下角使用第三个值。
        如果设置四个值，则依次对应左上角、右上角、右下角、左下角（顺时针顺序）。adadad
        '''
        # stop:0 rgba(125, 175, 175, 255));
        self.setStyleSheet('''
            .QMainWindow
            {
                background:transparent;
                border-bottom:10px;
            }
            .QWidget
            {
                border-top-left-radius:     7px;
                border-top-right-radius:    7px;
                border-bottom-right-radius: 0px;
                border-bottom-left-radius:  0px;
                border-style: solid;

                background:url('img/XMPlayerWindowTitleBarBackground.png');
                /*
                background: qlineargradient(spread:reflect,
                x1:1, y1:1, x2:1, y1:1,
                stop:1 rgba(224,224,224,255),
                stop:0 rgba(175,175,175,255));
                */

                border-top:     1px solid #919191;
                border-left:    1px solid #919191;
                border-right:   1px solid #919191;
                border-bottom:  0px solid rgb(104,104,104);
            }            
                    ''')

        # 水平管理器
        self.title_layout = QtGui.QHBoxLayout()
        self.title_layout.setContentsMargins(20,2,25,0)
    
        # self.title_layout.addStretch()
        # title 
        self.title_layout.addWidget(self.title_label,1,QtCore.Qt.AlignLeft)
        self.title_layout.addWidget(self.min_button  ,0,QtCore.Qt.AlignVCenter)
        self.title_layout.addWidget(self.max_button  ,0,QtCore.Qt.AlignVCenter)
        self.title_layout.addWidget(self.close_button,0,QtCore.Qt.AlignVCenter)
   
        self.widget = QtGui.QWidget()
        self.widget.setMouseTracking(True)
        self.setCentralWidget(self.widget)
        self.widget.setLayout(self.title_layout)


    def mouseMoveEvent(self,event):
        self.setCursor(QtCore.Qt.ArrowCursor)
        event.ignore()

    def enterEvent(self,event):
        self.setCursor(QtCore.Qt.ArrowCursor)
        event.ignore()

    def wheelEvent(self,event):
        if self.master.animationEndFlag and event.delta()>0:
            self.master.showFullScreen3()
        if self.master.animationEndFlag and event.delta()<0:
            self.master.showNormal3()

    def mouseDoubleClickEvent(self,event):
        '''双击标题栏'''
        self.master.MaxAndNormal()

# media file 
class AudioFile(object):
    def __init__(self, fileName):
        #fileName = u'D:/pythonWorkspace/XiamiForLinuxProject-master/test.mp3'
        self.fileName = fileName
        self.filePath = 'd:/'+fileName	 #'./'+fileName 
        self.time = '00:00'
        self.totalTime = 0
        self.audioInfo(self.filePath)

    def audioInfo(self, filePath):
       
        suffix = 'mp3' #self.suffix()
        if suffix == 'mp3':
            audio = MP3(filePath)
            if audio.info.length:
                time = QTime().addSecs(audio.info.length).toString("mm:ss")  
            self.time = time
            #print self.time
            self.totalTime = audio.info.length*1000
    # 暂时没用    
    def suffix(self):
        return self.file.suffix().toLower()         



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    testWidget = MainWindow()
    testWidget.show()
    sys.exit(app.exec_())
