import random

from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        self.axes.cla()
        #data = [random.random() for i in range(25)]
        data = [0, 0, 0]
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        #ax.set_title('Plot placeholder')
        ax.set_ylabel('')
        self.draw()

    def plotChecked(self, data):
        self.axes.cla()
        colors = ['bo', 'go', 'co', 'mo']
        length = max([4, len(max(data, key=len))])
        line = [0 for i in range(0, length)]
        ax = self.figure.add_subplot(111)
        ax.plot(line, 'r-')
        for i in range(0, 4):
            ax.plot(data[i], colors[i])
        ax.set_ylabel('distance from the original centre [mm]')
        self.draw()