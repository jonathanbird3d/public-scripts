# Proper way to do imports for maya with PySide2 according to official Maya documentation
# https://help.autodesk.com/view/MAYAUL/2017/ENU/?guid=__files_GUID_3F96AF53_A47E_4351_A86A_396E7BFD6665_htm
# Assumes you have access to some files provided by Autodesk in their Maya 2017 dev kit install
import sys
#sys.path.append('/some/path/')
import os
from maya import cmds, mel
from maya import OpenMayaUI as omui
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance

# To obtain the Maya main window widget as a PySide widget
omui.MQtUtil.mainWindow()
ptr = omui.MQtUtil.mainWindow()
widget = wrapInstance(long(ptr), QWidget)

# This demonstrates how to edit the style sheet to change the Maya background color
def changeMayaBackgroundColor(background='black', color='yellow'):
    widget.setStyleSheet(
        'background-color:%s;'%background +
        'color:%s;'%color
        )
changeMayaBackgroundColor()

# This demonstrates how to get a Maya cont
