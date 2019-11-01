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

    def deleteUI(self, name):
        if cmds.window(name, exists=True):
            cmds.deleteUI(name)

    def getSelectedMeshes(self):
        # Get list of selected meshes and return them
        return [i for i in cmds.ls(sl=True) if cmds.ls(i, dag=1, type='mesh', ni=1)]
  
    def rerollHSV(self, *args):
        selection = self.getSelectedMeshes()
        list_of_meshes_missing_shaders = []
        for mesh in selection:
            # Check if shader already exists for currently selected mesh
            if not cmds.objExists(mesh + '_rand_shdr'):
                list_of_meshes_missing_shaders.append(mesh)
            else:
                h = random.uniform(0, 1)
                s = random.uniform(0, 0.5)
                v = random.uniform(0, 1)
                cmds.setAttr(mesh + '_rand_shdr' + '.color', h, s, v)
        if len(list_of_meshes_missing_shaders != 0:
            # Some meshes do not have a random shader applied yet so call 
            # function to apply new shaders
            self.applyRandomShaders()
           
    def applyTechBlinnShader(self, *args):
        selection = self.getSelectedMeshes()
        if cmds.objExists('deform_tech_blinn'):
            # Assign default tech blinn shader to mesh
            for mesh in selection:
                cmds.select(mesh)
                cmds.hyperShade(assign = 'deform_tech_blinn'
        else:
            # Re-visit this later, create the shader if it doesn't exist
            cmds.warning('deform_tech_blinn shader does not exist')
        cmds.select(selection)

                               
