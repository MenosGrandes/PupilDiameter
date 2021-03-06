'''
Module responsible for GUI.
I know it's awaful....
'''
import sys
import time
import itertools
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


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from DoubleSlider import *

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self,pupil,luminance_range):
        super(ApplicationWindow, self).__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        self.resize(800,1000)
        self.layout = QtWidgets.QVBoxLayout(self._main)
        self.pupil = pupil
        self.luminance_range=luminance_range
        static_canvas = FigureCanvas(Figure(figsize=(5.5, 7)))
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
        self.eyes_two_radio_button.setChecked(True)
        self.eyes_layout.addWidget(self.eyes_label)
        self.eyes_layout.addWidget(self.eyes_one_radio_button)
        self.eyes_layout.addWidget(self.eyes_two_radio_button) 
        self.layout.addLayout(self.eyes_layout)
        self.eyes_one_radio_button.toggled.connect(lambda:self.eyes_OnValueChanged(self.eyes_one_radio_button))
        self.eyes_two_radio_button.toggled.connect(lambda:self.eyes_OnValueChanged(self.eyes_two_radio_button))
        ''' Range of luminance
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
    	'''
        self.algorithm_layout_grid = QHBoxLayout()#QGridLayout()	
        ''' Checkboxes for algorithm'''
        self.algorith_checkboxes =[QCheckBox("Holladay",self),
                              QCheckBox("MoonSpancer",self),
                              QCheckBox("DeGroot Gebhard",self),
                              QCheckBox("Stanley Davies",self),
                              QCheckBox("Barten",self),
                              QCheckBox("Blackie Howland",self),
                              QCheckBox("Unified",self),
                              QCheckBox("Crawford",self)
        #                      QCheckBox("Winn",self)
                             #      QCheckBox("Winn Age Slope",self)
                             ]
        for i in range(0,len(self.algorith_checkboxes)):
            self.algorithm_layout_grid.addWidget(self.algorith_checkboxes[i])
            self.algorith_checkboxes[i].stateChanged.connect(lambda checked,i=i:self.updatePlot())
        self.layout.addLayout(self.algorithm_layout_grid)

        self.addToolBar(NavigationToolbar(static_canvas, self))
        self._static_ax = static_canvas.figure.subplots()
        self.updatePlot()

    def field_diameter_OnSliderReleased(self):
        self.pupil.a=self.field_diameter_slider.value()
        self.updatePlot()
    def field_diameter_OnValueChanged(self):
        text = "{:0.2f}".format(self.field_diameter_slider.value())
        self.field_diameter_value_label.setText(text)
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
        self.updatePlot()
    '''def range_luminance_OnValueChanged(self):
        #self.pupil.L =np.arange(10**self.range_luminance_cb_min.value(),np.power(10,self.range_luminance_cb_max.value()),0.001)
        self.updatePlot()
    '''
    def updatePlot(self):
        self._static_ax.cla()

        if self.algorith_checkboxes[0].isChecked():
            self._static_ax.plot(self.luminance_range,self.pupil.holladay(self.luminance_range),color=(1,0,0),label="Holladay")
        if self.algorith_checkboxes[1].isChecked():
            self._static_ax.plot(self.luminance_range,self.pupil.moon_spancer(self.luminance_range),color=(0,1,0),label="MoonSpencer")
        if self.algorith_checkboxes[2].isChecked():
            self._static_ax.plot(self.luminance_range,self.pupil.deGroot_gebhard(self.luminance_range),color=(0,0,1),label="DeGroot Gebhard")
        if self.algorith_checkboxes[3].isChecked():
            self._static_ax.plot(self.luminance_range,self.pupil.stanley_davies(self.luminance_range,self.pupil.a),color=(1,0.51,0),label="Stanley Davies")
        if self.algorith_checkboxes[4].isChecked():
           self._static_ax.plot(self.luminance_range,self.pupil.barten(self.luminance_range),color=(0,1,1),label="Barten")
        if self.algorith_checkboxes[5].isChecked():
           self._static_ax.plot(self.luminance_range,self.pupil.blackie_howland(self.luminance_range),color=(0.5,0.5,0),label="Blackie Howland")
        if self.algorith_checkboxes[6].isChecked():
            self._static_ax.plot(self.luminance_range,self.pupil.unified_formula(self.luminance_range),color=(0,0,0),linestyle='--',label="Unified")
        if self.algorith_checkboxes[7].isChecked():
            self._static_ax.plot(self.luminance_range,self.pupil.crawford(self.luminance_range),color=(0.5,0.7,0.3),label="Crawford")
        
        def flip(items, ncol):
            return itertools.chain(*[items[i::ncol] for i in range(ncol)])
            
            
        handles, labels = self._static_ax.get_legend_handles_labels()
        handles = np.concatenate((handles[::2],handles[1::2]),axis=0)
        labels = np.concatenate((labels[::2],labels[1::2]),axis=0)
        self._static_ax.legend(flip(handles, 2), flip(labels, 2), loc=9, ncol=2)
        self._static_ax.set_xscale('log')
        self._static_ax.xaxis.set_major_locator(ticker.LogLocator(base=10,numticks=5))
        self._static_ax.yaxis.set_major_locator(ticker.MultipleLocator(base=1.0))
        self._static_ax.set_ylim(top=10,bottom=0)
        self._static_ax.set_xlim(right=10**4,left=10**-4)  
        self._static_ax.set_ylabel('Diameter (mm)')
        self._static_ax.set_xlabel(r'Luminance (cd $m^{-2}$)')
        self._static_ax.grid()
        #self._static_ax.figure.tight_layout();
        self._static_ax.figure.canvas.draw()

def show_GUI(pupil,luminance_range):
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow(pupil,luminance_range)
    app.show()
    qapp.exec_()
