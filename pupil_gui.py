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
class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self,pupil):
        super(ApplicationWindow, self).__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        self.layout = QtWidgets.QVBoxLayout(self._main)

        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.layout.addWidget(static_canvas)
        ''' Field Diameter Slider'''
        self.field_diameter_layout = QtWidgets.QHBoxLayout()
        self.field_diameter_slider = QSlider(Qt.Horizontal)
        self.field_diameter_slider.setMaximum(60)
        self.field_diameter_slider.setMinimum(0.1)
        self.field_diameter_slider.setValue(10)
        self.field_diameter_slider.setTickPosition(QSlider.TicksBelow)
        self.field_diameter_slider.setTickInterval(0.1)
        self.field_diameter_label = QLabel()
        self.field_diameter_label.setText("Field diameter (deg)")
        self.field_diameter_label.setAlignment(Qt.AlignCenter)
        self.field_diameter_value_label = QLabel()
        self.field_diameter_value_label.setText(str(self.field_diameter_slider.value()))
        self.field_diameter_value_label.setAlignment(Qt.AlignCenter)
        self.field_diameter_layout.addWidget(self.field_diameter_label)
        self.field_diameter_layout.addWidget(self.field_diameter_slider)
        self.field_diameter_layout.addWidget(self.field_diameter_value_label)
        self.layout.addLayout(self.field_diameter_layout)
        self.field_diameter_slider.valueChanged.connect(self.field_diameter_OnValueChanged)
        '''Age Slider '''
        self.age_layout = QtWidgets.QHBoxLayout()
        self.age_slider = QSlider(Qt.Horizontal)
        self.age_slider.setMaximum(83)
        self.age_slider.setMinimum(20)
        self.age_slider.setValue(30)
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
        self.range_luminance_cb_max = QSpinBox()
        self.range_luminance_cb_max.setMinimum(1)
        self.range_luminance_cb_max.setMaximum(10)
        self.range_luminance_layout.addRow((QLabel("Minimum (log cd m-2)")),self.range_luminance_cb_min)
        self.range_luminance_layout.addRow((QLabel("Maximum (log cd m-2)")),self.range_luminance_cb_max)
        self.layout.addLayout(self.range_luminance_layout)
        self.range_luminance_cb_max.valueChanged.connect(self.range_luminance_max_OnValueChanged)
        self.range_luminance_cb_min.valueChanged.connect(self.range_luminance_min_OnValueChanged)



        self.addToolBar(NavigationToolbar(static_canvas, self))
        self._static_ax = static_canvas.figure.subplots()
        t = np.linspace(0, 10, 501)
        self.updatePlot(pupil)


    def age_onValueChanged(self):
        self.age_value_label.setText(str(self.age_slider.value()))
    def field_diameter_OnValueChanged(self):
        self.field_diameter_value_label.setText(str(self.field_diameter_slider.value()))
    def eyes_OnValueChanged(self,button):
        print (int(button.text()))
    def range_luminance_min_OnValueChanged(self):
        print "Min value of luminance range changed to" +str(self.range_luminance_cb_min.value())
    def range_luminance_max_OnValueChanged(self):
         print "Max value of luminance range changed to" +str(self.range_luminance_cb_max.value())
    def updatePlot(self,pupil_diameter_logic__):
        self._static_ax.plot(pupil_diameter_logic__.L,pupil_diameter_logic__.holladay(),color="blue")

        #plt.plot(L,crawford(L),color="green",label="Crowford")
        #plt.plot(L,moon_spancer(L),color="yellow",label="Moon Spancer")
        #plt.plot(L,deGroot_gebhard(L),color="red",label="DeGrootGebhard")
        #plt.plot(L,stanley_davies(L,25.4),color=(0.6,0.10,0.6),label="StanleyDavies")
        #plt.plot(L,barten(L,10),color=(0.4,0.6,0.2),label="Barten")
        #plt.plot(L,blackie_howland(L),color=(0.6,0.10,0.6),label="BlackieHowland")
        #plt.plot(L,winn_whitaker_elliott_phillips(L,25),color=(0.6,0.10,0.6))
        #plt.plot(L,unified_formula(L,a,y,y0,e),dashes=[10,10],color=(0,0,0),label="Unified")
        #plt.legend(loc='upper right')
        #plt.show()
        
        l
    
def show_GUI(pupil):
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow(pupil)
    app.show()
    qapp.exec_()
