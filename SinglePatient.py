import sys
from tkinter import Tk, filedialog

from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import (QWidget, QDialog, QDialogButtonBox, QGridLayout, QGroupBox, QLabel, QMenu, QMenuBar,
                             QTextEdit, QHBoxLayout, QScrollBar,
                             QVBoxLayout, QAction, QApplication, QCheckBox, QScrollArea, QMainWindow)
import ReadOdt
import os

import ui
from PlotCanvas import PlotCanvas
from PyQt5.QtCore import Qt


class SinglePatientWindow(QMainWindow):


    def __init__(self, file, threshold):
        QMainWindow.__init__(self)
        super(SinglePatientWindow, self).__init__()
        self.form_widget = FormWidget(self, file, threshold)
        self.setCentralWidget(self.form_widget)
        self.filename = os.path.split(file)[1]
        self.setWindowTitle(self.filename)


class FormWidget(QWidget):
    toplot = [[], [], [], []]
    vrt = []
    lng = []
    lat = []
    rtn = []
    dates = []
    def __init__(self, parent, file, threshold):
        super(FormWidget, self).__init__(parent)
        self.threshold = threshold
        self.table = ReadOdt.read_table(file, self.threshold)[2]
        [self.mean_table, self.std_table] = ReadOdt.calculate_avg_stdev(self.table)
        self.tables_to_separate()

        self.filename = os.path.split(file)[1]

        mainLayout = QVBoxLayout()
        self.create_data()
        mainLayout.addWidget(self.resultFrame)

        self.createPlotFrame()
        mainLayout.addWidget(self.plotFrame)

        self.setLayout(mainLayout)

    def create_data(self):

        self.resultFrame = QGroupBox("Data ")
        self.resultFrame.setMaximumHeight(400)
        self.data_print = QWidget()
        self.data_print.setMinimumWidth(400)
        #self.data_print.setFixedHeight(300)
        self.frameLayout = QGridLayout()
        self.main_frame = QHBoxLayout()
        self.dates.clear()

        for row in range(0, len(self.table)):
            if row > 2:
                self.dates.append(self.table[row][4])
            for col in range(0, len(self.table[0])):
                self.frameLayout.addWidget(QLabel(str(self.table[row][col])), row, col)
                #print(self.table[row][col])

        self.data_print.setLayout(self.frameLayout)

        scroll = QScrollArea()
        scroll.setWidget(self.data_print)

        self.main_frame.addWidget(scroll)
        self.resultFrame.setLayout(self.main_frame)

    def tables_to_separate(self):
        self.vrt.clear()
        self.lng.clear()
        self.lat.clear()
        self.rtn.clear()

        for row in range(ReadOdt.TABLE_DATA_ROW, len(self.table)):
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
'''
if __name__ == '__main__':
    root = Tk()
    root.withdraw()
    file = filedialog.askopenfilename(parent=root, filetypes=(("ODT files", "*.odt"), ("All files", "*")))

    if file:
        app = ui.QApplication(sys.argv)
        dialog = SinglePatientWindow(file, 0.3)
        dialog.show()
        sys.exit(app.exec_())
'''