from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QFileDialog

class ModSelecter:
    '''
    select mod to track
    '''
    def __init__(self):
        self.observers = []

    def addObserver(self, observer):
        if not observer in self.observers:
            self.observers.append(observer)

    def notify(self, data):
        for each in self.observers:
            each.update(data)

    @staticmethod
    def parseMod(mod_dir):
        '''
        parse mod file <name>.zip
        e.g. 24520_PunchoutAnywhereMod_1.1.zip
        mod id: 24520
        mod name: PunchoutAnywhereMod
        '''
        result = {
            'id': '',
            'name': '',
            'version': '',
            'date': '',
            'path': ''
            }

        result['path'] = mod_dir
        fileName= mod_dir.split('/')[-1].replace('.zip', '')
        
        fileSplit = fileName.split('_')
        result['id'] = fileSplit[0]
        result['name'] = fileSplit[1]

        try: # some mods has no version
            result['version'] = fileSplit[2]
        except:
            pass
        
        return result

    def getModNames(self):
        file_dirs = QFileDialog.getOpenFileNames()
        parsed = map(lambda x: ModSelecter.parseMod(x), file_dirs[0])
        parsedList = list(parsed)
        print(parsedList)
        self.notify(parsedList)

class ModSelecterBtn(QWidget):
    def __init__(self):
        super().__init__()
        self.selecter: ModSelecter = None
        self.btn = QPushButton('Select mods')

        layout = QGridLayout()
        layout.addWidget(self.btn)

        self.setLayout(layout)
        self.btn.clicked.connect(self.getModNames)

    def addSelecter(self, selecter: ModSelecter):
        self.selecter = selecter

    def getModNames(self):
        self.selecter.getModNames()
