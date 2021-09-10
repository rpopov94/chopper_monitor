from PyQt5 import QtWidgets, uic, QtCore
from status import Ui_STATUS_CHOPPER
from smclib import *


class CH_Monitor(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        # загрузка с ui
        # self.w_root = uic.loadUi('status.ui')
        # self.w_root.show()
        # Загрузка с *.py
        self.w_root = Ui_STATUS_CHOPPER()
        self.w_root.setupUi(self)
        # установка параметров подключения
        self.w_root.block_combo.addItems(block_list)
        self.w_root.comList.addItems(serial_ports())
        # ссылка на timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.setdata)
        # кнопки
        self.w_root.pushButton_6.clicked.connect(self.send)
        self.w_root.pushButton.clicked.connect(self.connOn)
        self.w_root.pushButton_2.clicked.connect(self.connOff)
        self.w_root.pushButton_22.clicked.connect(self.UIStop)
        self.w_root.pushButton_22.clicked.connect(self.UIStop)
        self.w_root.pushButton_23.clicked.connect(self.UIRun)

    def send(self):
        '''ответ контроллера'''
        self.w_root.plainTextEdit_5.setPlainText("")
        cmd = 'W' if self.w_root.ch_RorW.isChecked() else 'R'
        data = self.w_root.plainTextEdit_3.toPlainText().rstrip()
        block = self.w_root.block_combo.currentText()
        register = self.w_root.plainTextEdit_2.toPlainText().rstrip()
        if data == '' or block == '' or register == '':
            self.w_root.plainTextEdit_5.setPlainText('Введите недостающие параметры!')
        else:
            req = command(int(block), int(register), cmd, int(data))
            req = strconvert(req)
            self.w_root.plainTextEdit_4.setPlainText(req)

    def connOn(self):
        # print('connOn')
        ch_connect(str(self.w_root.comList.currentText()))
        self.w_root.plainTextEdit_5.appendPlainText('Редактирование регистров')
        self.w_root.pushButton_2.setEnabled(True)
        self.w_root.pushButton.setEnabled(False)
        self.w_root.pushButton_6.setEnabled(True)

    def connOff(self):
        ch_disconnect()
        self.w_root.plainTextEdit_5.appendPlainText(f"")
        self.w_root.plainTextEdit_5.setPlainText("COM - порт отключен!")
        self.w_root.pushButton_2.setEnabled(False)
        self.w_root.pushButton.setEnabled(True)
        self.w_root.pushButton_6.setDisabled(True)

    def clearData(self):
        '''
        очистить данные окна онлайн параметров
        '''
        self.w_root.plainTextEdit_5.setPlainText("")
        self.w_root.label_28.setText('')
        self.w_root.label_30.setText('')
        self.w_root.label_32.setText('')
        self.w_root.label_34.setText('')
        self.w_root.label_36.setText('')
        self.w_root.label_38.setText('')
        self.w_root.label_40.setText('')
        self.w_root.label_41.setText('')

    def online(self):
        block = self.w_root.block_combo.currentText()
        resp = online_parameters(block)
        self.w_root.label_28.setText(resp['f'])
        self.w_root.label_30.setText(resp['ts'])
        self.w_root.label_32.setText(resp['tp'])
        self.w_root.label_34.setText(resp['pst'])
        self.w_root.label_36.setText(resp['win'])
        self.w_root.label_38.setText(resp['ps'])
        self.w_root.label_40.setText(resp['psel'])
        self.w_root.label_41.setText(resp['ppst'])

    def UIRun(self):
        # print('UIRun')
        # print('start ui')
        self.w_root.plainTextEdit_5.appendPlainText(f"")
        if self.timer.isActive():
            self.w_root.plainTextEdit_5.appendPlainText(f"Timer запущен!")
        else:
            self.timer.start(5000)
            self.w_root.pushButton_23.setDisabled(True)
            self.w_root.pushButton.setDisabled(True)
            self.w_root.pushButton_2.setDisabled(True)
            self.w_root.pushButton_6.setDisabled(True)

    def UIStop(self):
        # print('UIStop')
        # print('stop ui')
        if self.timer.isActive():
            self.timer.stop()
        self.w_root.pushButton_23.setEnabled(True)
        self.w_root.pushButton.setEnabled(True)
        self.w_root.pushButton_2.setEnabled(True)
        self.w_root.pushButton_6.setEnabled(True)
        # self.w_root.l_about.setText(f'')
        self.w_root.plainTextEdit_5.setPlainText("")
        self.w_root.pushButton_6.setDisabled(False)
        self.clearUI()
        self.clearData()

    def setdata(self):
        '''
        Set current data
        '''
        self.clearUI()
        self.clearData()
        bl = str(self.w_root.block_combo.currentText())
        try:
            rep = reply(bl)
            self.w_root.plainTextEdit_5.appendPlainText(f'Включен режим мониторинга блока {bl}')
            if rep['firstbit'] == '1':
                self.w_root.l_first.setStyleSheet('border: 2px solid red;')
            if rep['twobit'] == '1':
                self.w_root.l_second.setStyleSheet('border: 2px solid red')
            if rep['threebit'] == '1':
                self.w_root.l_three.setStyleSheet('border: 2px solid red')
            if rep['fourbit'] == '1':
                self.w_root.l_four.setStyleSheet('border: 2px solid red')
            if rep['fivebit'] == '1':
                self.w_root.l_five.setStyleSheet('border: 2px solid red')
            if rep['sixbit'] == '1':
                self.w_root.l_six.setStyleSheet('border: 2px solid red')
            if rep['sevenbit'] == '1':
                self.w_root.l_seven.setStyleSheet('border: 2px solid red')
            if rep['eightbit'] == '1':
                self.w_root.l_eight.setStyleSheet('border: 2px solid red')
            if rep['ninebit'] == '1':
                self.w_root.l_nine.setStyleSheet('border: 2px solid red')
            if rep['tenbit'] == '1':
                self.w_root.l_ten.setStyleSheet('border: 2px solid red')
            if rep['elevenbit'] == '1':
                self.w_root.l_eleven.setStyleSheet('border: 2px solid red')
            if rep['twentybit'] == '1':
                self.w_root.l_twenty.setStyleSheet('border: 2px solid red')
            if rep['thirtybit'] == '1':
                self.w_root.l_threteen.setStyleSheet('border: 2px solid red')
            if rep['fourteenbit'] == '1':
                self.w_root.l_fourteen.setStyleSheet('border: 2px solid red')
            if rep['fifteenbit'] == '1':
                self.w_root.l_fifteen.setStyleSheet('border: 2px solid red')
            if rep['sixteenbit'] == '1':
                self.w_root.l_sixteen.setStyleSheet('border: 2px solid red')
            self.online()
        except:
            self.UIStop()
            self.w_root.plainTextEdit_5.setPlainText("Произошла непридвиденная ошибка, "
                                                        "COM - порт внезапно отлючился.")
    def clearUI(self):
        '''
        reset interface
        '''
        self.w_root.l_first.setStyleSheet('border: 2px solid black;\nbackground: white')
        self.w_root.l_second.setStyleSheet('border: 2px solid black;\nbackground: white')
        self.w_root.l_three.setStyleSheet('border: 2px solid black;\nbackground: white')
        self.w_root.l_four.setStyleSheet('border: 2px solid black;\nbackground: white')
        self.w_root.l_five.setStyleSheet('border: 2px solid black;\nbackground: white')
        self.w_root.l_six.setStyleSheet('border: 2px solid black;\nbackground: white')
        self.w_root.l_seven.setStyleSheet('border: 2px solid black;\nbackground: white')
        self.w_root.l_eight.setStyleSheet('border: 2px solid black;\nbackground: white')
        self.w_root.l_nine.setStyleSheet('border: 2px solid black;\nbackground: white')
        self.w_root.l_ten.setStyleSheet('border: 2px solid black;\nbackground: white')
        self.w_root.l_eleven.setStyleSheet('border: 2px solid black;\nbackground: white')
        self.w_root.l_twenty.setStyleSheet('border: 2px solid black;\nbackground: white')
        self.w_root.l_threteen.setStyleSheet('border: 2px solid black;\nbackground: white')
        self.w_root.l_fourteen.setStyleSheet('border: 2px solid black;\nbackground: white')
        self.w_root.l_fifteen.setStyleSheet('border: 2px solid black;\nbackground: white')
        self.w_root.l_sixteen.setStyleSheet('border: 2px solid black;\nbackground: white')

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication([])
    # закоментировать 2 последующие строки при загрузке с ui
    application = CH_Monitor()
    application.show()
    sys.exit(app.exec())
