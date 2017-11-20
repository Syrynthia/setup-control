from PyQt5.QtWidgets import (QWidget, QDialog, QDialogButtonBox, QGridLayout, QGroupBox, QLabel, QMenu, QMenuBar, QTextEdit,
                             QVBoxLayout, QAction, QApplication)
from ReadOdt import readOdt
from PlotCanvas import PlotCanvas

class UiDialog(QDialog):
    labels = ["Date", "Time", "Vrt", "Lng", "Lat", "Rtn"]
    table = [[0] * 1 for i in range(0, 1)]
    tabR = 0
    tabC = 0

    def __init__(self):
        super(UiDialog, self).__init__()
        self.createMenu()
        self.createGridGroupBox()

        bigEditor = QTextEdit()
        bigEditor.setPlainText("Here is where the plot of moving averages will be")

        buttonBox = QDialogButtonBox(QDialogButtonBox.Close)

        mainLayout = QVBoxLayout()
        mainLayout.setMenuBar(self.menuBar)
        mainLayout.addWidget(self.resultFrame)
        #mainLayout.addWidget(bigEditor)
        #mainLayout.addWidget(buttonBox)

        self.m = PlotCanvas(self, width=5, height=4)
        mainLayout.addWidget(self.m)

        self.setLayout(mainLayout)

        self.setWindowTitle("Setup control")

    def createMenu(self):
        self.menuBar = QMenuBar()

        self.fileMenu = QMenu("&File", self)
        # self.openAct = self.fileMenu.addAction(self,QAction("&Open...", self, shortcut=QKeySequence.Open,
        # statusTip="Open an existing file", triggered=self.open))
        # self.saveAct = self.fileMenu.addAction(self,QAction("&Save", self, shortcut=QKeySequence.Save,
        # statusTip="Save the document to disk", triggered=self.save))
        impMenu = QMenu('Import', self)
        impAct = QAction('Import from file', self)
        manAct = QAction('Add data points manually', self)
        impMenu.addAction(impAct)
        #impAct.triggered.connect(lambda: readOdt(self.tabR, self.tabC, self.table))
        impAct.triggered.connect(lambda: self.fillTable())
        impMenu.addAction(manAct)
        self.fileMenu.addMenu(impMenu)
        #self.saveAction = self.fileMenu.addAction("&Save")
        saveMenu = QMenu('Save As...',self)
        pdfAct = QAction('.odt file', self)
        csvAct = QAction('.csv file', self)
        saveMenu.addAction(pdfAct)
        saveMenu.addAction(csvAct)
        self.fileMenu.addMenu(saveMenu)
        self.exitAction = self.fileMenu.addAction("E&xit")

        self.menuBar.addMenu(self.fileMenu)

        self.exitAction.triggered.connect(self.accept)

    def createGridGroupBox(self):
        self.resultFrame = QGroupBox("Data ")
        self.frameLayout = QGridLayout()
        # resultLabel = QLabel(
        #     "Vrt\tLng\tLat\tRtn\tDate\tTime\tVrt (Moving Average)\tLng (Moving Average)\tLat (Moving Average)\tRtn (Moving Average)")
        # frameLayout.addWidget(resultLabel)
        self.resultFrame.setLayout(self.frameLayout)
    def fillTable(self):
        stuff = readOdt()
        self.tabR = stuff[0]
        self.tabC = stuff[1]
        self.table = stuff[2]
        QWidget().setLayout(self.frameLayout)
        self.frameLayout = QGridLayout(self)
        for row in range(0, self.tabR):
            for col in range(0, self.tabC):
                self.frameLayout.addWidget(QLabel(str(self.table[row][col])), row, col)
                #print(self.table[row][col])


        self.resultFrame.setLayout(self.frameLayout)
        self.m.plot()
        #self.gridGroupBox.layout().addWidget(self.resultFrame)