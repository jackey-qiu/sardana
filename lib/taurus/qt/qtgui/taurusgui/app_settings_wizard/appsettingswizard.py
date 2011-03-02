#!/usr/bin/env python

#############################################################################
##
## This file is part of Taurus, a Tango User Interface Library
## 
## http://www.tango-controls.org/static/taurus/latest/doc/html/index.html
##
## Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
## 
## Taurus is free software: you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## Taurus is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
## 
## You should have received a copy of the GNU Lesser General Public License
## along with Taurus.  If not, see <http://www.gnu.org/licenses/>.
##
###########################################################################

"""
This Wizard provide functionality of creation of configuration file 
for constructing a GUI based on TaurusGUI  

The configuration file determines the default, permanent, pre-defined
contents of the GUI. While the user may add/remove more elements at run
time and those customizations will also be stored, this file defines what a
user will find when launching the GUI for the first time.
"""

import os, sys, shutil
from PyQt4 import Qt
import taurus.qt.qtgui.resource
import taurus.qt.qtgui.extra_macroexecutor.common
import taurus.qt.qtgui.panel
import taurus.qt.qtgui.taurusgui.paneldescriptionwizard
import taurus.qt.qtgui.input
import copy
from taurus.core.util import etree
from taurus.core.util import Enumeration
from taurus.qt.qtgui.util import ExternalAppAction
        

        
class BooleanWidget(Qt.QWidget):
    """
        This class represents the simple boolean widget with two RadioButtons
        true and false. The default value of the widget is true.
        It change the value by using getValue and setValue methods
    """
    
    def __init__(self, parent=None):
        Qt.QWidget.__init__(self,parent)
        self._formLayout = Qt.QHBoxLayout(self)
        self.trueButton = Qt.QRadioButton(self)
        self._formLayout.addWidget(self.trueButton)
        self.falseButton = Qt.QRadioButton(self)
        self._formLayout.addWidget(self.falseButton)
        self.trueButton.setText("Yes")
        self.falseButton.setText("No")
        Qt.QObject.connect(self.trueButton, Qt.SIGNAL("clicked()"), self.valueChanged)
        Qt.QObject.connect(self.falseButton, Qt.SIGNAL("clicked()"), self.valueChanged)
        self.setValue(self.getDefaultValue(), undo=False)

    def valueChanged(self):
        if not (self.trueButton.isChecked() == self._actualValue):
            self.emit(Qt.SIGNAL("valueChanged"),self._actualValue,not self._actualValue)
        self._actualValue = self.trueButton.isChecked()
    
    def setValue(self, value, undo=False):
        if value is None:
            value = self.getDefaultValue()
        self.trueButton.setChecked(value)
        self.falseButton.setChecked(not value)
        self._actualValue = value
       
    def getValue(self):
        return self.trueButton.isChecked()
    
    @classmethod 
    def getDefaultValue(self):
        return False


class BasePage(Qt.QWizardPage):
    """
        This class represents the base page for all of the pages in the wizard
    """
    
    def __init__(self, parent = None):
        Qt.QWizardPage.__init__(self, parent)
        self._item_funcs = {}
        self._layout = Qt.QGridLayout()  
        self.setLayout(self._layout)
        self._setupUI()
        
    def initializePage(self):
        Qt.QWizardPage.initializePage(self)
        self.checkData()
        
    def fromXml(self, xml):
        """
        :param xml: (etree.Element) root node
        """
        pass
    
    def _setupUI(self):
        pass
        
    def __setitem__(self, name, value):
        self._item_funcs[name] = value

    def __getitem__(self, name):
        return self._item_funcs[name]
        
    def checkData(self):
        self._valid = True
        self.emit(Qt.SIGNAL('completeChanged()'))
        
    def isComplete(self):
        return self._valid

    def _markRed(self, label):
        """
            Set the color of the given label to red
        """
        palette = label.palette()
        palette.setBrush(Qt.QPalette.WindowText, Qt.Qt.red)
        label.update()
        
    def _markBlack(self, label):
        """
            Set the color of the given label to black
        """
        palette = label.palette()
        palette.setBrush(Qt.QPalette.WindowText, Qt.Qt.black)
        label.update()

    def setStatusLabelPalette(self, label):
        """
            Set the label look as as status label
        """
        label.setAutoFillBackground(True)
        palette = label.palette()
        gradient = Qt.QLinearGradient(0, 0, 0, 15)
        gradient.setColorAt(0.0, Qt.QColor.fromRgb( 60, 150, 255))
        gradient.setColorAt(0.5, Qt.QColor.fromRgb(  0,  85, 227))
        gradient.setColorAt(1.0, Qt.QColor.fromRgb( 60, 150, 255))
        gradient.setSpread(Qt.QGradient.RepeatSpread)
        palette.setBrush(Qt.QPalette.Window, Qt.QBrush(gradient))
        palette.setBrush(Qt.QPalette.WindowText, Qt.Qt.white)

    def __setitem__(self, name, value):
        self._item_funcs[name] = value

    def __getitem__(self, name):
        return self._item_funcs[name]
  
    def setNextPageId(self, id):
        self._nextPageId = id
        
    def nextId(self):
        return self._nextPageId


class IntroPage(BasePage):
    """
        Introduction page
    """
    
    def __init__(self, parent = None):
        BasePage.__init__(self, parent)
        
    def _setupUI(self): 
        self.setTitle('Introduction')
        self.setPixmap(Qt.QWizard.WatermarkPixmap, taurus.qt.qtgui.resource.getThemeIcon("document-properties").pixmap(120,120))
        label = Qt.QLabel(self.getIntroText())
        label.setWordWrap(True)
        self._layout.addWidget(label,0,0)
        self._spacerItem1 = Qt.QSpacerItem(10, 200, Qt.QSizePolicy.Minimum, Qt.QSizePolicy.Fixed)  
        self._layout.addItem(self._spacerItem1,1,0)
        self.setLayout(self._layout)
        
    def getIntroText(self):
        text = 'This wizard will guide you through the process of creating a '+\
               'GUI based on TaurusGUI.\n' +\
               'TaurusGui-based applications are very customizable. The user can ' +\
               'add/remove elements at run time and store those customizations. So ' +\
               'with this wizard you will define just the default contents of the GUI.' 
        return text
    
    def setNextPageId(self, id):
        self._nextPageId = id
        
        
class ProjectPage(BasePage):
    
    def __init__(self, parent = None):
        BasePage.__init__(self, parent)
        self.setTitle('Project')
        self.setSubTitle('Choose a location for the application files (i.e., the "project directory")')
        self.__setitem__('projectDir', self._getProjectDir)
        

    def _setupUI(self):
        BasePage._setupUI(self)
        self._projectDirLabel = Qt.QLabel("Project Directory:")
        self._projectDirLE = Qt.QLineEdit(Qt.QDir.homePath())
        self._projectDirLE.setMinimumSize(150, 30)
        self._projectDirLE.setToolTip('This directory will be used to store all files needed by the application.')
        self._projectDirBT = Qt.QPushButton(taurus.qt.qtgui.resource.getThemeIcon("document-properties"), '...')
        self._layout.addWidget(self._projectDirLabel,1,0)
        self._layout.addWidget(self._projectDirLE,1,1)
        self._layout.addWidget(self._projectDirBT,1,2)
                
        Qt.QObject.connect(self._projectDirBT, Qt.SIGNAL("clicked()"), self.onSelectDir)       
        
    def onSelectDir(self):
        dirname = Qt.QFileDialog.getExistingDirectory(self, 'Choose the project directory', self._projectDirLE.text())
        if dirname.isNull(): return
        self._projectDirLE.setText(dirname)
        
    def validatePage(self):
        dirname = unicode(self._projectDirLE.text())
        
        if not os.path.exists(dirname):
            Qt.QDir().mkpath(Qt.QString(dirname) )
        fname = os.path.join(dirname, self.wizard().CONFIGFILENAME)
        if os.path.exists(fname):
            option = Qt.QMessageBox.question(self, 'Overwrite project?', 
                                    'The "%s" file already exists in the project directory.\n Do you want to edit the existing project?'%(os.path.basename(fname)),
                                     Qt.QMessageBox.Yes|Qt.QMessageBox.Cancel)
            if option == Qt.QMessageBox.Yes:
                try:
                    self.wizard().loadXml(fname)
                except Exception, e:
                    Qt.QMessageBox.warning(self, 'Error loading project configuration', 
                                    'Could not load the existing configuration.\nReason:%s'%repr(e),
                                     Qt.QMessageBox.Cancel)
                    return False
            else:
                return False
        elif len(os.listdir(dirname)):
            option = Qt.QMessageBox.question(self, 'Non empty project dir', 
                                    'The project directory ("%s") is not empty.\nAre you sure you want to use it?'%(os.path.basename(dirname)),
                                     Qt.QMessageBox.Yes|Qt.QMessageBox.No)
            if option != Qt.QMessageBox.Yes:
                return False
        #if all went ok...
        return True
    
    def _getProjectDir(self):
        return unicode(self._projectDirLE.text())
        
           
class GeneralSettings(BasePage):
    
    def __init__(self, parent = None):
        BasePage.__init__(self, parent)
        self.setTitle('General settings')

    def initializePage(self):
        BasePage.initializePage(self)
        self.wizard().__setitem__("guiName",self._getGUIName)
        self.wizard().__setitem__("organizationName",self._getOrganizationName)
        
    def fromXml(self,xml):
        guiName = AppSettingsWizard.getValueFromNode(xml, "GUI_NAME", default=None)
        organizationName = AppSettingsWizard.getValueFromNode(xml, "ORGANIZATION", default=None)

        if guiName is not None and len(guiName):
            self._guiNameLineEdit.setText(guiName)
        else:
            self._guiNameLineEdit.setText("")
            
        if organizationName is not None and len(organizationName):
            self._organizationCombo.setEditText(organizationName)
        else:
            self._organizationCombo.setCurrentIndex(0)
        
    def _getGUIName(self):
        return str(self._guiNameLineEdit.text())
    
    def _getOrganizationName(self):
        if len(self._organizationCombo.currentText())>0:
            return str(self._organizationCombo.currentText())
        else:
            return None
        
    def _setupUI(self):
        BasePage._setupUI(self)
        self._guiNameLabel = Qt.QLabel("GUI name:")
        font = Qt.QFont() #set bigger font 
        font.setPointSize(14)
        
        self._label = Qt.QLabel()
        self._layout.addWidget(self._label,0,0,1,2,Qt.Qt.AlignRight)
        self._guiNameLineEdit = Qt.QLineEdit()
        self._guiNameLineEdit.setFont(font)
        self._guiNameLineEdit.setMinimumSize(150, 30)
        self._layout.addWidget(self._guiNameLabel,1,0,1,1,Qt.Qt.AlignRight)
        self._layout.addWidget(self._guiNameLineEdit,1,1,1,1,Qt.Qt.AlignRight)
        self._organizationNameLabel = Qt.QLabel("Organization name:")
        self._organizationCombo = Qt.QComboBox()
        self._organizationCombo.addItems(self._getOrganizationNames())
        self._organizationCombo.setMinimumSize(150, 25)
        self._organizationCombo.setEditable(True)
        self._layout.addWidget(self._organizationNameLabel,2,0,1,1,Qt.Qt.AlignRight)
        self._layout.addWidget(self._organizationCombo,2,1,1,1,Qt.Qt.AlignRight)

        
        self._spacerItem1 = Qt.QSpacerItem(10, 0, Qt.QSizePolicy.Fixed, Qt.QSizePolicy.Expanding)
        self._layout.addItem(self._spacerItem1,8,0,1,1,Qt.Qt.AlignCenter)
        self._status_label = Qt.QLabel()
        self.setStatusLabelPalette(self._status_label)
        self._layout.addWidget(self._status_label,9,0,1,3)
        
        Qt.QObject.connect(self._guiNameLineEdit, Qt.SIGNAL("textChanged(const QString&)"), self.checkData)
        Qt.QObject.connect(self._organizationCombo, Qt.SIGNAL("editTextChanged(const QString&)"), self.checkData)
        Qt.QObject.connect(self._organizationCombo, Qt.SIGNAL("currentIndexChanged(const QString&)"), self.checkData)
        
    def _getOrganizationNames(self):
        return ["TAURUS","ALBA", "DESY", "Elettra", "ESRF", "MAX-lab", "SOLEIL", "XFEL"]         

    def checkData(self):
        self._valid = True
        if not len(self._guiNameLineEdit.text()):
            self._valid = False
            self._markRed(self._guiNameLabel)
        else:
            self._markBlack(self._guiNameLabel)
            
        self.emit(Qt.SIGNAL('completeChanged()'))
        
        if not self._valid:
            self._setStatus("Please type the name of the GUI")
        else:
            self._setStatus("Press next button to continue")   

    def _setStatus(self,text):
        self._status_label.setText(text)
        

class CustomLogoPage(BasePage):
    def __init__(self, parent = None):
        BasePage.__init__(self, parent)
        self._customLogoDefaultPath=":/logo.png"
        self._customLogoPath=self._customLogoDefaultPath
        
    def initializePage(self):
        BasePage.initializePage(self)
        self.wizard().__setitem__("customLogo",self._getCustomLogo)
        self._changeImage()
    
    def _setupUI(self):
        BasePage._setupUI(self)
        self.setTitle('Custom logo')
        self._label = Qt.QLabel("\nIf you want to have a custom logo inside your application panel, please select the image file. \n")
        self._label.setWordWrap(True)
        self._layout.addWidget(self._label,0,0,1,4) 
        self._customLogoLabel = Qt.QLabel("Custom logo:")
        self._customLogoLineEdit = Qt.QLineEdit()
        self._customLogoLineEdit.setMinimumSize(250, 25)
        self._customLogoLineEdit.setReadOnly(False)
        self._customLogoButton = Qt.QPushButton()
        self._customLogoButton.setToolTip("Browse...")
        self._customLogoButton.setIcon(taurus.qt.qtgui.resource.getThemeIcon("folder-open"))
        self._customLogoButton.setMaximumSize(80, 25)
        self._spacerItem1 = Qt.QSpacerItem(30, 30, Qt.QSizePolicy.Fixed, Qt.QSizePolicy.Fixed)  
        self._customLogo = Qt.QLabel(self)
        self._customLogo.setAlignment(Qt.Qt.AlignCenter)
        self._customLogo.setMinimumSize(120, 120)
        self._customLogoDefaultButton = Qt.QPushButton()
        self._customLogoDefaultButton.setToolTip("Default")
        self._customLogoDefaultButton.setMaximumSize(80, 25)
        self._customLogoDefaultButton.setIcon(taurus.qt.qtgui.resource.getIcon(":/actions/edit-undo.svg"))
        self._customLogoRemoveButton = Qt.QPushButton()
        self._customLogoRemoveButton.setToolTip("Remove")
        self._customLogoRemoveButton.setMaximumSize(80, 25)
        self._customLogoRemoveButton.setIcon(taurus.qt.qtgui.resource.getIcon(":/emblems/emblem-unreadable.svg"))
        self._spacerItem2 = Qt.QSpacerItem(30, 30, Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Fixed)  

        self._layout.addWidget(self._customLogoLabel,2,0,Qt.Qt.AlignRight)
        self._layout.addWidget(self._customLogoLineEdit,2,1,Qt.Qt.AlignRight)
        self._layout.addWidget(self._customLogoButton,2,2,Qt.Qt.AlignLeft)
        self._layout.addWidget(self._customLogoDefaultButton,2,3,Qt.Qt.AlignLeft)
        self._layout.addWidget(self._customLogoRemoveButton,2,4,Qt.Qt.AlignLeft) 
        self._layout.addItem(self._spacerItem2,2,5)
        self._layout.addItem(self._spacerItem1,3,2)
        self._layout.addWidget(self._customLogo,4,1,1,1,Qt.Qt.AlignHCenter)
             
        Qt.QObject.connect(self._customLogoButton, Qt.SIGNAL("clicked()"), self._selectImage)
        Qt.QObject.connect(self._customLogoDefaultButton, Qt.SIGNAL("clicked()"), self._setDefaultImage)
        Qt.QObject.connect(self._customLogoRemoveButton, Qt.SIGNAL("clicked()"), self._removeImage)
        Qt.QObject.connect(self._customLogoLineEdit, Qt.SIGNAL("textChanged(const QString&)"), self._changeImage)
        
        self._spacerItem1 = Qt.QSpacerItem(10, 0, Qt.QSizePolicy.Fixed, Qt.QSizePolicy.Expanding)
        self._layout.addItem(self._spacerItem1,8,0,1,1,Qt.Qt.AlignCenter)
        self._status_label = Qt.QLabel("Press next button to continue")
        self.setStatusLabelPalette(self._status_label)
        self._layout.addWidget(self._status_label,9,0,1,6)
        self._setNoImage()
    
    def fromXml(self, xml):
        customLogo = AppSettingsWizard.getValueFromNode(xml, "CUSTOM_LOGO", default=None)
        if customLogo is not None and len(customLogo):
            self._customLogoLineEdit.setText(customLogo)
        else:
            self._setDefaultImage()
        
    def _setDefaultImage(self):
        self._customLogoLineEdit.setText(self._customLogoDefaultPath)
        
    def _setNoImage(self):
        self._customLogo.setPixmap(taurus.qt.qtgui.resource.getThemePixmap("image-missing").scaled(50,50))
        self._customLogoPath=None
        self._customLogoRemoveButton.hide()
    
    def _removeImage(self):
        self._customLogoLineEdit.setText("")
        self._setNoImage()
    
    def _getCustomLogo(self):
        if (self._customLogoPath is not None):
            return str(self._customLogoPath)
        else:
            return None
                
    def _selectImage(self):
            fileName = Qt.QFileDialog.getOpenFileName(self, self.tr("Open File"), Qt.QDir.homePath() , self.tr("Images (*.png *.xpm *.jpg *.jpeg)"))
            self._customLogoLineEdit.setText(fileName)
            self._changeImage()
        
    def _changeImage(self):
        fileName = str(self._customLogoLineEdit.text())
        if (len(fileName)):
            if  fileName[0]==":":
                pixmap =taurus.qt.qtgui.resource.getPixmap(fileName)
                if ( pixmap.height()):
                    image = pixmap.toImage()
                    self._setImage(image)
                    self._customLogoPath = fileName
                    self._setStatus("Press next button to continue")
                    self._customLogoRemoveButton.show()
                else:
                    self._setNoImage()
                    self._setStatus("The resource is invalid")    
            else:
                if (os.path.exists(fileName)):
                    image = Qt.QImage()
                    if image.load(fileName):
                        self._setImage(image)
                        self._customLogoPath = fileName
                        self._setStatus("Press next button to continue")
                        self._customLogoRemoveButton.show() 
                    else:
                        self._setNoImage()
                        self._setStatus("The file is invalid")
                else:
                    self._setNoImage()
                    self._setStatus("The file does not exist")
        else:
            self._setNoImage()
            self._setStatus("No image")
        
        
    def _setImage(self, image):     
        if type(image)==Qt.QPixmap:
            self._customLogo.setPixmap(image.scaled(60,200,Qt.Qt.KeepAspectRatio))
        elif type(image)==Qt.QImage:
            self._customLogo.setPixmap(Qt.QPixmap().fromImage(image).scaled(60,200,Qt.Qt.KeepAspectRatio))
        else:
            self._customLogo.setPixmap(taurus.qt.qtgui.resource.getThemePixmap("image-missing").scaled(50,50))
            self._customLogoPath = None
            
    def _setStatus(self,text):
        self._status_label.setText(text)
        

class SynopticPage(BasePage):  
    def __init__(self, parent = None):
        BasePage.__init__(self, parent)
        self._synoptics = []
        
    def fromXml(self, xml):
        self._synoptics=[]
        synopticNodes = AppSettingsWizard.getArrayFromNode(xml, "SYNOPTIC", default=None)
        if synopticNodes is not None:
            for child in synopticNodes:
                if child.get("str") is not None and len(child.get("str")):
                        self._synoptics.append(child.get("str"))
        
    def initializePage(self):
        BasePage.initializePage(self)
        self.wizard().__setitem__("synoptics",self._getSynoptics)
        self._refreshSynopticList()
        
    def _setupUI(self):
        BasePage._setupUI(self)
        self.setTitle('Synoptics')
        self._label = Qt.QLabel("If you want to add one or more synoptic panels (graphical views of instruments) select the corresponding JDRAW files here\n")
        self._label.setWordWrap(True)
        self._layout.addWidget(self._label,0,0)
        self.setLayout(self._layout)
        self._synopticGroupBox = Qt.QGroupBox()
        self._synopticGroupBox.setCheckable(False)
        self._synopticGroupBox.setAlignment(Qt.Qt.AlignLeft)
        self._synopticGroupBox.setStyleSheet(" QGroupBox::title {  subcontrol-position: top left; padding: 5 5px; }")
        self._layout.addWidget(self._synopticGroupBox,2,0,1,1)
        self._horizontalLayout = Qt.QHBoxLayout(self._synopticGroupBox)
        self._synopticList = Qt.QListWidget(self._synopticGroupBox)
        self._horizontalLayout.addWidget(self._synopticList)
        self._verticalLayout = Qt.QVBoxLayout()
        self._addButton = Qt.QPushButton("Add Synoptic")
        self._addButton.setStyleSheet("text-align: left;")
        self._verticalLayout.addWidget(self._addButton)
        self._removeButton = Qt.QPushButton("Remove Synoptic")
        self._removeButton.setStyleSheet("text-align: left;")
        self._verticalLayout.addWidget(self._removeButton)
        self._upButton = Qt.QPushButton("Move Up")
        self._upButton.setStyleSheet("text-align: left;")
        self._verticalLayout.addWidget(self._upButton)
        self._downButton = Qt.QPushButton("Move Down")
        self._downButton.setStyleSheet("text-align: left;")
        self._verticalLayout.addWidget(self._downButton)
        self._horizontalLayout.addLayout(self._verticalLayout)
        self._addButton.setIcon(taurus.qt.qtgui.resource.getThemeIcon("list-add"))
        self._removeButton.setIcon(taurus.qt.qtgui.resource.getThemeIcon("list-remove"))
        self._upButton.setIcon(taurus.qt.qtgui.resource.getThemeIcon("go-up"))
        self._downButton.setIcon(taurus.qt.qtgui.resource.getThemeIcon("go-down"))
        Qt.QObject.connect(self._addButton, Qt.SIGNAL("clicked()"), self._addSynoptic)
        Qt.QObject.connect(self._removeButton, Qt.SIGNAL("clicked()"), self._removeSynoptic)
        Qt.QObject.connect(self._upButton, Qt.SIGNAL("clicked()"), self._moveUp)
        Qt.QObject.connect(self._downButton, Qt.SIGNAL("clicked()"), self._moveDown)
        #Qt.QObject.connect(self._synopticList, Qt.SIGNAL("itemDoubleClicked(QListWidgetItem*)"), self._editSynoptic) 
        self._spacerItem1 = Qt.QSpacerItem(10, 0, Qt.QSizePolicy.Fixed, Qt.QSizePolicy.Expanding)
        self._layout.addItem(self._spacerItem1,8,0,1,1,Qt.Qt.AlignCenter)
        self._status_label = Qt.QLabel("Press next button to continue")
        self.setStatusLabelPalette(self._status_label)
        self._layout.addWidget(self._status_label,9,0,1,1)
        
    
    def _addSynoptic (self):
        pdir = self.wizard().__getItem__('projectDir')
        fileNames = Qt.QFileDialog.getOpenFileNames(self, self.tr("Open File"), pdir, self.tr("JDW (*.jdw );; All files (*)")  )
        for fileName in fileNames:
            fileName = unicode(fileName)
            if not fileName in self._synoptics:
                self._synoptics.append(fileName)
        self._refreshSynopticList()
        
    def _editSynoptic (self):
        # edit
        self._refreshSynopticList()
            
    def _removeSynoptic(self):
        if len(self._synopticList.selectedIndexes())>0:
            self._synoptic_id=self._synopticList.selectedIndexes()[0].row()
            self._synoptics.remove(self._synoptics[self._synoptic_id])
            self._refreshSynopticList()
            
    def _moveUp(self):
        if len(self._synopticList.selectedIndexes())>0:
            self._synoptic_id=self._synopticList.selectedIndexes()[0].row()
            if self._synoptic_id > 0:
                tmp =  self._synoptics[self._synoptic_id]
                self._synoptics[self._synoptic_id]=self._synoptics[self._synoptic_id-1]
                self._synoptics[self._synoptic_id-1]=tmp
                self._refreshSynopticList()
                self._synopticList.setCurrentIndex(self._synopticList.indexFromItem(self._synopticList.item(self._synoptic_id-1) ))
                
    def _moveDown(self):
        if len(self._synopticList.selectedIndexes())>0:
            self._synoptic_id=self._synopticList.selectedIndexes()[0].row()
            if self._synoptic_id < self._synopticList.count()-1:
                tmp =  self._synoptics[self._synoptic_id]
                self._synoptics[self._synoptic_id]=self._synoptics[self._synoptic_id+1]
                self._synoptics[self._synoptic_id+1]=tmp
                self._refreshSynopticList()
                self._synopticList.setCurrentIndex(self._synopticList.indexFromItem(self._synopticList.item(self._synoptic_id+1) ))
              
    def _refreshSynopticList(self):
        self._synopticList.clear()
        for name in self._synoptics:
            self._synopticList.addItem(name)
            
    def _getSynoptics(self):
        if len(self._synoptics)<=0:
            return None
        else:
            return self._synoptics
        
    def checkData(self):
        BasePage.checkData(self)          
        self._valid=True
    
    def _setStatus(self,text):
        self._status_label.setText(text)


class MacroServerInfoPage(BasePage):
    
    def __init__(self, parent = None):
        BasePage.__init__(self, parent)
    
    def initializePage(self):
        BasePage.initializePage(self)
        self._label.setText("\n <b>%s</b> can communicate with a Sardana's Macro Server and Pool.\nYou can enable and configure them here:\n" % self.wizard().__getitem__("guiName"))
        self.wizard().__setitem__("macroServerName",self._getMacroServerName)
        self.wizard().__setitem__("doorName",self._getDoorName)
        
    def _setupUI(self):
        BasePage._setupUI(self)
        self.setTitle('Macro Server Info')
        self._label = Qt.QLabel()
        self._label.setWordWrap(True)
        self._macroGroupBox = Qt.QGroupBox()
        self._macroGroupBox.setTitle("Enable Sardana communication")
        self._macroGroupBox.setCheckable(True)
        self._macroGroupBox.setChecked(False)
        self._macroGroupBox.setAlignment(Qt.Qt.AlignLeft)
        self._macroGroupBox.setStyleSheet(" QGroupBox::title {  subcontrol-position: top left; padding: 5 5px; }")
        self._horizontalLayout = Qt.QHBoxLayout(self._macroGroupBox)
        self._confWidget = taurus.qt.qtgui.extra_macroexecutor.common.TaurusMacroConfigurationDialog(self)
        self._confWidget.setWindowFlags(Qt.Qt.Widget)
        self._confWidget.setModal(False)
        self._confWidget.setVisible(True)
        self._confWidget.buttonBox.setVisible(False)
        self._horizontalLayout.addWidget(self._confWidget)
        
        self._layout.addWidget(self._label,0,0,1,1)
        self._layout.addWidget(self._macroGroupBox,1,0,1,1) 
        
        self._spacerItem1 = Qt.QSpacerItem(10, 0, Qt.QSizePolicy.Fixed, Qt.QSizePolicy.Expanding)
        self._layout.addItem(self._spacerItem1,8,0,1,1,Qt.Qt.AlignCenter)
        self._status_label = Qt.QLabel("Press next button to continue")
        self.setStatusLabelPalette(self._status_label)
        self._layout.addWidget(self._status_label,9,0,1,1)
        
        Qt.QObject.connect(self._confWidget.macroServerComboBox, Qt.SIGNAL("currentIndexChanged(const QString&)"), self.checkData)
        Qt.QObject.connect(self._confWidget.doorComboBox, Qt.SIGNAL("currentIndexChanged(const QString&)"), self.checkData)
        Qt.QObject.connect(self._macroGroupBox, Qt.SIGNAL("toggled(bool)"), self.checkData)
    
    def fromXml(self, xml):
        
        macroserverName = AppSettingsWizard.getValueFromNode(xml, "MACROSERVER_NAME", default=None)
        doorName = AppSettingsWizard.getValueFromNode(xml, "DOOR_NAME", default="")
        macroEditorsPath = AppSettingsWizard.getValueFromNode(xml, "MACROEDITORS_PATH", default="")
        
        if macroserverName is not None and len(macroserverName):
            id = self._confWidget.macroServerComboBox.findText( macroserverName, Qt.Qt.MatchExactly)
            if id >=0:
                self._confWidget.macroServerComboBox.setCurrentIndex(id)
                self._macroGroupBox.setChecked(True)
            else:
                self._macroGroupBox.setChecked(False)
                return
        
        #print self._confWidget.doorComboBox.itemText(1)
        #print doorName
        
        if doorName is not None and len(doorName):
            id = self._confWidget.doorComboBox.findText( doorName, Qt.Qt.MatchExactly)
            if id >=0:
                self._confWidget.doorComboBox.setCurrentIndex(id)
                
        #print self._confWidget.doorComboBox.currentText()
        
    def checkData(self):
        BasePage.checkData(self)
        if (self._macroGroupBox.isChecked()) and len(self._confWidget.macroServerComboBox.currentText()):
            self.setNextPageId(self.wizard().currentId()+1)
        else:
            self.setNextPageId(self.wizard().currentId()+2)
          
    def _getMacroServerName(self):
        if (self._macroGroupBox.isChecked()) and len(self._confWidget.macroServerComboBox.currentText()):
            return str(self._confWidget.macroServerComboBox.currentText())
        else:
            return None
    
    def _getDoorName(self):
        if (self._macroGroupBox.isChecked()) and len(self._confWidget.macroServerComboBox.currentText()):
            return str(self._confWidget.doorComboBox.currentText())
        else:
            return None

    def _setStatus(self,text):
        self._status_label.setText(text)
        
           
class InstrumentsPage(BasePage):
    def __init__(self, parent = None):
        BasePage.__init__(self, parent)
        
    def initializePage(self):
        BasePage.initializePage(self)
        self.wizard().__setitem__("instruments",self._getInstruments)
        self._label.setText("<b>%s</b> can use instrument information stored in the Sardana's Pool to create instrument panels." % self.wizard().__getitem__("guiName"))
        
    def _setupUI(self):
        BasePage._setupUI(self)
        self.setTitle('Instruments from Pool:')
        self._label = Qt.QLabel()
        self._label.setWordWrap(True)
        self._layout.addWidget(self._label,0,0,1,3)
        
        self._instrumentsLabel = Qt.QLabel("Generate panels from Pool Info?")
        self._intstrumentsBoolean = BooleanWidget()
        self._intstrumentsBoolean.setMinimumSize(150, 25)
        self._layout.addWidget(self._instrumentsLabel,5,0,1,1,Qt.Qt.AlignRight)
        self._layout.addWidget(self._intstrumentsBoolean,5,1,1,1,Qt.Qt.AlignRight)
        
        self._spacerItem1 = Qt.QSpacerItem(10, 0, Qt.QSizePolicy.Fixed, Qt.QSizePolicy.Expanding)
        self._layout.addItem(self._spacerItem1,8,0,1,1,Qt.Qt.AlignCenter)
        self._status_label = Qt.QLabel("Press next button to continue")
        self.setStatusLabelPalette(self._status_label)
        self._layout.addWidget(self._status_label,9,0,1,3)
        
    def _getInstruments(self):
        return str(self._intstrumentsBoolean.getValue())
        
    def checkData(self):
        self._valid=True
    
    def _setStatus(self,text):
        self._status_label.setText(text)
        
    
class PanelsPage(BasePage):
    
    def __init__(self, parent = None):
        BasePage.__init__(self, parent)
        self._panels = []
        
    def initializePage(self):
        BasePage.initializePage(self)
        self.wizard().__setitem__("panels",self._getPanels)
        self._refreshPanelList()
        
    def _setupUI(self):
        BasePage._setupUI(self)
        self.setTitle('Panels editor')
        self._label = Qt.QLabel("If you want extra panels add them to this list\n")
        self._layout.addWidget(self._label,0,0)
        self.setLayout(self._layout)
        self._panelGroupBox = Qt.QGroupBox()
        self._panelGroupBox.setCheckable(False)
        self._panelGroupBox.setAlignment(Qt.Qt.AlignLeft)
        self._panelGroupBox.setStyleSheet(" QGroupBox::title {  subcontrol-position: top left; padding: 5 5px; }")
        self._layout.addWidget(self._panelGroupBox,2,0,1,1)
        self._horizontalLayout = Qt.QHBoxLayout(self._panelGroupBox)
        self._panelList = Qt.QListWidget(self._panelGroupBox)
        self._horizontalLayout.addWidget(self._panelList)
        self._verticalLayout = Qt.QVBoxLayout()
        self._addButton = Qt.QPushButton("Add Panel")
        self._addButton.setStyleSheet("text-align: left;")
        self._verticalLayout.addWidget(self._addButton)
        self._removeButton = Qt.QPushButton("Remove Panel")
        self._removeButton.setStyleSheet("text-align: left;")
        self._verticalLayout.addWidget(self._removeButton)
        self._upButton = Qt.QPushButton("Move Up")
        self._upButton.setStyleSheet("text-align: left;")
        self._verticalLayout.addWidget(self._upButton)
        self._downButton = Qt.QPushButton("Move Down")
        self._downButton.setStyleSheet("text-align: left;")
        self._verticalLayout.addWidget(self._downButton)
        self._horizontalLayout.addLayout(self._verticalLayout)
        self._addButton.setIcon(taurus.qt.qtgui.resource.getThemeIcon("list-add"))
        self._removeButton.setIcon(taurus.qt.qtgui.resource.getThemeIcon("list-remove"))
        self._upButton.setIcon(taurus.qt.qtgui.resource.getThemeIcon("go-up"))
        self._downButton.setIcon(taurus.qt.qtgui.resource.getThemeIcon("go-down"))
        Qt.QObject.connect(self._addButton, Qt.SIGNAL("clicked()"), self._addPanel)
        Qt.QObject.connect(self._removeButton, Qt.SIGNAL("clicked()"), self._removePanel)
        Qt.QObject.connect(self._upButton, Qt.SIGNAL("clicked()"), self._moveUp)
        Qt.QObject.connect(self._downButton, Qt.SIGNAL("clicked()"), self._moveDown)
        Qt.QObject.connect(self._panelList, Qt.SIGNAL("itemDoubleClicked(QListWidgetItem*)"), self._editPanel) 
        self._spacerItem1 = Qt.QSpacerItem(10, 0, Qt.QSizePolicy.Fixed, Qt.QSizePolicy.Expanding)
        self._layout.addItem(self._spacerItem1,8,0,1,1,Qt.Qt.AlignCenter)
        self._status_label = Qt.QLabel("Press next button to continue")
        self.setStatusLabelPalette(self._status_label)
        self._layout.addWidget(self._status_label,9,0,1,1)
        
    def _addPanel (self):
        paneldesc,ok = taurus.qt.qtgui.taurusgui.paneldescriptionwizard.PanelDescriptionWizard.getDialog(self)
        if ok:
            w = paneldesc.getWidget()
            self._panels.append((paneldesc.name,paneldesc.toXml()))
            
        self._refreshPanelList()
        
    def _editPanel (self):
        # edit
        self._refreshPanelList()
            
    def _removePanel(self):
        if len(self._panelList.selectedIndexes())>0:
            self._panel_id=self._panelList.selectedIndexes()[0].row()
            self._panels.remove(self._panels[self._panel_id])
            self._refreshPanelList()
            
    def _moveUp(self):
        if len(self._panelList.selectedIndexes())>0:
            self._panel_id=self._panelList.selectedIndexes()[0].row()
            if self._panel_id > 0:
                tmp =  self._panels[self._panel_id]
                self._panels[self._panel_id]=self._panels[self._panel_id-1]
                self._panels[self._panel_id-1]=tmp
                self._refreshPanelList()
                self._panelList.setCurrentIndex(self._panelList.indexFromItem(self._panelList.item(self._panel_id-1) ))
                
    def _moveDown(self):
        if len(self._panelList.selectedIndexes())>0:
            self._panel_id=self._panelList.selectedIndexes()[0].row()
            if self._panel_id < self._panelList.count()-1:
                tmp =  self._panels[self._panel_id]
                self._panels[self._panel_id]=self._panels[self._panel_id+1]
                self._panels[self._panel_id+1]=tmp
                self._refreshPanelList()
                self._panelList.setCurrentIndex(self._panelList.indexFromItem(self._panelList.item(self._panel_id+1) ))
              
    def _refreshPanelList(self):
        self._panelList.clear()
        for panel in self._panels:
            name,xml = panel
            self._panelList.addItem(name)
            
    def _getPanels(self):
        if len(self._panels)<=0:
            return None
        else:
            return self._panels
        
    def checkData(self):
        BasePage.checkData(self)          
        self._valid=True
    
    def _setStatus(self,text):
        self._status_label.setText(text)
        
        
class ExternalAppEditor(Qt.QDialog):
    def __init__(self, parent = None):
        Qt.QDialog.__init__(self, parent)
        self.setModal(True)
        self.setWindowTitle('External Application Editor')
        
        self._dlgBox = Qt.QDialogButtonBox(Qt.QDialogButtonBox.Ok| Qt.QDialogButtonBox.Cancel)
        
        self._layout = Qt.QVBoxLayout()
        self._layout1 = Qt.QGridLayout()
        self._layout2 = Qt.QHBoxLayout()
        self._layout.addLayout(self._layout1)
        self._layout.addLayout(self._layout2)
        self._layout.addWidget(self._dlgBox)
        self.setLayout(self._layout)
        
        self._icon = None
        self._label = Qt.QLabel("\n On this page you can define an external application. \n")
        self._label.setWordWrap(True)
        self._layout1.addWidget(self._label,0,0,1,4) 
        self._execFileLabel = Qt.QLabel("Command:")
        self._execFileLineEdit = Qt.QLineEdit()
        self._execFileLineEdit.setMinimumSize(150, 25)
        #self._execFileLineEdit.setReadOnly(True)
        self._execFileButton = Qt.QPushButton()
        self._execFileButton.setIcon(taurus.qt.qtgui.resource.getThemeIcon("folder-open"))
        self._execFileButton.setToolTip("Browse...")
        self._execFileButton.setMaximumSize(80, 25)
        self._layout1.addWidget(self._execFileLabel,2,0,Qt.Qt.AlignRight)
        self._layout1.addWidget(self._execFileLineEdit,2,1,Qt.Qt.AlignRight)
        self._layout1.addWidget(self._execFileButton,2,2,Qt.Qt.AlignLeft)
        self._paramsLabel = Qt.QLabel("Parameters:")
        self._paramsLineEdit = Qt.QLineEdit()
        self._paramsLineEdit.setMinimumSize(150, 25)
        self._layout1.addWidget(self._paramsLabel,3,0,Qt.Qt.AlignRight)
        self._layout1.addWidget(self._paramsLineEdit,3,1,Qt.Qt.AlignRight)
        self._textLabel = Qt.QLabel("Text:")
        self._textLineEdit = Qt.QLineEdit()
        self._textLineEdit.setMinimumSize(150, 25)
        self._layout1.addWidget(self._textLabel,4,0,Qt.Qt.AlignRight)
        self._layout1.addWidget(self._textLineEdit,4,1,Qt.Qt.AlignRight)
        
        self._iconLabel = Qt.QLabel("Icon:")
        self._iconLogo = Qt.QPushButton()
        self._iconLogo.setIcon(Qt.QIcon(taurus.qt.qtgui.resource.getThemePixmap("image-missing") ) )
        self._iconLogo.setIconSize(Qt.QSize(60,60))
        self._iconLogo.setStyleSheet(" QPushButton:flat { border: none; /* no border for a flat push button */} ")
        self._iconLogo.setFlat(True)
        self._layout1.addWidget(self._iconLabel,5,0,Qt.Qt.AlignRight)
        self._layout1.addWidget(self._iconLogo,5,1,Qt.Qt.AlignCenter)
        self._spacerItem1 = Qt.QSpacerItem(10, 0, Qt.QSizePolicy.Fixed, Qt.QSizePolicy.Expanding)
        self._layout1.addItem(self._spacerItem1,8,0,1,1,Qt.Qt.AlignCenter)
             
        #connections
        Qt.QObject.connect(self._execFileButton, Qt.SIGNAL("clicked()"), self._selectExecFile)
        Qt.QObject.connect(self._execFileLineEdit, Qt.SIGNAL("textChanged(const QString&)"), self._setDefaultText)
        Qt.QObject.connect(self._iconLogo, Qt.SIGNAL("clicked()"), self._selectIcon)
        self.connect(self._dlgBox,Qt.SIGNAL('accepted()'), self.accept)
        self.connect(self._dlgBox,Qt.SIGNAL('rejected()'), self.reject)
        self.checkData()
        self._setIcon(ExternalAppAction.DEFAULT_ICON_NAME)
        
    def _getExecFile(self):
        return self._execFileLineEdit.text()
    
    def checkData(self):
        if len(self._execFileLineEdit.text())>0:
            self._dlgBox.button(Qt.QDialogButtonBox.Ok).setEnabled(True)
        else:
            self._dlgBox.button(Qt.QDialogButtonBox.Ok).setEnabled(False)
    
    def _setDefaultText(self):
        fileName = self._execFileLineEdit.text().split('/')[-1]
        index = str(fileName).rfind(".")
        if (index>0):
            self._textLineEdit.setText ( str(fileName)[0:index] )
        else:
            self._textLineEdit.setText(fileName)
        self.checkData()
        
    def _selectExecFile(self):
            filePath = Qt.QFileDialog.getOpenFileName(self, self.tr("Open File"),Qt.QDir.homePath(), self.tr("All files (*)")  )
            if len(filePath):
                self._execFileLineEdit.setText(filePath)
                self._setDefaultText()
             
    def _selectIcon(self):
        iconNameList=[]
        pixmapList={}
        rowIconName = []
        #rowPixmap=[]
        rowSize = 7
        r=0
        i=0
        
        progressBar = Qt.QProgressDialog  ("Loading icons...", "Abort", 0, len(taurus.qt.qtgui.resource.getThemeMembers().items()), self)
        progressBar.setModal(True)
        progressBar.setMinimumDuration(0)
                
        for k,v in taurus.qt.qtgui.resource.getThemeMembers().items():
            progressBar.setValue(progressBar.value()+1)
            progressBar.setLabelText(k)
            for iconName in v:
                if (not progressBar.wasCanceled()):
                    rowIconName.append(iconName)
                    pixmapList[iconName] = taurus.qt.qtgui.resource.getThemePixmap(iconName)
                    i=i+1
                    if r == rowSize-1:
                        r=0
                        iconNameList.append(rowIconName)
                        rowIconName=[]
                    else:
                        r=r+1
                    
        if (len (rowIconName)>0) and not (progressBar.wasCanceled()):
            iconNameList.append(rowIconName)
        
        if not progressBar.wasCanceled():
            progressBar.close()
            name,ok = taurus.qt.qtgui.input.GraphicalChoiceDlg.getChoice(parent=None, title= 'Panel chooser', msg='Choose the type of Panel:', choices=iconNameList, pixmaps=pixmapList, iconSize=60)            
            if ok:
                self._setIcon(name)
        else:
            progressBar.close()
            
    def _setIcon(self , name):
        if taurus.qt.qtgui.resource.getThemePixmap(name).width()!=0:
            self._iconLogo.setIcon(Qt.QIcon(taurus.qt.qtgui.resource.getThemePixmap(name) ) )
            self._iconLogo.setIconSize(Qt.QSize(60,60))
            self._iconLogo.setText("")
            self._icon = name
        else:
            self._iconLogo.setText(name)
            self._icon = name
        
    
    def _getExecFile(self):
        return str(self._execFileLineEdit.text())
    
    def _getParams(self):
        return str(self._paramsLineEdit.text())
        #return str(self._paramsLineEdit.text()).split()
    
    def _getText(self):
        return str(self._textLineEdit.text())
    
    def _getIcon(self):
        return str(self._icon)
      
    def _toXml(self):
        root = etree.Element("ExternalApp")
        command = etree.SubElement(root, "command")
        command.text = self._getExecFile()
        params = etree.SubElement(root, "params")
        params.text = self._getParams()
        text = etree.SubElement(root, "text")
        text.text = self._getText()
        icon = etree.SubElement(root, "icon")
        icon.text = self._getIcon()
        
        return etree.tostring(root)

    @staticmethod    
    def getDialog():
        dlg = ExternalAppEditor()
        dlg.exec_()
        return dlg._getExecFile(), dlg._toXml() , (dlg.result() == dlg.Accepted)   
    
        
class ExternalAppPage(BasePage):
    def __init__(self, parent = None):
        BasePage.__init__(self, parent)
        self._externalApps = []
        
    def initializePage(self):
        BasePage.initializePage(self)
        self.wizard().__setitem__("externalApps",self._getExternalApps)
        self._refreshApplicationList()
        
    def _setupUI(self):
        BasePage._setupUI(self)
        self.setTitle('External Applications')
        self._label = Qt.QLabel("The GUI may include shortcuts to external applications. You can add them now.\n")
        self._layout.addWidget(self._label,0,0)
        self.setLayout(self._layout)
        self._externalAppGroupBox = Qt.QGroupBox()
        self._externalAppGroupBox.setCheckable(False)
        self._externalAppGroupBox.setAlignment(Qt.Qt.AlignLeft)
        self._externalAppGroupBox.setStyleSheet(" QGroupBox::title {  subcontrol-position: top left; padding: 5 5px; }")
        self._layout.addWidget(self._externalAppGroupBox,2,0,1,1)
        self._horizontalLayout = Qt.QHBoxLayout(self._externalAppGroupBox)
        self._externalAppList = Qt.QListWidget(self._externalAppGroupBox)
        self._horizontalLayout.addWidget(self._externalAppList)
        self._verticalLayout = Qt.QVBoxLayout()
        self._addButton = Qt.QPushButton("Add Application")
        self._addButton.setStyleSheet("text-align: left;")
        self._verticalLayout.addWidget(self._addButton)
        self._removeButton = Qt.QPushButton("Remove Application")
        self._removeButton.setStyleSheet("text-align: left;")
        self._verticalLayout.addWidget(self._removeButton)
        self._upButton = Qt.QPushButton("Move Up")
        self._upButton.setStyleSheet("text-align: left;")
        self._verticalLayout.addWidget(self._upButton)
        self._downButton = Qt.QPushButton("Move Down")
        self._downButton.setStyleSheet("text-align: left;")
        self._verticalLayout.addWidget(self._downButton)
        self._horizontalLayout.addLayout(self._verticalLayout)
        self._addButton.setIcon(taurus.qt.qtgui.resource.getThemeIcon("list-add"))
        self._removeButton.setIcon(taurus.qt.qtgui.resource.getThemeIcon("list-remove"))
        self._upButton.setIcon(taurus.qt.qtgui.resource.getThemeIcon("go-up"))
        self._downButton.setIcon(taurus.qt.qtgui.resource.getThemeIcon("go-down"))
        Qt.QObject.connect(self._addButton, Qt.SIGNAL("clicked()"), self._addApplication)
        Qt.QObject.connect(self._removeButton, Qt.SIGNAL("clicked()"), self._removeApplication)
        Qt.QObject.connect(self._upButton, Qt.SIGNAL("clicked()"), self._moveUp)
        Qt.QObject.connect(self._downButton, Qt.SIGNAL("clicked()"), self._moveDown)
        Qt.QObject.connect(self._externalAppList, Qt.SIGNAL("itemDoubleClicked(QListWidgetItem*)"), self._editApplication) 
        self._spacerItem1 = Qt.QSpacerItem(10, 0, Qt.QSizePolicy.Fixed, Qt.QSizePolicy.Expanding)
        self._layout.addItem(self._spacerItem1,8,0,1,1,Qt.Qt.AlignCenter)
        self._status_label = Qt.QLabel("Press next button to continue")
        self.setStatusLabelPalette(self._status_label)
        self._layout.addWidget(self._status_label,9,0,1,1)
        
    
    def _addApplication (self):
        name, xml, ok = ExternalAppEditor.getDialog()
        if ok:
            self._externalApps.append((name,xml))
            
        self._refreshApplicationList()
        
    def _editApplication (self):
        # edit
        self._refreshApplicationList()
            
    def _removeApplication(self):
        if len(self._externalAppList.selectedIndexes())>0:
            self._app_id=self._externalAppList.selectedIndexes()[0].row()
            self._externalApps.remove(self._externalApps[self._app_id])
            self._refreshApplicationList()
            
    def _moveUp(self):
        if len(self._externalAppList.selectedIndexes())>0:
            self._app_id=self._externalAppList.selectedIndexes()[0].row()
            if self._app_id > 0:
                tmp =  self._externalApps[self._app_id]
                self._externalApps[self._app_id]=self._externalApps[self._app_id-1]
                self._externalApps[self._app_id-1]=tmp
                self._refreshApplicationList()
                self._externalAppList.setCurrentIndex(self._externalAppList.indexFromItem(self._externalAppList.item(self._app_id-1) ))
                
    def _moveDown(self):
        if len(self._externalAppList.selectedIndexes())>0:
            self._app_id=self._externalAppList.selectedIndexes()[0].row()
            if self._app_id < self._externalAppList.count()-1:
                tmp =  self._externalApps[self._app_id]
                self._externalApps[self._app_id]=self._externalApps[self._app_id+1]
                self._externalApps[self._app_id+1]=tmp
                self._refreshApplicationList()
                self._externalAppList.setCurrentIndex(self._externalAppList.indexFromItem(self._externalAppList.item(self._app_id+1) ))
              
    def _refreshApplicationList(self):
        self._externalAppList.clear()
        for panel in self._externalApps:
            name,xml = panel
            self._externalAppList.addItem(name)
            
    def _getExternalApps(self):
        if len(self._externalApps)<=0:
            return None
        else:
            return self._externalApps
        
    def checkData(self):
        BasePage.checkData(self)          
        self._valid=True
    
    def _setStatus(self,text):
        self._status_label.setText(text)     
        
        
class MonitorPage(BasePage):
    def __init__(self, parent = None):
        BasePage.__init__(self, parent)
    
    def initializePage(self):
        BasePage.initializePage(self)
        self.wizard().__setitem__("monitor",self._getMonitor)
    
    def _setupUI(self):
        BasePage._setupUI(self)
        self.setTitle('Monitor List')
        self._label = Qt.QLabel("\nIf you want to monitor some attributes, add them to the monitor list. \n")
        self._label.setWordWrap(True)
        self._layout.addWidget(self._label,0,0,1,4) 
        self._monitorLabel = Qt.QLabel("Monitor List:")
        self._monitorLineEdit = Qt.QLineEdit()
        self._monitorLineEdit.setToolTip("Comma-separated list of attribute names")
        self._monitorLineEdit.setMinimumSize(400, 25)
        self._monitorLineEdit.setReadOnly(False)
        self._monitorButton = Qt.QPushButton()
        self._monitorButton.setToolTip("Browse...") 
        #self._monitorButton.setIcon(taurus.qt.qtgui.resource.getThemeIcon("system-search"))
        self._monitorButton.setIcon(taurus.qt.qtgui.resource.getIcon(":/designer/devs_tree.png"))     
        self._monitorButton.setMaximumSize(80, 25)
        self._monitorClearButton = Qt.QPushButton()
        self._monitorClearButton.setToolTip("Clear")
        self._monitorClearButton.setMaximumSize(80, 25)
        self._monitorClearButton.setIcon(taurus.qt.qtgui.resource.getIcon(":/actions/edit-clear.svg"))     
        self._layout.addWidget(self._monitorLabel,2,0,Qt.Qt.AlignRight)
        self._layout.addWidget(self._monitorLineEdit,2,1,Qt.Qt.AlignRight)
        self._layout.addWidget(self._monitorButton,2,2,Qt.Qt.AlignLeft)
        self._layout.addWidget(self._monitorClearButton,2,3,Qt.Qt.AlignLeft)
        Qt.QObject.connect(self._monitorButton, Qt.SIGNAL("clicked()"), self._selectMonitor)
        Qt.QObject.connect(self._monitorClearButton, Qt.SIGNAL("clicked()"), self._clearMonitor)
        #self._synopticClear.hide()

        self._spacerItem1 = Qt.QSpacerItem(10, 0, Qt.QSizePolicy.Fixed, Qt.QSizePolicy.Expanding)
        self._layout.addItem(self._spacerItem1,8,0,1,1,Qt.Qt.AlignCenter)
        self._status_label = Qt.QLabel("Press next button to continue")
        self.setStatusLabelPalette(self._status_label)
        self._layout.addWidget(self._status_label,9,0,1,4)
        
    
    def _clearMonitor(self):
        self._monitorLineEdit.clear()
        #self._monitorClearButton.hide()
    
    def _getMonitor(self):
        return str(self._monitorLineEdit.text())
        
    def _selectMonitor(self):
            models, ok = taurus.qt.qtgui.panel.TaurusModelChooser.modelChooserDlg(host=None)
            if ok:
                self._monitorLineEdit.setText(",".join(models))
            self.checkData()      
    
    def _setStatus(self,text):
        self._status_label.setText(text)

        
class OutroPage(BasePage):
    
    def __init__(self, parent = None):
        BasePage.__init__(self, parent)
        self._valid = True
        self.setTitle('Confirmation Page')
        self._label = Qt.QLabel("XML configuration file:")
        self._label.setWordWrap(True)
        self._layout.addWidget(self._label,0,0,2,1)
        self._spacerItem1 = Qt.QSpacerItem(20, 20, Qt.QSizePolicy.Fixed, Qt.QSizePolicy.Fixed)  
        self._layout.addItem(self._spacerItem1,1,0,1,1)
        self._xml = Qt.QTextEdit()
        self._xml.setMinimumHeight(200)
        self._xml.setMinimumWidth(200)
        self._xml.setSizePolicy(Qt.QSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Expanding))
        self._layout.addWidget(self._xml,2,0,1,2)
        
        #self._spacerItem1 = Qt.QSpacerItem(10, 0, Qt.QSizePolicy.Fixed, Qt.QSizePolicy.Expanding)
        #self._layout.addItem(self._spacerItem1,4,0,1,1,Qt.Qt.AlignCenter)
        self._status_label = Qt.QLabel("Write it to file on Finish")
        self.setStatusLabelPalette(self._status_label)
        self._layout.addWidget(self._status_label,5,0,1,2)

        
    def _getXml(self):
        return str(self._xml.toPlainText())
    
    def _setStatus(self,text):
        self._status_label.setText(text)
    
    def checkData(self):
        saveToFile = self.wizard().getSaveToFile()
        if not self._valid and not (saveToFile is not None and len(saveToFile)):
            self._setStatus("Please save the file before finish")
        else:
            self._setStatus("Click finish to exit the wizard")
            self._valid = True
            
        self.emit(Qt.SIGNAL('completeChanged()'))
#        
#        if not self._valid:
#            self._setStatus("Please type the name of the GUI")
#        else:
#            self._setStatus("Press next button to continue")   
        
    def saveAs(self):
        saveToFile = self.wizard().getSaveToFile()
        if saveToFile is not None and len(saveToFile):
            defaultName = Qt.QDir.homePath() + '/' + saveToFile
        else:
            defaultName = Qt.QDir.homePath() + '/' + self.wizard().__getitem__("guiName") + "_config.xml"
        
        fileName = Qt.QFileDialog.getSaveFileName(self, self.tr("Save As"),
                        defaultName, self.tr("XML (*.xml );; All files (*)"))
        
        if not len(fileName):
            return False
        
#        Add extension if user did not
#
#        fInfo = Qt.QFileInfo(fileName)
#        if not len(fInfo.suffix()):
#            fileName = fileName+".xml"
            
        return self.saveFile(fileName)
  
    def saveFile(self, fileName):
        file = Qt.QFile(fileName)
        
        if not file.open(Qt.QFile.WriteOnly | Qt.QFile.Text):
            Qt.QMessageBox.warning(self, self.tr("Saving XML..."),
                    self.tr("Cannot write file %1:\n%2.")
                    .arg(fileName)
                    .arg(file.errorString()))
            return False
        
        file.write(str(self._xml.toPlainText()))
        self._valid = True
        self.checkData()
        file.close()
  
        return True

#    Ask about changes
#
#    def cleanupPage(self):
#        BasePage.cleanupPage(self)
#        msgBox = Qt.QMessageBox()
#        msgBox.setText("Warning              ")
#        msgBox.setStandardButtons(Qt.QMessageBox().No | Qt.QMessageBox().Yes )
#        msgBox.setInformativeText("Do you want to leave the editor of without saving the changes?")
#        ret = msgBox.exec_()
        
    def _createConfigFile(self):
        if True:
            return True
        else:
            return False
        
    def initializePage(self):
        Qt.QWizardPage.initializePage(self)
        self.wizard().setOption (Qt.QWizard.NoCancelButton , True)
        self._xml.setText(self._toXml())
        self.wizard().__setitem__("xml",self._getXml)
        #if self.wizard().getSaveToFile() is not None:
        self._saveButton = Qt.QPushButton("Save to file")
        self._saveButton.setMaximumWidth(120)
        self._saveButton.setIcon(taurus.qt.qtgui.resource.getThemeIcon("document-save"))     
        Qt.QObject.connect(self._saveButton, Qt.SIGNAL("clicked()"), self.saveAs)
        self._layout.addWidget(self._saveButton,3,1,1,1)
        self._valid = False
        self.checkData()
        
    def setNextPageId(self, id):
        self._nextPageId = id
    
    def _toXml(self):
        root = etree.Element("taurusgui_config")
        guiName = etree.SubElement(root, "GUI_NAME")
        guiName.text = self.wizard().__getitem__("guiName")
        organizationName = etree.SubElement(root, "ORGANIZATION")
        organizationName.text = self.wizard().__getitem__("organizationName")
        customLogo = etree.SubElement(root, "CUSTOM_LOGO")
        customLogo.text = self.wizard().__getitem__("customLogo")
        synopticList = self.wizard().__getitem__("synoptics")
        if synopticList:
            synoptics = etree.SubElement(root, "SYNOPTIC")
            for item in synopticList:
                    child = etree.SubElement(synoptics, "synoptic", str = item)

        if self.wizard().__getitem__("macroServerName"):
            macroServerName = etree.SubElement(root, "MACROSERVER_NAME")
            macroServerName.text = self.wizard().__getitem__("macroServerName")
            doorName = etree.SubElement(root, "DOOR_NAME")
            doorName.text = self.wizard().__getitem__("doorName")
            instruments = etree.SubElement(root, "INSTRUMENTS_FROM_POOL")
            instruments.text = str(self.wizard().__getitem__("instruments"))
        
        panelList = self.wizard().__getitem__("panels")
        if panelList:
            panels = etree.SubElement(root, "PanelDescriptions")
            for panel in panelList:
                name,xml = panel
                item = etree.fromstring(xml)
                panels.append(item)
            
        externalAppList = self.wizard().__getitem__("externalApps")
        if externalAppList:
            externalApps = etree.SubElement(root, "ExternalApps")
            for externalApp in externalAppList:
                name,xml = externalApp
                item = etree.fromstring(xml)
                externalApps.append(item)
       
        monitor = etree.SubElement(root, "MONITOR")
        monitor.text = self.wizard().__getitem__("monitor")
        
        return  etree.tostring(root, pretty_print=True)


class AppSettingsWizard(Qt.QWizard):
    CONFIGFILENAME = 'config.xml'
    Pages = Enumeration('Pages', ('IntroPage', 'ProjectPage', 'GeneralSettings', 'CustomLogoPage','SynopticPage','MacroServerInfo','InstrumentsPage', 'PanelsPage','ExternalAppPage','MonitorPage','OutroPage'))
        
    
    def __init__(self, parent=None, jdrawCommand='jdraw', saveToFile = None):
        Qt.QWizard.__init__(self, parent)
        self.installEventFilter(self)
        self._item_funcs = {}
        self._pages = {}
        self._jdrawCommand = jdrawCommand
        self._saveToFile = saveToFile
        self._loadPages()
        
    def getSaveToFile(self):
        return self._saveToFile
   
    @staticmethod
    def getValueFromNode(rootNode, nodeName, default=None):
        '''
        returns a value from given Node
        :param rootNode: (etree.Element) root node
        :param nodeName: the name of node to find
        :param default: returned value if node is None or contains empty string
        '''
        node = rootNode.find(nodeName)
        if (node is not None) and (node.text is not None):
            return node.text
        else:
            return default
        
    @staticmethod
    def getArrayFromNode(rootNode, nodeName, default=None):
        '''
        returns an array contained by given Node
        :param rootNode: (etree.Element) root node
        :param nodeName: the name of node to find
        :param default: returned value if node is None or contains empty string
        '''
        array = []
        node = rootNode.find(nodeName)
        if (node is not None) and (node.text is not None):
            for child in node:
                array.append(child)
            return array
        else:
            return None
        
    
    def loadXml(self, fname):
        '''
        parses xml code and sets all pages according to its contents. It
        raises an exception if something could not be processed
        
        :param fname: (unicode) path to file containing xml code
        '''
        projectDir, cfgfile = os.path.split(fname)
        f = open(fname, 'r')
        xml = f.read()
        root = etree.fromstring(xml)
        
        #print self.Pages
        for pageNumber in range(len(self.Pages.keys())):
            self.page(pageNumber).fromXml(root)
        


#                        
#        self.page(self.Pages.SynopticPage).fromXml(synoptics=synoptics)
#                    
#      
#              
#        macroserverNameNode = root.find("MACROSERVER_NAME")
#        if (macroserverNameNode is not None) and (macroserverNameNode.text is not None):
#            macroserverName = macroserverNameNode.text
#        else:
#            macroserverName = None
#            
#        doorNameNode = root.find("DOOR_NAME")
#        if (doorNameNode is not None) and (doorNameNode.text is not None):
#            doorName = doorNameNode.text
#        else:
#            doorName = ''    
#
#        macroEditorsPathNode = root.find("MACROEDITORS_PATH")
#        if (macroEditorsPathNode is not None) and (macroEditorsPathNode.text is not None):
#            macroEditorsPath = macroEditorsPathNode.text
#        else:
#            macroEditorsPath = ''   
#        
#        self.page(self.Pages.MacroServerInfo).fromXml(macroserverName=macroserverName, doorName = doorName)
        
#        instrumentsFromPool = root.find("INSTRUMENTS_FROM_POOL")
#        if (instrumentsFromPool is not None) and (instrumentsFromPool.text is not None) and (str(instrumentsFromPool.text).lower() =="true"):
#            INSTRUMENTS_FROM_POOL = True
#        else:
#            INSTRUMENTS_FROM_POOL = False
#        
#        #create instrument panels and custom panels
#        CUSTOM_PANELS = []
#        
#        panelDescriptions = root.find("PanelDescriptions")
#        if (panelDescriptions is not None):
#            for child in panelDescriptions:
#                    if (child.tag == "PanelDescription"):
#                        pd = PanelDescription.fromXml(etree.tostring(child))
#                        if pd is not None:
#                            CUSTOM_PANELS.append(pd)
#                        
#        if INSTRUMENTS_FROM_POOL:
#            POOLINSTRUMENTS = self.createInstrumentsFromPool(MACROSERVER_NAME) #auto create instruments from pool 
#        else:
#            POOLINSTRUMENTS = []
#
#        for p in CUSTOM_PANELS + POOLINSTRUMENTS:
#            try:
#                w = p.getWidget(sdm=Qt.qApp.SDM, setModel=False)
#                if hasattr(w,'setCustomWidgetMap'):
#                    w.setCustomWidgetMap(self.getCustomWidgetMap())
#                if p.model is not None:
#                    w.setModel(p.model)
#                #create a panel
#                self.createPanel(w, p.name, p.area)
#                #connect the widget
#                Qt.qApp.SDM.connectWriter("SelectedInstrument", w, "panelSelected")
#                
#            except Exception,e:
#                msg='Cannot create panel %s'%getattr(p,'name','__Unknown__')
#                self.error(msg)
#                self.traceback(level=taurus.Info)
#                result = Qt.QMessageBox.critical(self,'Initialization error', '%s\n\n%s'%(msg,repr(e)), Qt.QMessageBox.Abort|Qt.QMessageBox.Ignore)
#                if result == Qt.QMessageBox.Abort:
#                    sys.exit()
#                    
#        
#        #add external applications
#        EXTERNAL_APPS = [] 
#        
#        externalAppsNode = root.find("ExternalApps")
#        if (externalAppsNode is not None):
#            for child in externalAppsNode:
#                    if (child.tag == "ExternalApp"):
#                        ea = ExternalApp.fromXml(etree.tostring(child))
#                        if ea is not None:
#                            EXTERNAL_APPS.append(ea)
#        
#        #[obj for name,obj in inspect.getmembers(conf) if isinstance(obj, ExternalApp)]
#        for a in EXTERNAL_APPS:
#            self.addExternalAppLauncher(a.getAction())
#        
#        #add a beam monitor      
#        monitorNode = root.find("MONITOR")
#        if (monitorNode is not None) and (monitorNode.text is not None):
#            MONITOR = str(monitorNode.text).split(",")
#        else:
#            MONITOR = []
#        
#        if MONITOR:
#            self.__monitor = TaurusMonitorTiny()
#            self.__monitor.setModel(MONITOR)
#            self.jorgsBar.addWidget(self.__monitor)
#            self.registerConfigDelegate(self.__monitor, 'monitor')
        
        
        
        
        #raise NotImplementedError('Loading previous projects is not yet implemented')
    
    def getXml(self):
        try:
            return self.__getitem__("xml")
        except Exception,e:
            return None

    def __setitem__(self, name, value):
        self._item_funcs[name] = value
        
    def __getitem__(self, name):
        for id in self.getPages():
            p = self.page(id)
            if isinstance(p, BasePage):
                try:
                    return p[name]()
                except Exception,e:
                    pass
        return self._item_funcs[name]()
    
    def addPage(self, page):
        id = Qt.QWizard.addPage(self, page)
        self._pages[id] = page

    def setPage(self, id, page):
        Qt.QWizard.setPage(self, id, page)
        self._pages[id] = page
        
    def getPages(self):
        return self._pages
    
    def _loadPages(self):
        intro = IntroPage()
        self.setPage(self.Pages.IntroPage, intro)
        intro.setNextPageId(self.Pages.ProjectPage)
        
        project_page = ProjectPage()
        self.setPage(self.Pages.ProjectPage, project_page)
        project_page.setNextPageId(self.Pages.GeneralSettings)
        
        general_settings_page = GeneralSettings()
        self.setPage(self.Pages.GeneralSettings, general_settings_page)
        general_settings_page.setNextPageId(self.Pages.CustomLogoPage)
        
        custom_logo_page = CustomLogoPage()
        self.setPage(self.Pages.CustomLogoPage, custom_logo_page)
        custom_logo_page.setNextPageId(self.Pages.SynopticPage)
        
        synoptic_page = SynopticPage()
        self.setPage(self.Pages.SynopticPage, synoptic_page)
        synoptic_page.setNextPageId(self.Pages.MacroServerInfo)
        
        macroserver_page = MacroServerInfoPage()
        self.setPage(self.Pages.MacroServerInfo, macroserver_page)
        macroserver_page.setNextPageId(self.Pages.InstrumentsPage) 
        
        instruments_page = InstrumentsPage()
        self.setPage(self.Pages.InstrumentsPage, instruments_page)
        instruments_page.setNextPageId(self.Pages.PanelsPage)
        
        panels_page = PanelsPage()
        self.setPage(self.Pages.PanelsPage, panels_page)
        panels_page.setNextPageId(self.Pages.ExternalAppPage)
        
        external_app_page = ExternalAppPage()
        self.setPage(self.Pages.ExternalAppPage, external_app_page)
        external_app_page.setNextPageId(self.Pages.MonitorPage)
          
        monitor_page = MonitorPage()
        self.setPage(self.Pages.MonitorPage, monitor_page)
        monitor_page.setNextPageId(self.Pages.OutroPage)   
        
        outro_page = OutroPage()
        self.setPage(self.Pages.OutroPage, outro_page)
        outro_page.setNextPageId(-1)
    
        self.setOption (Qt.QWizard.CancelButtonOnLeft , True)
        
        
def main():
    app = Qt.QApplication([])
    wizard = AppSettingsWizard(saveToFile=None)
    wizard.show()
    sys.exit(app.exec_())
  
if __name__ == "__main__":
    main()

        
    
