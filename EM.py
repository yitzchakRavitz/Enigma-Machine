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
        self.setGeometry(100, 100, 450, 400)

        # Create a QTimer object to reset button styles
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.resetKeyboardButtonStyle)
        self.wheel_I = {1: 22, 2: 3, 3: 17, 4: 16, 5: 20, 6: 6, 7: 8, 8: 12, 9: 19, 10: 2, 11: 24, 12: 1, 13: 5,
                        14: 7, 15: 15, 16: 4, 17: 14, 18: 26, 19: 23, 20: 13, 21: 11, 22: 21, 23: 25, 24: 9, 25: 10,
                        26: 18}
        self.wheel_II = {1: 1, 2: 7, 3: 15, 4: 10, 5: 19, 6: 6, 7: 14, 8: 4, 9: 3, 10: 17, 11: 5, 12: 23, 13: 16,
                         14: 9, 15: 2, 16: 12, 17: 8, 18: 24, 19: 11, 20: 20, 21: 21, 22: 25, 23: 22, 24: 26, 25: 18,
                         26: 13}
        self.wheel_III = {1: 22, 2: 7, 3: 19, 4: 6, 5: 17, 6: 25, 7: 3, 8: 13, 9: 10, 10: 1, 11: 21, 12: 24, 13: 5,
                          14: 8, 15: 9, 16: 14, 17: 2, 18: 23, 19: 26, 20: 15, 21: 4, 22: 12, 23: 18, 24: 20, 25: 11,
                          26: 16}
        self.wheel_IV = {1: 9, 2: 13, 3: 24, 4: 1, 5: 2, 6: 15, 7: 22, 8: 3, 9: 10, 10: 17, 11: 7, 12: 8, 13: 25, 14: 6,
                         15: 12,
                         16: 18, 17: 5, 18: 11, 19: 21, 20: 4, 21: 14, 22: 16, 23: 19, 24: 23, 25: 20, 26: 26}
        self.wheel_V = {1: 22, 2: 7, 3: 15, 4: 9, 5: 8, 6: 4, 7: 26, 8: 14, 9: 17, 10: 13, 11: 12, 12: 5, 13: 10,
                        14: 21, 15: 20,
                        16: 1, 17: 2, 18: 25, 19: 16, 20: 18, 21: 11, 22: 23, 23: 3, 24: 6, 25: 24, 26: 19}

        self.wheel1 = self.wheel_I
        self.wheel2 = self.wheel_II
        self.wheel3 = self.wheel_III
        self.reflector = {1: 7, 7: 1, 2: 11, 11: 2, 3: 12, 12: 3, 4: 15, 15: 4, 5: 20, 20: 5, 6: 16, 16: 6, 8: 19,
                          19: 8, 9: 18,
                          18: 9, 10: 22, 13: 26, 26: 13, 14: 23, 23: 14, 17: 25, 25: 17, 21: 24, 24: 21, 22: 10}
        self.prevText = ""
        self.rotor1_prev = 'I'
        self.rotor2_prev = 'II'
        self.rotor3_prev = 'III'

        rotor = QtWidgets.QLabel('select rotors:', self)
        rotor.move(10, 10)

        self.rotor1 = QtWidgets.QComboBox(self)
        self.rotor1.move(70, 30)
        self.rotor1.resize(50, 20)
        self.rotor1.currentIndexChanged.connect(self.selecte_rotor_1)

        self.rotor2 = QtWidgets.QComboBox(self)
        self.rotor2.move(210, 30)
        self.rotor2.resize(50, 20)
        self.rotor2.currentIndexChanged.connect(self.selecte_rotor_2)

        self.rotor3 = QtWidgets.QComboBox(self)
        self.rotor3.move(370, 30)
        self.rotor3.resize(50, 20)
        self.rotor3.currentIndexChanged.connect(self.selecte_rotor_3)

        options = ['I', 'II', 'III', 'IV', 'V']
        for option in options:
            self.rotor1.addItem(option)
            self.rotor2.addItem(option)
            self.rotor3.addItem(option)



        self.rotor2.setCurrentText('II')
        self.rotor3.setCurrentText('III')
        # Create rotor input widgets
        rotor1_label = QtWidgets.QLabel('Rotor 1:', self)
        rotor1_label.move(10, 70)

        self.rotor1_input = QtWidgets.QSpinBox(self)
        self.rotor1_input.move(70, 70)
        self.rotor1_input.resize(50, 20)
        self.rotor1_input.setMinimum(1)
        self.rotor1_input.setMaximum(26)

        rotor2_label = QtWidgets.QLabel('Rotor 2:', self)
        rotor2_label.move(160, 70)

        self.rotor2_input = QtWidgets.QSpinBox(self)
        self.rotor2_input.move(210, 70)
        self.rotor2_input.resize(50, 20)
        self.rotor2_input.setMinimum(1)
        self.rotor2_input.setMaximum(26)

        rotor3_label = QtWidgets.QLabel('Rotor 3:', self)
        rotor3_label.move(310, 70)

        self.rotor3_input = QtWidgets.QSpinBox(self)
        self.rotor3_input.move(370, 70)
        self.rotor3_input.resize(50, 20)
        self.rotor3_input.setMinimum(1)
        self.rotor3_input.setMaximum(26)

        # Create plugboard input widget
        plugboard_label = QtWidgets.QLabel('INPUT:', self)
        plugboard_label.move(10, 100)

        self.userInput = QtWidgets.QLineEdit(self)
        self.userInput.move(70, 100)
        self.userInput.resize(350, 20)
        self.userInput.textChanged.connect(self.updateKeyboardButtons)

        # Keep track of the last keyboard button that was pressed
        self.last_keyboard_button = None

        # Create output widget
        output_label = QtWidgets.QLabel('Output:', self)
        output_label.move(10, 130)

        self.outputText = ""

        self.output_output = QtWidgets.QLineEdit(self)
        self.output_output.move(70, 130)
        self.output_output.resize(350, 20)

        # Create keyboard widget
        keyboard_frame = QtWidgets.QFrame(self)
        keyboard_frame.setGeometry(10, 170, 400, 180)
        keyboard_frame.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)

        layout = QtWidgets.QGridLayout()
        keyboard_frame.setLayout(layout)

        self.keyboard_buttons = {}
        self.lastLetterPressed = ''
        self.mixLettersMap = {}
        self.lastColor = 0
        self.colors = ['Red','Blue','Green','Yellow','Purple','Orange','Brown','Azure','White','Gray','Pink','Teal','Navy','Light Brown']
        self.buttonsColors = {}
        letters = 'abcdefghijklmnopqrstuvwxyz'

        for i in range(len(letters)):
            button = QtWidgets.QPushButton(letters[i])
            button.setFixedSize(20, 20)
            button.clicked.connect(self.onKeyboardButtonClicked) # Connect the clicked signal to a method
            self.keyboard_buttons[letters[i]] = button
            layout.addWidget(button, i // 10, i % 10)

        # Create key press event filter for the keyboard buttons
        for button in keyboard_frame.findChildren(QtWidgets.QPushButton):
            button.installEventFilter(self)

        # Show the window
        self.show()
    def getLastColor(self):
        if self.lastLetterPressed != '':
            return self.buttonsColors[self.lastLetterPressed]
        for color in self.colors:
            if color not in self.buttonsColors.values():
                return color

    def onKeyboardButtonClicked(self):
        button = self.sender()  # Get the button that was clicked
        lastColor = self.getLastColor()
        self.buttonsColors[button.text()] = lastColor
        if self.lastLetterPressed != button.text() and self.lastLetterPressed != '':
            if button.text() in self.mixLettersMap:
                letter = self.mixLettersMap[button.text()]
                self.mixLettersMap.pop(letter)
                self.mixLettersMap.pop(button.text())
                letter  = self.keyboard_buttons[letter]
                letter.setStyleSheet('')
                self.buttonsColors[letter.text()] = ''


            self.mixLettersMap[self.lastLetterPressed] = button.text()
            self.mixLettersMap[button.text()] = self.lastLetterPressed
            button.setStyleSheet("background-color:" + lastColor)

            self.lastLetterPressed = ''


        elif self.lastLetterPressed == '':
            if button.text() in self.mixLettersMap:
                letter = self.mixLettersMap[button.text()]
                self.mixLettersMap.pop(letter)
                self.mixLettersMap.pop(button.text())
                letter  = self.keyboard_buttons[letter]
                letter.setStyleSheet('')
                self.buttonsColors[letter.text()] = ''

            button.setStyleSheet("background-color:" + lastColor)
            self.lastLetterPressed = button.text()
        # print(self.buttonsColors)
        # print(self.mixLettersMap)

    # def resetKeyboardButtonStyle(self):
    #     for button in self.keyboard.findChildren(QtWidgets.QPushButton):
    #         button.setStyleSheet("")  # Reset the background color of all buttons


    def get_rotor(self, rotor):
        if rotor == 'I':
            return self.wheel_I
        if rotor == 'II':
            return self.wheel_II
        if rotor == 'III':
            return self.wheel_III
        if rotor == 'IV':
            return self.wheel_IV
        if rotor == 'V':
            return self.wheel_V

    def selecte_rotor_1(self):
        selected_option = self.rotor1.currentText()
        rotor = self.get_rotor(selected_option)
        if self.wheel2 == rotor or self.wheel3 == rotor:
            self.rotor1.setCurrentText(self.rotor1_prev)
        else:
            self.wheel1 = rotor
            self.rotor1_prev = selected_option

    def selecte_rotor_2(self):
        selected_option = self.rotor2.currentText()
        rotor = self.get_rotor(selected_option)
        if self.wheel1 == rotor or self.wheel3 == rotor:
            self.rotor2.setCurrentText(self.rotor2_prev)
        else:
            self.wheel2 = rotor
            self.rotor2_prev = selected_option

    def selecte_rotor_3(self):
        selected_option = self.rotor3.currentText()
        rotor = self.get_rotor(selected_option)
        if self.wheel2 == rotor or self.wheel1 == rotor:
            self.rotor3.setCurrentText(self.rotor3_prev)
        else:
            self.wheel3 = rotor
            self.rotor3_prev = selected_option

    def updateKeyboardButtons(self, text):
        count = len(text) - len(self.prevText)
        text = text.lower()
        if text and count > 0 and text[len(text) - 1] in 'abcdefghijklmnopqrstuvwxyz ':
            if count > 1:
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
                if text[len(text) - 1] != ' ':
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

    def lightTheKeyboard(self, text):
        # count = len(text) -1
        # text = text.lower()
        # print(text[count])
        #
        # button = self.keyboard_buttons[text[count]]
        # style = button.style()
        # print(style)
        # button.setStyleSheet('background-color: #aaffaa')
        # self.timer.start(500)  # Set the timer interval to 1 second

        for letter in text:
            if letter in self.keyboard_buttons:
                button = self.keyboard_buttons[letter]

                # Reset the stylesheet of the last button that was pressed
                if self.last_keyboard_button:
                    if self.last_keyboard_button.text() in self.buttonsColors:
                        self.last_keyboard_button.setStyleSheet('background-color: ' + self.buttonsColors[self.last_keyboard_button.text()])
                    else:
                        self.last_keyboard_button.setStyleSheet('')
                self.last_keyboard_button = button
                print(button.text())
                button.setStyleSheet('background-color: #aaffaa')
                self.timer.start(500)  # Set the timer interval to 1 second

    def forwardWheelOutput(self, wheelShift, wheel, value):
        location = (value + wheelShift - 1)
        if location > 26:
            location = location % 26
        res = int(wheel[location]) - wheelShift + 1
        if res <= 0:
            res += 26
        return res

    def backwardsWheelOutput(self, wheelShift, wheel, value):
        location = (value + wheelShift - 1)
        if location > 26:
            location = location % 26
        for exit, enter in wheel.items():
            if enter == location:
                res = exit
                break
        res = res - wheelShift + 1
        if res <= 0:
            res += 26
        return res

    def encoder(self, button):
        if button in self.mixLettersMap:
            button = self.mixLettersMap[button]

        letterNum = int(ord(button) - ord('a') + 1)
        wheelNum3 = int(self.rotor3_input.text())
        # rand = int(self.wheel3[(letterNum + wheelNum3 -1)% 27])
        # print(letterNum+(rand-(letterNum + wheelNum3 -1)))
        # print(self.forwardWheelOutput(wheelNum3,self.wheel3,letterNum))
        res1 = self.forwardWheelOutput(wheelNum3, self.wheel3, letterNum)

        wheelNum2 = int(self.rotor2_input.text())
        # print(self.forwardWheelOutput(wheelNum2, self.wheel2, res))
        res2 = self.forwardWheelOutput(wheelNum2, self.wheel2, res1)

        wheelNum1 = int(self.rotor1_input.text())
        # print(self.forwardWheelOutput(wheelNum1, self.wheel1, res))
        res3 = self.forwardWheelOutput(wheelNum1, self.wheel1, res2)
        # print(res1, res2, res3)
        res4 = self.reflector[res3]
        # print(res4)

        res5 = self.backwardsWheelOutput(wheelNum1, self.wheel1, res4)

        res6 = self.backwardsWheelOutput(wheelNum2, self.wheel2, res5)

        res7 = (self.backwardsWheelOutput(wheelNum3, self.wheel3, res6))
        # print(res5, res6, res7)
        val = chr(res7 + 96)
        if val in self.mixLettersMap:
            return self.mixLettersMap[val]
        else:
            return chr(res7 + 96)

    def spinTheWheels(self, count):
        if count > 0:
            if (int(self.rotor3_input.text()) + count) > 26:
                self.rotor3_input.setValue(((int(self.rotor3_input.text()) + count) % 26))
                if int(self.rotor2_input.text()) == 26:
                    self.rotor2_input.setValue(1)
                    if int(self.rotor1_input.text()) == 26:
                        self.rotor1_input.setValue(1)
                    else:
                        self.rotor1_input.setValue(int(self.rotor1_input.text()) + 1)
                else:
                    self.rotor2_input.setValue(int(self.rotor2_input.text()) + 1)
            else:
                self.rotor3_input.setValue((int(self.rotor3_input.text()) + count))
        else:
            if (int(self.rotor3_input.text()) + count) < 1:
                self.rotor3_input.setValue(((int(self.rotor3_input.text()) + count) + 26))
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
        lastOutput = self.outputText[len(self.outputText)-1]
        button = self.keyboard_buttons[lastOutput]
        if button.text() in self.buttonsColors:
            button.setStyleSheet('background-color: ' + self.buttonsColors[lastOutput])
        else:
            button.setStyleSheet('')

        # for button in self.keyboard_buttons.values():
        #     button.setStyleSheet('')


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    gui = EnigmaGUI()
    app.exec_()

#
# import random
#
# def generate_random_map():
#     numbers = list(range(1, 27))
#     random.shuffle(numbers)
#     return {k: v for k, v in zip(range(1, 27), numbers)}
#
# my_map = generate_random_map()
# print(my_map)
