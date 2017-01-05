# encoding: utf-8

import math
import numpy as np
import matplotlib.pyplot as plt


#for package

import Tkinter
import FileDialog

#---------------------------------------------------------------------------------------#
# https://docs.scipy.org/doc/numpy/reference/generated/numpy.polyfit.html
# I know I can use the LinearFit Function in numpy(previous page), but I will use the 
# Least-Square Method to make a new wheel.


#---------------------------------------------------------------------------------------#
#Using ownFuncion named with _CAM in the end

def linearFit_CAM(x, y, n):
#check the amount of x and y
    if len(x) != len(y) or len(x) == 0:
        print u"无试验数据 或者 试验数据长度不匹配"
    else:
        P = getAugmentedMatrix(x, y, n)
        # print P
        A = eliminationMethod(P)
        Fin = A.T[-1]
        # draw a picture
        x_f = np.linspace(x[0], x[-1], 100)
        z = linearFitFunc_CAM(x_f, n, Fin)
        figNames = locals()
        figNames['fig%s' % n] = plt.figure('%s Times Fitting' % n)
        plt.plot(x_f, z, '-', x, y, '.')

        zpoint = linearFitFunc_CAM(x, n, Fin)
        
        #calculate deviation
        Err = []
        for i in range(0, len(x)):
            if y[i] - zpoint[i] < 0:
                Err.append(zpoint[i] - y[i])
            else:
                Err.append(y[i] - zpoint[i])
        ErrCounter = 0
        for i in range(0, len(x)):
            if Err[i] > 0.01:
                ErrCounter = ErrCounter + 1

        #return result
        return [x_f, z]
        # print u"多项式次数：", n
        # print u"不满足精度要求的点数：", ErrCounter
        # print ""


#Modules process for linearFit

def getAugmentedMatrix(x, y, n):
    coefficient = np.array([])
    value = np.array([])
    AM = np.array([])
    m = len(x)
    counter1 = 0
    counter2 = 0
    counter3 = 0
    #get coefficientMatrix
    coefficientCache = 0
    coefficientCache_r = np.array([])    
    while counter1 <= n:
        while counter2 <= n:
            while counter3 < m:
                coefficientCache = coefficientCache + x[counter3]**(counter1 + counter2)
                counter3 = counter3 + 1
            coefficientCache_r = np.append(coefficientCache_r, coefficientCache)
            coefficientCache = 0
            counter3 = 0
            counter2 = counter2 + 1
        coefficient = np.append(coefficient, coefficientCache_r)
        coefficientCache_r = np.array([])
        counter2 = 0
        counter3 = 0
        counter1 = counter1 + 1
    counter1 = 0
    counter2 = 0
    counter3 = 0
    coefficient = coefficient.reshape((n+1, n+1))
    #get valueMatrix    
    while counter1 <= n:
        while counter2 < m:
            valueCache = y[counter2] * (x[counter2]**counter1)
            try:
                value[counter1] = value[counter1] + valueCache
            except:
                valueCacheList = []
                valueCacheList.append(valueCache)
                value = np.append(value, valueCacheList)
            counter2 = counter2 + 1
        counter1 = counter1 +1
        counter2 = 0
    counter1 = 0
    counter2 = 0
    counter3 = 0
    value = value.reshape((n+1, 1))
    AM = np.hstack((coefficient, value))
    return AM


#Gauss elimination 
def eliminationMethod(Arr):
    if len(Arr) != 0 and (len(Arr[0]) - len(Arr)) == 1:
        n = len(Arr)
        for i in range(0, n-1):
            for j in range(i+1, n):
                if Arr[j, i] != 0:
                    Arr[j] = (Arr[i][i]/Arr[j][i])*Arr[j] - Arr[i]
        #get fit parameters
        for i in range(0, n):
            Arr[i] = Arr[i]/Arr[i][i]
        for i in range(n-1, -1, -1):
            for j in range(i-1, -1, -1):
                Arr[j] = Arr[j] - Arr[j, i]*Arr[i]        
        return Arr
    else:
        print "I can't deal with this Matrix'"
        return

#generate linearFit Function
def linearFitFunc_CAM(x, n, A):
    m = len(x)
    y = []
    ans = 0
    for i in range(0, m):
        for j in range(0, n+1):
            ans = ans + A[j]*(x[i]**j)
        y.append(ans)
        ans = 0
    return y



def lnFit_CAM(x, y):
    if len(x) != len(y) or len(x) == 0:
        print u"无试验数据 或者 试验数据长度不匹配"
    else:
        P = getAugmentedMatrixforlnFit(x, y)
        A = eliminationMethod(P)
        Fin = A.T[-1]
        # draw a picture
        x_f = np.linspace(x[0], x[-1], 100)
        z = lnFitFunc_CAM(x_f, Fin)
        figLn = plt.figure('Logarithmic Equation Fitting')
        plt.plot(x_f, z, '-', x, y, '.')
        
        zpoint = lnFitFunc_CAM(x, Fin)
        #calculate deviation
        Err = []
        for i in range(0, len(x)):
            if y[i] - zpoint[i] < 0:
                Err.append(zpoint[i] - y[i])
            else:
                Err.append(y[i] - zpoint[i])
        ErrCounter = 0
        for i in range(0, len(x)):
            if Err[i] > 0.01:
                ErrCounter = ErrCounter + 1

        print u"对数方程拟合"        
        print u"不满足精度要求的点数：", ErrCounter
        print ""



#Modules process for lnFit

def getAugmentedMatrixforlnFit(x, y):
    #This time, I will calculate augmented matrix directly.
    arg11 = len(x)
    arg12 = 0
    for i in range(0, arg11):
        arg12 = arg12 + math.log(x[i], math.e)
    arg13 = 0
    for i in range(0, arg11):
        arg13 = arg13 + y[i]
    arg21 = arg12
    arg22 = 0
    for i in range(0, arg11):
        arg22 = arg22 + (math.log(x[i], math.e))**2
    arg23 = 0
    for i in range(0, arg11):
        arg23 = arg23 + y[i]*math.log(x[i], math.e)
    AMList = [arg11, arg12, arg13, arg21, arg22, arg23]
    AM = np.array(AMList)
    AM = AM.reshape((2, 3))
    return AM

#generate lnFit Function
def lnFitFunc_CAM(x, Fin):
    m = len(x)
    y = []
    ans = 0
    for i in range(0, m):
        ans = Fin[0] + Fin[1] * math.log(x[i], math.e)
        y.append(ans)
        ans = 0
    return y