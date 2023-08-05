"""
    Module Name: upnumber (universal precision number)
	Path:'<package_path>\\upmath\\src\\upnumber.py'
    Author: Engr. A.K.M. Aminul Islam
	Email:aminul71bd@gmail.com
    Date: 2020,July,15
    Version:'2.8.2023.02.03'
	Package Version:'2.0.0'
	Last Modified:2023/02/03
    Description:This module contains the functions needed for handling numbers of
        any type and many bases. The functions of this module can convert a number 
        of a base 2,8,10,16,32,64 to base 2,8,10,16,32,64. It can create a number
        with the accuracy to the desired precision level. All numbers are returned 
        and manipulated in string format. It can handle integer and floating 
        point numbers of any base from 2,8,10,16,32,64. This module can process
        any number from ultra small to ultra large level.

        The central number system is binary and denary. Numbers of bases 8,16,32 and 64 are
        converted efficiently through binary. Number arithmetic operations are performed by 
        denary (base10) arithmetic operations.

        Number data are stored in a dictionary data format.
        (base='bXX', sign='','+','-' ipart=integer part, fpart=floating part,
         expo=exponent, numerator, deno=denominator)

    Information on the module content		Numeric Output		Digits
    Base=2	Binary Number			b02:-11001.011p600	0,1
    Base=8	Octal Number			b08:-4572.0273p-600	0-7
    Base=10	Denary Number			b10:-9078.0412p40	0-9
    Base=16	Hexadecimal Number		b16:-f04d.32abp70	0-9a-fA-F
    Base=32	DuoTrigesimal/base32 Number	b32:-vV0o.25f9p+147	0-9a-vA-V
    Base=64	base64 Number			b64:-zXo0.a4Btp-250	0-9a-zA-Z!@

    Number showing modes (show_mode):'fp' and 'fr'
	'fp' (floating point) mode means numbers with floating digits.
		Like:b02:-11110001.11p-10,b10:92.45e33
	'fr' (fractional) mode which displays number as mixed or proper fraction.
		Like:b02:-11110001 11/100p+17, b10:92 9/20e+23.
	Difference: 'fp' numbers contain '.', but 'fr' numbers have '/'.

    ***If a floating or fractional number is recurring, this module can handle it
    very efficiently. Recurring floatings can be converted into recurring fractions.

    Valid Input Format: (fp)11110.101,11110.101p+34,11110.101p34,11110.101p-23, -0.1101p-45
		(fr) '-1101 11/1101', "-1101 11/1101p+7", "-1101 11/1101p7", '-1101 11/1101p-17'

    Location:cpysoft/pmath/upNumber.py
    Function naming type: camel case like isBinary()
    Class naming style=Starting with upper case + camel case
    Date of Last Edit:15th July,2020 (Version 2.7.2020.07.15)
    Module Code:PMATH-2-7-2020-07-15

    CONSTANTS
	=============
	pi = constant ratio of circumference to diameter of a circle
	e = exp(0)
	INF = a/0 where a is a positive non-zero number
	UNDEFINED = 0/0, INF/INF, INF - INF, invalid domain of a function
	
	Properties of INF and UNDEFINED
	-------------------------------
		15 Rules on INF
		(1) INF == INF, But (2) INF is not INF
				(3) INF-INF==UND, (4) INF+INF=INF, (5) INF*INF=INF, (6) INF/INF==UND, (7) INF+a==INF 
				(8) a/INF=ZERO, (9) INF*(-a)== -INF	(10) INF/(-a)==-INF, (11) INF/0==UND
				(12) ~INF=ZERO, (13) INF//a=INF, (14) INF%INF=UND, (15) INF**INF=INF
         3 Golden Rules on UND
		(1) UND!=UND, (2) UND is not UND (3) Any Math Operation on UND = UND  
"""
from __future__ import division
import re
import sys

__version__=version='2.8.2023.02.03'


# dnm1=denary number match 1, dnm2=denary number match 2
# bnm1=binary number match 1, bnm2=binary number match 2
# onm1=octal number match 1, onm22=octal number match 2
# hnm1=hex number match 1, hnm2=hex number match 2
dnm1=re.compile('^[+-]?\d+\.?\d*([eEpP][+-]?\d+)?$')
dnm2=re.compile('^[+-]?\d*\.?\d+([eEpP][+-]?\d+)?$')
dnm3=re.compile('^[+-]?\d*(\s?\d+/\d+)?([eEpP][+-]?\d+)?$')

bnm1=re.compile('^[+-]?[0-1]+\.?[0-1]*([pP][+-]?[0-9]+)?$')
bnm2=re.compile('^[+-]?[0-1]*\.?[0-1]+([pP][+-]?[0-9]+)?$')
bnm3=re.compile('^[+-]?[0-1]*(\s?[0-1]+/[0-1]+)?([pP][+-]?[0-9]+)?$')

onm1=re.compile('^[+-]?[0-7]+\.?[0-7]*([pP][+-]?[0-9]+)?$')
onm2=re.compile('^[+-]?[0-7]*\.?[0-7]+([pP][+-]?[0-9]+)?$')
onm3=re.compile('^[+-]?[0-7]*(\s?[0-7]+/[0-7]+)?([pP][+-]?[0-9]+)?$')

hnm1=re.compile('^[+-]?[\da-fA-F]+\.?[0-9a-fA-F]*([pP][+-]?[0-9]+)?$')
hnm2=re.compile('^[+-]?[\da-fA-F]*\.?[0-9a-fA-F]+([pP][+-]?[0-9]+)?$')
hnm3=re.compile('^[+-]?[\da-fA-F]*(\s?[\da-fA-F]+/[\da-fA-F]+)?([pP][+-]?[0-9]+)?$')

b32nm1=re.compile('^[+-]?[\da-vA-V]+\.?[0-9a-vA-V]*([pP][+-][0-9]+)?$')
b32nm2=re.compile('^[+-]?[\da-vA-V]*\.?[0-9a-vA-V]+([pP][+-][0-9]+)?$')
b32nm3=re.compile('^[+-]?[\da-vA-V]*(\s?[\da-vA-V]+/[\da-vA-V]+)?([pP][+-][0-9]+)?$')

b64nm1=re.compile('^[+-]?[\da-zA-Z!@]+\.?[0-9a-zA-Z!@]*([pP][+-][0-9]+)?$')
b64nm2=re.compile('^[+-]?[\da-zA-Z!@]*\.?[0-9a-zA-Z!@]+([pP][+-][0-9]+)?$')
b64nm3=re.compile('^[+-]?[\da-zA-Z!@]*(\s?[\da-zA-Z!@]+/[\da-zA-Z!@]+)?([pP][+-][0-9]+)?$')



# dataType() function returns the type of a data
# type(2.0) returns "(type 'float')"
def dataType(data=None):
    s=str(type(data)).split(' ')[1]
    return s.split("'")[1]

# baseInsert(base) inserts the appropriate base prefix to all numerics
def _baseInsert(base=10):
    if base==2:return "b02:"
    elif base==8:return "b08:"
    elif base==10:return "b10:"
    elif base==16:return "b16:"
    elif base==32:return "b32:"
    elif base==64:return "b64:"

# isBinary(num) checks the input whether a valid binary number
# For large value input, the number input must be string
def isBinary(num=None):
    if num==None:raise ValueError('Argument of isBinary() missing')
    s=''
    if dataType(num)!='str':s=str(num).strip()
    elif dataType(num)=='str':s=num.strip()
    return _isBinary(s)

# input must be string
def _isBinary(num=''):
    if bnm1.match(num) or bnm2.match(num) or bnm3.match(num):return True
    else:return False

# isOctal(num) checks the input whether a valid octal number
# For large value input, the number input must be string
def isOctal(num=None):
    if num==None:raise ValueError('Argument of isOctal() missing')
    s=''
    if dataType(num)!='str':s=str(num).strip()
    elif dataType(num)=='str':s=num.strip()
    return _isOctal(s)

# input must be string
def _isOctal(num=''):
    if onm1.match(num) or onm2.match(num) or onm3.match(num):return True
    else:return False

# isDenary(num) checks the input whether a valid denary/decimal number
# For large value input, the number input must be string
def isDenary(num=None):
    if num==None:raise ValueError('Argument of isDenary() missing')
    s=''
    if dataType(num)!='str':s=str(num).strip()
    elif dataType(num)=='str':s=num.strip()
    return _isDenary(s)

# input must be string
def _isDenary(num=''):
    if dnm1.match(num) or dnm2.match(num) or dnm3.match(num):return True
    else:return False

# isHexaDecimal(num) checks the input whether a valid hexadecimal number
# For large value or hexa input, the number input must be string
def isHexadecimal(num=None):
    if num==None:raise ValueError('Argument of isHexadecimal() missing')
    s=''
    if dataType(num)!='str':s=str(num).strip()
    elif dataType(num)=='str':s=num.strip()
    return _isHexadecimal(s)

# input must be string
def _isHexadecimal(num=''):
    if hnm1.match(num) or hnm2.match(num) or hnm3.match(num):return True
    else:return False

# isBase32Number(num) checks the input whether a valid duotrigesimal
# (base 32) number or not
# For large value or hexa input, the number input must be string
def isBase32Number(num=None):
    if num==None:raise ValueError('Argument of isBase32Number() missing')
    s=''
    if dataType(num)!='str':s=str(num).strip()
    elif dataType(num)=='str':s=num.strip()
    return _isBase32Number(s)

# input must be string
def _isBase32Number(num=''):
    if b32nm1.match(num) or b32nm2.match(num) or b32nm3.match(num):return True
    else:return False

# isBase64Number(num) checks the input whether a valid base64 number
# For large value or hexa input, the number input must be string
def isBase64Number(num=None):
    if num==None:raise ValueError('Argument of isBase64Number() missing')
    s=''
    if dataType(num)!='str':s=str(num).strip()
    elif dataType(num)=='str':s=num.strip()
    return _isBase64Number(s)

# input must be string
def _isBase64Number(num=''):
    if b64nm1.match(num) or b64nm2.match(num) or b64nm3.match(num):return True
    else:return False

# isNumeric(num,base) checks the input is a valid denary, octal,
# hexadecimal, duotrigesimal, or base64 number
# For large value input, the number input must be string
def isNumeric(num=None,base=10):
    if num==None:raise ValueError('Argument of isNumeric() missing')
    if base not in [2,8,10,16,32,64]:raise ValueError('Invalid base.')
    s=''
    if dataType(num)!='str':s=str(num).strip()
    elif dataType(num)=='str':s=num.strip()
    return _isNumeric(s,base)

# input must be string
def _isNumeric(num='',base=10):
    if base==2 and _isBinary(num):return True
    elif base==8 and _isOctal(num):return True
    elif base==10 and _isDenary(num):return True
    elif base==16 and _isHexadecimal(num):return True
    elif base==32 and _isBase32Number(num):return True
    elif base==64 and _isBase64Number(num):return True    
    else:return False

# _prec_multiplier() returns multiplier of precision needed to maintain
# the set precision level
def _precMultiplier(base=None):
    if base==2:return 1
    elif base==8:return 3
    elif base==16: return 4
    elif base==32: return 5
    elif base==64: return 6

# parseNumberString(num) parses different parts of a number into a dictionary
def parseNumberString(num=None,base=10):
    if num==None:raise ValueError('Argument of parseNumberString() missing')

    if num in ['inf','Inf','INF','<inf>','<Inf>','<INF>']:
        return {'base':base,'input_mode':'fp','sign':'+','ipart':'<INF>','fpart':'0','exp':0,'prec':0}
    elif num in ['-inf','-Inf','-INF','<-inf>','<-Inf>','<-INF>']:
        return {'base':base,'input_mode':'fp','sign':'-','ipart':'<INF>','fpart':'0','exp':0,'prec':0,\
		'is_accurate':True}
    elif num in ['undefined','Undefined','UNDEFINED','<undefined>','<Undefined>','<UNDEFINED>']:
        return {'base':base,'input_mode':'fp','sign':'','ipart':'<UNDEFINED>','fpart':'','exp':0,'prec':0}

    if num=='0' or num==0:
        return {'base':base,'input_mode':'fp','sign':'+','ipart':'0','fpart':'0','exp':0,'prec':0}
    elif num=='-0' or num==-0:
        return {'base':base,'input_mode':'fp','sign':'-','ipart':'0','fpart':'0','exp':0,'prec':0}
    elif num=='0.0' or num==0.0:
        return {'base':base,'input_mode':'fp','sign':'+','ipart':'0','fpart':'0','exp':0,'prec':0}
    elif num=='-0.0' or num==-0.0:
        return {'base':base,'input_mode':'fp','sign':'-','ipart':'0','fpart':'0','exp':0,'prec':0}
    if base not in [2,8,10,16,32,64]:raise ValueError('Invalid base.')

    s=''
    if dataType(num)!='str':s=str(num).strip()
    elif dataType(num)=='str':s=num.strip()
    if not _isNumeric(s,base):raise ValueError('Invalid number value')
    return _parseNumberString(s,base)


# _parseNumberString(num) parses different parts of a number into a dictionary
def _parseNumberString(numstr='',base=10):
    s=numstr;prec=0
    if '/' in s: input_mode='fr'	#fr=fractional
    else: input_mode='fp'		#fp=floating-point

    sign='+'
    if s[0]=='-':
        s=s[1:];sign='-'
    elif s[0]=='+':s=s[1:]

    bodystr="";exponent=0;
    if base==10 and 'e+' in s:
        bodystr=s.split('e+')[0]
        exponent=int(s.split('e+')[1])
    elif base==10 and 'E+' in s:
        bodystr=s.split('E+')[0]
        exponent=int(s.split('E+')[1])
    elif base==10 and 'e-' in s:
        bodystr=s.split('e-')[0]
        exponent=-1*int(s.split('e-')[1])
    elif base==10 and 'E-' in s:
        bodystr=s.split('E-')[0]
        exponent=-1*int(s.split('E-')[1])
    if base==10 and 'e' in s:
        bodystr=s.split('e')[0]
        exponent=int(s.split('e')[1])
    elif base==10 and 'E' in s:
        bodystr=s.split('E')[0]
        exponent=int(s.split('E')[1])
    elif base in [2,8,10,16] and 'p+' in s:
        bodystr=s.split('p+')[0]
        exponent=int(s.split('p+')[1])
    elif base in [2,8,10,16] and 'p-' in s:
        bodystr=s.split('p-')[0]
        exponent=-1*int(s.split('p-')[1])
    elif base in [2,8,10,16] and 'p' in s:
        bodystr=s.split('p')[0]
        exponent=int(s.split('p')[1])
    elif base in [2,8,10,16] and 'P+' in s:
        bodystr=s.split('P+')[0]
        exponent=int(s.split('P+')[1])
    elif base in [2,8,10,16] and 'P-' in s:
        bodystr=s.split('P-')[0]
        exponent=-1*int(s.split('P-')[1])
    elif base in [2,8,10,16] and 'P' in s:
        bodystr=s.split('P')[0]
        exponent=int(s.split('P')[1])
    elif base in [32,64] and 'p+' in s:
        bodystr=s.split('p+')[0]
        exponent=int(s.split('p+')[1])
    elif base in [32,64] and 'p-' in s:
        bodystr=s.split('p-')[0]
        exponent=-1*int(s.split('p-')[1])
    elif base in [32,64] and 'P+' in s:
        bodystr=s.split('P+')[0]
        exponent=int(s.split('P+')[1])
    elif base in [32,64] and 'P-' in s:
        bodystr=s.split('P-')[0]
        exponent=-1*int(s.split('P-')[1])
    else: bodystr=s

    numerator='';deno='';ipart='';fpart='';mantissa=''
    
    if input_mode=='fp':
        if '.' in bodystr:
            ipart=bodystr.split('.')[0]
            fpart=(bodystr.split('.')[1]).rstrip('0')
            prec=len(ipart)+len(fpart)
        else:
            ipart=bodystr.lstrip('0'); prec=len(ipart)
        if ipart=='' and fpart=='':ipart='0';fpart='0';prec=0
        elif ipart=='':ipart='0';prec=len(fpart)
        elif fpart=='':fpart='0';prec=len(ipart)
        return {'base':base,'input_mode':'fp','sign':sign,'ipart':ipart,'fpart':fpart,\
        'exp':exponent,'prec':prec}
 
    elif input_mode=='fr':
        if ' ' in bodystr:
            ipart=bodystr.split(' ')[0]
            numerator=(bodystr.split(' ')[1]).split('/')[0]
            deno=(bodystr.split(' ')[1]).split('/')[1]
            prec=len(ipart)+len(numerator)+len(deno)
        elif ' ' not in s:
            numerator=bodystr.split('/')[0]
            deno=bodystr.split('/')[1]
            prec=len(numerator)+len(deno)
        if ipart=='':ipart='0';prec=len(numerator)+len(deno)
        if deno=='0' or deno=='':raise ValueError("Invalid fraction")
        if numerator in ['','0']:
            prec=len(ipart)
            return {'base':base,'input_mode':'fp','sign':sign,'ipart':ipart,'fpart':'0',\
            'exp':exponent,'prec':prec}
        return {'base':base,'input_mode':'fr','sign':sign,'ipart':ipart,'numerator':numerator,\
            'deno':deno,'exp':exponent,'prec':prec}


# Dividing unsigned binary numerator by unsigned binary denominator. 
# 'prec' sets the maximum limit of the floaiting digits.
def binFractionToFloat(numerator=None,denominator=None,prec=36):
    if numerator==None or denominator==None:
        raise ValueError('Argument of binFractionToFloat() missing')
    if denominator=='0' or denominator==0:raise ValueError('Invalid denominator.')
    if numerator=='0' or numerator==0:return 'b02:0'
    s=''
    if dataType(numerator)!='str':s1=str(numerator).strip()
    elif dataType(numerator)=='str':s1=numerator.strip()
    if dataType(denominator)!='str':s2=str(denominator).strip()
    elif dataType(denominator)=='str':s2=denominator.strip()
    if not _isNumeric(s1,2):raise SyntaxError('Invalid numerator.')
    if not _isNumeric(s2,2):raise SyntaxError('Invalid denominator.')
    (l,b)=_binFractionToFloat(s1,s2,prec)
    if l[1]=='':return 'b02:'+l[0]
    elif l[0]=='':return 'b02:'+'0.'+l[1]
    else:return 'b02:'+l[0]+'.'+l[1]

# Converts binary a/b into ([ipart,fpart],boolean)
def _binFractionToFloat(numstr='',denostr='',prec=36): 
    if numstr==denostr:return (['1',''],True)
    n1,n2=int(numstr,2),int(denostr,2)
    s1='';q=0;is_accurate=False
    # Dividing n1 by n2
    if n1<n2:s1='0'
    elif n1>n2:
        q=n1//n2
        s1=bin(q)[2:]
        n1=n1%n2    
    if n1==0:return ([s1,''],True)
    s2,n,d='','',''
    i=0
    while(i<prec+2):        
        n1=n1*10
        if n1<n2:s2+='0'
        elif n1%n2==0:
            s2+=str(n1//n2)
            is_accurate=True
            break
        else:
            q=n1//n2
            s2+=str(q)
            n1=n1-q*n2 
            i+=1
    # string 'fpart' converting to floating number
    lf=len(s2)
    tmp=int(s2)
    check=int('1'+'0'*lf) # check integer
    i=0;s=''
    while(i<prec+2):
        tmp=tmp*2
        if tmp<check:
            s+='0'
        elif tmp>check:
            tmp=tmp-check
            s+='1'
        elif tmp==check:
            s+='1'
            is_accurate=True
            break
        i=i+1
    if is_accurate:return ([s1,s],True)
    else:return ([s1,s[:prec]],False)



# _intBinarySub2() is faster than _intBinarySub()
# Output is differrent. String is initialized by '0b' or '-0b'
# Inputs must be binary integer strings
def _intBinarySub2(num1='',num2=''):
    s=bin(int(num1,2)+1+(~int(num2,2)))
    if s[0]=='-':return 'b02:'+'-'+s[3:]
    else:return 'b02:'+s[2:]

# Inputs must be binary integer strings
def _binSub(num1='',num2=''):
    if num2=='':return 'b02:'+num1
    s1,s2=num1,num2
    if s1[0]=='+':s1=s1[1:]    
    if s2[0]=='+':s2=s2[1:]

    if '.' not in s1 and '.' not in s2:return _intBinarySub2(s1,s2)

    if '.' in s1:
        ipart1=s1.split('.')[0]
        fpart1=s1.split('.')[1]
    else:
        ipart1=s1
        fpart1=''

    if '.' in s2:
        ipart2=s2.split('.')[0]
        fpart2=s2.split('.')[1]
    else:
        ipart2=s2
        fpart2=''

    dp=-1
    lfp1,lfp2=len(fpart1),len(fpart2)
    if lfp1>lfp2:
        dp=lfp1
        fpart2=fpart2+'0'*(lfp1-lfp2)
    elif lfp1<lfp2:
        dp=lfp2
        fpart1=fpart1+'0'*(lfp2-lfp1)
    elif lfp1==lfp2:dp=lfp1    
    
    fs1,fs2=ipart1+fpart1,ipart2+fpart2
    s=bin(int(fs1,2)+1+(~int(fs2,2))) # '0b.......' or '-0b........'
    l=len(s)  
    if s[0]=='-':return 'b02:'+'-'+s[3:l-dp-1]+'.'+s[-1*dp:]        
    return 'b02:'+s[2:l-dp]+'.'+s[-1*dp:]


# input is a parsed number dictionary
def _isRecurring(parseddict={},prec=36):
    s='';ipart,fpart='',''
    if parseddict['input_mode']=='fp':
        if parseddict['ipart']!='0':ipart=parseddict['ipart']
        if parseddict['fpart']=='0':return False
        else: fpart=parseddict['fpart']
    elif parseddict['input_mode']=='fr':
        ipart,n,d=0,0,0
        if parseddict['base']==10:
            n=int(parseddict['numerator']);d=int(parseddict['deno'])
            if n%d==0:return False
            n=n%d;i=0;fpart=''
            while(i<=prec):        
                n=n*10
                if n<d:fpart+='0'
                elif n%d==0:return False
                else:
                    q=n//d
                    fpart+=str(q)
                    n=n-q*d 
                    i+=1
        elif parseddict['base']==2:
            (s,b)=_binFractionToFloat(parseddict['numerator'],parseddict['deno'],prec)[4:]
            if '.' in s:
                if parseddict['ipart']=='':
                    ipart=bin(int(s.split('.')[0],2))[2:]
                else:
                    ipart=bin(int(parseddict['ipart'],2)+int(s.split('.')[0],2))[2:]
                fpart=s.split('.')[1]
            else: return False
        elif parseddict['base'] in [8,16,32,64]:
            (n,b)=_toBinary(parseddict['numerator'],parseddict['base'],part='integer')
            (d,b)=_toBinary(parseddict['deno'],parseddict['base'],part='integer')
            (l,b)=_binFractionToFloat(n,d,prec)
            ipart=_binToOtherBase(l[0],parseddict['base'])
            fpart=_binToOtherBase(l[1],parseddict['base'])
    td=len(fpart)    # td=target digits
    for i in range(td//3):
        nsd=1	# nsd=Number of search digits
        while (nsd<(td-i)//2):
            matchcount=0
            searchstr=fpart[i:i+nsd]
            for j in range(i,td,nsd):
                if fpart[j:j+nsd]!=searchstr:break
                else:matchcount+=1
            reqcount=(td-i)//nsd	# reqcount=required count
            if matchcount>=reqcount and nsd*matchcount>=td-i:return True
            nsd+=1
    return False


# input is a parsed number dictionary
def _modifyNumber(parseddict={}):
    if 'normalized' in parseddict.keys():
        if parseddict['normalized']['fpart']=='0':return
    s='';ipart,fpart='',''
    if parseddict['input_mode']=='fr':
        if parseddict['base']==10:
            if parseddict['ipart']=='0':
                i,n,d=0,int(parseddict['numerator']),int(parseddict['deno'])                
            else:
                i,n,d=int(parseddict['ipart']),int(parseddict['numerator']),int(parseddict['deno'])             
            if n%d==0:
                ipart=str(i+(n//d))
                parseddict['input_mode']='fp';parseddict['ipart']=ipart;parseddict['fpart']='0'
                parseddict.pop('numerator',None);parseddict.pop('deno',None)
                parseddict['prec']=len(ipart)
            # simplifying the ratio saving time
            sratio=_sratio(n,d)
            n=sratio[0];d=sratio[1]       
            if n>d:i=i+n//d;n=n%d
            ipart=str(i);
            parseddict['ipart']=ipart;parseddict['numerator']=str(n);parseddict['deno']=str(d)
            parseddict['prec']=len(ipart)+len(parseddict['numerator'])+len(parseddict['deno'])
        elif parseddict['base']==2:
            if parseddict['ipart']=='0':
                i,n,d=0,int(parseddict['numerator'],2),int(parseddict['deno'],2)                
            else:
                i,n,d=int(parseddict['ipart'],2),int(parseddict['numerator'],2),int(parseddict['deno'],2) 
            if n%d==0:
                ipart=bin(i+(n//d))[2:]
                parseddict['input_mode']='fp';parseddict['ipart']=ipart;parseddict['fpart']='0'
                parseddict['prec']=len(ipart);parseddict.pop('numerator',None);parseddict.pop('deno',None)
            # simplifying the ratio saving time
            sratio=_sratio(n,d)
            n=sratio[0];d=sratio[1]
            if n>d:i=i+n//d;n=n%d
            # adding or updating 'base10fr' part
            if parseddict['exp']==0:           
                parseddict['base10fr']={'sign':parseddict['sign'],'ipart':str(i),'numerator':str(n),\
                    'deno':str(d),'is_accurate':True}
            ipart=bin(i)[2:]; 
            n=bin(n)[2:];d=bin(d)[2:]
            parseddict['ipart']=ipart;parseddict['numerator']=str(n);parseddict['deno']=str(d)
            parseddict['prec']=len(ipart)+len(parseddict['numerator'])+len(parseddict['deno'])
        elif parseddict['base'] in [8,16,32,64]:
            if parseddict['ipart']=='0':
                i=0;
                (n,b1)=_toBinary(parseddict['numerator'],parseddict['base'],part='integer')
                n=int(n,2)
                (d,b2)=_toBinary(parseddict['deno'],parseddict['base'],part='integer')
                d=int(d,2) 
            else:
                (i,b1)=_toBinary(parseddict['ipart'],parseddict['base'],part='integer');
                i=int(i,2);
                (n,b2)=_toBinary(parseddict['numerator'],parseddict['base'],part='integer');
                n=int(n,2);
                (d,b3)=_toBinary(parseddict['deno'],parseddict['base'],part='integer');
                d=int(d,2);
            
            if n%d==0:
                ipart=_binToOtherBase(bin(i+(n//d))[2:],parseddict['base'],part='integer')
                parseddict['input_mode']='fp';parseddict['ipart']=ipart;parseddict['fpart']='0'
                parseddict['prec']=len(ipart);parseddict.pop('numerator',None);parseddict.pop('deno',None)
                
            # simplifying the ratio saving time
            [n,d]=_sratio(n,d)
            if n>d:i=i+n//d;n=n%d 
            if parseddict['exp']==0:           
                parseddict['base10fr']={'sign':parseddict['sign'],'ipart':str(i),'numerator':str(n),\
                    'deno':str(d),'is_accurate':True}
            ipart=_binToOtherBase(bin(i)[2:],parseddict['base'],part='integer')
            n=_binToOtherBase(bin(n)[2:],parseddict['base'],part='integer')
            d=_binToOtherBase(bin(d)[2:],parseddict['base'],part='integer')
            parseddict['ipart']=ipart;parseddict['numerator']=str(n);parseddict['deno']=str(d)
            parseddict['prec']=len(ipart)+len(parseddict['numerator'])+len(parseddict['deno'])

    elif parseddict['input_mode']=='fp':
        ipart,fpart='0','0'
        if parseddict['ipart']!='0':ipart=parseddict['ipart']
        if parseddict['fpart']!='0':fpart=parseddict['fpart']
        if fpart!='0':
            td=len(fpart)	# td=target digits
            for i in range(td//3):
                nsd=1	# nsd=Number of search digits
                while (nsd<(td-i)//2):
                    matchcount=0
                    searchstr=fpart[i:i+nsd]
                    fpart=fpart+'0'*(nsd+nsd*(td//nsd)-td)
                    for j in range(i,td,nsd):
                        if fpart[j:j+nsd]!=searchstr:break
                        else:matchcount+=1
                    reqcount=(td-i)//nsd	# reqcount=required count
                    if matchcount>=reqcount and nsd*matchcount>=td-i: # if recurring
                        if parseddict['base']==10:
                            if i==0:n=int(fpart[0:i+nsd])	          # n=numerator
                            else:n=int(fpart[0:i+nsd])-int(fpart[0:i])    # n=numerator
                            d=int('9'*nsd+'0'*i)                          # d=denominator
                            # simplifying the ratio saving time
                            sratio=_sratio(n,d)
                            n=sratio[0];d=sratio[1]
                            parseddict['input_mode']='fr';parseddict['ipart']=ipart;
                            parseddict['numerator']=str(n);parseddict['deno']=str(d)                           
                            parseddict['prec']=len(ipart)+len(parseddict['numerator'])+len(parseddict['deno'])
                            if 'fpart' in parseddict.keys():parseddict.pop('fpart',None)
                        elif parseddict['base']==2:
                            n=_binSub(fpart[0:i+nsd],fpart[0:i])[4:]    # n=numerator
                            d='1'*nsd+'0'*i				# d=denominator
                            # simplifying the ratio saving time
                            sratio=_sratio(int(n,2),int(d,2))
                            if 'base10' in parseddict.keys():
                                i10fr=parseddict['base10']['ipart']
                                parseddict['base10fr']={'sign': parseddict['sign'], 'ipart':i10fr,\
                                 'numerator': str(sratio[0]), 'deno': str(sratio[1])}
                            else:
                                i10fr=int(ipart,2)
                                parseddict['base10fr']={'sign': parseddict['sign'], 'ipart': str(i10fr),\
                                 'numerator': str(sratio[0]), 'deno': str(sratio[1])}
                            n=bin(sratio[0])[2:];d=bin(sratio[1])[2:]
                            parseddict['input_mode']='fr';parseddict['ipart']=ipart;
                            parseddict['numerator']=n;parseddict['deno']=d
                            parseddict['prec']=len(ipart)+len(parseddict['numerator'])+len(parseddict['deno'])
                            if 'fpart' in parseddict.keys():parseddict.pop('fpart',None)
                        elif parseddict['base'] in [8,16,32,64]:
                            n=_binSub(_toBinary(fpart[0:i+nsd],parseddict['base']),\
                                _toBinary(fpart[0:i],parseddict['base']))[4:]
                            if parseddict['base']==8:
                                d='7'*nsd+'0'*i; d=_toBinary(d,8)
                            elif parseddict['base']==16:
                                d='f'*nsd+'0'*i; d=_toBinary(d,16)
                            elif parseddict['base']==32:
                                d='v'*nsd+'0'*i; d=_toBinary(d,32)
                            elif parseddict['base']==64:
                                d='@'*nsd+'0'*i; d=_toBinary(d,64)
                            # simplifying the ratio saving time
                            sratio=_sratio(int(n,2),int(d,2))
                            if 'base10' in parseddict.keys():
                                i10fr=parseddict['base10']['ipart']
                                parseddict['base10fr']={'sign': parseddict['sign'], 'ipart':i10fr,\
                                 'numerator': str(sratio[0]), 'deno': str(sratio[1])}
                            else: 
                                i10fr=int(_toBinary(parseddict['ipart'],base=parseddict['base'])[4:],2)
                                parseddict['base10fr']={'sign': parseddict['sign'], 'ipart': str(i10fr),\
                                 'numerator': str(sratio[0]), 'deno': str(sratio[1])}
                            n=bin(sratio[0])[2:];d=bin(sratio[1])[2:]                            
                            n=_binToOtherBase(n,parseddict['base'],part='integer')
                            d=_binToOtherBase(d,parseddict['base'],part='integer')
                            parseddict['input_mode']='fr';parseddict['ipart']=ipart;
                            parseddict['numerator']=n;parseddict['deno']=d
                            parseddict['prec']=len(ipart)+len(parseddict['numerator'])+len(parseddict['deno'])
                            if 'fpart' in parseddict.keys():parseddict.pop('fpart',None)
                    nsd+=1


# input is a parsed number dictionary
def _ultraModifyNumber(parseddict={},prec=36):
    if 'normalized' in parseddict.keys():
        if parseddict['normalized']['fpart']=='0':return
    s='';ipart,fpart='',''
    if parseddict['input_mode']=='fr':
        if parseddict['base']==10:
            if parseddict['ipart']=='0':
                i,n,d=0,int(parseddict['numerator']),int(parseddict['deno'])                
            else:
                i,n,d=int(parseddict['ipart']),int(parseddict['numerator']),int(parseddict['deno'])             
            if n%d==0:
                ipart=str(i+(n//d))
                parseddict['input_mode']='fp';parseddict['ipart']=ipart;parseddict['fpart']='0'
                parseddict.pop('numerator',None);parseddict.pop('deno',None)
                parseddict['prec']=len(ipart)
            # simplifying the ratio saving time
            sratio=_sratio2(n,d)
            n=sratio[0];d=sratio[1]       
            if n>d:i=i+n//d;n=n%d
            ipart=str(i);
            parseddict['ipart']=ipart;parseddict['numerator']=str(n);parseddict['deno']=str(d)
            parseddict['prec']=len(ipart)+len(parseddict['numerator'])+len(parseddict['deno'])
        elif parseddict['base']==2:
            if parseddict['ipart']=='0':
                i,n,d=0,int(parseddict['numerator'],2),int(parseddict['deno'],2)                
            else:
                i,n,d=int(parseddict['ipart'],2),int(parseddict['numerator'],2),int(parseddict['deno'],2) 
            if n%d==0:
                ipart=bin(i+(n//d))[2:]
                parseddict['input_mode']='fp';parseddict['ipart']=ipart;parseddict['fpart']='0'
                parseddict['prec']=len(ipart);parseddict.pop('numerator',None);parseddict.pop('deno',None)
            # simplifying the ratio saving time
            sratio=_sratio2(n,d)
            n=sratio[0];d=sratio[1]
            if n>d:i=i+n//d;n=n%d
            # adding or updating 'base10fr' part
            parseddict['base10fr']={'sign': parseddict['sign'], 'ipart': str(i), 'numerator': str(n), 'deno': str(d)}
            ipart=bin(i)[2:]; 
            n=bin(n)[2:];d=bin(d)[2:]
            parseddict['ipart']=ipart;parseddict['numerator']=str(n);parseddict['deno']=str(d)
            parseddict['prec']=len(ipart)+len(parseddict['numerator'])+len(parseddict['deno'])
        elif parseddict['base'] in [8,16,32,64]:
            if parseddict['ipart']=='0':
                i=0;
                (n,b)=_toBinary(parseddict['numerator'],parseddict['base'],part='integer')
                n=int(n,2)
                (d,b)=_toBinary(parseddict['deno'],parseddict['base'],part='integer')
                d=int(d,2) 
            else:
                (i,b)=_toBinary(parseddict['ipart'],parseddict['base'],part='integer')
                i=int(i,2)
                (n,b)=_toBinary(parseddict['numerator'],parseddict['base'],part='integer')
                n=int(n,2)
                (d,b)=_toBinary(parseddict['deno'],parseddict['base'],part='integer')
                d=int(d,2)
            if n%d==0:
                ipart=_binToOtherBase(bin(i+(n//d))[2:],parseddict['base'],part='integer')
                parseddict['input_mode']='fp';parseddict['ipart']=ipart;parseddict['fpart']='0'
                parseddict['prec']=len(ipart);parseddict.pop('numerator',None);parseddict.pop('deno',None)
            # simplifying the ratio saving time
            [n,d]=_sratio2(n,d)
            if n>d:i=i+n//d;n=n%d
            parseddict['base10fr']={'sign': parseddict['sign'], 'ipart': str(i), 'numerator': str(n), 'deno': str(d)}
            ipart=_binToOtherBase(bin(i)[2:],parseddict['base'],part='integer')
            n=_binToOtherBase(bin(n)[2:],parseddict['base'],part='integer')
            d=_binToOtherBase(bin(d)[2:],parseddict['base'],part='integer')
            parseddict['ipart']=ipart;parseddict['numerator']=str(n);parseddict['deno']=str(d)
            parseddict['prec']=len(ipart)+len(parseddict['numerator'])+len(parseddict['deno'])
    elif parseddict['input_mode']=='fp':
        ipart,fpart='0','0'
        if parseddict['ipart']!='0':ipart=parseddict['ipart']
        if parseddict['fpart']!='0':fpart=parseddict['fpart']
        if fpart!='0':
            td=len(fpart)	# td=target digits
            for i in range(td//3):
                nsd=1	# nsd=Number of search digits
                while (nsd<(td-i)//2):
                    matchcount=0
                    searchstr=fpart[i:i+nsd]
                    fpart=fpart+'0'*(nsd+nsd*(td//nsd)-td)
                    for j in range(i,td,nsd):
                        if fpart[j:j+nsd]!=searchstr:break
                        else:matchcount+=1
                    reqcount=(td-i)//nsd	# reqcount=required count
                    if matchcount>=reqcount and nsd*matchcount>=td-i: # if recurring
                        if parseddict['base']==10:
                            if i==0:n=int(fpart[0:i+nsd])	          # n=numerator
                            else:n=int(fpart[0:i+nsd])-int(fpart[0:i])    # n=numerator
                            d=int('9'*nsd+'0'*i)                          # d=denominator
                            # simplifying the ratio saving time
                            sratio=_sratio2(n,d)
                            n=sratio[0];d=sratio[1]
                            parseddict['input_mode']='fr';parseddict['ipart']=ipart;
                            parseddict['numerator']=str(n);parseddict['deno']=str(d)                           
                            parseddict['prec']=len(ipart)+len(parseddict['numerator'])+len(parseddict['deno'])
                            if 'fpart' in parseddict.keys():parseddict.pop('fpart',None)
                        elif parseddict['base']==2:
                            n=_binSub(fpart[0:i+nsd],fpart[0:i])[4:]    # n=numerator
                            d='1'*nsd+'0'*i				# d=denominator
                            # simplifying the ratio saving time
                            sratio=_sratio2(int(n,2),int(d,2))
                            if 'base10' in parseddict.keys():
                                i10fr=parseddict['base10']['ipart']
                                parseddict['base10fr']={'sign': parseddict['sign'], 'ipart':i10fr,\
                                 'numerator': str(sratio[0]), 'deno': str(sratio[1])}
                            else:
                                i10fr=int(ipart,2)
                                parseddict['base10fr']={'sign': parseddict['sign'], 'ipart': str(i10fr),\
                                 'numerator': str(sratio[0]), 'deno': str(sratio[1])}
                            n=bin(sratio[0])[2:];d=bin(sratio[1])[2:]
                            parseddict['input_mode']='fr';parseddict['ipart']=ipart;
                            parseddict['numerator']=n;parseddict['deno']=d
                            parseddict['prec']=len(ipart)+len(parseddict['numerator'])+len(parseddict['deno'])
                            if 'fpart' in parseddict.keys():parseddict.pop('fpart',None)
                        elif parseddict['base'] in [8,16,32,64]:
                            n=_binSub(_toBinary(fpart[0:i+nsd],parseddict['base']),\
                                _toBinary(fpart[0:i],parseddict['base']))[4:]
                            if parseddict['base']==8:
                                d='7'*nsd+'0'*i; d=_toBinary(d,8)
                            elif parseddict['base']==16:
                                d='f'*nsd+'0'*i; d=_toBinary(d,16)
                            elif parseddict['base']==32:
                                d='v'*nsd+'0'*i; d=_toBinary(d,32)
                            elif parseddict['base']==64:
                                d='@'*nsd+'0'*i; d=_toBinary(d,64)
                            # simplifying the ratio saving time
                            sratio=_sratio2(int(n,2),int(d,2))
                            if 'base10' in parseddict.keys():
                                i10fr=parseddict['base10']['ipart']
                                parseddict['base10fr']={'sign': parseddict['sign'], 'ipart':i10fr,\
                                 'numerator': str(sratio[0]), 'deno': str(sratio[1])}
                            else: 
                                i10fr=int(_toBinary(parseddict['ipart'],base=parseddict['base'])[4:],2)
                                parseddict['base10fr']={'sign': parseddict['sign'], 'ipart': str(i10fr),\
                                 'numerator': str(sratio[0]), 'deno': str(sratio[1])}
                            n=bin(sratio[0])[2:];d=bin(sratio[1])[2:]                            
                            n=_binToOtherBase(n,parseddict['base'],part='integer')
                            d=_binToOtherBase(d,parseddict['base'],part='integer')
                            parseddict['input_mode']='fr';parseddict['ipart']=ipart;
                            parseddict['numerator']=n;parseddict['deno']=d
                            parseddict['prec']=len(ipart)+len(parseddict['numerator'])+len(parseddict['deno'])
                            if 'fpart' in parseddict.keys():parseddict.pop('fpart',None)
                    nsd+=1


# normalizeNumberString(num) converts a number of a.bP-c format into x.y format
# prec=No of floating digits in the normalized part
def normalizeNumberString(num=None,base=10,prec=36,is_accurate=True):
    if num==None:raise ValueError('Argument of normalizedNumberString() missing')
    if num in [0,-0,0.0,-0.0]:return '0'
    if base not in [2,8,10,16,32,64]:raise ValueError('Invalid base.')
    s=''
    if dataType(num)!='str':s=str(num).strip()
    elif dataType(num)=='str':s=num.strip()
    if not _isNumeric(s,base):raise SyntaxError('Input not valid numeric.')
    parseddict=_parseNumberString(s,base)
    return _normalizeNumberString(parseddict,prec,is_accurate)

# prec=No of floating digits in the normalized part
def _normalizeNumberString(parseddict={},prec=36,is_accurate=True):
    tempdict={};
    # adding normalized part to INF and UNDEFINED
    if parseddict['ipart']=='<INF>':
        parseddict['normalized']={'sign':parseddict['sign'],'ipart':'<INF>','fpart':'0','is_accurate':True}
        parseddict['normal_prec']=0
    elif parseddict['ipart']=='<UNDEFINED>':
        parseddict['normalized']={'sign':None,'ipart':'<UNDEFINED>','fpart':None,'is_accurate':True}
        parseddict['normal_prec']=None
		
    if parseddict['exp']==0:
        # normalizing integers
        if parseddict['input_mode']=='fr' and parseddict['numerator']=='0':
            parseddict['input_mode']='fp'
            parseddict.pop('numerator',None);parseddict.pop('deno',None)
            parseddict['fpart']='0'
            parseddict['normalized']={'sign':parseddict['sign'],'ipart':parseddict['ipart'],\
                'fpart':'0','is_accurate':is_accurate}
            parseddict['is_integer']=True;parseddict['is_float']=False
            return;
        elif parseddict['input_mode']=='fp' and parseddict['fpart']=='0':
            parseddict['normalized']={'sign':parseddict['sign'],'ipart':parseddict['ipart'],\
                'fpart':'0','is_accurate':is_accurate}
            parseddict['is_integer']=True;parseddict['is_float']=False
            return;
        elif parseddict['input_mode']=='fp' and parseddict['fpart']!='0':
            parseddict['normalized']={'sign':parseddict['sign'],'ipart':parseddict['ipart'],\
                'fpart':parseddict['fpart'],'is_accurate':is_accurate}
            parseddict['is_integer']=False;parseddict['is_float']=True
            return;

    if parseddict['input_mode']=='fp' and parseddict['exp']!=0:
        ipart,fpart=parseddict['ipart'],parseddict['fpart']
        is_accurate=is_accurate

    elif parseddict['input_mode']=='fr':
        tempdict={'base':parseddict['base'],'ipart':parseddict['ipart'],\
      'numerator':parseddict['numerator'],'deno':parseddict['deno'],'exp':parseddict['exp']}
        if tempdict['base']==10:
            n,d=int(tempdict['ipart'])*int(tempdict['deno'])+int(tempdict['numerator']),int(tempdict['deno'])
            ipart=str(n//d);n=n%d;i=0;fpart=''
            while(i<=prec+1):        
                n=n*10
                if n<d:fpart+='0'
                elif n%d==0:
                    fpart+=str(n//d)
                    is_accurate=is_accurate & True
                    break
                else:
                    q=n//d
                    fpart+=str(q)
                    n=n-q*d 
                    i+=1            
        elif tempdict['base']==2:
            if tempdict['ipart']=='0':
                ([ipart,fpart],is_accurate)=_binFractionToFloat(tempdict['numerator'],tempdict['deno'],prec)
                if ipart!='0':ipart=bin(int(ipart,2))[2:];
            else:
                ([ipart,fpart],is_accurate)=_binFractionToFloat(parseddict['numerator'],parseddict['deno'],prec)
                if ipart=='0':ipart=parseddict['ipart']
                else:ipart=bin(int(ipart,2)+int(parseddict['ipart'],2))[2:]
        elif tempdict['base'] in [8,16,32,64]:
            # converting to binary
            (i,b1)=_toBinary(tempdict['ipart'],tempdict['base'],part='integer')
            (n,b2)=_toBinary(tempdict['numerator'],tempdict['base'],part='integer')
            (d,b3)=_toBinary(tempdict['deno'],tempdict['base'],part='integer')
            # converting to floating point binary
            prec=prec*_precMultiplier(tempdict['base'])
            ([ipart,fpart],b4)=_binFractionToFloat(n,d,prec)
            if ipart=='0':ipart=i #tempdict['ipart']
            else:ipart=bin(int(i,2)+int(tempdict['ipart'],2))[2:]
            is_accurate=is_accurate & b1 & b2 & b3 & b4
            # converting to original base
            ipart=_binToOtherBase(ipart,tempdict['base'],part='integer');
            fpart=_binToOtherBase(fpart,tempdict['base'],part='float');

    if parseddict['exp']==0:
        parseddict['normalized']={'sign':parseddict['sign'],'ipart':ipart,'fpart':fpart,'is_accurate':is_accurate}
        if fpart!='0':
            parseddict['is_integer']=False;parseddict['is_float']=True
        elif fpart=='0':
            parseddict['is_integer']=True;parseddict['is_float']=False

    elif parseddict['exp']>0:
        if ipart=='0' and fpart=='0':
            parseddict['normalized']={'sign':parseddict['sign'],'ipart':'0','fpart':'0','is_accurate':is_accurate}
            parseddict['is_integer']=True;parseddict['is_float']=False
        elif ipart=='0' and fpart!='0':
            l=parseddict['exp']-len(fpart)
            if l<0:
                parseddict['normalized']={'sign':parseddict['sign'],'ipart':fpart[0:parseddict['exp']].lstrip('0'),\
                    'fpart':fpart[parseddict['exp']:].rstrip('0'),'is_accurate':is_accurate}
                parseddict['is_integer']=False;parseddict['is_float']=True
            elif l>0:
                parseddict['normalized']={'sign':parseddict['sign'],'ipart':(fpart+'0'*l).lstrip('0'),\
                    'fpart':'0','is_accurate':is_accurate}
                parseddict['is_integer']=True;parseddict['is_float']=False
            else: 
                parseddict['normalized']={'sign':parseddict['sign'],'ipart':fpart.lstrip['0'],\
                    'fpart':'0','is_accurate':is_accurate}
                parseddict['is_integer']=True;parseddict['is_float']=False
        elif ipart!='0' and fpart=='0':
            l=len(ipart)-parseddict['exp']
            parseddict['normalized']={'sign':parseddict['sign'],\
                'ipart':(ipart+'0'*parseddict['exp']).lstrip('0'),'fpart':'0','is_accurate':is_accurate}
            parseddict['is_integer']=True;parseddict['is_float']=False
        elif ipart!='0' and fpart!='0':
            l=parseddict['exp']-len(fpart)
            if l>0:
                parseddict['normalized']={'sign':parseddict['sign'],'ipart':ipart+fpart+'0'*l,\
                    'fpart':'0','is_accurate':is_accurate}
                parseddict['is_integer']=True; parseddict['is_float']=False
            elif l<0:
                parseddict['normalized']={'sign':parseddict['sign'],'ipart':ipart+fpart[0:parseddict['exp']],\
                    'fpart':fpart[parseddict['exp']:],'is_accurate':is_accurate}
                parseddict['is_integer']=False;parseddict['is_float']=True
            else: 
                parseddict['normalized']={'sign':parseddict['sign'],'ipart':ipart+fpart,\
                    'fpart':'0','is_accurate':is_accurate}
                parseddict['is_integer']=True;parseddict['is_float']=False
    elif parseddict['exp']<0:
        if ipart=='0' and fpart=='0':
            parseddict['normalized']={'sign':parseddict['sign'],'ipart':'0','fpart':'0','is_accurate':is_accurate}
            parseddict['is_integer']=True;parseddict['is_float']=False
        elif ipart=='0' and fpart!='0':
            l=parseddict['exp']-len(fpart)
            parseddict['normalized']={'sign':parseddict['sign'],'ipart':'0',\
               'fpart':('0'*(-parseddict['exp'])+fpart).rstrip('0'),'is_accurate':is_accurate}
            parseddict['is_integer']=False;parseddict['is_float']=True
        elif ipart!='0' and fpart=='0':
            l=-parseddict['exp']-len(ipart)
            if l>0:
                parseddict['normalized']={'sign':parseddict['sign'],\
                    'ipart':'0','fpart':('0'*l+ipart).rstrip('0'),'is_accurate':is_accurate}
                parseddict['is_integer']=False;parseddict['is_float']=True
            elif l<0:
                parseddict['normalized']={'sign':parseddict['sign'],'ipart':ipart[0:-l].lstrip('0'),\
                    'fpart':(ipart[parseddict['exp']:]).rstrip('0'),'is_accurate':is_accurate}
                parseddict['is_integer']=False;parseddict['is_float']=True
            else: 
                parseddict['normalized']={'sign':parseddict['sign'],'ipart':'0',\
                    'fpart':ipart.rstrip('0'),'is_accurate':is_accurate}
                parseddict['is_integer']=False;parseddict['is_float']=True
        elif ipart!='0' and fpart!='0':
            l=-parseddict['exp']-len(ipart)
            if l>0:
                parseddict['normalized']={'sign':parseddict['sign'],'ipart':'0',\
                    'fpart':('0'*l+ipart+fpart).rstrip('0'),'is_accurate':is_accurate}
                parseddict['is_integer']=False;parseddict['is_float']=True
            elif l<0:
                parseddict['normalized']={'sign':parseddict['sign'],'ipart':ipart[0:-l].lstrip('0'),\
                    'fpart':(ipart[parseddict['exp']:]+fpart).rstrip('0'),'is_accurate':is_accurate}
                parseddict['is_integer']=False;parseddict['is_float']=True
            else: 
                parseddict['normalized']={'sign':parseddict['sign'],'ipart':(ipart+fpart).lstrip('0'),\
                    'fpart':'0','is_accurate':is_accurate}
                parseddict['is_integer']=True;parseddict['is_float']=False


# _normalizeToFP() converts the parsed dictionary into a normalized and simplified dictionary
# prec=No of floating digits in the normalized part
def _normalizeToFP(parseddict={},prec=36,is_accurate=True):
    ipart='';fpart='';i,n,d='','',''
    if parseddict['base']==2:
        if parseddict['input_mode']=='fr':
            if parseddict['ipart']=='0':
                (l,is_accurate)=_binFractionToFloat(parseddict['numerator'],parseddict['deno'],prec)
                if l[0]=='0':ipart='';fpart=l[1]
                else:ipart=bin(int(l[0],2))[2:];fpart=l[1]
            else:
                (l,is_accurate)=_binFractionToFloat(parseddict['numerator'],parseddict['deno'],prec)
                if l[0]=='0':ipart=parseddict['ipart'];fpart=l[1]
                else:ipart=bin(int(l[0],2)+int(parseddict['ipart'],2))[2:];fpart=l[1]            
        elif parseddict['input_mode']=='fp':
            ipart=parseddict['ipart']
            fpart=parseddict['fpart']
            is_accurate=is_accurate & True
    elif parseddict['base'] in [8,16,32,64]:
        if parseddict['input_mode']=='fp':
            ipart=parseddict['ipart'];fpart=parseddict['fpart']
            is_accurate=is_accurate & True
        elif parseddict['input_mode']=='fr':
            i,n,d=parseddict['ipart'],parseddict['numerator'],parseddict['deno']
            if parseddict['ipart']=='0':
                # converting to binary
                (parseddict['numerator'],b1)=_toBinary(parseddict['numerator'],parseddict['base'],part='integer')
                (parseddict['deno'],b2)=_toBinary(parseddict['deno'],parseddict['base'],part='integer')
                # converting to floating point binary
                prec=prec*_precMultiplier(parseddict['base'])
                (l,b3)=_binFractionToFloat(parseddict['numerator'],parseddict['deno'],prec)
                is_accurate=is_accurate & b1 & b2 & b3
                if l[0]=='0':ipart='';fpart=l[1]
                else:ipart=l[0];fpart=l[1]
                # converting to original base
                ipart=_binToOtherBase(ipart,parseddict['base'],part='integer');
                fpart=_binToOtherBase(fpart,parseddict['base'],part='float');
                parseddict['ipart']=i;parseddict['numerator']=n;parseddict['deno']=d
            else:
                # converting to binary
                (parseddict['ipart'],b1)=_toBinary(parseddict['ipart'],parseddict['base'],part='integer')
                (parseddict['numerator'],b2)=_toBinary(parseddict['numerator'],parseddict['base'],part='integer')
                (parseddict['deno'],b3)=_toBinary(parseddict['deno'],parseddict['base'],part='integer')
                # converting to floating point binary
                prec=prec*_precMultiplier(parseddict['base'])
                (l,b4)=_binFractionToFloat(parseddict['numerator'],parseddict['deno'],prec)
                is_accurate=is_accurate & b1 & b2 & b3 & b4
                if l[0]=='0':ipart=parseddict['ipart'];fpart=l[1]
                else:ipart=bin(int(l[0],2)+int(parseddict['ipart'],2))[2:];fpart=l[1]
                # converting to original base
                ipart=_binToOtherBase(ipart,parseddict['base'],part='integer');
                fpart=_binToOtherBase(fpart,parseddict['base'],part='float');
                parseddict['ipart']=i;parseddict['numerator']=n;parseddict['deno']=d
    elif parseddict['base']==10:
        if parseddict['input_mode']=='fr':
            ipart,n,d='',0,0
            n=int(parseddict['numerator']);d=int(parseddict['deno'])
            ipart=str(int(parseddict['ipart'])+n//d)
            # dividing n by d
            n=n%d;i=0;fpart=''
            while(i<=prec+1):
                n=n*10
                if n<d:fpart+='0'
                elif n%d==0:
                    fpart+=str(n//d)
                    is_accurate=True
                    break
                else:
                    q=n//d
                    fpart+=str(q)
                    n=n-q*d 
                    i+=1            
        elif parseddict['input_mode']=='fp':
            ipart=parseddict['ipart']
            fpart=parseddict['fpart']
            is_accurate=is_accurate & True
    exponent=parseddict['exp']
    if exponent>0:
        if exponent<len(fpart):
            ipart=ipart+fpart[:exponent];fpart=fpart[exponent:]
        else:
            ipart=ipart+fpart+'0'*(exponent-len(fpart));fpart=''
    elif exponent<0:
        lmd=len(ipart)+exponent #lmd=leftmost digits
        if lmd>0:
            fpart=ipart[lmd:]+fpart;ipart=ipart[:lmd];
        elif lmd==0:
            fpart=ipart+fpart;ipart='';
        else:
            fpart='0'*(-1*lmd)+ipart+fpart;ipart='';
    return {'input_mode':'fp','base':parseddict['base'],'sign':parseddict['sign'],'ipart':ipart,'fpart':fpart,'exp':0,'is_accurate':is_accurate}



# toBinary(num,base,part,prec) converts denary, octal, hexadecimal,
# duotrigesimal (base32), and base64 unsigned integer or floating part to binary
# For large value input, the number input must be string
def toBinary(num=None,base=10,part='integer',prec=36):
    if num==None:raise ValueError('Argument of toBinary() missing')
    if base not in [2,8,10,16,32,64]:raise ValueError('Invalid Number Base.')
    s=''
    if dataType(num)!='str':s=str(num).strip()
    elif dataType(num)=='str':s=num.strip()
    if not _isNumeric(s,base):raise SyntaxError('Input is not a valid number.')
    if s[0]=='-': raise ValueError("Input number must be unsigned or positive")
    if base==2:return 'b02:'+s
    if part=='integer':(s1,b)=_toBinary(s,base,part,prec);return 'b02:'+s1
    elif part=='float':(s1,b)=_toBinary(s,base,part,prec);return 'b02:'+s1


# input number must be a string.
# there is some accuracy loss when floating denary is converted to
# floating binary
def _toBinary(numstr='',base=10,part='integer',prec=36):
    if numstr=='':return ''
    if numstr[0]=='-': raise ValueError("Input number must be unsigned or positive")
    is_accurate=False

    # Converting denary to binary
    if base==10:
        if part=='integer':
            namestr=numstr.lstrip('0')
            return (bin(int(numstr))[2:],True)
        elif part=='float':
            namestr=numstr.rstrip('0')
            lf=len(numstr)
            tmp=int(numstr)
            check=int('1'+'0'*len(numstr)) # check integer
            i=0;s=''
            while(i<prec+1):	# i<prec*6 to maintain precision upto base64 number
                tmp=tmp*2
                if tmp<check:
                    s+='0'
                elif tmp>check:
                    tmp=tmp-check
                    s+='1'
                elif tmp==check:
                    s+='1'
                    is_accurate=True
                    break
                i=i+1
            if is_accurate: return (s,True)
            else: return (s,False)

    # Converting octal to binary
    elif base==8:
        octalDigits={'0':'000','1':'001','2':'010','3':'011','4':'100',\
            '5':'101','6':'110','7':'111'}
        s=''
        if part=='integer':
            namestr=numstr.lstrip('0')
            l=len(numstr)
            for i in range(l-1,-1,-1):s=octalDigits[numstr[i]]+s
            return (s.lstrip('0'),True)
        elif part=='float':
            namestr=numstr.rstrip('0')
            l=len(numstr)
            for i in range(l):s=s+octalDigits[numstr[i]]
            return (s.rstrip('0'),True)

    # Converting hexadecimal to binary
    elif base==16:
        hexaDigits={'0':'0000','1':'0001','2':'0010','3':'0011','4':'0100',\
            '5':'0101','6':'0110','7':'0111','8':'1000','9':'1001','a':'1010',\
            'A':'1010','b':'1011','B':'1011','c':'1100','C':'1100','d':'1101',\
            'D':'1101','e':'1110','E':'1110','f':'1111','F':'1111'}
        s='';
        if part=='integer':
            numstr=numstr.lstrip('0')
            l=len(numstr);          
            for i in range(l-1,-1,-1):s=hexaDigits[numstr[i]]+s 
            return (s.lstrip('0'),True)
        elif part=='float':
            numstr=numstr.rstrip('0')
            l=len(numstr)
            for i in range(l):s=s+hexaDigits[numstr[i]]
            return (s.rstrip('0'),True)


    # Converting duotrigesimal(base32) to binary
    elif base==32:
        base32Digits={'0':'00000','1':'00001','2':'00010','3':'00011','4':'00100',\
       	    '5':'00101','6':'00110','7':'00111','8':'01000','9':'01001','a':'01010',\
            'A':'01010','b':'01011','B':'01011','c':'01100','C':'01100','d':'01101',\
            'D':'01101','e':'01110','E':'01110','f':'01111','F':'01111','g':'10000',\
            'G':'10000','h':'10001','H':'10001','i':'10010','I':'10010','j':'10011',\
            'J':'10011','k':'10100','K':'10100','l':'10101','L':'10101','m':'10110',\
            'M':'10110','n':'10111','N':'10111','o':'11000','O':'11000','p':'11001',\
            'P':'11001','q':'11010','Q':'11010','r':'11011','R':'11011','s':'11100',\
            'S':'11100','t':'11101','T':'11101','u':'11110','U':'11110','v':'11111',\
            'V':'11111'}
        s=''
        if part=='integer':
            namestr=numstr.lstrip('0')
            l=len(numstr);
            for i in range(l-1,-1,-1):s=base32Digits[numstr[i]]+s                
            return (s.lstrip('0'),True)
        elif part=='float':
            namestr=numstr.rstrip('0')
            l=len(numstr)
            for i in range(l):s=s+base32Digits[numstr[i]]
            return (s.rstrip('0'),True)

    # Converting base64 to binary
    elif base==64:
        base64Digits={'0':'000000','1':'000001','2':'000010','3':'000011','4':'000100',\
        '5':'000101','6':'000110','7':'000111','8':'001000','9':'001001','a':'001010',\
        'b':'001011','c':'001100','d':'001101','e':'001110','f':'001111','g':'010000',\
        'h':'010001','i':'010010','j':'010011','k':'010100','l':'010101','m':'010110',\
        'n':'010111','o':'011000','p':'011001','q':'011010','r':'011011','s':'011100',\
        't':'011101','u':'011110','v':'011111','w':'100000','x':'100001','y':'100010',\
        'z':'100011','A':'100100','B':'100101','C':'100110','D':'100111','E':'101000',\
        'F':'101001','G':'101010','H':'101011','I':'101100','J':'101101','K':'101110',\
        'L':'101111','M':'110000','N':'110001','O':'110010','P':'110011','Q':'110100',\
        'R':'110101','S':'110110','T':'110111','U':'111000','V':'111001','W':'111010',\
        'X':'111011','Y':'111100','Z':'111101','!':'111110','@':'111111'}
        s=''
        if part=='integer':
            namestr=numstr.lstrip('0')
            l=len(numstr);
            for i in range(l-1,-1,-1):s=base64Digits[numstr[i]]+s                
            return (s.lstrip('0'),True)
        elif part=='float':
            namestr=numstr.rstrip('0')
            l=len(numstr)
            for i in range(l):s=s+base64Digits[numstr[i]]
            return (s.rstrip('0'),True)


# binToOtherBase(num,base,part,prec) converts binary to octal, hexadecimal, duotrigesimal
# (base32), and base64 number
# For large value input, the number input must be string
def binToOtherBase(num=None,base=10,part='integer'):
    if num==None:raise ValueError('Argument of binToOtherBase() missing')
    if base not in [2,8,10,16,32,64]:raise ValueError('Invalid Number Base.')
    s=''
    if dataType(num)!='str':s=str(num).strip()
    elif dataType(num)=='str':s=num.strip()
    if not _isNumeric(s,base):raise SyntaxError('Input is not a valid number.')
    if s[0]=='-': raise ValueError("Input number must be unsigned or positive")
    if base==2:return 'b02:'+s
    if part=='integer':return _baseInsert(base)+_binToOtherBase(s,base,part)
    elif part=='float':return _baseInsert(base)+'0.'+_binToOtherBase(s,base,part)

# input number must be a string; No precision loss during conversion
def _binToOtherBase(numstr="",base=10,part='integer'):
    if numstr=='':return ''
    if numstr[0]=='-': raise ValueError("Input number must be unsigned or positive")
    # Converting binary to denary
    if base==10:
        if part=='integer':
            return str(int(numstr,2))
        elif part=='float':
            lf=len(numstr) #lf=length of floating part
            i,SUM,deno=0,0,1
            while(i<lf):
                if numstr[lf-i-1]=='1':SUM+=deno
                i+=1
                deno*=2
            # Dividing numerator by denominator
            numerator=SUM
            s=''
            i=0
            while(i<lf):
                numerator=numerator*10
                if numerator<deno:s+='0'
                elif numerator==deno:
                    s+='1'
                    break
                else:
                    if numerator>=deno*9:s+='9';numerator=numerator-9*deno
                    elif numerator>=deno*8:s+='8';numerator=numerator-8*deno
                    elif numerator>=deno*7:s+='7';numerator=numerator-7*deno
                    elif numerator>=deno*6:s+='6';numerator=numerator-6*deno
                    elif numerator>=deno*5:s+='5';numerator=numerator-5*deno
                    elif numerator>=deno*4:s+='4';numerator=numerator-4*deno
                    elif numerator>=deno*3:s+='3';numerator=numerator-3*deno
                    elif numerator>=deno*2:s+='2';numerator=numerator-2*deno
                    elif numerator>=deno:s+='1';numerator=numerator-1*deno
                    if numerator==0:break
                i+=1
            return s

    # Converting binary to octal
    elif base==8:
        octalDigits=('000','001','010','011','100','101','110','111')
        s=''
        if part=='integer':
            numstr=numstr.lstrip('0')
            l=len(numstr)
            if l%3!=0:
                numstr='0'*(3-l%3)+numstr
                l=l+3-l%3
            for i in range(l,0,-3):s=str(octalDigits.index(numstr[i-3:i]))+s
            return s
        # Converting floating part
        elif part=='float':
            numstr=numstr.rstrip('0')
            l=len(numstr)
            if l%3!=0:
                numstr=numstr+'0'*(3-l%3)
                l=l+3-l%3
            for i in range(0,l,3):s=s+str(octalDigits.index(numstr[i:i+3]))
            return s


    # Converting binary to hexadecimal
    elif base==16:
        hexaDigits=('0000','0001','0010','0011','0100','0101','0110','0111',\
            '1000','1001','1010','1011','1100','1101','1110','1111')
        hextouple=('0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f')
        # Converting integer part
        if part=='integer':
            s=''
            namestr=numstr.lstrip('0')
            l=len(numstr)
            if l%4!=0:
                numstr='0'*(4-l%4)+numstr
                l=l+4-l%4
            for i in range(l,0,-4):s=hextouple[hexaDigits.index(numstr[i-4:i])]+s
            return s
        # Converting floating part
        elif part=='float':
            s=''
            namestr=numstr.rstrip('0')
            l=len(numstr)
            if l%4!=0:
                numstr=numstr+'0'*(4-l%4)
                l=l+4-l%4
            for i in range(0,l,4):s=s+hextouple[hexaDigits.index(numstr[i:i+4])]
            return s


    # Converting binary to duotrigesimal(base32)
    elif base==32:
        base32Digits=('00000','00001','00010','00011','00100','00101','00110','00111',\
            '01000','01001','01010','01011','01100','01101','01110','01111','10000',\
            '10001','10010','10011','10100','10101','10110','10111','11000','11001',\
            '11010','11011','11100','11101','11110','11111')
        base32touple=('0','1','2','3','4','5','6','7','8','9','a','b','c','d','e',\
             'f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v')
        # Converting integer part
        if part=='integer':
            s=''
            namestr=numstr.lstrip('0')
            l=len(numstr) 
            if l%5!=0:
                numstr='0'*(5-l%5)+numstr
                l=l+5-l%5
            for i in range(l,0,-5):s=base32touple[base32Digits.index(numstr[i-5:i])]+s
            return s
        # Converting floating part
        elif part=='float':
            s=''
            namestr=numstr.rstrip('0')
            l=len(numstr)
            if l%5!=0:
                numstr=numstr+'0'*(5-l%5)
                l=l+5-l%5
            for i in range(0,l,5):s=s+base32touple[base32Digits.index(numstr[i:i+5])]
            return s

    # Converting binary to base64
    elif base==64:
        base64Digits=('000000','000001','000010','000011','000100',\
            '000101','000110','000111','001000','001001','001010',\
            '001011','001100','001101','001110','001111','010000',\
            '010001','010010','010011','010100','010101','010110',\
            '010111','011000','011001','011010','011011','011100',\
            '011101','011110','011111','100000','100001','100010',\
            '100011','100100','100101','100110','100111','101000',\
            '101001','101010','101011','101100','101101','101110',\
            '101111','110000','110001','110010','110011','110100',\
            '110101','110110','110111','111000','111001','111010',\
            '111011','111100','111101','111110','111111')
        base64touple=('0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g',\
            'h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',\
            'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S',\
            'T','U','V','W','X','Y','Z','!','@')
        # Converting integer part
        if part=='integer':
            s=''
            namestr=numstr.lstrip('0')
            l=len(numstr) 
            if l%6!=0:
                numstr='0'*(6-l%6)+numstr
                l=l+6-l%6
            for i in range(l,0,-6):s=base64touple[base64Digits.index(numstr[i-6:i])]+s
            return s
        # Converting floating part
        elif part=='float':
            s=''
            namestr=numstr.rstrip('0')
            l=len(numstr)
            if l%6!=0:
                numstr=numstr+'0'*(6-l%6)
                l=l+6-l%6
            for i in range(0,l,6):s=s+base64touple[base64Digits.index(numstr[i:i+6])]
            return s

# _addBase64(parseddict) adds base64 version of the number
def _addBase64(parseddict={},prec=36):    
    if parseddict['base']!=64:
        if 'normalized' in parseddict.keys():
            ndict={'input_mode':'fp','base':parseddict['base'],'sign':parseddict['sign'],\
                'ipart':parseddict['normalized']['ipart'],'fpart':parseddict['normalized']['fpart'],'exp':0}
        else:ndict=_normalizeToFP(parseddict,prec)

        if ndict['ipart']=='0' and ndict['fpart']=='0':
            parseddict['base64']={'sign':parseddict['sign'],'ipart':'0','fpart':'0','is_accurate':True}

        ipart,fpart='','';is_accurate=ndict['is_accurate']
        if ndict['base']==2:
            if ndict['ipart']=='0':
                fpart=_binToOtherBase(ndict['fpart'],64,'float')
            elif ndict['fpart']=='0':
                ipart=_binToOtherBase(ndict['ipart'],64,'integer')
            else:
                ipart=_binToOtherBase(ndict['ipart'],64,'integer')
                fpart=_binToOtherBase(ndict['fpart'],64,'float')
            is_accurate=is_accurate & True
        elif ndict['base'] in [10,8,16,32]:
            if ndict['ipart']=='0':
                (fpart,b1)=_toBinary(ndict['fpart'],ndict['base'],'float',prec)
                fpart=_binToOtherBase(fpart,64,'float')
                is_accurate=is_accurate & b1
            else:
                (ipart,b1)=_toBinary(ndict['ipart'],ndict['base'],'integer',prec)
                ipart=_binToOtherBase(ipart,64,'integer')
                (fpart,b2)=_toBinary(ndict['fpart'],ndict['base'],'float',prec)
                fpart=_binToOtherBase(fpart,64,'float')
                is_accurate=is_accurate & b1 & b2
        if ipart=='':ipart='0'
        if fpart=='':fpart='0'
        parseddict['base64']={'sign':parseddict['sign'],'ipart':ipart,'fpart':fpart,'is_accurate':is_accurate}


# _getBase64Form(parseddict) converts the number into base64 version
def _getBase64Form(parseddict={},prec=36):
    if parseddict['base']==64:return parseddict

    if 'normalized' in parseddict.keys():
        ndict={'input_mode':'fp','base':parseddict['base'],'sign':parseddict['sign'],\
            'ipart':parseddict['normalized']['ipart'],'fpart':parseddict['normalized']['fpart'],'exp':0}
    else:ndict=_normalizeToFP(parseddict,prec)

    if ndict['ipart']=='0' and ndict['fpart']=='0':
        return {'input_mode':'fp','base':64,'sign':ndict['sign'],'ipart':'0','fpart':'0','exp':0}

    ipart,fpart='',''
    if ndict['base']==2:
        if ndict['ipart']=='0':
            fpart=_binToOtherBase(ndict['fpart'],64,part='float')
        else:
            ipart=_binToOtherBase(ndict['ipart'],64,part='integer')
            fpart=_binToOtherBase(ndict['fpart'],64,part='float')
    elif ndict['base'] in [10,8,16,32]:
        if ndict['ipart']=='0':
            (fpart,is_accurate)=_toBinary(ndict['fpart'],ndict['base'],part='float',prec=prec)
            fpart=_binToOtherBase(fpart,64,part='float')
        elif ndict['fpart']=='0':
            (ipart,is_accurate)=_toBinary(ndict['ipart'],ndict['base'],part='integer',prec=prec)
            ipart=_binToOtherBase(ipart,64,part='integer')
        else:
            (ipart,b1)=_toBinary(ndict['ipart'],ndict['base'],part='integer',prec=prec)
            ipart=_binToOtherBase(ipart,64,part='integer')
            (fpart,b2)=_toBinary(ndict['ipart'],ndict['base'],part='integer',prec=prec)
            fpart=_binToOtherBase(fpart,64,part='float')
            is_accurate=b1 & b2
    if ipart=='':ipart='0'
    if fpart=='':fpart='0'
    return {'input_mode':'fp','base':64,'sign':ndict['sign'],'ipart':ipart,'fpart':fpart,'exp':0}


# _addBinaryForm(parseddict) adds binary form in the number dictionary
def _addBinaryForm(parseddict={},prec=36):
    if parseddict['base']!=2:
        if 'normalized' in parseddict.keys():
            ndict={'input_mode':'fp','base':parseddict['base'],'sign':parseddict['sign'],\
            'ipart':parseddict['normalized']['ipart'],'fpart':parseddict['normalized']['fpart'],'exp':0}
        else:ndict=_normalizeToFP(parseddict,prec)

        if ndict['ipart']=='0' and ndict['fpart']=='0':
            parseddict['base2']={'sign':parseddict['sign'],'ipart':'0','fpart':'0','is_accurate':True}

        ipart,fpart='','';is_accurate=ndict['is_accurate']
        if ndict['base']==10:
            if ndict['ipart']=='0':
                (fpart,b1)=_toBinary(ndict['fpart'],10,part='float',prec=prec)
                is_accurate=is_accurate & b1
            elif ndict['fpart']=='0':
                (ipart,b1)=_toBinary(ndict['ipart'],10,part='integer',prec=prec)
                is_accurate=is_accurate & b1
            else:
                (ipart,b1)=_toBinary(ndict['ipart'],10,part='integer',prec=prec)
                (fpart,b2)=_toBinary(ndict['fpart'],10,part='float',prec=prec)
                is_accurate=is_accurate & b1 & b2
        elif ndict['base'] in [8,16,32,64]:
            if ndict['ipart']=='0':
                (fpart,is_accurate)=_toBinary(ndict['fpart'],ndict['base'],part='float',prec=prec)
            else:
                (ipart,b1)=_toBinary(ndict['ipart'],ndict['base'],part='integer',prec=prec)
                (fpart,b2)=_toBinary(ndict['fpart'],ndict['base'],part='float',prec=prec)
                is_accurate=b1 & b2
        if ipart=='':ipart='0'
        if fpart=='':fpart='0'
        parseddict['base2']={'sign':parseddict['sign'],'ipart':ipart,'fpart':fpart,'is_accurate':is_accurate}


# _getBinaryForm(parseddict) converts the parsed dictionary into binary form
def _getBinaryForm(parseddict={},prec=36):
    if parseddict['base']==2:
       return parseddict
    if 'normalized' in parseddict.keys():
        ndict={'input_mode':'fp','base':parseddict['base'],'sign':parseddict['sign'],\
            'ipart':parseddict['normalized']['ipart'],'fpart':parseddict['normalized']['fpart'],'exp':0}
    else:ndict=_normalizeToFP(parseddict,prec)

    if ndict['ipart']=='0' and ndict['fpart']=='0':
        return {'input_mode':'fp','base':2,'sign':ndict['sign'],'ipart':'0','fpart':'0','exp':0}

    ipart,fpart='',''
    if ndict['base']==10:
        if ndict['ipart']=='0':
            (fpart,b1)=_toBinary(ndict['fpart'],10,part='float',prec=prec)
        elif ndict['fpart']=='0':
            (ipart,b1)=_toBinary(ndict['ipart'],10,part='integer',prec=prec)
        else:
            (ipart,b1)=_toBinary(ndict['ipart'],10,part='integer',prec=prec)
            (fpart,b2)=_toBinary(ndict['fpart'],10,part='float',prec=prec)
    elif ndict['base'] in [8,16,32,64]:
        if ndict['ipart']=='0':
            (fpart,b1)=_toBinary(ndict['fpart'],ndict['base'],part='float',prec=prec)
        else:
            (ipart,b1)=_toBinary(ndict['ipart'],ndict['base'],part='integer',prec=prec)
            (fpart,b2)=_toBinary(ndict['fpart'],ndict['base'],part='float',prec=prec)
    if ipart=='':ipart='0'
    if fpart=='':fpart='0'
    return {'input_mode':'fp','base':2,'sign':ndict['sign'],'ipart':ipart,'fpart':fpart,'exp':0}


# _addDenary(parseddict) add denary component if the number is not denary 
def _addDenary(parseddict={},prec=36):
    if parseddict['base']!=10:
        if 'normalized' in parseddict.keys():
            ndict={'input_mode':'fp','base':parseddict['base'],'sign':parseddict['sign'],\
                'ipart':parseddict['normalized']['ipart'],'fpart':parseddict['normalized']['fpart'],'exp':0,\
                'is_accurate':parseddict['normalized']['is_accurate']}
        else:ndict=_normalizeToFP(parseddict,prec)

        if ndict['ipart']=='0' and ndict['fpart']=='0':
            parseddict['base10']={'sign':parseddict['sign'],'ipart':'0','fpart':'0','is_accurate':True}

        ipart,fpart='','';is_accurate=ndict['is_accurate']
        if ndict['base']==2:
            if ndict['ipart']=='0':
                fpart=_binToOtherBase(ndict['fpart'],10,part='float')
            elif ndict['fpart']=='0':
                ipart=_binToOtherBase(ndict['ipart'],10,part='integer')
            else:
                ipart=_binToOtherBase(ndict['ipart'],10,part='integer')
                fpart=_binToOtherBase(ndict['fpart'],10,part='float')
            is_accurate=is_accurate & True
        elif ndict['base'] in [8,16,32,64]:
            if ndict['ipart']=='0':
                (fpart,is_accurate)=_toBinary(ndict['fpart'],ndict['base'],part='float',prec=prec)
                fpart=_binToOtherBase(fpart,10,part='float')
            elif ndict['fpart']=='0':
                (ipart,b1)=_toBinary(ndict['ipart'],ndict['base'],part='integer',prec=prec)
                ipart=_binToOtherBase(ipart,10,part='integer')
                is_accurate=is_accurate & b1
            else:
                (ipart,b1)=_toBinary(ndict['ipart'],ndict['base'],part='integer',prec=prec)
                ipart=_binToOtherBase(ipart,10,part='integer')
                (fpart,b2)=_toBinary(ndict['fpart'],ndict['base'],part='float',prec=prec)
                fpart=_binToOtherBase(fpart,10,part='float')
                is_accurate=is_accurate & b1 & b2
        if ipart=='':ipart='0'
        if fpart=='':fpart='0'
        parseddict['base10']={'sign':parseddict['sign'],'ipart':ipart,'fpart':fpart,'is_accurate':is_accurate}
    elif parseddict['base']==10:	#adding denary part in denary number
        parseddict['base10']=parseddict['normalized']

# _addDenaryFR(parseddict) adds fractional denary component in the number dictionary 
def _addDenaryFR(parseddict={},prec=36): 
    #if parseddict['ipart']=='0' and parseddict['numerator']=='0':
    #    parseddict['base10fr']={'sign':parseddict['sign'],'ipart':'0','numerator':'0','deno':parseddict['deno']}
    if parseddict['base']==2 and parseddict['input_mode']=='fr' and parseddict['exp']==0:
        if parseddict['ipart']=='0':ipart='0'
        else:ipart=_binToOtherBase(parseddict['ipart'],10,part='integer')
        n=_binToOtherBase(parseddict['numerator'],10,part='integer')
        d=_binToOtherBase(parseddict['deno'],10,part='integer')
        parseddict['base10fr']={'sign':parseddict['sign'],'ipart':ipart,'numerator':n,'deno':d,'is_accurate':True}
    elif parseddict['base'] in [8,16,32,64] and parseddict['input_mode']=='fr' and parseddict['exp']==0:
        if parseddict['ipart']=='0':ipart='0'
        else:
            (ipart,b1)=_toBinary(parseddict['ipart'],parseddict['base'],prec=prec)
            ipart=_binToOtherBase(ipart,10,part='integer')
        (n,b2)=_toBinary(parseddict['numerator'],parseddict['base'],prec=prec)
        n=_binToOtherBase(n,10,part='integer')
        (d,b3)=_toBinary(parseddict['deno'],parseddict['base'],prec=prec)
        d=_binToOtherBase(d,10,part='integer')
        is_accurate=b1 & b2 & b3
        #if ipart=='':ipart='0'
        if n=='':n='0'
        if d=='':d='0'
        parseddict['base10fr']={'sign':parseddict['sign'],'ipart':ipart,'numerator':n,'deno':d,\
            'is_accurate':is_accurate}
    elif parseddict['base']==10:	#adding denary part in denary number
        parseddict['base10']=parseddict['normalized']

# _getDenaryForm(parseddict={},prec=36) returns denary form of other base numbers 
def _getDenaryForm(parseddict={},prec=36):
    if parseddict['base']==10:
       return parseddict
    if 'normalized' in parseddict.keys():
        ndict={'input_mode':'fp','base':parseddict['base'],'sign':parseddict['sign'],\
            'ipart':parseddict['normalized']['ipart'],'fpart':parseddict['normalized']['fpart'],'exp':0}
    else:ndict=_normalizeToFP(parseddict,prec)

    if ndict['ipart']=='0' and ndict['fpart']=='0':
        return {'input_mode':'fp','base':10,'sign':ndict['sign'],'ipart':'0','fpart':'0','exp':0}

    ipart,fpart='',''
    if ndict['base']==2:
        if ndict['ipart']=='0':
            fpart=_binToOtherBase(ndict['fpart'],10,part='float')
        elif ndict['fpart']=='0':
            ipart=_binToOtherBase(ndict['ipart'],10,part='integer')
        else:
            ipart=_binToOtherBase(ndict['ipart'],10,part='integer')
            fpart=_binToOtherBase(ndict['fpart'],10,part='float')
    elif ndict['base'] in [8,16,32,64]:
        if ndict['ipart']=='0':
            (fpart,b1)=_toBinary(ndict['fpart'],ndict['base'],part='float',prec=prec)
            fpart=_binToOtherBase(fpart,10,part='float')
        else:
            (ipart,b1)=_toBinary(ndict['ipart'],ndict['base'],part='integer',prec=prec)
            ipart=_binToOtherBase(ipart,10,part='integer')
            (fpart,b2)=_toBinary(ndict['fpart'],ndict['base'],part='float',prec=prec)
            fpart=_binToOtherBase(fpart,10,part='float')
    if ipart=='':ipart='0'
    if fpart=='':fpart='0'
    return {'input_mode':'fp','base':10,'sign':ndict['sign'],'ipart':ipart,'fpart':fpart,'exp':0}


# _getOctalForm(parseddict) converts the number dictionary into base8 version
def _getOctalForm(parseddict={},prec=36):
    if parseddict['base']==8:return parseddict
    if 'normalized' in parseddict.keys():
        ndict={'input_mode':'fp','base':parseddict['base'],'sign':parseddict['sign'],\
            'ipart':parseddict['normalized']['ipart'],'fpart':parseddict['normalized']['fpart'],'exp':0}
    else:ndict=_normalizeToFP(parseddict,prec)

    if ndict['ipart']=='0' and ndict['fpart']=='0':
        return {'input_mode':'fp','base':8,'sign':ndict['sign'],'ipart':'0','fpart':'0','exp':0}
 
    ipart,fpart='',''
    if ndict['base']==2:
        if ndict['ipart']=='0':
            fpart=_binToOtherBase(ndict['fpart'],8,part='float')
        else:
            ipart=_binToOtherBase(ndict['ipart'],8,part='integer')
            fpart=_binToOtherBase(ndict['fpart'],8,part='float')
    elif ndict['base'] in [10,16,32,64]:
        if ndict['ipart']=='0':
            (fpart,b)=_toBinary(ndict['fpart'],ndict['base'],part='float',prec=prec)
            fpart=_binToOtherBase(fpart,8,part='float')
        elif ndict['fpart']=='0':
            (ipart,b)=_toBinary(ndict['ipart'],ndict['base'],part='integer',prec=prec)
            ipart=_binToOtherBase(ipart,8,part='integer')
        else:
            (ipart,b1)=_toBinary(ndict['ipart'],ndict['base'],part='integer',prec=prec)
            ipart=_binToOtherBase(ipart,8,part='integer')
            (fpart,b2)=_toBinary(ndict['fpart'],ndict['base'],part='float',prec=prec)
            fpart=_binToOtherBase(fpart,8,part='float')
    if ipart=='':ipart='0'
    if fpart=='':fpart='0'
    return {'input_mode':'fp','base':8,'sign':ndict['sign'],'ipart':ipart,'fpart':fpart,'exp':0}

# _getHexadecimalForm(parseddict) converts the number dictionary into base16 version
def _getHexadecimalForm(parseddict={},prec=36):
    if parseddict['base']==16:return parseddict
    if 'normalized' in parseddict.keys():
        ndict={'input_mode':'fp','base':parseddict['base'],'sign':parseddict['sign'],\
            'ipart':parseddict['normalized']['ipart'],'fpart':parseddict['normalized']['fpart'],'exp':0}
    else:ndict=_normalizeToFP(parseddict,prec)

    if ndict['ipart']=='0' and ndict['fpart']=='0':
        return {'input_mode':'fp','base':16,'sign':ndict['sign'],'ipart':'0','fpart':'0','exp':0}

    ipart,fpart='',''
    if ndict['base']==2:
        if ndict['ipart']=='0':
            fpart=_binToOtherBase(ndict['fpart'],16,part='float')
        else:
            ipart=_binToOtherBase(ndict['ipart'],16,part='integer')
            fpart=_binToOtherBase(ndict['fpart'],16,part='float')
    elif ndict['base'] in [10,8,32,64]:
        if ndict['ipart']=='0':
            (fpart,b)=_toBinary(ndict['fpart'],ndict['base'],part='float',prec=prec)
            fpart=_binToOtherBase(fpart,16,part='float')
        elif ndict['fpart']=='0':
            (ipart,b)=_toBinary(ndict['ipart'],ndict['base'],part='integer',prec=prec)
            ipart=_binToOtherBase(ipart,16,part='integer')
        else:
            (ipart,b1)=_toBinary(ndict['ipart'],ndict['base'],part='integer',prec=prec)
            ipart=_binToOtherBase(ipart,16,part='integer')
            (fpart,b2)=_toBinary(ndict['fpart'],ndict['base'],part='float',prec=prec)
            fpart=_binToOtherBase(fpart,16,part='float')
    if ipart=='':ipart='0'
    if fpart=='':fpart='0'
    return {'input_mode':'fp','base':16,'sign':ndict['sign'],'ipart':ipart,'fpart':fpart,'exp':0}


# _getBase32Form(parseddict) converts the number dictionary into base8 version
def _getBase32Form(parseddict={},prec=36):
    if parseddict['base']==32:return parseddict
    if 'normalized' in parseddict.keys():
        ndict={'input_mode':'fp','base':parseddict['base'],'sign':parseddict['sign'],\
            'ipart':parseddict['normalized']['ipart'],'fpart':parseddict['normalized']['fpart'],'exp':0}
    else:ndict=_normalizeToFP(parseddict,prec)

    if ndict['ipart']=='0' and ndict['fpart']=='0':
        return {'input_mode':'fp','base':32,'sign':ndict['sign'],'ipart':'0','fpart':'0','exp':0}

    ipart,fpart='',''
    if ndict['base']==2:
        if ndict['ipart']=='0':
            fpart=_binToOtherBase(ndict['fpart'],32,part='float')
        else:
            ipart=_binToOtherBase(ndict['ipart'],32,part='integer')
            fpart=_binToOtherBase(ndict['fpart'],32,part='float')
    elif ndict['base'] in [10,8,16,64]:
        if ndict['ipart']=='0':
            (fpart,b)=_toBinary(ndict['fpart'],ndict['base'],part='float',prec=prec)
            fpart=_binToOtherBase(fpart,32,part='float')
        elif ndict['fpart']=='0':
            (ipart,b)=_toBinary(ndict['ipart'],ndict['base'],part='integer',prec=prec)
            ipart=_binToOtherBase(ipart,32,part='integer')
        else:
            (ipart,b1)=_toBinary(ndict['ipart'],ndict['base'],part='integer',prec=prec)
            ipart=_binToOtherBase(ipart,32,part='integer')
            (fpart,b2)=_toBinary(ndict['fpart'],ndict['base'],part='float',prec=prec)
            fpart=_binToOtherBase(fpart,32,part='float')
    if ipart=='':ipart='0'
    if fpart=='':fpart='0'
    return {'input_mode':'fp','base':32,'sign':ndict['sign'],'ipart':ipart,'fpart':fpart,'exp':0}


# _getBase64Form(parseddict) converts the number dictionary into base8 version
def _getBase64Form(parseddict={},prec=36):
    if parseddict['base']==64:return parseddict
    if 'normalized' in parseddict.keys():
        ndict={'input_mode':'fp','base':parseddict['base'],'sign':parseddict['sign'],\
            'ipart':parseddict['normalized']['ipart'],'fpart':parseddict['normalized']['fpart'],'exp':0}
    else:ndict=_normalizeToFP(parseddict,prec)

    if ndict['ipart']=='0' and ndict['fpart']=='0':
        return {'input_mode':'fp','base':64,'sign':ndict['sign'],'ipart':'0','fpart':'0','exp':0}

    ipart,fpart='',''
    if ndict['base']==2:
        if ndict['ipart']=='0':
            fpart=_binToOtherBase(ndict['fpart'],64,part='float')
        else:
            ipart=_binToOtherBase(ndict['ipart'],64,part='integer')
            fpart=_binToOtherBase(ndict['fpart'],64,part='float')
    elif ndict['base'] in [10,8,16,32]:
        if ndict['ipart']=='0':
            (fpart,b)=_toBinary(ndict['fpart'],ndict['base'],part='float',prec=prec)
            fpart=_binToOtherBase(fpart,64,part='float')
        elif ndict['fpart']=='0':
            (ipart,b)=_toBinary(ndict['ipart'],ndict['base'],part='integer',prec=prec)
            ipart=_binToOtherBase(ipart,64,part='integer')
        else:
            (ipart,b1)=_toBinary(ndict['ipart'],ndict['base'],part='integer',prec=prec)
            ipart=_binToOtherBase(ipart,64,part='integer')
            (fpart,b2)=_toBinary(ndict['fpart'],ndict['base'],part='float',prec=prec)
            fpart=_binToOtherBase(fpart,64,part='float')
    if ipart=='':ipart='0'
    if fpart=='':fpart='0'
    return {'input_mode':'fp','base':64,'sign':ndict['sign'],'ipart':ipart,'fpart':fpart,'exp':0}


# _getScientificForm(parseddict) returns scientific form of data (-7.124587p-23)
def _getScientificForm(parseddict={},prec=36):
    if 'normalized' in parseddict.keys():
        ndict={'input_mode':'fp','base':parseddict['base'],'sign':parseddict['sign'],\
            'ipart':parseddict['normalized']['ipart'],'fpart':parseddict['normalized']['fpart'],'exp':0}
    else:ndict=_normalizeToFP(parseddict,prec)

    if ndict['ipart']=='0' and ndict['fpart']=='0':
        return {'input_mode':'fp','base':ndict['base'],'sign':ndict['sign'],'ipart':'0','fpart':'0','exp':0}

    if ndict['ipart']=='0' and ndict['fpart']=='0':return ndict
    elif ndict['ipart']=='0' and ndict['fpart']!='0':
        if len(ndict['fpart'])==1:
            ndict['ipart']=ndict['fpart'];ndict['fpart']='0';ndict['exp']=-1
        else:
            i=0
            while ndict['fpart'][i]=='0':i=i+1
            ndict['ipart']=ndict['fpart'][i];
            ndict['fpart']=ndict['fpart'][i+1:]
            if len(ndict['fpart'])>prec:
                ndict['fpart']=ndict['fpart'][:prec]
            ndict['exp']=ndict['exp']-i-1
    elif ndict['ipart']!='0' and ndict['fpart']=='0':
        l=len(ndict['ipart'])
        if l==1: ndict['fpart']='0'
        else:ndict['fpart']=ndict['ipart'][1:];
        if len(ndict['fpart'])>prec:
            ndict['fpart']=ndict['fpart'][:prec]
        ndict['ipart']=ndict['ipart'][0];
        ndict['exp']=ndict['exp']+l-1
    else:
        l=len(ndict['ipart'])
        ndict['fpart']=ndict['fpart'].rstrip('0')
        ndict['fpart']=ndict['ipart'][1:]+ndict['fpart'];
        if len(ndict['fpart'])>prec:
            ndict['fpart']=ndict['fpart'][:prec]
        ndict['ipart']=ndict['ipart'][0]
        ndict['exp']=ndict['exp']+l-1
    if ndict['ipart']!='0':ndict['ipart']=ndict['ipart'].lstrip('0')
    if ndict['fpart']!='0':ndict['fpart']=ndict['fpart'].rstrip('0')
    return ndict

# _stringify(ndict) converts number dictionary into a string
def _stringify(ndict={}):
    if ndict==None:return None

    if ndict['base'] in [2,8]:base='b0'+str(ndict['base'])
    else:base='b'+str(ndict['base'])

    if 'sign' in ndict.keys():
        if ndict['sign'] in ['','+']:sign=''
        else: sign='-'
    else:sign=''

    if ndict['ipart']=='<INF>':
        return base+':<'+sign+'INF>'
    if ndict['ipart']=='<UNDEFINED>':
        return base+':<UNDEFINED>'

    if ndict['exp']==0:exp=''
    elif ndict['exp']>0:
        if ndict['base']==10:exp='e+'+str(ndict['exp'])
        else:exp='p+'+str(ndict['exp'])
    else:
        if ndict['base']==10:exp='e'+str(ndict['exp'])
        else:exp='p'+str(ndict['exp'])

    if ndict['input_mode']=='fr':
        if ndict['deno']=='0':
            return base+':'+sign+'INF'
        elif ndict['ipart']=='0' and ndict['numerator']=='0':
            return base+':'+sign+'0'
        elif ndict['ipart']=='0' and ndict['numerator']!='0' and ndict['deno']!='0':
            return base+':'+sign+ndict['numerator']+'/'+ndict['deno']+exp
        elif ndict['ipart']=='0' and ndict['numerator']!='0' and ndict['deno']!='0':
            return base+':'+sign+ndict['numerator']+'/'+ndict['deno']+exp
        else:
            return base+':'+sign+ndict['ipart']+' '+ndict['numerator']+'/'+ndict['deno']+exp
    elif ndict['input_mode']=='fp':
        if ndict['ipart']=='0' and ndict['fpart']=='0':
            return base+':'+sign+'0'
        elif ndict['ipart']=='0' and ndict['fpart']!='0':
            return base+':'+sign+'0.'+ndict['fpart']+exp
        elif ndict['ipart']!='0' and ndict['fpart']=='0':
            return base+':'+sign+ndict['ipart']+exp
        else:
            return base+':'+sign+ndict['ipart']+'.'+ndict['fpart']+exp


# _displayNumber(parseddict,prec,scientific) displays
# a UPN (universal precision number) upto the given precision either
# in floating point format or in scientific format
def _displayNumber(parseddict={},prec=36,scientific=False):
    if dataType(prec)!='int' or prec<1: prec=36

    ndict={}
    if 'normalized' in parseddict.keys():
        ndict={'input_mode':'fp','base':parseddict['base'],'sign':parseddict['sign'],\
            'ipart':parseddict['normalized']['ipart'],'fpart':parseddict['normalized']['fpart'],'exp':0}
    elif parseddict['input_mode']=='fp':
        ndict={'input_mode':'fp','base':parseddict['base'],'sign':parseddict['sign'],\
            'ipart':parseddict['ipart'],'fpart':parseddict['fpart'],'exp':parseddict['exp']}
    elif parseddict['input_mode']=='fr':
        return _stringify(parseddict)
    elif parseddict['input_mode']==None:
        ndict=parseddict.copy()
    else:raise Exception("Unknown Exception")

    if ndict['base'] in [2,8]:base='b0'+str(ndict['base'])
    else:base='b'+str(ndict['base'])

    if 'sign' in ndict.keys():
        if ndict['sign'] in ['','+']:sign=''
        else: sign='-'
    else:sign=''

    if ndict['ipart']=='<INF>':
        return base+':<'+sign+'INF>'
    if ndict['ipart']=='<UNDEFINED>':
        return base+':<UNDEFINED>'

    if ndict['ipart']=='0' and ndict['fpart']=='0':
        return base+':'+0

    if scientific==False:
        if ndict['fpart']=='0' and ndict['base']==10:
            s=ndict['ipart'];l=len(s)
            if l>prec:
                if int(s[prec])<5:
                    s=s[0:prec]+'0'*(l-prec)
                else:
                    s=str(int(s[0:prec])+1)+'0'*(l-prec)
            return base+':'+sign+s

        elif ndict['fpart']=='0' and ndict['base'] in [2,8,16,32,64]:
            s=ndict['ipart'];l=len(s)
            if l>prec:
                s=s[0:prec]+'0'*(l-prec)
            return base+':'+sign+s
        elif ndict['fpart']!='0' and ndict['base']==10:
            s1=ndict['ipart'];
            if s1=='0':li=0;
            else:li=len(s1)
            s2=ndict['fpart'];
            if s2=='0':lf=0
            else:lf=len(s2)
    
            if li>prec:
                if int(s1[prec])<5:
                    s1=s1[0:prec]+'0'*(li-prec)
                else:
                    s1=str(int(s1[0:prec])+1)+'0'*(li-prec)
                s2=''
            elif li==prec:
                if int(s2[0])>=5:s1=str(int(s1)+1)
                s2=''
            elif prec>li and lf>prec-li:
                if int(s2[prec-li])<5:s2=s2[0:prec-li]
                else:
                    tmp=str(int(s2[0:prec-li])+1);
                    if len(tmp)>(prec-li):s2=tmp[1:];s1=str(int(s1)+1);
                    elif len(tmp)==(prec-li):s2=tmp.rstrip('0')
                    else:s2=tmp.rstrip('0')
            if s2=='':s=s1
            else:s=s1+'.'+s2
            return base+':'+sign+s

        elif ndict['fpart']!='0' and ndict['base'] in [2,8,16,32,64]:
            s1=ndict['ipart'];
            if s1=='0':li=0;
            else:li=len(s1)
            s2=ndict['fpart'];
            if s2=='0':lf=0
            else:lf=len(s2)
    
            if li>prec:
                s1=s1[0:prec]+'0'*(li-prec);
                s2=''
            elif li==prec:
                s2=''
            if prec>li and lf>prec-li:
                s2=s2[0:prec-li]
            if s2=='':s=s1
            else:s=s1+'.'+s2
            return base+':'+sign+s

    elif scientific==True:
        return _stringify(_getScientificForm(parseddict,prec))


# _createNewNumber(parseddict,prec,is_accurate) changes the given 
# precision to the UPN and creates a new UPN
def _createNewNumber(parseddict={},prec=36,is_accurate=True):
    if dataType(prec)!='int' or prec<1: prec=36

    ndict={}
    if 'normalized' in parseddict.keys():
        ndict={'input_mode':'fp','base':parseddict['base'],'sign':parseddict['sign'],\
            'ipart':parseddict['normalized']['ipart'],'fpart':parseddict['normalized']['fpart'],'exp':0}
    elif parseddict['input_mode']=='fp':
        ndict={'input_mode':'fp','base':parseddict['base'],'sign':parseddict['sign'],\
            'ipart':parseddict['ipart'],'fpart':parseddict['fpart'],'exp':parseddict['exp']}
    elif parseddict['input_mode']=='fr':
        return self.copy()
    elif parseddict['input_mode']==None:
        ndict=parseddict.copy()
    else:raise Exception("Unknown Exception")

    if 'sign' in ndict.keys():
        if ndict['sign'] in ['','+']:sign=''
        else: sign='-'
    else:sign=''

    if ndict['ipart']=='<INF>':
        return Number('<'+sign+'INF>',base=ndict['base'],prec=prec,is_accurate=True)
    if ndict['ipart']=='<UNDEFINED>':
        return Number('<undefined>',base=ndict['base'],prec=prec,is_accurate=True)

    if ndict['ipart']=='0' and ndict['fpart']=='0':
        return Number('0',base=ndict['base'],prec=prec,is_accurate=True)

    if ndict['fpart']=='0' and ndict['base']==10:
        s=ndict['ipart'];l=len(s)
        if l>prec:
            if int(s[prec])<5:
                s=s[0:prec]+'0'*(l-prec)
            else:
                s=str(int(s[0:prec])+1)+'0'*(l-prec)
            is_accurate=is_accurate & False
        else: is_accurate=is_accurate & True
        return Number(sign+s,base=ndict['base'],prec=prec,is_accurate=is_accurate)
    elif ndict['fpart']=='0' and ndict['base'] in [2,8,16,32,64]:
        s=ndict['ipart'];l=len(s)
        if l>prec:
            s=s[0:prec]+'0'*(l-prec);is_accurate=is_accurate & False
        else:is_accurate=is_accurate & True
        return Number(sign+s,base=ndict['base'],prec=prec,is_accurate=is_accurate)
    elif ndict['fpart']!='0' and ndict['base']==10:
        s1=ndict['ipart'];
        if s1=='0':li=0;
        else:li=len(s1)
        s2=ndict['fpart'];
        if s2=='0':lf=0
        else:lf=len(s2)

        next_of_last=None
        if prec<li:
            if int(s1[prec])<5:
                s1=s1[0:prec]+'0'*(li-prec)
            else:
                s1=str(int(s1[0:prec])+1)+'0'*(li-prec)
            is_accurate=is_accurate & False
            s2=''
        elif prec==li:
            if int(s2[0])>=5:s1=str(int(s1)+1)
            is_accurate=is_accurate & False 
            s2=''
        elif prec>li and lf<prec-li:is_accurate=is_accurate & True
        elif li==0 and lf!=0:
            for i in range(lf):
                if s2[i]!='0':
                    if lf-i<=prec:
                        s2='0'*i+s2[i:]
                        is_accurate=is_accurate & True
                    elif lf-i>prec:
                        next_of_last=s2[i+prec-li]
                        s2='0'*i+s2[i:i+prec]
                        is_accurate=is_accurate & False
                    break
        elif prec>li and lf>prec-li:
            next_of_last=s2[prec-li];
            s2=s2[0:prec-li]
        if next_of_last!=None and int(next_of_last)>=5:
            (s2,carry)=__add_1_to_fpart(s2)
            if carry==1:s1=str(int(s1)+1)
            s2=s2.rstrip('0')
        if s2=='':s=s1
        else:s=s1+'.'+s2
        return Number(sign+s,base=ndict['base'],prec=prec,is_accurate=is_accurate)

    elif ndict['fpart']!='0' and ndict['base'] in [2,8,16,32,64]:
        s1=ndict['ipart'];
        if s1=='0':li=0;
        else:li=len(s1)
        s2=ndict['fpart'];
        if s2=='0':lf=0
        else:lf=len(s2)
       
        if li>prec:
            s1=s1[0:prec]+'0'*(li-prec);
            is_accurate=is_accurate & False
            s2=''
        elif li==prec:
            if s2=='0':is_accurate=is_accurate & True
            else:is_accurate=is_accurate & False
            s2=''
        elif li<prec:
            is_accurate=is_accurate & True
        if prec>li and lf>prec-li:
            s2=s2[0:prec-li]
            is_accurate=is_accurate & False
        elif li+lf<prec:
            is_accurate=is_accurate & True
        if s2=='':s=s1
        else:s=s1+'.'+s2
        return Number(sign+s,base=ndict['base'],prec=prec,is_accurate=is_accurate)


def __add_1_to_fpart(fpart=''):
    l=len(fpart);carry=1;s=''
    for i in range(l-1,-1,-1):
        digit=str(int(fpart[i])+carry)
        if digit=='10':s='0'+s;carry=1
        else:s=digit+s;carry=0
    return (s,carry)




########################################################################
# denary number functions and arithmetic

# _isPrime(num) returns true if the denary integer is a 
# prime number
def _isPrime(num=None):
    if num==1:return False
    elif num in [2,3,5,7,11.13,17,19,23,29,31,37]: return True
    elif num in [41,43,47,53,59,61,67,71,73,79,83,89,97]: return True
    elif str(num)[-1:] in ['0','2','4','5','6','8']:return False
    elif str(num)[-1:] in ['1','3','7','9']:
        if num%3==0:return False
        elif num%7==0:return False
        r=1+int(num**0.5);i=11
        for i in range(11,r,2):
            if num%i==0:return False
    return True

# primeFactors(num) returns all the denary prime factors of the
# given denary integer in a list format [[2,1],[3,2],[17,1]]
def _primeFactors(num=None):
    p={}
    if num<0: raise ValueError("Invalid number to factorize.") 
    if num==2:return [[2,1]]
    # reducing the integer as far as possible
    # divisible by 10
    i=0
    while str(num)[-1:]=='0':		# str(num)[-1:]=last digit
        num=int(num//10)
        i+=1
    if i>0:
        p[2]=i
        p[5]=i
    if num==1:
        # converting dictionary into a 2D list
        l=[];i=0
        for f in p.keys():
            l.append([f,p[f]])
        return l

    # divisible by 5
    i=0
    while str(num)[-1:]=='5':
        num=int(num//5)
        i+=1
    if i>0:
        if 5 in p.keys():p[5]+=i
        else:p[5]=i
    if num==1:
        # converting dictionary into a 2D list
        l=[];i=0
        for f in p.keys():
            l.append([f,p[f]])
        return l

    # divisible by 2
    i=0
    while str(num)[-1:] in ['2','4','6','8']:
        num=int(num//2)
        i+=1
    if i>0:
        if 2 in p.keys():p[2]+=i
        else:p[2]=i
    if num==1:
        # converting dictionary into a 2D list
        l=[];i=0
        for f in p.keys():
            l.append([f,p[f]])
        return l

    # divisible by 3
    i=0 
    if num%3==0:
        while num%3==0:
            num=int(num//3)
            i+=1
        p[3]=i
    if num==1:
        # converting dictionary into a 2D list
        l=[];i=0
        for f in p.keys():
            l.append([f,p[f]])
        return l

    # divisible by 7
    i=0 
    if num%7==0:
        while num%7==0:
            num=int(num//7)
            i+=1
        p[7]=i
    if num==1:
        # converting dictionary into a 2D list
        l=[];i=0
        for f in p.keys():
            l.append([f,p[f]])
        return l
    n=11
    while n<num+1:	# for n in range(11,num+1,2):
        if str(num)[-1:]=='5':continue
        icount=0
        isfactor=0
        while num%n==0:
            num=int(num//n)
            icount+=1
            isfactor=1            
        if isfactor==1:p[n]=icount
        n=n+2
    # converting dictionary into a 2D list
    l=[];i=0
    for f in p.keys():
        l.append([f,p[f]])
    return l

# sratio(num1,num2) returns the simplest proper ratio of two denary unsigned integers 
# called numerator and denominator in the form [numerator,denominator]
def _sratio(num1=None,num2=None):
    if num2==0:raise ValueError("Invalid denominator")
    if num1==0:return [0,num2] 
    if num1%num2==0:return [int(num1/num2),1]
    while str(num1)[-1:] in ['0','2','4','6','8'] and str(num2)[-1:] in ['0','2','4','6','8']:
        num1=num1//2; num2=num2//2;

    for n in [3,5,7,11,13,17,19,23,29,31,37]:
        while num1>=n and num2>=n and num1%n==0 and num2%n==0:
            num1=num1//n; num2=num2//n
 
    for n in [41,43,47,53,59,61,67,71,73,79,83,89,97]:
        while num1>=n and num2>=n and num1%n==0 and num2%n==0:
            num1=num1//n; num2=num2//n

    return [num1,num2]		


# sratio(num1,num2) returns the simplest proper ratio of two denary unsigned integers 
# called numerator and denominator in the form [numerator,denominator]
def _sratio2(num1=None,num2=None): 
    if num2==0:raise ValueError("Invalid denominator")
    if num1==0:return [0,num2]
    if num1%num2==0:return [int(num1/num2),1]
    while str(num1)[-1:] in ['0','2','4','6','8'] and str(num2)[-1:] in ['0','2','4','6','8']:
        num1=num1//2; num2=num2//2;

    for n in [3,5,7,11,13,17,19,23,29,31,37]:
        while num1>=n and num2>=n and num1%n==0 and num2%n==0:
            num1=num1//n; num2=num2//n

    for n in [41,43,47,53,59,61,67,71,73,79,83,89,97]:
        while num1>=n and num2>=n and num1%n==0 and num2%n==0:
            num1=num1//n; num2=num2//n

    # Make further simplification
    nfactors=_primeFactors(num1)		# nfactors=factors of numerator
    dfactors=_primeFactors(num2)		# dfactors=factors of denominator
    prodnume,proddeno=1,1
    while 0<len(nfactors):
        cff=False                               # cff=common factor found, boolean
        j=0				
        while j<len(dfactors):	    
            if nfactors[0][0]==dfactors[j][0]:
                cff=True
                if nfactors[0][1]>=dfactors[j][1]:
                    prodnume*=nfactors[0][0]**(nfactors[0][1]-dfactors[j][1])
                else:
                    proddeno*=dfactors[j][0]**(dfactors[j][1]-nfactors[0][1])
                del(dfactors[j])	# deleting the common factor of the denominator		
            j+=1	    
        if not cff:prodnume*=nfactors[0][0]**nfactors[0][1]
        del(nfactors[0])		# deleting the common factor of the numerator	
    for k in range(len(dfactors)):
        proddeno*=dfactors[k][0]**dfactors[k][1]
    return [prodnume,proddeno]

# _fact() and _fact2() return the factorial of a denary integer
# _fact() is more efficient
def _fact(num=None):
    if num==0 or num==1:return 1
    p=1
    for i in range(2,num+1):p=p*i
    return p

def _fact2(num=None):
    if num==0 or num==1:return 1
    else: return num*_fact(num-1)

# _normalizeDenary(num=None) parses a denary number
# into a touple (sign,ipart,fpart)
def _normalizeDenary(num=None):
    numstr=str(num)
    ipart,fpart,exp,s='','',0,''
    if numstr[0]=='-':sign='-';s=numstr[1:]
    elif numstr[0]=='+':sign='+';s=numstr[1:]
    elif numstr[0]not in ['+','-']:sign='+';s=numstr
    if 'e' in s:
        exp=int(s.split('e')[1])
        s=s.split('e')[0]
    if '.' in s:
        ipart=s.split('.')[0]
        fpart=s.split('.')[1]
    else:
        ipart=s
        fpart=''

    if exp==0:
        if ipart=='':ipart='0'
        return {'sign':sign,'ipart':ipart,'fpart':fpart}
    elif exp>0:
        if fpart=='':l=0
        else:l=len(fpart)
        if exp<l:ipart=ipart+fpart[0:exp];fpart=fpart[exp:]
        elif exp==l:ipart=ipart+fpart;fpart=''
        elif exp>l:ipart=ipart+fpart+'0'*(exp-l);fpart=''
    elif exp<0:
        if ipart=='':l=0
        else:l=len(ipart)
        exp=-1*exp
        if exp<l:fpart=ipart[l-exp:]+fpart;ipart=ipart[0:l-exp]
        elif exp==l:fpart=ipart+fpart;ipart=''
        else:fpart='0'*(exp-l)+ipart+fpart; ipart=''
    if ipart=='':ipart='0'
    if fpart=='':fpart='0'
    return {'sign':sign,'ipart':ipart,'fpart':fpart}



########################################################################
# Functions to support mathematical operations

# assuming den1 and den2, both are positive
# don't change '' to '0'
def _unsignedDenaryAdd(den1={},den2={}):
    ipart1,ipart2=den1['ipart'].lstrip('0'),den2['ipart'].lstrip('0')
    fpart1,fpart2=den1['fpart'].rstrip('0'),den2['fpart'].rstrip('0')

    if ipart1=='':li1=0
    else:li1=len(ipart1);
    if fpart1=='':lf1=0
    else:lf1=len(fpart1);
    if ipart2=='':li2=0
    else:li2=len(ipart2);
    if fpart2=='':lf2=0
    else:lf2=len(fpart2);
    #lf1=len(fpart1);li2=len(ipart2);lf2=len(fpart2)

    if li1==0 and lf1==0:return {'ipart':ipart2,'fpart':fpart2,'is_accurate':True}
    elif li2==0 and lf2==0:return {'ipart':ipart1,'fpart':fpart1,'is_accurate':True}
    elif lf1==0 and lf2==0:return {'ipart':str(int(ipart1)+int(ipart2)),'fpart':'0','is_accurate':True}

    if li1>li2:ipart2='0'*(li1-li2)+ipart2;l=li1;
    elif li2>li1:ipart1='0'*(li2-li1)+ipart1;l=li2;
    else:l=li1;

    if lf1==0:fpart1='0'*lf2;l=l+lf2;dp=lf2
    elif lf2==0:fpart2='0'*lf1;l=l+lf1;dp=lf1
    else:
        if lf1>lf2:fpart2=fpart2+'0'*(lf1-lf2);l=l+lf1;dp=lf1
        elif lf1<lf2:fpart1=fpart1+'0'*(lf2-lf1);l=l+lf2;dp=lf2
        else:l=l+lf1;dp=lf1

    # check whether int_max_str_digits exceeds
    strdigits=max(len(ipart1+fpart1),len(ipart2+fpart2))
    if sys.get_int_max_str_digits()<=strdigits:sys.set_int_max_str_digits(2*strdigits)

    num1=ipart1+fpart1
    num2=ipart2+fpart2

    s='';carry=0	# dsum=digit sum
    for i in range(l):
        dsum=0 
        dsum=int(num1[l-i-1])+int(num2[l-i-1])+carry;
        if dsum>=10:carry=1;s=(str(dsum))[-1]+s;
        elif dsum==10:carry=1;s='0'+s;
        else: carry=0;s=str(dsum)+s;
    if carry==1:
        s='1'+s
        ipart=s[0:l+1-dp].lstrip('0');fpart=s[l+1-dp:l+1].rstrip('0')
    else:
        ipart=s[0:l-dp].lstrip('0');fpart=s[l-dp:l].rstrip('0')
    if ipart=='':ipart='0'
    if fpart=='':fpart='0' 
    return {'ipart':ipart,'fpart':fpart,'is_accurate':True}


# assuming den1 and den2, both are positive
# den={'ipart':ipart,'numerator':numerator,'deno':deno}
# it supports addition between two fractions or between fraction and integer 
# or between two integers
# integer to be input: {'ipart':intvalue,'numerator':'0','deno':'1'}
def _unsignedDenaryFRAdd(den1={},den2={}):
    if den1['ipart']=='0':ipart1=0
    else:ipart1=int(den1['ipart'])
    if den2['ipart']=='0':ipart2=0
    else:ipart2=int(den2['ipart'])

    if den1['numerator']=='0':den1['numerator']=0;den1['deno']=1
    else:den1['numerator']=int(den1['numerator']);den1['deno']=int(den1['deno'])
    if den2['numerator']=='0':den2['numerator']=0;den2['deno']=1
    else:den2['numerator']=int(den2['numerator']);den2['deno']=int(den2['deno'])

    ipart=ipart1+ipart2
    d=den2['deno']*den1['deno']
    n=ipart*d+den1['numerator']*den2['deno']+den2['numerator']*den1['deno']

    [n,d]=_sratio(n,d)	# simplifying the fraction
    if d==1:return {'sign':'+','ipart':str(n),'numerator':'0','deno':'1','is_accurate':True}
    ipart=n//d;n=n%d 
    return {'ipart':str(ipart),'numerator':str(n),'deno':str(d),'is_accurate':True}



# assuming den1 and den2, both are positive
# den={'ipart':ipart,'numerator':numerator,'deno':deno}
# it supports subtraction between two fractions or between fraction and integer 
# or between two integers
def _unsignedDenaryFRAdd2(den1={},den2={}):
    if den1['ipart']=='0':ipart1=0
    else:ipart1=int(den1['ipart'])
    if den2['ipart']=='0':ipart2=0
    else:ipart2=int(den2['ipart'])

    if den1['numerator']=='0':den1['numerator']=0;den1['deno']=1
    else:den1['numerator']=int(den1['numerator']);den1['deno']=int(den1['deno'])
    if den2['numerator']=='0':den2['numerator']=0;den2['deno']=1
    else:den2['numerator']=int(den2['numerator']);den2['deno']=int(den2['deno'])

    ipart=ipart1+ipart2
    d=den2['deno']*den1['deno']
    n=ipart*d+den1['numerator']*den2['deno']+den2['numerator']*den1['deno']

    [n,d]=_sratio2(n,d)	# simplifying the fraction
    if d==1:return {'sign':'+','ipart':str(n),'numerator':'0','deno':'1','is_accurate':True}
    ipart=n//d;n=n%d 
    return {'ipart':str(ipart),'numerator':str(n),'deno':str(d),'is_accurate':True}



# assuming den1 and den2, both are positive
# don't change '' to '0'
def _unsignedDenarySubtract(den1={},den2={}):
    ipart1,ipart2=den1['ipart'].lstrip('0'),den2['ipart'].lstrip('0')
    fpart1,fpart2=den1['fpart'].rstrip('0'),den2['fpart'].rstrip('0')

    # li=length of ipart, lf=length of fpart, dp=dot position
    if ipart1=='':li1=0
    else: li1=len(ipart1)

    if fpart1=='':lf1=0
    else: lf1=len(fpart1)

    if ipart2=='':li2=0
    else: li2=len(ipart2)

    if fpart2=='':lf2=0
    else: lf2=len(fpart2)

    sign='+'
    if li1>li2:dp=li1;ipart2='0'*(li1-li2)+ipart2;l=li1;
    elif li2>li1:dp=li2;ipart1='0'*(li2-li1)+ipart1;l=li2;
    else:l=li1;

    # check whether int_max_str_digits exceeds
    strdigits=max(len(ipart1+fpart1),len(ipart2+fpart2))
    if sys.get_int_max_str_digits()<=strdigits:sys.set_int_max_str_digits(2*strdigits)

    if lf1>lf2:fpart2=fpart2+'0'*(lf1-lf2);l=l+lf1;dp=lf1
    elif lf1<lf2:fpart1=fpart1+'0'*(lf2-lf1);l=l+lf2;dp=lf2
    else:l=l+lf1;dp=lf1

    num1=ipart1+fpart1; n1=int(num1)
    num2=ipart2+fpart2; n2=int(num2)

    if n1==n2:return {'sign':'+','ipart':'','fpart':''}
    elif lf1==0 and lf2==0 and n1>n2:return {'sign':'+','ipart':str(n1-n2),'fpart':'0','is_accurate':True}
    elif lf1==0 and lf2==0 and n1<n2:return {'sign':'-','ipart':str(n2-n1),'fpart':'0','is_accurate':True}
    elif n1<n2:num1,num2=num2,num1;sign='-'

    s='';carry=0
    for i in range(l): 
        a,b=int(num1[l-i-1]),int(num2[l-i-1]) 
        if a>b:diff=a-b-carry;carry=0
        elif b>a:diff=10+a-b-carry;carry=1
        else: 
            if carry==0:diff=0
            else:diff=9;
        s=str(diff)+s;
    ipart=s[0:l-dp].lstrip('0');fpart=s[l-dp:l].rstrip('0')
    return {'sign':sign,'ipart':ipart,'fpart':fpart,'is_accurate':True}


# assuming den1 and den2, both are positive
# den={'ipart':ipart,'numerator':numerator,'deno':deno}
# it supports subtraction between two fractions or between fraction and integer 
# or between two integers
def _unsignedDenaryFRSubtract(den1={},den2={}):
    if den1['ipart']=='0':ipart1=0
    else:ipart1=int(den1['ipart'])
    if den2['ipart']=='0':ipart2=0
    else:ipart2=int(den2['ipart'])

    if den1['numerator']=='0':den1['numerator']=0;den1['deno']=1
    else:den1['numerator']=int(den1['numerator']);den1['deno']=int(den1['deno'])
    if den2['numerator']=='0':den2['numerator']=0;den2['deno']=1
    else:den2['numerator']=int(den2['numerator']);den2['deno']=int(den2['deno'])

    ipart=ipart1-ipart2
    d=den2['deno']*den1['deno']
    n=ipart*d+den1['numerator']*den2['deno']-den2['numerator']*den1['deno']
    if n>0:	# 1st fraction is greater
        [n,d]=_sratio(n,d)	# simplifying the fraction
        if d==1:return {'sign':'+','ipart':str(n),'numerator':'0','deno':'1','is_accurate':True}
        ipart=n//d;n=n%d 
        return {'sign':'+','ipart':str(ipart),'numerator':str(n),'deno':str(d),'is_accurate':True}
    elif n==0:return {'sign':'+','ipart':'0','numerator':'0','deno':str(d),'is_accurate':True}
    elif n<0:
        n=-1*n; [n,d]=_sratio(n,d)	# simplifying the fraction
        if d==1:return {'sign':'-','ipart':str(n),'numerator':'0','deno':'1','is_accurate':True}
        ipart=n//d;n=n%d 
        return {'sign':'-','ipart':str(ipart),'numerator':str(n),'deno':str(d),'is_accurate':True}



# assuming den1 and den2, both are positive
# den={'ipart':ipart,'numerator':numerator,'deno':deno}
# it supports subtraction between two fractions or between fraction and integer 
# or between two integers
def _unsignedDenaryFRSubtract2(den1={},den2={}):
    if den1['ipart']=='0':ipart1=0
    else:ipart1=int(den1['ipart'])
    if den2['ipart']=='0':ipart2=0
    else:ipart2=int(den2['ipart'])

    if den1['numerator']=='0':den1['numerator']=0;den1['deno']=1
    else:den1['numerator']=int(den1['numerator']);den1['deno']=int(den1['deno'])
    if den2['numerator']=='0':den2['numerator']=0;den2['deno']=1
    else:den2['numerator']=int(den2['numerator']);den2['deno']=int(den2['deno'])

    ipart=ipart1-ipart2
    d=den2['deno']*den1['deno']
    n=ipart*d+den1['numerator']*den2['deno']-den2['numerator']*den1['deno']
    if n>0:	# 1st fraction is greater
        [n,d]=_sratio2(n,d)	# simplifying the fraction
        if d==1:return {'sign':'+','ipart':str(n),'numerator':'0','deno':'1','is_accurate':True}
        ipart=n//d;n=n%d 
        return {'sign':'+','ipart':str(ipart),'numerator':str(n),'deno':str(d),'is_accurate':True}
    elif n==0:return {'sign':'+','ipart':'0','numerator':'0','deno':str(d),'is_accurate':True}
    elif n<0:
        n=-1*n; [n,d]=_sratio2(n,d)	# simplifying the fraction
        if d==1:return {'sign':'-','ipart':str(n),'numerator':'0','deno':'1','is_accurate':True}
        ipart=n//d;n=n%d 
        return {'sign':'-','ipart':str(ipart),'numerator':str(n),'deno':str(d),'is_accurate':True}



# assuming den1 and den2, both are positive
def _unsignedDenaryMultiply(den1={},den2={}):
    ipart1,ipart2=den1['ipart'],den2['ipart']    # den1['ipart'].lstrip('0'),den2['ipart'].lstrip('0')
    fpart1,fpart2=den1['fpart'],den2['fpart']    # den1['fpart'].rstrip('0'),den2['fpart'].rstrip('0')

    if ipart1=='0':ipart1=''
    if ipart2=='0':ipart2=''

    # lf=length of fpart, dp=dot position
    if fpart1=='0':lf1=0;fpart1=''
    else: lf1=len(fpart1)

    if fpart2=='0':lf2=0;fpart2=''
    else: lf2=len(fpart2)

    dp=lf1+lf2
    num1=ipart1+fpart1;
    num2=ipart2+fpart2;
	
    # check whether int_max_str_digits exceeds
    strdigits=len(num1)+len(num2)
    if sys.get_int_max_str_digits()<=strdigits:sys.set_int_max_str_digits(2*strdigits)
	
    if num1=='':n1=0
    else: n1=int(num1)
    if num2=='':n2=0
    else: n2=int(num2)
    s=str(n1*n2);l=len(s)

    if s=='0':return {'ipart':'0','fpart':'0','is_accurate':True}
    if l>dp:ipart=s[0:l-dp];fpart=s[l-dp:l]
    elif l==dp:ipart='';fpart=s
    else:ipart='';fpart='0'*(dp-l)+s

    return {'ipart':ipart,'fpart':fpart,'is_accurate':True}


# assuming den1 and den2, both are positive
# den={'ipart':ipart,'numerator':numerator,'deno':deno}
def _unsignedDenaryFRMultiply(den1={},den2={}):
    if den1['ipart']=='0':ipart1=0
    else:ipart1=int(den1['ipart'])
    if den2['ipart']=='0':ipart2=0
    else:ipart2=int(den2['ipart'])

    n1,n2=int(den1['numerator']),int(den2['numerator'])
    d1,d2=int(den1['deno']),int(den2['deno'])

    n=(ipart1*d1+n1)*(ipart2*d2+n2)
    d=d1*d2
    [n,d]=_sratio(n,d)	# simplifying the fraction
    if d==1:return {'ipart':str(n),'numerator':'0','deno':'1','is_accurate':True}
    ipart=n//d;n=n%d 
    return {'ipart':str(ipart),'numerator':str(n),'deno':str(d),'is_accurate':True}

# assuming den1 and den2, both are positive
# den={'ipart':ipart,'numerator':numerator,'deno':deno}
def _unsignedDenaryFRMultiply2(den1={},den2={}):
    if den1['ipart']=='0':ipart1=0
    else:ipart1=int(den1['ipart'])
    if den2['ipart']=='0':ipart2=0
    else:ipart2=int(den2['ipart'])

    n1,n2=int(den1['numerator']),int(den2['numerator'])
    d1,d2=int(den1['deno']),int(den2['deno'])

    n=(ipart1*d1+n1)*(ipart2*d2+n2)
    d=d1*d2
    [n,d]=_sratio2(n,d)	# simplifying the fraction
    if d==1:return {'ipart':str(n),'numerator':'0','deno':'1','is_accurate':True}
    ipart=n//d;n=n%d 
    return {'ipart':str(ipart),'numerator':str(n),'deno':str(d),'is_accurate':True}
        

# assuming den1 and den2, both are positive
# division correct to 2*prec
def _unsignedDenaryDivision(den1={},den2={},prec=36):
    ipart1,ipart2=den1['ipart'].lstrip('0'),den2['ipart'].lstrip('0')
    fpart1,fpart2=den1['fpart'].rstrip('0'),den2['fpart'].rstrip('0')

    if ipart1=='' and fpart1=='':
            return {'ipart':'0','fpart':'0','is_accurate':True}

    if ipart2=='' and fpart2=='':
            return {'ipart':'<inf>','fpart':'0','is_accurate':True}

    # converting floating denary to integer
    # lf=length of fpart, dp=dot position
    if fpart1=='':lf1=0
    else:lf1=len(fpart1)

    if fpart2=='':lf2=0
    else:lf2=len(fpart2)

    # Redefining prec 
    prec2=prec+2

    if lf1==0 and lf2==0:
        num1=ipart1
        num2=ipart2
    elif lf1==0 and lf2>0:
        num1=ipart1+'0'*lf2
        num2=ipart2+fpart2
        #if prec<lf2:prec=lf2
    elif lf1!=0 and lf1<lf2:
        num1=ipart1+fpart1+'0'*(lf2-lf1)
        num2=ipart2+fpart2
        #if prec<lf2:prec=lf2
    elif lf2==0 and lf1>0:
        num1=ipart1+fpart1
        num2=ipart2+'0'*(lf1-lf2)
        #if prec<lf1:prec=lf1
    elif lf2!=0 and lf1>lf2:
        num1=ipart1+fpart1
        num2=ipart2+fpart2+'0'*(lf1-lf2)
        #if prec<lf1:prec=lf1
    elif lf1!=0 and lf1==lf2:
        num1=ipart1+fpart1
        num2=ipart2+fpart2
        #if prec<lf1:prec=lf1

    # check whether int_max_str_digits exceeds
    strdigits=max(len(num1),len(num2))
    if sys.get_int_max_str_digits()<=strdigits:sys.set_int_max_str_digits(3*strdigits)
	
    n1=int(num1); n2=int(num2)
    if n1==n2: return {'ipart':'1','fpart':'0','is_accurate':True}
    elif n1%n2==0: return {'ipart':str(n1//n2),'fpart':'0','is_accurate':True}
    is_accurate=False
    [n1,n2]=_sratio(n1,n2);
    if n2==1: ipart=str(n1);fpart=''
    else:
        ipart='';fpart='';i=0
        if n1>n2:ipart=str(n1//n2);n1=n1%n2    
        while(i<prec2):	## division correct to prec2
            n1=n1*10
            if n1<n2:fpart=fpart+'0'
            elif n1%n2==0:
                fpart=fpart+str(n1//n2)
                is_accurate=True
                break
            else:
                fpart=fpart+str(n1//n2)
                n1=n1%n2
            i+=1
    return {'ipart':ipart.lstrip('0'),'fpart':fpart.rstrip('0'),'is_accurate':is_accurate}


# assuming den1 and den2, both are positive
# den={'ipart':ipart,'numerator':numerator,'deno':deno}
# to pass integer, shape it to {'ipart':'ipart','numerator':'0','deno':'1'}
def _unsignedDenaryFRDivision(den1={},den2={}):
    if den1['ipart']=='0':ipart1=0
    else:ipart1=int(den1['ipart'])
    if den2['ipart']=='0':ipart2=0
    else:ipart2=int(den2['ipart'])

    if den1['numerator']=='0':n1=0;d1=1
    else:n1=int(den1['numerator']);d1=int(den1['deno'])
    if den2['numerator']=='':n2=0;d2=1
    else:n2=int(den2['numerator']);d2=int(den2['deno'])

    if ipart2==0 and n2==0: return {'ipart':'<inf>','fpart':'0','is_accurate':True}

    n=(ipart1*d1+n1)*d2
    d=d1*(ipart2*d2+n2)
    [n,d]=_sratio(n,d)	# simplifying the fraction
    if d==1:return {'ipart':str(n),'numerator':'0','deno':'1','is_accurate':True}
    ipart=n//d;n=n%d 
    return {'ipart':str(ipart),'numerator':str(n),'deno':str(d),'is_accurate':True}

# assuming den1 and den2, both are positive
# den={'ipart':ipart,'numerator':numerator,'deno':deno}
def _unsignedDenaryFRDivision2(den1={},den2={}):
    if den1['ipart']=='0':ipart1=0
    else:ipart1=int(den1['ipart'])
    if den2['ipart']=='0':ipart2=0
    else:ipart2=int(den2['ipart'])

    if den1['numerator']=='0':n1=0;d1=1
    else:n1=int(den1['numerator']);d1=int(den1['deno'])
    if den2['numerator']=='0':n2=0;d2=1
    else:n2=int(den2['numerator']);d2=int(den2['deno'])

    if ipart2==0 and n2==0: return {'ipart':'<inf>','fpart':'0','is_accurate':True}

    n=(ipart1*d1+n1)*d2
    d=d1*(ipart2*d2+n2)
    [n,d]=_sratio2(n,d)	# simplifying the fraction
    if d==1:return {'ipart':str(n),'numerator':'0','deno':'1','is_accurate':True}
    ipart=n//d;n=n%d 
    return {'ipart':str(ipart),'numerator':str(n),'deno':str(d),'is_accurate':True}



# assuming den1 and den2, both are positive
def _unsignedDenaryInverse(den={},prec=36):
    ipart,fpart=den['ipart'].lstrip('0'),den['fpart'].rstrip('0')

    if ipart=='' and fpart=='':
            return {'ipart':'<inf>','fpart':'0','is_accurate':True}

    #if ipart=='0' and fpart=='0':
    #        return {'ipart':'INF','fpart':'0','is_accurate':True}

    # lf=length of fpart, dp=dot position
    if fpart=='':lf=0
    else: lf=len(fpart)

    dp=lf
    num=ipart+fpart;n=int(num)
    
    if n==1: ipart='1';fpart=''
    else:
        n1=1;n2=n
        ipart='';fpart='';i=0
        if n1>n2:ipart=str(n1//n2);n1=n1%n2    
        while(i<prec):
            n1=n1*10
            if n1<n2:fpart=fpart+'0'
            elif n1%n2==0:
                fpart=fpart+str(n1//n2)
                break
            else:
                fpart=fpart+str(n1//n2)
                n1=n1%n2
            i+=1
    if dp==0: return {'ipart':ipart,'fpart':fpart,'is_accurate':True}
    ipart=ipart+fpart[0:dp];fpart=fpart[dp:]
    return {'ipart':ipart.lstrip('0'),'fpart':fpart.rstrip('0'),'is_accurate':True}

# assuming den1 and den2, both are positive
# den={'ipart':ipart,'numerator':numerator,'deno':deno}
# to pass integer, shape it to {'ipart':'ipart','numerator':'0','deno':'1'}
def _unsignedDenaryFRInverse(den={}):
    if den['ipart']=='0':ipart=0
    else:ipart=int(den['ipart'])
    if den['numerator']=='0':n=0;d=1	# n=numerator,d=denominator
    else:n=int(den['numerator']);d=int(den['deno'])
    if ipart==0 and n==0: return {'ipart':'<inf>','fpart':'0','is_accurate':True}
    n2=d
    d=ipart*d+n
    n=n2
    [n,d]=_sratio(n,d)	# simplifying the fraction
    if d==1:return {'ipart':str(n),'numerator':'0','deno':'1','is_accurate':True}
    return {'ipart':'','numerator':str(n),'deno':str(d),'is_accurate':True}

# assuming den1 and den2, both are positive
# den={'ipart':ipart,'numerator':numerator,'deno':deno}
def _unsignedDenaryFRInverse2(den1={},den2={}):
    if den['ipart']=='0':ipart=0
    else:ipart=int(den['ipart'])
    if den['numerator']=='0':n=0;d=1	# n=numerator,d=denominator
    else:n=int(den['numerator']);d=int(den['deno'])
    if ipart==0 and n==0: return {'ipart':'<inf>','fpart':'0','is_accurate':True}
    n2=d
    d=ipart*d+n
    n=n2
    [n,d]=_sratio2(n,d)	# simplifying the fraction
    if d==1:return {'ipart':str(n),'numerator':'0','deno':'1','is_accurate':True}
    return {'ipart':'','numerator':str(n),'deno':str(d),'is_accurate':True}


# den=denary number dictionary
def _denaryFPToFRMode(den={}):
    sign=den['sign']
    if den['input_mode']=='fp':
        if 'normalized' in den.keys():
            ipart,fpart=den['normalized']['ipart'],den['normalized']['fpart'];
            lf=len(fpart)

            for i in range(lf//3):
                nsd=1	# nsd=Number of search digits
                while (nsd<(lf-i)//2):
                    matchcount=0
                    searchstr=fpart[i:i+nsd]
                    for j in range(i,lf,nsd):
                        if fpart[j:j+nsd]!=searchstr:break
                        else:matchcount+=1
                    reqcount=(lf-i)//nsd	# reqcount=required count
                    if matchcount>=reqcount and nsd*matchcount>=lf-i:
                        if i==0:n=int(fpart[0:i+nsd])	          # n=numerator
                        else:n=int(fpart[0:i+nsd])-int(fpart[0:i])    # n=numerator
                        d=int('9'*nsd+'0'*i)                          # d=denominator
                        # simplifying the ratio saving time
                        [n,d]=_sratio2(n,d)
                        return {'ipart':ipart,'numerator':str(n),'deno':str(d),'is_accurate':True}
                    nsd+=1 
            
            if lf<=8:
                n=int(fpart);d=int('1'+'0'*lf)
                [n,d]=_sratio(n,d)
                return {'ipart':ipart,'numerator':str(n),'deno':str(d),'is_accurate':True}
            else: return den
    else: return den





########################################################################	
# The main number object
class Number:

    # public parts
    def __init__(self,num=None,base=10,prec=36,is_accurate=True,modify=False,ultraModify=False):
        try:            
            self.__parseddict=parseNumberString(num,base);
            self.__base=self.__parseddict['base']			
            if dataType(prec)!='int' or prec<0:raise Exception("Invalid precision is set")
            self.__max_prec=self.__prec=max(prec,self.__parseddict['prec'])            
            self.__is_accurate=is_accurate
            if modify in [True,False]:self.__modify=modify
            else:raise Exception("Invalid modify argument in __init__()")
            if ultraModify in [True,False]:self.__ultra_modify=ultraModify
            else:raise Exception("Invalid ultraModify argument in __init__()")
        except SyntaxError as e:
            del(self); return None
        except Exception as e:
            del(self); return None
 
        if num in ['inf','Inf','INF','<inf>','<Inf>','<INF>']:
            self.__num='<INF>';self.__base=base;self.__is_numeric=True;
            self.__parseddict['input_mode']='fp';
            self.__parseddict['is_integer']=False;
            self.__parseddict['is_float']=False;
            self.__parseddict['is_accurate']=is_accurate
            self.__prec=0;self.__max_prec=0;
            self.__parseddict['max_prec']=0;
            self.__parseddict['normalized']={'sign':'+','ipart':'<INF>','fpart':'0','is_accurate':True}
            self.__normal_prec=0
            self.__parseddict['normal_prec']=0
            self.__parseddict['base10']={'sign':'+','ipart':'<INF>','fpart':'0','is_accurate':True}	
            self.__base10_prec=0
            self.__parseddict['base10_prec']=0
        elif num in ['-inf','-Inf','-INF','<-inf>','<-Inf>','<-INF>']:
            self.__num='<-INF>';self.__base=base;self.__is_numeric=True;
            self.__parseddict['input_mode']='fp';
            self.__parseddict['is_integer']=False;
            self.__parseddict['is_float']=False;
            self.__parseddict['is_accurate']=is_accurate
            self.__prec=0;self.__max_prec=0;
            self.__parseddict['max_prec']=0
            self.__parseddict['normalized']={'sign':'-','ipart':'<INF>','fpart':'0','is_accurate':True}
            self.__normal_prec=0
            self.__parseddict['normal_prec']=0
            self.__parseddict['base10']={'sign':'-','ipart':'<INF>','fpart':'0','is_accurate':True}	
            self.__base10_prec=0
            self.__parseddict['base10_prec']=0				
        elif num in ['undefined','Undefined','UNDEFINED','<undefined>','<Undefined>','<UNDEFINED>']:
            self.__num='<UNDEFINED>';self.__base=base;self.__is_numeric=False;
            self.__parseddict['is_integer']=False;
            self.__parseddict['is_float']=False;
            self.__parseddict['is_accurate']=is_accurate
            self.__prec=0;self.__max_prec=0;
            self.__parseddict['max_prec']=0
            self.__parseddict['normalized']={'sign':'','ipart':'<UNDEFINED>','fpart':'','is_accurate':True}
            self.__normal_prec=0
            self.__parseddict['normal_prec']=0
            self.__parseddict['base10']={'sign':'','ipart':'<UNDEFINED>','fpart':'','is_accurate':True}	
            self.__parseddict['base10_prec']=0
        else:
            self.__num=num; self.__base=base; self.__is_numeric=True 
            self.__parseddict['is_accurate']=is_accurate

            # fixing the precision of the number
            if self.__parseddict['input_mode']=='fr' and self.__parseddict['numerator']!='0':
                # automatically modify in fractional mode
                _modifyNumber(self.__parseddict)
                self.__parseddict['max_prec']=self.__max_prec
            if modify==True and self.__parseddict['input_mode']=='fp':
                # modify the number dictionary in floating point mode
                _modifyNumber(self.__parseddict)
                self.__parseddict['max_prec']=self.__max_prec
            if ultraModify==True:
                # modifying the number dictionary
                _ultraModifyNumber(self.__parseddict)
                self.__parseddict['max_prec']=self.__max_prec
            # Fixing precision before normalization
            if self.__parseddict['exp']>0 and self.__parseddict['exp']>prec:
                self.__max_prec=self.__parseddict['exp']+self.__prec
                self.__parseddict['max_prec']=self.__max_prec
            
			# normalizing the number dictionary
            _normalizeNumberString(self.__parseddict,self.__max_prec,is_accurate)
            if self.__parseddict['normalized']['ipart']=='0' and self.__parseddict['normalized']['fpart']=='0': 
                self.__normal_prec=0
            elif self.__parseddict['normalized']['ipart']=='0' and self.__parseddict['normalized']['fpart']!='0': 
                self.__normal_prec=len(self.__parseddict['normalized']['fpart'])
            elif self.__parseddict['normalized']['ipart']!='0' and self.__parseddict['normalized']['fpart']=='0': 
                self.__normal_prec=len(self.__parseddict['normalized']['ipart'])
            elif self.__parseddict['normalized']['ipart']!='0' and self.__parseddict['normalized']['fpart']!='0': 
                self.__normal_prec=len(self.__parseddict['normalized']['ipart'])+\
                    len(self.__parseddict['normalized']['fpart'])
            self.__parseddict['normal_prec']=self.__normal_prec 
            self.__max_prec=max(self.__prec,self.__normal_prec)
            self.__parseddict['max_prec']=self.__max_prec

            # adding denary component if number is not denary
            _addDenary(self.__parseddict,self.__max_prec)
            _addDenaryFR(self.__parseddict,self.__max_prec)
            if self.__parseddict['base'] in [2,8,16,32,64]:

                if self.__parseddict['base10']['ipart']=='0' and self.__parseddict['base10']['fpart']=='0': 
                    self.__base10_prec=0
                elif self.__parseddict['base10']['ipart']=='0' and self.__parseddict['base10']['fpart']!='0': 
                    self.__base10_prec=len(self.__parseddict['base10']['fpart'])
                elif self.__parseddict['base10']['ipart']!='0' and self.__parseddict['base10']['fpart']=='0': 
                    self.__base10_prec=len(self.__parseddict['base10']['ipart'])
                elif self.__parseddict['base10']['ipart']!='0' and self.__parseddict['base10']['fpart']!='0': 
                    self.__base10_prec=len(self.__parseddict['base10']['ipart'])+\
                        len(self.__parseddict['base10']['fpart'])
                self.__parseddict['base10_prec']=self.__base10_prec
            elif self.__parseddict['base']==10:
                self.__base10_prec=self.__max_prec
                self.__parseddict['base10_prec']=self.__base10_prec
        # --------------------- END of the Constructor Function -------------------------

    # quick modify the number (time saving)
    def modify(self):
        if self.__parseddict['ipart'] not in ['<INF>','<UNDEFINED>']:
            _modifyNumber(self.__parseddict)

    # ultra modify the number, but can be very time consuming sometime
    def ultraModify(self):
        if self.__parseddict['ipart'] not in ['<INF>','<UNDEFINED>']:
            _ultraModifyNumber(self.__parseddict)

    # deep copying a number
    def copy(self):
        n=Number('0',base=self.__base,prec=self.__max_prec)
        for k in self.__parseddict.keys():
            if dataType(self.__parseddict[k])=='dict':n.__parseddict[k]=self.__parseddict[k].copy()
            else:n.__parseddict[k]=self.__parseddict[k]
        n.__num=self.__num;n.__base=self.__base;n.__prec=self.__prec;n.__max_prec=self.__max_prec;
        n.__base10_prec=self.__base10_prec; n.__normal_prec=self.__normal_prec;
        n.__is_accurate=self.__is_accurate; n.__is_numeric=self.__is_numeric
        return n

    # denary floating-point to denary fractional mode conversion
    def denaryFPtoFRMode(self):
        if self.__parseddict['ipart'] not in ['<INF>','<UNDEFINED>']:
            if self.__parseddict['base']==10:
                d=_denaryFPToFRMode(self.__parseddict)
                if 'numerator' in d.keys():
                    self.__parseddict['input_mode']='fr'
                    self.__parseddict['numerator']=d['numerator']
                    self.__parseddict['deno']=d['deno']
                    self.__parseddict.pop('fpart',None)


    # return different parts of the number
    def getOriginal(self): return self.__num

    def getDict(self): return self.__parseddict

    def getSign(self): return self.__parseddict['sign']

    def getBase(self): return self.__parseddict['base']

    def getPrecision(self): return self.__prec

    def getMaxPrecision(self): return self.__max_prec

    def getNormalPrecision(self): return self.__normal_prec

    def getBase10Precision(self): return self.__base10_prec

    def getInputMode(self): 
        return self.__parseddict['input_mode']

    def getIntegerPart(self):
        return self.__parseddict['normalized']['ipart']
 
    def getFloatingPart(self):
        return self.__parseddict['normalized']['fpart']

    def getNumerator(self):
        if 'numerator' in self.__parseddict.keys():
            if self.__parseddict['numerator']!='0':return self.__parseddict['numerator']
        return None

    def getDenominator(self):
        if 'deno' in self.__parseddict.keys():
            if self.__parseddict['deno'] not in ['','0']:return self.__parseddict['deno']
        return None

    def getExponent(self):
        return self.__parseddict['exp']


    def getNormalizedPart(self):
        return self.__parseddict['normalized']

    def getBase10Part(self):
        return self.__parseddict['base10']

    def getBase10frPart(self):
        if 'base10fr' in self.__parseddict.keys(): return self.__parseddict['base10fr']
            

    def getDenaryForm(self):
        if self.__parseddict['ipart'] not in ['<INF>','<UNDEFINED>']:
            return _stringify(_getDenaryForm(self.__parseddict,self.__max_prec))
        else:
            d=self.__parseddict.copy();d['base']=10
            return _stringify(d)

    def getBinaryForm(self):
        if self.__parseddict['ipart'] not in ['<INF>','<UNDEFINED>']:
            return _stringify(_getBinaryForm(self.__parseddict,self.__max_prec))
        else:
            d=self.__parseddict.copy();d['base']=2
            return _stringify(d)

    def getOctalForm(self):
        if self.__parseddict['ipart'] not in ['<INF>','<UNDEFINED>']:
            return _stringify(_getOctalForm(self.__parseddict,self.__max_prec))
        else:
            d=self.__parseddict.copy();d['base']=8;
            return _stringify(d)

    def getHexadecimalForm(self):
        if self.__parseddict['ipart'] not in ['<INF>','<UNDEFINED>']:
            return _stringify(_getHexadecimalForm(self.__parseddict,self.__max_prec))
        else:
            d=self.__parseddict.copy();d['base']=16
            return _stringify(d)

    def getBase32Form(self):
        if self.__parseddict['ipart'] not in ['<INF>','<UNDEFINED>']:
            return _stringify(_getBase32Form(self.__parseddict,self.__max_prec))
        else:
            d=self.__parseddict.copy();d['base']=32
            return _stringify(d)

    def getBase64Form(self):
        if self.__parseddict['ipart'] not in ['<INF>','<UNDEFINED>']:
            return _stringify(_getBase64Form(self.__parseddict,self.__max_prec))
        else:
            d=self.__parseddict.copy();d['base']=64
            return _stringify(d)
    
    def getAccuracy(self):return self.__parseddict['is_accurate']

    def getNormalizedPart(self):
        return self.__parseddict['normalized']

    def getNormalizedForm(self):
        if self.__parseddict['ipart'] not in ['<INF>','<UNDEFINED>']:
            if 'normalized' in self.__parseddict.keys():
                tempdir={'input_mode':'fp','base':self.__parseddict['base'],'sign':self.__parseddict['sign'],\
                    'ipart':self.__parseddict['normalized']['ipart'],'fpart':self.__parseddict['normalized']['fpart'],\
                     'exp':0}
                return _stringify(tempdir)
            else:
                return _stringify(_normalizeToFP(self.__parseddict,self.__normal_prec,self.__is_accurate))
        else: return self.__str__()

    def getScientificForm(self):
        if self.__parseddict['ipart'] not in ['<INF>','<UNDEFINED>']:
            return _stringify(_getScientificForm(self.__parseddict,self.__normal_prec))
        else: return self.__str__()

    # setting some properties
    # In precision mathematics, significant digits cannot be lost
    def setMaxPrecision(self,prec):
        if dataType(prec)!='int' or prec<1:raise ValueError("Invalid precision")
        if self.__parseddict['ipart'] not in ['<INF>','<UNDEFINED>']:
            if self.__max_prec < prec:
                self.__max_prec=prec;self.__parseddict['max_prec']=prec

    def displayInFPMode(self,prec=36,scientific=False):
        if dataType(prec)!='int' or prec<1:raise ValueError("Invalid precision")
        if scientific not in [False,True]:
            raise ValueError("Invalid boolean arguement 'scientific'")
        return _displayNumber(self.__parseddict,prec,scientific)

    def createNewNumber(self,prec=36,is_accurate=True):
        return _createNewNumber(self.__parseddict,prec,is_accurate)

    # if floating digits exceeds 6 more than its maximum set precision, floating digits
    # are kept within max+6 boundary
    def limitFloatingDigits(self,prec=36,is_accurate=False):
        if len(self.__parseddict['normalized']['fpart'])>6+self.__parseddict['base10_prec']:
            __parseddict['normalized']['fpart']=__parseddict['normalized']['fpart'][:6+self.__parseddict['base10_prec']]

    # To loss significant digits force fully
    def forceResetPrecision(self,newprec):
        if dataType(newprec)!='int' or newprec<1:raise ValueError("Invalid precision")
        if self.__parseddict['ipart'] not in ['<INF>','<UNDEFINED>']:
            _normalizeNumberString(self.__parseddict,newprec)
            if self.__parseddict['normalized']['ipart']=='0' and self.__parseddict['normalized']['fpart']=='0': 
                self.__normal_prec=0
            elif self.__parseddict['normalized']['ipart']=='0' and self.__parseddict['normalized']['fpart']!='0': 
                self.__normal_prec=len(self.__parseddict['normalized']['fpart'])
            elif self.__parseddict['normalized']['ipart']!='0' and self.__parseddict['normalized']['fpart']=='0': 
                self.__normal_prec=len(self.__parseddict['normalized']['ipart'])
            elif self.__parseddict['normalized']['ipart']!='0' and self.__parseddict['normalized']['fpart']!='0': 
                self.__normal_prec=len(self.__parseddict['normalized']['ipart'])+\
                    len(self.__parseddict['normalized']['fpart'])
            self.__parseddict['normal_prec']=self.__normal_prec 
            self.__max_prec=max(newprec,self.__prec,self.__normal_prec)
            self.__parseddict['max_prec']=self.__max_prec

            if self.__parseddict['base'] in [2,8,16,32,64]:
                # adding denary component if number is not denary
                _addDenary(self.__parseddict,newprec)
                _addDenaryFR(self.__parseddict,newprec)
                if self.__parseddict['base10']['ipart']=='0' and self.__parseddict['base10']['fpart']=='0': 
                    self.__base10_prec=0
                elif self.__parseddict['base10']['ipart']=='0' and self.__parseddict['base10']['fpart']!='0': 
                    self.__base10_prec=len(self.__parseddict['base10']['fpart'])
                elif self.__parseddict['base10']['ipart']!='0' and self.__parseddict['base10']['fpart']=='0': 
                    self.__base10_prec=len(self.__parseddict['base10']['ipart'])
                elif self.__parseddict['base10']['ipart']!='0' and self.__parseddict['base10']['fpart']!='0': 
                    self.__base10_prec=len(self.__parseddict['base10']['ipart'])+\
                        len(self.__parseddict['base10']['fpart'])
                self.__parseddict['base10_prec']=self.__base10_prec

    # return the boolean status of the number
    def isNumeric(self):
        if self.__parseddict['ipart']=='<UNDEFINED>': return False
        return self.__is_numeric
  
    def isPositive(self):
        if self.__parseddict['sign']=='+':return True
        else: return False

    def isNegative(self):
        if self.__parseddict['sign']=='-':return True
        else: return False
 
    def isInteger(self):
        return self.__parseddict['is_integer']        

    def isFloat(self):
        return self.__parseddict['is_float']

    def isFractional(self):
        if self.__parseddict['input_mode']=='fr':return True
        else: return False

    def isDenary(self):
        if self.__parseddict['base']==10:return True
        else: return False

    def isBinary(self):
        if self.__parseddict['base']==2:return True
        else: return False

    def isOctal(self):
        if self.__parseddict['base']==8:return True
        else: return False

    def isHexadecimal(self):
        if self.__parseddict['base']==16:return True
        else: return False

    def isBase32Number(self):
        if self.__parseddict['base']==32:return True
        else: return False

    def isBase64Number(self):
        if self.__parseddict['base']==64:return True
        else: return False

    def isRecurring(self):
        if self.__parseddict['ipart'] in ['<INF>','<UNDEFINED>']: return False
        if _isRecurring(self.__parseddict,self.__prec):return True
        else: return False

 
    def isAccurate(self):
        return self.__is_accurate


    def isPrime(self):
        if self.__parseddict['ipart'] in ['<INF>','<-INF>','<UNDEFINED>']: return False
        if 'normalized' not in self.__parseddict.keys():
            tempdict=_normalizeNumberString(self.__parseddict,self.__prec)
        else:tempdict=self.__parseddict
        if tempdict['is_float']:return False
        tint=tempdict['normalized']['ipart']	# tint=temporary integer
        if tempdict['base']==10:return _isPrime(int(tint))
        elif tempdict['base'] in [8,16,32,64]:
            tint=_toBinary(tint,base=tempdict['base'],part='integer')
        tint=_binToOtherBase(tint,base=10,part='integer')
        return _isPrime(int(tint))
        

    def denaryInteger(self):
        if self.__parseddict['ipart'] not in ['<INF>','<UNDEFINED>']:
            return int(self.__parseddict['sign']+self.__parseddict['base10']['ipart'])
#-------------------------------------------------------------------------------
    # representing the number in string format
    def __str__(self):
        if self.__parseddict==None:return ''
        return _stringify(self.__parseddict)

    # representing the number by value
    #def __repr__(self):
    #    if self.__parseddict==None:return None
    #    return _stringify(self.__parseddict)

      
        
#-------------------------------------------------------------------------------
    # __abs__() returns abs() 
    # returning positive copy of the given number
    def __abs__(self):
        if self.__parseddict['sign']=='-':
            return -1*self.copy()
        return self.copy()	

# Performing the mathematical operations
    # To add two numbers (a+b,a+7,a+2.56)
    def __add__(self,right):
        # addition: a+b or b+a (number.Number+number.Number) 
        if dataType(right)==str(__name__)+'.Number':
            # set precision of addition operation
            if self.__max_prec<right.__max_prec:max_prec=right.__max_prec
            else: max_prec=self.__max_prec
            
            #adding zero with zero
            if self==Number('0',is_accurate=True) and right==Number('0',is_accurate=True):
                return Number('0',is_accurate=True)
            elif self==Number('0',is_accurate=True) and right!=Number('0',is_accurate=True):
                return right
            elif self!=Number('0',is_accurate=True) and right==Number('0',is_accurate=True):
                return self.copy()

            if self.__parseddict['ipart'] not in ['<INF>','<-INF>','<UNDEFINED>']:
                if right.__parseddict['ipart']=='<INF>' and right.__parseddict['sign']=='+':
                    return Number('<inf>',10,0,True)
                elif right.__parseddict['ipart']=='<INF>' and right.__parseddict['sign']=='-':
                    return Number('<-inf>',10,0,True)
                elif right.__parseddict['ipart']=='<UNDEFINED>':return Number('<undefined>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+':
                if right.__parseddict['ipart']=='<INF>' and right.__parseddict['sign']=='+':
                    return Number('<inf>',10,0,True)
                elif right.__parseddict['ipart']=='<INF>' and right.__parseddict['sign']=='-':
                    return Number('<undefined>',10,0,True)
                elif right.__parseddict['ipart']=='<UNDEFINED>':return Number('<undefined>',10,0,True)
                else: return Number('<inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-':
                if right.__parseddict['ipart']=='<INF>' and right.__parseddict['sign']=='+':
                    return Number('<undefined>',10,0,True)
                elif right.__parseddict['ipart']=='<INF>' and right.__parseddict['sign']=='-':
                    return Number('<-inf>',10,0,True)
                elif right.__parseddict['ipart']=='<UNDEFINED>':return Number('<undefined>',10,0,True)
                else: return Number('<-inf>',10,0,True)
            elif self.__parseddict['ipart']=='<UNDEFINED>': return Number('<undefined>',10,0,True)

            # to support addition like Number('5 3/7') + Number('3 2/5')
            if self.__parseddict['input_mode']=='fr' and right.__parseddict['input_mode']=='fr'\
                 and self.__parseddict['exp']==0 and right.__parseddict['exp']==0:
                if self.__parseddict['sign']=='+' and right.__parseddict['sign']=='+':
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRAdd(a,b)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        d=_unsignedDenaryFRAdd(a,right.__parseddict['base10fr'])
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRAdd(self.__parseddict['base10fr'],b)
                    else:
                        d=_unsignedDenaryFRAdd(self.__parseddict['base10fr'],right.__parseddict['base10fr'])
                    return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)
            # to support addition like Number('5 3/7') + Number('10')
            elif self.__parseddict['input_mode']=='fr' and right.__parseddict['input_mode']=='fp'\
              and self.__parseddict['exp']==0 and right.__parseddict['exp']==0 and right.__parseddict['fpart']=='0':
                if self.__parseddict['sign']=='+' and right.__parseddict['sign']=='+':
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        b={'ipart':right.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRAdd(a,b)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        b={'ipart':right.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRAdd(a,b)
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        b={'ipart':right.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRAdd(self.__parseddict['base10fr'],b)
                    else:
                        b={'ipart':right.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRAdd(self.__parseddict['base10fr'],b)
                    return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                        prec=max_prec,is_accurate=d['is_accurate'],modify=False, ultraModify=False)

                elif self.__parseddict['sign']=='-' and right.__parseddict['sign']=='-':
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        b={'ipart':right.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRAdd(a,b)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        b={'ipart':right.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRAdd(a,b)
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        b={'ipart':right.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRAdd(self.__parseddict['base10fr'],b)
                    else:
                        b={'ipart':right.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRAdd(self.__parseddict['base10fr'],b)
                    return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)

                elif self.__parseddict['sign']=='+' and right.__parseddict['sign']=='-':                    
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        b={'ipart':right.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRSubtract(a,b)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        b={'ipart':right.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRSubtract(a,b)
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        b={'ipart':right.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRSubtract(self.__parseddict['base10fr'],b)
                    else:
                        b={'ipart':right.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRSubtract(self.__parseddict['base10fr'],b)

                    if d['ipart']=='0' and d['numerator']=='0':return Number('0',10,1,True)
                    if d['sign']=='+':
                        return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif d['sign']=='-':
                        return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)

                elif self.__parseddict['sign']=='-' and right.__parseddict['sign']=='+':
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        b={'ipart':right.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRSubtract(a,b)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        b={'ipart':right.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRSubtract(a,b)
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        b={'ipart':right.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRSubtract(self.__parseddict['base10fr'],b)
                    else:
                        b={'ipart':right.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRSubtract(self.__parseddict['base10fr'],b)

                    if d['ipart']=='0' and d['numerator']=='0':return Number('0',10,1,True)
                    if d['sign']=='+':
                        return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif d['sign']=='-':
                        return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
            # to support addition like Number('10') + Number('5 3/7') 
            elif self.__parseddict['input_mode']=='fp' and right.__parseddict['input_mode']=='fr'\
              and self.__parseddict['exp']==0 and right.__parseddict['exp']==0 and self.__parseddict['fpart']=='0':
                if self.__parseddict['sign']=='+' and right.__parseddict['sign']=='+':
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRAdd(a,b)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        a={'ipart':self.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        b={'ipart':right.__parseddict['base10']['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRAdd(a,b)
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRAdd(a,b)
                    else:
                        a={'ipart':self.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRAdd(a,right.__parseddict['base10fr'])
                    return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                        prec=max_prec,is_accurate=d['is_accurate'],modify=False, ultraModify=False)

                elif self.__parseddict['sign']=='-' and right.__parseddict['sign']=='-':
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRAdd(a,b)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        a={'ipart':self.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRAdd(a,b)
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRAdd(a,right.__parseddict['base10fr'])
                    else:
                        a={'ipart':self.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRAdd(a,right.__parseddict['base10fr'])
                    return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)

                elif self.__parseddict['sign']=='+' and right.__parseddict['sign']=='-':                    
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRSubtract(a,b)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        a={'ipart':self.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRSubtract(a,right.__parseddict['base10fr'])
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRSubtract(a,b)
                    else:
                        a={'ipart':self.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRSubtract(a,right.__parseddict['base10fr'])

                    if d['ipart']=='0' and d['numerator']=='0':return Number('0',10,1,True)
                    if d['sign']=='+':
                        return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif d['sign']=='-':
                        return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)

                elif self.__parseddict['sign']=='-' and right.__parseddict['sign']=='+':
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRSubtract(a,b)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        a={'ipart':self.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRSubtract(a,right.__parseddict['base10fr'])
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRSubtract(a,b)
                    else:
                        a={'ipart':self.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRSubtract(a,right.__parseddict['base10fr'])

                    if d['ipart']=='0' and d['numerator']=='0':return Number('0',10,1,True)
                    if d['sign']=='+':
                        return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif d['sign']=='-':
                        return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)

            # to support other type of additions addition like Number('5 3/7') + Number('10.45')
            else:
                if self.__parseddict['sign']=='+' and right.__parseddict['sign']=='+':
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        d=_unsignedDenaryAdd(self.__parseddict['normalized'],right.__parseddict['normalized'])
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        d=_unsignedDenaryAdd(self.__parseddict['normalized'],right.__parseddict['base10'])
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        d=_unsignedDenaryAdd(self.__parseddict['base10'],right.__parseddict['normalized'])
                    else:
                        d=_unsignedDenaryAdd(self.__parseddict['base10'],right.__parseddict['base10'])
                    return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)

                elif self.__parseddict['sign']=='-' and right.__parseddict['sign']=='-':
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        d=_unsignedDenaryAdd(self.__parseddict['normalized'],right.__parseddict['normalized'])
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        d=_unsignedDenaryAdd(self.__parseddict['normalized'],right.__parseddict['base10'])
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        d=_unsignedDenaryAdd(self.__parseddict['base10'],right.__parseddict['normalized'])
                    else:
                        d=_unsignedDenaryAdd(self.__parseddict['base10'],right.__parseddict['base10'])
                    return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)

                elif self.__parseddict['sign']=='+' and right.__parseddict['sign']=='-':
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        d=_unsignedDenarySubtract(self.__parseddict['normalized'],right.__parseddict['normalized'])
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        d=_unsignedDenarySubtract(self.__parseddict['normalized'],right.__parseddict['base10'])
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        d=_unsignedDenarySubtract(self.__parseddict['base10'],right.__parseddict['normalized'])
                    else:
                        d=_unsignedDenarySubtract(self.__parseddict['base10'],right.__parseddict['base10'])

                    if d['ipart']=='' and d['fpart']=='':return Number('0',10,1,True)
                    if d['sign']=='+':
                        return Number(d['ipart']+'.'+d['fpart'],base=10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif d['sign']=='-':
                        return Number('-'+d['ipart']+'.'+d['fpart'],base=10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)

                elif self.__parseddict['sign']=='-' and right.__parseddict['sign']=='+':
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        d=_unsignedDenarySubtract(self.__parseddict['normalized'],right.__parseddict['normalized'])
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        d=_unsignedDenarySubtract(self.__parseddict['normalized'],right.__parseddict['base10'])
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        d=_unsignedDenarySubtract(self.__parseddict['base10'],right.__parseddict['normalized'])
                    else:
                        d=_unsignedDenarySubtract(self.__parseddict['base10'],right.__parseddict['base10'])

                    if d['ipart']=='0' and d['fpart']=='0':return Number('0',10,1,True)
                    if d['sign']=='+':
                        return Number('-'+d['ipart']+'.'+d['fpart'],base=10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif d['sign']=='-':
                        return Number(d['ipart']+'.'+d['fpart'],base=10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)

        # to support these additions: a+50; b+10 (number.Number+denary integer)
        elif dataType(right)=='int':
            # set precision of addition operation
            max_prec=self.__max_prec

            if right==0:return self.copy()

            if self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+': return Number('<inf>',10)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-':return Number('<-inf>',10)
            elif self.__parseddict['ipart']=='<UNDEFINED>': return Number('<undefined>',10)
            
            if self.__parseddict['sign']=='+':sign=1
            elif self.__parseddict['sign']=='-':sign=-1

            if self.__parseddict['base']==10:
                if self.__parseddict['input_mode']=='fr' and self.__parseddict['exp']==0:
                    if self.__parseddict['sign']=='+' and right>0:
                        d=_unsignedDenaryFRAdd(self.__parseddict,{'ipart':str(right),'numerator':'0','deno':'1'})
                        return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right<0:
                        d=_unsignedDenaryFRAdd(self.__parseddict,{'ipart':str(-1*right),'numerator':'0','deno':'1'})
                        return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right>0:
                        d=_unsignedDenaryFRSubtract(self.__parseddict,{'ipart':str(right),'numerator':'0','deno':'1'})

                        if d['ipart']=='0' and d['numerator']=='0':return Number('0',10,1)
                        if d['sign']=='+':
                            return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                                prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        elif d['sign']=='-':
                            return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                                prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='+' and right<0:
                        d=_unsignedDenaryFRSubtract(self.__parseddict,{'ipart':str(-1*right),'numerator':'0','deno':'1'})

                        if d['ipart']=='0' and d['numerator']=='0':return Number('0',10,1,True)
                        if d['sign']=='+':
                            return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                                prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        elif d['sign']=='-':
                            return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                                prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                else:                    
                    if self.__parseddict['sign']=='+' and right>0:
                        d=_unsignedDenaryAdd(self.__parseddict['normalized'],{'ipart':str(right),'fpart':'0'})
                        return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right<0:
                        d=_unsignedDenaryAdd(self.__parseddict['normalized'],{'ipart':str(-1*right),'fpart':'0'})
                        return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right>0:
                        d=_unsignedDenarySubtract(self.__parseddict['normalized'],{'ipart':str(right),'fpart':'0'})

                        if d['ipart']=='0' and d['fpart']=='0':return Number('0',10,1,True)
                        if d['sign']=='+':
                            return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                                is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        elif d['sign']=='-':
                            return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                                is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='+' and right<0:
                        d=_unsignedDenarySubtract(self.__parseddict['normalized'],{'ipart':str(-1*right),'fpart':'0'})

                        if d['ipart']=='0' and d['fpart']=='0':return Number('0',10,1,True)
                        if d['sign']=='+':
                            return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                                is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        elif d['sign']=='-':
                            return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                                is_accurate=d['is_accurate'],modify=False,ultraModify=False)

            elif self.__parseddict['base'] in [2,8,16,32,64]:
                if self.__parseddict['input_mode']=='fr' and self.__parseddict['exp']==0:
                    if self.__parseddict['sign']=='+' and right>0:
                        d=_unsignedDenaryFRAdd(self.__parseddict['base10fr'],{'ipart':str(right),\
                            'numerator':'0','deno':'1'})
                        return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right<0:
                        d=_unsignedDenaryFRAdd(self.__parseddict['base10fr'],{'ipart':str(-1*right),\
                            'numerator':'0','deno':'1'})
                        return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right>0:
                        d=_unsignedDenaryFRSubtract(self.__parseddict['base10fr'],{'ipart':str(right),\
                            'numerator':'0','deno':'1'})

                        if d['ipart']=='0' and d['numerator']=='0':return Number('0',10,1,True)
                        if d['sign']=='+':
                            return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                                prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        elif d['sign']=='-':
                            return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                                prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='+' and right<0:
                        d=_unsignedDenaryFRSubtract(self.__parseddict['base10fr'],{'ipart':str(-1*right),\
                            'numerator':'0','deno':'1'})

                        if d['ipart']=='0' and d['numerator']=='0':return Number('0',10,1,True)
                        if d['sign']=='+':
                            return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                                prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        elif d['sign']=='-':
                            return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                                prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                else:
                    if self.__parseddict['sign']=='+' and right>0:
                        d=_unsignedDenaryAdd(self.__parseddict['base10'],{'ipart':str(right),'fpart':'0'})
                        return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right<0:
                        d=_unsignedDenaryAdd(self.__parseddict['base10'],{'ipart':str(-1*right),'fpart':'0'})
                        return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right>0:
                        d=_unsignedDenarySubtract(self.__parseddict['base10'],{'ipart':str(right),'fpart':'0'})

                        if d['ipart']=='0' and d['fpart']=='0':return Number('0',10,1,True)
                        if d['sign']=='+':
                            return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                                is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        elif d['sign']=='-':
                            return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                                is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='+' and right<0:
                        d=_unsignedDenarySubtract(self.__parseddict['base10'],{'ipart':str(-1*right),'fpart':'0'})

                        if d['ipart']=='0' and d['fpart']=='0':return Number('0',10,1,True)
                        if d['sign']=='+':
                            return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                                is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        elif d['sign']=='-':
                            return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                                is_accurate=d['is_accurate'],modify=False,ultraModify=False)

        # to support these additions: a+50.25; b+10.0124; c+12e15 etc (number.Number+denary float)
        elif dataType(right)=='float':
            rdict=_normalizeDenary(right)
            # set precision of addition operation
            max_prec=self.__max_prec

            if right==0.0:return self.copy()

            if self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+':
                return Number('<inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-':
                return Number('<-inf>',10,0,True)
            elif self.__parseddict['ipart']=='<UNDEFINED>': return Number('<undefined>',10,0,True)

            if self.__parseddict['base']==10:
                if self.__parseddict['sign']=='+' and rdict['sign']=='+':
                    d=_unsignedDenaryAdd(self.__parseddict['normalized'],rdict)
                    return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                elif self.__parseddict['sign']=='-' and rdict['sign']=='-':
                    d=_unsignedDenaryAdd(self.__parseddict['normalized'],rdict)
                    return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                elif self.__parseddict['sign']=='+' and rdict['sign']=='-':
                    d=_unsignedDenarySubtract(self.__parseddict['normalized'],rdict)

                    if d['ipart']=='' and d['fpart']=='':return Number('0',10,1,True)
                    if d['sign']=='+':
                        return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif d['sign']=='-':
                        return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                elif self.__parseddict['sign']=='-' and rdict['sign']=='+':
                    d=_unsignedDenarySubtract(self.__parseddict['normalized'],rdict)

                    if d['ipart']=='' and d['fpart']=='':return Number('0',10,1,True)
                    if d['sign']=='+':
                        return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif d['sign']=='-':
                        return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)

            elif self.__parseddict['base'] in [2,8,16,32,64]:
                if self.__parseddict['sign']=='+' and rdict['sign']=='+':
                    d=_unsignedDenaryAdd(self.__parseddict['base10'],rdict)
                    return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                elif self.__parseddict['sign']=='-' and rdict['sign']=='-':
                    d=_unsignedDenaryAdd(self.__parseddict['base10'],rdict)
                    return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                elif self.__parseddict['sign']=='+' and rdict['sign']=='-':
                    d=_unsignedDenarySubtract(self.__parseddict['base10'],rdict)

                    if d['ipart']=='' and d['fpart']=='':return Number('0',10,1,True)
                    if d['sign']=='+':
                        return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif d['sign']=='-':
                        return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                elif self.__parseddict['sign']=='-' and rdict['sign']=='+':
                    d=_unsignedDenarySubtract(self.__parseddict['base10'],rdict)

                    if d['ipart']=='' and d['fpart']=='':return Number('0',10,1,True)
                    if d['sign']=='+':
                        return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif d['sign']=='-':
                        return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
        else: raise TypeError("Invalid operand of the operator '+'")
            

    # addition:10+a or 10.25+a (left+self)
    def __radd__(self,left):
        if dataType(left) in ['int','float'] or dataType(left)==str(__name__)+'.Number':
            return self.__add__(left)
        else: raise TypeError("Invalid operand of the operator '+'")


    # To subtract two numbers (a-b,a-7,a-2.56)
    def __sub__(self,right):
        # subtraction: a-b or b-a (number.Number - number.Number) 
        if dataType(right)==str(__name__)+'.Number':
            # set precision of addition operation
            if self.__max_prec<right.__max_prec:max_prec=right.__max_prec
            else: max_prec=self.__max_prec

            if self.__parseddict['ipart'] not in ['<INF>','<-INF>','<UNDEFINED>']:
                if right.__parseddict['ipart']=='<INF>' and right.__parseddict['sign']=='+':
                    return Number('<-inf>',10,0,True)
                elif right.__parseddict['ipart']=='<INF>' and right.__parseddict['sign']=='-':
                    return Number('<inf>',10,0,True)
                elif right.__parseddict['ipart']=='<UNDEFINED>':return Number('<undefined>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+':
                if right.__parseddict['ipart']=='<INF>' and right.__parseddict['sign']=='+':
                    return Number('<undefined>',10,0,True)
                elif right.__parseddict['ipart']=='<INF>' and right.__parseddict['sign']=='-':
                    return Number('<inf>',10,0,True)
                elif right.__parseddict['ipart']=='<UNDEFINED>':return Number('<undefined>',10,0,True)
                else: return Number('<inf>',10)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-':
                if right.__parseddict['ipart']=='<INF>' and right.__parseddict['sign']=='+':
                    return Number('<-inf>',10,0,True)
                elif right.__parseddict['ipart']=='<INF>' and right.__parseddict['sign']=='-':
                    return Number('<undefined>',10,0,True)
                elif right.__parseddict['ipart']=='<UNDEFINED>':return Number('<undefined>',10,0,True)
                else: return Number('<-inf>',10,0,True)
            elif self.__parseddict['ipart']=='<UNDEFINED>': return Number('<undefined>',10,0,True)

            # to support subtraction like Number('5 3/7') - Number('3 2/5')
            if self.__parseddict['input_mode']=='fr' and right.__parseddict['input_mode']=='fr'\
                 and self.__parseddict['exp']==0 and right.__parseddict['exp']==0:
                if self.__parseddict['sign']=='+' and right.__parseddict['sign']=='+':
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRSubtract(a,b)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        d=_unsignedDenaryFRSubtract(a,right.__parseddict['base10fr'])
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRSubtract(self.__parseddict['base10fr'],b)
                    else:
                        d=_unsignedDenaryFRSubtract(self.__parseddict['base10fr'],right.__parseddict['base10fr'])

                    if d['ipart']=='0' and d['numerator']=='':return Number('0',10,1,True)
                    if d['sign']=='+': # a-b; a>b; 5 2/3 - 2 4/5
                        return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif d['sign']=='-': # a-b; a<b; 2 4/5 - 5 2/3 
                        return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)

                elif self.__parseddict['sign']=='-' and right.__parseddict['sign']=='-':
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRSubtract(a,b)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        d=_unsignedDenaryFRSubtract(a,right.__parseddict['base10fr'])
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRSubtract(self.__parseddict['base10fr'],b)
                    else:
                        d=_unsignedDenaryFRSubtract(self.__parseddict['base10fr'],right.__parseddict['base10fr'])

                    if d['ipart']=='0' and d['numerator']=='':return Number('0',10,1,True)
                    if d['sign']=='+': # a-b; a>b; 5 2/3 - 2 4/5
                        return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif d['sign']=='-': # a-b; a<b; 2 4/5 - 5 2/3
                        return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)

                elif self.__parseddict['sign']=='+' and right.__parseddict['sign']=='-':
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRAdd(a,b)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        d=_unsignedDenaryFRAdd(a,right.__parseddict['base10fr'])
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRAdd(self.__parseddict['base10fr'],b)
                    else:
                        d=_unsignedDenaryFRAdd(self.__parseddict['base10fr'],right.__parseddict['base10fr'])
                    return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)

                elif self.__parseddict['sign']=='-' and right.__parseddict['sign']=='+':
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRAdd(a,b)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        d=_unsignedDenaryFRAdd(a,right.__parseddict['base10fr'])
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRAdd(self.__parseddict['base10fr'],b)
                    else:
                        d=_unsignedDenaryFRAdd(self.__parseddict['base10fr'],right.__parseddict['base10fr'])
                    return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)

            # to support subtraction like Number('5 3/7') - Number('10')
            elif self.__parseddict['input_mode']=='fr' and right.__parseddict['input_mode']=='fp'\
              and self.__parseddict['exp']==0 and right.__parseddict['exp']==0 and right.__parseddict['fpart']=='0':
                if self.__parseddict['sign']=='+' and right.__parseddict['sign']=='+':
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        b={'ipart':right.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRSubtract(a,b)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        b={'ipart':right.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRSubtract(a,b)
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        b={'ipart':right.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRSubtract(self.__parseddict['base10fr'],b)
                    else:
                        b={'ipart':right.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRSubtract(self.__parseddict['base10fr'],b)

                    if d['ipart']=='0' and d['numerator']=='0':return Number('0',10,1,True)
                    if d['sign']=='+':
                        return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif d['sign']=='-':
                        return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)

                elif self.__parseddict['sign']=='-' and right.__parseddict['sign']=='-':
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        b={'ipart':right.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRSubtract(a,b)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        b={'ipart':right.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRSubtract(a,b)
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        b={'ipart':right.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRSubtract(self.__parseddict['base10fr'],b)
                    else:
                        b={'ipart':right.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRSubtract(self.__parseddict['base10fr'],b)

                    if d['ipart']=='0' and d['numerator']=='0':return Number('0',10,1,True)
                    if d['sign']=='+':
                        return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif d['sign']=='-':
                        return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)

                elif self.__parseddict['sign']=='+' and right.__parseddict['sign']=='-':                    
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        b={'ipart':right.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRAdd(a,b)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        b={'ipart':right.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRAdd(a,b)
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        b={'ipart':right.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRAdd(self.__parseddict['base10fr'],b)
                    else:
                        b={'ipart':right.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRAdd(self.__parseddict['base10fr'],b)
                    return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)

                elif self.__parseddict['sign']=='-' and right.__parseddict['sign']=='+':
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        b={'ipart':right.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRAdd(a,b)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        b={'ipart':right.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRAdd(a,b)
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        b={'ipart':right.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRAdd(self.__parseddict['base10fr'],b)
                    else:
                        b={'ipart':right.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRAdd(self.__parseddict['base10fr'],b)
                    return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)

            # to support subtraction like Number('10') - Number('5 3/7') 
            elif self.__parseddict['input_mode']=='fp' and right.__parseddict['input_mode']=='fr'\
              and self.__parseddict['exp']==0 and right.__parseddict['exp']==0 and self.__parseddict['fpart']=='0':
                if self.__parseddict['sign']=='+' and right.__parseddict['sign']=='+':
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRSubtract(a,b)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        a={'ipart':self.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRSubtract(a,right.__parseddict['base10fr'])
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRSubtract(a,b)
                    else:
                        a={'ipart':self.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRSubtract(a,right.__parseddict['base10fr'])

                    if d['ipart']=='0' and d['numerator']=='0':return Number('0',10,1,True)
                    if d['sign']=='+':
                        return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif d['sign']=='-':
                        return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)

                elif self.__parseddict['sign']=='-' and right.__parseddict['sign']=='-':
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRSubtract(a,b)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        a={'ipart':self.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRSubtract(a,b)
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRSubtract(a,right.__parseddict['base10fr'])
                    else:
                        a={'ipart':self.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRSubtract(a,right.__parseddict['base10fr'])

                    if d['ipart']=='0' and d['numerator']=='0':return Number('0',10,1,True)
                    if d['sign']=='+':
                        return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif d['sign']=='-':
                        return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)

                elif self.__parseddict['sign']=='+' and right.__parseddict['sign']=='-':                    
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRAdd(a,b)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        a={'ipart':self.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRAdd(a,right.__parseddict['base10fr'])
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRAdd(a,b)
                    else:
                        a={'ipart':self.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRAdd(a,right.__parseddict['base10fr'])
                    return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                        prec=max_prec,is_accurate=d['is_accurate'],modify=False, ultraModify=False)

                elif self.__parseddict['sign']=='-' and right.__parseddict['sign']=='+':
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRAdd(a,b)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        a={'ipart':self.__parseddict['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRAdd(a,right.__parseddict['base10fr'])
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRAdd(a,b)
                    else:
                        a={'ipart':self.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                        d=_unsignedDenaryFRAdd(a,right.__parseddict['base10fr'])
                    return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)

            # to support subtraction like Number('10 2/5') - Number('5.478p-5')
            else:
                if self.__parseddict['sign']=='+' and right.__parseddict['sign']=='+':
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        d=_unsignedDenarySubtract(self.__parseddict['normalized'],right.__parseddict['normalized'])
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        d=_unsignedDenarySubtract(self.__parseddict['normalized'],right.__parseddict['base10'])
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        d=_unsignedDenarySubtract(self.__parseddict['base10'],right.__parseddict['normalized'])
                    else:
                        d=_unsignedDenarySubtract(self.__parseddict['base10'],right.__parseddict['base10'])

                    if d['ipart']=='' and d['fpart']=='':return Number('0',10,1,True)
                    if d['sign']=='+':
                        return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif d['sign']=='-':
                        return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)

                elif self.__parseddict['sign']=='-' and right.__parseddict['sign']=='-':
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        d=_unsignedDenarySubtract(self.__parseddict['normalized'],right.__parseddict['normalized'])
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        d=_unsignedDenarySubtract(self.__parseddict['normalized'],right.__parseddict['base10'])
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        d=_unsignedDenarySubtract(self.__parseddict['base10'],right.__parseddict['normalized'])
                    else:
                        d=_unsignedDenarySubtract(self.__parseddict['base10'],right.__parseddict['base10'])

                    if d['ipart']=='' and d['fpart']=='':return Number('0',10,1)
                    if d['sign']=='+':
                        return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif d['sign']=='-':
                        return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)

                elif self.__parseddict['sign']=='+' and right.__parseddict['sign']=='-':
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        d=_unsignedDenaryAdd(self.__parseddict['normalized'],right.__parseddict['normalized'])
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        d=_unsignedDenaryAdd(self.__parseddict['normalized'],right.__parseddict['base10'])
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        d=_unsignedDenaryAdd(self.__parseddict['base10'],right.__parseddict['normalized'])
                    else:
                        d=_unsignedDenaryAdd(self.__parseddict['base10'],right.__parseddict['base10'])
                    return Number(d['ipart']+'.'+d['fpart'],base=10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)

                elif self.__parseddict['sign']=='-' and right.__parseddict['sign']=='+':
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        d=_unsignedDenaryAdd(self.__parseddict['normalized'],right.__parseddict['normalized'])
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        d=_unsignedDenaryAdd(self.__parseddict['normalized'],right.__parseddict['base10'])
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        d=_unsignedDenaryAdd(self.__parseddict['base10'],right.__parseddict['normalized'])
                    else:
                        d=_unsignedDenaryAdd(self.__parseddict['base10'],right.__parseddict['base10'])
                    return Number('-'+d['ipart']+'.'+d['fpart'],base=10,\
                        prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)

        # to support these subtractions: a-50; b-10 (number.Number - denary integer)
        elif dataType(right)=='int':
            if right==0:return self.copy()
            max_prec=self.__max_prec
            if self.__parseddict['sign']=='+':sign=1
            elif self.__parseddict['sign']=='-':sign=-1

            if self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+':
                return Number('<inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-':
                return Number('<-inf>',10,0,True)
            elif self.__parseddict['ipart']=='<UNDEFINED>': return Number('<undefined>',10,0,True)

            if self.__parseddict['base']==10:
                if self.__parseddict['input_mode']=='fr' and self.__parseddict['exp']==0:
                    if self.__parseddict['sign']=='+' and right>0:
                        d=_unsignedDenaryFRSubtract(self.__parseddict,{'ipart':str(right),'numerator':'0','deno':'1'})

                        if d['ipart']=='' and d['numerator']=='':return Number('0',10,1,True)
                        if d['sign']=='+':
                            return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                                prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        elif d['sign']=='-':
                            return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                                prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right<0:
                        d=_unsignedDenaryFRSubtract(self.__parseddict,{'ipart':str(-1*right),'numerator':'0','deno':'1'})

                        if d['ipart']=='' and d['numerator']=='':return Number('0',10,1,True)
                        if d['sign']=='+':
                            return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                                prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        elif d['sign']=='-':
                            return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                                prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right>0:
                        d=_unsignedDenaryFRAdd(self.__parseddict,{'ipart':str(right),'numerator':'0','deno':'1'})
                        return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)

                    elif self.__parseddict['sign']=='+' and right<0:
                        d=_unsignedDenaryFRAdd(self.__parseddict,{'ipart':str(-1*right),'numerator':'0','deno':'1'})
                        return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)

                else:                    
                    if self.__parseddict['sign']=='+' and right>0:
                        d=_unsignedDenarySubtract(self.__parseddict['normalized'],{'ipart':str(right),'fpart':'0'})

                        if d['ipart']=='' and d['fpart']=='':return Number('0',10,1,True)
                        if d['sign']=='+':
                            return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                                is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        elif d['sign']=='-':
                            return Number('-'+d['ipart']+'.'+d['fpart'],10,\
                                prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right<0:
                        d=_unsignedDenarySubtract(self.__parseddict['normalized'],{'ipart':str(-1*right),'fpart':'0'})

                        if d['ipart']=='' and d['fpart']=='':return Number('0',10,1,True)
                        if d['sign']=='+':
                            return Number('-'+d['ipart']+'.'+d['fpart'],10,\
                                prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        elif d['sign']=='-':
                            return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                                is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right>0:
                        d=_unsignedDenaryAdd(self.__parseddict['normalized'],{'ipart':str(right),'fpart':'0'})
                        return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='+' and right<0:
                        d=_unsignedDenaryAdd(self.__parseddict['normalized'],{'ipart':str(-1*right),'fpart':'0'})
                        return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)

            elif self.__parseddict['base'] in [2,8,16,32,64]:
                if self.__parseddict['input_mode']=='fr' and self.__parseddict['exp']==0:
                    if self.__parseddict['sign']=='+' and right>0:
                        d=_unsignedDenaryFRSubtract(self.__parseddict['base10fr'],{'ipart':str(right),\
                            'numerator':'','deno':''})

                        if d['ipart']=='' and d['numerator']=='':return Number('0',10,1,True)
                        if d['sign']=='+':
                            return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                                prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        elif d['sign']=='-':
                            return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                                prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right<0:
                        d=_unsignedDenaryFRSubtract(self.__parseddict['base10fr'],{'ipart':str(-1*right),\
                            'numerator':'','deno':''})

                        if d['ipart']=='' and d['fpart']=='':return Number('0',10,1,True)
                        if d['sign']=='+':
                            return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                                prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        elif d['sign']=='-':
                            return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                                prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right>0:
                        d=_unsignedDenaryFRAdd(self.__parseddict['base10fr'],{'ipart':str(right),\
                            'numerator':'','deno':''})
                        return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='+' and right<0:
                        d=_unsignedDenaryFRAdd(self.__parseddict['base10fr'],{'ipart':str(-1*right),\
                            'numerator':'','deno':''})
                        return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                else:
                    if self.__parseddict['sign']=='+' and right>0:
                        d=_unsignedDenarySubtract(self.__parseddict['base10'],{'ipart':str(right),'fpart':'0'})

                        if d['ipart']=='' and d['fpart']=='':return Number('0',10,1,True)
                        if d['sign']=='+':
                            return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                                is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        elif d['sign']=='-':
                            return Number('-'+d['ipart']+'.'+d['fpart'],10,\
                                prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right<0:
                        d=_unsignedDenarySubtract(self.__parseddict['base10'],{'ipart':str(-1*right),'fpart':'0'})

                        if d['ipart']=='' and d['fpart']=='':return Number('0',10,1,True)
                        if d['sign']=='+':
                            return Number('-'+d['ipart']+'.'+d['fpart'],10,\
                                prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        elif d['sign']=='-':
                            return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                                is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right>0:
                        d=_unsignedDenaryAdd(self.__parseddict['base10'],{'ipart':str(right),'fpart':'0'})
                        return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='+' and right<0:
                        d=_unsignedDenaryAdd(self.__parseddict['base10'],{'ipart':str(-1*right),'fpart':'0'})
                        return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)

        # to support these subtractions: a-50.25; b-10.0124; c-12e15 etc (number.Number - denary float)
        elif dataType(right)=='float':
            rdict=_normalizeDenary(right)
            max_prec=self.__max_prec

            if self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+':
                return Number('<inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-':
                return Number('<-inf>',10,0,True)
            elif self.__parseddict['ipart']=='<UNDEFINED>': return Number('<undefined>',10,0,True)

            if self.__parseddict['base']==10:
                if self.__parseddict['sign']=='+' and rdict['sign']=='+':
                    d=_unsignedDenarySubtract(self.__parseddict['normalized'],rdict)

                    if d['ipart']=='' and d['fpart']=='':return Number('0',10,1,True)
                    if d['sign']=='+':
                        return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif d['sign']=='-':
                        return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                elif self.__parseddict['sign']=='-' and rdict['sign']=='-':
                    d=_unsignedDenarySubtract(self.__parseddict['normalized'],rdict)

                    if d['ipart']=='' and d['fpart']=='':return Number('0',10,1,True)
                    if d['sign']=='+':
                        return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif d['sign']=='-':
                        return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                elif self.__parseddict['sign']=='+' and rdict['sign']=='-':
                    d=_unsignedDenaryAdd(self.__parseddict['normalized'],rdict)
                    return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                elif self.__parseddict['sign']=='-' and rdict['sign']=='+':
                    d=_unsignedDenaryAdd(self.__parseddict['normalized'],rdict)
                    return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)

            elif self.__parseddict['base'] in [2,8,16,32,64]:
                if self.__parseddict['sign']=='+' and rdict['sign']=='+':
                    d=_unsignedDenarySubtract(self.__parseddict['base10'],rdict)

                    if d['ipart']=='' and d['fpart']=='':return Number('0',10,1,True)
                    if d['sign']=='+':
                        return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif d['sign']=='-':
                        return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                elif self.__parseddict['sign']=='-' and rdict['sign']=='-':
                    d=_unsignedDenarySubtract(self.__parseddict['base10'],rdict)

                    if d['ipart']=='' and d['fpart']=='':return Number('0',10,1,True)
                    if d['sign']=='+':
                        return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif d['sign']=='-':
                        return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                elif self.__parseddict['sign']=='+' and rdict['sign']=='-':
                    d=_unsignedDenaryAdd(self.__parseddict['base10'],rdict)
                    return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                elif self.__parseddict['sign']=='-' and rdict['sign']=='+':
                    d=_unsignedDenaryAdd(self.__parseddict['base10'],rdict)
                    return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)

        else: raise TypeError("Invalid operand of the operator '-'")


    # left subtraction: 10-a or 10.25-a (left - self)
    def __rsub__(self,left):
        if dataType(left) in ['int','float',str(__name__)+'.Number']:
            a=self.__sub__(left)
            if a.__parseddict['sign']=='+':a.__parseddict['sign']='-'
            elif a.__parseddict['sign']=='-':a.__parseddict['sign']='+'
            return a
        else: raise TypeError("Invalid operand of the operator '-'")

    # negating a number: -a (-self)
    def __neg__(self):
        if self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+':
            return Number('<-inf>',10,0,True)
        elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-':
            return Number('<inf>',10,0,True)
        elif self.__parseddict['ipart']=='<UNDEFINED>': return Number('<undefined>',10,0,True)

        n=Number('0',base=10,prec=self.__max_prec)
        for k in self.__parseddict.keys():
            if dataType(self.__parseddict[k])=='dict':n.__parseddict[k]=self.__parseddict[k].copy()
            else:n.__parseddict[k]=self.__parseddict[k]
        
        if n.__parseddict['sign']=='-':n.__parseddict['sign']='+'
        else:n.__parseddict['sign']='-'

        if 'normalized' in n.__parseddict.keys():
            if n.__parseddict['normalized']['sign']=='-':n.__parseddict['normalized']['sign']='+'
            else:n.__parseddict['normalized']['sign']='-'
        if 'base10' in n.__parseddict.keys():
            if n.__parseddict['base10']['sign']=='-':n.__parseddict['base10']['sign']='+'
            else:n.__parseddict['base10']['sign']='-'
        if 'base10fr' in n.__parseddict.keys():
            if n.__parseddict['base10fr']['sign']=='-':n.__parseddict['base10fr']['sign']='+'
            else:n.__parseddict['base10fr']['sign']='-'
        if 'base2' in n.__parseddict.keys():
            if n.__parseddict['base2']['sign']=='-':n.__parseddict['base2']['sign']='+'
            else:n.__parseddict['base2']['sign']='-'
        if 'base64' in n.__parseddict.keys():
            if n.__parseddict['base64']['sign']=='-':n.__parseddict['base64']['sign']='+'
            else:n.__parseddict['base64']['sign']='-'
        return n


    # multiplying two numbers: a*b, a*10, a*10.5, a*12e+7
    def __mul__(self,right):
        # multiplication: a*b or b*a (number.Number * number.Number) 
        if dataType(right)==str(__name__)+'.Number':
            # set precision of addition operation
            if self.__max_prec<right.__max_prec:max_prec=right.__max_prec
            else: max_prec=self.__max_prec

            if self.__parseddict['ipart'] not in ['<INF>','<-INF>','<UNDEFINED>']:
                if self.__parseddict['normalized']['ipart']=='0' and self.__parseddict['normalized']['fpart']=='0':
                    if right.__parseddict['ipart']=='<INF>':return Number('<undefined>',10,0,True)
                    elif right.__parseddict['ipart']=='<UNDEFINED>':return Number('<undefined>',10,0,True)
                elif self.__parseddict['sign']=='+':
                    if right.__parseddict['ipart']=='<INF>' and right.__parseddict['sign']=='+':
                        return Number('<inf>',10,0,True)
                    elif right.__parseddict['ipart']=='<INF>' and right.__parseddict['sign']=='-':
                        return Number('<-inf>',10,0,True)
                    elif right.__parseddict['ipart']=='<UNDEFINED>':return Number('<undefined>',10,0,True)
                elif self.__parseddict['sign']=='-':
                    if right.__parseddict['ipart']=='<INF>' and right.__parseddict['sign']=='+':
                        return Number('<-inf>',10,0,True)
                    elif right.__parseddict['ipart']=='<INF>' and right.__parseddict['sign']=='-':
                        return Number('<inf>',10,0,True)
                    elif right.__parseddict['ipart']=='<UNDEFINED>':return Number('<undefined>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+':
                if right.__parseddict['ipart']=='<INF>' and right.__parseddict['sign']=='+':
                    return Number('<inf>',10,0,True)
                elif right.__parseddict['ipart']=='<INF>' and right.__parseddict['sign']=='-':
                    return Number('<-inf>',10,0,True)
                elif right.__parseddict['ipart']=='<UNDEFINED>':return Number('<undefined>',10,0,True)
                else: return Number('<inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-':
                if right.__parseddict['ipart']=='<INF>' and right.__parseddict['sign']=='+':
                    return Number('<-inf>',10,0,True)
                elif right.__parseddict['ipart']=='<INF>' and right.__parseddict['sign']=='-':
                    return Number('<inf>',10,0,True)
                elif right.__parseddict['ipart']=='<UNDEFINED>':return Number('<undefined>',10,0,True)
                else: return Number('<-inf>',10,0,True)
            elif self.__parseddict['ipart']=='<UNDEFINED>': return Number('<undefined>',10)

            # To support fractional multiplication like Number('12 3/4') * Number('7 5/7')
            if self.__parseddict['input_mode']=='fr' and right.__parseddict['input_mode']=='fr'\
                 and self.__parseddict['exp']==0 and right.__parseddict['exp']==0:
                if self.__parseddict['sign']==right.__parseddict['sign']:
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRMultiply(a,b)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        d=_unsignedDenaryFRMultiply(a,right.__parseddict['base10fr'])
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRMultiply(self.__parseddict['base10fr'],b)
                    else:
                        d=_unsignedDenaryFRMultiply(self.__parseddict['base10fr'],right.__parseddict['base10fr'])
                    if d['deno']=='1':return Number(d['ipart'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'], modify=False,ultraModify=False)                         
                    return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                        prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)

                elif self.__parseddict['sign']!=right.__parseddict['sign']:
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRMultiply(a,b)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        d=_unsignedDenaryFRMultiply(a,right.__parseddict['base10fr'])
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRMultiply(self.__parseddict['base10fr'],b)
                    else:
                        d=_unsignedDenaryFRMultiply(self.__parseddict['base10fr'],right.__parseddict['base10fr'])
                    if d['deno']=='1':return Number('-'+d['ipart'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                        prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)

            # To support fractional multiplication like Number('12 3/4') * Number('7')
            elif self.__parseddict['input_mode']=='fr' and right.__parseddict['input_mode']=='fp'\
              and self.__parseddict['exp']==0 and right.__parseddict['exp']==0 and right.__parseddict['fpart']=='0':
                if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                    a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                        'deno':self.__parseddict['deno']}
                    b={'ipart':right.__parseddict['ipart'],'numerator':'0','deno':'1'}
                    d=_unsignedDenaryFRMultiply(a,b)
                elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                    a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                        'deno':self.__parseddict['deno']}
                    b={'ipart':right.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                    d=_unsignedDenaryFRMultiply(a,b)
                elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                    b={'ipart':right.__parseddict['ipart'],'numerator':'0','deno':'1'}
                    d=_unsignedDenaryFRMultiply(self.__parseddict['base10fr'],b)
                else:
                    b={'ipart':right.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                    d=_unsignedDenaryFRMultiply(self.__parseddict['base10fr'],b)
                if self.__parseddict['sign']==right.__parseddict['sign']:
                    return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                elif self.__parseddict['sign']!=right.__parseddict['sign']:
                    return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)

            # to support multiplication like Number('10') * Number('5 3/7') 
            elif self.__parseddict['input_mode']=='fp' and right.__parseddict['input_mode']=='fr'\
              and self.__parseddict['exp']==0 and right.__parseddict['exp']==0 and self.__parseddict['fpart']=='0':
                if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                    a={'ipart':self.__parseddict['ipart'],'numerator':'0','deno':'1'}
                    b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                        'deno':right.__parseddict['deno']}
                    d=_unsignedDenaryFRMultiply(a,b)
                elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                    a={'ipart':self.__parseddict['ipart'],'numerator':'0','deno':'1'}
                    d=_unsignedDenaryFRMultiply(a,right.__parseddict['base10fr'])
                elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                    a={'ipart':self.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                    b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                        'deno':right.__parseddict['deno']}
                    d=_unsignedDenaryFRMultiply(a,b)
                else:
                    a={'ipart':self.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                    d=_unsignedDenaryFRMultiply(a,right.__parseddict['base10fr'])
                if self.__parseddict['sign']==right.__parseddict['sign']:
                    return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                           prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                elif self.__parseddict['sign']!=right.__parseddict['sign']:
                    return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                           prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)

            # To support fractional multiplication like Number('12 3/4') * Number('12.48p-7')
            else:
                if self.__parseddict['sign']==right.__parseddict['sign']:
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        d=_unsignedDenaryMultiply(self.__parseddict['normalized'],right.__parseddict['normalized'])
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        d=_unsignedDenaryMultiply(self.__parseddict['normalized'],right.__parseddict['base10'])
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        d=_unsignedDenaryMultiply(self.__parseddict['base10'],right.__parseddict['normalized'])
                    else:
                        d=_unsignedDenaryMultiply(self.__parseddict['base10'],right.__parseddict['base10'])
                    return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)

                elif self.__parseddict['sign']!=right.__parseddict['sign']:
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        d=_unsignedDenaryMultiply(self.__parseddict['normalized'],right.__parseddict['normalized'])
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        d=_unsignedDenaryMultiply(self.__parseddict['normalized'],right.__parseddict['base10'])
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        d=_unsignedDenaryMultiply(self.__parseddict['base10'],right.__parseddict['normalized'])
                    else:
                        d=_unsignedDenaryMultiply(self.__parseddict['base10'],right.__parseddict['base10'])
                    return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)


        # to support these multiplication: a*50; b*10 (number.Number * denary integer)
        elif dataType(right)=='int':
            max_prec=self.__max_prec

            if self.__parseddict['ipart']=='<INF>' and right==0: return Number('<undefined>',10)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+' and right>0:
                return Number('<inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+' and right<0:
                return Number('<-inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-' and right>0:
                return Number('<-inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-' and right<0:
                return Number('<inf>',10,0,True)
            elif self.__parseddict['ipart']=='<UNDEFINED>': return Number('<undefined>',10,0,True)

            if self.__parseddict['base']==10:
                if self.__parseddict['input_mode']=='fr' and self.__parseddict['exp']==0:
                    if self.__parseddict['sign']=='+' and right>0:
                        d=_unsignedDenaryFRMultiply(self.__parseddict,{'ipart':str(right),'numerator':'0','deno':'1'})
                        if d['deno']=='1':return Number(d['ipart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right<0:
                        d=_unsignedDenaryFRMultiply(self.__parseddict,{'ipart':str(-1*right),\
                            'numerator':'0','deno':'1'})
                        if d['deno']=='1':return Number(d['ipart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right>0:
                        d=_unsignedDenaryFRMultiply(self.__parseddict,{'ipart':str(right),'numerator':'0','deno':'1'})
                        if d['deno']=='1':return Number('-'+d['ipart'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='+' and right<0:
                        d=_unsignedDenaryFRMultiply(self.__parseddict,{'ipart':str(-1*right),
                            'numerator':'0','deno':'1'})
                        if d['deno']=='1':return Number('-'+d['ipart'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif right==0: return Number('0',10,1,True)
 
                else:                    
                    if self.__parseddict['sign']=='+' and right>0:
                        d=_unsignedDenaryMultiply(self.__parseddict['normalized'],{'ipart':str(right),'fpart':'0'})
                        if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                        return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right<0:
                        d=_unsignedDenaryMultiply(self.__parseddict['normalized'],{'ipart':str(-1*right),'fpart':'0'})
                        if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                        return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right>0:
                        d=_unsignedDenaryMultiply(self.__parseddict['normalized'],{'ipart':str(right),'fpart':'0'})
                        if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                        return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='+' and right<0:
                        d=_unsignedDenaryMultiply(self.__parseddict['normalized'],{'ipart':str(-1*right),'fpart':'0'})
                        if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                        return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif right==0: return Number('0',10,1,True)
            elif self.__parseddict['base'] in [2,8,16,32,64]:
                if self.__parseddict['input_mode']=='fr' and self.__parseddict['exp']==0:
                    if self.__parseddict['sign']=='+' and right>0:
                        d=_unsignedDenaryFRMultiply(self.__parseddict['base10fr'],{'ipart':str(right),\
                            'numerator':'0','deno':'1'})
                        if d['deno']=='1':return Number(d['ipart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right<0:
                        d=_unsignedDenaryFRMultiply(self.__parseddict['base10fr'],{'ipart':str(-1*right),\
                            'numerator':'0','deno':'1'})
                        if d['deno']=='1':return Number(d['ipart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right>0:
                        d=_unsignedDenaryFRMultiply(self.__parseddict['base10fr'],{'ipart':str(right),\
                            'numerator':'0','deno':'1'})
                        if d['deno']=='1':return Number('-'+d['ipart'],10,\
                            prec=prec,modify=False,ultraModify=False)
                        return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='+' and right<0:
                        d=_unsignedDenaryFRMultiply(self.__parseddict['base10fr'],{'ipart':str(-1*right),\
                            'numerator':'0','deno':'1'})
                        if d['deno']=='1':return Number('-'+d['ipart'],10,\
                            prec=prec,modify=False,ultraModify=False)
                        return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif right==0: return Number('0',10,1,True)
                else:
                    if self.__parseddict['sign']=='+' and right>0:
                        d=_unsignedDenaryMultiply(self.__parseddict['base10'],{'ipart':str(right),'fpart':'0'})
                        if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                        return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right<0:
                        d=_unsignedDenaryMultiply(self.__parseddict['base10'],{'ipart':str(-1*right),'fpart':'0'})
                        if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                        return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right>0:
                        d=_unsignedDenaryMultiply(self.__parseddict['base10'],{'ipart':str(right),'fpart':'0'})
                        if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                        return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='+' and right<0:
                        d=_unsignedDenaryMultiply(self.__parseddict['base10'],{'ipart':str(-1*right),'fpart':'0'})
                        if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                        return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif right==0: return Number('0',10,1,True)

        # to support these multiplications: a*50.25; b*10.0124; c*12e15 etc (number.Number * denary float)
        elif dataType(right)=='float':
            rdict=_normalizeDenary(right)
            max_prec=self.__max_prec

            if self.__parseddict['ipart']=='<INF>' and right==0.0: return Number('<undefined>',10)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+' and right>0:
                return Number('<inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+' and right<0:
                return Number('<-inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-' and right>0:
                return Number('<-inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-' and right<0:
                return Number('<inf>',10,0,True)
            elif self.__parseddict['ipart']=='<UNDEFINED>': return Number('<undefined>',10,0,True)

            if self.__parseddict['base']==10:
                if self.__parseddict['sign']==rdict['sign']:
                    d=_unsignedDenaryMultiply(self.__parseddict['normalized'],rdict)
                    if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                    return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                elif self.__parseddict['sign']!=rdict['sign']:
                    d=_unsignedDenaryMultiply(self.__parseddict['normalized'],rdict)
                    if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                    return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)
            elif self.__parseddict['base'] in [2,8,16,32,64]:
                if self.__parseddict['sign']==rdict['sign']:
                    d=_unsignedDenaryMultiply(self.__parseddict['base10'],rdict)
                    if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                    return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                elif self.__parseddict['sign']!=rdict['sign']:
                    d=_unsignedDenaryMultiply(self.__parseddict['base10'],rdict)
                    if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                    return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)

        else: raise TypeError("Invalid operand of the operator '*'")
            

    # left multiplication:10*a or 10.25*a (left * self)
    def __rmul__(self,left):	# multiplication:10*a	
        if dataType(left) in ['int','float',str(__name__)+'.Number']:return self.__mul__(left)
        else:raise TypeError("Invalid operand of the operator '*'")


    # dividing two numbers: a/b, a/10, a/10.5, a/12e+7
    def __truediv__(self,right):
        # division: a/b or b/a (number.Number / number.Number) 
        if dataType(right)==str(__name__)+'.Number':
            # set precision of addition operation
            if self.__max_prec<right.__max_prec:max_prec=right.__max_prec
            else: max_prec=self.__max_prec

            if self.__parseddict['ipart'] not in ['<INF>','<-INF>','<UNDEFINED>']:
                if self.__parseddict['normalized']['ipart']=='0' and self.__parseddict['normalized']['fpart']=='0':
                    if right.__parseddict['ipart']=='<INF>':return Number('0',10,1,True)
                    elif right.__parseddict['ipart']=='<UNDEFINED>':return Number('<undefined>',10,0,True)
                    elif right.__parseddict['ipart']=='0' and right.__parseddict['fpart']=='0':
                        return Number('<undefined>',10,0,True)
                else:
                    if right.__parseddict['ipart']=='<INF>':return Number('0',10,1,True)
                    elif right.__parseddict['ipart']=='<UNDEFINED>':return Number('<undefined>',10,0,True)
                    elif right.__parseddict['ipart']=='0' and right.__parseddict['fpart']=='0':
                        if self.__parseddict['sign']=='+': return Number('<inf>',10,0,True)
                        elif self.__parseddict['sign']=='-': return Number('<-inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+':
                if right.__parseddict['ipart']=='<INF>':return Number('<undefined>',10,0,True)
                elif right.__parseddict['ipart']=='<UNDEFINED>':return Number('<undefined>',10,0,True)
                else:
                    if right.__parseddict['sign']=='+': return Number('<inf>',10,0,True)
                    elif right.__parseddict['sign']=='-': return Number('<-inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-':
                if right.__parseddict['ipart']=='<INF>':return Number('<undefined>',10,0,True)
                elif right.__parseddict['ipart']=='<UNDEFINED>':return Number('<undefined>',10,0,True)
                else:
                    if right.__parseddict['sign']=='+': return Number('<-inf>',10,0,True)
                    elif right.__parseddict['sign']=='-': return Number('<inf>',10,0,True)
            elif self.__parseddict['ipart']=='<UNDEFINED>': return Number('<undefined>',10,0,True)

            if right.__parseddict['ipart']=='0' and right.__parseddict['fpart']=='0':
                if self.__parseddict['ipart']=='0' and self.__parseddict['fpart']=='0':
                    return Number('<undefined>',self.__parseddict['base'],0,True)
                elif self.__parseddict['sign']=='+':return Number('<inf>',self.__parseddict['base'],0,True)
                elif self.__parseddict['sign']=='-':return Number('<-inf>',self.__parseddict['base'],0,True)

            # To support division like Number('8 3/5') / Number('3 2/7')
            if self.__parseddict['input_mode']=='fr' and right.__parseddict['input_mode']=='fr'\
                 and self.__parseddict['exp']==0 and right.__parseddict['exp']==0:
                if self.__parseddict['sign']==right.__parseddict['sign']:
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRDivision(a,b)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        d=_unsignedDenaryFRDivision(a,right.__parseddict['base10fr'])
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRDivision(self.__parseddict['base10fr'],b)
                    else:
                        d=_unsignedDenaryDivision(self.__parseddict['base10fr'],right.__parseddict['base10fr'])
                    if d['deno']=='1':return Number(d['ipart'],10,prec=max_prec-6,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)                        
                    return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                        prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)

                elif self.__parseddict['sign']!=right.__parseddict['sign']:
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRDivision(a,b)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        d=_unsignedDenaryFRDivision(a,right.__parseddict['base10fr'])
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRDivision(self.__parseddict['base10fr'],b)
                    else:
                        d=_unsignedDenaryFRDivision(self.__parseddict['base10fr'],right.__parseddict['base10fr'])
                    if d['deno']=='1':return Number('-'+d['ipart'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                        prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)

            # To support fractional multiplication like Number('12 3/4') / Number('7')
            elif self.__parseddict['input_mode']=='fr' and right.__parseddict['input_mode']=='fp'\
              and self.__parseddict['exp']==0 and right.__parseddict['exp']==0 and right.__parseddict['fpart']=='0':
                if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                    a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                        'deno':self.__parseddict['deno']}
                    b={'ipart':right.__parseddict['ipart'],'numerator':'0','deno':'1'}
                    d=_unsignedDenaryFRDivision(a,b)
                elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                    a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                        'deno':self.__parseddict['deno']}
                    b={'ipart':right.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                    d=_unsignedDenaryFRDivision(a,b)
                elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                    b={'ipart':right.__parseddict['ipart'],'numerator':'0','deno':'1'}
                    d=_unsignedDenaryFRDivision(self.__parseddict['base10fr'],b)
                else:
                    b={'ipart':right.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                    d=_unsignedDenaryFRDivision(self.__parseddict['base10fr'],b)
                if self.__parseddict['sign']==right.__parseddict['sign']:
                    return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                        prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                elif self.__parseddict['sign']!=right.__parseddict['sign']:
                    return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                        prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)

            # to support multiplication like Number('10') / Number('5 3/7') 
            elif self.__parseddict['input_mode']=='fp' and right.__parseddict['input_mode']=='fr'\
              and self.__parseddict['exp']==0 and right.__parseddict['exp']==0 and self.__parseddict['fpart']=='0':
                if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                    a={'ipart':self.__parseddict['ipart'],'numerator':'0','deno':'1'}
                    b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                        'deno':right.__parseddict['deno']}
                    d=_unsignedDenaryFRDivision(a,b)
                elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                    a={'ipart':self.__parseddict['ipart'],'numerator':'0','deno':'1'}
                    d=_unsignedDenaryFRDivision(a,right.__parseddict['base10fr'])
                elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                    a={'ipart':self.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                    b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                        'deno':right.__parseddict['deno']}
                    d=_unsignedDenaryFRDivision(a,b)
                else:
                    a={'ipart':self.__parseddict['base10']['ipart'],'numerator':'0','deno':'1'}
                    d=_unsignedDenaryFRDivision(a,right.__parseddict['base10fr'])
                if self.__parseddict['sign']==right.__parseddict['sign']:
                    return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                        prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                elif self.__parseddict['sign']!=right.__parseddict['sign']:
                    return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                        prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)

            # To support division like Number('8 3/5') / Number('3.27')
            else:
                if right.__parseddict['normalized']['ipart']=='0' and right.__parseddict['normalized']['fpart']=='0':
                    if self.__parseddict['sign']==right.__parseddict['sign']: 
                        return Number('<inf>',right.__parseddict['base'],0,True)
                    elif self.__parseddict['sign']!=right.__parseddict['sign']: 
                        return Number('<-inf>',right.__parseddict['base'],0,True)
                if self.__parseddict['sign']==right.__parseddict['sign']:
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        d=_unsignedDenaryDivision(self.__parseddict['normalized'],\
                            right.__parseddict['normalized'],prec=max_prec)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        d=_unsignedDenaryDivision(self.__parseddict['normalized'],\
                            right.__parseddict['base10'],prec=max_prec)
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        d=_unsignedDenaryDivision(self.__parseddict['base10'],\
                            right.__parseddict['normalized'],prec=max_prec)
                    else:
                        d=_unsignedDenaryDivision(self.__parseddict['base10'],right.__parseddict['base10'],prec=max_prec)
                    return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)

                elif self.__parseddict['sign']!=right.__parseddict['sign']:
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        d=_unsignedDenaryDivision(self.__parseddict['normalized'],\
                            right.__parseddict['normalized'],prec=max_prec)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        d=_unsignedDenaryDivision(self.__parseddict['normalized'],\
                            right.__parseddict['base10'],prec=max_prec)
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        d=_unsignedDenaryDivision(self.__parseddict['base10'],\
                            right.__parseddict['normalized'],prec=max_prec)
                    else:
                        d=_unsignedDenaryDivision(self.__parseddict['base10'],right.__parseddict['base10'],prec=max_prec)
                    return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)

        # to support these divisions: a/50; b/10 (number.Number / denary integer)
        elif dataType(right)=='int':
            max_prec=self.__max_prec
            if self.__parseddict['base10']['ipart']=='0' and self.__parseddict['base10']['fpart']=='0' and right==0:
                return Number('<undefined>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+' and right==0:
                return Number('<inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-' and right==0:
                return Number('<-inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+' and right>0:
                return Number('<inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+' and right<0:
                return Number('<-inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-' and right>0:
                return Number('<-inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-' and right<0:
                return Number('<inf>',10,0,True)
            elif self.__parseddict['ipart']=='<UNDEFINED>': return Number('<undefined>',10,0,True)

            if right==0:
                if self.__parseddict['base10']['ipart']=='0' and self.__parseddict['base10']['fpart']=='0':
                    return Number('<undefined>',self.__parseddict['base'],0,True)
                elif self.__parseddict['sign']=='+':return Number('<inf>',self.__parseddict['base'],0,True)
                elif self.__parseddict['sign']=='-':return Number('<-inf>',self.__parseddict['base'],0,True)

            if self.__parseddict['base']==10:
                if self.__parseddict['input_mode']=='fr' and self.__parseddict['exp']==0:
                    if self.__parseddict['sign']=='+' and right>0:
                        d=_unsignedDenaryFRDivision(self.__parseddict,{'ipart':str(right),'numerator':'0','deno':'1'})
                        if d['deno']=='1':return Number(d['ipart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right<0:
                        d=_unsignedDenaryFRDivision(self.__parseddict,{'ipart':str(-1*right),\
                            'numerator':'0','deno':'1'})
                        if d['deno']=='1':return Number(d['ipart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right>0:
                        d=_unsignedDenaryFRDivision(self.__parseddict,{'ipart':str(right),'numerator':'0','deno':'1'})
                        if d['deno']=='1':return Number('-'+d['ipart'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='+' and right<0:
                        d=_unsignedDenaryFRDivision(self.__parseddict,{'ipart':str(-1*right),\
                            'numerator':'0','deno':'1'})
                        if d['deno']=='1':return Number('-'+d['ipart'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif right==0:
                        if self.__parseddict['sign']=='+':return Number('<inf>',10,0,True)
                        elif self.__parseddict['sign']=='-':return Number('<-inf>',10,0,True)
                else: 
                    if self.__parseddict['sign']=='+' and right>0:
                        d=_unsignedDenaryDivision(self.__parseddict['normalized'],{'ipart':str(right),'fpart':'0'},prec=max_prec)
                        if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                        return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right<0:
                        d=_unsignedDenaryDivision(self.__parseddict['normalized'],{'ipart':str(-1*right),'fpart':'0'},prec=max_prec)
                        if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                        return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right>0:
                        d=_unsignedDenaryDivision(self.__parseddict['normalized'],{'ipart':str(right),'fpart':'0'},prec=max_prec)
                        if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                        return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='+' and right<0:
                        d=_unsignedDenaryDivision(self.__parseddict['normalized'],{'ipart':str(-1*right),'fpart':'0'},prec=max_prec)
                        if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                        return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif right==0: 
                        if self.__parseddict['sign']=='+':return Number('<inf>',10,0,True)
                        elif self.__parseddict['sign']=='-':return Number('<-inf>',10,0,True)
            elif self.__parseddict['base'] in [2,8,16,32,64]:
                if self.__parseddict['input_mode']=='fr' and self.__parseddict['exp']==0:
                    if self.__parseddict['sign']=='+' and right>0:
                        d=_unsignedDenaryFRDivision(self.__parseddict['base10fr'],{'ipart':str(right),\
                            'numerator':'0','deno':'1'})
                        if d['deno']=='1':return Number(d['ipart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right<0:
                        d=_unsignedDenaryFRDivision(self.__parseddict['base10fr'],{'ipart':str(-1*right),\
                            'numerator':'0','deno':'1'})
                        if d['deno']=='1':return Number(d['ipart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right>0:
                        d=_unsignedDenaryFRDivision(self.__parseddict['base10fr'],{'ipart':str(right),\
                            'numerator':'0','deno':'1'})
                        if d['deno']=='1':return Number('-'+d['ipart'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='+' and right<0:
                        d=_unsignedDenaryFRDivision(self.__parseddict['base10fr'],{'ipart':str(-1*right),\
                            'numerator':'0','deno':'1'})
                        if d['deno']=='1':return Number('-'+d['ipart'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif right==0:
                        if self.__parseddict['sign']=='+':
                            return Number('<inf>',self.__parseddict['base'],0,True)
                        elif self.__parseddict['sign']=='-':
                            return Number('<-inf>',self.__parseddict['base'],0,True)
                else:
                    if self.__parseddict['sign']=='+' and right>0:
                        d=_unsignedDenaryDivision(self.__parseddict['base10'],{'ipart':str(right),'fpart':'0'},prec=max_prec)
                        if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                        return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right<0:
                        d=_unsignedDenaryDivision(self.__parseddict['base10'],{'ipart':str(-1*right),'fpart':'0'},prec=max_prec)
                        if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                        return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right>0:
                        d=_unsignedDenaryDivision(self.__parseddict['base10'],{'ipart':str(right),'fpart':'0'},prec=max_prec)
                        if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                        return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='+' and right<0:
                        d=_unsignedDenaryDivision(self.__parseddict['base10'],{'ipart':str(-1*right),'fpart':'0'},prec=max_prec)
                        if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                        return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif right==0:
                        if self.__parseddict['sign']=='+':
                            return Number('<inf>',self.__parseddict['base'],0,True)
                        elif self.__parseddict['sign']=='-':
                            return Number('<-inf>',self.__parseddict['base'],0,True)

        # to support these divisions: a/50.25; b/10.0124; c/12e15 etc (number.Number / denary float)
        elif dataType(right)=='float':
            rdict=_normalizeDenary(right)
            max_prec=self.__max_prec

            if self.__parseddict['ipart']=='0' and self.__parseddict['fpart']=='0' and right==0.0:
                return Number('<undefined>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+' and right==0.0:
                return Number('<inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-' and right==0.0:
                return Number('<-inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+' and right>0.0:
                return Number('<inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+' and right<0.0:
                return Number('<-inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-' and right>0.0:
                return Number('<-inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-' and right<0.0:
                return Number('<inf>',10,0,True)
            elif self.__parseddict['ipart']=='<UNDEFINED>': return Number('<undefined>',10,0,True)

            if rdict['ipart']=='0' and rdict['fpart']=='0':
                if self.__parseddict['ipart']=='0' and self.__parseddict['fpart']=='0':
                    return Number('<undefined>',self.__parseddict['base'],0,True)
                elif self.__parseddict['sign']=='+':return Number('<inf>',self.__parseddict['base'],0,True)
                elif self.__parseddict['sign']=='-':return Number('<-inf>',self.__parseddict['base'],0,True)

            if self.__parseddict['base']==10:
                if self.__parseddict['sign']==rdict['sign']:
                    d=_unsignedDenaryDivision(self.__parseddict['normalized'],rdict,prec=max_prec)
                    if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                    return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                elif self.__parseddict['sign']!=rdict['sign']:
                    d=_unsignedDenaryDivision(self.__parseddict['normalized'],rdict,prec=max_prec)
                    if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                    return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)
            elif self.__parseddict['base'] in [2,8,16,32,64]:
                if self.__parseddict['sign']==rdict['sign']:
                    d=_unsignedDenaryDivision(self.__parseddict['base10'],rdict,prec=max_prec)
                    if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                    return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                elif self.__parseddict['sign']!=rdict['sign']:
                    d=_unsignedDenaryDivision(self.__parseddict['base10'],rdict,prec=max_prec-6)
                    if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                    return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)
        else: raise TypeError("Invalid operand of the operator '/'")
            

    # left division:10/a or 10.25/a (left / self)
    def __rtruediv__(self,left):
        # to support these divisions: 50/a; 10/b (denary integer / number.Number)
        if dataType(left)=='int':
            max_prec=self.__max_prec + len(str(left))
            
            if self.__parseddict['ipart']=='<INF>': return Number('0',10,1,True)
            elif self.__parseddict['ipart']=='<UNDEFINED>': return Number('<undefined>',10,0,True)

            if self.__parseddict['normalized']['ipart']=='0' and self.__parseddict['normalized']['fpart']=='0'\
                                   and self.__parseddict['normalized']['sign']=='+':
                if left > 0:return Number('<inf>',10,0,True)
                elif left < 0:return Number('<-inf>',10,0,True)
                elif left == 0:return Number('<undefined>',10,0,True)
            elif self.__parseddict['normalized']['ipart']=='0' and self.__parseddict['normalized']['fpart']=='0'\
                                   and self.__parseddict['normalized']['sign']=='-':
                if left > 0:return Number('<-inf>',10,0,True)
                elif left < 0:return Number('<inf>',10,0,True)
                elif left == 0:return Number('<undefined>',10,0,True)

            if self.__parseddict['base']==10:
                if self.__parseddict['input_mode']=='fr' and self.__parseddict['exp']==0:
                    if self.__parseddict['sign']=='+' and left>0:
                        d=_unsignedDenaryFRDivision({'ipart':str(left),'numerator':'0','deno':'1'},self.__parseddict)
                        if d['deno']=='1':return Number(d['ipart'],10,prec=prec,modify=False,ultraModify=False)
                        return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and left<0:
                        d=_unsignedDenaryFRDivision({'ipart':str(-1*left),\
                            'numerator':'0','deno':'1'},self.__parseddict)
                        if d['deno']=='1':return Number(d['ipart'],10,prec=prec,modify=False,ultraModify=False)
                        return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and left>0:
                        d=_unsignedDenaryFRDivision({'ipart':str(left),'numerator':'0','deno':'1'},self.__parseddict)
                        if d['deno']=='1':return Number('-'+d['ipart'],10,\
                            prec=self.__prec,modify=False,ultraModify=False)
                        return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='+' and left<0:
                        d=_unsignedDenaryFRDivision({'ipart':str(-1*left),\
                            'numerator':'0','deno':'1'},self.__parseddict)
                        if d['deno']=='1':return Number('-'+d['ipart'],10,\
                            prec=prec,modify=False,ultraModify=False)
                        return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif left==0: return Number('0',10,1,True)
 
                else:                    
                    if self.__parseddict['sign']=='+' and left>0:
                        d=_unsignedDenaryDivision({'ipart':str(left),'fpart':''},self.__parseddict['normalized'],prec=max_prec)
                        if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                        return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and left<0:
                        d=_unsignedDenaryDivision({'ipart':str(-1*left),'fpart':''},self.__parseddict['normalized'],prec=max_prec)
                        if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                        return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and left>0:
                        d=_unsignedDenaryDivision({'ipart':str(left),'fpart':''},self.__parseddict['normalized'],prec=max_prec)
                        if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                        return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='+' and left<0:
                        d=_unsignedDenaryDivision({'ipart':str(-1*left),'fpart':''},self.__parseddict['normalized'],prec=max_prec)
                        if d['ipart']=='0' and d['fpart']=='0':return Number('0',10,1,True)
                        return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif left==0: return Number('0',10,1,True)
            elif self.__parseddict['base'] in [2,8,16,32,64]:
                if self.__parseddict['input_mode']=='fr' and self.__parseddict['exp']==0:
                    if self.__parseddict['sign']=='+' and left>0:
                        d=_unsignedDenaryFRDivision({'ipart':str(left),'numerator':'0','deno':'1'},\
                            self.__parseddict['base10fr'])
                        if d['deno']=='1':return Number(d['ipart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and left<0:
                        d=_unsignedDenaryFRDivision({'ipart':str(-1*left),'numerator':'0','deno':'1'},\
                            self.__parseddict['base10fr'])
                        if d['deno']=='1':return Number(d['ipart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        return Number(d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and left>0:
                        d=_unsignedDenaryFRDivision({'ipart':str(left),'numerator':'0','deno':'1'},\
                            self.__parseddict['base10fr'])
                        if d['deno']=='1':return Number('-'+d['ipart'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                        return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='+' and left<0:
                        d=_unsignedDenaryFRDivision({'ipart':str(-1*left),'numerator':'0','deno':'1'},\
                            self.__parseddict['base10fr'])
                        if d['deno']=='1':return Number('-'+d['ipart'],10,\
                            prec=self.__prec,modify=False,ultraModify=False)
                        return Number('-'+d['ipart']+' '+d['numerator']+'/'+d['deno'],10,\
                            prec=max_prec,is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif left==0: return Number('0',10,1,True)
                else:
                    if self.__parseddict['sign']=='+' and left>0:
                        d=_unsignedDenaryDivision({'ipart':str(left),'fpart':''},self.__parseddict['base10'],prec=max_prec)
                        if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                        return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and left<0:
                        d=_unsignedDenaryDivision({'ipart':str(-1*left),'fpart':''},self.__parseddict['base10'],prec=max_prec)
                        if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                        return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and left>0:
                        d=_unsignedDenaryDivision({'ipart':str(left),'fpart':''},self.__parseddict['base10'],prec=max_prec)
                        if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                        return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='+' and left<0:
                        d=_unsignedDenaryDivision({'ipart':str(-1*left),'fpart':''},self.__parseddict['base10'],prec=max_prec)
                        if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                        return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                            is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                    elif left==0: return Number('0',10,1,True)

        # to support these divisions: 50.75/a; 10.3/b (denary float / number.Number)
        elif dataType(left)=='float':
            rdict=_normalizeDenary(left)
            max_prec=self.__max_prec

            if self.__parseddict['ipart']=='<INF>': return Number('0',10)
            elif self.__parseddict['ipart']=='<UNDEFINED>': return Number('<undefined>',10,0,True)

            if self.__parseddict['normalized']['ipart']=='0' and self.__parseddict['normalized']['fpart']=='0':
                if left > 0.0:return Number('<inf>',10,0,True)
                elif left < 0.0:return Number('<-inf>',10,0,True)
                elif left == 0.0:return Number('<undefined>',10,0,True)


            if self.__parseddict['base']==10:
                if self.__parseddict['sign']==rdict['sign']:
                    d=_unsignedDenaryDivision(rdict,self.__parseddict['normalized'],prec=max_prec)
                    if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                    return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                elif self.__parseddict['sign']!=rdict['sign']:
                    d=_unsignedDenaryDivision(rdict,self.__parseddict['normalized'],prec=max_prec)
                    if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                    return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)
            elif self.__parseddict['base'] in [2,8,16,32,64]:
                if self.__parseddict['sign']==rdict['sign']:
                    d=_unsignedDenaryDivision(rdict,self.__parseddict['base10'],prec=max_prec)
                    if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                    return Number(d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)
                elif self.__parseddict['sign']!=rdict['sign']:
                    d=_unsignedDenaryDivision(rdict,self.__parseddict['base10'],prec=max_prec)
                    if d['ipart']=='0' and d['fpart']=='':return Number('0',10,1,True)
                    return Number('-'+d['ipart']+'.'+d['fpart'],10,prec=max_prec,\
                        is_accurate=d['is_accurate'],modify=False,ultraModify=False)
        else: raise TypeError("Invalid operand of the operator '/'")


    # dividing two numbers: a//b, a//10, a//10.5, a//12e+7
    def __floordiv__(self,right):
        # division: a//b or b//a (number.Number // number.Number) 
        if dataType(right)==str(__name__)+'.Number':
            # set precision of addition operation
            if self.__max_prec<right.__max_prec:max_prec=right.__max_prec
            else: max_prec=self.__max_prec

            if self.__parseddict['ipart'] not in ['<INF>','<-INF>','<UNDEFINED>']:
                if self.__parseddict['normalized']['ipart']=='0' and self.__parseddict['normalized']['fpart']=='0':
                    if right.__parseddict['ipart']=='<INF>':return Number('0',10,1,True)
                    elif right.__parseddict['ipart']=='<UNDEFINED>':return Number('<undefined>',10,0,True)
                    elif right.__parseddict['ipart']=='0' and right.__parseddict['fpart']=='0':
                        return Number('<undefined>',10,0,True)
                else:
                    if right.__parseddict['ipart']=='<INF>':return Number('0',10,1,True)
                    elif right.__parseddict['ipart']=='<UNDEFINED>':return Number('<undefined>',10,0,True)
                    elif right.__parseddict['ipart']=='0' and right.__parseddict['fpart']=='0':
                        if self.__parseddict['sign']=='+': return Number('<inf>',10,0,True)
                        elif self.__parseddict['sign']=='-': return Number('<-inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+':
                if right.__parseddict['ipart']=='<INF>':return Number('<undefined>',10,0,True)
                elif right.__parseddict['ipart']=='<UNDEFINED>':return Number('<undefined>',10,0,True)
                else:
                    if right.__parseddict['sign']=='+': return Number('<inf>',10,0,True)
                    elif right.__parseddict['sign']=='-': return Number('<-inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-':
                if right.__parseddict['ipart']=='<INF>':return Number('<undefined>',10,0,True)
                elif right.__parseddict['ipart']=='<UNDEFINED>':return Number('<undefined>',10,0,True)
                else:
                    if right.__parseddict['sign']=='+': return Number('<-inf>',10,0,True)
                    elif right.__parseddict['sign']=='-': return Number('<inf>',10,0,True)
            elif self.__parseddict['ipart']=='<UNDEFINED>': return Number('<undefined>',10,0,True)

            if 'normalized' in right.__parseddict.keys() and right.__parseddict['normalized']['ipart']=='0'\
                 and right.__parseddict['normalized']['fpart']=='0':
                 if self.__parseddict['sign']=='+':return Number('<inf>',10,0,True)
                 elif self.__parseddict['sign']=='-':return Number('<-inf>',10,0,True)

            if self.__parseddict['input_mode']=='fr' and right.__parseddict['input_mode']=='fr'\
                 and self.__parseddict['exp']==0 and right.__parseddict['exp']==0:
                if self.__parseddict['sign']==right.__parseddict['sign']:
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRDivision(a,b)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        d=_unsignedDenaryFRDivision(a,right.__parseddict['base10fr'])
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRDivision(self.__parseddict['base10fr'],b)
                    else:
                        d=_unsignedDenaryDivision(self.__parseddict['base10fr'],right.__parseddict['base10fr'])
                    if d['ipart']=='':d['ipart']='0'
                    return Number(d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                        modify=False,ultraModify=False)
                elif self.__parseddict['sign']!=right.__parseddict['sign']:
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRDivision(a,b)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        a={'ipart':self.__parseddict['ipart'],'numerator':self.__parseddict['numerator'],\
                            'deno':self.__parseddict['deno']}
                        d=_unsignedDenaryFRDivision(a,right.__parseddict['base10fr'])
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        b={'ipart':right.__parseddict['ipart'],'numerator':right.__parseddict['numerator'],\
                            'deno':right.__parseddict['deno']}
                        d=_unsignedDenaryFRDivision(self.__parseddict['base10fr'],b)
                    else:
                        d=_unsignedDenaryFRDivision(self.__parseddict['base10fr'],right.__parseddict['base10fr'])
                    if d['ipart']=='':d['ipart']='0'
                    return Number('-'+d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                        modify=False,ultraModify=False)

            else:
                if self.__parseddict['sign']==right.__parseddict['sign']:
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        d=_unsignedDenaryDivision(self.__parseddict['normalized'],right.__parseddict['normalized'],prec=max_prec)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        d=_unsignedDenaryDivision(self.__parseddict['normalized'],right.__parseddict['base10'],prec=max_prec)
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        d=_unsignedDenaryDivision(self.__parseddict['base10'],right.__parseddict['normalized'],prec=max_prec)
                    else:
                        d=_unsignedDenaryDivision(self.__parseddict['base10'],right.__parseddict['base10'],prec=max_prec)
                    if d['ipart']=='':d['ipart']='0'
                    return Number(d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                        modify=False,ultraModify=False)

                elif self.__parseddict['sign']!=right.__parseddict['sign']:
                    if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                        d=_unsignedDenaryDivision(self.__parseddict['normalized'],right.__parseddict['normalized'],prec=max_prec)
                    elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                        d=_unsignedDenaryDivision(self.__parseddict['normalized'],right.__parseddict['base10'],prec=max_prec)
                    elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                        d=_unsignedDenaryDivision(self.__parseddict['base10'],right.__parseddict['normalized'],prec=max_prec)
                    else:
                        d=_unsignedDenaryDivision(self.__parseddict['base10'],right.__parseddict['base10'],prec=max_prec)
                    if d['ipart']=='':d['ipart']='0'
                    return Number('-'+d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                        modify=False,ultraModify=False)


        # to support these divisions: a//50; b//10 (number.Number // denary integer)
        elif dataType(right)=='int':
            max_prec=self.__max_prec

            if self.__parseddict['ipart']=='0' and self.__parseddict['fpart']=='0' and right==0:
                return Number('<undefined>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+' and right==0:
                return Number('<inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-' and right==0:
                return Number('<-inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+' and right>0:
                return Number('<inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+' and right<0:
                return Number('<-inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-' and right>0:
                return Number('<-inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-' and right<0:
                return Number('<inf>',10,0,True)
            elif self.__parseddict['ipart']=='<UNDEFINED>': return Number('<undefined>',10,0,True)

            if self.__parseddict['base']==10:
                if self.__parseddict['input_mode']=='fr' and self.__parseddict['exp']==0:
                    if self.__parseddict['sign']=='+' and right>0:
                        d=_unsignedDenaryFRDivision(self.__parseddict,{'ipart':str(right),'numerator':'0','deno':'1'})
                        if d['ipart']=='':d['ipart']='0'
                        return Number(d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right<0:
                        d=_unsignedDenaryFRDivision(self.__parseddict,{'ipart':str(-1*right),\
                            'numerator':'0','deno':'1'})
                        if d['ipart']=='':d['ipart']='0'
                        return Number(d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right>0:
                        d=_unsignedDenaryFRDivision(self.__parseddict,{'ipart':str(right),'numerator':'0','deno':'1'})
                        if d['ipart']=='':d['ipart']='0'
                        return Number('-'+d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='+' and right<0:
                        d=_unsignedDenaryFRDivision(self.__parseddict,{'ipart':str(-1*right),\
                            'numerator':'0','deno':'1'})
                        if d['ipart']=='':d['ipart']='0'
                        return Number('-'+d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif right==0: #raise ValueError("Trying to divide by zero.")
                        if self > 0.0:return Number('<inf>',10,0,True)
                        elif self < 0.0:return Number('<-inf>',10,0,True)
 
                else:                    
                    if self.__parseddict['sign']=='+' and right>0:
                        d=_unsignedDenaryDivision(self.__parseddict['normalized'],{'ipart':str(right),'fpart':'0'},prec=max_prec)
                        if d['ipart']=='':d['ipart']='0'
                        return Number(d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right<0:
                        d=_unsignedDenaryDivision(self.__parseddict['normalized'],{'ipart':str(-1*right),'fpart':'0'},prec=max_prec)
                        if d['ipart']=='':d['ipart']='0'
                        return Number(d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right>0:
                        d=_unsignedDenaryDivision(self.__parseddict['normalized'],{'ipart':str(right),'fpart':'0'},prec=max_prec)
                        if d['ipart']=='':d['ipart']='0'
                        return Number('-'+d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='+' and right<0:
                        d=_unsignedDenaryDivision(self.__parseddict['normalized'],{'ipart':str(-1*right),'fpart':'0'},prec=max_prec)
                        if d['ipart']=='':d['ipart']='0'
                        return Number('-'+d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif right==0: #raise ValueError("Trying to divide by zero.")
                        if self > 0.0:return Number('<inf>',10,0,True)
                        elif self < 0.0:return Number('<-inf>',10,0,True)
            elif self.__parseddict['base'] in [2,8,16,32,64]:
                if self.__parseddict['input_mode']=='fr' and self.__parseddict['exp']==0:
                    if self.__parseddict['sign']=='+' and right>0:
                        d=_unsignedDenaryFRDivision(self.__parseddict['base10fr'],{'ipart':str(right),\
                            'numerator':'0','deno':'1'})
                        if d['ipart']=='':d['ipart']='0'
                        return Number(d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right<0:
                        d=_unsignedDenaryFRDivision(self.__parseddict['base10fr'],{'ipart':str(-1*right),\
                            'numerator':'0','deno':'1'})
                        if d['ipart']=='':d['ipart']='0'
                        return Number(d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right>0:
                        d=_unsignedDenaryFRDivision(self.__parseddict['base10fr'],{'ipart':str(right),\
                            'numerator':'0','deno':'1'})
                        if d['ipart']=='':d['ipart']='0'
                        return Number('-'+d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='+' and right<0:
                        d=_unsignedDenaryFRDivision(self.__parseddict['base10fr'],{'ipart':str(-1*right),\
                            'numerator':'0','deno':'1'})
                        if d['ipart']=='':d['ipart']='0'
                        return Number('-'+d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif right==0: #raise ValueError("Trying to divide by zero.")
                        if self > 0.0:return Number('<inf>',10,0,True)
                        elif self < 0.0:return Number('<-inf>',10,0,True)
                else:
                    if self.__parseddict['sign']=='+' and right>0:
                        d=_unsignedDenaryDivision(self.__parseddict['base10'],{'ipart':str(right),'fpart':'0'},prec=max_prec)
                        if d['ipart']=='':d['ipart']='0'
                        return Number(d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right<0:
                        d=_unsignedDenaryDivision(self.__parseddict['base10'],{'ipart':str(-1*right),'fpart':'0'},prec=max_prec)
                        if d['ipart']=='':d['ipart']='0'
                        return Number(d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and right>0:
                        d=_unsignedDenaryDivision(self.__parseddict['base10'],{'ipart':str(right),'fpart':'0'},prec=max_prec)
                        if d['ipart']=='':d['ipart']='0'
                        return Number('-'+d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='+' and right<0:
                        d=_unsignedDenaryDivision(self.__parseddict['base10'],{'ipart':str(-1*right),'fpart':'0'},prec=max_prec)
                        if d['ipart']=='':d['ipart']='0'
                        return Number('-'+d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif right==0: #raise ValueError("Trying to divide by zero.")
                        if self > 0.0:return Number('<inf>',10,0,True)
                        elif self < 0.0:return Number('<-inf>',10,0,True)

        # to support these divisions: a//50.25; b//10.0124; c//12e15 etc (number.Number // denary float)
        elif dataType(right)=='float':
            rdict=_normalizeDenary(right)
            max_prec=self.__max_prec

            if self.__parseddict['ipart']=='0' and self.__parseddict['fpart']=='0' and right==0.0:
                return Number('<undefined>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+' and right==0.0:
                return Number('<inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-' and right==0.0:
                return Number('<-inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+' and right>0.0:
                return Number('<inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+' and right<0.0:
                return Number('<-inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-' and right>0.0:
                return Number('<-inf>',10,0,True)
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-' and right<0.0:
                return Number('<inf>',10,0,True)
            elif self.__parseddict['ipart']=='<UNDEFINED>': return Number('<undefined>',10,0,True)

            if self.__parseddict['base']==10:
                if self.__parseddict['sign']==rdict['sign']:
                    d=_unsignedDenaryDivision(self.__parseddict['normalized'],rdict,prec=max_prec)
                    if d['ipart']=='':d['ipart']='0'
                    return Number(d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                        modify=False,ultraModify=False)
                elif self.__parseddict['sign']!=rdict['sign']:
                    d=_unsignedDenaryDivision(self.__parseddict['normalized'],rdict,prec=max_prec)
                    if d['ipart']=='':d['ipart']='0'
                    return Number('-'+d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                        modify=False,ultraModify=False)
            elif self.__parseddict['base'] in [2,8,16,32,64]:
                if self.__parseddict['sign']==rdict['sign']:
                    d=_unsignedDenaryDivision(self.__parseddict['base10'],rdict,prec=max_prec)
                    if d['ipart']=='':d['ipart']='0'
                    return Number(d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                        modify=False,ultraModify=False)
                elif self.__parseddict['sign']!=rdict['sign']:
                    d=_unsignedDenaryDivision(self.__parseddict['base10'],rdict,prec=max_prec)
                    if d['ipart']=='':d['ipart']='0'
                    return Number('-'+d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                        modify=False,ultraModify=False)

        else: raise TypeError("Invalid operand of the operator '//'")
            

    # left division:10//a or 10.25//a (left // self)
    def __rfloordiv__(self,left):	
        # to support these divisions: 50//a; 10//b (denary integer // number.Number)
        if dataType(left)=='int':
            max_prec=self.__max_prec

            if self.__parseddict['ipart']=='<INF>': return Number('0',10,1,True)
            elif self.__parseddict['ipart']=='<UNDEFINED>': return Number('<undefined>',10,0,True)

            if 'normalized' in self.__parseddict.keys() and self.__parseddict['normalized']['ipart']=='0'\
                 and self.__parseddict['normalized']['fpart']=='0':
                 if left > 0:return Number('<inf>',10,0,True)
                 elif left < 0:return Number('<-inf>',10,0,True)

            if self.__parseddict['base']==10:
                if self.__parseddict['input_mode']=='fr' and self.__parseddict['exp']==0:
                    if self.__parseddict['sign']=='+' and left>0:
                        d=_unsignedDenaryFRDivision({'ipart':str(left),'numerator':'0','deno':'1'},self.__parseddict)
                        if d['ipart']=='':d['ipart']='0'
                        return Number(d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and left<0:
                        d=_unsignedDenaryFRDivision({'ipart':str(-1*left),\
                            'numerator':'0','deno':'1'},self.__parseddict)
                        if d['ipart']=='':d['ipart']='0'
                        return Number(d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and left>0:
                        d=_unsignedDenaryFRDivision({'ipart':str(left),'numerator':'0','deno':'1'},self.__parseddict)
                        if d['ipart']=='':d['ipart']='0'
                        return Number('-'+d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='+' and left<0:
                        d=_unsignedDenaryFRDivision({'ipart':str(-1*left),\
                            'numerator':'0','deno':'1'},self.__parseddict)
                        if d['ipart']=='':d['ipart']='0'
                        return Number('-'+d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif left==0: return Number('0',10,1,True)
 
                else:
                    if self.__parseddict['sign']=='+' and left>0:
                        d=_unsignedDenaryDivision({'ipart':str(left),'fpart':''},self.__parseddict['normalized'],prec=max_prec)
                        if d['ipart']=='':d['ipart']='0'                        
                        return Number(d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and left<0:
                        d=_unsignedDenaryDivision({'ipart':str(-1*left),'fpart':''},self.__parseddict['normalized'],prec=max_prec)
                        if d['ipart']=='':d['ipart']='0'
                        return Number(d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and left>0:
                        d=_unsignedDenaryDivision({'ipart':str(left),'fpart':''},self.__parseddict['normalized'],prec=max_prec)
                        if d['ipart']=='':d['ipart']='0'
                        return Number('-'+d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='+' and left<0:
                        d=_unsignedDenaryDivision({'ipart':str(-1*left),'fpart':''},self.__parseddict['normalized'],prec=max_prec)
                        if d['ipart']=='':d['ipart']='0'
                        return Number('-'+d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif left==0: return Number('0',10,1,True)
            elif self.__parseddict['base'] in [2,8,16,32,64]:
                if self.__parseddict['input_mode']=='fr' and self.__parseddict['exp']==0:
                    if self.__parseddict['sign']=='+' and left>0:
                        d=_unsignedDenaryFRDivision({'ipart':str(left),'numerator':'0','deno':'1'},\
                            self.__parseddict['base10fr'])
                        if d['ipart']=='':d['ipart']='0'
                        return Number(d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and left<0:
                        d=_unsignedDenaryFRDivision({'ipart':str(-1*left),'numerator':'0','deno':'1'},\
                            self.__parseddict['base10fr'])
                        if d['ipart']=='':d['ipart']='0'
                        return Number(d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and left>0:
                        d=_unsignedDenaryFRDivision({'ipart':str(left),'numerator':'0','deno':'1'},
                            self.__parseddict['base10fr'])
                        if d['ipart']=='':d['ipart']='0'
                        return Number('-'+d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='+' and left<0:
                        d=_unsignedDenaryFRDivision({'ipart':str(-1*left),'numerator':'0','deno':'1'},\
                            self.__parseddict['base10fr'])
                        if d['ipart']=='':d['ipart']='0'
                        return Number('-'+d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif left==0: return Number('0',10,1,True)
                else:
                    if self.__parseddict['sign']=='+' and left>0:
                        d=_unsignedDenaryDivision({'ipart':str(left),'fpart':''},self.__parseddict['base10'],prec=max_prec)
                        if d['ipart']=='':d['ipart']='0'
                        return Number(d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and left<0:
                        d=_unsignedDenaryDivision({'ipart':str(-1*left),'fpart':''},self.__parseddict['base10'],prec=max_prec)
                        if d['ipart']=='':d['ipart']='0'
                        return Number(d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='-' and left>0:
                        d=_unsignedDenaryDivision({'ipart':str(left),'fpart':''},self.__parseddict['base10'],prec=max_prec)
                        if d['ipart']=='':d['ipart']='0'
                        return Number('-'+d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif self.__parseddict['sign']=='+' and left<0:
                        d=_unsignedDenaryDivision({'ipart':str(-1*left),'fpart':''},self.__parseddict['base10'],prec=max_prec)
                        if d['ipart']=='':d['ipart']='0'
                        return Number('-'+d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                            modify=False,ultraModify=False)
                    elif left==0: return Number('0',10,1,True)

        # to support these floor divisions: 50.75//a; 10.3//b (denary float // number.Number)
        elif dataType(left)=='float':
            rdict=_normalizeDenary(left)
            max_prec=self.__max_prec

            if self.__parseddict['ipart']=='<INF>': return Number('0',10,1,True)
            elif self.__parseddict['ipart']=='<UNDEFINED>': return Number('<undefined>',10,0,True)

            if 'normalized' in self.__parseddict.keys() and self.__parseddict['normalized']['ipart']=='0'\
                 and self.__parseddict['normalized']['fpart']=='0':
                 if left > 0.0:return Number('<inf>',10,0,True)
                 elif left < 0.0:return Number('<-inf>',10,0,True)

            if self.__parseddict['base']==10:
                if self.__parseddict['sign']==rdict['sign']:
                    d=_unsignedDenaryDivision(rdict,self.__parseddict['normalized'],prec=max_prec)
                    if d['ipart']=='':d['ipart']='0'
                    return Number(d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                        modify=False,ultraModify=False)
                elif self.__parseddict['sign']!=rdict['sign']:
                    d=_unsignedDenaryDivision(rdict,self.__parseddict['normalized'],prec=max_prec)
                    if d['ipart']=='':d['ipart']='0'
                    return Number('-'+d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                        modify=False,ultraModify=False)
            elif self.__parseddict['base'] in [2,8,16,32,64]:
                if self.__parseddict['sign']==rdict['sign']:
                    d=_unsignedDenaryDivision(rdict,self.__parseddict['base10'],prec=max_prec)
                    if d['ipart']=='':d['ipart']='0'
                    return Number(d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                        modify=False,ultraModify=False)
                elif self.__parseddict['sign']!=rdict['sign']:
                    d=_unsignedDenaryDivision(rdict,self.__parseddict['base10'],prec=max_prec)
                    if d['ipart']=='':d['ipart']='0'
                    return Number('-'+d['ipart'],10,prec=max_prec,is_accurate=d['is_accurate'],\
                        modify=False,ultraModify=False)
        else: raise TypeError("Invalid operand of the operator '//'")


    # remainder operation between two numbers: a%b, a%10, a%10.5, a%12e+7
    def __mod__(self,right):
        if dataType(right) in [str(__name__)+'.Number']:
            if self.__parseddict['ipart']=='<UNDEFINED>' or  right.__parseddict['ipart']=='<UNDEFINED>':
                return UNDEFINED
            elif self.__parseddict['ipart']=='<INF>' and  right.__parseddict['ipart']=='<INF>':
                return UNDEFINED
            elif self.__parseddict['ipart']!='<INF>' and right.__parseddict['ipart']=='<INF>':
                return UNDEFINED
            elif self.__parseddict['ipart']=='<INF>' and right.__parseddict['ipart']!='<INF>':
                return UNDEFINED
            elif self==right: return ZERO
            else: return self-right*(self//right)
        elif dataType(right) in ['int','float']:
            if self.__parseddict['ipart']=='<UNDEFINED>':return UNDEFINED               
            elif self.__parseddict['ipart']=='<INF>':return UNDEFINED                
            elif self==right: return ZERO
            else: return self-right*(self//right)
        else: raise TypeError("Invalid operand of the operator '%'")

    # left division:10%a or 10.25%a (left % self)
    def __rmod__(self,left):
        if dataType(left)==str(__name__)+'.Number':
            if self.__parseddict['ipart']=='<UNDEFINED>' or left.__parseddict['ipart']=='<UNDEFINED>':
                return UNDEFINED
            elif self.__parseddict['ipart']=='<INF>' and left.__parseddict['ipart']=='<INF>':
                return UNDEFINED
            elif self.__parseddict['ipart']!='<INF>' and left.__parseddict['ipart']=='<INF>':
                return UNDEFINED
            elif self.__parseddict['ipart']=='<INF>' and left.__parseddict['ipart']!='<INF>':
                return UNDEFINED 
            elif self==left: return ZERO
            elif self<left: return left-self*(left//self)
        elif dataType(left) in ['int','float']:
            if self.__parseddict['ipart']=='<UNDEFINED>':UNDEFINED                
            elif self.__parseddict['ipart']=='<INF>':return UNDEFINED
            elif self==left: return ZERO
            elif self<left: return left-self*(left//self)
        else: raise TypeError("Invalid operand of the operator '%'")


    # inverse operation: ~a
    def __invert__(self):
        return 1/self.copy()


    # -------------------------- comparison operators --------------------------------------------------
    # comparison operator: equal_to (==); a==b, b==a, a==10, b==10.67
    def __eq__(self,right):
        if right==None:
            if self.__parseddict==None:return True 
            else:return False
        if id(self)==id(right):return True

        # check equality for INF and UNDEFINED where base doesn't matter
        if dataType(self)==str(__name__)+'.Number' and dataType(right)==str(__name__)+'.Number':
            if self.__parseddict['sign']=='+' and self.__parseddict['ipart']=='<INF>':
                if right.__parseddict['sign']=='+' and right.__parseddict['ipart']=='<INF>':return True
                return False
            elif self.__parseddict['sign']=='-' and self.__parseddict['ipart']=='<INF>':
                if right.__parseddict['sign']=='-' and right.__parseddict['ipart']=='<INF>':return True
                return False
            elif self.__parseddict['ipart']=='<UNDEFINED>': return False
                #if right.__parseddict['ipart']=='<UNDEFINED>':return True
                #return False
            elif self.__parseddict['ipart']!='' or self.__parseddict['fpart']!='':
                return False
        elif dataType(self)==str(__name__)+'.Number' and dataType(right) in ['int','float']:
            if self.__parseddict['ipart'] in ['<INF>','<UNDEFINED>']:return False
		
        if self.__parseddict['base']==10:
            if self.__parseddict['normalized']['ipart']=='0':ipart1='0'
            else: ipart1=self.__parseddict['normalized']['ipart']
            if self.__parseddict['normalized']['fpart']=='0':fpart1='0'
            else: fpart1=self.__parseddict['normalized']['fpart']
        elif self.__parseddict['base'] in [2,8,16,32,64]:
            if self.__parseddict['base10']['ipart']=='0':ipart1='0'
            else:ipart1=self.__parseddict['base10']['ipart']
            if self.__parseddict['base10']['fpart']=='0':fpart1='0'
            else: fpart1=self.__parseddict['base10']['fpart']

        if dataType(right)==str(__name__)+'.Number':
            if right.__parseddict['base']==10:
                if right.__parseddict['normalized']['ipart']=='0':ipart2='0'
                else: ipart2=right.__parseddict['normalized']['ipart']
                if right.__parseddict['normalized']['fpart']=='0':fpart2='0'
                else: fpart2=right.__parseddict['normalized']['fpart']
            elif right.__parseddict['base'] in [2,8,16,32,64]:
                if right.__parseddict['base10']['ipart']=='0':ipart2='0'
                else:ipart2=right.__parseddict['base10']['ipart']
                if right.__parseddict['base10']['fpart']=='0':fpart2='0'
                else: fpart2=right.__parseddict['base10']['fpart']

            if self.__parseddict['sign']!=right.__parseddict['sign']:return False
            elif self.__parseddict['sign']==right.__parseddict['sign']:
                if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                    if int(ipart1)==int(ipart2):
                       lf1,lf2=len(fpart1),len(fpart2)
                       if lf1>lf2:fpart2=fpart2+'0'*(lf1-lf2)
                       elif lf1<lf2:fpart1=fpart1+'0'*(lf2-lf1)
                       if int(fpart1)==int(fpart2): return True
                       else: return False 
                    else: return False
                elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                    if int(ipart1)==int(ipart2):
                       lf1,lf2=len(fpart1),len(fpart2)
                       if lf1>lf2:fpart2=fpart2+'0'*(lf1-lf2)
                       elif lf1<lf2:fpart1=fpart1+'0'*(lf2-lf1)
                       if int(fpart1)==int(fpart2): return True
                       else: return False 
                    else: return False
                elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                    if int(ipart1)==int(ipart2):
                       lf1,lf2=len(fpart1),len(fpart2)
                       if lf1>lf2:fpart2=fpart2+'0'*(lf1-lf2)
                       elif lf1<lf2:fpart1=fpart1+'0'*(lf2-lf1)
                       if int(fpart1)==int(fpart2): return True
                       else: return False 
                    else: return False
                elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base'] in [2,8,16,32,64]:
                    if int(ipart1)==int(ipart2):
                       lf1,lf2=len(fpart1),len(fpart2)
                       if lf1>lf2:fpart2=fpart2+'0'*(lf1-lf2)
                       elif lf1<lf2:fpart1=fpart1+'0'*(lf2-lf1)
                       if int(fpart1)==int(fpart2): return True
                       else: return False 
                    else: return False

        elif dataType(right)=='int':
            if right==0:
                if self.__parseddict['normalized']['ipart']=='0' and\
                    self.__parseddict['normalized']['fpart']=='0':return True
                else:return False
            elif self.__parseddict['sign']=='+' and  right<0:return False
            elif self.__parseddict['sign']=='-' and  right>0: return False
            elif self.__parseddict['sign']=='+' and  right>0:
                if int(ipart1)==right and fpart1=='0':return True
                else: return False
            elif self.__parseddict['sign']=='-' and  right<0:
                if int(ipart1)==-1*right and fpart1=='0':return True
                else: return False

        elif dataType(right)=='float':
            if right==0.0:
                if self.__parseddict['normalized']['ipart']=='0' and\
                    self.__parseddict['normalized']['fpart']=='0':return True
                else:return False
            rdict=_normalizeDenary(right)            
            if self.__parseddict['sign']!=rdict['sign']:return False
            elif self.__parseddict['sign']==rdict['sign']:
                if self.__parseddict['base']==10:
                    if int(ipart1)==int(rdict['ipart']):
                       fpart2=rdict['fpart']
                       lf1,lf2=len(fpart1),len(fpart2)
                       if lf1>lf2:fpart2=fpart2+'0'*(lf1-lf2)
                       elif lf1<lf2:fpart1=fpart1+'0'*(lf2-lf1)
                       if int(fpart1)==int(fpart2): return True
                       else: return False 
                    else: return False
                elif self.__parseddict['base'] in [2,8,16,32,64]:
                    if int(ipart1)==int(rdict['ipart']):
                       fpart2=rdict['fpart']
                       lf1,lf2=len(fpart1),len(fpart2)
                       if lf1>lf2:fpart2=fpart2+'0'*(lf1-lf2)
                       elif lf1<lf2:fpart1=fpart1+'0'*(lf2-lf1)
                       if int(fpart1)==int(fpart2): return True
                       else: return False 
                    else: return False
        else: raise TypeError("Invalid operand of the operator '=='")

    # comparison operator: left equal_to (==); 10==a, 10.67==b
    def __req__(self,left):
        if left==None:
            if self.__parseddict==None:return True 
            else:return False
        if dataType(left) in ['int','float']: return self.__eq__(left)
        else: raise TypeError("Invalid operand of the operator '=='")

    # comparison operator: not equal_to (!=); a!=b, a!=10, a!=10.67
    def __ne__(self,right):
        if right==None:
            if self.__parseddict==None:return False 
            else:return True
        if dataType(right) in [str(__name__)+'.Number']:
            return not self.__eq__(right)
        elif dataType(right) in ['int','float']:           
            return not self.__eq__(right)
        else: raise TypeError("Invalid operand of the operator '!='")

    # comparison operator: left not equal_to (!=); 10!=a, 10.67!=a
    def __rne__(self,left):
        if left==None:
            if self.__parseddict==None:return False 
            else:return True
        if self.__parseddict['ipart']=='<INF>' or self.__parseddict['ipart']=='<UNDEFINED>':
            return True
        if dataType(left) in ['int','float']: return not self.__eq__(left)
        else: raise TypeError("Invalid operand of the operator '!='")

    # comparison operator: greater_than (>); a>b, b>a, a>10, b>10.67
    def __gt__(self,right):
        if right==None:raise Exception("Invalid comparison")

        if dataType(right) in ['int','float'] and self.__parseddict['ipart'] in ['INF','<UNDEFINED>']:
            if self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+': return True
            elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-':return False
            elif self.__parseddict['ipart']=='<UNDEFINED>':return False
        elif dataType(right) in [str(__name__)+'.Number']:
            if right.__parseddict['ipart']=='<INF>':
                if right.__parseddict['sign']=='+':return False
                elif right.__parseddict['sign']=='-':return True
            elif self.__parseddict['ipart']=='<INF>' and right.__parseddict['ipart']=='<INF>':
                if self.__parseddict['sign']=='+' and right.__parseddict['sign']=='-':return True
                else: return False
            elif self.__parseddict['ipart']=='<UNDEFINED>':return False
            elif right.__parseddict['ipart']=='<UNDEFINED>':return False
 
        if self.__parseddict['base']==10:
            ipart1,fpart1=self.__parseddict['normalized']['ipart'],self.__parseddict['normalized']['fpart']
        elif self.__parseddict['base'] in [2,8,16,32,64]:
            ipart1,fpart1=self.__parseddict['base10']['ipart'],self.__parseddict['base10']['fpart']


        if dataType(right)==str(__name__)+'.Number':
            if right.__parseddict['base']==10:
                if right.__parseddict['normalized']['ipart']=='0':ipart2='0'
                else: ipart2=right.__parseddict['normalized']['ipart']
                if right.__parseddict['normalized']['fpart']=='0':fpart2='0'
                else: fpart2=right.__parseddict['normalized']['fpart']
            elif right.__parseddict['base'] in [2,8,16,32,64]:
                if right.__parseddict['base10']['ipart']=='0':ipart2='0'
                else:ipart2=right.__parseddict['base10']['ipart']
                if right.__parseddict['base10']['fpart']=='0':fpart2='0'
                else: fpart2=right.__parseddict['base10']['fpart']
            #print(self.__parseddict)
            if self.__parseddict['sign']=='+' and  right.__parseddict['sign']=='-':return True
            elif self.__parseddict['sign']=='-' and  right.__parseddict['sign']=='+': return False
            elif self.__parseddict['sign']=='+' and  right.__parseddict['sign']=='+':
                if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                    if int(ipart1)>int(ipart2):
                        return True
                    elif int(ipart1)<int(ipart2):
                        return False
                    else:
                       lf1,lf2=len(fpart1),len(fpart2)
                       if lf1>lf2:fpart2=fpart2+'0'*(lf1-lf2)
                       elif lf1<lf2:fpart1=fpart1+'0'*(lf2-lf1)
                       if int(fpart1)>int(fpart2): return True
                       else: return False
                elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:
                    if int(ipart1)>int(ipart2):
                        return True
                    elif int(ipart1)<int(ipart2):
                        return False
                    else:
                       lf1,lf2=len(fpart1),len(fpart2)
                       if lf1>lf2:fpart2=fpart2+'0'*(lf1-lf2)
                       elif lf1<lf2:fpart1=fpart1+'0'*(lf2-lf1)
                       if int(fpart1)>int(fpart2): return True
                       else: return False
                elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                    if int(ipart1)>int(ipart2):
                        return True
                    elif int(ipart1)<int(ipart2):
                        return False
                    else:
                       lf1,lf2=len(fpart1),len(fpart2)
                       if lf1>lf2:fpart2=fpart2+'0'*(lf1-lf2)
                       elif lf1<lf2:fpart1=fpart1+'0'*(lf2-lf1)
                       if int(fpart1)>int(fpart2): return True
                       else: return False
                elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base'] in [2,8,16,32,64]:
                    if int(ipart1)>int(ipart2):
                        return True
                    elif int(ipart1)<int(ipart2):
                        return False
                    else:
                       lf1,lf2=len(fpart1),len(fpart2)
                       if lf1>lf2:fpart2=fpart2+'0'*(lf1-lf2)
                       elif lf1<lf2:fpart1=fpart1+'0'*(lf2-lf1)
                       if int(fpart1)>int(fpart2): return True
                       else: return False

            elif self.__parseddict['sign']=='-' and  right.__parseddict['sign']=='-':
                if self.__parseddict['base']==10 and right.__parseddict['base']==10:
                    if int(ipart1)>int(ipart2):
                        return False
                    elif int(ipart1)<int(ipart2):
                        return True
                    else:
                       lf1,lf2=len(fpart1),len(fpart2)
                       if lf1>lf2:fpart2=fpart2+'0'*(lf1-lf2)
                       elif lf1<lf2:fpart1=fpart1+'0'*(lf2-lf1)
                       if int(fpart1)<int(fpart2): return True
                       else: return False
                elif self.__parseddict['base']==10 and right.__parseddict['base'] in [2,8,16,32,64]:                    
                    if int(ipart1)>int(ipart2):
                        return False
                    elif int(ipart1)<int(ipart2):
                        return True
                    else:
                       lf1,lf2=len(fpart1),len(fpart2)
                       if lf1>lf2:fpart2=fpart2+'0'*(lf1-lf2)
                       elif lf1<lf2:fpart1=fpart1+'0'*(lf2-lf1)
                       if int(fpart1)<int(fpart2): return True
                       else: return False
                elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base']==10:
                    if int(ipart1)>int(ipart2):
                        return False
                    elif int(ipart1)<int(ipart2):
                        return True
                    else:
                       lf1,lf2=len(fpart1),len(fpart2)
                       if lf1>lf2:fpart2=fpart2+'0'*(lf1-lf2)
                       elif lf1<lf2:fpart1=fpart1+'0'*(lf2-lf1)
                       if int(fpart1)<int(fpart2): return True
                       else: return False
                elif self.__parseddict['base'] in [2,8,16,32,64] and right.__parseddict['base'] in [2,8,16,32,64]:
                    if int(ipart1)>int(ipart2):
                        return False
                    elif int(ipart1)<int(ipart2):
                        return True
                    else:
                       lf1,lf2=len(fpart1),len(fpart2)
                       if lf1>lf2:fpart2=fpart2+'0'*(lf1-lf2)
                       elif lf1<lf2:fpart1=fpart1+'0'*(lf2-lf1)
                       if int(fpart1)<int(fpart2): return True
                       else: return False

        elif dataType(right)=='int':
            if right==0:
                if self.__parseddict['normalized']['ipart']=='0' and self.__parseddict['normalized']['fpart']=='0':return False
                elif self.__parseddict['sign']=='+':return True
                elif self.__parseddict['sign']=='-':return False
            elif self.__parseddict['sign']=='+' and  right<0:return True
            elif self.__parseddict['sign']=='-' and  right>0: return False
            elif self.__parseddict['sign']=='+' and  right>0:
                if self.__parseddict['base']==10:
                    if int(ipart1) > right: return True                        
                    elif int(ipart1) < right: return False
                    else:
                       if fpart1 not in ['','0']: return True
                       else: return False
                elif self.__parseddict['base'] in [2,8,16,32,64]:
                    if int(ipart1) > right: return True                        
                    elif int(ipart1) < right: return False
                    else:
                       if fpart1 not in ['','0']: return True
                       else: return False
            elif self.__parseddict['sign']=='-' and  right<0:
                if self.__parseddict['base']==10:
                    if int(ipart1) > -1*right: return False                       
                    elif int(ipart1) < -1*right: return True
                    else:
                       if fpart1 in ['','0']: return False
                       else: return True
                elif self.__parseddict['base'] in [2,8,16,32,64]:
                    if int(ipart1) > -1*right: return False                        
                    elif int(ipart1) < -1*right: return True
                    else:
                       if fpart1 in ['','0']: return False
                       else: return True

        elif dataType(right)=='float':
            print('hello2')
            rdict=_normalizeDenary(right)            
            if self.__parseddict['sign']=='+' and  rdict['sign']=='-':return True
            elif self.__parseddict['sign']=='-' and  rdict['sign']=='+': return False
            elif self.__parseddict['sign']=='+' and  rdict['sign']=='+':
                if self.__parseddict['base']==10:
                    if int(ipart1) > int(rdict['ipart']): return True
                    elif int(ipart1) < int(rdict['ipart']): return False
                    else:
                       fpart2=rdict['fpart']
                       lf1,lf2=len(fpart1),len(fpart2)
                       if lf1>lf2:fpart2=fpart2+'0'*(lf1-lf2)
                       elif lf1<lf2:fpart1=fpart1+'0'*(lf2-lf1)
                       if int(fpart1)>int(fpart2): return True
                       else: return False
                elif self.__parseddict['base'] in [2,8,16,32,64]:
                    if int(ipart1) > int(rdict['ipart']): return True
                    elif int(ipart1) < int(rdict['ipart']): return False
                    else:
                       fpart2=rdict['fpart']
                       lf1,lf2=len(fpart1),len(fpart2)
                       if lf1>lf2:fpart2=fpart2+'0'*(lf1-lf2)
                       elif lf1<lf2:fpart1=fpart1+'0'*(lf2-lf1)
                       if int(fpart1)>int(fpart2): return True
                       else: return False
            elif self.__parseddict['sign']=='-' and  rdict['sign']=='-':
                if self.__parseddict['base']==10:
                    if int(ipart1) > int(rdict['ipart']): return False
                    elif int(ipart1) < int(rdict['ipart']): return True
                    else:
                       fpart2=rdict['fpart']
                       lf1,lf2=len(fpart1),len(fpart2)
                       if lf1>lf2:fpart2=fpart2+'0'*(lf1-lf2)
                       elif lf1<lf2:fpart1=fpart1+'0'*(lf2-lf1)
                       if int(fpart1)<int(fpart2): return True
                       else: return False
                elif self.__parseddict['base'] in [2,8,16,32,64]:
                    if int(ipart1) > int(rdict['ipart']): return False
                    elif int(ipart1) < int(rdict['ipart']): return True
                    else:
                       fpart2=rdict['fpart']
                       lf1,lf2=len(fpart1),len(fpart2)
                       if lf1>lf2:fpart2=fpart2+'0'*(lf1-lf2)
                       elif lf1<lf2:fpart1=fpart1+'0'*(lf2-lf1)
                       if int(fpart1)<int(fpart2): return True
                       else: return False
        else: raise TypeError("Invalid operand of the operator '>'")

    # comparison operator: left greater_than (>); 10>a, 10.67>b
    def __rgt__(self,left):
        if left==None:raise Exception("Invalid comparison")

        if self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+':return False
        elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-':return True
        elif self.__parseddict['ipart']=='<UNDEFINED>':return False

        if dataType(left) in ['int','float']:
            if self>left:return False
            elif self==left:return False
            else:return True
        else: raise TypeError("Invalid operand of the operator '>'")


    # comparison operator: less_than (<); a<b, a<10, a<10.67
    def __lt__(self,right):
        if right==None:raise Exception("Invalid comparison")

        if self.__parseddict['ipart']=='<UNDEFINED>': return False
        elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+':
            if dataType(right) in ['int','float']: return False
            elif dataType(right) in [str(__name__)+'.Number']:
                if right.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+': return False
                elif right.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-':return False
                elif right.__parseddict['ipart']=='<UNDEFINED>':return False
                else: return False
        elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-':
            if dataType(right) in ['int','float']: return True
            elif dataType(right) in [str(__name__)+'.Number']:
                if right.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+': return True
                elif right.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-':return False
                elif right.__parseddict['ipart']=='<UNDEFINED>':return False
                else: return True

        if dataType(right) in ['int','float']:
            if self==right:return False
            elif self>right:return False
            else:return True
        elif dataType(right) in [str(__name__)+'.Number']:
            if self==right:return False
            elif self>right:return False
            else:return True
        else: raise TypeError("Invalid operand of the operator '<'")

    # comparison operator: less_than (<); 10<a, 10.67<a
    def __rlt__(self,left):
        if right==None:raise Exception("Invalid comparison")

        if self.__parseddict['ipart']=='<UNDEFINED>': return False
        elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+': return True
        elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-': return False

        if dataType(left) in ['int','float']:
            if self==left:return False
            elif self>left:return True
            else:return False
        else: raise TypeError("Invalid operand of the operator '<'")

    # comparison operator: less_than or equal_to (<); a<=b, a<=10, a<=10.67
    def __le__(self,right):
        if right==None:raise Exception("Invalid comparison")

        if self.__parseddict['ipart']=='<UNDEFINED>': return False
        elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+':
            if dataType(right) in ['int','float']: return False
            elif dataType(right) in [str(__name__)+'.Number']:
                if right.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+': return False
                elif right.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-':return False
                elif right.__parseddict['ipart']=='<UNDEFINED>':return False
                else: return False
        elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-':
            if dataType(right) in ['int','float']: return True
            elif dataType(right) in [str(__name__)+'.Number']:
                if right.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+': return True
                elif right.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-':return False
                elif right.__parseddict['ipart']=='<UNDEFINED>':return False
                else: return True

        if dataType(right) in ['int','float']:
            if self==right:return True
            elif self>right:return False
            else:return True
        elif dataType(right)==str(__name__)+'.Number':
            if right.__parseddict['ipart']=='<UNDEFINED>':return False
            elif right.__parseddict['ipart']=='<INF>' and right.__parseddict['sign']=='+': return True
            elif right.__parseddict['ipart']=='<INF>' and right.__parseddict['sign']=='-': return False
            elif self==right:return True
            elif self>right:return False
            else:return True
        else: raise TypeError("Invalid operand of the operator '<='")

    # comparison operator: less_than or equal_to (<); a<=b, 10<=a, 10.67<=a
    def __rle__(self,left):
        if dataType(left) in ['int','float']:
            if self==left:return True
            elif self>right:return False
            else:return True
        else: raise TypeError("Invalid operand of the operator '<='")

    # comparison operator: greater_than or equal_to (>=); a>=b, a>=10, a>=10.67
    def __ge__(self,right):
        if right==None:raise Exception("Invalid comparison")

        if self.__parseddict['ipart']=='<UNDEFINED>': return False
        elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+':
            if dataType(right) in ['int','float']: return True
            elif dataType(right) in [str(__name__)+'.Number']:
                if right.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+': return False
                elif right.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-':return True
                elif right.__parseddict['ipart']=='<UNDEFINED>':return False
                else: return True
        elif self.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-':
            if dataType(right) in ['int','float']: return False
            elif dataType(right) in [str(__name__)+'.Number']:
                if right.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='+': return False
                elif right.__parseddict['ipart']=='<INF>' and self.__parseddict['sign']=='-':return False
                elif right.__parseddict['ipart']=='<UNDEFINED>':return False
                else: return False

        if dataType(right) in ['int','float']:
            if self==right:return True
            elif self>right:return True
            else:return False
        elif dataType(right)==str(__name__)+'.Number':
            if right.__parseddict['ipart']=='<UNDEFINED>':return False
            elif right.__parseddict['ipart']=='<INF>' and right.__parseddict['sign']=='+': return False
            elif right.__parseddict['ipart']=='<INF>' and right.__parseddict['sign']=='-': return True
            elif self==right:return True
            elif self>right:return True
            else:return False
        else: raise TypeError("Invalid operand of the operator '>='")

    # comparison operator: less_than or equal_to (>=); a>=b, 10>=a, 10.67>=a
    def __rge__(self,left):
        if dataType(left) in ['int','float']:
            if self==left:return True
            elif self>left:return True
            else:return False
        else: raise TypeError("Invalid operand of the operator '>='")

    # -------------------------- in-place operators --------------------------------------------------
    # in-place addition operator (+=): a+=b, a+=10, a+=14.75e+7
    def __iadd__(self,right):
        if dataType(right) in [str(__name__)+'.Number','int','float']:
            return self+right 
        else: raise TypeError("Invalid operand of the operator '+='")

    # in-place subtraction operator (-=): a-=b, a-=10, a-=14.75e+7
    def __isub__(self,right):
        if dataType(right) in [str(__name__)+'.Number','int','float']:
            return self-right
        else: raise TypeError("Invalid operand of the operator '-='")

    # in-place multiplication operator (*=): a*=b, a*=10, a*=14.75e+7
    def __imul__(self,right):
        if dataType(right) in [str(__name__)+'.Number','int','float']:
            return self*right 
        else: raise TypeError("Invalid operand of the operator '*='")

    # in-place true division operator (/=): a/=b, a/=10, a/=14.75e+7
    def __itruediv__(self,right):
        if dataType(right) in [str(__name__)+'.Number','int','float']:
            return self/right 
        else: raise TypeError("Invalid operand of the operator '/='")

    # in-place floor division operator (//=): a//=b, a//=10, a//=14.75e+7
    def __ifloordiv__(self,right):
        if dataType(right) in [str(__name__)+'.Number','int','float']:
            return self//right
        else: raise TypeError("Invalid operand of the operator '//='")

    # in-place mod/remainder operator (%=): a%=b, a%=10, a%=14.75e+7
    def __imod__(self,right):
        if dataType(right) in [str(__name__)+'.Number','int','float']:
            return self%right
        else: raise TypeError("Invalid operand of the operator '%='")






    
	# --------------------- new addition to version upmath-1.3.1 --------------------------
    # Number type conversion
    # int(x) returns denary integer value of x
    def __int__(self):
        if self.__parseddict['ipart'] in ['<INF>','<UNDEFINED>']:
	        raise ValueError("Invalid value for int()")
        return int(self.__parseddict['sign']+self.__parseddict['base10']['ipart'])

    # float(x) returns denary float value of x
    def __float__(self):
        if self.__parseddict['ipart'] in ['<INF>','<UNDEFINED>']:
            raise ValueError("Invalid value for float()")
        return float(self.__parseddict['sign']+self.__parseddict['base10']['ipart']+'.'+self.__parseddict['base10']['fpart'])


    # floor() returns the denary floor value of x when calling by x.floor()
    def floor(self):
        if self.__parseddict['ipart'] in ['<INF>','<UNDEFINED>']:
            raise ValueError("Invalid value for int()")
        if self.__parseddict['base10']['fpart']=='0':
            return int(self.__parseddict['sign']+self.__parseddict['base10']['ipart'])
        elif self.__parseddict['base10']['fpart']!='0':
            if self.__parseddict['sign']=='+':
                return int(self.__parseddict['sign']+self.__parseddict['base10']['ipart'])
            elif self.__parseddict['sign']=='-':
                return int(self.__parseddict['sign']+self.__parseddict['base10']['ipart'])-1
				
    # __floor__() returns the denary floor value of x when calling by math.floor(x)
    def __floor__(self):
        return self.floor()


    # ceil() returns the denary ceiling value of x when calling by x.ceil()
    def ceil(self):
        if self.__parseddict['ipart'] in ['<INF>','<UNDEFINED>']:
	        raise ValueError("Invalid value for int()")
        if self.__parseddict['base10']['fpart']=='0':
            return int(self.__parseddict['sign']+self.__parseddict['base10']['ipart'])
        elif self.__parseddict['base10']['fpart']!='0':
            if self.__parseddict['sign']=='+':
                return int(self.__parseddict['sign']+self.__parseddict['base10']['ipart'])+1
            elif self.__parseddict['sign']=='-':
                return int(self.__parseddict['sign']+self.__parseddict['base10']['ipart'])

    # __ceil__() returns the denary ceiling value of x when calling by math.ceil(x)
    def __ceil__(self):
        return self.ceil()

    # __round__(dp) returns the rounded denary value truncated at the given decimal point
    def __round__(self,dp=0):
        if dataType(dp)!='int' or dp<0:
            raise ValueError("Invalid decimal point value where to be truncated")
		
        if dp==0 or self.__parseddict['base10']['fpart']=='0': # return integer part
            return int(self.__parseddict['sign']+self.__parseddict['base10']['ipart'])
        dfpart=self.__parseddict['base10']['fpart'] # denary floating part
        if len(dfpart)<=dp:		
            return float(self.__parseddict['sign']+self.__parseddict['base10']['ipart']+'.'+dfpart)
        else:
            if dfpart[dp] in ['5','6','7','8','9']:
                last_digit=str(int(dfpart[dp-1])+1)
                dfpart=dfpart[:dp-1]+last_digit
                return float(self.__parseddict['sign']+self.__parseddict['base10']['ipart']+'.'+dfpart)
            else:return float(self.__parseddict['sign']+self.__parseddict['base10']['ipart']+'.'+dfpart[:dp])


    # __pos__() returns the number object when unary + is used like +x
    def __pos__(self):
        return self.copy()


    # __neg__() returns the number object when unary - is used like -x
    def __neg__(self):
        if self.__parseddict['ipart']=='<UNDEFINED>': return UNDEFINED
        return -1*self.copy()


    # representing the number by denary value
    # Rewritten in the new version upmath-1.3.1
    def __repr__(self):
        if self.__parseddict['ipart']=="<UNDEFINED>":return str(UNDEFINED)
        if self.__parseddict['base10']['fpart']=='0':
            if self.__parseddict['sign']=='+':
                if self.__parseddict['ipart']=="<INF>":return str(INF)
                return "b10:"+self.__parseddict['base10']['ipart']
            elif self.__parseddict['sign']=='-':
                if self.__parseddict['ipart']=="<INF>":return str(-INF)
                return "b10:-"+self.__parseddict['base10']['ipart']
        else:
            if self.__parseddict['sign']=='+':
                return "b10:"+self.__parseddict['base10']['ipart']+'.'+self.__parseddict['base10']['fpart']
            if self.__parseddict['sign']=='-':
                return "b10:-"+self.__parseddict['base10']['ipart']+'.'+self.__parseddict['base10']['fpart']



    # __pow__(self,right) returns the value of power operation, x**right (x**4.5)
    def __pow__(self,right):
        if dataType(right) in ['int','float']:
            prec=self.__max_prec
            tmp=power(self.copy(),right,prec)
            return Number(str(tmp)[4:],10,prec,self.__is_accurate)
        elif dataType(right) == str(__name__)+'.Number':
            prec=max(self.__max_prec,right.__max_prec)
            tmp=power(self,right.copy(),prec)
            return Number(str(tmp)[4:],10,self.__max_prec,self.__is_accurate)
        elif dataType(right)==str(__name__)+'.Number':
            prec=max(self.__max_prec,right.__max_prec)
            tmp=power(self,right.copy(),prec)
            return Number(str(tmp)[4:],10,self.__max_prec,self.__is_accurate)
        else: raise TypeError("Invalid right operand of the operator '**'")


    # power operation: a**b, a**3, a**-2.5, a**-3
    def __rpow__(self,left,prec=36):
        if dataType(left) in ['int','float']:
            tmp=power(left,self.copy(),prec)
            return Number(str(tmp)[4:],10,self.getMaxPrecision(),self.isAccurate())
        elif dataType(left)==str(__name__)+'.Number':
            tmp=power(left.copy(),self.copy(),prec)
            return Number(str(tmp)[4:],10,self.getMaxPrecision(),self.isAccurate())
        else: raise TypeError("Invalid operand of the operator '**'")


    # in-place power operator (**=): a**=b, a**=10, a**=14.75e+7
    def __ipow__(self,right):
        if dataType(right) in [str(__name__)+'.Number','int','float']:
            return self**right
        else: raise TypeError("Invalid operand of the operator '%='")











###################### End of Number Class ####################################

# ------------------------- Functions getE(prec) and getPI(prec) --------------------------
# These functions are necessary for power(x,y) function and to avoid circular import

# getE(prec) returns the exponential value of e='exp(1)'
# e=1+1/1!+1/2!+1/3!+...

# >>> t=time.time();pe.getE();time.time()-t
# b10:2.7182818284590452353602874713526625
# 0.015628576278686523 s
# >>> t=time.time();pe.getE(prec=100);time.time()-t
# b10:2.71828182845904523536028747135266249775724709369995957496696762
# 7724076630353547594571382178525166427
# 0.031263113021850586 s
def getE(prec=36):
    if dataType(prec)!='int': prec=36
    delP=Number('1p-'+str(prec),10,prec=prec);
    prec2=prec+4

    SUM=Number('1',10,prec=prec2);
    t1=Number('1',10,prec=prec2);
    i=0 
    while t1>delP:
        t1=t1/(i+1)
        t1.limitFloatingDigits(prec=prec2)
        SUM=SUM+t1
        i=i+1
    return SUM.createNewNumber(prec=prec,is_accurate=False)




# Calculating pi using Bellard's Formula (most efficient formula)
# It takes 14 iterations to produce a number correct to 34 d.p.

# >>> t=time.time();upmath2.mypi.getPI(prec=100);time.time()-t
# b10:3.14159265358979323846264338327950288419716939937510582097494459230781640
# 6286208998628034825342117068
# 0.07861542701721191 s
# >>>
# >>> t=time.time();upmath2.mypi.getPI(prec=50);time.time()-t
# b10:3.1415926535897932384626433832795028841971693993751
# 0.03758668899536133 s
def getPI(prec=36):
    if dataType(prec)!='int': prec=36
    delP=Number('1p-'+str(prec),10,prec=prec)
    prec2=prec+4

    SUM=Number('0',10,prec=prec2);
    t=Number('1.0',10,prec=prec2)
    sign=1;i=0;deno=64

    while(t > delP):        
        a=Number(str(10*i+1),10,prec=prec2)
        b=Number(str(10*i+9),10,prec=prec2)
        c=Number(str(4*i+1),10,prec=prec2)
        d=Number(str(4*i+3),10,prec=prec2)
        e=Number(str(10*i+3),10,prec=prec2)
        f=Number(str(10*i+5),10,prec=prec2)
        g=Number(str(10*i+7),10,prec=prec2)

        t=((256/a)+(1/b)-(32/c)-(1/d)-(64/e)-(4/f)-(4/g))/deno
        deno=deno*1024
        SUM=SUM+sign*t
        sign=-sign
        i=i+1; 
    return SUM.createNewNumber(prec=prec,is_accurate=False)

# ---------------------------- END of getE() and getPI() functions ---------------------------


# Defining Numeric Constants
#=============================
UND=UNDEFINED=Number('<undefined>',10,0,is_accurate=True)
INF=Number('<inf>',10,0,is_accurate=True)
ZERO=Number('0',10,1,is_accurate=True)
ONE=Number('1',10,1,is_accurate=True)
e=E=getE(prec=36)
pi=PI=getPI(prec=36)



# --------- ln2(),ln10(),ln(x),exp(x) functions to be used in __pow__() function ----------------
# ----------------------- logarithmic function -----------------------------
# ln2(prec) returns the natural logarithm of ln(2) correct to the 
# given precision value
# ln2(100)=0.6931471805599453094172321214581765680755001343602552541206
#            800094933936219696947156058633269964186875

# it takes 0.04687 s in 64 bit system for 100 prec
def ln2(prec=36):
    if dataType(prec)!='int' or prec<1: prec=36
    delP=Number('1p-'+str(prec),10,prec=prec)
    prec2=prec+4	

    SUM=Number('0.0',10,prec=prec2);
    t=Number('1.0',10,prec=prec2)
    i=0;m=1
    while(t >= delP):        
        t=Number(str(3*(2*i+1)*m),base=10,prec=prec2)
        t=2/t;
        SUM=SUM+t
        m=m*9; i=i+1
    return SUM.createNewNumber(prec2,False)

# ln3(prec) returns the natural logarithm of ln(3) correct to the 
# given precision value
# ln3(100)=1.098612288668109691395245236922525704647490557822749451
#            734694333637494293218608966873615754813732089

# it takes 0.04687 s in 64 bit system for 100 prec
def ln3(prec=36):
    if dataType(prec)!='int' or prec<1: prec=36
    delP=Number('1p-'+str(prec),10,prec=prec)
    prec2=prec+4	

    SUM=Number('0',10,prec=prec2);
    t=Number('1.0',10,prec=prec2)
    i=0;m=2
    while(t > delP):
        t=1/Number(str(m*(2*i+1)),10,prec=prec2)
        SUM=SUM+t
        m=m*4;i=i+1
    SUM=2*SUM
    return SUM.createNewNumber(prec2,False)
	
	
# ln10(prec) returns the natural logarithm of ln(10) correct to the 
# given precision value
# ln10(100)=2.3025850929940456840179914546843642076011014886287729760
#            33327900967572609677352480235997205089598298

# it takes 0.08495 s in 64 bit system for 100 prec
def ln10(prec=36):
    if dataType(prec)!='int' or prec<1: prec=36
    delP=Number('1p-'+str(prec),10,prec=prec)
    prec2=prec+4	

    SUM=Number('0.0',10,prec=prec2);
    t=Number('1.0',10,prec=prec2)  #term of the series
    r=1  #loop count

    while(abs(t)>delP):        
        t=Number(str((-1)**(r+1)))/Number(str(r*4**r),10,prec=prec2)		
        SUM=SUM+t
        #if t<0:t=-t
        r=r+1
    SUM=SUM+3*ln2(prec=prec)
    return SUM.createNewNumber(prec2,False)


# ----------------------------- start of ln() -----------------------------------
# ln(x,prec) calculates the natural logarithm of an 'upNumber' x
# correct to the given precision by calling _ln(x,prec) or __ln(x,prec)
def ln(x=None,prec=36):
    if x==None:raise ValueError("Invalid arguement of ln(x,prec).")
    if dataType(prec)!='int' or prec<0: prec=36
    if dataType(x) not in ['int','float',str(__name__)+'.Number']:
        raise ValueError("Invalid argument of function ln(x,prec)")
    if dataType(prec)!='int' or prec<1: prec=36

	# convert to denary if x not denary
    if x.getBase() in [2,8,16,32,64]:
        numstr=x.getDict()['base10']['sign']+x.getDict()['base10']['ipart']+'.'+x.getDict()['base10']['fpart']
        x=Number(numstr,10,x.getDict()['base10_prec'],False)
    elif x.getBase()==10:
        if dataType(x) in ['int','float']: x=Number(str(x),base=10,prec=prec,is_accurate=True)
    else: raise ValueError("Invalid base of x in ln(x)")	

    prec2=prec+4

    if x==0:return Number('<-inf>',10,0,is_accurate=True)
    elif x<0:return Number('<undefined>',10,0,is_accurate=True)
    elif x==1:return Number('0',base=10,prec=1,is_accurate=True)
    elif x==2:return ln2(prec2)
    elif x==e or x==E:return Number('1',base=10,prec=1,is_accurate=True)
    elif x==3:return ln3(prec2)
    elif x==4:return ln2(prec2)*2
    elif x==8:return ln2(prec2)*3
    elif x==9:return ln3(prec2)*2
    elif x==10:return ln10(prec2)
    elif x==16:return ln2(prec2)*4
    elif x==27:return ln3(prec2)*3
    elif x==32:return ln2(prec2)*5
    elif x==64:return ln2(prec2)*6
    elif x==81:return ln3(prec2)*4
    elif x==100:return ln10(prec2)*2

    delP=Number('1p-'+str(prec),10,prec=prec,is_accurate=True)	

	# Reducing the number by using exponential form
    # ln(a.b p**d)=ln(a.b)+d*ln(p)	p=10 for denary numbers
    # ln(a b/c p**d)=ln(a b/c)+d*ln(p)	p=10 for denary numbers
    addme=Number('0',10,prec,True)
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
            if x==1: return addme.createNewNumber(prec2,is_accurate=False)
        elif len(ipart) > 1:
            addme=(len(ipart)-1)*ln10(prec2)
            reduced_x_str=ipart[0]+"."+ipart[1:]
            x=Number(reduced_x_str,10,prec2,is_accurate=True)
            if x==1:return addme.createNewNumber(prec2,is_accurate=False)    
    elif x.isFloat():
        if ipart!='0':
            if len(ipart)>1:
                reduced_x_str=ipart[0]+"."+ipart[1:]+fpart	
                x=Number(reduced_x_str,10,prec2,is_accurate=True)
                addme=(len(ipart)-1)*ln10(prec2);
        else:
            i=0;
            while fpart[i]=='0':i=i+1
            reduced_x_str=fpart[i]+"."+fpart[i+1:]
            x=Number(reduced_x_str,10,prec2,is_accurate=True)
            addme=-(i+1)*ln10(prec2);
    # x=2^n*a; ln(x)=nln(2) + ln(a); x between 1 and 9
    n=0;
    while(x>1):
        x=x/2
        n=n+1;
    addme=addme+(n*ln2(prec2))
    if x==1 or x==1.0:return addme.createNewNumber(prec2,is_accurate=False)

    # Finding ln(reduced_x) where 1<x<2
    # ln(1+x)=x/1 - x**2/2 + x**3/3 - x**4/4 + ...
    delP=Number('1p-'+str(prec),10,prec=prec)
    x=x-1
    SUM=x #Sum upto the first term
    t=x # First Term
    t1=Number('1.0',10,prec=prec2)    
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
    return SUM.createNewNumber(prec2,is_accurate=False)

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
    if dataType(x) not in ['int','float',str(__name__)+".Number"]:
        raise ValueError("Invalid argument in function exp(x,prec)")

    if dataType(x) in ['int','float']: x=Number(str(x),base=10,prec=prec,is_accurate=True)	
	# convert to denary if x not denary
    if x.getBase() in [2,8,16,32,64]:
        numstr=x.getDict()['base10']['sign']+x.getDict()['base10']['ipart']+'.'+x.getDict()['base10']['fpart']
        x=Number(numstr,10,x.getDict()['base10_prec'],False)
    elif x.getBase()==10:
        if dataType(x) in ['int','float']: x=Number(str(x),base=10,prec=prec,is_accurate=True)
    else: raise ValueError("Invalid base of x in exp(x)")

    prec2=prec+6
	
    if x==0: return Number('1',10,prec=prec,is_accurate=True)
    elif x==1 or x==1.0: return pE.getE(prec2)
    elif x==-1 or x==-1.0: return (1/pE.getE(prec)).createNewNumber(prec2,is_accurate=False)

    delP=Number('1p-'+str(prec),10,prec=prec);    
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
        t1=Number(str((2+4*i)*y),base=10,prec=prec2)
        t2=Number(str((6+4*i)*y),base=10,prec=prec2)
        return (t1+x*x/t2).createNewNumber(prec2,is_accurate=False)

    # converting x to x/y; where y=1
    i=prec2//4;
    while True:
        deno=denoFunc(x,1,i,prec2)
        for j in range(i,0,-1):
            deno=Number(str(2+4*j),base=10,prec=prec2,is_accurate=False)+x*x/deno
        num1=1+(2*x/(2-x+(x*x/deno)))
        i=i+1
        deno=denoFunc(x,1,i,prec2)
        for j in range(i,0,-1):
            deno=Number(str(2+4*j),base=10,prec=prec2,is_accurate=False)+x*x/deno
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
    return result.createNewNumber(prec2,is_accurate=False)


# ---------------------- end of exponential functions --------------------------

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
    if dataType(x) not in ['int','float',str(__name__)+".Number"]:
        raise ValueError("Invalid argument in function power(x,y,prec)")
    if dataType(y) not in ['int','float',str(__name__)+".Number"]:
        raise ValueError("Invalid argument in function power(x,y,prec)")

    if dataType(x) in ['int','float']:x=Number(str(x),10,prec,True)
    if dataType(y) in ['int','float']:y=Number(str(y),10,prec,True)

	# convert to denary if x, y not denary
    if x.getBase() in [2,8,16,32,64]:
        numstr=x.getDict()['base10']['sign']+x.getDict()['base10']['ipart']+'.'+x.getDict()['base10']['fpart']
        x=Number(numstr,10,x.getDict()['base10_prec'],False)
    elif x.getBase()==10:
        if dataType(x) in ['int','float']: x=Number(str(x),base=10,prec=prec,is_accurate=True)
    else: raise ValueError("Invalid base of x in power(x,y)")
	
	# convert to denary if y not denary
    if y.getBase() in [2,8,16,32,64]:
        numstr=y.getDict()['base10']['sign']+y.getDict()['base10']['ipart']+'.'+y.getDict()['base10']['fpart']
        y=Number(numstr,10,y.getDict()['base10_prec'],False)
    elif y.getBase()==10:
        if dataType(y) in ['int','float']: y=Number(str(y),base=10,prec=prec,is_accurate=True)
    else: raise ValueError("Invalid base")

    # handling exceptional cases ('inf','undefined')
    if x==UNDEFINED or y == UNDEFINED:return UNDEFINED
    elif x==0 and y==0: return UNDEFINED
    elif x==0 and y>0: return ZERO
    elif x==0 and y<0: return INF
    elif x==INF and y>0: return INF
    elif x==INF and y<0: return ZERO
    elif x==INF and y==0: return UNDEFINED
    elif x==-INF: return UNDEFINED
    elif x!=INF and y==INF: return INF
    elif x!=INF and y==-INF:return ZERO
     
    # handling 0, 1 cases
    if x==1: return Number('1',10,prec,True)            
    elif y==0: return Number('1',10,prec,True)
    elif y==1: return x.createNewNumber(prec,is_accurate=False)

    prec2=prec+6
    prod=Number('1',10,prec2,True)
    if y.isInteger():  # base x can be positive or negative
        if y>0:
            for i in range(int(y)):
                prod=prod*x;
                if prod.getMaxPrecision()>prec2: prod=prod.createNewNumber(prec2,is_accurate=False)
            return prod.createNewNumber(prec,is_accurate=False)
        elif y<0:
            y1=-y
            for i in range(int(y1)):
                prod=prod*x;
                if prod.getMaxPrecision()>prec2: prod=prod.createNewNumber(prec2,is_accurate=False)
            return (1/prod).createNewNumber(prec,is_accurate=False)
    elif y.isFloat() and x<0: return UNDEFINED
    elif y.isFloat() and x>0:
        # x^y=x^(m+0.n)=x^m*x^0.n=x^m*e^(0.n*lnx)
        prod1=Number('1',10,prec2,True)
        prod2=Number('1',10,prec2,True)
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





