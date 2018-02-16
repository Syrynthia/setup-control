from PyQt5.QtWidgets import (QWidget, QDialog, QDialogButtonBox, QGridLayout, QGroupBox, QLabel, QMenu, QMenuBar,
                             QTextEdit,
                             QVBoxLayout, QAction, QApplication, QCheckBox, QHBoxLayout, QScrollArea, QMainWindow)
import ReadOdt
from PlotCanvas import PlotCanvas
from PyQt5.QtCore import Qt
from Preferences import PreferencesDialog
from tkinter import filedialog
from tkinter import Tk
from SinglePatient import SinglePatientWindow
import os
from os.path import isfile, join


class UiDialog(QDialog):
    #ates = ["Date", "Time", "Vrt", "Lng", "Lat", "Rtn"]
    #table = [[0] * 1 for i in range(0, 1)]
    tabR = 0
    tabC = 0
    vrt = []
    lng = []
    lat = []
    rtn = []
    vrt_error = []
    lng_error = []
    lat_error = []
    rtn_error = []
    toplot = [[], [], [], []]
    toplot_errors = [[], [], [], []]
    dates = []
    threshold = 0.3
    table = []
    mean_table = []
    std_table = []
    filenames = []

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


        multiPat = QMenu('Multiple Patients', self)
        chooseFiles = QAction('Choose multiple files', self)
        chooseFolder = QAction('Choose folder', self)
        multiPat.addAction(chooseFiles)
        multiPat.addAction(chooseFolder)
        chooseFiles.triggered.connect(self.choose_multi_patients)
        chooseFolder.triggered.connect(self.choose_dir_multi_patients)

        impMenu.addMenu(multiPat)

        impAct = QAction('Single Patient', self)
        # manAct = QAction('Multiple Patients', self)
        impMenu.addAction(impAct)
        impAct.triggered.connect(self.single_pat)

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

        #self.exitAction.triggered.connect(self.accept)

    def createGridGroupBox(self):
        self.resultFrame = QGroupBox("Data ")
        #self.frame_grid = QGridLayout()
        #self.data_print = QWidget()
        self.main_frame = QHBoxLayout()
        #self.data_print.setLayout(self.frame_grid)
        # resultLabel = QLabel(
        #     "Vrt\tLng\tLat\tRtn\tDate\tTime\tVrt (Moving Average)\tLng (Moving Average)\tLat (Moving Average)\tRtn (Moving Average)")
        # frameLayout.addWidget(resultLabel)
        self.resultFrame.setLayout(self.main_frame)

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
        #self.data_print = QWidget()
        #self.data_print.setMinimumWidth(400)
        # self.data_print.setFixedHeight(300)
        #QWidget().setLayout(self.frame_grid)
        data_print = QWidget()
        frame_grid = QGridLayout()
        QWidget().setLayout(self.main_frame)
        self.main_frame = QHBoxLayout()

        frame_grid.addWidget(QLabel("Filename"), 0, 0)
        frame_grid.addWidget(QLabel("Mean vrt"), 0, 1)
        frame_grid.addWidget(QLabel("Mean lng"), 0, 2)
        frame_grid.addWidget(QLabel("Mean lat"), 0, 3)
        frame_grid.addWidget(QLabel("Mean rtn"), 0, 4)

        for row in range(0, len(self.mean_table)):
            frame_grid.addWidget(QLabel(self.filenames[row]), row + 1, 0)
            for col in range(0, len(self.mean_table[row])):
                tmp = str(self.mean_table[row][col]) + u"\u00B1" + str(self.std_table[row][col])
                frame_grid.addWidget(QLabel(tmp), row + 1, col + 1)

        data_print.setLayout(frame_grid)

        scroll = QScrollArea()
        scroll.setWidget(data_print)

        self.main_frame.addWidget(scroll)
        self.resultFrame.setLayout(self.main_frame)


    def drawVrt(self, state):
            if state == Qt.Checked:
                self.toplot[0] = self.vrt
                self.toplot_errors[0] = self.vrt_error

                self.m.plot_checked_errors(self.toplot, self.toplot_errors, self.filenames)
            else:
                self.toplot[0] = []
                self.toplot_errors[0] = []

                self.m.plot_checked_errors(self.toplot, self.toplot_errors, self.filenames)

    def drawLng(self, state):
            if state == Qt.Checked:
                self.toplot[1] = self.lng
                self.toplot_errors[1] = self.lng_error

                self.m.plot_checked_errors(self.toplot, self.toplot_errors, self.filenames)
            else:
                self.toplot[1] = []
                self.toplot_errors[1] = []

                self.m.plot_checked_errors(self.toplot, self.toplot_errors, self.filenames)

    def drawLat(self, state):
            if state == Qt.Checked:
                self.toplot[2] = self.lat
                self.toplot_errors[2] = self.lat_error

                self.m.plot_checked_errors(self.toplot, self.toplot_errors, self.filenames)
            else:
                self.toplot[2] = []
                self.toplot_errors[2] = []

                self.m.plot_checked_errors(self.toplot, self.toplot_errors, self.filenames)

    def drawRtn(self, state):
            if state == Qt.Checked:
                self.toplot[3] = self.rtn
                self.toplot_errors[3] = self.rtn_error

                self.m.plot_checked_errors(self.toplot, self.toplot_errors, self.filenames)
            else:
                self.toplot[3] = []
                self.toplot_errors[3] = []

                self.m.plot_checked_errors(self.toplot, self.toplot_errors, self.filenames)

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
            self.files_to_table(filez)
            self.fillTable()

    def choose_dir_multi_patients(self):
        root = Tk()
        root.withdraw()
        directory = filedialog.askdirectory(parent=root)
        files = [f for f in os.listdir(directory) if isfile(join(directory, f))]
        filez = [directory + "/" + f for f in files]
        if filez:
            self.files_to_table(filez)
            self.fillTable()

    def files_to_table(self, filez):
        self.table.clear()
        self.filenames.clear()
        self.mean_table.clear()
        self.std_table.clear()
        for file in filez:
            self.table.append(ReadOdt.read_table(file, self.threshold)[2])
            self.filenames.append(os.path.split(file)[1])

        for i in range(0, len(self.table)):
            tmp = ReadOdt.calculate_avg_stdev(self.table[i])
            self.mean_table.append(tmp[0])
            self.std_table.append(tmp[1])

        self.tables_to_separate()

    def tables_to_separate(self):
        self.vrt.clear()
        self.lng.clear()
        self.lat.clear()
        self.rtn.clear()

        self.vrt_error.clear()
        self.lng_error.clear()
        self.lat_error.clear()
        self.rtn_error.clear()

        for row in self.mean_table:
            self.vrt.append(row[0])
            self.lng.append(row[1])
            self.lat.append(row[2])
            self.rtn.append(row[3])

        for row in self.std_table:
            self.vrt_error.append(row[0])
            self.lng_error.append(row[1])
            self.lat_error.append(row[2])
            self.rtn_error.append(row[3])

    def single_pat(self):
        root = Tk()
        root.withdraw()
        file = filedialog.askopenfilename(parent=root, filetypes=(("ODT files", "*.odt"), ("All files", "*")))

        if file:
            self.widget = SinglePatientWindow(file, self.threshold)
            self.widget.show()
