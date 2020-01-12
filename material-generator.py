# Getting Qt Modules
from PyQt4 import QtCore, QtGui, QtWidgets
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
        # self.defShadersBtn = QtWidgets.QPushButton("Apply Tech Blinn Shader")
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
        # self.main_layout.addWidget(self.defShadersBtn)
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
        # self.defShadersBtn.clicked.connect(self.applyTechBlinnShader)
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
        return [i for i in cmds.ls(selection=True) if cmds.ls(i, dagObjects=True, type='mesh', noIntermediate=True)]

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
        if len(list_of_meshes_missing_shaders != 0):
            # Some meshes do not have a random shader applied yet so call 
            # function to apply new shaders
            self.applyRandomShaders()

    def applyRandomShaders(self, *args):
        selection = self.getSelectedMeshes()
            for mesh in selection:
                # Does a random material exist for this object?
                if not cmds.objExists(mesh + '_rand_shdr'):
                    # Material doesn't exist so create random value for hue, saturation, value
                    h = random.uniform(0, 1)
                    s = random.uniform(0, 0.5)
                    v = random.uniform(0, 1)
                    # Create a shader named accordingly to this mesh
                    my_shdr = cmds.shadingNode(
                        self.shaderType,
                        asShader = True,
                        name = mesh + '_rand_shdr')
                else:
                    # A random shader already exists for this mesh.
                    # Check if the existing material is assigned to the mesh
                    the_nodes = cmds.ls(mesh, dagObjects = True, shapes = True)
                    shading_engine = cmds.listConnections(
                        the_nodes,
                        type = 'shadingEngine')
                    material = cmds.ls(cmds.listConnections(
                        shading_engine),
                        materials = True)
                    # If existing material is not assigned to this mesh, then assign it
                    if material != mesh + '_rand_shdr':
                        cmds.select(mesh)
                        cmds.hyperShade(assign = mesh + '_rand_shdr')
        cmds.select(selection)

    def setBlinn(self, *args):
        if self.blinnChkBox.isChecked():
            self.lambertChkBox.setChecked(False)
            self.shaderType = 'blinn'
                            
    def setLambert(self, *args):
        if self.lambertChkBox.isChecked():
            self.blinnChkBox.setChecked(False)
            self.shaderType = 'lambert'

    def applyDefaultLambert(self):
        selection = self.getSelectedMeshes()
        if cmds.objExists('lambert1')
            for mesh in selection:
                cmds.select(mesh)
                cmds.hyperShade(assign = 'lambert1')
            cmds.select(selection)
        else:
            cmds.warning('lambert1 shader does not exist')

    def reRollWireframe(self):
        selection = self.getSelectedMeshes()
        for mesh in selection:
            if cmds.getAttr(mesh+'.overrideEnabled') == False:
                try:
                    cmds.setAttr(mesh+'.overrideEnabled', True)
                except:
                    print('Could not set {0}.overrideEnabled to True'.format(mesh))

    def toggleWireframeOnShaded(self):
        if self.wireframeOnShaded == True:
            try:
                mel.eval('setWireframeOnshadedOption false modelPanel4')
                self.wireframeOnShaded = False
            except:
                cmds.warning('Could not toggle wireframe on shaded')
        else:
            try:
                mel.eval('setWireframeOnShadedOption true modelPanel4')
                self.wireframeOnShaded = True
            except:
                cmds.warning('Could not toggle wireframe on shaded')

    def toggleSelectionHighlighting(self, *args):
        if self.selectionHighlight == True:
            try:
                mel.eval("modelEditor -e -sel false modelPanel4")
                self.selectionHighlight = False
            except:
                cmds.warning('Could not toggle selection highlighting')
        else:
            try:
                mel.eval("modelEditor -e -sel true modelPanel4")
                self.selectionHighlight = True
            except:
                cmds.warning('Could not toggle selection highlighting')
