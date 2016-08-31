import QtQuick 1.0

Rectangle {
    id: page
    width: 360
    height: 640
 

    ListModel {
        id: model
        ListElement { title: "1" }
        ListElement { title: "2" }
        ListElement { title: "3" }
        ListElement { title: "4" }
        ListElement { title: "5" }
        ListElement { title: "6" }
        ListElement { title: "7" }
        ListElement { title: "8" }
    }
 

    ListView {
        id: view
        anchors.fill: parent
        anchors.rightMargin: 12
        model: model
        delegate: delegate
        spacing: 5
    }

    Component {
        id: delegate
 

        Rectangle {
            width: parent.width
            height: 100
            border.color: "red"
 
            Text {
                anchors.centerIn: parent
                text: title
                font.pointSize: 24
                color: "black"
            }
        }
    }
 

    Rectangle {
        id: scrollbar
        x: 350
        y: 0
        width: 10
        height: 640
        color: "black"
 

        Rectangle {
            id: button
            x: 0
            y: view.visibleArea.yPosition * scrollbar.height
            width: 10
            height: view.visibleArea.heightRatio * scrollbar.height;
            color: "green"
 

            MouseArea {
                id: mouseArea
                anchors.fill: button
                drag.target: button
                drag.axis: Drag.YAxis
                drag.minimumY: 0
                drag.maximumY: scrollbar.height - button.height
 

                onMouseYChanged: {
                    view.contentY = button.y / scrollbar.height * view.contentHeight
                }
            }
        }
    }
}