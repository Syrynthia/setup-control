from odf.opendocument import load
from tkinter import filedialog
from tkinter import Tk
from odf.table import Table, TableRow, TableCell
from math import fabs
import numpy as np

# global variable that holds the value of the treshold
TRESH = 0.2
# this is the row data in the table starts on
TABLE_DATA_ROW = 3

def read_odt():
    table = [[0] * 1 for i in range(0, 1)]
    root = Tk()
    root.withdraw()
    filez = filedialog.askopenfilename(parent=root, filetypes=(("ODT files", "*.odt"),
                                                               ("All files", "*")))
    if not filez:
        row = 0
        col = 0
    else:
        [row, col, table] = read_table(filez)
    return [row, col, table]


def read_table(filez):
    table = [[0] * 1 for i in range(0, 1)]
    doc = load(filez)
    tab = doc.text.getElementsByType(Table)[0]
    row = len(tab.getElementsByType(TableRow))
    col = len(tab.getElementsByType(TableRow)[0].getElementsByType(TableCell))
    for i in range(0, row):
        if len(table) != row:
            if i == 0 and len(table[0]) != col:
                for k in range(1, col):
                    table[0].append(0)
            else:
                table.append([0] * col)
        for j in range(0, col):
            string = str(tab.getElementsByType(TableRow)[i].getElementsByType(TableCell)[j])
            table[i][j] = string

    for i in range(6, row):
        vrtAv = float(table[i - 1][6])
        lngAv = float(table[i - 1][7])
        latAv = float(table[i - 1][8])
        rtnAv = float(table[i - 1][9])
        if fabs(vrtAv) > TRESH:
            table[i][0] = str(float(table[i][0]) - vrtAv)
        if fabs(lngAv) > TRESH:
            table[i][1] = str(float(table[i][0]) - lngAv)
        if fabs(latAv) > TRESH:
            table[i][2] = str(float(table[i][0]) - latAv)
        if fabs(rtnAv) > TRESH:
            table[i][3] = str(float(table[i][0]) - rtnAv)
        return [row, col, table]


def calculate_avg_stdev(table):
    vrt = []
    lng = []
    lat = []
    rtn = []
    for row in range(TABLE_DATA_ROW, len(table)):
        vrt.append(float(table[row][0]))
        lng.append(float(table[row][1]))
        lat.append(float(table[row][2]))
        rtn.append(float(table[row][3]))

    mean = [np.mean(vrt), np.mean(lng), np.mean(lat), np.mean(rtn)]
    stdev = [np.std(vrt), np.std(lng), np.std(lat), np.std(rtn)]
    return [mean, stdev]