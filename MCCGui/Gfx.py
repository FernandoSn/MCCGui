from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class Canvas(FigureCanvas):

    _VISWND = (2,5,10,20,30)  # Do not change!

    PlotIdx = 0
    AxisON = False
    XLim = 0

    def __init__(self, XLim, parent=None, width=20, height=5,dpi=100):

        # Ctor. Calling the Ctor of the parent with custom params.
        super().__init__(Figure(figsize=(width, height), dpi=dpi))
        self.setParent(parent)
        self.figure = Figure(tight_layout=True, dpi=dpi)
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111)
        self.XLim = XLim
        self.ResetAxes()

    def plot(self, data):

        #self.axes.clear()

        PlotIdxEnd = self.PlotIdx + len(data)

        if ( PlotIdxEnd >= self.XLim):

            X1 = np.arange(self.PlotIdx,self.XLim)
            self.axes.plot(X1, data[0:len(X1)], color='black', linewidth=1)

            self.ResetAxes()

            X2 = np.arange(0,len(data) - len(X1))
            self.axes.plot(X2, data[len(X1):], color='black', linewidth=1)
            self.PlotIdx = len(X2)

        else:

            X1 = np.arange(self.PlotIdx,PlotIdxEnd)
            self.axes.plot(X1, data, color='black', linewidth=1)
            self.PlotIdx = PlotIdxEnd

        self.draw()

    def plotResp(self, data,mindata,maxdata):

        #self.axes.clear()

        PlotIdxEnd = self.PlotIdx + len(data)

        if ( PlotIdxEnd >= self.XLim):

            X1 = np.arange(self.PlotIdx,self.XLim)
            self.axes.plot(X1, data[0:len(X1)], color='black', linewidth=1)

            self.ResetAxes()

            X2 = np.arange(0,len(data) - len(X1))
            self.axes.plot(X2, data[len(X1):], color='black', linewidth=1)
            self.PlotIdx = len(X2)
            if X2.__len__() > 0:
                self.axes.plot([X2[-1],X2[-1]], [mindata,maxdata], color='red', linewidth=1)

        else:

            X1 = np.arange(self.PlotIdx,PlotIdxEnd)
            self.axes.plot(X1, data, color='black', linewidth=1)
            self.PlotIdx = PlotIdxEnd
            self.axes.plot([X1[-1], X1[-1]], [mindata, maxdata], color='red', linewidth=1)

        self.draw()

    def ResetAxes(self):
        self.axes.cla()
        self.axes.set_xlim(0, self.XLim)
        if not self.AxisON:
            self.axes.set_axis_off()
