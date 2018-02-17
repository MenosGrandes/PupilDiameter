from pupil_diameter_logic import *
from pupil_gui import *

pupil = PupilDiameter_calculation(a=90,
                                  y=30,
                                  y0=28.58,
                                  e=2)
luminance_range_1 = np.linspace(0.00001,1,10000)
luminance_range_2 = np.linspace(1,10000,10000)

luminance_range=np.concatenate((luminance_range_1,luminance_range_2),axis=0)
show_GUI(pupil,luminance_range)
