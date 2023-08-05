"""
   Module Name: psmf (precisional standard math functions)
   Path:'<package_path>\\upmath\\src\\psmf.py'
   Author:Engr. A.K.M. Aminul Islam
   Email:aminul71bd@gmail.com
   Date: 2020,July,15
   Version:'2.7.2023.02.03'
   Package Version:'2.0.0'
   Last Modified:2023/02/03
   Description:This module includes the standard math functions defined by npysoft.

	       psmf/PSMF=Precisional Standard Math Functions
               All functions can take upnumber (universal precisional numbers) 
               as input, process them and returns upnumber. Functions can generate
               numbers correct to the given precision.

               Numbers, other than denary, are converted to denary first and the
               the number returned is also denary.

               Mathematical Functions present here (n=integer, x=any number)
               ==============================================================
               1) fact(n)			returns factorial of given positive integer
               2) nCr(n,r)			returns no. of different combinations of r items from n items
               3) nPr(n,r)			returns no. of different permutations of r items from n items

               Logarithmic, Evponential Functions
               ---------------------------------------
               4) ln2(prec=36)			returns the value of ln2 correct to the given precision
               5) ln3(prec=36)			returns the value of ln3 correct to the given precision
               6) ln10(prec=36)			returns the value of ln10 correct to the given precision
               7) ln(x,prec=36)			returns the value of ln(x) correct to the given precision
               8) lg(x,prec=36)			returns the value of (10 based) lg(x) correct to the given precision
              9) exp(x,prec=36)		returns the value of e^(x) correct to the given precision
              10) sqrt2(prec=36)		returns the value of square root of 2 correct to the given precision
              11) sqrt(x,prec=36)		returns the value of square root of x correct to the given precision
              12) power(x,y,prec=36)		returns the value of x^y or x**y correct to the given precision

		Trigonometric Functions
		-------------------------
	      13) sin(x,unit='d',prec=36)	returns the value of sin(x) correct to the given precision	
	      14) cos(x,unit='d',prec=36)	returns the value of sin(x) correct to the given precision
	      15) tan(x,unit='d',prec=36)	returns the value of sin(x) correct to the given precision
	      16) cot(x,unit='d',prec=36)	returns the value of sin(x) correct to the given precision
	      17) sec(x,unit='d',prec=36)	returns the value of sin(x) correct to the given precision
	      18) cosec(x,unit='d',prec=36)	returns the value of sin(x) correct to the given precision
	      19) asin(x,unit='d',prec=36)	returns the value of sin(x) correct to the given precision	
	      20) acos(x,unit='d',prec=36)	returns the value of sin(x) correct to the given precision
	      21) atan(x,unit='d',prec=36)	returns the value of sin(x) correct to the given precision
	      22) acot(x,unit='d',prec=36)	returns the value of sin(x) correct to the given precision
	      23) asec(x,unit='d',prec=36)	returns the value of sin(x) correct to the given precision
	      24) acosec(x,unit='d',prec=36)	returns the value of sin(x) correct to the given precision

		Hyperbolic Functions
		-------------------------
	      25) sinh(x,prec=36)		returns the value of sinh(x) correct to the given precision	
	      26) cosh(x,prec=36)		returns the value of cosh(x) correct to the given precision
	      27) tanh(x,prec=36)		returns the value of tanh(x) correct to the given precision
	      28) coth(x,prec=36)		returns the value of coth(x) correct to the given precision
	      29) sech(x,prec=36)		returns the value of sech(x) correct to the given precision
	      30) cosech(x,prec=36)		returns the value of cosech(x) correct to the given precision
	      31) asinh(x,prec=36)		returns the value of asinh(x) correct to the given precision	
	      32) acosh(x,prec=36)		returns the value of acosh(x) correct to the given precision
	      33) atanh(x,prec=36)		returns the value of atanh(x) correct to the given precision
	      34) acoth(x,prec=36)		returns the value of acoth(x) correct to the given precision
	      35) asech(x,prec=36)		returns the value of asech(x) correct to the given precision
	      36) acosech(x,prec=36)		returns the value of acosech(x) correct to the given precision

		Gamma, Beta and Error Functions
		---------------------------------
	      37) gamma(x,prec=36)		returns the value of gamma(x) correct to the given precision	
	      38) beta(x,prec=36)		returns the value of beta(x) correct to the given precision
	      39) erf(x,prec=36)		returns the value of erf(x) correct to the given precision
	      40) erfc(x,prec=36)		returns the value of erfc(x) correct to the given precision

		Numbers of Number Theory
		---------------------------------
	      41) eulerNumber(r)		returns the eulerNumber(r) of the given positive integer
	      42) bernoulliNumber(r)		returns the bernoulliNumber(r) of the given positive integer
	      43) tangentNumber(r)		returns the tangentNumber(r) of the given positive integer	

        Mathematical Constants
	    --------------------------
		1) e or E		2.718281828459045235360287471352662497
	    2) pi or PI		3.141592653589793238462643383279502884
		3) ZERO			0
		4) ONE			1
		5) INF			Infinity
		6) UND or UNDEFINED	UNDEFINED (0/0, inf/inf, Out-of-Domain)
			
   Dependency modules: __future__, upnumber-2.8.2023.02.03, pE-2.1.2023.01.27, mypi-2.2.2023.01.27


"""

# ---------------------------- import section ------------------------
from __future__ import division
from . import upnumber as upn
from . import pE as pe
from . import mypi

# ---------------------------- version info --------------------------
__version__=version="2.7.2023.02.03"

# ------------------------ numeric constants -------------------------
e=E=pe.E
pi=PI=mypi.PI

# ------------------- infinity, undefined constants -------------------
INF=upn.INF
UND=UNDEFINED=upn.UNDEFINED

# -------------------------- zero constants ---------------------------
ZERO=upn.Number('0',base=10,prec=0,is_accurate=True)
ONE=upn.Number('1',base=10,prec=0,is_accurate=True)
# --------------------------- utility functions -----------------------------------
# dataType() function returns the type of a data
# type(2.0) returns "(type 'float')"
def dataType(data=None):
    s=str(type(data)).split(' ')[1]
    return s.split("'")[1]



# ------------------------------- common functions ---------------------------------
# fact(pnum) returns the factorial value of the given precision number object
# >>> smf.fact(10)
# b10:3628800
# >>> smf.fact(upn.Number('1010',2))
# b10:3628800
# >>> smf.fact(upn.Number('i',64))
# b10:6402373705728000
def fact(intnum=None):
    if intnum==None:
        raise ValueError("Argument of fact() missing")
    if dataType(intnum) not in ['int',str(upn.__name__)+'.Number'] or intnum<0:
        raise ValueError("Input is not a positive integer.")
    if dataType(intnum)=='int' and intnum>=0:
        return __fact(intnum)
    elif dataType(intnum)==str(upn.__name__)+'.Number' and intnum.isInteger():
        return _fact(intnum)

# _fact() returns denary integer, a factorial of a upn number
def _fact(upnum=None):
    if upnum.isInteger() and upnum>=0:
        if upnum.getBase()==10:
            return __fact(int(upnum.getNormalizedPart()['ipart']))
        elif upnum.getBase() in [2,8,16,32,64]:
            return __fact(int(upnum.getBase10Part()['ipart']))
    else: raise ValueError("Arguemnt is not a positive integer UPN for fact().")

# __fact() returns denary integer, factorial of a denary integer
def __fact(num=None):
    if num==0 or num==1:return 1
    p=1
    for i in range(2,num+1):p=p*i
    return p #upn.Number(str(p),10,is_accurate=True)


# -----------------------------Binomial Coefficient-----------------------------
# nCr() returns the upn number of different combinations of different r items 
# from different n items where n>=r
# nCr=n!/r!(n-r)!
def nCr(n=None,r=None):
    if n==None or r==None:
        raise ValueError("Invalid arguement of nCr(n,r).")

    if dataType(n)=='int' and dataType(r)=='int' and n>=0 and r>=0  and n>=r:
        return upn.Number(str(__nCr(n,r)),10,is_accurate=True)
    elif dataType(n)=='int' and dataType(r)==str(upn.__name__)+'.Number' and n>=0 and r>=0 and n>=r:
        if r.getBase()==10:
            if r.getNormalizedPart()['fpart']!='0':
                raise ValueError("Invalid arguments of nCr() function")
            r=int(r.getNormalizedPart()['ipart'])
            return upn.Number(str(__nCr(n,r)),10,is_accurate=True)
        elif r.getBase() in [2,8,16,32,64]:
            if r.getBase10Part()['fpart']!='0':
                raise ValueError("Invalid arguments of nCr() function")
            r=int(r.getBase10Part()['ipart'])
            return upn.Number(str(__nCr(n,r)),10,is_accurate=True)
    elif dataType(n)==str(upn.__name__)+'.Number' and dataType(r)=='int' and n>=0 and r>=0 and n>=r:
        if n.getBase()==10:
            if n.getNormalizedPart()['fpart']!='0':
                raise ValueError("Invalid arguments of nCr() function")
            n=int(n.getNormalizedPart()['ipart'])
            return upn.Number(str(__nCr(n,r)),10,is_accurate=True)
        elif n.getBase() in [2,8,16,32,64]:
            if n.getBase10Part()['fpart']!='0':
                raise ValueError("Invalid arguments of nCr() function")
            n=int(n.getBase10Part()['ipart'])
            return upn.Number(str(__nCr(n,r)),10,is_accurate=True)
    elif dataType(n)==str(upn.__name__)+'.Number' and dataType(r)==str(upn.__name__)+'.Number'\
        and n>=0 and r>=0 and n>=r:
        return upn.Number(str(_nCr(n,r)),10,is_accurate=True)
    else:
        raise ValueError("Invalid arguments of nCr() function")

# _nCr(n,r) returns denary integer of upn numbers n,r where n>=r
def _nCr(n=None,r=None):
    if n.getBase()==10 and r.getBase()==10:
        if n.getNormalizedPart()['fpart']!='0' or r.getNormalizedPart()['fpart']!='0':
            raise ValueError("Invalid arguments of nCr() function")
        n=int(n.getNormalizedPart()['ipart'])
        r=int(r.getNormalizedPart()['ipart'])
        return __nCr(n,r)
    elif n.getBase() in [2,8,16,32,64] and r.getBase()==10:
        if n.getBase10PPart()['fpart']!='0' or r.getNormalizedPart()['fpart']!='0':
            raise ValueError("Invalid arguments of nCr() function")
        n=int(n.getBase10Part()['ipart'])
        r=int(r.getNormalizedPart()['ipart'])
        return __nCr(n,r)
    elif n.getBase()==10 and r.getBase() in [2,8,16,32,64]:
        if n.getNormalizedPart()['fpart']!='0' or r.getBase10Part()['fpart']!='0':
            raise ValueError("Invalid arguments of nCr() function")
        n=int(n.getNormalizedPart()['ipart'])
        r=int(r.getBase10Part()['ipart'])
        return __nCr(n,r)
    elif n.getBase() in [2,8,16,32,64] and r.getBase() in [2,8,16,32,64]:
        if n.getBase10Part()['fpart']!='0' or r.getBase10Part()['fpart']!='0':
            raise ValueError("Invalid arguments of nCr() function")
        n=int(n.getBase10Part()['ipart'])
        r=int(r.getBase10Part()['ipart'])
        return __nCr(n,r)

# __nCr(n,r) returns denary integer of denary integers n,r where n>=r
def __nCr(n=None,r=None):
    if r==0 or r==n:return 1
    if r==1 or r==n-1:return n
    if r>n/2:r=n-r	# nCr=nCn-r
    p=1;j=2		# p=product
    for i in range(n-r+1,n+1):
        p=p*i
        if p%j==0 and j<=r:p=p//j; j=j+1
    return p

# nPr() returns the upn number of different permutations of different r items 
# from different n items where n>=r
# nPr=n!/(n-r)!
def nPr(n=None,r=None):
    if n==None or r==None:
        raise ValueError("Invalid arguement of nPr(n,r).")
    if dataType(n)=='int' and dataType(r)=='int' and n>=0 and r>=0 and n>=r:
        return upn.Number(str(__nPr(n,r)),10,is_accurate=True)
    elif dataType(n)=='int' and dataType(r)==str(upn.__name__)+'.Number'and n>=0 and r>=0 and n>=r:
        if r.getBase()==10:
            if r.getNormalizedPart()['fpart']!='0':
                raise ValueError("Invalid arguments of nPr() function")
            r=int(r.getNormalizedPart()['ipart'])
            return upn.Number(str(__nPr(n,r)),10,is_accurate=True)
        elif r.getBase() in [2,8,16,32,64]:
            if r.getBase10Part()['fpart']!='0':
                raise ValueError("Invalid arguments of nPr() function")
            r=int(r.getBase10Part()['ipart'])
            return upn.Number(str(__nPr(n,r)),10,is_accurate=True)
    elif dataType(n)==str(upn.__name__)+'.Number' and dataType(r)=='int' and n>=0 and r>=0 and n>=r:
        if n.getBase()==10:
            if n.getNormalizedPart()['fpart']!='0':
                raise ValueError("Invalid arguments of nPr() function")
            n=int(n.getNormalizedPart()['ipart'])
            return upn.Number(str(__nPr(n,r)),10,is_accurate=True)
        elif n.getBase() in [2,8,16,32,64]:
            if n.getBase10Part()['fpart']!='0':
                raise ValueError("Invalid arguments of nPr() function")
            n=int(n.getBase10Part()['ipart'])
            return upn.Number(str(__nPr(n,r)),10,is_accurate=True)
    elif dataType(n)==str(upn.__name__)+'.Number' and dataType(r)==str(upn.__name__)+'.Number' and\
        n>=0 and r>=0 and n>=r:
        return upn.Number(str(_nPr(n,r)),10,is_accurate=True)
    else:
        raise ValueError("Invalid arguments of nPr() function")

# _nPr(n,r) returns denary integer of upn numbers n,r where n>=r
def _nPr(n=None,r=None):
    if n.getBase()==10 and r.getBase()==10:
        if n.getNormalizedPart()['fpart']!='0' or r.getNormalizedPart()['fpart']!='0':
            raise ValueError("Invalid arguments of nPr() function")
        n=int(n.getNormalizedPart()['ipart'])
        r=int(r.getNormalizedPart()['ipart'])
        return __nPr(n,r)
    elif n.getBase() in [2,8,16,32,64] and r.getBase()==10:
        if n.getBase10Part()['fpart']!='0' or r.getNormalizedPart()['fpart']!='0':
            raise ValueError("Invalid arguments of nPr() function")
        n=int(n.getBase10Part()['ipart'])
        r=int(r.getNormalizedPart()['ipart'])
        return __nPr(n,r)
    elif n.getBase()==10 and r.getBase() in [2,8,16,32,64]:
        if n.getNormalizedPart()['fpart']!='0' or r.getBase10Part()['fpart']!='0':
            raise ValueError("Invalid arguments of nPr() function")
        n=int(n.getNormalizedPart()['ipart'])
        r=int(r.getBase10Part()['ipart'])
        return __nPr(n,r)
    elif n.getBase() in [2,8,16,32,64] and r.getBase() in [2,8,16,32,64]:
        if n.getBase10Part()['fpart']!='0' or r.getBase10Part()['fpart']!='0':
            raise ValueError("Invalid arguments of nPr() function")
        n=int(n.getBase10Part()['ipart'])
        r=int(r.getBase10Part()['ipart'])
        return __nPr(n,r)

# __nPr(n,r) returns denary integer of denary integers n,r where n>=r
def __nPr(n=None,r=None):
    #if r>n:raise ValueError("Invalid arguments of __nPr() function")
    if r==0:return 1
    elif r==1:return n
    elif r==n:return __fact(n)
    p=1
    for i in range(n-r+1,n+1):
        p=p*i    
    return p

# ----------------------- End of Binomial Coefficients---------------------

# ----------------------- logarithmic function -----------------------------
# ln2(prec) returns the natural logarithm of ln(2) correct to the 
# given precision value
# ln2(100)=0.6931471805599453094172321214581765680755001343602552541206
#            800094933936219696947156058633269964186875

# it takes 0.04687 s in 64 bit system for 100 prec
def ln2(prec=36):
    if dataType(prec)!='int' or prec<1: prec=36
    delP=upn.Number('1p-'+str(prec),10,prec=prec)
    prec2=prec+4	

    SUM=upn.Number('0.0',10,prec=prec2);
    t=upn.Number('1.0',10,prec=prec2)
    i=0;m=1
    while(t >= delP):        
        t=upn.Number(str(3*(2*i+1)*m),base=10,prec=prec2)
        t=2/t;
        SUM=SUM+t
        m=m*9; i=i+1
    return SUM.createNewNumber(prec,False)

# ln3(prec) returns the natural logarithm of ln(3) correct to the 
# given precision value
# ln3(100)=1.098612288668109691395245236922525704647490557822749451
#            734694333637494293218608966873615754813732089

# it takes 0.04687 s in 64 bit system for 100 prec
def ln3(prec=36):
    if dataType(prec)!='int' or prec<1: prec=36
    delP=upn.Number('1p-'+str(prec),10,prec=prec)
    prec2=prec+4	

    SUM=upn.Number('0',10,prec=prec2);
    t=upn.Number('1.0',10,prec=prec2)
    i=0;m=2
    while(t > delP):
        t=1/upn.Number(str(m*(2*i+1)),10,prec=prec2)
        SUM=SUM+t #1/upn.Number(str(m*(2*i+1)),10,prec=prec2)
        m=m*4;i=i+1
    SUM=2*SUM
    return SUM.createNewNumber(prec,False)
	
	
# ln10(prec) returns the natural logarithm of ln(10) correct to the 
# given precision value
# ln10(100)=2.3025850929940456840179914546843642076011014886287729760
#            33327900967572609677352480235997205089598298

# it takes 0.08495 s in 64 bit system for 100 prec
def ln10(prec=36):
    if dataType(prec)!='int' or prec<1: prec=36
    delP=upn.Number('1p-'+str(prec),10,prec=prec)
    prec2=prec+4	

    SUM=upn.Number('0.0',10,prec=prec2);
    t=upn.Number('1.0',10,prec=prec2)  #term of the series
    r=1  #loop count

    while(abs(t)>delP):        
        t=upn.Number(str((-1)**(r+1)))/upn.Number(str(r*4**r),10,prec=prec2)		
        SUM=SUM+t
        #if t<0:t=-t
        r=r+1
    SUM=SUM+3*ln2(prec=prec)
    return SUM.createNewNumber(prec,False)



# ----------------------------- start of ln() -----------------------------------
# ln(x,prec) calculates the natural logarithm of an 'upNumber' x
# correct to the given precision by calling _ln(x,prec) or __ln(x,prec)
def ln(x=None,prec=36):
    if x==None:raise ValueError("Invalid arguement of ln(x,prec).")
    if dataType(prec)!='int' or prec<0: prec=36
    if dataType(x) not in ['int','float',str(upn.__name__)+'.Number']:
        raise ValueError("Invalid argument of function ln(x,prec)")
    if dataType(prec)!='int' or prec<1: prec=36

    # convert to denary if x not denary
    if dataType(x) in ['int','float']: x=upn.Number(str(x),10,prec,is_accurate=True)
    if x.getBase() in [2,8,16,32,64]:
        numstr=x.getDict()['base10']['sign']+x.getDict()['base10']['ipart']+'.'+x.getDict()['base10']['fpart']
        x=upn.Number(numstr,10,x.getDict()['base10_prec'],False)
    elif x.getBase()==10:pass
    else: raise ValueError("Invalid base of x in ln(x)")

    if x==0:return upn.Number('<-inf>',10,0,is_accurate=True)
    elif x<0:return upn.Number('<undefined>',10,0,is_accurate=True)
    elif x==1:return upn.Number('0',base=10,prec=1,is_accurate=True)
    elif x==2:return ln2(prec)
    elif x==e or x==E:return upn.Number('1',base=10,prec=1,is_accurate=True)
    elif x==3:return ln3(prec)
    elif x==4:return ln2(prec)*2
    elif x==8:return ln2(prec)*3
    elif x==9:return ln3(prec)*2
    elif x==10:return ln10(prec)
    elif x==16:return ln2(prec)*4
    elif x==27:return ln3(prec)*3
    elif x==32:return ln2(prec)*5
    elif x==64:return ln2(prec)*6
    elif x==81:return ln3(prec)*4
    elif x==100:return ln10(prec)*2

    if dataType(x) in ['int','float']:
        x=upn.Number(str(x),base=10,prec=prec,is_accurate=True)

    delP=upn.Number('1p-'+str(prec),10,prec=prec,is_accurate=True)
    prec2=prec+4	

	# Reducing the number by using exponential form
    # ln(a.b p**d)=ln(a.b)+d*ln(p)	p=10 for denary numbers
    # ln(a b/c p**d)=ln(a b/c)+d*ln(p)	p=10 for denary numbers
    addme=upn.Number('0',10,prec,True)
    ipart=x.getNormalizedPart()['ipart'];
    fpart=x.getNormalizedPart()['fpart'];
    if x.isInteger():
        if len(ipart)==1:
            # x=2^n*a; ln(x)=nln(2) + ln(a)
            n=0
            while(x>2):
                x=x/2
                n=n+1
            addme=addme+n*ln2(prec)
            if x==1: return addme
        elif len(ipart) > 1:
            addme=(len(ipart)-1)*ln10(prec)
            reduced_x_str=ipart[0]+"."+ipart[1:]
            x=upn.Number(reduced_x_str,10,prec,is_accurate=True)
            if x==1:return addme    
    elif x.isFloat():        
        if ipart!='0':
            if len(ipart)>1:
                reduced_x_str=ipart[0]+"."+ipart[1:]+fpart	
                x=upn.Number(reduced_x_str,10,prec,is_accurate=True)
                addme=(len(ipart)-1)*ln10(prec);
        else:
            i=0;
            while fpart[i]=='0':i=i+1
            reduced_x_str=fpart[i]+"."+fpart[i+1:]
            x=upn.Number(reduced_x_str,10,prec,is_accurate=True)
            addme=-(i+1)*ln10(prec);
    # x=2^n*a; ln(x)=nln(2) + ln(a); x between 1 and 9
    n=0;
    while(x>1):
        x=x/2
        n=n+1;
    addme=addme+(n*ln2(prec))
    if x==1 or x==1.0:return addme

    # Finding ln(reduced_x) where 1<x<2
    # ln(1+x)=x/1 - x**2/2 + x**3/3 - x**4/4 + ...
    delP=upn.Number('1p-'+str(prec),10,prec=prec)
    prec2=prec+4
    x=x-1
    SUM=x #Sum upto the first term
    t=x # First Term
    t1=upn.Number('1.0',10,prec=prec2)
    r=1  #loop count
    while(t1>delP):        
        t=(-1)*r*t*x/(r+1);
        SUM=SUM+t;
        if t.getPrecision()>prec+4:
            t=t.createNewNumber(prec=4+prec,is_accurate=False)
            SUM=SUM.createNewNumber(prec=4+prec,is_accurate=False)
        if t<0:t1=-t
        r=r+1
    SUM=SUM+addme
    return SUM.createNewNumber(prec,is_accurate=False)


# lg(x,prec) returns the 10 based logarithm of precision number object x, 
# correct to the given precision
# >>> smf.lg(16.75)
# b10:1.224014811372864043721653839777082527
def lg(x=None,prec=36):
    if x==None:raise ValueError("Invalid arguement of ln(x,prec).")
    if dataType(prec)!='int' or prec<0: prec=36
    if dataType(x) not in ['int','float',str(upn.__name__)+'.Number']:
        raise ValueError("Invalid argument of function lg(x,prec)")
    if dataType(prec)!='int' or prec<1: prec=36
    if x==0:return -INF
    elif x<0:return UNDEFINED
    elif x==1:return upn.Number('0',base=10,prec=1,is_accurate=True)
    elif x==10:return upn.Number('1',base=10,prec=1,is_accurate=True)
    tmp=ln(x,prec)/ln10(prec)
    return tmp.createNewNumber(prec,is_accurate=False)
# -------------------------- END of Logarithmic functions -----------------------

# -------------------------- exponential  functions -----------------------------
# exp(x,prec) returns the exponential value of e**x where x is a denary number
# correct to the given precision value by continued fraction method (CFM)
#>>> t=time.time();upmath.exp(30.2025,prec=50);time.time()-t
#b10:13085161575746.621900584311477674713796006558534808
#0.03124380111694336 s
#>>> t=time.time();upmath.exp(-30.2025,prec=50);time.time()-t
#b10:0.000000000000076422441879013735540900012516851115609336616719269
#0.046874046325683594 s
def exp(x=None,prec=36):
    if dataType(prec)!='int' or prec<1: prec=36
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function exp(x,prec)")

    if x==0: return upn.Number('1',10,prec=prec,is_accurate=True)
    elif x==1 or x==1.0: return pe.getE(prec)
    elif x==-1 or x==-1.0: return (1/pe.getE(prec)).createNewNumber(prec,is_accurate=False)

    # convert to denary if x not denary
    if dataType(x) in ['int','float']: x=upn.Number(str(x),10,prec,is_accurate=True)
    if x.getBase() in [2,8,16,32,64]:
        numstr=x.getDict()['base10']['sign']+x.getDict()['base10']['ipart']+'.'+x.getDict()['base10']['fpart']
        x=upn.Number(numstr,10,x.getDict()['base10_prec'],False)
    elif x.getBase()==10:pass
    else: raise ValueError("Invalid base of x in exp(x)")

    delP=upn.Number('1p-'+str(prec),10,prec=prec);
    prec2=prec+6
    
    x0=x.copy(); m=1 # m=multiplier
    if x>0 and x<1:pass
    elif x>1:
        # reducing x by considering x=r+kln2; e^x=e^r*2^k
        tmp=x/0.69314718; k=int(tmp.getNormalizedPart()['ipart']);
        x = x - k*ln2(prec=prec2);
        for i in range(k):m=2*m
    elif x<-1: # e^-x = 1/e^x
        x=-1*x
        # reducing x by considering x=r+kln2; e^x=e^r*2^k
        tmp=x/0.69314718; k=int(tmp.getNormalizedPart()['ipart']);
        x = x - k*ln2(prec=prec2);
        for i in range(k):m=2*m

    # private function
    def denoFunc(x,y,i,prec):
        t1=upn.Number(str((2+4*i)*y),base=10,prec=prec2)
        t2=upn.Number(str((6+4*i)*y),base=10,prec=prec2)
        return t1+x*x/t2

    # converting x to x/y; where y=1
    i=prec2//4;
    while True:
        deno=denoFunc(x,1,i,prec2)
        for j in range(i,0,-1):
            deno=upn.Number(str(2+4*j),base=10,prec=prec2,is_accurate=False)+x*x/deno
        num1=1+(2*x/(2-x+(x*x/deno)))
        i=i+1
        deno=denoFunc(x,1,i,prec2)
        for j in range(i,0,-1):
            deno=upn.Number(str(2+4*j),base=10,prec=prec2,is_accurate=False)+x*x/deno
        num2=1+(2*x/(2-x+(x*x/deno)))
        if num2==num1:break
        elif num2>num1 and num2-num1 < delP:break
        elif num1>num2 and num1-num2 < delP:break
        i=i+prec2//4;

    if x0>-1 and x0<1:result=num2
    elif x0>1:result=num2*m
    elif x0<-1:
        num2=num2*m; result=1/num2
        #num2.setPrecision(len(str(num2)[4:]))
    return result.createNewNumber(prec,is_accurate=False)


# ---------------------- end of exponential functions --------------------------

# ------------------------- square root estimations ----------------------------
# calculating sqrt(2) by bakhshali iterative method
#>>> t=time.time();psmf.sqrt2(prec=100);time.time()-t
#b10:1.414213562373095048801688724209698078569671875376948073176679
#737990732478462107038850387534327641573
#0.031246185302734375 s
def sqrt2(prec=36):
    if dataType(prec)!='int' or prec<1: prec=36
    delP=upn.Number('1p-'+str(prec),10,prec=prec);
    prec2=prec+4
    
    x=upn.Number('2',base=10,prec=prec2,is_accurate=False)
    xn1=upn.Number('1',base=10,prec=prec2,is_accurate=False)
    xn2=upn.Number('0',base=10,prec=prec2,is_accurate=False)
    diff=xn1-xn2
    while diff > delP:
        an=x/(2*xn1)-xn1/2
        bn=xn1+an
        xn2=bn-an*an/(2*bn)
        diff=xn1-xn2
        if diff<0:diff=-diff
        xn1=xn2
    return xn2.createNewNumber(prec,is_accurate=False)

       
# calculating sqrt(10) by bakhshali iterative method
#>>> t=time.time();psmf.sqrt10(prec=100);time.time()-t
#b10:3.16227766016837933199889354443271853371955513932521682685750485279
#2594438639238221344248108379300295
#0.038083553314208984 s
def sqrt10(prec=36):
    if dataType(prec)!='int' or prec<1: prec=36
    delP=upn.Number('1p-'+str(prec),10,prec=prec);
    prec2=prec+4

    x=upn.Number('10',base=10,prec=prec2,is_accurate=False)
    xn1=upn.Number('3',base=10,prec=prec2,is_accurate=False)
    xn2=upn.Number('2',base=10,prec=prec2,is_accurate=False)
    diff=xn1-xn2
    while diff > delP:
        an=x/(2*xn1)-xn1/2
        bn=xn1+an
        xn2=bn-an*an/(2*bn)
        diff=xn1-xn2
        if diff<0:diff=-diff
        xn1=xn2
    return xn2.createNewNumber(prec,is_accurate=False)


# calculating sqrt(x,prec) by bakhshali iterative method
#>>> t=time.time();psmf.sqrt(50000.258,prec=100);time.time()-t
#b10:223.607374654772958362438380492095343183004540356404090115274092621400731501717
#6923609773676732733127
#0.14745593070983887 s
#>>> t=time.time();psmf.sqrt(50000.258,prec=36);time.time()-t
#b10:223.607374654772958362438380492095343
#0.0 s
def sqrt(x=None,prec=36):
    if dataType(prec)!='int' or prec<1: prec=36
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function sqrt(x,prec)")
    if dataType(x) in ['int','float']:
        x=upn.Number(str(x),base=10,prec=prec,is_accurate=True)
    elif dataType(x)==str(upn.__name__)+".Number":pass
    else: raise ValueError("Invalid number of sqrt(x,prec)") 

    # convert to denary if x not denary
    if x.getBase() in [2,8,16,32,64]:
        numstr=x.getDict()['base10']['sign']+x.getDict()['base10']['ipart']+'.'+x.getDict()['base10']['fpart']
        x=upn.Number(numstr,10,x.getDict()['base10_prec'],False)
    elif x.getBase()==10:pass
    else: raise ValueError("Invalid base of x in sqrt(x)")

    if x<0: return UNDEFINED#upn.Number('<undefined>',10,0,is_accurate=True)
    elif x==2:return sqrt2(prec) #upn.Number(str(__sqrt2(prec))[4:],10,prec).createNewNumber(prec*2,False)
    elif x==10:return sqrt10(prec) #upn.Number(str(__sqrt10(prec))[4:],10,prec).createNewNumber(prec*2,False)

    l=[0,1,4,9,16,25,36,49,64,81,100,0.01,0.04,0.09,0.16,0.25,0.36,0.49,0.64,0.81]
    root=[0,1,2,3,4,5,6,7,8,9,10,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    for i in range(len(l)):
        if x==l[i]:return upn.Number(str(root[i]),10,prec,is_accurate=True)

    # private function
    def rootFunc(x,xn1):
        while True:
            an=x/(2*xn1)-xn1/2
            bn=xn1+an
            xn2=bn-an*an/(2*bn)  
            if xn1==xn2:break
            elif xn2>xn1 and xn2-xn1 < delP:break
            elif xn1>xn2 and xn1-xn2 < delP:break
            xn1=xn2
        return xn2

    delP=upn.Number('1p-'+str(prec),10,prec=prec);
    if prec<=36: prec2=prec+4
    elif prec>36:prec2=int(1.1*prec)

    if x>1:
        n=0;m=1
        # reducing the number x0 = x * 10^n            
        if x>100:
            while x>=100:                
                x=x/100;n=n+2;m=10*m	# x>=1, x<100
                if x==1:return upn.Number(str(m),base=10,prec=prec,is_accurate=True)

        #x=upn.Number(str(x),base=10,prec=prec2)
        if x<=4: xn2=rootFunc(x,upn.Number('2',base=10,prec=prec2));
        elif x<=9: xn2=rootFunc(x,upn.Number('3',base=10,prec=prec2))
        elif x<=16: xn2=rootFunc(x,upn.Number('4',base=10,prec=prec2))
        elif x<=25: xn2=rootFunc(x,upn.Number('5',base=10,prec=prec2))
        elif x<=36: xn2=rootFunc(x,upn.Number('6',base=10,prec=prec2))
        elif x<=49: xn2=rootFunc(x,upn.Number('7',base=10,prec=prec2))
        elif x<=64: xn2=rootFunc(x,upn.Number('8',base=10,prec=prec2))
        elif x<=81: xn2=rootFunc(x,upn.Number('9',base=10,prec=prec2))
        elif x<100: xn2=rootFunc(x,upn.Number('9',base=10,prec=prec2))
        xn2=xn2*m;
        if xn2.isInteger():return xn2.createNewNumber(prec,is_accurate=True)            
        else: return xn2.createNewNumber(prec,is_accurate=False)

    elif x<1:
        n=0;m=1
        if x<=0.01:
            while x<=0.01:
                x=x*100;n=n-2;m=10*m	# x>0.01, x<=1
                if x==1:
                    num=1/upn.Number(str(m),base=10,prec=prec2)
                    result=upn.Number(str(num)[4:],base=10,is_accurate=True)
                    return result.createNewNumber(prec,result.isAccurate())
           
        if x>=0.81: xn2=rootFunc(x,upn.Number('0.9',base=10,prec=prec2))
        elif x>=0.64: xn2=rootFunc(x,upn.Number('0.8',base=10,prec=prec2))
        elif x>=0.49: xn2=rootFunc(x,upn.Number('0.7',base=10,prec=prec2))
        elif x>=0.36: xn2=rootFunc(x,upn.Number('0.6',base=10,prec=prec2))
        elif x>=0.25: xn2=rootFunc(x,upn.Number('0.5',base=10,prec=prec2))
        elif x>=0.16: xn2=rootFunc(x,upn.Number('0.4',base=10,prec=prec2))
        elif x>=0.09: xn2=rootFunc(x,upn.Number('0.3',base=10,prec=prec2))
        elif x>=0.04: xn2=rootFunc(x,upn.Number('0.2',base=10,prec=prec2))
        elif x>0: xn2=rootFunc(x,upn.Number('0.1',base=10,prec=prec2))

        if m>100:
            num=xn2/m
            return num.createNewNumber(prec,is_accurate=False)
        xn2=xn2/m;        
        return xn2.createNewNumber(prec,is_accurate=False)

# ----------------------- end of square root estimations -------------------------

# ----------------------- power() function ---------------------------
# power(x,y,prec) calculates x**y
# >>> t=time.time();psmf.power(12.47,6.29);time.time()-t
# b10:7816277.90874183493285715989953841593632664
# 0.16991901397705078
# >>> t=time.time();psmf.power(12.47,-6.29);time.time()-t
# b10:0.000000127938132660506602850427035795013608317783
# 0.17138981819152832
# >>>
# >>> t=time.time();psmf.power(-12.47,6.29);time.time()-t
# b10:<UNDEFINED>
# 0.0
# >>> t=time.time();psmf.power(-12.47,-6.29);time.time()-t
# b10:<UNDEFINED>
# 0.0
# >>>
# >>> t=time.time();psmf.power(12.47,6);time.time()-t
# b10:3760094.162052865729
# 0.0
# >>> t=time.time();psmf.power(-12.47,6);time.time()-t
# b10:3760094.162052865729
# 0.0
def power(x=None,y=None,prec=36):
    if dataType(prec)!='int' or prec<1: prec=36
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function power(x,y,prec)")
    if dataType(y) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function power(x,y,prec)")

    # convert to denary if x not denary
    if dataType(x) in ['int','float']: x=upn.Number(str(x),10,prec,is_accurate=True)
    if x.getBase() in [2,8,16,32,64]:
        numstr=x.getDict()['base10']['sign']+x.getDict()['base10']['ipart']+'.'+x.getDict()['base10']['fpart']
        x=upn.Number(numstr,10,x.getDict()['base10_prec'],False)
    elif x.getBase()==10:pass
    else: raise ValueError("Invalid base of x in power(x)")

    # convert to denary if y not denary
    if dataType(y) in ['int','float']: y=upn.Number(str(y),10,prec,is_accurate=True)
    if y.getBase() in [2,8,16,32,64]:
        numstr=y.getDict()['base10']['sign']+y.getDict()['base10']['ipart']+'.'+y.getDict()['base10']['fpart']
        y=upn.Number(numstr,10,y.getDict()['base10_prec'],False)
    elif y.getBase()==10:pass
    else: raise ValueError("Invalid base of y in power(y)")

    # handling exceptional cases ('inf','undefined')
    if x==UNDEFINED or y == UNDEFINED:return UNDEFINED
    elif x==0 and y==0: return UNDEFINED
    elif x<0 and x.isFloat():return UNDEFINED
    elif x<0 and x.isInteger() and y.isFloat():return UNDEFINED
    elif x==0 and y>0: return ZERO
    elif x==0 and y<0: return INF
    elif x==INF and y>0: return INF
    elif x==INF and y<0: return ZERO
    elif x==INF and y==0: return UNDEFINED
    elif x==-INF: return UNDEFINED
    elif x!=INF and y==INF: return INF
    elif x!=INF and y==-INF:return ZERO
     
    # handling 0, 1 cases
    if x==1: return upn.Number('1',10,prec,True)            
    elif y==0: return upn.Number('1',10,prec,True)
    elif y==1: return x

    prec2=prec+6
    prod=upn.Number('1',10,prec2,True)
    if y.isInteger():  # base x can be positive or negative
        if y>0:
            for i in range(int(y)):
                prod=prod*x;
                if prod.getMaxPrecision()>prec2: prod=prod.createNewNumber(prec2,is_accurate=False)
            return prod
        elif y<0:
            y1=-y
            for i in range(int(y1)):
                prod=prod*x;
                if prod.getMaxPrecision()>prec2: prod=prod.createNewNumber(prec2,is_accurate=False)
            return (1/prod).createNewNumber(prec,is_accurate=False)
    elif y.isFloat() and x<0: return UNDEFINED
    elif y.isFloat() and x>0:
        # x^y=x^(m+0.n)=x^m*x^0.n=x^m*e^(0.n*lnx)
        prod1=upn.Number('1',10,prec2,True)
        prod2=upn.Number('1',10,prec2,True)
        ipart=int(y); fpart=y-int(y)
        if y>0:
            for i in range(int(y)):
                prod1=prod1*x;
                if prod1.getMaxPrecision()>prec2: prod1=prod1.createNewNumber(prec2,is_accurate=False)
            prod2=exp((y-int(y))*ln(x,prec2),prec2) 
            return (prod1*prod2).createNewNumber(prec,is_accurate=False)
        elif y<0:
            y1=-y
            for i in range(int(y1)):
                prod1=prod1*x;
                if prod1.getMaxPrecision()>prec2: prod1=prod1.createNewNumber(prec2,is_accurate=False)
            prod2=exp((y1-int(y1))*ln(x,prec2),prec2) 
            return (1/(prod1*prod2)).createNewNumber(prec,is_accurate=False)
			



# ------------------------ END of power() function -------------------



# ---------------------- trigonometric function estimations ------------------------
# sin(x,unit,prec) returns sine of x where x is in degree by default
# It can handle radian too. |x|<pi/2 or 2*|x|<pi
# unit='d','D' for degree, 'r','R','c' for radian
# Domain: {R}	Range: -1<=f(x)<=1
# >>> smf.sin(upn.Number('-200'),prec=50)
# b10:0.34202014332566873304409961468225958076308336751417
# >>> smf.sin(upn.Number('-900'),prec=50)
# b10:0
# >>> smf.sin(upn.Number('450'),prec=50)
# b10:1
def sin(x=None,unit='d',prec=36):
    if x==None:raise ValueError('Argument of sin() missing')
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function sin(x,unit,prec)")
    if unit not in ['d','D','Deg','deg','degre','Degre','r','R','c','rad','Rad','radian','Radian']:
        raise Exception('Unit Error.')
    if dataType(x)==str(upn.__name__)+".Number" and x.getDict()['ipart']=='<INF>':return UNDEFINED
    if dataType(x)==str(upn.__name__)+".Number" and x.getDict()['ipart']=='<UNDEFINED>':return UNDEFINED
    if dataType(prec)!='int' or prec<1: prec=36


    if dataType(x) in ['int','float']:
        x=upn.Number(str(x),base=10,prec=prec,is_accurate=True)
    elif dataType(x)==str(upn.__name__)+".Number":pass
    else: raise ValueError("Invalid number of sin(x,unit,prec)") 

    # checking base of x
    if x.getBase() in [2,8,16,32,64]:
        numstr=x.getDict()['base10']['sign']+x.getDict()['base10']['ipart']+'.'+x.getDict()['base10']['fpart']
        x=upn.Number(numstr,10,x.getDict()['base10_prec'],False)
    elif x.getBase()==10:pass
    else: raise ValueError("Invalid base of x in ln(x)")

    delP=upn.Number('1p-'+str(prec),10,prec=prec);
    prec2=prec+8

    neg=0				# neg=negative sign, 1 for true
    if x<0:
        neg=1
        x=-1*x
    
    PI=mypi.getPI(prec2)
    x1,x2=PI/2,PI/180  
  
    if unit in ['d','D','deg','Deg','degre','Degre']:
        if neg==0:
            if x%30==0 and (x//30)%12 in [0,6]:
                return upn.Number('0',base=10,prec=prec,is_accurate=True)
            elif x%30==0 and (x//30)%12 in [1,5]: 
                return upn.Number('0.5',base=10,prec=prec,is_accurate=True)
            elif x%30==0 and (x//30)%12 in [7,11]:
                return upn.Number('-0.5',base=10,prec=prec,is_accurate=True)
            elif x%30==0 and (x//30)%12==3:
                return upn.Number('1',base=10,prec=prec,is_accurate=True)
            elif x%30==0 and (x//30)%12==9:
                return upn.Number('-1',base=10,prec=prec,is_accurate=True)
        elif neg==1:
            if x%30==0 and (x//30)%12 in [0,6]:
                return upn.Number('0',base=10,prec=prec,is_accurate=True)
            elif x%30==0 and (x//30)%12 in [1,5]: 
                return upn.Number('-0.5',base=10,prec=prec,is_accurate=True)
            elif x%30==0 and (x//30)%12 in [7,11]:
                return upn.Number('0.5',base=10,prec=prec,is_accurate=True)
            elif x%30==0 and (x//30)%12==3:
                return upn.Number('-1',base=10,prec=prec,is_accurate=True)
            elif x%30==0 and (x//30)%12==9:
                return upn.Number('1',base=10,prec=prec,is_accurate=True)
        x=x*x2		# degree converted to radian

    # q=quadrant number, 1=First quadrant, 2=Second quadrant
    # 3=Third quadrant, 4=Fourth quadrant    
    q=1+x//x1-4*((x//x1)//4)
    if neg==1:q=5-q
    # find the basic angle in radian
    if neg==0 and q in [2,4]:x=x1-x%x1
    elif neg==1 and q in [1,3]:x=x1-x%x1
    else:x=x%x1  

    if neg==0:  
        if x==0:return upn.Number('0',base=10,prec=prec,is_accurate=True)
        elif x==PI/2:return upn.Number('1',base=10,prec=prec,is_accurate=True)
        elif x==PI/6:return upn.Number('0.5',base=10,prec=prec,is_accurate=True)
    elif neg==1:  
        if x==0:return upn.Number('0',base=10,prec=prec,is_accurate=True)
        elif x==PI/2:return upn.Number('-1',base=10,prec=prec,is_accurate=True)
        elif x==PI/6:return upn.Number('-0.5',base=10,prec=prec,is_accurate=True)

    i=1				# i=counter
    t,s=x.copy(),x.copy()	# initialization of term and sum
    while(True):        
        t=t*(-1)*x*x/(2*i*(2*i+1))
        if t.getPrecision()>3*prec2:
            t=t.createNewNumber(prec2,False)
        if t>0 and t<delP: break
        elif t<0 and -1*t<delP: break
        s=s+t
        i=i+1 
    if q in [1,2]: return s.createNewNumber(prec,False)
    elif q in [3,4]: return (-1*s).createNewNumber(prec,False)


# cos(x,unit,prec) returns cosine of x where x is in degree by default
# It can handle radian too. |x|<pi/2 or 2*|x|<pi
# unit='d','D' for degree, 'r','R','c' for radian
# Domain: {R}	Range: -1<=f(x)<=1
# >>> smf.cos(upn.Number('-200'),prec=50)
# b10:-0.93969262078590838405410927732473146993620813426446
# >>> smf.cos(upn.Number('-900'),prec=50)
# b10:-1
# >>> smf.cos(upn.Number('450'),prec=50)
# b10:0 
def cos(x=None,unit='d',prec=36):
    if x==None:raise ValueError('Argument of cos() missing')
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function cos(x,unit,prec)")
    if unit not in ['d','D','Deg','deg','degre','Degre','r','R','c','rad','Rad','radian','Radian']:
        raise Exception('Unit Error.')
    if dataType(x)==str(upn.__name__)+".Number" and x.getDict()['ipart']=='<INF>':return UNDEFINED
    if dataType(x)==str(upn.__name__)+".Number" and x.getDict()['ipart']=='<UNDEFINED>':return UNDEFINED
    if dataType(prec)!='int' or prec<1: prec=36

    if dataType(x) in ['int','float']:
        x=upn.Number(str(x),base=10,prec=prec,is_accurate=True)
    elif dataType(x)==str(upn.__name__)+".Number":pass
    else: raise ValueError("Invalid number of cos(x,unit,prec)") 

    # checking base of x
    if x.getBase() in [2,8,16,32,64]:
        numstr=x.getDict()['base10']['sign']+x.getDict()['base10']['ipart']+'.'+x.getDict()['base10']['fpart']
        x=upn.Number(numstr,10,x.getDict()['base10_prec'],False)
    elif x.getBase()==10:pass
    else: raise ValueError("Invalid base of x in cos(x)")

    delP=upn.Number('1p-'+str(prec),10,prec=prec);
    prec2=prec+8

    neg=0				# neg=negative sign, 1 for true
    if x<0:
        neg=1
        x=-1*x
    
    PI=mypi.getPI(prec2)
    x1,x2=PI/2,PI/180  
  
    if unit in ['d','D','deg','Deg','degre','Degre']:
        if x%30==0 and (x//30)%12==0:
            return upn.Number('1',base=10,prec=prec,is_accurate=True)
        elif x%30==0 and (x//30)%12==6:
            return upn.Number('-1',base=10,prec=prec,is_accurate=True)
        elif x%30==0 and (x//30)%12 in [2,10]: 
            return upn.Number('0.5',base=10,prec=prec,is_accurate=True)
        elif x%30==0 and (x//30)%12 in [4,8]:
            return upn.Number('-0.5',base=10,prec=prec,is_accurate=True)
        elif x%30==0 and (x//30)%12 in [3,9]:
            return upn.Number('0',base=10,prec=prec,is_accurate=True)
        x=x*x2		# degree converted to radian

    # q=quadrant number, 1=First quadrant, 2=Second quadrant
    # 3=Third quadrant, 4=Fourth quadrant    
    q=1+x//x1-4*((x//x1)//4)
    if neg==1:q=5-q
    # find the basic angle in radian
    if neg==0 and q in [2,4]:x=x1-x%x1
    elif neg==1 and q in [1,3]:x=x1-x%x1
    else:x=x%x1

    if neg==0 and x==0:return upn.Number('1',base=10,prec=prec,is_accurate=True)
    elif neg==1 and x==0:return upn.Number('-1',base=10,prec=prec,is_accurate=True)
    elif x==PI/2:return upn.Number('0',base=10,prec=prec,is_accurate=True)
    elif x==PI/3:return upn.Number('0.5',base=10,prec=prec,is_accurate=True)

    i=1
    t,s=upn.Number('1',10,prec2),upn.Number('1',10,prec2)	# initialization of term and sum
    while(True):        
        t=t*(-1)*x*x/(2*i*(2*i-1))
        if t.getPrecision()>3*prec2:
            t=t.createNewNumber(prec2,False)
        if t>0 and t<delP: break
        elif t<0 and -1*t<delP: break
        s=s+t
        i=i+1
    if q in [1,4]: return s.createNewNumber(prec,False)
    elif q in [2,3]: return (-1*s).createNewNumber(prec,False)


# tan(x,unit,prec) returns tangent of x where x is in degree by default
# It can handle radian too. |x|<pi/2 or 2*|x|<pi
# unit='d','D' for degree, 'r','R','c' for radian
# Domain: {R}	Range: -inf<=f(x)<=inf
# >>> smf.tan(upn.Number('-200'),prec=50)
# b10:-0.93969262078590838405410927732473146993620813426446
# >>> smf.tan(upn.Number('-900'),prec=50)
# b10:-1
# >>> smf.tan(upn.Number('450'),prec=50)
# b10:0 
def tan(x=None,unit='d',prec=36):
    if x==None:raise ValueError('Argument of tan() missing')
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function tan(x,unit,prec)")
    if unit not in ['d','D','Deg','deg','degre','Degre','r','R','c','rad','Rad','radian','Radian']:
        raise Exception('Unit Error.')
    if dataType(x)==str(upn.__name__)+".Number" and x.getDict()['ipart']=='<INF>':return UNDEFINED
    if dataType(x)==str(upn.__name__)+".Number" and x.getDict()['ipart']=='<UNDEFINED>':return UNDEFINED
    if dataType(prec)!='int' or prec<1: prec=36
 
    if dataType(x) in ['int','float']:
        x=upn.Number(str(x),base=10,prec=prec,is_accurate=True)
    elif dataType(x)==str(upn.__name__)+".Number":pass
    else: raise ValueError("Invalid number of tan(x,unit,prec)") 

    # checking base of x
    if x.getBase() in [2,8,16,32,64]:
        numstr=x.getDict()['base10']['sign']+x.getDict()['base10']['ipart']+'.'+x.getDict()['base10']['fpart']
        x=upn.Number(numstr,10,x.getDict()['base10_prec'],False)
    elif x.getBase()==10:pass
    else: raise ValueError("Invalid base of x in tan(x)")
  
    prec2=prec+8

    neg=0				# neg=negative sign, 1 for true
    if x<0:
        neg=1
        x=-1*x
    
    PI=mypi.getPI(prec2)
    x1,x2=PI/2,PI/180 

    if unit in ['d','D','deg','Deg','degre','Degre']:
        if neg==0:
            if x%45==0 and (x//45)%8 in [0,4]:
                return upn.Number('0',base=10,prec=prec,is_accurate=True)
            elif x%45==0 and (x//45)%8 in [1,5]: 
                return upn.Number('1',base=10,prec=prec,is_accurate=True)
            elif x%45==0 and (x//45)%8 in [3,7]: 
                return upn.Number('-1',base=10,prec=prec,is_accurate=True)
            elif x%45==0 and (x//45)%8==2: 
                return upn.Number('<inf>',base=10,prec=prec,is_accurate=True)
            elif x%45==0 and (x//45)%8==6: 
                return upn.Number('<-inf>',base=10,prec=prec,is_accurate=True)
        elif neg==1:
            if x%45==0 and (x//45)%8 in [0,4]:
                return upn.Number('0',base=10,prec=prec,is_accurate=True)
            elif x%45==0 and (x//45)%8 in [1,5]: 
                return upn.Number('-1',base=10,prec=prec,is_accurate=True)
            elif x%45==0 and (x//45)%8 in [3,7]: 
                return upn.Number('1',base=10,prec=prec,is_accurate=True)
            elif x%45==0 and (x//45)%8==2: 
                return upn.Number('<-inf>',base=10,prec=prec,is_accurate=True)
            elif x%45==0 and (x//45)%8==6: 
                return upn.Number('<inf>',base=10,prec=prec,is_accurate=True)
        x=x*x2		# degree converted to radian

    # q=quadrant number, 1=First quadrant, 2=Second quadrant
    # 3=Third quadrant, 4=Fourth quadrant    
    q=1+x//x1-4*((x//x1)//4)
    if neg==1:q=5-q
    # find the basic angle in radian
    if neg==0 and q in [2,4]:x=x1-x%x1
    elif neg==1 and q in [1,3]:x=x1-x%x1
    else:x=x%x1

    if neg==0:  
        if x==0 or x==PI:return upn.Number('0',base=10,prec=prec,is_accurate=True)
        elif x==PI/4:return upn.Number('1',base=10,prec=prec,is_accurate=True)
        elif x==PI/2:return upn.Number('<inf>',base=10,prec=prec,is_accurate=True)
    elif neg==1:  
        if x==0 or x==PI:return upn.Number('0',base=10,prec=prec,is_accurate=True)
        elif x==PI/4:return upn.Number('-1',base=10,prec=prec,is_accurate=True)
        elif x==PI/2:return upn.Number('<-inf>',base=10,prec=prec,is_accurate=True)

    if q in [1,3]:
        return (sin(x,unit='r',prec=prec2)/cos(x,unit='r',prec=prec2)).createNewNumber(prec,False)
    elif q in [2,4]:
        return (-1*sin(x,unit='r',prec=prec2)/cos(x,unit='r',prec=prec2)).createNewNumber(prec,False)



# cot(x,unit) returns cotangent of x where x is in degree by default
# unit='d','D' for degree, 'r','R','c' for radian
# Domain: {R}	Range: |f(x)|<=infinity
def cot(x=None,unit='d',prec=36):
    if x==None:raise ValueError('Argument of cot() missing')
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function cot(x,unit,prec)")
    if unit not in ['d','D','Deg','deg','degre','Degre','r','R','c','rad','Rad','radian','Radian']:
        raise Exception('Unit Error.')
    if dataType(x)==str(upn.__name__)+".Number" and x.getDict()['ipart']=='<INF>':return UNDEFINED
    if dataType(x)==str(upn.__name__)+".Number" and x.getDict()['ipart']=='<UNDEFINED>':return UNDEFINED
    if dataType(prec)!='int' or prec<1: prec=36

    if dataType(x) in ['int','float']:
        x=upn.Number(str(x),base=10,prec=prec,is_accurate=True)
    elif dataType(x)==str(upn.__name__)+".Number":pass
    else: raise ValueError("Invalid number of cot(x,unit,prec)") 

    # checking base of x
    if x.getBase() in [2,8,16,32,64]:
        numstr=x.getDict()['base10']['sign']+x.getDict()['base10']['ipart']+'.'+x.getDict()['base10']['fpart']
        x=upn.Number(numstr,10,x.getDict()['base10_prec'],False)
    elif x.getBase()==10:pass
    else: raise ValueError("Invalid base of x in cot(x)")
	
    prec2=prec+8

    neg=0				# neg=negative sign, 1 for true
    if x<0:
        neg=1
        x=-1*x
    
    PI=mypi.getPI(prec2)
    x1,x2=PI/2,PI/180  

    if unit in ['d','D','deg','Deg','degre','Degre']:
        if neg==0:
            if x%45==0 and (x//45)%8==0:
                return upn.Number('<inf>',base=10,prec=prec,is_accurate=True)
            elif x%45==0 and (x//45)%8==4:
                return upn.Number('<-inf>',base=10,prec=prec,is_accurate=True)
            elif x%45==0 and (x//45)%8 in [1,5]: 
                return upn.Number('1',base=10,prec=prec,is_accurate=True)
            elif x%45==0 and (x//45)%8 in [3,7]: 
                return upn.Number('-1',base=10,prec=prec,is_accurate=True)
            elif x%45==0 and (x//45)%8 in [2,6]: 
                return upn.Number('0',base=10,prec=prec,is_accurate=True)
        elif neg==1:
            if x%45==0 and (x//45)%8==0:
                return upn.Number('<-inf>',base=10,prec=prec,is_accurate=True)
            elif x%45==0 and (x//45)%8==4:
                return upn.Number('<inf>',base=10,prec=prec,is_accurate=True)
            elif x%45==0 and (x//45)%8 in [1,5]: 
                return upn.Number('-1',base=10,prec=prec,is_accurate=True)
            elif x%45==0 and (x//45)%8 in [3,7]: 
                return upn.Number('1',base=10,prec=prec,is_accurate=True)
            elif x%45==0 and (x//45)%8 in [2,6]: 
                return upn.Number('0',base=10,prec=prec,is_accurate=True)
        x=x*x2		# degree converted to radian

    # q=quadrant number, 1=First quadrant, 2=Second quadrant
    # 3=Third quadrant, 4=Fourth quadrant    
    q=1+x//x1-4*((x//x1)//4)
    if neg==1:q=5-q
    # find the basic angle in radian
    if neg==0 and q in [2,4]:x=x1-x%x1
    elif neg==1 and q in [1,3]:x=x1-x%x1
    else:x=x%x1

    if neg==0:  
        if x==0:return upn.Number('<inf>',base=10,prec=prec,is_accurate=True)
        if x==PI:return upn.Number('<-inf>',base=10,prec=prec,is_accurate=True)
        elif x==PI/4:return upn.Number('1',base=10,prec=prec,is_accurate=True)
        elif x==PI/2:return upn.Number('0',base=10,prec=prec,is_accurate=True)
    elif neg==1:  
        if x==0:return upn.Number('<-inf>',base=10,prec=prec,is_accurate=True)
        if x==PI:return upn.Number('<inf>',base=10,prec=prec,is_accurate=True)
        elif x==PI/4:return upn.Number('-1',base=10,prec=prec,is_accurate=True)
        elif x==PI/2:return upn.Number('0',base=10,prec=prec,is_accurate=True)

    if q in [1,3]:
        return (cos(x,unit='r',prec=prec2)/sin(x,unit='r',prec=prec2)).createNewNumber(prec,False)
    elif q in [2,4]:
        return (-1*cos(x,unit='r',prec=prec2)/sin(x,unit='r',prec=prec2)).createNewNumber(prec,False)


# sec(x,unit) returns secant of x where x is in degree by default
# unit='d','D' for degree, 'r','R','c' for radian
# Domain: {R}	Range: 1<|f(x)|<=infinity
def sec(x=None,unit='d',prec=36):
    if x==None:raise ValueError('Argument of sec() missing')
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function sec(x,unit,prec)")
    if unit not in ['d','D','Deg','deg','degre','Degre','r','R','c','rad','Rad','radian','Radian']:
        raise Exception('Unit Error.')
    if dataType(x)==str(upn.__name__)+".Number" and x.getDict()['ipart']=='<INF>':return UNDEFINED
    if dataType(x)==str(upn.__name__)+".Number" and x.getDict()['ipart']=='<UNDEFINED>':return UNDEFINED
    if dataType(prec)!='int' or prec<1: prec=36

    if dataType(x) in ['int','float']:
        x=upn.Number(str(x),base=10,prec=prec,is_accurate=True)
    elif dataType(x)==str(upn.__name__)+".Number":pass
    else: raise ValueError("Invalid number of sec(x,unit,prec)") 

    # checking base of x
    if x.getBase() in [2,8,16,32,64]:
        numstr=x.getDict()['base10']['sign']+x.getDict()['base10']['ipart']+'.'+x.getDict()['base10']['fpart']
        x=upn.Number(numstr,10,x.getDict()['base10_prec'],False)
    elif x.getBase()==10:pass
    else: raise ValueError("Invalid base of x in sec(x)")

    prec2=prec+8

    neg=0				# neg=negative sign, 1 for true
    if x<0:
        neg=1
        x=-1*x
    
    PI=mypi.getPI(prec2)
    x1,x2=PI/2,PI/180  
  
    if unit in ['d','D','deg','Deg','degre','Degre']:
        if x%30==0 and (x//30)%12==0:
            return upn.Number('1',base=10,prec=prec,is_accurate=True)
        elif x%30==0 and (x//30)%12==6:
            return upn.Number('-1',base=10,prec=prec,is_accurate=True)
        elif x%30==0 and (x//30)%12 in [2,10]: 
            return upn.Number('2',base=10,prec=prec,is_accurate=True)
        elif x%30==0 and (x//30)%12 in [4,8]:
            return upn.Number('-2',base=10,prec=prec,is_accurate=True)
        elif x%30==0 and (x//30)%12 in [3,9]:
            return upn.Number('<inf>',base=10,prec=prec,is_accurate=True)
        x=x*x2		# degree converted to radian

    # q=quadrant number, 1=First quadrant, 2=Second quadrant
    # 3=Third quadrant, 4=Fourth quadrant    
    q=1+x//x1-4*((x//x1)//4)
    if neg==1:q=5-q
    # find the basic angle in radian
    if neg==0 and q in [2,4]:x=x1-x%x1
    elif neg==1 and q in [1,3]:x=x1-x%x1
    else:x=x%x1

    if neg==0 and x==0:return upn.Number('1',base=10,prec=prec,is_accurate=True)
    elif neg==1 and x==0:return upn.Number('-1',base=10,prec=prec,is_accurate=True)
    elif x==PI/2:return upn.Number('<inf>',base=10,prec=prec,is_accurate=True)
    elif x==PI/3:return upn.Number('2',base=10,prec=prec,is_accurate=True)

    if q in [1,4]:
        return (1/cos(x,unit='r',prec=prec2)).createNewNumber(prec,False)
    elif q in [2,3]:
        return (-1/cos(x,unit='r',prec=prec2)).createNewNumber(prec,False)


# cosec(x,unit) returns cosecant of x where x is in degree by default
# unit='d','D' for degree, 'r','R','c' for radian
# Domain: {R}	Range: 1<|f(x)|<=infinity
def cosec(x=None,unit='d',prec=36):
    if x==None:raise ValueError('Argument of cosec() missing')
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function cosec(x,unit,prec)")
    if unit not in ['d','D','Deg','deg','degre','Degre','r','R','c','rad','Rad','radian','Radian']:
        raise Exception('Unit Error.')
    if dataType(x)==str(upn.__name__)+".Number" and x.getDict()['ipart']=='<INF>':return UNDEFINED
    if dataType(x)==str(upn.__name__)+".Number" and x.getDict()['ipart']=='<UNDEFINED>':return UNDEFINED
    if dataType(prec)!='int' or prec<1: prec=36

    if dataType(x) in ['int','float']:
        x=upn.Number(str(x),base=10,prec=prec,is_accurate=True)
    elif dataType(x)==str(upn.__name__)+".Number":pass
    else: raise ValueError("Invalid number of cosec(x,unit,prec)") 

    # checking base of x
    if x.getBase() in [2,8,16,32,64]:
        numstr=x.getDict()['base10']['sign']+x.getDict()['base10']['ipart']+'.'+x.getDict()['base10']['fpart']
        x=upn.Number(numstr,10,x.getDict()['base10_prec'],False)
    elif x.getBase()==10:pass
    else: raise ValueError("Invalid base of x in cosec(x)")

    prec2=prec+8

    neg=0				# neg=negative sign, 1 for true
    if x<0:
        neg=1
        x=-1*x
    
    PI=mypi.getPI(prec2)
    x1,x2=PI/2,PI/180  
  
    if unit in ['d','D','deg','Deg','degre','Degre']:
        if neg==0:
            if x%30==0 and (x//30)%12 in [0,6]:
                return upn.Number('<inf>',base=10,prec=prec,is_accurate=True)
            elif x%30==0 and (x//30)%12 in [1,5]: 
                return upn.Number('2',base=10,prec=prec,is_accurate=True)
            elif x%30==0 and (x//30)%12 in [7,11]:
                return upn.Number('-2',base=10,prec=prec,is_accurate=True)
            elif x%30==0 and (x//30)%12==3:
                return upn.Number('1',base=10,prec=prec,is_accurate=True)
            elif x%30==0 and (x//30)%12==9:
                return upn.Number('-1',base=10,prec=prec,is_accurate=True)
        elif neg==1:
            if x%30==0 and (x//30)%12 in [0,6]:
                return upn.Number('<inf>',base=10,prec=prec,is_accurate=True)
            elif x%30==0 and (x//30)%12 in [1,5]: 
                return upn.Number('-2',base=10,prec=prec,is_accurate=True)
            elif x%30==0 and (x//30)%12 in [7,11]:
                return upn.Number('2',base=10,prec=prec,is_accurate=True)
            elif x%30==0 and (x//30)%12==3:
                return upn.Number('-1',base=10,prec=prec,is_accurate=True)
            elif x%30==0 and (x//30)%12==9:
                return upn.Number('1',base=10,prec=prec,is_accurate=True)
        x=x*x2		# degree converted to radian

    # q=quadrant number, 1=First quadrant, 2=Second quadrant
    # 3=Third quadrant, 4=Fourth quadrant    
    q=1+x//x1-4*((x//x1)//4)
    if neg==1:q=5-q
    # find the basic angle in radian
    if neg==0 and q in [2,4]:x=x1-x%x1
    elif neg==1 and q in [1,3]:x=x1-x%x1
    else:x=x%x1  

    if neg==0:  
        if x==0:return upn.Number('<inf>',base=10,prec=prec,is_accurate=True)
        elif x==PI/2:return upn.Number('-1',base=10,prec=prec,is_accurate=True)
        elif x==PI/6:return upn.Number('2',base=10,prec=prec,is_accurate=True)
    elif neg==1:  
        if x==0:return upn.Number('<inf>',base=10,prec=prec,is_accurate=True)
        elif x==PI/2:return upn.Number('1',base=10,prec=prec,is_accurate=True)
        elif x==PI/6:return upn.Number('-2',base=10,prec=prec,is_accurate=True)

    if q in [1,2]:
        return (1/sin(x,unit='r',prec=prec2)).createNewNumber(prec,False)
    elif q in [3,4]:
        return (-1/sin(x,unit='r',prec=prec2)).createNewNumber(prec,False)


# --------------------------Trigonometric Inverse Functions--------------------------------
# asin(x,unit,prec) returns radian value of inverse of sine of x
# Default output unit is degree
# Domain: -1<=x<=1	Range: -90<=f(x)<=90 or -pi/2<=f(x)<=pi/2
# unit='d','D','Deg','deg','degre','Degre' for degree, 'r','R','c','rad','Rad','radian','Radian' for radian
# Multiple solutions exist.

# asin(x)=x + 1*x^3/2*3 + 1*3*x^5/2*4*5 + 1*3*5*x^7/2*4*6*7 + ... where |x|<1
# >>> t=time.time(); psmf.asin(-0.785,unit='d');time.time()-t
# b10:-51.7206782620722622846032596702957142
# 0.18749403953552246 s
# >>> t=time.time(); psmf.asin(0.255,unit='d');time.time()-t
# b10:14.7735851509074761517220873588902973
# 0.046874284744262695 s
# >>> t=time.time(); psmf.asin(0.987,unit='d');time.time()-t
# b10:80.7512952089710835437201655715937059
# 2.578071117401123 s
def asin(x=None,unit='d',prec=36):
    if x==None:raise ValueError('Argument of asin() missing')
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function asin(x,unit,prec), |x|<=1")
 
    if unit not in ['d','D','Deg','deg','degre','Degre','r','R','c','rad','Rad','radian','Radian']:
        raise ValueError('Invalid Angle Unit') 
    if dataType(prec)!='int' or prec<1: prec=36
    if dataType(x) in ['int','float']:
        x=upn.Number(str(x),base=10,prec=prec,is_accurate=True)
    elif dataType(x)==str(upn.__name__)+".Number":pass
    else: raise ValueError("Invalid number of asin(x,unit,prec)") 

    # checking base of x
    if x.getBase() in [2,8,16,32,64]:
        numstr=x.getDict()['base10']['sign']+x.getDict()['base10']['ipart']+'.'+x.getDict()['base10']['fpart']
        x=upn.Number(numstr,10,x.getDict()['base10_prec'],False)
    elif x.getBase()==10:pass
    else: raise ValueError("Invalid base of x in asin(x)")	
	
    if x<-1 or x>1:return UNDEFINED	
    if x.getDict()['ipart']=='<UNDEFINED>':return UNDEFINED 

    prec2=prec+8
    PI=mypi.getPI(prec2)

    if unit in ['r','R','c','rad','Rad','radian','Radian']:
        if x==0:return ZERO
        elif x==0.5:return (PI/6).createNewNumber(prec,False)
        elif x==1:return (PI/2).createNewNumber(prec,False)
        elif x==-0.5:return (-PI/6).createNewNumber(prec,False)
        elif x==-1:return (-PI/2).createNewNumber(prec,False)
    elif unit in ['d','D','deg','Deg','degre','Degre']:
        if x==0:return ZERO
        elif x==0.5:return upn.Number('30',base=10,prec=prec,is_accurate=True)
        elif x==1:return upn.Number('90',base=10,prec=prec,is_accurate=True)
        elif x==-0.5:return upn.Number('-30',base=10,prec=prec,is_accurate=True)
        elif x==-1:return upn.Number('-90',base=10,prec=prec,is_accurate=True)

    delP=upn.Number('1p-'+str(prec),10,prec=prec);    
    t=x; s=x; i=upn.Number('1',10,prec,True);
    t1=upn.Number('1',10,prec,True)
    while t1>delP:        
        t=t*x*x*(2*i-1)*(2*i-1)*(1/(2*i*(2*i+1)))
        s=s+t;
        if t.getPrecision()>prec2:
            t=t.createNewNumber(prec2,False)
            s=s.createNewNumber(prec2,False)
        if t<0:t1=-t
        else:t1=t
        i=i+1
    if unit in ['r','R','c','rad','Rad','radian','Radian']: 
        return s.createNewNumber(prec,False)
    elif unit in ['d','D','deg','Deg','degre','Degre']:
        return (s*180/PI).createNewNumber(prec,False)


# acos(x,unit,prec) returns radian or degree value of inverse of cosine of x
# Default output unit is degree
# Domain: -1<=x<=1	Range: -90<=f(x)<=90 or -pi/2<=f(x)<=pi/2
# unit='d','D' for degree, 'r','R','c' for radian
# Multiple solutions exist.
#
# acos(x)=PI/2-asin(x)
# >>> t=time.time(); psmf.acos(-0.567,unit='d');time.time()-t
# b10:124.541290458534002972870608842846589
# 0.09374570846557617 s
# >>> t=time.time(); psmf.acos(0.478,unit='d');time.time()-t
# b10:61.4451398641886103400687761177581865
# 0.07812094688415527 s
# >>> t=time.time(); psmf.acos(0.878,unit='d');time.time()-t
# b10:28.5979622215734677721780638643236638
# 0.3281211853027344 s
def acos(x=None,unit='d',prec=36):
    if x==None:raise ValueError('Argument of acos() missing')
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function acos(x,unit,prec), |x|<=1")
    if unit not in ['d','D','Deg','deg','degre','Degre','r','R','c','rad','Rad','radian','Radian']:
        raise ValueError('Invalid Angle Unit') 
    if dataType(prec)!='int' or prec<1: prec=36
    if dataType(x) in ['int','float']:
        x=upn.Number(str(x),base=10,prec=prec,is_accurate=True)
    elif dataType(x)==str(upn.__name__)+".Number":pass
    else: raise ValueError("Invalid number of acos(x,unit,prec)") 
    # checking base of x
    if x.getBase() in [2,8,16,32,64]:
        numstr=x.getDict()['base10']['sign']+x.getDict()['base10']['ipart']+'.'+x.getDict()['base10']['fpart']
        x=upn.Number(numstr,10,x.getDict()['base10_prec'],False)
    elif x.getBase()==10:pass
    else: raise ValueError("Invalid base of x in acos(x)")	

    if x.getDict()['ipart']=='<UNDEFINED>':return UNDEFINED 
    elif x>1 or x<-1 or x==INF or x==-INF:return UNDEFINED

    prec2=prec+8
    PI=mypi.getPI(prec2)

    if unit in ['r','R','c','rad','Rad','radian','Radian']:
        if x==0:return (PI/2).createNewNumber(prec,False)
        elif x==0.5 or x==-0.5:return (PI/3).createNewNumber(prec,False)
        elif x==1:return ZERO
        elif x==-1:return PI.createNewNumber(prec,False)
    elif unit in ['d','D','deg','Deg','degre','Degre']:
        if x==0:return upn.Number('90',base=10,prec=prec,is_accurate=True)
        elif x==0.5 or x==-0.5:return upn.Number('60',base=10,prec=prec,is_accurate=True)
        elif x==1:return ZERO
        elif x==-1:return upn.Number('180',base=10,prec=prec,is_accurate=True)

    delP=upn.Number('1p-'+str(prec),10,prec=prec);	
    t=x; s=x; i=upn.Number('1',10,prec,True);
    t1=upn.Number('1',10,prec,True)
    while t1>delP:        
        t=t*x*x*(2*i-1)*(2*i-1)*(1/(2*i*(2*i+1)))
        s=s+t;
        if t.getPrecision()>prec2:
            t=t.createNewNumber(prec2,False)
            s=s.createNewNumber(prec2,False)
        if t<0:t1=-t
        else:t1=t
        i=i+1
    if unit in ['r','R','c','rad','Rad','radian','Radian']: 
        return (PI/2-s).createNewNumber(prec,False)
    elif unit in ['d','D','deg','Deg','degre','Degre']:
        return (90-s*180/PI).createNewNumber(prec,False)


# atan(x,unit,prec) returns radian or degree value of inverse of tangent of x
# Domain: {R}	Range: -90<=f(x)<=90 or -PI/2<=f(x)<=PI/2
# Multiple solutions exist.

# atan(x)=SUM=x-x^3/3+x^5/5-x^7/7 + ... where |x|<1
#        =PI/2 -SUM, where x=1/x and x>1
#        ==PI/2-SUM where x=1/x and x<-1
# >>> t=time.time(); psmf.atan(0.02,unit='d');time.time()-t
# b10:1.14576283817510340227362748412511427
# 0.031246185302734375 s
# >>>
# >>> t=time.time(); psmf.atan(0.02,unit='d');time.time()-t
# b10:1.14576283817510340227362748412511427
# 0.031247854232788086 s
# >>> t=time.time(); psmf.atan(0.52,unit='d');time.time()-t
# b10:27.4744316262771307710895033688780267
# 0.06249666213989258 s
# >>> t=time.time(); psmf.atan(0.852,unit='d');time.time()-t
# b10:40.4309972549392401218318681353798316
# 0.20311856269836426 s
# >>> t=time.time(); psmf.atan(5,unit='d');time.time()-t
# b10:78.6900675259797869135254945616601394
# 0.046880483627319336 s
# >>> t=time.time(); psmf.atan(-1.5,unit='d');time.time()-t
# b10:-56.3099324740202130864745054383398606
# 0.12499403953552246 s
def atan(x=None,unit='d',prec=36):
    if x==None:raise ValueError('Argument of atan() missing')
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function atan(x,unit,prec), |x|<=1")
    if unit not in ['d','D','Deg','deg','degre','Degre','r','R','c','rad','Rad','radian','Radian']:
        raise ValueError('Invalid Angle Unit') 
    if dataType(prec)!='int' or prec<1: prec=36
    if dataType(x) in ['int','float']:
        x=upn.Number(str(x),base=10,prec=prec,is_accurate=True)
    elif dataType(x)==str(upn.__name__)+".Number":pass
    else: raise ValueError("Invalid number of atan(x,unit,prec)") 
    # checking base of x
    if x.getBase() in [2,8,16,32,64]:
        numstr=x.getDict()['base10']['sign']+x.getDict()['base10']['ipart']+'.'+x.getDict()['base10']['fpart']
        x=upn.Number(numstr,10,x.getDict()['base10_prec'],False)
    elif x.getBase()==10:pass
    else: raise ValueError("Invalid base of x in atan(x)")	

    prec2=prec+8
    PI=mypi.getPI(prec2)

    if x.getDict()['ipart']=='<UNDEFINED>':return UNDEFINED 
    elif x==INF:return (PI/2).createNewNumber(prec,True)
    elif x==-INF:return (-PI/2).createNewNumber(prec,True)
   
    # returning the standard values
    if unit in ['d','D','deg','Deg','degre','Degre']:
        if x==0:return ZERO
        elif x==1:return upn.Number('45',base=10,prec=prec,is_accurate=True)
        elif x==-1:return upn.Number('-45',base=10,prec=prec,is_accurate=True)
    elif unit in ['r','R','c','rad','Rad','radian','Radian']:
        if x==0:return ZERO
        elif x==1:return (PI/4).createNewNumber(prec,False)
        elif x==-1:return (-PI/4).createNewNumber(prec,False)

    # atan(x) where |x|<1
    def my_atan(x):
        delP=upn.Number('1p-'+str(prec),10,prec=prec);
        t=x;s=x;r=1
        t1=upn.Number('1',10,prec,True)
        while t1>delP:
            t=-t*x*x*(2*r-1)/(2*r+1)
            s=s+t
            if t.getPrecision()>prec2:
                t=t.createNewNumber(prec2,False)
                s=s.createNewNumber(prec2,False)
            if t<0:t1=-t
            r=r+1
        return s

    if unit in ['d','D','deg','Deg','degre','Degre']:
        if x>-1 and x<1:
            result=my_atan(x);
            return (result*180/PI).createNewNumber(prec,False)
        elif x>1:
            result=my_atan(1/x)
            return (90-180*result/PI).createNewNumber(prec,False)
        elif x<-1:
            x=abs(x); result=my_atan(1/x)
            return (180*result/PI-90).createNewNumber(prec,False)
    elif unit in ['r','R','c','rad','Rad','radian','Radian']:
        if x>-1 and x<1: 
            result=my_atan(x)
            return result.createNewNumber(prec,False)
        elif x>1:
            result=my_atan(1/x)
            return (PI/2-result).createNewNumber(prec,False)
        elif x<-1:
            x=abs(x); result=my_atan(1/x)
            return (result-PI/2).createNewNumber(prec,False)


# acot(x,unit,prec) returns radian or degree value of inverse of cotangent of x
# Domain: {R}	Range: -90<=f(x)<=90 or -PI/2<=f(x)<=PI/2
# Multiple solutions exist.
#
# acot(x)=PI/2 - atan(x)
# >>> t=time.time(); psmf.acot(0.478,unit='d');time.time()-t
# b10:64.4522003979940232465804502703778753
# 0.1005859375 s
# >>> t=time.time(); psmf.acot(-4.512,unit='d');time.time()-t
# b10:167.50346553913248296608687950510344
# 0.08495521545410156 s
# >>>
# >>> t=time.time(); psmf.acot(-4.512,unit='r');time.time()-t
# b10:-0.218105671431072661385160485165373212
# 0.06933045387268066 s
# >>> t=time.time(); psmf.acot(14.14,unit='r');time.time()-t
# b10:0.0706038058744858482689074626072848525
# 0.08495759963989258 s
def acot(x=None,unit='d',prec=36):
    if x==None:raise ValueError('Argument of acot() missing')
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function acot(x,unit,prec), |x|<=1")
    if unit not in ['d','D','Deg','deg','degre','Degre','r','R','c','rad','Rad','radian','Radian']:
        raise ValueError('Invalid Angle Unit') 
    if dataType(prec)!='int' or prec<1: prec=36
    if dataType(x) in ['int','float']:
        x=upn.Number(str(x),base=10,prec=prec,is_accurate=True)
    elif dataType(x)==str(upn.__name__)+".Number":pass
    else: raise ValueError("Invalid number of acot(x,unit,prec)") 
    # checking base of x
    if x.getBase() in [2,8,16,32,64]:
        numstr=x.getDict()['base10']['sign']+x.getDict()['base10']['ipart']+'.'+x.getDict()['base10']['fpart']
        x=upn.Number(numstr,10,x.getDict()['base10_prec'],False)
    elif x.getBase()==10:pass
    else: raise ValueError("Invalid base of x in acot(x)")	

    if x.getDict()['ipart']=='<UNDEFINED>':return UNDEFINED 
    elif x==INF or x==-INF:return ZERO

    prec2=prec+8	
    PI=mypi.getPI(prec2)

    if unit in ['d','D','deg','Deg','degre','Degre']:
        if x==0:return upn.Number('90',base=10,prec=prec,is_accurate=True)
        elif x==1:return upn.Number('45',base=10,prec=prec,is_accurate=True)
        elif x==-1:return upn.Number('-45',base=10,prec=prec,is_accurate=True)
        elif x>0:
            r=90-atan(x,'d',prec2)
            return r.createNewNumber(prec,False)
        elif x<0:
            r=-atan(x,'d',prec)-90
            return r.createNewNumber(prec,False)
    elif unit in ['r','R','c','rad','Rad','radian','Radian']:
        if x==0:return (PI/2).createNewNumber(prec,False)
        elif x==1:return (PI/4).createNewNumber(prec,False)
        elif x==-1:return (-PI/4).createNewNumber(prec,False)
        elif x>0:
            r=(PI/2)-atan(x,'r',prec2)
            return r.createNewNumber(prec,False)
        elif x<0:
            r=-atan(x,'r',prec)-(PI/2)
            return r.createNewNumber(prec,False)
        


# asec(x,unit,prec) returns radian or degree value of inverse of secant of x
# Domain: -1>=x>=1	Range: -180<=f(x)<=180 or -PI<=f(x)<=PI
# Multiple solutions exist.
#
# asec(x)=acos(1/x); x>1 or x<-1
# >>> t=time.time(); psmf.asec(22.57,unit='r');time.time()-t
# b10:1.5264752160938902419417174929564325
# 0.06883788108825684
# >>> t=time.time(); psmf.asec(-12.57,unit='r');time.time()-t
# b10:1.65043497716196244627292952550282845
# 0.06249690055847168
def asec(x=None,unit='d',prec=36):
    if x==None:raise ValueError('Argument of asec() missing')
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function asec(x,unit,prec), |x|<=1")
    if unit not in ['d','D','Deg','deg','degre','Degre','r','R','c','rad','Rad','radian','Radian']:
        raise ValueError('Invalid Angle Unit') 
    if dataType(prec)!='int' or prec<1: prec=36
    if dataType(x) in ['int','float']:
        x=upn.Number(str(x),base=10,prec=prec,is_accurate=True)
    elif dataType(x)==str(upn.__name__)+".Number":pass
    else: raise ValueError("Invalid number of asec(x,unit,prec)") 
    # checking base of x
    if x.getBase() in [2,8,16,32,64]:
        numstr=x.getDict()['base10']['sign']+x.getDict()['base10']['ipart']+'.'+x.getDict()['base10']['fpart']
        x=upn.Number(numstr,10,x.getDict()['base10_prec'],False)
    elif x.getBase()==10:pass
    else: raise ValueError("Invalid base of x in asex(x)")	

    PI=mypi.getPI(prec)

    if x.getDict()['ipart']=='<UNDEFINED>':return UNDEFINED 
    elif x>-1 and x<1:return UNDEFINED	
    
    if unit in ['d','D','deg','Deg','degre','Degre']:
        if x==1:return ZERO
        elif x==INF or x==-INF:return  upn.Number('90',base=10,prec=prec,is_accurate=True)
        elif x==-1:return upn.Number('60',base=10,prec=prec,is_accurate=True)
        elif x==2:return upn.Number('60',base=10,prec=prec,is_accurate=True)
        elif x==-2:return upn.Number('120',base=10,prec=prec,is_accurate=True)
        else:return acos(1/x,'d',prec).createNewNumber(prec,False)
    elif unit in ['r','R','c','rad','Rad','radian','Radian']:
        if x==1:return ZERO
        elif x==INF or x==-INF:return (PI/2).createNewNumber(prec,False)
        elif x==-1:return PI.createNewNumber(prec,False)
        elif x==2:return (PI/3).createNewNumber(prec,False)
        elif x==-2:return (2*PI/3).createNewNumber(prec,False)
        else:return acos(1/x,'r',prec).createNewNumber(prec,False)


# acosec(x,unit,prec) returns radian or degree value of inverse of cosecant of x
# Domain: -1>=x>=1	Range: -180<=f(x)<=180 or -PI<=f(x)<=PI
# Multiple solutions exist.
def acosec(x=None,unit='d',prec=36):
    if x==None:raise ValueError('Argument of acosec() missing')
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function acosec(x,unit,prec), |x|<=1")
    if unit not in ['d','D','Deg','deg','degre','Degre','r','R','c','rad','Rad','radian','Radian']:
        raise ValueError('Invalid Angle Unit') 
    if dataType(prec)!='int' or prec<1: prec=36
    if dataType(x) in ['int','float']:
        x=upn.Number(str(x),base=10,prec=prec,is_accurate=True)
    elif dataType(x)==str(upn.__name__)+".Number":pass
    else: raise ValueError("Invalid number of acosec(x,unit,prec)") 
    # checking base of x
    if x.getBase() in [2,8,16,32,64]:
        numstr=x.getDict()['base10']['sign']+x.getDict()['base10']['ipart']+'.'+x.getDict()['base10']['fpart']
        x=upn.Number(numstr,10,x.getDict()['base10_prec'],False)
    elif x.getBase()==10:pass
    else: raise ValueError("Invalid base of x in acosec(x)")	

    if x.getDict()['ipart']=='<UNDEFINED>':return UNDEFINED 
    elif x>-1 and x<1:return UNDEFINED # Out of Domain
    elif x==INF or x==-INF:return ZERO

    prec2=prec+4
    PI=mypi.getPI(prec2)

    if unit in ['d','D','deg','Deg','degre','Degre']:
        if x==1:return upn.Number('90',base=10,prec=prec,is_accurate=True)
        elif x==-1:return upn.Number('-90',base=10,prec=prec,is_accurate=True)
        elif x==2:return upn.Number('30',base=10,prec=prec,is_accurate=True)
        elif x==-2:return upn.Number('-30',base=10,prec=prec,is_accurate=True)
        else:return asin(1/x,'d',prec).createNewNumber(prec,False)
    elif unit in ['r','R','c','rad','Rad','radian','Radian']:
        if x==1:return upn.Number(str(PI/2)[4:],base=10,prec=prec).createNewNumber(prec*2,False)
        elif x==-1:return (PI/2).createNewNumber(prec,False)
        elif x==2:return (PI/6).createNewNumber(prec,False)
        elif x==-2:return (-PI/6).createNewNumber(prec,False)
        else:return asin(1/x,'r',prec).createNewNumber(prec,False)

# -------------------------- end of triginometric inverse functions -----------------------------









# -------------------------------- Hyperbolic Functions----------------------------
# sinh(x,prec) calculates hyperbolic sine function with high precision
# Domain: {R}		Range: {R}			Continuous Curve
# >>> t=time.time();psmf.sinh(10.27);time.time()-t
# b10:14426.9435659156329069170188787656726187852947
# 0.11620593070983887 s
# >>>
# >>> t=time.time();psmf.sinh(-10.27);time.time()-t
# b10:-14426.9435659156329069170188787656726187852947
# 0.11620497703552246 s
def sinh(x=None,prec=36):
    if x==None:raise ValueError('Argument of sinh() missing')
    if dataType(prec)!='int' or prec<1: prec=36
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function sinh(x,prec)")

    if x==0:return upn.Number('0',10,prec=1,is_accurate=True)
    elif x==INF:return INF
    elif x==-INF:return -INF

    if dataType(x) in ['int','float']: x=upn.Number(str(x),10,prec=prec,is_accurate=True)
    return ((exp(x,prec)-exp(-1*x,prec))/2).createNewNumber(prec,False)


# cosh(x,prec) calculates hyperbolic cosine function with high precision
# Domain: {R}		Range: f(x)>=1			Continuous Curve
# >>> t=time.time();psmf.cosh(10.27);time.time()-t
# b10:14426.9436005730083319313559968360320812147053
# 0.1548173427581787 s
# >>>
# >>> t=time.time();psmf.cosh(-10.27);time.time()-t
# b10:14426.9436005730083319313559968360320812147053
# 0.11620426177978516 s
def cosh(x=None,prec=36):
    if x==None:raise ValueError('Argument of cosh() missing')
    if dataType(prec)!='int' or prec<1: prec=36
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function cosh(x,prec)")

    if x==0:return upn.Number('1',10,prec=1,is_accurate=True)
    elif x==INF or x==-INF:return INF

    if dataType(x) in ['int','float']: x=upn.Number(str(x),10,prec=prec,is_accurate=True)
    return ((exp(x,prec)+exp(-1*x,prec))/2).createNewNumber(prec,False)


# tanh(x,prec) calculates hyperbolic tangent function with high precision
# Domain: {R}		Range: {R:-1<=f(x)<=1}		Continuous Curve
# >>> t=time.time();psmf.tanh(10.27);time.time()-t
# b10:0.99999999759773266018466878065360977918
# 0.015623807907104492 s
# >>>
# >>> t=time.time();psmf.tanh(-10.27);time.time()-t
# b10:-0.9999999975977326601846687806536097791857181805
# 0.031745195388793945 s
def tanh(x=None,prec=36):
    if x==None:raise ValueError('Argument of tanh() missing')
    if dataType(prec)!='int' or prec<1: prec=36
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function tanh(x,prec)")

    if x==0:return ZERO
    elif x==INF:return upn.Number('1',10,1,True)
    elif x==-INF:return upn.Number('-1',10,1,True)

    if dataType(x) in ['int','float']: x=upn.Number(str(x),10,prec=prec,is_accurate=True)
    tmp=exp(2*x,prec)
    return ((tmp-1)/(tmp+1)).createNewNumber(prec,False)


# coth(x,prec) calculates hyperbolic cotangent function with high precision
# Domain: {R}		Range: {R:1<=f(x)<=-1}		Broken Curve at Origin
# >>> t=time.time();psmf.coth(10.27);time.time()-t
# b10:1.00000000240226734558621960515303495
# 0.021962642669677734 s
# >>>
# >>> t=time.time();psmf.coth(-10.27);time.time()-t
# b10:-1.00000000240226734558621960515303495
# 0.02245783805847168 s
def coth(x=None,prec=36):
    if x==None:raise ValueError('Argument of coth() missing')
    if dataType(prec)!='int' or prec<1: prec=36
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function coth(x,prec)")

    if x==0:return (INF,-INF)
    elif x==INF:return upn.Number('1',10,1,True)
    elif x==-INF:return upn.Number('-1',10,1,True)

    if dataType(x) in ['int','float']: x=upn.Number(str(x),10,prec=prec,is_accurate=True)
    tmp=exp(2*x,prec)
    return ((tmp+1)/(tmp-1)).createNewNumber(prec,False)


# sech(x,prec) calculates hyperbolic secant function with high precision
# Domain: {R}		Range: 0<=f(x)<=1		Continuous Curve
# >>> t=time.time();psmf.sech(10.27);time.time()-t
# b10:0.0000693147507667723931689102930947604516
# 0.11622238159179688
# >>>
# >>> t=time.time();psmf.sech(-10.27);time.time()-t
# b10:0.0000693147507667723931689102930947604516
# 0.10692143440246582

def sech(x=None,prec=36):
    if x==None:raise ValueError('Argument of sech() missing')
    if dataType(prec)!='int' or prec<1: prec=36
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function sech(x,prec)")

    if x==0:return upn.Number('1',10,prec=1,is_accurate=True)
    elif x==INF or x==-INF:return ZERO

    if dataType(x) in ['int','float']: x=upn.Number(str(x),10,prec=prec,is_accurate=True)
    return (2/(exp(x,prec)+exp(-1*x,prec))).createNewNumber(prec,False)


# cosech(x,prec) calculates hyperbolic cosecant function with high precision
# Domain: {R}		Range: {R}		Broken Curve at Origin
# >>> t=time.time();psmf.cosech(10.27);time.time()-t
# b10:0.0000693147509332849555033749900777130568
# 0.11620688438415527
# >>>
# >>> t=time.time();psmf.cosech(-10.27);time.time()-t
# b10:-0.0000693147509332849555033749900777130568
# 0.1005864143371582
def cosech(x=None,prec=36):
    if x==None:raise ValueError('Argument of cosech() missing')
    if dataType(prec)!='int' or prec<1: prec=36
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function cosech(x,prec)")

    if x==0:return (INF,-INF)
    elif x==INF:return ZERO
    elif x==-INF:return ZERO

    if dataType(x) in ['int','float']: x=upn.Number(str(x),10,prec=prec,is_accurate=True)
    return (2/(exp(x,prec)-exp(-1*x,prec))).createNewNumber(prec,False)



# ---------------------Hyperbolic Inverse Function----------------------------
# asinh(x,prec) calculates the inverse of the hyperbolic sine function 
# with high precision asinh() is more efficient than asinh2()
# Domain: {R}		Range: {R}
# >>> t=time.time();psmf.asinh(5);time.time()-t
# b10:2.31243834127275262025356234136441439
# 0.06933283805847168 s
# >>> t=time.time();psmf.asinh(0.99);time.time()-t
# b10:0.874284812187294926764635198002652825
# 0.06933212280273438 s
def asinh(x=None,prec=36):
    if x==None:raise ValueError('Argument of asinh() missing')
    if dataType(prec)!='int' or prec<1: prec=36
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function asinh(x,prec)")
    if dataType(x) in ['int','float']: x=upn.Number(str(x),10,prec=prec,is_accurate=True)
    elif dataType(x)==str(upn.__name__)+".Number":pass
    else:raise ValueError("Invalid arguement of asinh(x.prec)")

    if x==0:return ZERO
    elif x==INF:return INF
    elif x== -INF:return -INF

    return ln((x+sqrt(1+x*x,prec)),prec).createNewNumber(prec,False)

# asinh2(x,prec) calculates the inverse of the hyperbolic sine function 
# with high precision. This function is less efficient than asinh()
# asinh(x)=ln(x+sqrt(x^2+1))=x-(1/2)x^3/3+(1x3/2x4)x^5/5-(1x3x5/2x4x6)x^7/7+ ...
# atnah(-x)=-atanh(x)
# atanh(x)=x+x^3/3+x^5/5+x^7/7+ ...
# Domain: -1<x<1		Range: {R}
# >>> t=time.time();psmf.asinh2(0.99);time.time()-t
# b10:0.874284812187294926764635198002652825
# 2.329054355621338 s
# >>>						**DONT USE asinh2()**

def asinh2(x=None,prec=36):
    if x==None:raise ValueError('Argument of acosh() missing')
    if dataType(prec)!='int' or prec<1: prec=36
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function atanh(x,prec)")

    if dataType(x) in ['int','float']: x=upn.Number(str(x),10,prec=prec,is_accurate=True)
    elif dataType(x)==str(upn.__name__)+".Number":pass
    else:raise ValueError("Invalid arguement of atanh(x.prec)")

    if x==0:return ZERO
    elif x == INF:return INF
    elif x == -INF:return -INF

    delP=upn.Number('1.0e-'+str(prec),10,prec,True)
    r=1;t=x; SUM=x;t1=upn.Number('1',10,prec,True)
    while(t1>delP):        
        t=-1*t*x*x*(2*r-1)*(2*r-1)/(2*r*(2*r+1));
        SUM=SUM+t;
        if t.getPrecision()>prec+6:
            t=t.createNewNumber(prec=6+prec,is_accurate=False)
            SUM=SUM.createNewNumber(prec=6+prec,is_accurate=False)
        if t<0:t1=-t
        else:t1=t
        r=r+1
    return SUM.createNewNumber(prec,is_accurate=False)



# acosh(x,prec) calculates the inverse of the hyperbolic cosine function 
# with high precision
# Domain: {R:x>=1}		Range: {R}
# >>> t=time.time();psmf.acosh(5);time.time()-t
# b10:2.29243166956117768780078731134801543
# 0.07812786102294922
def acosh(x=None,prec=36):
    if x==None:raise ValueError('Argument of acosh() missing')
    if dataType(prec)!='int' or prec<1: prec=36
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function acosh(x,prec)")
    if dataType(x) in ['int','float']: x=upn.Number(str(x),10,prec=prec,is_accurate=True)
    elif dataType(x)==str(upn.__name__)+".Number":pass
    else:raise ValueError("Invalid arguement of acosh(x.prec)")

    if x==1:return ZERO
    elif x<1 or x == -INF:return UNDEFINED
    elif x == INF:return INF

    tmp=x+sqrt(x*x-1,prec);
    return ln(tmp,prec).createNewNumber(prec,False)



# atanh(x,prec) calculates the inverse of the hyperbolic tangent function 
# with high precision
# atnah(-x)=-atanh(x)
# atanh(x)=x+x^3/3+x^5/5+x^7/7+ ...
# Domain: {R:-1<x<1}		Range: {R}

# >>> import time
# >>> t=time.time();psmf.atanh(0.56987);time.time()-t
# b10:0.647330301894214558717038806058200135
# 0.046874046325683594 s
# >>> t=time.time();psmf.atanh(0.56987,prec=100);time.time()-t
# b10:0.647330301894214558717038806058200135600017587223740908938463960491017783313
# 8888242410246403442145253
# 0.16991567611694336 s
# >>> t=time.time();psmf.atanh(-0.56987,prec=100);time.time()-t
# b10:-0.647330301894214558717038806058200135600017587223740908938463960491017783313
# 8888242410246403442145253
# 0.17918848991394043 s
def atanh(x=None,prec=36):
    if x==None:raise ValueError('Argument of acosh() missing')
    if dataType(prec)!='int' or prec<1: prec=36
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function atanh(x,prec)")

    if dataType(x) in ['int','float']: x=upn.Number(str(x),10,prec=prec,is_accurate=True)
    elif dataType(x)==str(upn.__name__)+".Number":pass
    else:raise ValueError("Invalid arguement of atanh(x.prec)")
    if x>1 or x<-1 or x == INF or x == -INF:return UNDEFINED
    if x==1:return INF
    elif x==-1:return -INF
    elif x==0:return ZERO

    delP=upn.Number('1.0e-'+str(prec),10,prec,True)
    sign=1;
    if x<0:x=-x;sign=-1
    r=1;t=x; SUM=t	
    while(t>delP):        
        t=t*x*x*(2*r-1)/(2*r+1);
        SUM=SUM+t;
        if t.getPrecision()>prec+4:
            t=t.createNewNumber(prec=4+prec,is_accurate=False)
            SUM=SUM.createNewNumber(prec=4+prec,is_accurate=False)
        if t<0:t=-t
        r=r+1
    return (SUM*sign).createNewNumber(prec,is_accurate=False)


# acoth(x,prec) calculates the inverse of the hyperbolic cotangent function 
# with high precision
# acoth(-x)=-acoth(x)
# acoth(x)=x^-1+x^-3/3+x^-5/5+x^-7/7+ ...
# Domain: {R:-1<x<1}		Range: {R}
# >>>
# >>> t=time.time();psmf.acoth(2.56987,prec=100);time.time()-t
# b10:0.4107681835892846002033171359287388796872068143953391121820969145050187922
# 907387053920231358212298834
# 0.10058188438415527 s
# >>> t=time.time();psmf.acoth(-2.56987,prec=100);time.time()-t
# b10:-0.4107681835892846002033171359287388796872068143953391121820969145050187922
# 907387053920231358212298834
# 0.10058140754699707 s
def acoth(x=None,prec=36):
    if x==None:raise ValueError('Argument of acosh() missing')
    if dataType(prec)!='int' or prec<1: prec=36
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function atanh(x,prec)")

    if dataType(x) in ['int','float']: x=upn.Number(str(x),10,prec=prec,is_accurate=True)
    elif dataType(x)==str(upn.__name__)+".Number":pass
    else:raise ValueError("Invalid arguement of atanh(x.prec)")
    if x<1 and x>-1:return UNDEFINED
    if x==1:return INF
    elif x==-1:return -INF
    elif x == INF or x == -INF:return ZERO

    delP=upn.Number('1.0e-'+str(prec),10,prec,True)
    sign=1;
    if x<0:x=-x;sign=-1
    r=1;t=1/x; SUM=t	
    while(t>delP):        
        t=t*(2*r-1)/(x*x*(2*r+1));
        SUM=SUM+t;
        if t.getPrecision()>prec+4:
            t=t.createNewNumber(prec=4+prec,is_accurate=False)
            SUM=SUM.createNewNumber(prec=4+prec,is_accurate=False)
        if t<0:t=-t
        r=r+1
    return (SUM*sign).createNewNumber(prec,is_accurate=False)




# asech(x,prec) calculates the inverse of the hyperbolic secant function 
# with high precision
# Domain: {R: 0<x<=1}		Range: {R}
# >>> t=time.time();psmf.asech(0.999);time.time()-t
# b10:0.0447400054775150981356221725525384249
# 0.08495450019836426 s
# >>>
# >>> t=time.time();psmf.asech(0.0001);time.time()-t
# b10:9.90348755003612803611419788811229973
# 0.06299328804016113 s
def asech(x=None,prec=36):
    if x==None:raise ValueError('Argument of acosh() missing')
    if dataType(prec)!='int' or prec<1: prec=36
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function asech(x,prec)")
    if x<0 or x>1:return UNDEFINED
    if dataType(x) in ['int','float']: x=upn.Number(str(x),10,prec=prec,is_accurate=True)
    elif dataType(x)==str(upn.__name__)+".Number":pass
    else:raise ValueError("Invalid arguement of asech(x.prec)")
	
    if x==1:return ZERO
    elif x>1 or x<0 or x == INF or x == -INF:return UNDEFINED
    elif x==0:return INF
	
    return ln((1+sqrt(1-x*x))/x,prec).createNewNumber(prec,False)


# acosech(x,prec) calculates the inverse of the hyperbolic cosecant function 
# with high precision
# Domain: {R:x>=0}		Range: {R}
# >>> t=time.time();psmf.acosech(0.75);time.time()-t
# b10:1.0986122886681096913952452369225257
# 0.015623807907104492 s
# >>>
# >>> t=time.time();psmf.acosech(175.47);time.time()-t
# b10:0.00569894903412071257692391245565785023
# 0.09424281120300293 s
def acosech(x=None,prec=36):
    if x==None:raise ValueError('Argument of acosh() missing')
    if dataType(prec)!='int' or prec<1: prec=36
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function acosech(x,prec)")
    if dataType(x) in ['int','float']: x=upn.Number(str(x),10,prec=prec,is_accurate=True)
    elif dataType(x)==str(upn.__name__)+".Number":pass
    else:raise ValueError("Invalid arguement of acosech(x.prec)")

    if x<0:return UNDEFINED	
    elif x==0:return INF
    elif x == INF or x == -INF:return UNDEFINED

    return ln((1+sqrt(1+x*x))/x,prec).createNewNumber(prec,False)

# --------------------------End of Hyperbolic Functions---------------------------

# -------------------------- Gamma, beta and error functions ----------------------
# gamma(x) function returns approximate value of gamma of x
# T(z)=Int((t^(z-1))*e^(-t)dt),0,inf)
# T(n)=(n-1)! where n is an integer
# Method name: Lanczos Apprximation Algorithm (Numerical recepies in C, 
# Cambridge University Press,1992) 
# Domain: {R:x>0}		Range: {R:f(x)>=0}

# >>> t=time.time();psmf.gamma(-1);time.time()-t
# b10:<UNDEFINED>
# 0.0 s
# >>> t=time.time();psmf.gamma(0);time.time()-t
# b10:<INF>
# 0.0 s
# >>> t=time.time();psmf.gamma(0.00125);time.time()-t
# b10:799.4240192390721293717451037821999190509
# 0.24803900718688965 s
# >>> t=time.time();psmf.gamma(1.25);time.time()-t
# b10:0.9064024770554722792917903696058164002836
# 0.20116543769836426 s
# >>> t=time.time();psmf.gamma(2.25);time.time()-t
# b10:1.133003096319346864701112527492092486698
# 0.1479496955871582 s
# >>> t=time.time();psmf.gamma(5);time.time()-t
# b10:24
# 0.0 s
# >>> t=time.time();psmf.gamma(4.995);time.time()-t
# b10:23.82001061497065685283517463398246169517
# 0.2543816566467285 s
# >>> t=time.time();psmf.gamma(5.001);time.time()-t
# b10:24.03617671808178253261763264061611109907
# 0.2543811798095703 s
# >>>
def gamma(x=None,prec=36):
    if x==None:raise ValueError('Argument of gamma() missing')
    if dataType(prec)!='int' or prec<1: prec=36
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function gamma(x,prec)")
    if dataType(x) in ['int','float']:  x=upn.Number(str(x),10,prec,False)
		
    if x<0:return UNDEFINED
    if x==0:return INF
    elif x==1 or x==2:return upn.Number('1',10,1,True)

    if x.isInteger(): return fact(x-1)

    prec2=prec+4
    c0=1.000000000190015
    coeff=[76.18009172947146,-86.50532032941677,24.01409824083091,-1.231739572450155,0.001208650973866179,-0.000005395239384953]
    s=0
    for i in range(1,7):s+=coeff[i-1]/(x+i) 
    s=c0+s;
    tmp=sqrt(2*mypi.getPI(prec2),prec2)*s*power(x+5.5,x+0.5,prec2)*exp(-5.5-x,prec2)/x
    return tmp.createNewNumber(prec2,False)

# beta(x,y) is called beta function defined by Int(t^(x-1)*(1-t)^(y-1)dt)
# in the interval [0,1] which is equal to gamma(x)*gamma(y)/gamma(x+y)
# Domain:{R:x>=0,y>=0}	Range:{R:0<=f(x)<=1}

# >>> t=time.time();psmf.beta(0,5);time.time()-t
# b10:<INF>
# 0.0 s
# >>> t=time.time();psmf.beta(5,0);time.time()-t
# b10:<INF>
# 0.0 s
# >>> t=time.time();psmf.beta(-5,0);time.time()-t
# b10:<UNDEFINED>
# 0.0 s
# >>> t=time.time();psmf.beta(0,-2);time.time()-t
# b10:<UNDEFINED>
# 0.0 s
# >>> t=time.time();psmf.beta(2,5);time.time()-t
# b10:0.0333333333333333333333333333333333333
# 0.0 s
# >>> t=time.time();psmf.beta(5.2,3.57);time.time()-t
# b10:0.00473509296091992594453089528798505149
# 0.6738464832305908 s
def beta(x=None,y=None,prec=36):
    if x==None or y==None:raise ValueError('Argument of beta() missing')
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function beta(x,y,prec)")
    if dataType(prec)!='int' or prec<1: prec=36
    if dataType(x) in ['int','float']:  x=upn.Number(str(x),10,prec,False)

    if x<0 or y<0:return UNDEFINED
    elif x==0 or y==0:return INF
    result=gamma(x)*gamma(y)/gamma(x+y)
    return result.createNewNumber(prec,False)

# erf(x,prec) returns the integral Int(e^(-t^2)dt) in the interval 
# from 0 to x with high precision
# Domain:{R}	Range:{R:-1<=f(x)<=1}

# >>> t=time.time();psmf.erf(0);time.time()-t
# b10:0
# 0.0 s
# >>> t=time.time();psmf.erf(3);time.time()-t
# b10:0.999977909503001414558627223870417681
# 0.08446097373962402 s
# >>> t=time.time();psmf.erf(-3);time.time()-t
# b10:-0.999977909503001414558627223870417681
# 0.08445954322814941 s
# >>> t=time.time();psmf.erf(8);time.time()-t
# b10:0.999999999999999999027505818563938522
# 0.17920303344726562 s
# >>> t=time.time();psmf.erf(-8);time.time()-t
# b10:-0.999999999999999999027505818563938522
# 0.185042142868042 s
def erf(x=None,prec=36):
    if x==None:raise ValueError('Argument of erf() missing')
    if dataType(x) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function erf(x,prec)")
    if dataType(x) in ['int','float']:x=upn.Number(str(x),10,prec,True)
    if dataType(prec)!='int' or prec<1: prec=36

    if x==0:return ZERO
    elif x>9:return upn.Number('1',base=10,prec=prec,is_accurate=True)
    elif x<-9:return upn.Number('-1',base=10,prec=prec,is_accurate=True)

    delP=upn.Number('1p-'+str(prec),10,prec=prec)
    prec2=prec+8

    r=0;t=x;s=x;t1=upn.Number('1',10,1,True)
    while t1>delP:        
        t=t*(-1)*x*x*(2*r+1)/((r+1)*(2*r+3))
        if t.getPrecision()>prec2:t=t.createNewNumber(prec2,False)
        s=s+t
        if t<0:t1=-t        
        r=r+1
    m=2/sqrt(mypi.getPI(prec2))
    return (s*m).createNewNumber(prec,False)


# erfc(x,prec) returns the complementary error function of x (1-erf(X))
# in the interval from 0 to x with high precision
# Domain:{R}	Range:{R:0<=f(x)<=2}

# >>> t=time.time();psmf.erfc(0);time.time()-t
# b10:1
# 0.0 s
# >>> t=time.time();psmf.erfc(2);time.time()-t
# b10:0.00467773498104726583793074363274707
# 0.06883764266967773 s
# >>> t=time.time();psmf.erfc(-2);time.time()-t
# b10:1.99532226501895273416206925636725293
# 0.06933188438415527 s
# >>> t=time.time();psmf.erfc(8);time.time()-t
# b10:0.000000000000000000972494181436061478
# 0.18554091453552246 s
# >>> t=time.time();psmf.erfc(-8);time.time()-t
# b10:1.99999999999999999902750581856393852
# 0.16991662979125977 s
def erfc(x=None,prec=36):
    if x==None:raise ValueError('Argument of erf() missing')
    result=1-erf(x,prec)
    return result.createNewNumber(prec,False)






# -------------------- END of gamma, beta and error functions ----------------------





# ------------------------ Numbers of Number Theory ----------------------------
# eulerNumber(r) calculates and returns the euler number of the given positive 
# and even integer by double sum method
# Odd positive integer returns 0
# SUM(((-1)^i*(SUM(((-1)^j*nCr(2i,j)*(i-j)^r),j=0,j=2i))/2^i),i=1,i=r)
# r=0,1,2,3,4,5,6,7,8,9,10
# E(r)=1,0,-1,0,5,0,-61,0,1385,0,-50521
# >>> smf.eulerNumber(18)
# b10:-2404879675441
def eulerNumber(r=None):
    if r==None:raise ValueError('Argument of eulerNumber() missing')
    if dataType(r) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function eulerNumber(r)")
    if dataType(r)=='int' and r>=0:k=r
    elif dataType(r)==str(upn.__name__)+'.Number' and r.isInteger():
        k=r.toDenaryInteger() 
    else: raise ValueError('Argument of eulerNumber() is not a positive integer')

    if k==0:return upn.Number('1',10,prec=1,is_accurate=True)
    elif k%2==1:return upn.Number('0',10,prec=1,is_accurate=True) #returns 0 if k is odd
  
    p1=1;p=1;sum1=0;sum2=0;i=1   
    while True:
        if i%2==0:neg1=1
        else:neg1=-1

        sum2=0;p2=1
        for j in range(0,2*i+1):
            if j%2==0:neg2=1
            else:neg2=-1
            p2=neg2*(nCr(2*i,j).toDenaryInteger())*((i-j)**k)
            sum2=sum2+p2
        p=neg1*sum2/2**i
        sum1=sum1+p
        if i>=k:break
        i=i+1
    return upn.Number(str(sum1),10,is_accurate=True) 

# bernoulliNumber(r) calculates and returns the Bernoulli number of the given positive 
# and even integer (2,4,6,...) by the following definition
# Odd positive integer returns 0
# B(r)=0 if r is an odd positive integer
# SUM((nCr(r-1,i)*r*E(r)/(4^r-2^r)),i=0,i=r-1)
# r=1,2,3,4,5,6,7,8,9,10
# B(r)=0,1/6,0,-1/30,0,1/42,0,-1/30,0,5/66
# >>> smf.eulerNumber(18)
# b10:-2404879675441
def bernoulliNumber(r=None):
    if r==None:raise ValueError('Argument of eulerNumber() missing')
    if dataType(r) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function bernoulliNumber(r)")
    if dataType(r)=='int' and r>0:k=r
    elif dataType(r)==str(upn.__name__)+'.Number' and r.isInteger():
        k=r.toDenaryInteger() 
    else: raise ValueError('Argument of bernoulliNumber() is not a positive integer and greater than 0')

    if k%2==1:return upn.Number('0',10,prec=1,is_accurate=True) #returns 0 if k is odd

    SUM=0 #upn.Number('0',10,is_accurate=True)
    deno=4**k-2**k
    for i in range(0,k,2):        
        SUM=SUM+nCr(k-1,i).toDenaryInteger()*k*eulerNumber(i).toDenaryInteger()
    return upn.Number(str(SUM)+'/'+str(deno),10,modify=True)

# tangentNumber(r) calculates and returns the Tangent number of the given positive 
# and even integer (2,4,6,...) by the following definition
# Odd positive integer returns 0
# T(r)=0 if r is an odd positive integer
# 2^r*2^(r-1)*B(r)
# r=0,1,2,3,4,5,6,7,8,9,10
# T(r)=1,0,-1,0,5,0,-61,0,1385,0,-50521
# >>> smf.bernoulliNumber(18)
# b10:54 775/798
def tangentNumber(r=None):
    if r==None:raise ValueError('Argument of eulerNumber() missing')
    if dataType(r) not in ['int','float',str(upn.__name__)+".Number"]:
        raise ValueError("Invalid argument in function tangentNumber(r)")
    if dataType(r)=='int' and r>0:k=r
    elif dataType(r)==str(upn.__name__)+'.Number' and r.isInteger():
        k=r.toDenaryInteger() 
    else: raise ValueError('Argument of bernoulliNumber() is not a positive integer and greater than 0')
    if k%2==1:return upn.Number('0',10,prec=1,is_accurate=True) #returns 0 if k is odd

    SUM=0 #upn.Number('0',10,is_accurate=True)
    p=2**k;deno=(4**k-p)*k
    for i in range(0,k,2):        
        SUM=SUM+nCr(k-1,i).toDenaryInteger()*k*eulerNumber(i).toDenaryInteger()
    SUM=upn.Number(str(SUM),10,is_accurate=True)
    tval=0
    if (k//2)%2==0:tval=(-1*p*(p-1))*SUM/deno
    elif (k//2)%2==1:tval=(p*(p-1))*SUM/deno
    return tval

# ---------------------------------- END of the MODULE ---------------------------------------




















