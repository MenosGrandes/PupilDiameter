from pupil_diameter_logic import *
from pupil_gui import *

pupil = PupilDiameter_calculation(a=90,
                                  y=30,
                                  y0=28.58,
                                  e=2)
luminance_range = np.arange(0.00001,10**3,0.01,dtype=np.float)
show_GUI(pupil,luminance_range)
