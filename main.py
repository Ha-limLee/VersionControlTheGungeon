from PySide6.QtWidgets import QApplication, QGridLayout, QVBoxLayout, QWidget
import sys
import asyncio

from src.ModSelecter import ModSelecter, ModSelecterBtn
from src.ModWriter import ModWriter
from src.ModFetcher import ModFetcher, ModFetcherBtn
from src.ModTable import ModTable, ModTableRefreshBtn
from src.ModUpdater import ModUpdater, ModUpdaterBtn
from src.ModUntracker import ModUntracker, ModUntrackerBtn
from src.EtgLauncher import EtgLauncher, EtgLauncherBtn
from src.EtgSelecter import EtgSelecter, EtgSelecterBtn


class MainFrame(QWidget):
    def __init__(self):
        super().__init__()
        self.table = ModTable()

        refreshBtn = ModTableRefreshBtn()
        refreshBtn.addTable(self.table)

        modSelecter = ModSelecter()
        modSelecterBtn = ModSelecterBtn()
        modSelecterBtn.addSelecter(modSelecter)
        modWriter = ModWriter()
        modSelecter.addObserver(modWriter)
        modWriter.addObserver(self.table)

        container = [] # holds response
        fetcherBtn = ModFetcherBtn()
        fetcher = ModFetcher()
        fetcher.addContainer(container)
        fetcherBtn.addModFetcher(fetcher)
        fetcher.addObserver(self.table)

        fetcher.addObserver(self.table)

        updatables = []
        self.table.addUpdatables(updatables)
        updaterBtn = ModUpdaterBtn()
        updater = ModUpdater()
        updaterBtn.addModUpdater(updater)
        updater.addUpdatables(updatables)
        updater.addTable(self.table)

        untracker = ModUntracker()
        untrackerBtn = ModUntrackerBtn()
        untrackerBtn.addUntracker(untracker)
        untracker.addTable(self.table)

        selecter = EtgSelecter()
        selecterBtn = EtgSelecterBtn()
        selecterBtn.addSelecter(selecter)

        launcher = EtgLauncher()
        launcherBtn = EtgLauncherBtn()
        launcherBtn.addLauncher(launcher)
        launcher.addSelecter(selecter)

        btnLayout = QVBoxLayout()
        btnLayout.addWidget(refreshBtn)
        btnLayout.addWidget(modSelecterBtn)
        btnLayout.addWidget(untrackerBtn)
        btnLayout.addWidget(fetcherBtn)
        btnLayout.addWidget(updaterBtn)
        btnLayout.addWidget(selecterBtn)
        btnLayout.addWidget(launcherBtn)

        layout = QGridLayout()
        layout.addWidget(self.table, 0, 0)
        layout.addLayout(btnLayout, 0, 1)

        self.setLayout(layout)


def run_window():
    from qasync import QEventLoop

    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    with loop:
        win = MainFrame()    
        win.show()
        loop.run_forever()

if __name__ == "__main__":
    run_window()