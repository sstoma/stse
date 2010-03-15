#!/bin/python
import os
import string

filenames = os.listdir( os.curdir )
tiffs = []
for i in filenames:
    if i.find(".tiff") > -1:
        tiffs.append( i )
for i in tiffs:
    os.system("convert "+'\"'+i+'\"'+" "+'\"'+i.replace(".tiff", ".png")+'\"' )
