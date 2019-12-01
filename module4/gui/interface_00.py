import threading
from time import time, sleep

from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget

import numpy as np

from scope import TektronixScope
import vxi11

class MyThread(threading.Thread):
    def __init__(self, callback):
        self.callback = callback
        self.want_to_terminate = False
        threading.Thread.__init__(self)

    def run(self):
        t0 = time()
        while not self.want_to_terminate:
            self.callback(time() - t0)
            sleep(.1)

class StopWatchWindows(QtGui.QWidget):

    def __init__(self, args):
        self.app = QtGui.QApplication([])
        QtGui.QWidget.__init__(self)

        self.main_layout = main_layout = QtGui.QVBoxLayout()
        self.setLayout(main_layout)
                
        self.btn = QtGui.QPushButton('Start', self)
        main_layout.addWidget(self.btn)

        self.label = QtGui.QLabel(self)
        self.label.setText('Bonjour')
        main_layout.addWidget(self.label)

        self.btn.clicked.connect(self.on_btn_clicked)

        self.w_plot = MatplotlibWidget()
        main_layout.addWidget(self.w_plot)
        self.plot_data([1, 2, 1, 5])

        instr = vxi11.Instrument('134.157.91.150')
        self.scope = TektronixScope(instr)

        self.display_time(0)


    def display_time(self, t):
        self.label.setText('{:.2f}'.format(t))
        self.plot_data(self.scope.get_waveform(1))

    def on_btn_clicked(self):
        print('Hello')
        if self.btn.text()=="Start":
            self.thread = MyThread(self.display_time)
            self.thread.start()
            self.btn.setText('Stop')
        elif self.btn.text()=="Stop":
            self.thread.want_to_terminate = True
            self.thread.join()
            self.btn.setText('Start')

    def plot_data(self, data):
        fig = self.w_plot.getFigure()
        fig.clf()
        ax = fig.subplots(1, 1)
        ax.plot(data)
        fig.canvas.draw()

if __name__ == "__main__":
    main = StopWatchWindows([])
    main.show()
    exit(main.app.exec_())
