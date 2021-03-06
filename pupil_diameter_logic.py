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

    def __init__(self, a, y, y0, e):
        self.a = a
        self.y = y
        self.y0 = y0
        self.e = e
    '''
    TODO Pupil size estimation based on spatially weighted corneal flux density.pdf
    '''
    def spatiallyWeightedCornealFluxDensity(self):
        f = (self.cornealFluxDensity() / 2506) * np.power(0.8)
        return 5.12 - 2.76 * (f / f + 10)

    def cornealFluxDensity(self):
        return 1
    '''
    ####################
    '''
    def holladay(self, L):
        return 7 * np.exp(-0.1007 * np.power(L, 0.4))

    def crawford(self, L):
        return 5 - 2.2 * np.tanh(0.61151 + 0.447 * np.log10(L))

    def moon_spancer(self, L):
        return 4.9 - 3 * np.tanh(0.4 * np.log10(L))

    def deGroot_gebhard(self, L):
        return 7.175 * np.exp(-0.00092 * np.power(7.597 + np.log10(L), 3))

    def stanley_davies(self, L, a):
        frac_1 = np.power(((L * (a**2)) / 846), 0.41)
        frac_2 = frac_1 + 2
        return 7.75 - 5.75 * (frac_1 / frac_2)

    def barten(self, L):
        return 5 - 3 * np.tanh(0.4 * np.log10((L * (self.a**2)) / np.power(40, 2)))

    def blackie_howland(self, L):
        return 5.697 - 0.658 * np.log10(L) - 0.07 * np.power(np.log10(L), 2)

    def unified_formula(self, L):
        F = L * np.power(self.a, 2) * self.number_of_eyes()
        return self.stanley_davies(F, 1) + (self.y - self.y0) * (0.02132 - 0.009562 * self.stanley_davies(F, 1))
        # return stanley_davies(L*number_of_eyes(e),a) + ageEffect(L,a,y,y0,e)

    def winn(self, L):
        '''    iTuple = [6.9039,2.7765,-1.909,0.25599]
        sTuple = [-0.024501, -0.0368073, 0.0210892,0.00281557]
        intercept = [sum(s* np.log(min(4400,max(9,l)))**power*self.y+ i*np.log(min(4400,max(9,l)))**power for power, (s,i)  in enumerate(zip(sTuple,iTuple))) for l in L]
        return intercept #(sum(s* (log(min(4400,max(9,L))))**power)*y+sum(b* (log(min(4400,max(9,L))))**power) )
        '''

    def number_of_eyes(self):
        if self.e == 1:
            return 0.1
        elif self.e == 2:
            return 1

    def ageSplop_unified(self, L):
        return 0.021323 - 0.0095623 * self.stanley_davies(L, self.a)

    def ageEffect_unified(self, L):
        if 20 <= self.y <= 83:
            return (self.y - self.y0) * self.ageSplop_unified(L, self.a, self.e)
        else:
            print("Wrong y range. It must be between 20 and 83")

    def winnSlope(self, l):
        Ws = 0
        for i, tuple in enumerate(sTuple):
            Ws += tuple * np.power(np.log(min(4400, max(9, l))), i)
        return Ws

    def winnIntercept(self, l):
        Ws = 0
        for i, tuple in enumerate(bTuple):
            Ws += tuple * np.power(np.log(min(4400, max(9, l))), i)
        return Ws
