from math import fabs

import numpy as np
from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from docx import Document

# this is the row data in the table starts on
TABLE_DATA_ROW = 3
#this is the number of sessions after which corrections were applied
SESSION_NUM = 3


def read_table(filez, threshold, correction_sessions):
    table = []
    doc = load(filez)
    try:
        tab = doc.text.getElementsByType(Table)[0]
        row = len(tab.getElementsByType(TableRow))
        col = len(tab.getElementsByType(TableRow)[0].getElementsByType(TableCell))
        for i in range(0, row):
            table.append([])
            for j in range(0, col):
                string = str(tab.getElementsByType(TableRow)[i].getElementsByType(TableCell)[j])
                table[i].append(string)

        start = TABLE_DATA_ROW+correction_sessions
        if start < row:
            for i in range(start, row):
                vrtAv = float(table[i - 1][6])
                lngAv = float(table[i - 1][7])
                latAv = float(table[i - 1][8])
                rtnAv = float(table[i - 1][9])
                if fabs(vrtAv) > threshold:
                    try:
                        vrt = float(table[i][0])
                        table[i][0] = str(np.around(vrt - vrtAv, decimals=1))
                    except ValueError:
                        pass
                if fabs(lngAv) > threshold:
                    try:
                        lng = float(table[i][1])
                        table[i][1] = str(np.around(lng - lngAv, decimals=1))
                    except ValueError:
                        pass
                if fabs(latAv) > threshold:
                    try:
                        lat = float(table[i][2])
                        table[i][2] = str(np.around(lat - latAv, decimals=1))
                    except ValueError:
                        pass
                if fabs(rtnAv) > threshold:
                    try:
                        rtn = float(table[i][3])
                        table[i][3] = str(np.around(rtn - rtnAv, decimals=1))
                    except ValueError:
                        pass
    except IndexError:
        row = 0
        col = 0
    return [row, col, table]


def calculate_avg_stdev(table, mean_number):
    vrt = []
    lng = []
    lat = []
    rtn = []

    if mean_number == 0 or len(table) < mean_number:
        length = len(table)
    else:
        length = mean_number

    for row in range(TABLE_DATA_ROW, length):
        try:
            vr = float(table[row][0])
            vrt.append(vr)
        except ValueError:
            pass
        try:
            ln = float(table[row][1])
            lng.append(ln)
        except ValueError:
            pass
        try:
            la = float(table[row][2])
            lat.append(la)
        except ValueError:
            pass
        try:
            rt = float(table[row][3])
            rtn.append(rt)
        except ValueError:
            pass

    mean = np.around([np.mean(vrt), np.mean(lng), np.mean(lat), np.mean(rtn)], decimals=1)
    stdev = np.around([np.std(vrt), np.std(lng), np.std(lat), np.std(rtn)], decimals=2)

    return [mean, stdev]

def read_docx(filez, threshold, correction_sessions):
    table = []
    doc = Document(filez)
    tables = doc.tables
    row = 0 
    col = 0 
    for tab in tables:
        row = len(tab.rows)
        for i in range(0, len(tab.rows)):
            table.append([])
            col = len(tab.rows[i].cells)
            for j in range(0, len(tab.rows[i].cells)):
                for paragraph in tab.rows[i].cells[j].paragraphs:
                    str = paragraph.text
                    if "," in str:
                        str = str.replace(",", ".")
                    table[i].append(str)


    start = TABLE_DATA_ROW+correction_sessions
    if start < row:
        for i in range(start, row):
            vrtAv = float(table[i - 1][6])
            lngAv = float(table[i - 1][7])
            latAv = float(table[i - 1][8])
            rtnAv = float(table[i - 1][9])
            if fabs(vrtAv) > threshold:
                try:
                    vrt = float(table[i][0])
                    table[i][0] = str(np.around(vrt - vrtAv, decimals=1))
                except ValueError:
                    pass
            if fabs(lngAv) > threshold:
                try:
                    lng = float(table[i][1])
                    table[i][1] = str(np.around(lng - lngAv, decimals=1))
                except ValueError:
                    pass
            if fabs(latAv) > threshold:
                try:
                    lat = float(table[i][2])
                    table[i][2] = str(np.around(lat - latAv, decimals=1))
                except ValueError:
                    pass
            if fabs(rtnAv) > threshold:
                try:
                    rtn = float(table[i][3])
                    table[i][3] = str(np.around(rtn - rtnAv, decimals=1))
                except ValueError:
                    pass

    return [row, col, table]
