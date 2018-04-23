import csv
import os
from os.path import isfile, join
from tkinter import Tk
from tkinter import filedialog
import numpy as np

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (QWidget, QDialog, QGridLayout, QGroupBox, QLabel, QMenu, QMenuBar,
                             QVBoxLayout, QAction, QCheckBox, QHBoxLayout, QScrollArea)

import ReadOdt
from HelpWindow import HelpWindow
from PlotCanvas import PlotCanvas
from Preferences import PreferencesDialog
from SinglePatient import SinglePatientWindow


# class containing the main dialog
class UiDialog(QDialog):
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
    correction_sessions = 3
    mean_sessions = 0
    table = []
    mean_table = []
    std_table = []
    filenames = []
    filez = []
    population_bias_mean = []
    population_bias_std = []
    population_mean = []

    # initialisation - this cretes the dialog with empty franes and plot
    def __init__(self):
        super(UiDialog, self).__init__()
        self.createMenu()
        self.createGridGroupBox()
        self.createPlotFrame()
        self.create_pop_box()

        mainLayout = QVBoxLayout()
        mainLayout.setMenuBar(self.menuBar)
        mainLayout.addWidget(self.resultFrame)
        mainLayout.addWidget(self.pop_frame)
        mainLayout.addWidget(self.plotFrame)

        self.setLayout(mainLayout)

        self.setWindowTitle("Setup control")

    # method creating the menu bar and assiging actions and shortcuts to menu items
    def createMenu(self):
        self.menuBar = QMenuBar()

        self.fileMenu = QMenu("&File", self)

        impMenu = QMenu('Import', self)

        multiPat = QMenu('Multiple Patients', self)
        chooseFiles = QAction('Choose multiple files', self, shortcut=QKeySequence("Ctrl+O"))
        chooseFolder = QAction('Choose folder', self, shortcut=QKeySequence("Ctrl+F"))
        multiPat.addAction(chooseFiles)
        multiPat.addAction(chooseFolder)
        chooseFiles.triggered.connect(self.choose_multi_patients)
        chooseFolder.triggered.connect(self.choose_dir_multi_patients)

        impMenu.addMenu(multiPat)

        impAct = QAction('Single Patient', self, shortcut=QKeySequence("Ctrl+A"))
        impMenu.addAction(impAct)
        impAct.triggered.connect(self.single_pat)

        self.fileMenu.addMenu(impMenu)

        saveMenu = QMenu('Save...', self)
        pdfAct = QAction('plot', self, shortcut=QKeySequence("Ctrl+L"))
        csvAct = QAction('data to a .csv file', self, shortcut=QKeySequence("Ctrl+S"))
        csvAct.triggered.connect(self.save_csv)
        pdfAct.triggered.connect(self.save_plot)

        saveMenu.addAction(csvAct)
        saveMenu.addAction(pdfAct)
        self.fileMenu.addMenu(saveMenu)

        help_act = QAction('Help', self, shortcut=QKeySequence("Ctrl+H"))
        help_act.triggered.connect(self.help)
        self.fileMenu.addAction(help_act)
        self.exitAction = self.fileMenu.addAction("E&xit")

        self.menuBar.addMenu(self.fileMenu)

        self.edit_menu = QMenu("&Edit", self)
        pref_act = QAction("Preferences", self, shortcut=QKeySequence("Ctrl+P"))
        pref_act.triggered.connect(self.preferences)
        self.edit_menu.addAction(pref_act)

        self.menuBar.addMenu(self.edit_menu)

        self.exitAction.triggered.connect(self.accept)

    # method creating an empty frame to be filled with averages and standard deviations from each file
    def createGridGroupBox(self):
        self.resultFrame = QGroupBox("Data ")
        self.resultFrame.setMinimumHeight(200)
        self.main_frame = QHBoxLayout()
        self.resultFrame.setLayout(self.main_frame)

    # method creating an empty frame to be filled with population error data
    def create_pop_box(self):
        self.pop_frame = QGroupBox("Population error")
        self.pop_frame.setMinimumHeight(100)
        self.pop_layout = QHBoxLayout()
        self.pop_frame.setLayout(self.pop_layout)

    # method creating the frame containing an empty plot and the checkboxes
    def createPlotFrame(self):
        self.plotFrame = QGroupBox(" ")
        self.plotFrame.setMinimumHeight(500)
        self.plotFrame.setStyleSheet("border:0;")
        self.plotLayout = QGridLayout()
        self.m = PlotCanvas(self, width=7, height=6)
        self.plotLayout.addWidget(self.m, 0, 0)

        self.checkboxes = QGroupBox("")
        self.checkboxes.setStyleSheet("border:0;")
        self.checkboxesLayout = QVBoxLayout()

        self.cbVrt = QCheckBox('Vertical', self)
        self.cbVrt.stateChanged.connect(self.drawVrt)
        cbLng = QCheckBox('Longitudinal', self)
        cbLng.stateChanged.connect(self.drawLng)
        cbLat = QCheckBox('Latertal', self)
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

    # method filling the Data frame with means and standard deviations from each file
    def fillTable(self):
        data_print = QWidget()
        frame_grid = QGridLayout()
        QWidget().setLayout(self.main_frame)
        self.main_frame = QHBoxLayout()

        frame_grid.addWidget(QLabel("Filename"), 0, 0)
        frame_grid.addWidget(QLabel("Mean vrt [cm]"), 0, 1)
        frame_grid.addWidget(QLabel("Mean lng [cm]"), 0, 2)
        frame_grid.addWidget(QLabel("Mean lat [cm]"), 0, 3)
        frame_grid.addWidget(QLabel("Mean rtn [cm]"), 0, 4)

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

    # method filling the Population Error frame with analysed data
    def fill_pop(self):
        data_print = QWidget()
        frame_grid = QGridLayout()
        QWidget().setLayout(self.pop_layout)
        self.pop_layout = QHBoxLayout()

        frame_grid.addWidget(QLabel(" "), 0, 0)
        frame_grid.addWidget(QLabel("Vertical [cm]"), 0, 1)
        frame_grid.addWidget(QLabel("Longitudinal [cm]"), 0, 2)
        frame_grid.addWidget(QLabel("Lateral [cm]"), 0, 3)
        frame_grid.addWidget(QLabel("Rotational [cm]"), 0, 4)

        frame_grid.addWidget(QLabel("Systematic error"), 1, 0)
        i = 1
        for val in self.population_bias_mean:
            string = str(val)
            if string == '-0.0':
                string = string.replace("-", "")
            frame_grid.addWidget(QLabel(string + u"\u00B1" + str(self.population_bias_std[i - 1])), 1, i)
            i += 1

        frame_grid.addWidget(QLabel("Random error"), 2, 0)
        i = 1
        for val in self.population_mean:
            frame_grid.addWidget(QLabel(str(val)), 2, i)
            i += 1

        data_print.setLayout(frame_grid)

        self.pop_layout.addWidget(data_print)
        self.pop_frame.setLayout(self.pop_layout)

    # method adding the Vrt data to the plot
    def drawVrt(self, state):
        if state == Qt.Checked:
            self.toplot[0] = self.vrt
            self.toplot_errors[0] = self.vrt_error

            self.m.plot_checked_errors(self.toplot, self.toplot_errors, self.filenames)
        else:
            self.toplot[0] = []
            self.toplot_errors[0] = []

            self.m.plot_checked_errors(self.toplot, self.toplot_errors, self.filenames)

    # method adding the Lng data to the plot
    def drawLng(self, state):
        if state == Qt.Checked:
            self.toplot[1] = self.lng
            self.toplot_errors[1] = self.lng_error

            self.m.plot_checked_errors(self.toplot, self.toplot_errors, self.filenames)
        else:
            self.toplot[1] = []
            self.toplot_errors[1] = []

            self.m.plot_checked_errors(self.toplot, self.toplot_errors, self.filenames)

    # method adding the Lat data to the plot
    def drawLat(self, state):
        if state == Qt.Checked:
            self.toplot[2] = self.lat
            self.toplot_errors[2] = self.lat_error

            self.m.plot_checked_errors(self.toplot, self.toplot_errors, self.filenames)
        else:
            self.toplot[2] = []
            self.toplot_errors[2] = []

            self.m.plot_checked_errors(self.toplot, self.toplot_errors, self.filenames)

    # method adding the Rtn data to the plot
    def drawRtn(self, state):
        if state == Qt.Checked:
            self.toplot[3] = self.rtn
            self.toplot_errors[3] = self.rtn_error

            self.m.plot_checked_errors(self.toplot, self.toplot_errors, self.filenames)
        else:
            self.toplot[3] = []
            self.toplot_errors[3] = []

            self.m.plot_checked_errors(self.toplot, self.toplot_errors, self.filenames)

    # method changing the threshold value
    def change_thresh(self, value):
        self.threshold = value

    # method opening the preferences dialog and saving all the changes afterwards
    def preferences(self):
        widget = PreferencesDialog(self.threshold, self.correction_sessions, self.mean_sessions)
        widget.exec_()
        self.threshold = widget.get_threshold()
        self.correction_sessions = widget.get_correction_sessions()
        self.mean_sessions = widget.get_mean_sessions()

        self.files_to_table()
        self.fillTable()

    # methond for opening a file choice dialog and filling the dialog with data afterwards
    def choose_multi_patients(self):
        root = Tk()
        root.withdraw()
        tmpfilez = filedialog.askopenfilenames(parent=root, filetypes=(("ODT files", "*.odt"),
                                                                       ("DOCX files", "*.docx"),
                                                                       ("All files", "*")))
        if tmpfilez:
            self.filez = tmpfilez
            self.files_to_table()
            self.fillTable()
            self.fill_pop()

    # methond for opening a directory choice dialog and filling the dialog with data afterwards
    def choose_dir_multi_patients(self):
        root = Tk()
        root.withdraw()
        directory = filedialog.askdirectory(parent=root)
        if directory:
            files = [f for f in os.listdir(directory) if isfile(join(directory, f))]
            tmpfilez = [directory + "/" + f for f in files]
            if tmpfilez:
                self.filez = tmpfilez
                self.files_to_table()
                self.fillTable()
                self.fill_pop()

    # method that reads each file, calculates the data and puts it in lists
    def files_to_table(self):
        self.table.clear()
        self.filenames.clear()
        self.mean_table.clear()
        self.std_table.clear()
        for file in self.filez:
            if file.endswith('.odt') and '~' not in file:
                tmp = ReadOdt.read_table(file, self.threshold, self.correction_sessions)[2]
                if tmp:
                    self.table.append(tmp)
                    self.filenames.append(os.path.split(file)[1])
            elif file.endswith('.docx') and '~' not in file:
                tmp = ReadOdt.read_docx(file, self.threshold, self.correction_sessions)[2]
                if tmp:
                    self.table.append(tmp)
                    self.filenames.append(os.path.split(file)[1])

        for i in range(0, len(self.table)):
            tmp = ReadOdt.calculate_avg_stdev(self.table[i], self.mean_sessions)

            self.mean_table.append(tmp[0])
            self.std_table.append(tmp[1])

        self.population_bias_mean = np.around(np.mean(self.mean_table, axis=0), decimals=1)
        self.population_bias_std = np.around(np.std(self.mean_table, axis=0), decimals=2)
        self.population_mean = np.around(np.mean(self.std_table, axis=0), decimals=2)

        self.tables_to_separate()

    # method that separates the main list into the ones according to the vector value - for plotting
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

    # method opening the single patient window - with single file selection first
    def single_pat(self):
        root = Tk()
        root.withdraw()
        file = filedialog.askopenfilename(parent=root, filetypes=(("ODT files", "*.odt"),
                                                                  ("DOCX files", "*.docx"),
                                                                  ("All files", "*")))

        if file and file.endswith(('.odt', '.docx')):
            self.widget = SinglePatientWindow(file, self.threshold, self.correction_sessions, self.mean_sessions)
            self.widget.show()

    # method for saving the data to a csv file
    def save_csv(self):
        root = Tk()
        root.withdraw()
        file = filedialog.asksaveasfile(parent=root, filetypes=(("CSV files", "*.csv"), ("All files", "*")),
                                        title='Save file...',
                                        defaultextension='.csv')

        if file and file.name.endswith('.csv'):
            with open(file.name, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=' ')  # ,

                csvwriter.writerow(
                    ['Filenames', 'Mean vrt', 'Mean lng', 'Mean lat', 'Mean rtn', 'Std vrt', 'Std lng', 'Std lat',
                     'Std rtn'])

                for row in range(0, len(self.mean_table)):
                    tmp = [self.filenames[row]]
                    tmp.extend(self.mean_table[row][:])
                    tmp.extend(self.std_table[row][:])

                    csvwriter.writerow(tmp)
                csvwriter.writerow([])
                population = ['Systematic error']
                population.extend(self.population_bias_mean)
                population.extend(self.population_bias_std)
                csvwriter.writerow(population)
                rand = ['Random error']
                rand.extend(self.population_mean)
                csvwriter.writerow(rand)

    # method for saving the plot as is
    def save_plot(self):
        root = Tk()
        root.withdraw()
        file = filedialog.asksaveasfile(parent=root, filetypes=(("PNG files", "*.png"), ("PDF files", "*.pdf"),
                                                                ("SVG files", "*.svg"), ("PS files", "*.ps"),
                                                                ("EPS files", "*.eps"), ("All files", "*")),
                                        title='Save file...',
                                        defaultextension='.png')
        ext = [".png", ".pdf", ".svg", ".ps", ".eps"]
        if file and file.name.endswith(tuple(ext)):
            self.m.save(file.name)

    # method opening the help window
    def help(self):
        self.widget = HelpWindow()
        self.widget.show()
