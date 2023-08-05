"""
 Module Name:'mypi'
 Path:'<package_path>\\upmath\\src\\mypi'
 Author:Engr. A.K.M. Aminul Islam  
 Email:aminul71bd@gmail.com
 Version:'2.2.2023.01.27'
 Package Version:'2.0.0'
 Description:This module returns the value of PI either through
    a public variable or getPI(prec=36) function
    t=sum(0.015625*(256/(10*i+1)+1/(10*i+9)-32/(4*i+1)-1/(4*i+3)-64/(10*i+3)-4/(10*i+5)-4/(10*i+7))/d)
       where i=0,1,2,3,...
 Date of Last Edit:25th Jun,2020 (Version 2.1.2020.07.13)
 Module Code:CPY-2-1-2020-07-13
>>>
>>> t=time.time();upmath2.mypi.getPI(prec=100);time.time()-t
b10:3.14159265358979323846264338327950288419716939937510582097494459230781640
6286208998628034825342117068
0.07861542701721191 s
>>>
>>> t=time.time();upmath2.mypi.getPI(prec=50);time.time()-t
b10:3.1415926535897932384626433832795028841971693993751
0.03758668899536133 s
>>>
"""
from __future__ import division
from . import upnumber as upn

version='2.2.2023.01.27'

# Calculating pi using Bellard's Formula (most efficient formula)
# It takes 14 iterations to produce a number correct to 34 d.p.
def getPI(prec=36):
    if dataType(prec)!='int': prec=36
    delP=upn.Number('1p-'+str(prec),10,prec=prec)
    prec2=prec+4

    SUM=upn.Number('0',10,prec=prec2);
    t=upn.Number('1.0',10,prec=prec2)
    sign=1;i=0;deno=64

    while(t > delP):        
        a=upn.Number(str(10*i+1),10,prec=prec2)
        b=upn.Number(str(10*i+9),10,prec=prec2)
        c=upn.Number(str(4*i+1),10,prec=prec2)
        d=upn.Number(str(4*i+3),10,prec=prec2)
        e=upn.Number(str(10*i+3),10,prec=prec2)
        f=upn.Number(str(10*i+5),10,prec=prec2)
        g=upn.Number(str(10*i+7),10,prec=prec2)

        t=((256/a)+(1/b)-(32/c)-(1/d)-(64/e)-(4/f)-(4/g))/deno
        deno=deno*1024
        SUM=SUM+sign*t
        sign=-sign
        i=i+1; 

    return SUM.createNewNumber(prec=prec,is_accurate=False) 

# dataType() function returns the type of a data
# type(2.0) returns "(type 'float')"
def dataType(data=None):
    s=str(type(data)).split(' ')[1]
    return s.split("'")[1]

pi=PI=upn.Number('3.141592653589793238462643383279502884',10,36,False)

## ******************************************************************















