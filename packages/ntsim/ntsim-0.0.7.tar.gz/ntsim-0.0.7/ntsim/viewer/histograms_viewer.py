from ntsim.viewer.viewer_base import viewerbase
import numpy as np
from pyqtgraph.Qt import QtGui
import pyqtgraph as pg

import logging
log = logging.getLogger('histograms_viewer')

class BarGraph(pg.BarGraphItem):
    def mouseClickEvent(self, event):
        print(event)

def clicked(plot, points):
    print("curve clicked, amount: ", int(points.pos()[1]))

class histograms_viewer(viewerbase):
    def configure(self,opts):
        self.options = opts

    def build_energy_histogram(self):
        '''
        primary_energy = np.array([self.data[track]['E_GeV'][0] for track in self.data])
        hist = np.histogram(primary_energy, bins = 1000)
        bg1 = BarGraph(x = hist[1][:-1], height = hist[0], width=0.1, brush='r', data='hello')
        self.widgets["primary_energy"].addItem(bg1)
        '''
        primary_energy = np.array([self.data[track]['E_GeV'][0] for track in self.data])
        self.hist = np.histogram(primary_energy, bins = 1000)
        bg1 = self.widgets["primary_energy"].plot(x = self.hist[1], y = self.hist[0], stepMode='center', fillLevel=0, fillOutline=True, brush=(0,0,255,150), clickable=True)
        self.widgets["primary_energy"].setLabel('left', 'Amount')
        self.widgets["primary_energy"].setLabel('bottom', 'Energy', units='GeV')
        bg1.curve.setClickable(True)
        bg1.sigClicked.connect(clicked)

    def display_static(self):
        pass

    def display_frame(self):
        pass
