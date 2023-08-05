"""
  Package Name:upmath (universal precisional mathematics)
  Path:'<package_path>\\upmath\\__init__.py'
  Version:'2.0.0'
  Previous Version:1.3
  Last Modified: 21st Jan, 2023
  Author:A K M Aminul Islam
  Email:aminul71bd@gmail.com
  Company:Newtonia Ltd

  package structure:
    package_root/__init__.py (version=1.3.1=latest)
    package_root/upmath/src/digits.py     	(version=1.0.2023.01.27, md5sum='c9fab1c9481c737f7a175e398945f73b')
    package_root/upmath/src/mypi.py       	(version=2.2.2023.01.27, md5sum='88fd6384c81f52037f8b97018c9ab9f4')
	package_root/upmath/src/pE.py         	(version=2.1.2023.01.27, md5sum='ea4ea9b87e729fbb52f8bdbe4b6c9cc8')
	package_root/upmath/src/psmf.py     	(version=2.7.2023.02.03, md5sum='b19e6e2606ffa05449f0421bd3b236f7')    
    package_root/upmath/src/upnumber.py 	(version=2.8.2023.02.03, md5sum='3cb14106ce5b1979f15e34ba24cc4cd0')
    package_root/upmath/lib.py			 	(version=1.0.2023.02.03, md5sum='9db6f46d2fe78a87e9d6cc5cd24c6bcb')
        
  Limitation: Python interpreter's maximum_integer_digit is set to 4300. If this limit
              is exceeded internally, ValueError is raised. If it happens so, raise the
              int_max_str_digits
			For Example: sys.set_int_max_str_digits(100000)

  Dependencies: __future__, re, sys, random

"""

# Python interpreter's max-int-str-digits raised to ten thousand
import sys
#sys.set_int_max_str_digits(100000)

# upmath package version
__version__ = "2.0.0"
version = "2.0.0"


