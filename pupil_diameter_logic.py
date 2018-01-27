import numpy as np
'''
Function to calculate pupil diameter:
L - luminance in candela per cubic meter or in older name as nit, <float>, array between 0.0001 and 10000 with 0.01 step
a - field diameter in degrees <float>
y - age in years, <float>, between 20 and 83
y0 - reference age, constant <float> 28.58
e - quantity of eyes used in survey, <int> 1 or 2
    '''
class PupilDiameter_calculation:
    ''' Methods'''
    def __init__(self):
        self.e = 100
    def __init__(self,L,a,y,y0,e):
       self.L  = L
       self.a  = a
       self.y  = y
       self.y0 = y0
       self.e  = e
    def holladay():
        return 7*np.exp(-0.1007*np.power(L,0.4))
    def crawford():
        return 5- 2.2*np.tanh(0.61151 +0.447*np.log10(L))
    def moon_spancer():
        return 4.9 -3* np.tanh(0.4*np.log10(L))
    def deGroot_gebhard():
        return 7.175*np.exp(-0.00092*np.power(7.597 + np.log10(L),3))
    def stanley_davies():
        return 7.75-5.75*(np.power(((L*a)/846),(0.41))/(np.power(((L*a)/846),(0.41))+2))
    def barten():
        return 5 - 3 * np.tanh(0.4*np.log10((L*a)/np.power(40,2)))
    def blackie_howland():
        return 5.697 -0.658*np.log10(L)+0.07*np.power(np.log10(L),2)
    def winn_whitaker_elliott_phillips():
        Ws = 0
        Wl = 0
        s=[-0.024501,-0.0368073,0.0210892,0.00281557]
        b=[6.90390,2.77650,-1.909,0.25599]
        return 1
    def unified_formula():
        #return stanley_davies(L*number_of_eyes(e),a) + ageEffect(L,a,y,y0,e)
        F = L*a*number_of_eyes(e)
        D_sd = stanley_davies(F,1)
        return D_sd + (y-y0)*(0.02132 - 0.009562*D_sd)
    ''' Helper functions'''
    def number_of_eyes():
        if   e == 1: return 0.1
        elif e == 2: return 1
    def ageSplop_unified():
        return 0.021323 - 0.0095623*stanley_davies(L*number_of_eyes(e),a)
    def ageEffect_unified():
        if 20<=y<=83:
            return (y-y0)*ageSplop_unified(L,a,e)
        else:
            print "Wrong y range. It must be between 20 and 83"

