import QtQuick 1.0

Item {
    TitleBar { id: titleBar; width: parent.width; height: 60;
        y: -80
        untaggedString: "Latest tweets from everyone"
        taggedString: "Latest tweets from "
    }
    states: [
        State {
            name: "search"; when: screen.state!="search"
            PropertyChanges { target: titleBar; y: 0 }
        }
    ]
    transitions: [
        Transition { NumberAnimation { properties: "x,y"; duration: 500; easing.type: Easing.InOutQuad } }
    ]
}