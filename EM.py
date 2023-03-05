import random

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QTimer


class EnigmaGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window properties
        self.setWindowTitle('Enigma Machine')
        self.setGeometry(100, 100, 450, 300)

        # Create a QTimer object to reset button styles
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.resetKeyboardButtonStyle)

        self.wheel1 = {1: 22, 2: 3, 3: 17, 4: 16, 5: 20, 6: 6, 7: 8, 8: 12, 9: 19, 10: 2, 11: 24, 12: 1, 13: 5,
                            14: 7, 15: 15, 16: 4, 17: 14, 18: 26, 19: 23, 20: 13, 21: 11, 22: 21, 23: 25, 24: 9, 25: 10,
                            26: 18}
        self.wheel2 = {1: 1, 2: 7, 3: 15, 4: 10, 5: 19, 6: 6, 7: 14, 8: 4, 9: 3, 10: 17, 11: 5, 12: 23, 13: 16,
                            14: 9, 15: 2, 16: 12, 17: 8, 18: 24, 19: 11, 20: 20, 21: 21, 22: 25, 23: 22, 24: 26, 25: 18,
                            26: 13}
        self.wheel3 = {1: 22, 2: 7, 3: 19, 4: 6, 5: 17, 6: 25, 7: 3, 8: 13, 9: 10, 10: 1, 11: 21, 12: 24, 13: 5,
                            14: 8, 15: 9, 16: 14, 17: 2, 18: 23, 19: 26, 20: 15, 21: 4, 22: 12, 23: 18, 24: 20, 25: 11,
                            26: 16}
        self.wheel4 ={1: 7, 7: 1, 2: 11, 11: 2, 3: 12, 12: 3, 4: 15, 15: 4, 5: 20, 20: 5, 6: 16, 16: 6, 8: 19, 19: 8, 9: 18,
                18: 9, 10: 10, 13: 26, 26: 13, 14: 23, 23: 14, 17: 25, 25: 17, 21: 24, 24: 21, 22: 22}
        self.prevText = ""

        # Create rotor input widgets
        rotor1_label = QtWidgets.QLabel('Rotor 1:', self)
        rotor1_label.move(10, 10)

        self.rotor1_input = QtWidgets.QSpinBox(self)
        self.rotor1_input.move(70, 10)
        self.rotor1_input.resize(50, 20)
        self.rotor1_input.setMinimum(1)
        self.rotor1_input.setMaximum(26)

        rotor2_label = QtWidgets.QLabel('Rotor 2:', self)
        rotor2_label.move(160, 10)

        self.rotor2_input = QtWidgets.QSpinBox(self)
        self.rotor2_input.move(210, 10)
        self.rotor2_input.resize(50, 20)
        self.rotor2_input.setMinimum(1)
        self.rotor2_input.setMaximum(26)



        rotor3_label = QtWidgets.QLabel('Rotor 3:', self)
        rotor3_label.move(310, 10)

        self.rotor3_input = QtWidgets.QSpinBox(self)
        self.rotor3_input.move(370, 10)
        self.rotor3_input.resize(50, 20)
        self.rotor3_input.setMinimum(1)
        self.rotor3_input.setMaximum(26)

        # Create plugboard input widget
        plugboard_label = QtWidgets.QLabel('INPUT:', self)
        plugboard_label.move(10, 40)

        self.userInput = QtWidgets.QLineEdit(self)
        self.userInput.move(70, 40)
        self.userInput.resize(350, 20)
        self.userInput.textChanged.connect(self.updateKeyboardButtons)

        # Keep track of the last keyboard button that was pressed
        self.last_keyboard_button = None

        # Create output widget
        output_label = QtWidgets.QLabel('Output:', self)
        output_label.move(10, 70)

        self.outputText = ""

        self.output_output = QtWidgets.QLineEdit(self)
        self.output_output.move(70, 70)
        self.output_output.resize(350, 20)

        # Create keyboard widget
        keyboard_frame = QtWidgets.QFrame(self)
        keyboard_frame.setGeometry(10, 100, 380, 180)
        keyboard_frame.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)

        layout = QtWidgets.QGridLayout()
        keyboard_frame.setLayout(layout)

        self.keyboard_buttons = {}

        letters = 'abcdefghijklmnopqrstuvwxyz'

        for i in range(len(letters)):
            button = QtWidgets.QPushButton(letters[i])
            button.setFixedSize(20, 20)
            self.keyboard_buttons[letters[i]] = button
            layout.addWidget(button, i // 10, i % 10)

        # Create key press event filter for the keyboard buttons
        for button in keyboard_frame.findChildren(QtWidgets.QPushButton):
            button.installEventFilter(self)

        # Show the window
        self.show()

    def updateKeyboardButtons(self, text):
        count = len(text) - len(self.prevText)
        text = text.lower()
        if text and count>0 and text[len(text)-1] in 'abcdefghijklmnopqrstuvwxyz ' :
            if count>1:
                output = ''
                input = text[-count:]
                for i in range(count):
                    if input[i] != ' ':
                        self.lightTheKeyboard(input[i])
                        output += self.encoder(input[i])
                        self.spinTheWheels(1)
                    else:
                        self.spinTheWheels(1)
                        output += ' '
                for i in range(count):
                    self.spinTheWheels(-1)
                self.outputText += output
                self.output_output.setText(self.outputText)
            else:
                if text[len(text)-1] != ' ':
                    output = self.encoder(text[len(text) - 1])
                    self.outputText += output
                    self.output_output.setText(self.outputText)
                    self.lightTheKeyboard(self.outputText)

                else:
                    self.outputText += " "
                    self.output_output.setText(self.outputText)

        if count < 0:
            self.outputText = self.outputText[:count]
            self.output_output.setText(self.outputText)

        self.prevText = text
        # Update the GUI to highlight letters that appear in the plugboard input
        # for button in self.keyboard_buttons.values():
        #     button.setStyleSheet('')


        self.spinTheWheels(count)
    def lightTheKeyboard(self,text):
        for letter in text:
            if letter in self.keyboard_buttons:
                button = self.keyboard_buttons[letter]

                # Reset the stylesheet of the last button that was pressed
                if self.last_keyboard_button:
                    self.last_keyboard_button.setStyleSheet('')
                self.last_keyboard_button = button

                button.setStyleSheet('background-color: #aaffaa')
                self.timer.start(500)  # Set the timer interval to 1 second


    def forwardWheelOutput(self,wheelShift,wheel,value):
        location = (value + wheelShift -1)
        if location >26:
            location = location % 26
        res = int(wheel[location]) - wheelShift +1
        if res <= 0 :
            res +=26
        return res

    def backwardsWheelOutput(self,wheelShift,wheel,value):
        location = (value + wheelShift - 1)
        if location > 26:
            location = location % 26
        for exit, enter in wheel.items():
            if enter == location:
                res = exit
                break
        res = res - wheelShift + 1
        if res <= 0 :
            res +=26
        return res



    def encoder(self,button):

        letterNum = int(ord(button) - ord('a') + 1)
        wheelNum3 = int(self.rotor3_input.text())
        # rand = int(self.wheel3[(letterNum + wheelNum3 -1)% 27])
        # print(letterNum+(rand-(letterNum + wheelNum3 -1)))
        #print(self.forwardWheelOutput(wheelNum3,self.wheel3,letterNum))
        res1 = self.forwardWheelOutput(wheelNum3,self.wheel3,letterNum)

        wheelNum2 = int(self.rotor2_input.text())
        #print(self.forwardWheelOutput(wheelNum2, self.wheel2, res))
        res2 = self.forwardWheelOutput(wheelNum2, self.wheel2, res1)

        wheelNum1 = int(self.rotor1_input.text())
        #print(self.forwardWheelOutput(wheelNum1, self.wheel1, res))
        res3 = self.forwardWheelOutput(wheelNum1, self.wheel1, res2)
        #print(res1, res2, res3)
        res4 = self.wheel4[res3]
        #print(res4)


        res5 = self.backwardsWheelOutput(wheelNum1, self.wheel1, res4)

        res6 = self.backwardsWheelOutput(wheelNum2, self.wheel2, res5)

        res7 = (self.backwardsWheelOutput(wheelNum3, self.wheel3, res6))
        #print(res5, res6, res7)
        return chr(res7 + 96)
        print(chr(res7 + 96))

    def spinTheWheels(self, count):
        if count > 0:
            if (int(self.rotor3_input.text()) + count )> 26:
                self.rotor3_input.setValue(((int(self.rotor3_input.text()) + count)%26))
                if int(self.rotor2_input.text())  == 26:
                    self.rotor2_input.setValue(1)
                    if int(self.rotor1_input.text()) == 26:
                        self.rotor1_input.setValue(1)
                    else:
                        self.rotor1_input.setValue(int(self.rotor1_input.text()) + 1)
                else:
                    self.rotor2_input.setValue(int(self.rotor2_input.text()) +1)
            else:
                self.rotor3_input.setValue((int(self.rotor3_input.text()) + count))
        else:
            if (int(self.rotor3_input.text()) + count) < 1:
                self.rotor3_input.setValue(((int(self.rotor3_input.text()) + count)+26))
                if int(self.rotor2_input.text()) == 1:
                    self.rotor2_input.setValue(26)
                    if int(self.rotor1_input.text()) == 1:
                        self.rotor1_input.setValue(26)
                    else:
                        self.rotor1_input.setValue(int(self.rotor1_input.text()) - 1)
                else:
                    self.rotor2_input.setValue(int(self.rotor2_input.text()) - 1)
            else:
                self.rotor3_input.setValue((int(self.rotor3_input.text()) + count))


    def resetKeyboardButtonStyle(self):
        # Reset the stylesheet of all keyboard buttons
        for button in self.keyboard_buttons.values():
            button.setStyleSheet('')


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    gui = EnigmaGUI()
    app.exec_()
