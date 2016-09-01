import QtQuick 1.0
ListView {
    property string mediaCurrTime;
    width: parent.width; height: parent.width
    model: Less {}
    snapMode : ListView.SnapToItem 
    delegate: Component {
        id: contactDelegate        
            Column {
                width : parent.width     
                
                TextEdit {                 
                    id: contentText
                    width: parent.width             
                    wrapMode : Text.WordWrap
                    font.pointSize: 14
                    text: content +"\n"
                    font.family: "Calibri"
                    /*MouseArea {
                        anchors.fill: parent
                        onClicked: {
                           console.log('11:'+timeStart)
                        }
                        
                    }*/
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            console.log('section time :'+timeStart)
                            console.log('mediaCurrTime time :'+mediaCurrTime)
                            
                            
                            if (!contentText.activeFocus) {
                                contentText.forceActiveFocus();
                                contentText.openSoftwareInputPanel();
                            } else {
                                contentText.focus = false;
                            }
                        }
                        onPressAndHold: contentText.closeSoftwareInputPanel();
                    }
                    
                    states: [
                        State {
                            name: "wide text"
                            when: (mediaCurrTime >= timeStart) & (mediaCurrTime < timeEnd)
                            PropertyChanges {
                                target: contentText
                                font.pointSize: 18
                            }
                        },
                        State {
                            name: "not wide text"
                            when: !((mediaCurrTime >= timeStart) & (mediaCurrTime < timeEnd))
                            PropertyChanges {
                                target: contentText
                                font.pointSize: 14
                            }
                        }
                    ]
                }
            }
       
    }
}

