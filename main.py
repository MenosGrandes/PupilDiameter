from pupil_diameter_logic import *
from pupil_gui import *

pupil = PupilDiameter_calculation(L=np.arange(10**-4,10**4,0.01),
                                  a=60,
                                  y=30,
                                  y0=28.58,
                                  e=2)
show_GUI(pupil)




#plt.figure(1)




#plt.plot(L,holladay(L),color="blue")

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

