import QtQuick 1.0

FocusScope {
    id: wrapper
    Column {
        anchors.centerIn: parent
        spacing: 20
        Column{
            spacing: 4
            Text {
                text: "Posted by:"
                font.pixelSize: 16; font.bold: true; color: "white"; style: Text.Raised; styleColor: "black"
                horizontalAlignment: Qt.AlignRight
            }
            Input{
                id: fromIn
                KeyNavigation.backtab: searchbutton
                KeyNavigation.tab:toIn
                onAccepted:searchbutton.doSearch();
                focus: true
            }
            Text {
                text: "In reply to:"
                font.pixelSize: 16; font.bold: true; color: "white"; style: Text.Raised; styleColor: "black"
                horizontalAlignment: Qt.AlignRight
            }
            Input{
                id: toIn
                KeyNavigation.backtab: fromIn
                KeyNavigation.tab:phraseIn
                onAccepted:searchbutton.doSearch();
            }
            Text {
                text: "Search phrase:"
                font.pixelSize: 16; font.bold: true; color: "white"; style: Text.Raised; styleColor: "black"
                horizontalAlignment: Qt.AlignRight
            }
            Input{
                id: phraseIn
                KeyNavigation.backtab: toIn
                KeyNavigation.tab:searchbutton
                onAccepted:searchbutton.doSearch();
                text: "Qt Quick"
            }
        }
        Button {
            width: 100
            height: 32
            id: searchbutton
            keyUsing: true;
            opacity: 1
            text: "Search"
            KeyNavigation.tab: fromIn
            Keys.onReturnPressed: searchbutton.doSearch();
            Keys.onEnterPressed: searchbutton.doSearch();
            Keys.onSelectPressed: searchbutton.doSearch();
            Keys.onSpacePressed: searchbutton.doSearch();
            onClicked: searchbutton.doSearch();

            function doSearch() {
                // Search ! allowed
                if (wrapper.state=="invalidinput")
                    return;

                rssModel.from=fromIn.text;
                rssModel.to= toIn.text;
                rssModel.phrase = phraseIn.text;
                screen.focus = true;
                screen.state = ""
            }
        }
    }
    states:
    State {
        name: "invalidinput"
        when: fromIn.text=="" && toIn.text=="" && phraseIn.text==""
        PropertyChanges { target: searchbutton ; opacity: 0.6 ; }
    }
    transitions:
    Transition {
        NumberAnimation { target: searchbutton; property: "opacity"; duration: 200 }
    }
}