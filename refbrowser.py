import sys
from PyQt4 import QtCore, QtGui, QtSql
from db_connection import DbConnection
from bibItem import bibItem
from bibTable import bibTable
from bibImporter import bibImporter
from tagsQList import tagsQList

class RefBrowser(QtGui.QMainWindow):
    def __init__(self, parent=None):
	QtGui.QMainWindow.__init__(self,parent)
	
	# holds the currently selected reference
	#self.reference = None
	self.setupDbConnection()


	# the projects window
	tagsWindow = QtGui.QDockWidget(self.tr("Tags "), self)
	tagsWindow.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea |
					    QtCore.Qt.RightDockWidgetArea)
	self.addDockWidget(QtCore.Qt.LeftDockWidgetArea,
			   tagsWindow)
	self.tagsList = tagsQList(tagsWindow, db=self.dbCon.db)
	tagsWindow.setWidget(self.tagsList)
	
	# the reference Display window
	self.refDisplayWindow = QtGui.QDockWidget(self.tr("Reference"), self)
	self.refDisplayWindow.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
	self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, 
			   self.refDisplayWindow)
	self.refDisplay = QtGui.QTextEdit(self.refDisplayWindow)
	self.refDisplayWindow.setWidget(self.refDisplay)


	# the search window
	self.searchWindow = QtGui.QDockWidget(self.tr("Search"), self)
	self.searchWindow.setAllowedAreas(QtCore.Qt.TopDockWidgetArea)
	self.addDockWidget(QtCore.Qt.TopDockWidgetArea, self.searchWindow)
	self.searchEdit = QtGui.QLineEdit(self.searchWindow)
	self.searchWindow.setWidget(self.searchEdit)

	# the main window
	self.refView = bibTable(self, db=self.dbCon.db)
	self.setCentralWidget(self.refView)


	self.resize(800,600)


	# create menus
	self.createActions()
	self.createMenus()


	self.connect(self.refView, QtCore.SIGNAL("referenceChanged(QString)"),
		     self.formatCitation)
	self.connect(self.searchEdit, QtCore.SIGNAL("returnPressed()"),
		     self.searchDB)

    def setupDbConnection(self):
	""" takes care of connection to database and sets up model-view """

	self.dbCon = DbConnection()
	self.dbCon.guiPrompt()

	#self.refView.setupConnection()

    def searchDB(self):
	searchText = self.searchEdit.text()
	self.refView.searchDB(searchText)

    
    def importFile(self):
	print "inside importing file"
	filename = QtGui.QFileDialog.getOpenFileName(self,
						     "Choose a file", 
						     "/",
						     "XML (*.xml)")
	print "Filename to import: %s" % filename
	if filename:
	    imp = bibImporter(self.dbCon.db)
	    imp.importXML(filename)

    def formatCitation(self, formattedRef):
	""" display formatted citation in GUI """
	self.refDisplay.clear()

	#for modelIndex in self.refView.selectionModel().selectedIndexes():
	#key = self.model.record(modelIndex.row()).value(0).toString()
	#reference = bibItem(key)
	#print "Key is: %s" % key
	print "inside formatCitation: %s" % formattedRef
	self.refDisplay.insertPlainText(formattedRef)
	
    def importPMID(self):
	PMID = QtGui.QInputDialog.getInteger(self, "Retrieve PubMed Record",
					     "PMID:")
	ref = bibItem(db=self.dbCon.db)
	ref.modify = False
	ref.buildEntryFromPMID(PMID)
	ref.guiEdit()

    def createActions(self):
        """ create the actions to be used by the menus """
	self.importAct = QtGui.QAction("&Import file", self)
	self.importAct.setShortcut("Ctrl+I")
	self.importAct.setEnabled(True)
	self.connect(self.importAct, QtCore.SIGNAL("triggered()"), 
		     self.importFile)

	self.PMIDAct = QtGui.QAction("Import PMID", self)
	self.connect(self.PMIDAct, QtCore.SIGNAL("triggered()"),
		     self.importPMID)
    
    def createMenus(self):
        """ create the menu bar for the main application/popups """
	# the menu bar
	fileMenu = self.menuBar().addMenu("&File")
	fileMenu.addAction(self.importAct)

	PubMedMenu = self.menuBar().addMenu("PubMed")
	PubMedMenu.addAction(self.PMIDAct)

	self.menuBar().addMenu(self.refView.refMenu)
        self.menuBar().addMenu(self.tagsList.tagsMenu)



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    r = RefBrowser()
    r.show()
    app.exec_()
