import QtQuick
import QtQuick.Window
import QtQuick 6.2
import QtQuick.Controls 6.2
import Backend 1.0

Window {
    id: mainWindow
    width: 500
    height: 500
    visible: true
    title: qsTr("NoteWise")

    Backend {
        id: backend
        onProcessingFinished: {
            msgDialog.open()
        }
    }

    Text {
        id: info0
        x: 313
        y: 8
        width: 278
        height: 51
        text: qsTr("NoteWise 0.1.0  15.05.23 build")
        anchors.top: parent.top
        font.pixelSize: 12
        anchors.topMargin: 3
    }

    TextInput {
        id: input_file_name
        x: 350
        y: 100
        width: 140
        height: 20
        color: input_file_name.focus ? "#434343" : "#888888"
        text: qsTr("plik_do_odczytu.txt")
        font.pixelSize: 12
        onFocusChanged: {
            if (input_file_name.focus && input_file_name.text === "plik_do_odczytu.txt") {
                input_file_name.text = "";
            }
        }
        onTextChanged: backend.setInputFileName(text)
    }

    Text {
        id: info1
        x: 20
        y: 100
        width: 203
        height: 52
        text: qsTr("Wprowadz nazwe pliku z formatem .txt")
        font.pixelSize: 12
    }

    Button {
        id: startButton
        x: 55
        y: 302
        width: 233
        height: 93
        text: qsTr("Generuj plik")
        anchors.horizontalCenterOffset: 130
        anchors.horizontalCenter: info1.horizontalCenter
        onClicked: {
            backend.setInputFileName(input_file_name.text !== "" ? input_file_name.text : "plik_do_odczytu.txt");
            backend.setSaveFileName(new_file_name.text !== "" ? new_file_name.text : "wygenerowane_notatki.txt");
            backend.startProcessing();
        }
    }

    Text {
        id: info2
        x: 20
        y: 155
        width: 321
        height: 52
        text: qsTr("Wprowadz nazwe pod ktora chcesz zeby zapisaly sie notatki")
        anchors.left: info1.left
        anchors.top: info1.bottom
        font.pixelSize: 12
        anchors.topMargin: 6
    }

    TextInput {
        id: new_file_name
        x: 350
        y: 155
        width: 140
        height: 20
        color: new_file_name.focus ? "#434343" : "#888888"
        text: qsTr("wygenerowane_notatki.txt")
        font.pixelSize: 12
        onFocusChanged: {
            if (new_file_name.focus && new_file_name.text === "wygenerowane_notatki.txt") {
                new_file_name.text = "";
            }
        }
        onTextChanged: backend.setSaveFileName(text)
    }
}
