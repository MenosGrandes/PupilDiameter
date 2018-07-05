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
    def __init__(self,a,y,y0,e):
       self.a  = a
       self.y  = y
       self.y0 = y0
       self.e  = e
    def holladay(self,L):
        return 7*np.exp(-0.1007*np.power(L,0.4))
    def crawford(self,L):
        return 5-2.2*np.tanh(0.61151 +0.447*np.log10(L))
    def moon_spancer(self,L):
        return 4.9 -3* np.tanh(0.4*np.log10(L))
    def deGroot_gebhard(self,L):
        return 7.175*np.exp(-0.00092*np.power(7.597 + np.log10(L),3))
    def stanley_davies(self,L,a):
        frac_1 = np.power(( (L*(a**2))/846),0.41)
        frac_2 = frac_1 + 2
        return 7.75-5.75*(frac_1/frac_2)
    def barten(self,L):
        return 5 - 3 * np.tanh(0.4*np.log10((L*(self.a**2))/np.power(40,2)))
    def blackie_howland(self,L):
        return 5.697 - 0.658* np.log10(L) - 0.07 * np.power(np.log10(L),2)
    def unified_formula(self,L):
        F = L * np.power(self.a,2) * self.number_of_eyes()
        return self.stanley_davies(F,1) + (self.y-self.y0)*(0.02132 - 0.009562*self.stanley_davies(F,1))
        #return stanley_davies(L*number_of_eyes(e),a) + ageEffect(L,a,y,y0,e) 
    def winn(self,L):
        return self.winnSlope(L)*self.y + self.winnIntercept(L)
    def number_of_eyes(self):
        if   self.e == 1: return 0.1
        elif self.e == 2: return 1
    def ageSplop_unified(self,L):
        return 0.021323 - 0.0095623*self.stanley_davies(L,self.a)
    def ageEffect_unified(self,L):
        if 20<=self.y<=83:
            return (self.y-self.y0)*self.ageSplop_unified(L,self.a,self.e)
        else:
            print ("Wrong y range. It must be between 20 and 83")
    def winnSlope(self,L):
        sTuple = [-0.024501, -0.0368073, 0.0210892,0.00281557]
        Ws =[]
        for j,l in enumerate(L):
            Ws.append(0)
            for i,s in enumerate(sTuple):
                print ("l =%d, i=%d",l,i)
                Ws[j]+= ( s* np.power(np.log10( np.minimum(4400, np.maximum(9,l))),i))
                print Ws[j]
        print "aaa"
        print Ws
        return Ws
    def winnIntercept(self,L):
        bTuple = [6.9039,2.7765,-1.909,0.25599]
        Wi = 0
        for i,b in enumerate(bTuple):
            Wi= Wi + (b * np.power(np.log10( np.minimum(4400, np.maximum(9,L))),i))
        return Wi
