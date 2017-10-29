from odf.opendocument import load
from tkinter import filedialog
from tkinter import Tk
from odf.table import Table, TableRow, TableCell


def readOdt(row, col, table):
    root = Tk()
    root.withdraw()
    filez = filedialog.askopenfilename(parent=root, filetypes=(("ODT files", "*.odt"),
                                                               ("All files", "*")))
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
                table.append([0]*col)
        for j in range(0, col):
            string = str(tab.getElementsByType(TableRow)[i].getElementsByType(TableCell)[j])
            table[i][j] = string

    print('reading done')
    print(table)
