import numpy as np
import matplotlib.pyplot as plt

'''
Function to calculate pupil diameter
'''

def holladay(L):
     return 7*np.exp(-0.1007*np.power(L,0.4))
def crawford(L):
    return 5- 2.2*np.tanh(0.61151 +0.447*np.log10(L))
def moon_spancer(L):
    return 4.9 -3* np.tanh(0.4*np.log10(L))
def deGroot_gebhard(L):
    return 7.175*np.exp(-0.00092*np.power(7.597 + np.log10(L),3))
def stanley_davies(L,a):
    return 7.75-5.75*(np.power(((L*a)/846),(0.41))/(np.power(((L*a)/846),(0.41))+2))
def barten(L,a):
    return 5 - 3 * np.tanh(0.4*np.log10((L*a)/np.power(40,2)))
def blackie_howland(L):
    return 5.697 -0.658*np.log10(L)+0.07*np.power(np.log10(L),2)
def winn_whitaker_elliott_phillips(L,y):
    Ws = 0
    Wl = 0
    s=[-0.024501,-0.0368073,0.0210892,0.00281557]
    b=[6.90390,2.77650,-1.909,0.25599]
    return 1
def unifiedFormula(L,a,y,y0,e):
    #return stanley_davies(L*number_of_eyes(e),a) + ageEffect(L,a,y,y0,e)
    F = L*a*number_of_eyes(e)
    D_sd = stanley_davies(F,1)
    return D_sd + (y-y0)*(0.02132 - 0.009562*D_sd)
'''
Helper functions
'''
def number_of_eyes(eyes):
    if   eyes == 1: return 0.1
    elif eyes == 2: return 1
def ageSplop_unified(L,a,e):
    return 0.021323 - 0.0095623*stanley_davies(L*number_of_eyes(e),a)
def ageEffect_unified(L,a,y,y0,e):
    if 20<=y<=83:
        return (y-y0)*ageSplop_unified(L,a,e)
    else:
        print "Wrong y range. It must be between 20 and 83"
''' 
L - luminance in candela per cubic meter or in older name as nit, <float>, array between 0.0001 and 10000 with 0.01 step
a - field diameter in degrees <float>
y - age in years, <float>, between 20 and 83
y0 - reference age, constant <float> 28.58
e - quantity of eyes used in survey, <int> 1 or 2
'''
L  = np.arange(0.0001,np.power(10,4),0.01)
a  = 0.4
y  = 30
y0 = 28.58
e  = 2

plt.figure(1)




#plt.plot(L,holladay(L),color="blue")

plt.plot(L,crawford(L),color="green",label="Crowford")
plt.plot(L,moon_spancer(L),color="yellow",label="Moon Spancer")
plt.plot(L,deGroot_gebhard(L),color="red",label="DeGrootGebhard")
plt.plot(L,stanley_davies(L,25.4),color=(0.6,0.10,0.6),label="StanleyDavies")
plt.plot(L,barten(L,10),color=(0.4,0.6,0.2),label="Barten")
plt.plot(L,blackie_howland(L),color=(0.6,0.10,0.6),label="BlackieHowland")
#plt.plot(L,winn_whitaker_elliott_phillips(L,25),color=(0.6,0.10,0.6))
plt.plot(L,unifiedFormula(L,a,y,y0,e),dashes=[10,10],color=(0,0,0),label="Unified")
plt.legend(loc='upper right')
plt.show()
