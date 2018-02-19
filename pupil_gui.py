"""
===============
Embedding in Qt
===============

Simple Qt application embedding Matplotlib canvases.  This program will work
equally well using Qt4 and Qt5.  Either version of Qt can be selected (for
example) by setting the ``MPLBACKEND`` environment variable to "Qt4Agg" or
"Qt5Agg", or by first importing the desired version of PyQt.
"""

import sys
import time

import numpy as np
import matplotlib.ticker as ticker
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


from PyQt4.QtCore import *
from PyQt4.QtGui import *
from DoubleSlider import *
#  
# class UpdatePlotThread(QThread)
#     def __init__(selfi,pupil):
#         QThread.__init__(self)
#         self.pupil=pupil
#     def __del__(self):
#         self.wait()
#     def run(self)
#         
# 

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self,pupil,luminance_range):
        super(ApplicationWindow, self).__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        self.resize(800,800)
        self.layout = QtWidgets.QVBoxLayout(self._main)
        self.pupil = pupil
        self.luminance_range=luminance_range
        static_canvas = FigureCanvas(Figure(figsize=(6.5, 5)))
        self.layout.addWidget(static_canvas)
        ''' Field Diameter Slider'''
        self.field_diameter_layout = QtWidgets.QHBoxLayout()
        self.field_diameter_slider = DoubleSlider(Qt.Horizontal)
        self.field_diameter_slider.setMaximum(60)
        self.field_diameter_slider.setMinimum(0.1)
        self.field_diameter_slider.setValue(10)
        self.field_diameter_slider.setTickPosition(QSlider.TicksBelow)
        self.field_diameter_slider.setTickInterval(1)
        self.field_diameter_label = QLabel()
        self.field_diameter_label.setText("Field diameter (deg)")
        self.field_diameter_label.setAlignment(Qt.AlignCenter)
        self.field_diameter_value_label = QLabel()
        text = "{:0.2f}".format(self.field_diameter_slider.value())
        self.field_diameter_value_label.setText(text)#   str(self.field_diameter_slider.value()))
        self.field_diameter_value_label.setAlignment(Qt.AlignCenter)
        self.field_diameter_layout.addWidget(self.field_diameter_label)
        self.field_diameter_layout.addWidget(self.field_diameter_slider)
        self.field_diameter_layout.addWidget(self.field_diameter_value_label)
        self.layout.addLayout(self.field_diameter_layout)
        self.field_diameter_slider.sliderReleased.connect(self.field_diameter_OnSliderReleased)
        self.field_diameter_slider.valueChanged.connect(self.field_diameter_OnValueChanged)


        '''Age Slider '''
        self.age_layout = QtWidgets.QHBoxLayout()
        self.age_slider = QSlider(Qt.Horizontal)
        self.age_slider.setMaximum(83)
        self.age_slider.setMinimum(20)
        self.age_slider.setValue(self.pupil.y)
        self.age_slider.setTickPosition(QSlider.TicksBelow)
        self.age_slider.setTickInterval(1)
        self.age_label = QLabel()
        self.age_label.setText("Age (years)")
        self.age_label.setAlignment(Qt.AlignCenter)
        self.age_value_label = QLabel()
        self.age_value_label.setText(str(self.age_slider.value()))
        self.age_value_label.setAlignment(Qt.AlignCenter)
        self.age_layout.addWidget(self.age_label)
        self.age_layout.addWidget(self.age_slider)
        self.age_layout.addWidget(self.age_value_label)
        self.layout.addLayout(self.age_layout)
        self.age_slider.valueChanged.connect(self.age_onValueChanged)
        self.age_slider.sliderReleased.connect(self.age_onSliderReleased)
        '''Radio button eyes'''
        self.eyes_layout = QtWidgets.QHBoxLayout()
        self.eyes_layout.setAlignment(Qt.AlignCenter)
        self.eyes_label = QLabel()
        self.eyes_label.setText("Eyes")
        self.eyes_one_radio_button = QRadioButton("1")
        self.eyes_two_radio_button = QRadioButton("2")
        self.eyes_one_radio_button.setChecked(True)
        self.eyes_layout.addWidget(self.eyes_label)
        self.eyes_layout.addWidget(self.eyes_one_radio_button)
        self.eyes_layout.addWidget(self.eyes_two_radio_button) 
        self.layout.addLayout(self.eyes_layout)
        self.eyes_one_radio_button.toggled.connect(lambda:self.eyes_OnValueChanged(self.eyes_one_radio_button))
        self.eyes_two_radio_button.toggled.connect(lambda:self.eyes_OnValueChanged(self.eyes_two_radio_button))
        ''' Range of luminance'''
        self.range_luminance_layout = QFormLayout()
        self.range_luminance_cb_min = QSpinBox()
        self.range_luminance_cb_min.setMinimum(-6)
        self.range_luminance_cb_min.setMaximum(-1)
        self.range_luminance_cb_min.setValue(-6)
        self.range_luminance_cb_max = QSpinBox()
        self.range_luminance_cb_max.setMinimum(1)
        self.range_luminance_cb_max.setMaximum(10)
        self.range_luminance_cb_max.setValue(1)
    #    self.pupil.L =np.arange(10**self.range_luminance_cb_min.value(),np.power(10,self.range_luminance_cb_max.value()),0.01)
        self.range_luminance_layout.addRow((QLabel("Minimum (log cd m-2)")),self.range_luminance_cb_min)
        self.range_luminance_layout.addRow((QLabel("Maximum (log cd m-2)")),self.range_luminance_cb_max)
        self.layout.addLayout(self.range_luminance_layout)
        self.range_luminance_cb_max.valueChanged.connect(self.range_luminance_OnValueChanged)
        self.range_luminance_cb_min.valueChanged.connect(self.range_luminance_OnValueChanged)



        self.addToolBar(NavigationToolbar(static_canvas, self))
        self._static_ax = static_canvas.figure.subplots()
        self.updatePlot()
    def field_diameter_OnSliderReleased(self):
        self.pupil.a=self.field_diameter_slider.value()
        self.updatePlot()
    def field_diameter_OnValueChanged(self):
        text = "{:0.2f}".format(self.field_diameter_slider.value()) 
        self.field_diameter_value_label.setText(text)
        #print ("field diameter = " + str(self.pupil.a))       
    def age_onValueChanged(self):
        self.age_value_label.setText(str(self.age_slider.value()))
    def age_onSliderReleased(self):
        self.pupil.y=self.age_slider.value()
        self.updatePlot()
    def eyes_OnValueChanged(self,button):
        if button.text() == "1" and button.isChecked() == True:
            self.pupil.e = 1
        elif button.text() == "2" and button.isChecked() == True:
            self.pupil.e = 2
            
        #self.pupil.e = (int(button.text()))
        #print '{}'.format(self.pupil.e)
        self.updatePlot()
    def range_luminance_OnValueChanged(self):
        #self.pupil.L =np.arange(10**self.range_luminance_cb_min.value(),np.power(10,self.range_luminance_cb_max.value()),0.001)
        self.updatePlot()
    def updatePlot(self):
        self._static_ax.cla()
       
       # self._static_ax.plot(self.luminance_range,self.pupil.holladay(self.luminance_range),color=(1,0,0),label="Holloday")
      #  self._static_ax.plot(self.luminance_range,self.pupil.moon_spancer(self.luminance_range),color=(0,1,0),label="Moon Spancer")
       # self._static_ax.plot(self.luminance_range,self.pupil.deGroot_gebhard(self.luminance_range),color=(0,0,1),label="DeGroot Gebhard")
       # self._static_ax.plot(self.luminance_range,self.pupil.stanley_davies(self.luminance_range,self.pupil.a),color=(1,0.51,0),label="Stanley Davies")
        #self._static_ax.plot(self.luminance_range,self.pupil.barten(self.luminance_range),color=(0,1,1),label="Barten")
       # self._static_ax.plot(self.luminance_range,self.pupil.blackie_howland(self.luminance_range),color=(0.5,0.5,0),label="Blackie Howland")
        self._static_ax.plot(self.luminance_range,self.pupil.unified_formula(self.luminance_range),color=(0,0,0),linestyle='--',label="Unified")
      #  self._static_ax.plot(self.luminance_range,self.pupil.crawford(self.luminance_range),color=(0.5,0.7,0.3),label="Crawford")
        
        self._static_ax.legend(loc="upper right")
        self._static_ax.set_xscale('log')
        self._static_ax.xaxis.set_major_locator(ticker.LogLocator(base=10,numticks=5))
        self._static_ax.yaxis.set_major_locator(ticker.MultipleLocator(base=1.0))
        self._static_ax.set_ylim(ymax=10,ymin=0)
        self._static_ax.set_xlim(xmax=10**4,xmin=10**-4) 
        self._static_ax.set_ylabel('Diameter (mm)')
        self._static_ax.set_xlabel(r'Luminance (cd $m^{-2}$)')
       
        self._static_ax.figure.canvas.draw()

def show_GUI(pupil,luminance_range):
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow(pupil,luminance_range)
    app.show()
    qapp.exec_()
