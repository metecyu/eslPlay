#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
from PyQt4 import QtGui,QtCore,Qt
from PyQt4.QtDeclarative import QDeclarativeView
from mutagen.mp3 import MP3     # mutagen v1.30: https://bitbucket.org/lazka/mutagen/downloads
from PyQt4.phonon import Phonon
from progressslider import *

class controlBar(QtGui.QMainWindow):
    def __init__(self,master,parent=None):
        super(controlBar,self).__init__(parent)
        self.setAutoFillBackground(True)
        self.master = master


        self.font = QtGui.QFont()
        self.font.setPixelSize(20)   # 设置字号32,以像素为单位
        self.font.setFamily("SimSun")# 设置字体，宋体
        self.font.setFamily(u"微软雅黑")
        # self.font.setWeight(20)    # 设置字型,不加粗
        self.font.setBold(True)
        self.font.setItalic(False)   # 设置字型,不倾斜
        self.font.setUnderline(False)# 设置字型,无下划线

        self.resize(700, 60)
        # play pause button
        self.playOrPauseBtn = QtGui.QCheckBox()
        self.playOrPauseBtn.setObjectName('playOrPauseBtn')
        # add efen
        self.playOrPauseBtn.clicked.connect(self.playOrPauseChange)
        self.master.mediaObject.stateChanged.connect(self.mediaStateChanged)  #播放状态改变触发事件        


        # 进度条
        self.seekslIder = progressSlider(QtCore.Qt.Horizontal, self)
        self.seekslIder.setObjectName('seekslIder')
        self.seekslIder.setMinimumWidth(300)
        self.seekslIder.setTracking(True)
        #self.seekslIder.setSingleStep(1000)


        # 已播放时间
        self.songTimeLabel = QtGui.QLabel()
        self.songTimeLabel.setObjectName('songTimeLabel') 
        # 歌曲总时间
        self.songTotalTimeLabel = QtGui.QLabel()
        self.songTotalTimeLabel.setObjectName('songTotalTimeLabel')
        # 歌曲名称
        self.songNameWidget = QtGui.QLabel()
        self.songNameWidget.setObjectName('songNameWidget')
        # 播放模式
        self.playModeBtn = QtGui.QPushButton()
        self.playModeBtn.setObjectName('playModeBtn')
        # 声音调节
        self.volumeBtn = QtGui.QPushButton()
        self.volumeBtn.setObjectName('volumeBtn')

        # 间隔Label
        self.emptyLabel = QtGui.QLabel()
        self.emptyLabel.setObjectName('emptyLabel')

        #self.midLayout = QtGui.QVBoxLayout()
        #self.midLayout.addWidget(self.seekslIder,  0,QtCore.Qt.AlignHCenter)
        #self.midLayout.addWidget(self.songNameWidget,0,QtCore.Qt.AlignHCenter)

        self.leftLayout   = QtGui.QHBoxLayout()
        self.centerLayout = QtGui.QHBoxLayout()
        self.rightLayout  = QtGui.QHBoxLayout()

        self.leftLayout.addWidget(self.playOrPauseBtn,  0,QtCore.Qt.AlignLeft)
        #self.leftLayout.setAlignment(self.playOrPauseBtn,QtCore.Qt.AlignLeft)
        

        #self.centerLayout.addWidget(self.emptyLabel         ,0,QtCore.Qt.AlignRight)
        self.centerLayout.addWidget(self.playModeBtn        ,0,QtCore.Qt.AlignHCenter)
        self.centerLayout.addWidget(self.songTimeLabel      ,0,QtCore.Qt.AlignHCenter)
        self.centerLayout.addWidget(self.seekslIder         ,0,QtCore.Qt.AlignHCenter)

        self.centerLayout.addWidget(self.songTotalTimeLabel ,0,QtCore.Qt.AlignHCenter)
        self.centerLayout.addWidget(self.volumeBtn          ,0,QtCore.Qt.AlignHCenter)
        
        
        # 水平管理器
        self.control_layout = QtGui.QHBoxLayout()
        self.control_layout.addLayout(self.leftLayout   ,0)
        self.control_layout.addStretch()
        self.control_layout.addLayout(self.centerLayout ,0)
        self.control_layout.addStretch()
        self.control_layout.setSpacing(0)
        # setContentMargins(10, 10, 10, 10)
        
        self.seekslIder.setMinimum(290)
        self.seekslIder.setMaximum(100000)
        
        
        self.songNameWidget.setText(' YuPlaer')
        self.emptyLabel.setText('   ')

        self.font = QtGui.QFont()
        self.font.setPixelSize(11)   # 设置字号32,以像素为单位
        self.font.setFamily("SimSun")# 设置字体，宋体
        self.font.setFamily(u"微软雅黑")
        # self.font.setWeight(20)     # 设置字型,不加粗
        self.font.setBold(True)
        self.font.setItalic(False)   # 设置字型,不倾斜
        self.font.setUnderline(False)# 设置字型,无下划线

        self.songTimeLabel.setFont(self.font)
        self.songTotalTimeLabel.setFont(self.font)
        self.songNameWidget.setFont(self.font)
        '''
        Constant        Value   Description
        Qt.AlignLeft    0x0001  Aligns with the left edge.
        Qt.AlignRight   0x0002  Aligns with the right edge.
        Qt.AlignHCenter 0x0004  Centers horizontally in the available space.
        Qt.AlignJustify 0x0008  Justifies the text in the available space.
        The vertical flags are:

        Constant        Value   Description
        Qt.AlignTop     0x0020  Aligns with the top.
        Qt.AlignBottom  0x0040  Aligns with the bottom.
        Qt.AlignVCenter 0x0080  Centers vertically in the available space.

        '''
        self.widget = QtGui.QWidget()        
        self.setCentralWidget(self.widget)
        self.widget.setMouseTracking(True)
        self.setMouseTracking(True)

        self.widget.setLayout(self.control_layout)

        self.setStyleSheet('''
        controlBar
        {
            border-image:url(img/bottom_bar_bg.tiff);
            border: 0px;
        }
        /*貌似因为背景图片圆角没起作用*/
        .QMainWindow
        {
            background:transparent;
        }
        controlBar QWidget
        {
            border-top-left-radius:0px;
            border-top-right-radius:0px;
            border-bottom-right-radius:5px;
            border-bottom-left-radius:5px;
            margin : 0px 0px 0px 14px;
        }
        /*播放与暂停*/
        QCheckBox#playOrPauseBtn::indicator 
        {
            width: 29px;
            height: 28px;
        }
        QCheckBox#playOrPauseBtn
        {
            min-width: 29px;
            max-width: 29px;
            min-height: 28px;
            max-width: 28px;
            qproperty-text: "";
        }

        /*播放*/
        QCheckBox#playOrPauseBtn::indicator:unchecked
        {
            image:url("img/control/play_normal.tiff");
        }
        QCheckBox#playOrPauseBtn::indicator:unchecked:hover,
        QCheckBox#playOrPauseBtn::indicator:unchecked:pressed
        {
            image:url("img/control/play_down.tiff");
        }

        /*暂停*/
        QCheckBox#playOrPauseBtn::indicator::checked
        {
            image:url("img/control/pause_normal.tiff");
        }
        QCheckBox#playOrPauseBtn::indicator::checked:hover,
        QCheckBox#playOrPauseBtn::indicator::checked:pressed
        {
            image:url("img/control/pause_down.tiff");
        }

        /*歌曲名*/
        QLabel#songNameWidget
        {
            color:gray;
        }
        QLabel#songTotalTimeLabel
        {
            color:gray;
        }
        QLabel#songTimeLabel
        {
            color:gray;
        } 
        

        /*音量*/
        QPushButton#volumeBtn
        {
            min-width: 20px;
            max-width: 20px;
            min-height:20px;
            max-width: 20px;
            image:url("img/control/volume_2_down.tiff");
        }
        QPushButton#volumeBtn:hover
        {
            image:url("img/control/volume_2_hover.tiff");
        }
        QPushButton#volumeBtn:pressed
        {
            image:url("img/control/volume_2_down.tiff");
        }

        /*播放模式*/
        QPushButton#playModeBtn
        {
            min-width:  20px;
            max-width:  20px;
            min-height: 20px;
            max-height: 20px;
            qproperty-text: "";
            image:url("img/control/fullscreen_repeat_all_normal.tiff");
        }
         /*当前时间*/
        QLabel#songTimeLabel
        {
            margin: 0px 14px 0px 0px;
        }
        

        /*进度条*/
        QSlider::groove:horizontal
        {
            border:0px;
            height:8px;
            margin: 0px 0px 0px -14px;
        }  
        QSlider::sub-page:horizontal
        {
            background:orange;
            margin:0px 0px 0px -14px;
          
        }  
        QSlider::add-page:horizontal
        {
            background:gray;
        } 
        QSlider::handle:horizontal
        {
            background:white;
            width:20px;
            height:10px;
            border-radius:5px;
            margin:-3px 0px -3px 0px;
        }       
                    ''')


        self.connect(self.master.mediaObject, QtCore.SIGNAL("tick(qint64)"), self.timeToSliderValue)
        self.connect(self.master.mediaObject, SIGNAL("finished()"), self.finished)
        self.connect(self.seekslIder, QtCore.SIGNAL("sliderMoved(int)"), self.sliderMovedToTime) 
        


    # refresh slider value    
    def timeToSliderValue(self, time):  
        #print 'timeToSliderValue...'
        t = QTime().addMSecs(time) #.addMSecs(int(self.offset))  
        self.songTimeLabel.setText(t.toString("mm:ss"))
        self.seekslIder.setValue(time)
        #print time


    def sliderMovedToTime(self, time):
        #print 'sliderMoved ... ' 
        if self.topLevelWidget().mediaObject.state() != 2:
            return
        self.master.mediaObject.seek(time)

    def mouseMoveEvent(self,event):
        self.setCursor(QtCore.Qt.ArrowCursor)

    def finished(self):
        print 'finished...'        
        #self.master.mediaObject.seek(time)
        self.master.mediaObject.stop()

        # step1 - play
        #self.master.mediaObject.play()
        # step2 - pause (can trigger clicked of playOrPauseBtn)
        self.playOrPauseBtn.setChecked(False)
        

  
    def initSlider(self):
        # totalTime = self.master.mediaObject.totalTime()
        # print 'totalTime',totalTime            
        # self.seekslIder.setRange(0, totalTime)

        totalTime = self.master.audioFile.totalTime
        print 'initSlider  totalTime',totalTime            
        self.seekslIder.setRange(0, totalTime)
        self.seekslIder.setValue(0)




    def playOrPauseChange(self):   #按下按钮后检测当前的播放状态，如果为播放状态，那么停止
        # print 'self.master.mediaObject.state() : ',self.master.mediaObject.state()
        if self.master.mediaObject.state() == Phonon.PlayingState:
            self.master.mediaObject.pause()
        else:   #如果状态本身就是停止的那么就打开文件对话框选择媒体
            #self.master.mediaObject.stop()
            self.master.mediaObject.play()  #开始播放
            #self.timeToSliderValue(0)

                # audio = MP3(path)
                # if audio.info.length:self.master.mediaObject.state()
                #     time = QTime().addSecs(audio.info.length).toString("mm:ss")  
                # print 'time:',time
            
            
    #  
    def mediaStateChanged(self, newstate, oldstate):   #当播放状态该表时触发这个函数
        print ' newstate ..%d,%d',(newstate,oldstate) 
        if newstate == Phonon.PlayingState:  #检查播放状态            
            print ' mediaStateChanged ...'
            # totalTime = self.master.mediaObject.totalTime()
            # print 'totalTime',totalTime            
            # self.seekslIder.setRange(0, totalTime)

        elif newstate == Phonon.StoppedState:
            #self.setText('Choose File')
            #self.sliderMovedToTime(0)
            print ' StoppedState ... '
            
        elif newstate == Phonon.ErrorState:  #判断播放异常，这个很实用
            source = self.mediaObject.currentSource().fileName()   #抛出播放出错的文件名
            print 'ERROR: could not play:', source.toLocal8Bit().data()

