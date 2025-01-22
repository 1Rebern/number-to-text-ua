import QtQuick 6
import QtQuick.Window 2.15
import QtQuick.Controls 6
import QtQuick.Controls.Material 2.15

ApplicationWindow{
    id: window
    width: 300
    height: 300
    visible: true
    title: qsTr("Конвертувач")

    flags: Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint | Qt.CustomizeWindowHint | Qt.MSWindowsFixedSizeDialogHint | Qt.WindowTitleHint

    Material.theme: Material.Dark
    Material.accent: Material.LightBlue

    property string textConvert: ""


    Rectangle {
        id: topBarNum
        height: 40
        color: Material.color(Material.Orange)
        anchors {
            left: parent.left
            right: parent.right
            top: parent.top
            margins: 10
        }
        radius: 5

        Text {
            text: qsTr("ВВЕДІТЬ ЧИСЛО")
            anchors.verticalCenter: parent.verticalCenter
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            color: "#ffffff"
            anchors.horizontalCenter: parent.horizontalCenter
            font.pointSize: 10
        }
    }

    TextField{
            id: number
            width: 280
            text: qsTr("")
            selectByMouse: true
            placeholderText: qsTr("Число")
            verticalAlignment: Text.AlignVCenter
            anchors.top: topBarNum.bottom
            anchors.topMargin: 10
            anchors.left: parent.left
            anchors.leftMargin: 10
        }

    Button{
            id: convertButton
            width: 280
            text: qsTr("Конвертувати в текст")
            anchors.horizontalCenter: parent.horizontalCenter 
            anchors.top: number.bottom
            anchors.topMargin: 5
            onClicked: backend.checkNumber(number.text)
        }

    Rectangle {
        id: topBarText
        height: 40
        color: Material.color(Material.Orange)
        anchors {
            left: parent.left
            right: parent.right
            top: convertButton.bottom
            margins: 7
        }
        radius: 5

        Text {
            text: qsTr("КОНВЕРТОВАНЕ ЧИСЛО")
            anchors.verticalCenter: parent.verticalCenter
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            color: "#ffffff"
            anchors.horizontalCenter: parent.horizontalCenter
            font.pointSize: 10
        }
    }

    TextField{
            id: convertedNumber
            width: 280
            text: textConvert
            selectByMouse: true
            verticalAlignment: Text.AlignVCenter
            anchors.top: topBarText.bottom
            anchors.topMargin: 10
            anchors.left: parent.left
            anchors.leftMargin: 10
        }
    
    Connections{
        target: backend

        function onSignalText(myText){
            textConvert = myText
        }

        function onSignalNum(boolValue){
            if(boolValue){
                number.Material.foreground = Material.Green
                number.Material.accent = Material.Green

            }else{
                textConvert = "Введіть числове значення"
                number.Material.foreground = Material.Pink
                number.Material.accent = Material.Pink
            }
        }

        function onSignalNumMax(boolValue){
            if(boolValue){
                textConvert = "Введене число завелике"
                number.Material.foreground = Material.Pink
                number.Material.accent = Material.Pink
            }
        }

        function onSignalNumDec(boolValue){
            if(boolValue){
                textConvert = "Забагато знаків після коми"
                number.Material.foreground = Material.Pink
                number.Material.accent = Material.Pink
            }
        }
    }
}