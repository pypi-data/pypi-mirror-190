"""
Module Name:'digits'
Path:'<package_path>\\upmath\\src\\digits.py'
Author: Engr. A.K.M. Aminul Islam
Email:aminul71bd@gmail.com
Version:'1.0.2023.01.27'
Package Version:'2.0.0'
Last Modified: 2023,Jan,31
Description: This module describes and returns the numeric digits u
             used in the different number systems
Digit Tuples:base2digits, base8digits, base10digits, base16digits, base32digits, base64digits
Functions:
    dataType(data=None)							returns data type ('int','float','str','upmath.upnumber.Number')
	digitChar(digitIndex=0,base=10) 			returns digit character of given index
	digitIndex(digitchar='0',base=10)			returns digit index or value of given character
	getRandomNumberString(length=1,base=10)		returns random numeric string of given length and base
	getRandomString(length=10)					returns base 64 random string of given length
    randomInteger(length=10,base=10)			returns a random integer of given base and length
    randomFloat(length=10,base=10)				returns a random float number of given base and length
"""
from __future__ import division
import random
from . import upnumber as upn

__version__=version='1.0.2023.01.27'


# dataType() function returns the type of a data
# type(2.0) returns "(type 'float')"; 
# It returns 'int', 'float', 'str', 'upmath.upNumber.Number'
def dataType(data=None):
    s=str(type(data)).split(' ')[1]
    return s.split("'")[1]


# =========================== Functions on Numeric Characters ============================
# Digits used in the number systems
base2digits=('0','1')
base8digits=('0','1','2','3','4','5','6','7')
base10digits=('0','1','2','3','4','5','6','7','8','9')
base16digits=('0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f')
base32digits=('0','1','2','3','4','5','6','7','8','9','a','b','c','d','e',\
             'f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v')
base64digits=('0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g',\
            'h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',\
            'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S',\
            'T','U','V','W','X','Y','Z','!','@')


# digitChar(digitIndex,base) returns digit character at the given index position
def digitChar(digitIndex=0,base=10):
    if digitIndex==None or base==None:
        raise ValueError("Argument value of digitChar() not set")
    if dataType(digitIndex)!="int" or digitIndex<0: 
        raise ValueError("Argument of digitChar() is positive integer")
    if base not in [2,8,10,16,32,64]: 
        raise ValueError("Base must be 2, 8, 10, 16, 32 or 64")    

    if base==2:
        if digitIndex>1: raise ValueError("Binary digitIndex is 0 or 1")
        return base2digits[digitIndex]
    elif base==8:
        if digitIndex>7: raise ValueError("Octal digitIndex must be between 0 and 7 inclusive")
        return base8digits[digitIndex]
    elif base==10:
        if digitIndex>9: raise ValueError("Denary digitIndex must be between 0 and 9 inclusive")
        return base10digits[digitIndex]
    elif base==16:
        if digitIndex>15: raise ValueError("Hexadecimal digitIndex must be between 0 and 15 inclusive")
        return base16digits[digitIndex]		
    elif base==32:
        if digitIndex>31: raise ValueError("Base32 digitIndex must be between 0 and 31 inclusive")
        return base32digits[digitIndex]
    elif base==64:
        if digitIndex>63: raise ValueError("Base64 digitIndex must be between 0 and 63 inclusive")
        return base64digits[digitIndex]		


# digitIndex(digitIndex,base) returns digit index or position of the given digit
def digitIndex(digitchar='0',base=10):
    if digitchar==None or base==None:
        raise ValueError("Argument value of digitIndex() not set")
    if dataType(digitchar)!="str" or len(digitchar)!=1: 
        raise ValueError("'digitchar' argument of digitIndex() must be a single character")
    if base not in [2,8,10,16,32,64]: 
        raise ValueError("Base must be 2, 8, 10, 16, 32 or 64")

    if base==2:
        for i in range(2):
            if digitchar==base2digits[i]:return i
        raise ValueError("Invalid binary character")
    elif base==8:
        for i in range(8):
            if digitchar==base8digits[i]:return i
        raise ValueError("Invalid octal character")
    elif base==10:
        for i in range(10):
            if digitchar==base10digits[i]:return i
        raise ValueError("Invalid denary character")
    elif base==16:
        for i in range(16):
            if digitchar==base16digits[i]:return i
        raise ValueError("Invalid hexadecimal character")
    elif base==32:
        for i in range(32):
            if digitchar==base32digits[i]:return i
        raise ValueError("Invalid base32 number character")
    elif base==64:
        for i in range(64):
            if digitchar==base64digits[i]:return i
        raise ValueError("Invalid base64 number character")


# getRandomNumberString(length,base) returns a random number string of given base and length
def getRandomNumberString(length=1,base=10):
    if length==None or base==None:
        raise ValueError("Argument value of getRandomNumberString() not set")
    if dataType(length)!="int" or dataType(base)!="int" or length<0 or base<0: 
        raise ValueError("Arguments of getRandomNumberString() are positive integers")
    if base not in [2,8,10,16,32,64]: 
        raise ValueError("Base must be 2, 8, 10, 16, 32 or 64")
    s=""
    for i in range(length):
        indx=int(random.random()*base)
        if base==2: s=s+base2digits[indx]
        elif base==8: s=s+base8digits[indx]
        elif base==10: s=s+base10digits[indx]
        elif base==16: s=s+base16digits[indx]
        elif base==32: s=s+base32digits[indx]
        elif base==64: s=s+base64digits[indx]
    return s

# getRandomString(length) returns a random base64 string of given length	
def getRandomString(length=10):
    if length==None and dataType(length)!="int": 
        raise ValueError("Invalid length of getRandomString()")
    return getRandomNumberString(length,64)

# randomInteger(length=10,base=10) creates a random integer number of given length and base
def randomInteger(length=10,base=10):
    if length==None or base==None:
        raise ValueError("Argument value of randomInteger() not set")
    if dataType(length)!="int" or dataType(base)!="int" or length<0 or base<0: 
        raise ValueError("Arguments of randomInteger() must be positive integers")
    if base not in [2,8,10,16,32,64]: 
        raise ValueError("Base must be 2, 8, 10, 16, 32 or 64")
    s=getRandomNumberString(length,base);c='0'
    while(c=='0'):
        c=getRandomNumberString(1,base)
    s=c+s[1:]
    return upn.Number(s,base,prec=length,is_accurate=True)

# randomFloat(length=10,base=10) creates a random floating point number of given length and base
def randomFloat(length=10,base=10):
    if length==None or base==None:
        raise ValueError("Argument value of randomFloat() not set")
    if dataType(length)!="int" or dataType(base)!="int" or length<0 or base<0: 
        raise ValueError("Arguments of randomFloat() must be positive integers")
    if base not in [2,8,10,16,32,64]: 
        raise ValueError("Base must be 2, 8, 10, 16, 32 or 64")
    if length<2:length=2
    s=str(randomInteger(length,base))[4:];
    dotposition=int(random.random()*(length))
    if dotposition==0:
        s='0.'+s
    elif dotposition==length:
        s=s+'.0'
    else:s=s[:dotposition]+"."+s[dotposition:]
    return upn.Number(s,base,prec=length,is_accurate=True)











	
