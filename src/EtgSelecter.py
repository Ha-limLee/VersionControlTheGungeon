from PySide6.QtWidgets import QGridLayout, QPushButton, QWidget, QFileDialog, QMessageBox
import os
import json

class EtgSelecter:
    def __init__(self):
        if not os.path.isfile('vctg-config.json'):
            data = {
                "etgPath": ""
            }
            file = open('vctg-config.json', 'w')
            json.dump(data, file)
            file.close()
        pass
    
    def select(self):
        file = open('vctg-config.json')

        data: dict = json.load(file)

        file.close()

        fileDir:str = QFileDialog.getOpenFileName()[0]

        if fileDir.find('EtG'):
            file = open('vctg-config.json', 'w')
            data['etgPath'] = fileDir
            json.dump(data, file, indent=4)
            file.close()

class EtgSelecterBtn(QWidget):
    def __init__(self):
        super().__init__()

        self.btn = QPushButton('Select etg')
        self.etgSelecter: EtgSelecter = None

        layout = QGridLayout()
        layout.addWidget(self.btn)

        self.setLayout(layout)

        self.btn.clicked.connect(self.select)

    def addSelecter(self, selecter):
        self.etgSelecter = selecter
    
    def select(self):
        self.etgSelecter.select()