## upmath-2.0.0 (universal precision mathematics)

**Description:** This python package contains a number class that supports 
high precision calculation and various number-bases like **2**, **8**, **10**, **16**, 
**32** and **64**. Numbers are correct to the precision level (significant digits) set 
by the user. Numbers of different bases are equivalent and interconvertible. 
Converting a number to a higher base saves memory space and reduces load on network traffic 
when a number is sent from one machine to another over the computer network.

Both the integers and floating point numbers are supported by all the numbers of 
mentioned bases. Since these numbers support binary, octal, denary, hexadecimal, base-32 
and base-64 numbers equivalently, that's why, they are called *'universal'* precisional
 numbers. 

All the standard mathematical functions are rewritten to support the high precision
calculations. Mathematical operators are also redefined accordingly. That's why, this package 
is called universal precision mathematics (upmath).

The latest package (version 2.0.0) is more faster and efficient.

### Features of upmath-2.0.0
1. Very fast and accurate calculations upto the set precision
2. Floating point binary, octal, hexadecimal, base32 and base64 numbers are supported
3. Mixed fractional numbers are also supported
4. Supported Math Operators: 
```python
   +(add), -(subtract), *(multiply), /(division), //(floor division), %(modulus 
   or remainder operation), **(power operation), ~(invertion), ==(equal to),
   !=(not equal to), >(greater than), >=(greater than or equal to), <(less than), 
   <(less than or equal to), +(unart positive), -(unary negative), +=(add and assign), 
   -=(subtract and assign), *=(multiply and assign), /=(divide and assign), 
   //=(floor division and assign), %=(find remainder and assign), **=(find power, 
   then assign) 
```
5. **Recurring decimals** can be converted to fractions quickly and automatically
6. Mathematical Constants: **E**, **PI**, **INF**, **ZERO**, **ONE** and **UNDEFINED**
7. Common Mathematical Functions: 
```python
		fact(n), nCr(n,r), nPr(n,r), ln(x,prec), logE(x,y), lg(x,prec), log10(x,prec), 
		exp(x,prec), power(x,y,prec), sqrt(x,prec)
```
8. Trigonometric Functions:  
```python
    sin(x,prec), cos(x,prec), tan(x,prec), cot(x,prec), sec(x,prec), csc(x,prec),
    cosec(x,prec), asin(x,prec), acos(x,prec), atan(x,prec), acot(x,prec), asec(x,prec), 
	acsc(x,prec), acosec(x,prec)
```
9. Hyperbolic Functions:  
```python
        sinh(x,prec), cosh(x,prec), tanh(x,prec), coth(x,prec), sech(x,prec),
        csch(x,prec), cosech(x,prec), asinh(x,prec), acosh(x,prec), atanh(x,prec), 
		acoth(x,prec), asech(x,prec), acsch(x,prec), acosech(x,prec)
```
10. Other Standard Functions: 
```python
gamma(x,prec), beta(x,y,prec), erf(x,prec), erfc(x,prec)```
```
11. Precision calculation of E and PI:
```python
getE(prec), getPI(prec)
```
12. Numbers of Number Theory: 
```python 
eulerNumber(n), bernoilliNumber(n), tangentNumber(n)
```
13. Methods and properties of upnumber (universal precision number)
```python
>>>
>>> a=lib.Number('11001.101',base=2)
>>> a;print(a)
b10:25.625
b02:11001.101
>>> dir(a)
['_Number__base', '_Number__base10_prec', '_Number__is_accurate', '_Number__is_numeric', 
'_Number__max_prec', '_Number__modify', '_Number__normal_prec', '_Number__num', 
'_Number__parseddict', '_Number__prec', '_Number__ultra_modify', '__abs__', '__add__', 
'__ceil__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', 
'__float__', '__floor__', '__floordiv__', '__format__', '__ge__', '__getattribute__', 
'__getstate__', '__gt__', '__hash__', '__iadd__', '__ifloordiv__', '__imod__', '__imul__', 
'__init__', '__init_subclass__', '__int__', '__invert__', '__ipow__', '__isub__', 
'__itruediv__', '__le__', '__lt__', '__mod__', '__module__', '__mul__', '__ne__', 
'__neg__', '__new__', '__pos__', '__pow__', '__radd__', '__reduce__', '__reduce_ex__', 
'__repr__', '__req__', '__rfloordiv__', '__rge__', '__rgt__', '__rle__', '__rlt__', 
'__rmod__', '__rmul__', '__rne__', '__round__', '__rpow__', '__rsub__', '__rtruediv__', 
'__setattr__', '__sizeof__', '__str__', '__sub__', '__subclasshook__', '__truediv__', 
'__weakref__', 'addBase64Form', 'ceil', 'copy', 'createNewNumber', 'denaryFPtoFRMode', 
'displayInFPMode', 'floor', 'forceResetPrecision', 'getAccuracy', 'getBase', 
'getBase10Part', 'getBase10Precision', 'getBase10frPart', 'getBase32Form', 'getBase64Form', 
'getBinaryForm', 'getDenaryForm', 'getDenominator', 'getDict', 'getExponent', 
'getFloatingPart', 'getHexadecimalForm', 'getInputMode', 'getIntegerPart', 
'getMaxPrecision', 'getNormalPrecision', 'getNormalizedForm', 'getNormalizedPart', 
'getNumerator', 'getOctalForm', 'getOriginal', 'getPrecision', 'getScientificForm', 
'getSign', 'isAbs', 'isAccurate', 'isBase32Number', 'isBase64Number', 'isBinary', 'isDenary', 
'isFloat', 'isFractional', 'isHexadecimal', 'isInteger', 'isNegative', 'isNumeric', 
'isOctal', 'isPositive', 'isPrime', 'isRecurring', 'limitFloatingDigits', 'modify', 
'setMaxPrecision', 'toDenaryInteger', 'ultraModify']
>>>
```
---
---
# Examples 
### Numeric digits of UPNumber and Random number generation
```python
>>> 
>>> import upmath
>>> upmath.version
'2.0.0'
>>> import upmath.lib as lib
>>>
>>> lib.base2digits
('0', '1')
>>> lib.base8digits
('0', '1', '2', '3', '4', '5', '6', '7')
>>> lib.base10digits
('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
>>> lib.base16digits
('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f')
>>> lib.base32digits
('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 
'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v')
>>> lib.base64digits
('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 
'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 
'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!', '@')
>>>
>>> lib.digitIndex('m',base=64)
22
>>> lib.digitChar(22,base=64)
'm'
>>>
>>> print(lib.randomInteger(length=40,base=2))
b02:1011100010110100111001111100100001100001
>>> print(lib.randomInteger(length=40,base=8))
b08:1443453462141027362365304051756402002661
>>> print(lib.randomInteger(length=40,base=10))
b10:4308311625313438552071180617956698018059
>>> print(lib.randomInteger(length=40,base=16))
b16:5bb28ee5df6640da35cc98d47b62d9536f2ac341
>>> print(lib.randomInteger(length=40,base=32))
b32:c82366mes4lpg58klcvoij0nrrihmala55qglqrf
>>> print(lib.randomInteger(length=40,base=64))
b64:fgX3IFNOXzE1c2cSn9Tw5ioIReXncSnueRQbgM4Z
>>>
>>> print(lib.randomFloat(length=50,base=2))
b02:1001011110111.1010001101101111100001111111000110011
>>> print(lib.randomFloat(length=50,base=8))
b08:635245411407012165217532161135752452566051445237.17
>>> print(lib.randomFloat(length=50,base=10))
b10:6555.7875474885111908514201013999991057580008396989
>>> print(lib.randomFloat(length=50,base=16))
b16:6b2ee2921bf8a9b576.b084f6b729bb4339d66479b08cec487d
>>> print(lib.randomFloat(length=50,base=32))
b32:b2k81.87vpfgbr5dsvks06d8lppc5dt28iitnmiiu8lmmh94a1e
>>> print(lib.randomFloat(length=50,base=64))
b64:lstJQpE2LYKkpho!SEwZtH.QlavtOy1DsF85Nyy94DwPffdbCak
>>>

```

### Universal precision numbers (lib.Number) are accurate to the given precision. Default precision is 36.

```python
>>> 
>>> import upmath.lib as lib
>>>
>>> dir(lib)
['E', 'INF', 'Number', 'ONE', 'PI', 'UND', 'UNDEFINED', 'ZERO', '__builtins__', '__cached__', 
'__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', '__version__', 
'acos', 'acosec', 'acosech', 'acosh', 'acot', 'acoth', 'acsc', 'acsch', 'asec', 'asech', 
'asin', 'asinh', 'atan', 'atanh', 'base10digits', 'base16digits', 'base2digits', 
'base32digits', 'base64digits', 'base8digits', 'bernoulliNumber', 'beta', 'cos', 'cosec', 
'cosech', 'cosh', 'cot', 'coth', 'csc', 'csch', 'dataType', 'digitChar', 'digitIndex', 
'digits', 'e', 'erf', 'erfc', 'eulerNumber', 'exp', 'fact', 'gamma', 'getE', 'getPI', 
'inv', 'lg', 'ln', 'log10', 'logE', 'mypi', 'nCr', 'nPr', 'pe', 'pi', 'power', 'psmf', 
'randomFloat', 'randomInteger', 'randomNumberString', 'randomString', 'sec', 'sech', 'sin', 
'sinh', 'sqrt', 'tan', 'tangentNumber', 'tanh', 'upn', 'version']
>>>
>>>
>>> lib.e
b10:2.718281828459045235360287471352662497
>>>
>>> lib.getE(prec=300)
b10:2.71828182845904523536028747135266249775724709369995957496696762772407663035354759457
13821785251664274274663919320030599218174135966290435729003342952605956307381323286279434
90763233829880753195251019011573834187930702154089149934884167509244761460668082264800168
47741185374234544243710753907774499207
>>>
>>> lib.PI
b10:3.141592653589793238462643383279502884
>>>
>>> lib.getPI(prec=300)
b10:3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862
80348253421170679821480865132823066470938446095505822317253594081284811174502841027019385
21105559644622948954930381964428810975665933446128475648233786783165271201909145648566923
46034861045432664821339360726024914127
>>>
>>> a=lib.getE(prec=300)
>>> type(a)
<class 'upmath.src.upnumber.Number'>
>>> a.__sizeof__()
24
>>>
>>> b=lib.getPI(prec=300)
>>> type(b)
<class 'upmath.src.upnumber.Number'>
>>> b.__sizeof__()
24
>>>
**So, an upnumber carrying 300 digits requires only 24B memory space**
```
### Mathematical operations are able to create the numbers correct to the given precision.
```python
>>> import upmath.lib as lib
>>> a=lib.Number('998001',prec=500)
>>>
>>> lib.inv(a)
b10:0.00000100200300400500600700800901001101201301401501601701801902002102202302402502602
70280290300310320330340350360370380390400410420430440450460470480490500510520530540550560
57058059060061062063064065066067068069070071072073074075076077078079080081082083084085086
08708808909009109209309409509609709809910010110210310410510610710810911011111211311411511
61171181191201211221231241251261271281291301311321331341351361371381391401411421431441451
4614714814915015115215315415515615715815916016116216316416516616
>>>
```
### All numbers are returned and manipulated in **string** format. It can handle integer and floating point numbers of any base from 2,8,10,16,32,64. This package can process any number from ultra small to ultra large level.
```ptthon
>>> import upmath.lib as lib
>>> a=lib.Number('-1.6e-2020')
>>> b=lib.Number('4.85e+2020')
>>> print(a)
b10:-1.6e-2020
>>> print(b)
b10:4.85e+2020
>>>
>>> a+1
b10:0.9999999999999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
984
>>>
>>> b+1
b10:4850000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000001
>>>
```
### The central number system is binary and denary. Numbers of bases 8,16,32 and 64 are converted efficiently through binary. Arithmetic and other mathematical operations are performed by denary (base10) operations. 
```python
>>> 
>>> import upmath.lib as lib
>>> a=lib.Number('hello.world',64)
>>>
>>> a;print(a)
b10:288970072.505963635630905628204345703125
b64:hello.world
>>>
>>> a.getDenaryForm()
'b10:288970072.505963635630905628204345703125'
>>> 
>>> a.getBinaryForm()
'b02:10001001110010101010101011000.100000011000011011010101001101'
>>>
>>> a.getOctalForm()
'b08:2116252530.4030332515'
>>>
>>> a.getHexadecimalForm()
'b16:11395558.8186d534'
>>>
>>> a.getBase32Form()
'b32:8jilao.g63dad'
>>> 
```

---
<!-- table -->
| Base | Number System | Example | Digits |
| --- | --- | --- | --- |
| Base=2 | Binary | b02:-11001.011p600 | 0,1 |
| Base=8 | Octal | b08:-4572.0273p-600 | 0-7 |
| Base=10 | Denary | b10:-9078.0412p40 | 0-9 |
| Base=16 | Hexadecimal | b16:-f04d.32abp70 | 0-9a-fA-F |
| Base=32 | DuoTrigesimal | b32:-vV0o.25f9p+147 | 0-9a-vA-V |
| Base=64 | Base-64 | b64:-zXo0.a4Btp-250 | 0-9a-zA-Z!@ |



### Number input modes:'fp' and 'fr'
    fp' (floating point) mode means numbers with floating digits.
        Like:b02:-11110001.11p-10,b10:92.45e33
    'fr' (fractional) mode which displays number as mixed or proper fraction.
        Like:b02:-11110001 11/100p+17, b10:92 9/20e+23.
    Difference: 'fp' numbers contain '.', but 'fr' numbers have '/'.

### Valid Input Format:
```pytohn
(fp)11110.101,'11110.101p+34','11110.101p34','11110.101p-23','-0.1101p-45'
(fr) '-1101 11/1101', "-1101 11/1101p+7", "-1101 11/1101p7", '-1101 11/1101p-17'
```
### Default base is 10. If base is not given in the number definition, it automatically assumes 10.
```python
>>>
>>> import upmath.lib as lib
>>> a=lib.Number('24 5/7p-5')
>>> a;print(a)
b10:0.0002471428571428571428571428571428571428571
b10:24 5/7e-5
>>>
>>> a+1
b10:1.0002471428571428571428571428571428571428571
>>> a*1
b10:0.0002471428571428571428571428571428571428571
>>> 
```

### UPNumbers are stored internally as a dictionary. For example,
```python
>>> import upmath.lib as lib
>>> a=lib.Number('15.27')
>>>
>>> a.getDict()
{'base': 10, 'input_mode': 'fp', 'sign': '+', 'ipart': '15', 'fpart': '27', 'exp': 0, 
'prec': 4, 'is_accurate': True, 'normalized': {'sign': '+', 'ipart': '15', 'fpart': '27', 
'is_accurate': True}, 'is_integer': False, 'is_float': True, 'normal_prec': 4, 
'max_prec': 36, 'base10': {'sign': '+', 'ipart': '15', 'fpart': '27', 'is_accurate': True}, 
'base10_prec': 36}
>>>
>>>
>>> b=lib.Number('111001.11011',base=2)
>>> b.getDict()
{'base': 2, 'input_mode': 'fp', 'sign': '+', 'ipart': '111001', 'fpart': '11011', 'exp': 0, 
'prec': 11, 'is_accurate': True, 'normalized': {'sign': '+', 'ipart': '111001', 
'fpart': '11011', 'is_accurate': True}, 'is_integer': False, 'is_float': True, 
'normal_prec': 11, 'max_prec': 36, 'base10': {'sign': '+', 'ipart': '57', 'fpart': '84375', 
'is_accurate': True}, 'base10_prec': 7}
>>>
>>> c=lib.Number('45 21/33',base=8)
>>> c;print(c)
b10:37.62962962962962962962962962962962768943353750619202951397777635888803465791241364
9683003313839435577392578125
b08:45 21/33
>>> c.getDict()
{'base': 8, 'input_mode': 'fr', 'sign': '+', 'ipart': '45', 'numerator': '21', 'deno': '33', 
'exp': 0, 'prec': 6, 'is_accurate': True, 'base10fr': {'sign': '+', 'ipart': '37', 
'numerator': '17', 'deno': '27', 'is_accurate': True}, 'max_prec': 38, 
'normalized': {'sign': '+', 'ipart': '45', 'fpart': '502275502275502275502275502275502275', 
'is_accurate': False}, 'is_integer': False, 'is_float': True, 'normal_prec': 38, 
'base10': {'sign': '+', 'ipart': '37', 'fpart': '629629629629629629629629629629627689433537
506192029513977776358888034657912413649683003313839435577392578125', 'is_accurate': False}, 
'base10_prec': 110}
>>>
```

### Builtin Functions: int(), float(), round() on the UPNumber (universal precision number)
```python
>>>
>>> import upmath.lib as lib
>>> a=lib.Number('111001.11011',base=2)
>>> a;print(a)
b10:57.84375
b02:111001.11011
>>> b=lib.Number('111001',base=2)
>>> b;print(b)
b10:57
b02:111001
>>> int(a)
57
>>> float(b)
57.0
>>> round(a,4)
57.8438
>>> round(a,2)
57.84
>>> round(a,3)
57.844
>>>
```
### math.floor() and math.ceil() functions on UPNumber (universal precision number)
```python
>>>
>>> import upmath.lib as lib
>>> a=lib.Number('111001.11011',base=2)
>>> b=lib.Number('-25.7124',base=8)
>>> a;print(a)
b10:57.84375
b02:111001.11011
>>> b;print(b)
b10:-21.8955078125
b08:-25.7124
>>>
>>> import math
>>> math.ceil(a)
58
>>> math.floor(a)
57
>>> math.ceil(b)
-21
>>> math.floor(b)
-22
>>>
```

### If a floating or fractional number is recurring, upnumber can handle it very efficiently just by setting modify or ultraModify argument 'True'. modify() method and ultraModify() method also do the same job. These methods or arguments can also convert the improper fractions to proper fraction with necessary simplifications.
```python
>>> 
>>> import upmath.lib as lib
>>> a=lib.Number('245.20451045104510451',modify=True)
>>> print(a)
b10:245 1859/9090
>>> 
>>> a=lib.Number('245.20451045104510451')
>>> a
b10:245.20451045104510451
>>> a.modify()
>>> a;print(a)
b10:245.20451045104510451
b10:245 1859/9090
>>>
>>> b=lib.Number('245/37',modify=True)
>>> b;print(b)
b10:6.62162162162162162162162162162162162162
b10:6 23/37
>>>
>>> c=lib.Number('-30 245/35',modify=True)
>>> c;print(c)
b10:-37
b10:-37
>>>
>>> d=lib.Number('-30 245/45',modify=True)
>>> d;print(d)
b10:-35.44444444444444444444444444444444444444
b10:-35 4/9
>>> 
```

## Arithmetic operations
### Addition(+), subtraction(-), multiplication(*), division(/), floor division(//), remainder or mod operation(%), power operation(**) etc. can be done very easily.

```python
>>> 
>>> import upmath.lib as lib
>>> a=lib.Number('12.45')     #denary number
>>> b=lib.Number('-2 3/5')    #denary number
>>> c=lib.Number('1101.11',2) #binary number
>>> d=lib.Number('2 3/5',8)   #octal number
>>> a+b
b10:9.85
>>> a+2.45
b10:14.9
>>> 10-a
b10:-2.45
>>> print(5+b)
b10:2 2/5
>>> c*2.5
b10:34.375
>>> 30/a
b10:2.409638554216867469879518072289156626506
>>> a/0
b10:<INF>
>>> b/0
b10:<-INF>
>>> 30//a
b10:2
>>> 30%a
b10:5.1
>>> lib.power(a,2.5)
b10:546.919462835080042646792227676322546
>>> a**2.5
b10:546.919462835080042646792227676322546
>>> 5**a
b10:503705338.789256548289543848618036647
>>> lib.power(b,-2.5)
b10:<UNDEFINED>
>>> b**-2.5
b10:<UNDEFINED>
>>> c**2.5
b10:701.062513233261888120374289325692407
>>> 2.5**c
b10:296261.433052663007815877972404231589
>>> lib.power(c,-2.5)
b10:0.00142640632058338821552976539808037757
>>> c**-2.5
b10:0.00142640632058338821552976539808037757
>>> 2.5**lib.Number('4.5')
b10:61.7632355501636588281033895397015339
>>> 2**lib.Number('-4.5')
b10:0.044194173824159220275052772631553065
>>> 
```

## Logical operations
### Logical operations like equal-to(==), not-equal-to(!=), greater-than(>), less-than(<), greater-than-or-equal-to(>=) and less-than-or-equal-to(<=) can be performed on universal precision number objects as simple as done with the normal numbers. 'True' or 'False' are returned.

```python
>>> 
>>> import upmath.lib as lib
>>> a=lib.Number('-2.5')
>>> b=lib.Number('-10.1',2)
>>> c=lib.Number('ab c/d',16)
>>> d=lib.Number('f.10z',64)
>>> 
>>> a==b
True
>>> a>b
False
>>> c<d
False
>>> d>b
True
>>> a!=b
False
>>> c>a
True
>>> a>=b
True
>>> a<10
True
>>> 10>a
True
>>> 20>=c
False
>>> 20>=d
True
>>> 
>>> 
```

## In-Place assignment operations
### In-place assignment operations like +=, -=, *=, /=, //=, %= are also supported in this number system.

<!-- table -->
| operator | operation |
| --- | --- |
| += | Operands are added first, then the result is assigned to the left operand |
| -= | Right Operand is subtracted from the left, then the result is assigned to the left operand |
| *= | Operands are multiplied first, then the result is assigned to the left operand |
| **= | Left operands are raised to the power of the right operand and the value is assigned to the left |
| /= | Left operand is divided by the right one, then the result is assigned to the left operand |
| //= | Left operand is divided by the right one, then the floor value of quotient is assigned to the left operand |
| %= |Left operand is divided by the right one, then the remainder is assigned to the left operand |


```python
>>> 
>>> import upmath.lib as lib
>>> a=lib.Number('-2.5')
>>> b=lib.Number('10.75')
>>> c=lib.Number('13.25',8)
>>> 
>>> a+=b
>>> a
b10:8.25
>>> 
>>> a-=b
>>> a
b10:-2.5
>>> 
>>> a*=c
>>> a
b10:-28.3203125
>>> b/=c
>>> b
b10:0.9489655172413793103448275862068965517
>>> 
>>> b=lib.Number('10.75')
>>> c//=b
>>> c
b10:1
>>> c=lib.Number('13.25',8)
>>> c%=b
>>> c
b10:0.578125
>>> 
```

# Standard mathematical operations
### (Logarithmic, exponential, trigonometric, hyperbolic, gamma, beta and error functions are executed efficiently with this upnumber number system)
---
## Inverse, factorial, logarithmic, exponential, square-root and power operations

```python
>>> 
>>> import upmath.lib as lib
>>> a=lib.Number('-2.5')
>>> lib.inv(a)
b10:-0.4
>>> b=lib.Number('7')
>>> lib.fact(b)
b10:5040
>>> 
>>> lib.ln(a)
b10:<UNDEFINED>
>>> 
>>> a=lib.Number('3 4/7')
>>> lib.ln(a)
b10:1.27296567581288744409616592300919555
>>> lib.ln(a,prec=50)
b10:1.2729656758128874440961659230091955494141179789552
>>> 
>>> a=lib.Number('-2.5')
>>> b=lib.Number('4.75')
>>> lib.ln(b)        # logE(b)
b10:1.5581446180465498411745631889715004
>>> lib.lg(b)        #log10(b)
b10:0.676693609624866571108855686307943263
>>> 
>>> lib.exp(a)       #e^a
b10:0.0820849986238987951695286744671598078
>>> lib.exp(b)       #e^b
b10:115.584284527187658133414267136529079lib.sqrt()
>>> 
>>> lib.power(a,b)    #a^b
b10:<UNDEFINED>
>>> lib.power(b,a)    #b^a
b10:0.020336020730908522185680627421418239
>>> 
>>> lib=upn.Number('-2 1/2')
>>> b=upn.Number('4 3/4')
>>> lib.sqrt(b)
b10:<UNDEFINED>
>>> lib.sqrt(b)
b10:2.17944947177033677611849099192980783
>>> 
>>> lib.power(a,b)
b10:<UNDEFINED>
>>> lib.power(b,a)
b10:0.020336020730908522185680627421418239
>>> 
```

## Trigonometric and inverse trigonometric functions

```python
>>> 
>>> import upmath.lib as lib
>>> a=lib.Number('0')
>>> b=lib.Number('390')
>>> c=lib.Number('-405')
>>> d=lib.Number('540')
>>> e=lib.Number('-90')
>>> 
>>> lib.sin(a)
b10:0
>>> lib.sin(b)
b10:0.5
>>> lib.sin(c)
b10:-0.707106781186547524400844362104849039
>>> d.sin(d)
b10:0
>>> lib.sin(e)
b10:-1
>>> 
>>> lib.tan(a)
b10:0
>>> lib.tan(c)
b10:-1
>>> lib.tan(d)
b10:0
>>> lib.tan(e)
b10:<-INF>
>>> lib.cosec(c)
b10:-1.41421356237309504880168872420969808
>>> lib.sec(d)
b10:-1
>>> lib.cot(e)
b10:0
>>> 
>>> a=lib.Number('0')
>>> b=lib.Number('1')
>>> c=lib.Number('-1')
>>> 
>>> lib.asin(a)
b10:0
>>> lib.acos(a)
b10:90
>>> 
>>> lib.asin(b)
b10:90
>>> lib.acos(b)
b10:0
>>> 
>>> lib.acot(b,unit='rad')
b10:0.785398163397448309615660845819875721
>>> lib.acot(b,unit='d')
b10:45
>>> 
>>> lib.acot(c)
b10:-45
>>> lib.atan(c)
b10:-45
>>> 
```

## Hyperbolic and inverse hyperbolic functions

```python
>>> 
>>> import upmath.lib as lib
>>> a=lib.Number('2')
>>> b=lib.Number('-2')
>>> c=lib.Number('0')
>>> 
>>> lib.sinh(a)
b10:3.6268604078470187676682139828012617
>>> lib.cosh(a)
b10:3.76219569108363145956221347777374611
>>> lib.tanh(b)
b10:-0.96402758007581688394641372410092315
>>> c.coth()
b10:0
>>> lib.sech(a)
b10:0.265802228834079692120862739819888972
>>> lib.cosech(b)
b10:-0.275720564771783207758351482163027121
>>> 
>>> a=lib.Number('2')
>>> b=lib.Number('0.5')
>>> c=lib.Number('0')
>>> 
>>> lib.asinh(a)
b10:1.44363547517881034249327674027310527
>>> lib.acosh(a)
b10:1.31695789692481670862504634730796844
>>> lib.atanh(b)
b10:0.549306144334054845697622618461262852
>>> lib.atanh(c)
b10:0
>>> lib.acoth(a)
b10:0.549306144334054845697622618461262852
>>> lib.asech(b)
b10:1.31695789692481670862504634730796844
>>> lib.acosech(c)
b10:<INF>
>>>
```

## Gamma, beta and error functions
### (Gamma and beta functions give accurate answers for positive whole numbers and approximate values for floating point numbers.)

```python
>>> import upmath.lib as lib
>>> a=lib.Number('-1')
>>> b=lib.Number('2')
>>> c=lib.Number('0')
>>> 
>>> lib.gamma(b)
b10:1
>>> d=lib.Number('2.5')
>>> lib.gamma(d)
b10:1.32934038817913766044178571868836165
>>> lib.beta(b)
b10:0.5
>>> lib.beta(c)
b10:<INF>
>>> 
>>> lib.erf(a)
b10:-0.842700792949714869341220635082609259
>>> lib.erfc(a)
b10:1.84270079294971486934122063508260926
>>> lib.erfc(b)
b10:0.00467773498104726583793074363274707222
>>> lib.erf(b)
b10:0.995322265018952734162069256367252928
>>> lib.erf(c)
b10:0
>>> lib.erfc(c)
b10:1
>>> lib.erf(d)
b10:0.999593047982555041060435784260025087
>>> lib.erfc(d)
b10:0.000406952017444958939564215739974912563
>>> 
```

## Euler, Bernoulli and Tangent numbers. 
### For odd positive integers, these numbers return zero.

```python
>>> 
>>> import upmath.lib as lib
>>> a=lib.Number('2')
>>> b=lib.Number('3')
>>> c=lib.Number('7')
>>> d=lib.Number('8')
>>> e=lib.Number('9')
>>> 
>>> lib.eulerNumber(a)
b10:-1
>>> lib.eulerNumber(b)
b10:0
>>> lib.eulerNumber(c)
b10:0
>>> lib.eulerNumber(d)
b10:1385
>>> lib.eulerNumber(e)
b10:0
>>> 
>>> lib.bernoulliNumber(a)
b10:1/6
>>> lib.bernoulliNumber(b)
b10:0
>>> lib.bernoulliNumber(c)
b10:0
>>> lib.bernoulliNumber(d)
b10:-1/30
>>> lib.bernoulliNumber(e)
b10:0
>>> 
>>> lib.tangentNumber(a)
b10:1
>>> lib.tangentNumber(b)
b10:0
>>> lib.tangentNumber(c)
b10:0
>>> lib.tangentNumber(d)
b10:272
>>> lib.tangentNumber(e)
b10:0
>>> 
```

### UPNumber (universal precision number) is a class instance. PSM functions can take the integer and floating point denary numbers directly.
```python
>>> 
>>> import upmath.lib as lib
>>> lib.nCr(10,7)
b10:120
>>> lib.fact(15)
b10:1307674368000
>>> 
>>> lib.power(2,10)
b10:1024
>>> 
>>> lib.e
b10:2.7182818284590452353602874713526625
>>> lib.E
b10:2.7182818284590452353602874713526625
>>> lib.PI
b10:3.14159265358979323846264338327950288
>>> 
```
---
# Public Properties and Methods of upnumber (universal precision number)
#### (prec = precision = number of siginificant digits)
<!-- table -->
| **Property** | **Description** |
| --- | --- |
| __base | private property to hold the base of the upnumber |
| __base10prec | private property to hpld the prec of converted numbers of other bases |
| __is_accurate | private boolean property; True means the number is accurate within the given precision |
| __is_numeric | private boolean property; True means it is a valid upnumber |
| __max_prec | private property to hold the maximum prec value of the set prec and the number's prec |
| __modify | private boolen property; True means the number will be modified during creation by simplification |
| __normal_prec | private property to hold the prec value of the normalized number |
| __num | private property to hold the user's number value |
| __parseddict | private property to hold the **parsed dictionary** of the given upnumber |
| __prec | private property to hold the user's precision to the upnumber |
| __ultra_modify | private boolen property; True means super simplification done during creation of the upnumber |

---
### Magic Methods of UPNumber (universal precision number)
#### (a,b  = upnumbers; prec = precision = number of siginificant digits)
<!-- table -->
| **Magic Method** | **Arguments** | **Description** |
| --- | --- | --- |
| \_\_repr\_\_(self) | --- | repr(a) returns the denary equivalent normalized form of the upnumber,a |
| \_\_str\_\_(self) | --- | str(a) or print(a) returns the string representation of the upnumber,a |
| \_\_pos\_\_(self) | --- | +a returns positive value of the upnumber,a; if 'a' is negative, negative 'a' returned |
| \_\_neg\_\_(self) | --- | -a returns negative value of the upnumber,a; if 'a' is negative, positive 'a' returned |
| \_\_abs\_\_(self) | --- | abs(a) returns positive value of the upnumber, a |
| \_\_invert\_\_(self) | --- | ~a returns the inverted value (1/a) of the upnumber, a |
| \_\_int\_\_(self) | --- | int(a) returns the integer value of the upnumber, a |
| \_\_float\_\_(self) | --- | float(a) returns the floating point value of the upnumber, a |
| \_\_round\_\_(self,n) | n = positive integer | round(a) returns the rounded value of the upnumber, a at nth decimal point |
| \_\_add\_\_(self,right) | right | returns an upnumber carrying value of additions like a+10, a+3.5, a+b |
| \_\_radd\_\_(self,left) | left | returns an upnumber carrying value of additions like 10+a, 3.5+a, b+a |
| \_\_sub\_\_(self,right) | right | returns an upnumber carrying value of subtractios like a-10, a-3.5, a-b |
| \_\_rsub\_\_(self,left) | left | returns an upnumber carrying value of subtractions like 10-a, 3.5-a, b-a |
| \_\_mul\_\_(self,right) | right | returns an upnumber carrying value of multiplications like a\*10, a\*3.5, a\*b |
| \_\_rmul\_\_(self,left) | left | returns an upnumber carrying value of multiplications like 10\*a, 3.5\*a, b\*a |
| \_\_pow\_\_(self,right) | right | returns an upnumber carrying value of power operations like a\*\*10, a\*\*3.5, a**b |
| \_\_rpow\_\_(self,left) | left | returns an upnumber carrying value of power operations like 10\*\*a, 3.5\*\*a, b**a |
| \_\_truediv\_\_(self,right) | right | returns an upnumber carrying value of divisions like a/10, a/3.5, a/b |
| \_\_rtruediv\_\_(self,left) | left | returns an upnumber carrying value of divisions like 10/a, 3.5/a, b/a |
| \_\_floordiv\_\_(self,right) | right | returns an upnumber carrying value of floor divisions like a//10, a//3.5, a//b |
| \_\_rfloordiv\_\_(self,left) | left | returns an upnumber carrying value of floor divisions like 10//a, 3.5//a, b//a |
| \_\_mod\_\_(self,right) | right | returns an upnumber carrying value of remainder in division like a%10, a%3.5, a%b |
| \_\_rmod\_\_(self,left) | left | returns an upnumber carrying value of remainder in division like 10%a, 3.5%a, b%a |
| \_\_iadd\_\_(self,right) | right | returns an upnumber carrying the addition value of the right and the number itself; a+=10, a+=3.5, a+=b |
| \_\_isub\_\_(self,right) | right | returns an upnumber carrying the subtraction value of the right from the number itself; a-=10, a-=3.5, a-=b |
| \_\_imul\_\_(self,right) | right | returns an upnumber carrying the multiplication value of the right and the number itself; a*=10, a*=3.5, a*=b |
| \_\_itruediv\_\_(self,right) | right | returns an upnumber carrying the division value of the right and the number itself; a/=10, a/=3.5, a/=b |
| \_\_ifloordiv\_\_(self,right) | right | returns an upnumber carrying the floor division value of the right and the number itself; a//=10, a//=3.5, a//=b |
| \_\_ipow\_\_(self,right) | right | returns an upnumber carrying the value of power operation between the right and the number itself like a**=10, a**=3.5, a**=b |
| \_\_imod\_\_(self,right) | right | returns an upnumber carrying the remainder value of division between the right and the number itself; a%=10, a%=3.5, a%=b |
| \_\_eq\_\_(self,right) | right | returns **True** or **False**; True returned when the operands are equal like a==10, a==3.5, a==b |
| \_\_req\_\_(self,left) | left | returns **True** or **False**; True returned when the operands are equal like 10==a, 3.5==a, b==a |
| \_\_ne\_\_(self,right) | right | returns**True** or **False**; True returned when the operands are not equal like a!=10, a!=3.5, a!=b |
| \_\_rne\_\_(self,left) | left | returns **True** or **False**; True returned when the operands are not equal like 10!=a, 3.5!=a, b!=a |
| \_\_gt\_\_(self,right) | right | returns **True** or **False**; True returned when the upnumber,a is greater than the right operand like a>10, a>3.5, a>b |
| \_\_rgt\_\_(self,left) | left | returns **True** or **False**; True returned when the left operand is greater than the upnumber,a like 10>a, 3.5>a, b>a |
| \_\_lt\_\_(self,right) | right | returns **True** or **False**; True returned when the upnumber,a is less than the right operand like a<10, a<3.5, a<b |
| \_\_rlt\_\_(self,left) | left | returns **True** or **False**; True returned when the left operand is less than the upnumber,a like 10<a, 3.5<a, b<a |
| \_\_ge\_\_(self,right) | right | returns **True** or **False**; True returned when the upnumber,a is greater than or equal to the right operand like a>=10, a>=3.5, a>=b |
| \_\_rge\_\_(self,left) | left | returns **True** or **False**; True returned when the left operand is greater than or equal to the upnumber,a like 10>=a, 3.5>=a, b>=a |
| \_\_le\_\_(self,right) | right | returns **True** or **False**; True returned whenthe upnumber,a is less than or equal to the right operand like a<=10, a<=3.5, a<=b |
| \_\_rle\_\_(self,left) | left | returns **True** or **False**; True returned when the left operand is less than or equal to the upnumber,a like 10<=a, 3.5<=a, b<=a |

---
### Instance Methods of UPNumber (universal precision number)
#### (a,b  = upnumbers; calling style: a.method_name(); prec = precision = number of siginificant digits)
<!-- table -->
| **Instance Method** | **Arguments** | **Description** |
| --- | --- | --- |
| ceil(self) | --- | returns the ceiling value (an integer) of the number instance |
| floor(self) | --- | returns the floor value (an integer) of the number instance |
| copy(self) | --- | returns the copy of the number instance |
| modify(self) | --- | modify the given fractional number by simplification |
| ultraModify(self) | --- | modify the given fractional number by as much simplification as possible |
| isAccurate(self) | --- | returns **True** or **False**; True means the number is correct to the digits, displayed |
| isNumeric(self) | --- | returns **True** or **False**; True means the upnumber is not undefined |
| isInteger(self) | --- | returns **True** or **False**; True means the upnumber is an integer |
| isFloat(self) | --- | returns **True** or **False**; True means the upnumber is a floating point number |
| isFractional(self) | --- | returns **True** or **False**; True means the upnumber is a fractional number |
| isRecurring(self) | --- | returns **True** or **False**; True means the upnumber is a recurring denary |
| isPositive(self) | --- | returns **True** or **False**; True means the upnumber is greater than zero |
| isNegative(self) | --- | returns **True** or **False**; True means the upnumber is less than zero |
| isPrime(self) | --- | returns **True** or **False**; True means the upnumber is a prime |
| isBinary(self) | --- | returns **True** or **False**; True means the upnumber is a valid binary number |
| isOctal(self) | --- | returns **True** or **False**; True means the upnumber isa valid octal number |
| isDenary(self) | --- | returns **True** or **False**; True means the upnumber is a valid denary number |
| isHexadecimal(self) | --- | returns **True** or **False**; True means the upnumber is a valid hexadecimal number |
| isBase32Number(self) | --- | returns **True** or **False**; True means the upnumber is a valid base32 number |
| isBase64Number(self) | --- | returns **True** or **False**; True means the upnumber is a valid base64 number |
| getBase(self) | --- | returns the original base of the number |
| getAccuracy(self) | --- | returns **True** or **False**; True means the number is correct to the digits, displayed |
| getSign(self) | --- | returns the sign of the upnumber |
| getBase(self) | --- | returns the base of the upnumber |
| getBase10Part(self) | --- | returns the dictionary with key 'base10' from self.__parseddict |
| getBase10Precision(self) | --- | returns the denary precision (base10_prec) from from self.__parseddict |
| forceResetPrecision(self) | --- | sets number precision forcefully |
| getBase10frPart(self) | --- | returns the dictionary with key 'base10fr' from self.__parseddict |
| displayInFPMode(self) | --- | displays upnumber in floating point mode |
| denaryFPtoFRMode(self) | --- | denary floating point number is converted to fractional form |
| createNewNumber(self,prec,is_accurate) | --- | returns a new upnumber with the given precision and accuracy |
| limitFloatingDigits(self,newprec,is_accurate) | --- | limits the floating digits into the given precision |
| denaryInteger(self) | --- | returns equivalent denary integer |
| setMaxPrecision(self,prec) | --- | sets new maximum precision value of the upnumber |
| getBinaryForm(self) | --- | returns the string version of equivalent binary |
| getOctalForm(self) | --- | returns the string version of equivalent octal |
| getHexadecimalForm(self) | --- | returns the string version of equivalent hexadecimal |
| getBase32Form(self) | --- | returns the string version of equivalent base32 number |
| getBase64Form(self) | --- | returns the string version of equivalent base64 number |
| getDenaryForm(self) | --- | returns the string version of equivalent denary |
| getInputMode(self) | --- | returns the input ('fp','fr') mode of the upnumber |
| getIntegerPart(self) | --- | returns the the integer part of the upnumber |
| getFloatingPart(self) | --- | returns the floating part of the upnumber |
| getNormalizedPart(self) | --- | returns the normalized part of the number dictionary |
| getNumerator(self) | --- | returns the numerator of the fractional upnumber |
| getDenominator(self) | --- | returns the denominator of the fractional upnumber |
| getDict(self) | --- | returns the number dictionary |
| getExponent(self) | --- | returns the exponent part of the number dictionary |
| getNormalizedForm(self) | --- | returns the string representation of the normalized part of the upnumber |
| getScientificForm(self) | --- | returns the scientific form of the upnumber |
| getPrecision(self) | --- | returns the precision of the upnumber set by the user |
| getNormalPrecision(self) | --- | returns the precision of the normalized part of the upnumber |
| getMaxPrecision(self) | --- | returns the maximum precision of the upnumber |
| getOriginal(self) | --- | returns the original upnumber given by the user |


---
---
# Precisional Standard Mathematical Functions (PSMF) in Tabular Presentation
### **(Short descriptions of Precisional Standard Math Functions)**
<!-- table -->
| Function | Arguments | Domain and Return |
| --- | --- | --- |
| fact(n) | n=positive integer or zero; | factorial of n |
| nCr(n=None,r=None) | n=positive integer;r=positive integer;n>=r | integer; No of combinations |
| nPr(n=None,r=None) | n=positive integer;r=positive integer;n>=r | integer; No of permutations |
| ln(x=None,prec=36) | x={R:x>=0};prec=positive integer | natural logarithm of x |
| logE(x=None,prec=36) | x={R:x>=0};prec=positive integer | natural logarithm of x |
| lg(x=None,prec=36) | x={R:x>=0};prec=positive integer | 10-based logarithm of x |
| log10(x=None,prec=36) | x={R:x>=0};prec=positive integer | 10-based logarithm of x |
| exp(x=None,prec=36) | x={R};prec=positive integer | exponential of x, e**x |
| sqrt(x=None,prec=36) | x={R:x>=0};prec=positive integer | square root of x (real number) |
| power(x=None,y=None,prec=36) | x=base {R:x>=0};y=power;prec=positive integer | x**y is returned |
| sin(x=None,unit='d',prec=36) | x=angle{R};unit=unit of angle ('d','D','deg','Deg','degre','Degre','r','R','c','rad','Rad','radian','Radian');prec=positive integer | -1 <=sin(x) <=1 |
| cos(x=None,unit='d',prec=36) | x=angle{R};unit=unit of angle ('d','D','degre','Degre','r','R','c','rad','Rad','radian','Radian');prec=positive integer | -1<= cos(x) <=1 |
| tan(x=None,unit='d',prec=36) | x=angle{R};unit=unit of angle ('d','D','deg','Deg','degre','Degre','r','R','c','rad','Rad','radian','Radian');prec=positive integer | -INF <= tan(x) <= INF |
| cot(x=None,unit='d',prec=36) | x=angle{R};unit=unit of angle ('d','D','deg','Deg','degre','Degre','r','R','c','rad','Rad','radian','Radian');prec=positive integer | -INF <= cot(x) <= INF |
| sec(x=None,unit='d',prec=36) | x=angle{R};unit=unit of angle ('d','D','deg','Deg','degre','Degre','r','R','c','rad','Rad','radian','Radian');prec=positive integer | sec(x)>=1 or sec(x)<=-1 |
| csc(x=None,unit='d',prec=36) | x=angle{R};unit=unit of angle ('d','D','deg','Deg','degre','Degre','r','R','c','rad','Rad','radian','Radian');prec=positive integer | cosec(x)>=1 or cosec(x)<=-1 |
| cosec(x=None,unit='d',prec=36) | x=angle{R};unit=unit of angle ('d','D','deg','Deg','degre','Degre','r','R','c','rad','Rad','radian','Radian');prec=positive integer | cosec(x)>=1 or cosec(x)<=-1 |
| asin(x=None,unit='d',prec=36) | x={R:-1<=x<=1};unit=unit of output angle ('d','D','deg','Deg','degre','Degre','r','R','c','rad','Rad','radian','Radian');prec=positive integer | -PI/2<=asin(x)<=PI/2 |
| acos(x=None,unit='d',prec=36) | x={R:-1<=x<=1};unit=unit of output angle ('d','D','deg','Deg','degre','Degre','r','R','c','rad','Rad','radian','Radian');prec=positive integer | -PI/2<=acos(x)<=PI/2 |
| atan(x=None,unit='d',prec=36) | x={R};unit=unit of output angle ('d','D','deg','Deg','degre','Degre','r','R','c','rad','Rad','radian','Radian');prec=positive integer | -PI/2<=atan(x)<=PI/2 |
| acot(x=None,unit='d',prec=36) | x={R};unit=unit of output angle ('d','D','deg','Deg','degre','Degre','r','R','c','rad','Rad','radian','Radian');prec=positive integer | -PI/2<=acot(x)<=PI/2 |
| asec(x=None,unit='d',prec=36) | x={R:-1>=x>=1};unit=unit of output angle ('d','D','deg','Deg','degre','Degre','r','R','c','rad','Rad','radian','Radian');prec=positive integer | 0<=asec(x)<=PI |
| acosec(x=None,unit='d',prec=36) | x={R:-1>=x>=1};unit=unit of output angle ('d','D','deg','Deg','degre','Degre','r','R','c','rad','Rad','radian','Radian');prec=positive integer | -PI/2<=acosec(x)<=PI/2 |
| acsc(x=None,unit='d',prec=36) | x={R:-1>=x>=1};unit=unit of output angle ('d','D','deg','Deg','degre','Degre','r','R','c','rad','Rad','radian','Radian');prec=positive integer | -PI/2<=acosec(x)<=PI/2 |
| sinh(x=None,prec=36) | x={R};prec=positive integer | hyperbolic sin of x is returned;Range:{R} |
| cosh(x=None,prec=36) | x={R};prec=positive integer | hyperbolic cos of x is returned;Range:{R:y>=1} |
| tanh(x=None,prec=36) | x={R};prec=positive integer | hyperbolic tan of x is returned;Range:{R:-1<=f(x)<=1} |
| coth(x=None,prec=36) | x={R};prec=positive integer | hyperbolic cot of x is returned;Range:{R:-1>=f(x)>=1} |
| sech(x=None,prec=36) | x={R};prec=positive integer | hyperbolic sec of x is returned;Range:{R:1>=y>=0} |
| cosech(x=None,prec=36) | x={R:x!=0};prec=positive integer | hyperbolic cosec of x is returned;Range:{R} |
| csch(x=None,prec=36) | x={R:x!=0};prec=positive integer | hyperbolic cosec of x is returned;Range:{R} |
| asinh(x=None,prec=36) | x={R};prec=positive integer | hyperbolic sin inverse of x is returned;Range:{R} |
| acosh(x=None,prec=36) | x={R:x>=1};prec=positive integer | hyperbolic cos inverse of x is returned;Range:{R:y.=0} |
| atanh(x=None,prec=36) | x={R:-1<=x<=1};prec=positive integer | hyperbolic tan inverse of x is returned;Range:{R} |
| acoth(x=None,prec=36) | x={R:-1>=x>=1};prec=positive integer | hyperbolic cot inverse of x is returned;Range:{R} |
| asech(x=None,prec=36) | x={R:1>=x>0};prec=positive integer | hyperbolic sec inverse of x is returned;Range:{R:y>=0} |
| acosech(x=None,prec=36) | x={R:x>0};prec=positive integer | hyperbolic cosec inverse  of x is returned;Range:{R:y>0} |
| acsch(x=None,prec=36) | x={R:x>0};prec=positive integer | hyperbolic cosec inverse  of x is returned;Range:{R:y>0} |
| gamma(x=None,prec=36) | x={R:x>0};prec=positive integer | gamma of x is returned;Range:{R:f(x)>0} |
| beta(x=None,y=None,prec=36) | x={R:x>0};y={R:y>0};prec=positive integer | beta of x and y is returned;Range:{R:1>=f(x)>=0} |
| erf(x=None,prec=36) | x={R};prec=positive integer| | rror-function of x is returned;Range:{R:-1=<f(x)<=1} |
| erfc(x=None,prec=36) | x={R};prec=positive integer | complementary error-function of x is returned;Range:{R:0=<f(x)<=2} |
| eulerNumber(r=None) | r=positive integer | if r is odd, 0(zero) is returned;otherwise integer returned|
| bernoulliNumber(r=None) | r=positive integer | if r is odd, 0(zero) is returned;otherwise fraction is returned |
| tangentNumber(r=None) | r=positive integer | if r is odd, 0(zero) is returned;otherwise integer returned |

---
## The Author and Maintainer of upmath library
#### For any issue on this library, please feel free to mail me: aminul71bd@gmail.com
![ author's photo ](author_photo_w250.jpg)
---




















 



