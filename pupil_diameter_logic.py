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
    def holladay(self):
        return 7*np.exp(-0.1007*np.power(self.L,0.4))
    def crawfor(self):
        return 5- 2.2*np.tanh(0.61151 +0.447*np.log10(self.L))
    def moon_spancer(self):
        return 4.9 -3* np.tanh(0.4*np.log10(self.L))
    def deGroot_gebhard(self):
        return 7.175*np.exp(-0.00092*np.power(7.597 + np.log10(self.L),3))
    def stanley_davies(self):
        return 7.75-5.75*(np.power(((self.L*self.a)/846),(0.41))/(np.power(((self.L*self.a)/846),(0.41))+2))
    def barten(self):
        return 5 - 3 * np.tanh(0.4*np.log10((self.L*self.a)/np.power(40,2)))
    def blackie_howland(self):
        return 5.697 -0.658*np.log10(self.L)+0.07*np.power(np.log10(self.L),2) 
    def unified_formula(self):
        #return stanley_davies(L*number_of_eyes(e),a) + ageEffect(L,a,y,y0,e)
        F = self.L*self.a*self.number_of_eyes()
        D_sd = self.stanley_davies()
        return D_sd + (self.y-self.y0)*(0.02132 - 0.009562*D_sd)
    ''' Helper functions'''
    def number_of_eyes(self):
        if   self.e == 1: return 0.1
        elif self.e == 2: return 1
    def ageSplop_unified(self):
        return 0.021323 - 0.0095623*stanley_davies()
    def ageEffect_unified(self):
        if 20<=self.y<=83:
            return (self.y-self.y0)*self.ageSplop_unified(self.L,self.a,self.e)
        else:
            print "Wrong y range. It must be between 20 and 83"
