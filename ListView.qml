import QtQuick 1.0

Rectangle {
    width: 280; height: 300
    

    Component {
        id: contactDelegate2
        Item {
            width: 180; height: 40
            Column {
                Text { text: '<b>Name:</b> ' + name }
                Text { text: '<b>Number:</b> ' + number }
            }
        }
        
    }

    ListView {
        id:listview1
        anchors.fill: parent
        model: ContactModel {}
        highlight: Rectangle { color: "lightsteelblue"; radius: 5 }
        focus: true
        delegate: Component {
            id: contactDelegate
            Rectangle{
                property bool pressed: false;
                id:wrapper;
                width: wrapper.ListView.view.width;
                height: Math.max(wrapper.ListView.view.height/wrapper.ListView.view.model.count,60);
                color: "white";
                border.width: 0;
                Text {
                    id: text
                    anchors.centerIn: parent;
                    text: model.name;
                }
                
                MouseArea {
                    anchors.fill: parent;
                    onClicked: {
                        console.log('count:' + listview1.count)
                        for(var i=0;i<listview1.count;i ++) {
                            wrapper.color = "white";
                            console.log('listview1 0 :' + listview1[0])

                        }
                        listview1.currentIndex = index
                        console.log(listview1.currentIndex); 
                        wrapper.color = "blue";

                        
                    }
                    onExited: {
                        console.log("exit");
                        
                    }
                }
                states: [
                    State {
                        name: "pressed"; when: wrapper===true;
                        PropertyChanges {
                            target: wrapper;
                            color: "deepskyblue";
                        }
                    }
                ]

   
            }
            
        }

    }

  
}