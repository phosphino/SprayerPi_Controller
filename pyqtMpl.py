from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtWidgets


class MplCanvas(FigureCanvas):
	def __init__(self, parent = None, width = 6, height = 5, dpi = 82):
		fig = Figure(figsize=(width, height), dpi = dpi, tight_layout = True)
		self.axes = fig.add_subplot(111)

		fig.patch.set_facecolor('#f0f0f0')
		fig.subplots_adjust(left= 0.2, right = 0.9, bottom = 0.175, top = 0.9)
		FigureCanvas.__init__(self, fig)
		self.setParent(parent)


		FigureCanvas.setSizePolicy(self,
								   QtWidgets.QSizePolicy.Expanding,
								   QtWidgets.QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)



	def update_figure(self, x, y):
		slabel = 'time / sec'
		mlabel = 'time / min'
		hlabel = 'time / hour'
		self.axes.cla()
		if x[-1] < 60:
			self.axes.set_xlabel(slabel)
		if x[-1] >= 60 and x[-1] < 3600:
			x = [i/60.0 for i in x]
			self.axes.set_xlabel(mlabel)
		if x[-1] >= 3600:
			x = [i/3600.0 for i in x]
			self.axes.set_xlabel(hlabel)
		self.axes.set_ylabel('temperature / Celsius')

		self.axes.plot(x, y, '-r')
		self.draw()
