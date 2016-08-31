import QtQuick 1.0

Item {
    id: titleBar
    property string untaggedString: "Uploads from everyone"
    property string taggedString: "Recent uploads tagged "

    BorderImage { source: "images/titlebar.sci"; width: parent.width; height: parent.height + 14; y: -7 }

    Item {
        id: container
        width: (parent.width * 2) - 55 ; height: parent.height

        function accept() {
            titleBar.state = ""
            background.state = ""
            rssModel.tags = editor.text
        }

        Item {
            id:imageBox
            x: 6; width: 0; height: 50; smooth: true
            anchors.verticalCenter: parent.verticalCenter

            UserModel { user: rssModel.from; id: userModel }
            Component {
                id: imgDelegate;
                Item {
                    id:imageitem
                    visible:true
                    Loading { width:48; height:48; visible: realImage.status != Image.Ready }
                    Image { id: realImage; source: image; width:48; height:48; opacity:0; }
                    states:
                        State {
                        name: "loaded"
                        when:  (realImage.status == Image.Ready)
                        PropertyChanges { target: realImage; opacity:1 }
                    }
                    transitions: Transition {
                        NumberAnimation { target: realImage; property: "opacity"; duration: 200 }
                    }
                }
            }
            ListView { id:view; model: userModel.model; x:1; y:1; delegate: imgDelegate }
            states:
            State {
                when: !userModel.user==""
                PropertyChanges { target: imageBox; width: 50; }
            }
            transitions:
            Transition {
                NumberAnimation { target: imageBox; property: "width"; duration: 200 }
            }
        }

        Image {
            id: quitButton
            x: 5
            anchors.verticalCenter: parent.verticalCenter
            source: "images/quit.png"
            MouseArea {
                anchors.fill: parent
                onClicked: Qt.quit()
            }
        }

        Text {
            id: categoryText
            anchors {
                left: quitButton.right; right: parent.right; leftMargin: 10; rightMargin: 10
                verticalCenter: parent.verticalCenter
            }
            elide: Text.ElideLeft
            text: (rssModel.from=="" ? untaggedString : taggedString + rssModel.from)
            font.bold: true; color: "White"; style: Text.Raised; styleColor: "Black"
            font.pixelSize: 12
        }
    }

    states: State {
        name: "Tags"
        PropertyChanges { target: container; x: -tagButton.x + 5 }
        PropertyChanges { target: editor; focus: true }
    }

    transitions: Transition {
        NumberAnimation { properties: "x"; easing.type: Easing.InOutQuad }
    }
}