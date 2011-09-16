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

""" """

__all__ = ["EpsilonError", "State", "DataType", "DataFormat", "DataAccess",
           "DTYPE_MAP", "DACCESS_MAP", "from_dtype_str", "from_access_str",
           "to_dtype_dformat", "to_daccess"]

__docformat__ = 'restructuredtext'

from taurus.core.util import Enumeration

EpsilonError = 1E-9

State = Enumeration("State", ( \
    "On",
    "Off",
    "Close",
    "Open",
    "Insert",
    "Extract",
    "Moving",
    "Standby",
    "Fault",
    "Init",
    "Running",
    "Alarm",
    "Disable",
    "Unknown",
    "Invalid") )

DataType = Enumeration("DataType", ( \
    "Integer",
    "Double",
    "String",
    "Boolean",
    "Encoded",
    "Invalid") )
    
DataFormat = Enumeration("DataFormat", ( \
    "Scalar",
    "OneD",
    "TwoD",
    "Invalid") )
    
DataAccess = Enumeration("DataAccess", ( \
    "ReadOnly",
    "ReadWrite",
    "Invalid") )

#: dictionary dict<data type, :class:`sardana.DataType`>
DTYPE_MAP = { 
    'int'            : DataType.Integer,
    'integer'        : DataType.Integer,
    int              : DataType.Integer,
    long             : DataType.Integer,
    'long'           : DataType.Integer,
    DataType.Integer : DataType.Integer,
    'float'          : DataType.Double,
    'double'         : DataType.Double,
    float            : DataType.Double,
    DataType.Double  : DataType.Double,
    'str'            : DataType.String,
    'string'         : DataType.String,
    str              : DataType.String,
    DataType.String  : DataType.String,
    'bool'           : DataType.Boolean,
    'boolean'        : DataType.Boolean,
    bool             : DataType.Boolean,
    DataType.Boolean : DataType.Boolean,
}
#DTYPE_MAP.setdefault(DataType.Invalid)

#: dictionary dict<access type, :class:`sardana.DataAccess`>
DACCESS_MAP = { 
    'read'               : DataAccess.ReadOnly,
    DataAccess.ReadOnly  : DataAccess.ReadOnly,
    'readwrite'          : DataAccess.ReadWrite,
    'read_write'         : DataAccess.ReadWrite,
    DataAccess.ReadWrite : DataAccess.ReadWrite,
}
#DACCESS_MAP.setdefault(DataAccess.Invalid)

def from_dtype_str(dtype):
    dformat = DataFormat.Scalar
    if dtype is None:
        dtype = DataType.Double
    elif type(dtype) == str:
        dtype = dtype.lower()
        if dtype.startswith("pytango."):
            dtype = dtype[len("pytango."):]
        if dtype.startswith("dev"):
            dtype = dtype[len("dev"):]
        if dtype.startswith("var"):
            dtype = dtype[len("var"):]
        if dtype.endswith("array"):
            dtype = dtype[:dtype.index("array")]
            dformat = DataFormat.OneD
    return dtype, dformat

def from_access_str(access):
    if type(access) == str:
        access = access.lower()
        if access.startswith("pytango."):
            access = access[len("pytango."):]
    return access

def to_dtype_dformat(data):
    import operator
    dtype, dformat = data, DataFormat.Scalar
    if type(data) == str:
        dtype, dformat = from_dtype_str(data)
    elif operator.isSequenceType(data):
        dformat = DataFormat.OneD
        dtype = data[0]
        if type(dtype) == str:
            dtype, dformat2 = from_dtype_str(dtype)
            if dformat2 == DataFormat.OneD:
                dformat = DataFormat.TwoD
        elif operator.isSequenceType(dtype):
            dformat = DataFormat.TwoD
            dtype = dtype[0]
            if type(dtype) == str:
                dtype, _ = from_dtype_str(dtype)
    dtype = DTYPE_MAP.get(dtype, DataType.Invalid)
    return dtype, dformat

def to_daccess(data):
    daccess = DataAccess.Invalid
    if type(data) == str:
        daccess = DACCESS_MAP.get(from_access_str(data), DataAccess.ReadWrite)
    return daccess