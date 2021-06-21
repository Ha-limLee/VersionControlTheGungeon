from PySide6.QtWidgets import QFileDialog, QGridLayout, QMessageBox, QWidget, QPushButton
import subprocess
import json

from .EtgSelecter import EtgSelecter

class EtgLauncher:
    def __init__(self):
        self.selecter: EtgSelecter = None
        pass

    def addSelecter(self, selecter):
        self.selecter = selecter

    def getPath(self) -> str:
        file = open('vctg-config.json')
        
        data: dict = json.load(file)

        path = data['etgPath']

        file.close()
        
        return path
    
    def launch(self):
        path = self.getPath()
        if not path:
            self.selecter.select()
            path = self.getPath()

        if path:
            path = path.replace('/', '\\\\', 1).replace('/', '\\')
            subprocess.Popen(path)
    pass

class EtgLauncherBtn(QWidget):
    def __init__(self):
        super().__init__()

        self.btn = QPushButton('Launch')
        self.launcher: EtgLauncher = None

        layout = QGridLayout()
        layout.addWidget(self.btn)
        self.setLayout(layout)

        self.btn.clicked.connect(self.launch)

    def addLauncher(self, launcher):
        self.launcher = launcher
    
    def launch(self):
        self.launcher.launch()
