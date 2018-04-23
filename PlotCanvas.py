from math import ceil

from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# class creating a plot object
class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    # method for drawing the empty plot
    def plot(self):
        self.axes.cla()
        data = [0, 0, 0]
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_ylabel('')
        self.draw()

    # method for drawing the single patient plot
    def plotChecked(self, data, labels):
        self.axes.cla()
        colors = ['bo', 'go', 'co', 'mo']
        length = max([4, len(max(data, key=len))])
        x = [i for i in range(0, length)]
        line = [0 for i in range(0, length)]
        ax = self.figure.add_subplot(111)
        ax.plot(x, line, 'r-')
        for i in range(0, 4):
            ax.plot(data[i], colors[i])
        ax.set_ylabel('distance from isocenter [cm]')
        ax.plot(x, line, 'r-')
        step = ceil(length / 10)
        ax.set_xticks(x[::step])
        ax.set_xticklabels(labels[::step], rotation=15)
        self.draw()

    # method for drawing the main plot with errorbars
    def plot_checked_errors(self, data, errors, labels):
        self.axes.cla()
        colors = ['bo', 'go', 'co', 'mo']
        length = max([4, len(max(data, key=len))])
        x = [i for i in range(0, length)]
        line = [0 for i in range(0, length)]
        ax = self.figure.add_subplot(111)
        ax.plot(x, line, 'r-')
        for i in range(0, len(data)):
            if len(data[i]) > 0:
                ax.errorbar(x[:len(data[i])], data[i], yerr=errors[i], fmt=colors[i])
        ax.set_ylabel('distance from isocenter [cm]')
        ax.plot(x, line, 'r-')
        step = ceil(length / 10)
        ax.set_xticks(x[::step])
        ax.set_xticklabels(labels[::step], rotation=15)
        self.draw()

    def save(self, file):
        self.fig.savefig(file)
