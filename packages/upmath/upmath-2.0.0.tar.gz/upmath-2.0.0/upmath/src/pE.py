"""
Module Name:'pE'
Path:'<package_path>\\upmath\\src\\pE.py'
Author: Engr. A.K.M. Aminul Islam
Email:aminul71bd@gmail.com
Last Modified: 2022,Jan,27
Version:'2.1.2023.01.27'
Package Version:'2.0.0'
Description: The function getE() creates the value of e or E
correct to the given precision level
# e=1+1/1!+1/2!+1/3!+...
# >>> t=time.time();pe.getE();time.time()-t
# b10:2.7182818284590452353602874713526625
# 0.015628576278686523 s
# >>> t=time.time();pe.getE(prec=100);time.time()-t
# b10:2.71828182845904523536028747135266249775724709369995957496696762
# 7724076630353547594571382178525166427
# 0.031263113021850586 s
"""
from __future__ import division
from . import upnumber as upn

__version__=version='2.1.2023.01.27'

# getE(prec) returns the exponential value of e='exp(1)'
def getE(prec=36):
    if dataType(prec)!='int': prec=36
    delP=upn.Number('1p-'+str(prec),10,prec=prec);
    prec2=prec+4

    SUM=upn.Number('1',10,prec=prec2);
    t1=upn.Number('1',10,prec=prec2);
    i=0 
    while t1>delP:
        t1=t1/(i+1)
        t1.limitFloatingDigits(prec=prec2)
        SUM=SUM+t1
        i=i+1
    return SUM.createNewNumber(prec=prec,is_accurate=False)

# dataType() function returns the type of a data
# type(2.0) returns "(type 'float')"
def dataType(data=None):
    s=str(type(data)).split(' ')[1]
    return s.split("'")[1]

e=E=upn.Number('2.718281828459045235360287471352662497',10,36,False)

