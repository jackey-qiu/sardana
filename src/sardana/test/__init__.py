#!/usr/bin/env python

##############################################################################
##
## This file is part of Sardana
## 
## http://www.tango-controls.org/static/sardana/latest/doc/html/index.html
##
## Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
## 
## Sardana is free software: you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## Sardana is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
## 
## You should have received a copy of the GNU Lesser General Public License
## along with Sardana.  If not, see <http://www.gnu.org/licenses/>.
##
############################################################################## 


"""

Sardana includes a framework allowing to test its features. 
This framework is aimed to be used with the objective of finding bugs and 
promote test driven development.

Ideally, each bug found should be accompanied by a test revealing the bug.
That eases the process of correcting bugs.

The objective of the Sardana Test Framework is not to provide a test for 
every piece of code, but rather to ease collaborations and allow people
from other institutions to provide their own test classes.

At the moment the Sardana testing is focused on Unit Tests, but in the future 
the objective is to extend it to integration and system tests as well.

Sardana Test Framework is based on 'unittest'. This means that each of the 
Sardana python test classes inherits from unittest.TestCase.

Each of the Sardana Tests has to be acompanied by a documentation that is
written in the module, class and method docstrings; as well as in the assert
methods.

All tests have to be written in folders named 'test/'.

Sardana Test Framework provides tools for testing macros. These tools comes 
from:
sardana/src/sardana/macroserver/macros/test/base.py
sardana/src/sardana/macroserver/macros/test/macroexecutor.py
sardana/src/sardana/macroserver/macros/test/sardemoenv.py
sardana/src/sardana/tango/macroserver/test/macroexecutor.py


base.py provides the mean of executing macros and test the function Run and
Stop for each macro. Macro test classes can inherit from RunMacroTestCase,
RunStopMacroTestCase or BaseMacroTestCase.

Macros as 'lsm' inherits from RunMacroTestCase as it is interesting to test
if the macros can be executed, but as they are fast macros, it is not
so interesting to test if they can be aborted.

However, scan macros inherits from RunStopMacroTestCase as it is interesting 
to test both: if the macros can be executed and if they can be aborted.

Another capacity provided by the Framework is the option to execute the 
same test method with many different macro input parameters. These is done 
by the help of a decorator inserted at the beginning of the test function.
One decorator has to be used for each set of macro input parameters. An 
example of the decorator usage can be seen in: test_scan.py



Examples of Sardana tests using tools of Sardana Test Framework are:

- sardana/src/sardana/test/test_sardanavalue.py 
- sardana/src/sardana/test/test_parameter.py
- sardana/src/sardana/macroserver/macros/test_ct.py
- sardana/src/sardana/macroserver/macros/test_list.py
- sardana/src/sardana/macroserver/macros/test_wm.py


"""
