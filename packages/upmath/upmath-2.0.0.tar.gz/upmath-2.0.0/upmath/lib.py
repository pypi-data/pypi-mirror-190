"""
  Module Name:lib
  Path:'<package_path>\\upmath\\lib'
  Version:1.0.2023.02.03
  Package Version:'2.0.0'
  Previous Version:1.3
  Last Modified: 21st Jan, 2023
  Author:A K M Aminul Islam
  Email:aminul71bd@gmail.com
  Company:Newtonia Ltd

  Description: This module is the gateway of the package 'upmath'. All 
               functions of the source nodules are called here. Users
               call the wrapper functions of this module to reun.
 
  Dependencies: __future__, re, sys, random, pE, mypi, psmf, upnumber, digits

"""

# ================================================================================================
#=================================================================================================
# import the modules
import upmath.src.digits as digits
import upmath.src.upnumber as upn
import upmath.src.psmf as psmf
import upmath.src.pE as pe
import upmath.src.mypi as mypi

# version
__version__=version='1.0.2023.02.03'

# upnumber.Number class
Number=upn.Number

# ----------------------------------- CONSTANTS ---------------------------------------------
# Infinity, Undefined  and other constants
INF=upn.INF
UND=UNDEFINED=upn.UNDEFINED
ZERO=upn.ZERO
ONE=upn.ONE
e=E=pe.E
pi=PI=mypi.PI



# Numeric Digits, Random Numbers and Strings
# ============================================
# numeric digits used in the number systems
base2digits=digits.base2digits
base8digits=digits.base8digits
base10digits=digits.base10digits
base16digits=digits.base16digits
base32digits=digits.base32digits
base64digits=digits.base64digits


# digitChar(digitIndex,base) returns digit character at the given index position
def digitChar(digitIndex=0,base=10):
    return digits.digitChar(digitIndex,base)

# digitIndex(digitIndex,base) returns digit index or position value of the given digit
def digitIndex(digitchar='0',base=10):
    return digits.digitIndex(digitchar,base)

# randomNumberString(length,base) returns a random number string of given base and length
def randomNumberString(length=10,base=10):
    return digits.getRandomNumberString(length,base)

# randomString(length) returns a random base64 string of given length
def randomString(length=10):
    return digits.getRandomString(length)

# randomInteger(length,base) returns a random integer number of given length and given base
def randomInteger(length=5,base=10):
    return digits.randomInteger(length,base)

# randomFloat(length,base) returns a random floating point number of given length and given base
def randomFloat(length=5,base=10):
    return digits.randomFloat(length,base)
	
# ----------------- E and PI of high precision ------------------------
def getE(prec=36):
    return pe.getE(prec)

def getPI(prec=36):
    return mypi.getPI(prec)


# --------------------------------------------------------------------
# Calling the precision standard math functions
# --------------------------------------------------------------------
# dataType() function returns the type of a data
# type(2.0) returns "(type 'float')"
def dataType(data=None):
    s=str(type(data)).split(' ')[1]
    return s.split("'")[1]

# Inverse Function inv(n)
def inv(n=None):
    if dataType(n)==None: raise ValueError("Arguement of inv() not given") 
    if dataType(n) in ['int','float']: return 1/n
    elif dataType(n) == str(upn.__name__)+'.Number':
        return n.__invert__()
    else: raise ValueError("Arguement of inv() not valid")

# To find factorial of an integer
def fact(n=None):
    return psmf.fact(n)


# -------------------- Permutation and Combination Functions -----------------------
def nCr(n=None,r=None):
    return psmf.nCr(n,r)

def nPr(n=None,r=None):
    return psmf.nPr(n,r)

# ----------- Logarithmic, exponential, sqrt, and power Functions ------------------
def ln(x=None,prec=36):
    return psmf.ln(x,prec)

def logE(x=None,prec=36):
    return psmf.ln(x,prec)

def lg(x=None,prec=36):
    return psmf.lg(x,prec)

def log10(x=None,prec=36):
    return psmf.lg(x,prec)
	
def exp(x=None,prec=36):
    return psmf.exp(x,prec)
	
def sqrt(x=None,prec=36):
    return psmf.sqrt(x,prec)

def power(x=None,y=None,prec=36):
    return psmf.power(x,y,prec)


# ---------------------------- Trigonometric Functions ---------------------------
def sin(x=None,unit='d',prec=36):
    return psmf.sin(x,unit,prec)

def cos(x=None,unit='d',prec=36):
    return psmf.cos(x,unit,prec)

def tan(x=None,unit='d',prec=36):
    return psmf.tan(x,unit,prec)
	
def cot(x=None,unit='d',prec=36):
    return psmf.cot(x,unit,prec)

def sec(x=None,unit='d',prec=36):
    return psmf.sec(x,unit,prec)

def cosec(x=None,unit='d',prec=36):
    return psmf.cosec(x,unit,prec)

def csc(x=None,unit='d',prec=36):
    return psmf.cosec(x,unit,prec)

# --------------------- Trigonometric Inverse Functions ------------------------
def asin(x=None,unit='d',prec=36):
    return psmf.asin(x,unit,prec)

def acos(x=None,unit='d',prec=36):
    return psmf.acos(x,unit,prec)

def atan(x=None,unit='d',prec=36):
    return psmf.atan(x,unit,prec)
	
def acot(x=None,unit='d',prec=36):
    return psmf.acot(x,unit,prec)

def asec(x=None,unit='d',prec=36):
    return psmf.asec(x,unit,prec)

def acosec(x=None,unit='d',prec=36):
    return psmf.acosec(x,unit,prec)

def acsc(x=None,unit='d',prec=36):
    return psmf.acosec(x,unit,prec)
	
#--------------------------- Hyperbolic Functions ------------------------
# Trigonometric Functions
def sinh(x=None,prec=36):
    return psmf.sinh(x,prec)

def cosh(x=None,prec=36):
    return psmf.cosh(x,prec)

def tanh(x=None,prec=36):
    return psmf.tanh(x,prec)
	
def coth(x=None,prec=36):
    return psmf.coth(x,prec)

def sech(x=None,prec=36):
    return psmf.sech(x,prec)

def cosech(x=None,prec=36):
    return psmf.cosech(x,prec)

def csch(x=None,prec=36):
    return psmf.cosech(x,prec)

#----------------------- Inverse Hyperbolic Functions ------------------------
def asinh(x=None,prec=36):
    return psmf.asinh(x,prec)

def acosh(x=None,prec=36):
    return psmf.acosh(x,prec)

def atanh(x=None,prec=36):
    return psmf.atanh(x,prec)
	
def acoth(x=None,prec=36):
    return psmf.acoth(x,prec)

def asech(x=None,prec=36):
    return psmf.asech(x,prec)

def acosech(x=None,prec=36):
    return psmf.acosech(x,prec)

def acsch(x=None,prec=36):
    return psmf.acosech(x,prec)

# ------------------- gamma(), beta(), error functions --------------------------

def gamma(x=None,prec=36):
    return psmf.gamma(x,prec)

def beta(x=None,y=None,prec=36):
    return psmf.beta(x,y,prec)

def erf(x=None,prec=36):
    return psmf.erf(x,prec)

def erfc(x=None,prec=36):
    return psmf.erfc(x,prec)

# -------------------- Euler, Bernoulli and Tangent Numbers ----------------------------		
# EulerNumber, BernoulliNumber and TangentNumber Functions
# Inputs are positive integers; for odd inputs, 0 returned
def eulerNumber(n=None):
    return psmf.eulerNumber(n)

def bernoulliNumber(n=None):
    return psmf.bernoulliNumber(n)

def tangentNumber(n=None):
    return psmf.tangentNumber(n)





















