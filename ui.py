from PyQt5.QtWidgets import (QWidget, QDialog, QDialogButtonBox, QGridLayout, QGroupBox, QLabel, QMenu, QMenuBar,
                             QTextEdit,
                             QVBoxLayout, QAction, QApplication, QCheckBox)
from ReadOdt import read_odt
from PlotCanvas import PlotCanvas
from PyQt5.QtCore import Qt
from Preferences import PreferencesDialog
from tkinter import filedialog
from tkinter import Tk
from MultiplePatients import MultiPatientsDialog
from os import listdir
from os.path import isfile, join



class UiDialog(QDialog):
    dates = ["Date", "Time", "Vrt", "Lng", "Lat", "Rtn"]
    table = [[0] * 1 for i in range(0, 1)]
    tabR = 0
    tabC = 0
    vrt = []
    lng = []
    lat = []
    rtn = []
    toplot = [[], [], [], []]
    dates = []
    threshold = 0.3

    def __init__(self):
        super(UiDialog, self).__init__()
        self.createMenu()
        self.createGridGroupBox()
        self.createPlotFrame()

        mainLayout = QVBoxLayout()
        mainLayout.setMenuBar(self.menuBar)
        mainLayout.addWidget(self.resultFrame)
        # mainLayout.addWidget(bigEditor)
        # mainLayout.addWidget(buttonBox)


        # mainLayout.addWidget(self.m)
        mainLayout.addWidget(self.plotFrame)

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
        impAct = QAction('Single Patient', self)
        #manAct = QAction('Multiple Patients', self)
        impMenu.addAction(impAct)
        impAct.triggered.connect(lambda: self.fillTable())

        multiPat = QMenu('Multiple Patients', self)
        chooseFiles = QAction('Choose multiple files', self)
        chooseFolder = QAction('Choose folder', self)
        multiPat.addAction(chooseFiles)
        multiPat.addAction(chooseFolder)
        chooseFiles.triggered.connect(self.choose_multi_patients)
        chooseFolder.triggered.connect(self.choose_dir_multi_patients)

        impMenu.addMenu(multiPat)
        #impMenu.addAction(manAct)
        self.fileMenu.addMenu(impMenu)
        # self.saveAction = self.fileMenu.addAction("&Save")
        saveMenu = QMenu('Save As...', self)
        pdfAct = QAction('.odt file', self)
        csvAct = QAction('.csv file', self)
        saveMenu.addAction(pdfAct)
        saveMenu.addAction(csvAct)
        self.fileMenu.addMenu(saveMenu)
        self.fileMenu.addAction(QAction('Help', self))
        self.exitAction = self.fileMenu.addAction("E&xit")

        self.menuBar.addMenu(self.fileMenu)

        self.edit_menu = QMenu("&Edit", self)
        pref_act = QAction("Preferences", self)
        pref_act.triggered.connect(self.preferences)
        self.edit_menu.addAction(pref_act)

        self.menuBar.addMenu(self.edit_menu)

        self.exitAction.triggered.connect(self.accept)

    def createGridGroupBox(self):
        self.resultFrame = QGroupBox("Data ")
        self.frameLayout = QGridLayout()
        # resultLabel = QLabel(
        #     "Vrt\tLng\tLat\tRtn\tDate\tTime\tVrt (Moving Average)\tLng (Moving Average)\tLat (Moving Average)\tRtn (Moving Average)")
        # frameLayout.addWidget(resultLabel)
        self.resultFrame.setLayout(self.frameLayout)

    def createPlotFrame(self):
        self.plotFrame = QGroupBox(" ")
        self.plotFrame.setStyleSheet("border:0;")
        self.plotLayout = QGridLayout()
        self.m = PlotCanvas(self, width=7, height=5)
        self.plotLayout.addWidget(self.m, 0, 0)

        self.checkboxes = QGroupBox("")
        self.checkboxes.setStyleSheet("border:0;")
        self.checkboxesLayout = QVBoxLayout()

        self.cbVrt = QCheckBox('Vertical', self)
        self.cbVrt.stateChanged.connect(self.drawVrt)
        cbLng = QCheckBox('Longitudinal', self)
        cbLng.stateChanged.connect(self.drawLng)
        cbLat = QCheckBox('Latitudinal', self)
        cbLat.stateChanged.connect(self.drawLat)
        cbRtn = QCheckBox('Rotational', self)
        cbRtn.stateChanged.connect(self.drawRtn)

        self.checkboxesLayout.addWidget(self.cbVrt)
        self.checkboxesLayout.addWidget(cbLng)
        self.checkboxesLayout.addWidget(cbLat)
        self.checkboxesLayout.addWidget(cbRtn)
        self.checkboxes.setLayout(self.checkboxesLayout)

        self.plotLayout.addWidget(self.checkboxes, 0, 1)
        self.plotFrame.setLayout(self.plotLayout)

    def fillTable(self):
        stuff = read_odt(self.threshold)
        self.tabR = stuff[0]
        self.tabC = stuff[1]
        self.table = stuff[2]
        QWidget().setLayout(self.frameLayout)
        self.frameLayout = QGridLayout(self)
        self.vrt.clear()
        self.lng.clear()
        self.lat.clear()
        self.rtn.clear()
        self.dates.clear()
        for row in range(0, self.tabR):
            if row > 2:
                try:
                    vr = float(self.table[row][0])
                    self.vrt.append(vr)
                except ValueError:
                    pass
                try:
                    ln = float(self.table[row][1])
                    self.lng.append(ln)
                except ValueError:
                    pass
                try:
                    la = float(self.table[row][2])
                    self.lat.append(la)
                except ValueError:
                    pass
                try:
                    rt = float(self.table[row][3])
                    self.rtn.append(rt)
                except ValueError:
                    pass
                self.dates.append(self.table[row][4])
            for col in range(0, self.tabC):
                self.frameLayout.addWidget(QLabel(str(self.table[row][col])), row, col)
                # print(self.table[row][col])

        self.resultFrame.setLayout(self.frameLayout)
        self.cbVrt.toggle()
        if not self.cbVrt.checkState():
            self.cbVrt.toggle()

    def drawVrt(self, state):
            if state == Qt.Checked:
                self.toplot[0] = self.vrt
                self.m.plotChecked(self.toplot, self.dates)
            else:
                self.toplot[0] = []
                self.m.plotChecked(self.toplot, self.dates)

    def drawLng(self, state):
            if state == Qt.Checked:
                self.toplot[1] = self.lng
                self.m.plotChecked(self.toplot, self.dates)
            else:
                self.toplot[1] = []
                self.m.plotChecked(self.toplot, self.dates)

    def drawLat(self, state):
            if state == Qt.Checked:
                self.toplot[2] = self.lat
                self.m.plotChecked(self.toplot, self.dates)
            else:
                self.toplot[2] = []
                self.m.plotChecked(self.toplot, self.dates)

    def drawRtn(self, state):
            if state == Qt.Checked:
                self.toplot[3] = self.rtn
                self.m.plotChecked(self.toplot, self.dates)
            else:
                self.toplot[3] = []
                self.m.plotChecked(self.toplot, self.dates)

    def change_thresh(self, value):
        self.threshold = value

    def preferences(self):
        widget = PreferencesDialog(self.threshold)
        widget.exec_()
        self.threshold = widget.get_threshold()
        print(self.threshold)

    def choose_multi_patients(self):
        root = Tk()
        root.withdraw()
        filez = filedialog.askopenfilenames(parent=root, filetypes=(("ODT files", "*.odt"), ("All files", "*")))
        if filez:
            widget = MultiPatientsDialog(filez, self.threshold)
            widget.exec_()

    def choose_dir_multi_patients(self):
        root = Tk()
        root.withdraw()
        directory = filedialog.askdirectory(parent=root)
        files = [f for f in listdir(directory) if isfile(join(directory, f))]
        filez = [directory + "/" + f for f in files]
        if filez:
            widget = MultiPatientsDialog(filez, self.threshold)
            widget.exec_()
