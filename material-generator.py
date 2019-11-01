# Getting Qt Modules
from Qt import QtCore, QtGui, QtWidgets
# Getting Maya UI
from maya import OpenMayaUI
# Getting wrapInstance
from shiboken2 import wrapInstance
import random
from maya import cmds
from maya import mel

def main_maya_window():
  maya_window_ptr = OpenMayaUI.MQUtil.mainWindow()
  return wrapInstance(long(maya_window_ptr), QtWidgets.Qwidget)

class MaterialGenerator(QtWidgets.QDialog):
  def __init__(self, parent=None):
    super(MaterialGenerator, self).__init__(parent=main_maya_window())
    self.__init_ui__()
    self.__init_signal__()
    
    # Set some useful variables
    self.shaderType = 'lambert'
    self.wireframeOnShaded = False
    self.selectionHighlight = False
    
    # Need to define a maximum number of shaders allowed
    # If more than the maximum is needed, then we need to recycle old
    # shaders instead of creating millions of new ones
    
    def __init_ui__(self):
      # Define some stuff for the window
      self.setWindowTitle("Material Generator")
      self.setMinimumWidth(250)
      self.setMinimumHeight(50)
      self.setMaximumWidth(500)
      self.setMaximumHeight(600)
      
      # Define some layouts
      self.main_layout = QtWidgets.QVBoxLayout()
      self.btn_layout = QtWidgets.QVBoxLayout()
      self.check_box_layout = QtWidgets.QHBoxLayout()
      
      # Define some check boxes for lambert or blinn shaders
      self.blinnChxBox = QtWidgets.QCheckBox("Blinn")
      self.lambertChkBox = QtWidgets.QCheckBox("Lambert", checked = True)
      
      #Define a sort of horizontal spacer
      self.spacerFrame = QtWidgets.QFrame()
      
      # Define some buttons
      self.reRollBtn = QtWidgets.QPushButton("Re-roll Material Color")
      self.genShadersBtn = QtWidgets.QPushButton("Apply Random Shader")
      self.defShadersBtn = QtWidgets.QPushButton("Apply Tech Blinn Shader")
      self.defLambertBtn = QtWidgets.QPushButton("Apply Default lambert1 Shader")
      self.reRollOverrideBtn = QtWidgets.QPushButton("Re-roll Wireframe Color")
      self.toggleWireFrameOnShadedBtn = QtWidgets.QPushButton("Toggle Wireframe on Shaded")
      self.toggleSelectionHighlightingBtn = QtWidgets.QPushButton("Toggle Selection Highlighting")
      
      # Add elements to window
      self.main_layout.addLayout(self.check_box_layout)
      self.check_box_layout.addWidget(self.lambertChkBox)
      self.check_box_layout.addWidget(self.blinnChkBox)
      self.main_layout.addLayout(self.btn_layout)
      self.main_layout.addWidget(self.genShadersBtn)
      self.main_layout.addWidget(self.reRollBtn)
      self.main_layout.addWidget(self.spacerFrame)
      self.main_layout.addWidget(self.defShadersBtn)
      self.main_layout.addWidget(self.defLambertBtn)
      self.main_layout.addWidget(self.spacerFrame)
      self.main_layout.addWidget(self.toggleWireframeOnShadedBtn)
      self.main_layout.addWidget(self.reRollOverrideBtn)
      self.main_layout.addWidget(self.spacerFrame)
      self.main_layout.addWidget(self.toggleSelectionHighlightingBtn)
      self.setLayout(self.main_layout)
      
      #Show UI
      name = 'matGenWin'
      self.deleteUI(name)
      self.setObjectName(name)
      self.show()
      
  def __init_signal__(self):
    # Connect some UI actions to some functions
    self.reRollBtn.clicked.connect(self.rerollHSV)
    self.genShadersBtn.clicked.connect(self.applyRandomShaders)
    self.defShadersBtn.clicked.connect(self.applyTechBlinnShader)
    self.blinnChkBox.toggled.connect(self.setBlinn)
    self.lambertChkBox.toggled.connect(self.setLambert)
    self.defLambertBtn.clicked.connect(self.applyDefaultLambert)
    self.reRollOverrideBtn.clicked.connect(self.reRollWireframe)
    self.toggleWireframeOnShadedBtn.clicked.connect(self.toggleWreframeOnShaded)
    self.toggleSelectionHighlightingBtn.clicked.connect(self.toggleSelectionHighlighting)
      
      
      
      
      
      
      
      
      
      
      
      
