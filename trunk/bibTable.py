import sys, os
from PyQt4 import QtCore, QtGui, QtSql
from bibItem import bibItem
from bibArray import bibArray
from bibImporter import *
from db_connection import DbConnection

class bibTable(QtGui.QTableView):
    """ 
    A modified version of QTableView.
    """
    def __init__(self, parent=None, db=None):
	QtGui.QTableView.__init__(self, parent)

	# currently selected references
	self.reference = None        # used only when a single reference was selected
        self.selection = bibArray()  # always used to hold current selection

	# default display options
	self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
	self.setAlternatingRowColors(True)
	self.setShowGrid(False)

	# the column header
	self.header = self.horizontalHeader()

	# a proxy filter to take care of sorting
	self.filterModel = QtGui.QSortFilterProxyModel()

	# menus and actions
	self.createActions()
	self.createMenus()

	self.setupConnection()
	self.db = db

	sm = self.selectionModel()
	# signal slot connections
        self.connect(sm,
                     QtCore.SIGNAL("selectionChanged(QItemSelection, QItemSelection)"),
                     self.newSelection)
#	self.connect(sm, 
#		     QtCore.SIGNAL("currentChanged(QModelIndex, QModelIndex)"),
#		     self.newSelection)
	self.connect(self, QtCore.SIGNAL("doubleClicked(QModelIndex)"),
		     self.editCitation)
	self.connect(self.header, QtCore.SIGNAL("sectionPressed(int)"),
		     self.sortByColumn)
	self.connect(self, QtCore.SIGNAL("dbChanged()"),
		     self.refreshView)

    def setupConnection(self):
	""" establishes model to fill the table """

	# use the view created in the database for the data display
	self.model = QtSql.QSqlQueryModel(self)
	self.defaultQuery = "SELECT * FROM refview"
	currentQuery = "%s;" % self.defaultQuery
	self.model.setQuery(self.defaultQuery)
	print "Rowcount: %i" % self.model.rowCount()
	
	# a filter model in between the query and the table view
	# this allows for non-sql based sorting
	self.filterModel.setSourceModel(self.model)
	self.setModel(self.filterModel)
	
	# resize the year column
	self.resizeColumnToContents(1) 

    def refreshView(self):
	""" re-calls the current query """
	self.model.setQuery(self.defaultQuery)
	self.emit(QtCore.SIGNAL("referenceChanged(QString)"), 
		  "")

    def newSelection(self, selected, deselected):
        """sets the current selection"""

        # the two arguments contains lists of selected and deselected items

        # two hashes used as a quick way to only get unique elements
        selectedKeys = {}
        deselectedKeys = {}
        
        for i in selected.indexes():
            sourceIndex = self.filterModel.mapToSource(i)
            selectedKeys[str(self.model.record(sourceIndex.row()).value(0).toString())] = 1

        for i in deselected.indexes():
            sourceIndex = self.filterModel.mapToSource(i)
            deselectedKeys[str(self.model.record(sourceIndex.row()).value(0).toString())] = 1

        # add or remove the appropriate elements from the selection bibArray
        for key in selectedKeys.keys():
            self.selection.append(bibItem(key, db=self.db))
        for key in deselectedKeys.keys():
            self.selection.removeCitekey(key)

        # send a list of all the selected citekeys
        self.emit(QtCore.SIGNAL("selectionChanged"), self.selection)

        # send a string of the full citations to anyone who cares
        self.emit(QtCore.SIGNAL("referenceChanged(QString)"),
                  QtCore.QString(self.selection.getFullCitations()))

        # set the current reference if only a single item has been selected
        if len(self.selection) == 1:
            self.reference = self.selection[0]
        else:
            self.reference = None

        print "SELECTED: %s" % selectedKeys.keys()
        print "DESELECTED: %s" % deselectedKeys.keys()
        
    def sortByColumn(self, headerIndex):
	""" uses the proxy filter to sort the view by column """
	self.header.setSortIndicatorShown(1)
	if self.header.sortIndicatorOrder() == QtCore.Qt.DescendingOrder \
		and self.header.sortIndicatorSection() == headerIndex:
	    self.filterModel.sort(headerIndex, QtCore.Qt.AscendingOrder)
	    self.header.setSortIndicator(headerIndex, QtCore.Qt.AscendingOrder)
	else:
	    self.filterModel.sort(headerIndex, QtCore.Qt.DescendingOrder)
	    self.header.setSortIndicator(headerIndex, QtCore.Qt.DescendingOrder)

    # not used anymore - will be removed ere too long
    def sortByColumnSql(self, headerIndex):
	"""Sorts the columns in the model by using an ORDER BY SQL statement"""

	print "Column selected: %d" % headerIndex
	self.header.setSortIndicatorShown(1)
	headerName = self.model.record(0).fieldName(headerIndex)
	query = "%s ORDER BY refview.%s" % (self.defaultQuery, headerName)
	if self.header.sortIndicatorOrder() == QtCore.Qt.DescendingOrder \
		and self.header.sortIndicatorSection() == headerIndex:
	    query = "%s DESC" % query
	    self.header.setSortIndicator(headerIndex, QtCore.Qt.AscendingOrder)
	else:
	    self.header.setSortIndicator(headerIndex, QtCore.Qt.DescendingOrder)
	    
	self.model.setQuery("%s;" % query)


    def editCitation(self, modifyRecord=True):
	""" display a GUI from the bibitem to edit the citation """

        # give a warning message if more than one item was selected
        if self.reference == None:
            QtGui.QMessageBox.information(self,
                                          "Notice",
                                          "Only one item can be selected when a reference is to be modified")
        else:
            # the != False bit is due to the fact that some signals pass in
            # a QModelIndex - whenever that happens the record should be modified
            # rather than created from scratch.

            self.reference.modify = modifyRecord != False
            self.reference.guiEdit()

    def newRef(self):
	self.reference = bibItem(db=self.db)
	self.editCitation(modifyRecord=False)
        self.emit(QtCore.SIGNAL("dbChanged()"))

    def deleteRef(self):
        if self.reference == None:
            QtGui.QMessageBox.information(self,
                                          "Notice",
                                          "For the moment only one item can be selected when a reference is to be deleted")
        else:

            citekey = self.reference["citekey"]

            # counterintuitive, but appears to return 0 on "Yes"
            output = QtGui.QMessageBox.question(self,
                                                "Delete %s?" % citekey,
                                                "Delete %s from database?" 
                                                "(Cannot be undone)" % citekey,
                                                "Yes", "No", "", 0, 1)
            if output == 0: 
                self.reference.deleteFromDB()
                self.emit(QtCore.SIGNAL("dbChanged()"))
                print "%s deleted" % citekey
					    
    def searchDB(self, searchText):
	"""
	Search the database based on text fragments for author and title.
	The search is based on the ILIKE operator applied to multiple
	fields simultaneously, matching any part of those fields and
	returning just unique results.
	"""

        # clear selection array
        self.selection = bibArray()
        
	if searchText.isEmpty():
	    self.currentQuery = self.defaultQuery
	else:
	    self.currentQuery = "SELECT DISTINCT ON (refview.citekey) refview.* from refview, ref, author WHERE refview.citekey = ref.citekey AND refview.citekey = author.citekey AND (author.name ILIKE '%%%s%%' OR ref.title ILIKE '%%%s%%')" % (searchText, searchText)
	self.model.setQuery("%s;" % self.currentQuery)


    def limitByTag(self, tag):
        """limits the viewed references to a specified tag"""

        # clear selection array
        self.selection = bibArray()

        self.currentQuery = "SELECT DISTINCT refview.* FROM REFVIEW INNER JOIN tags_ref ON refview.citekey = tags_ref.citekey WHERE tags_ref.tag = '%s'" % str(tag)
        print self.currentQuery
        self.model.setQuery("%s;" % self.currentQuery)

    def exportCitations(self):
        """exports bibArray to MODS xml file"""
        # should put file selector here
        io = bibImporter()

	fd = QtGui.QFileDialog(self, "Save As:")
	fd.setFileMode(QtGui.QFileDialog.AnyFile)
	fd.setFilter( "XML Files (*.xml)" )

	file = None
	if fd.exec_():
	    fl = fd.selectedFiles()
	    file = fl[0]

	if file:
	    overwrite = 0 #0 since messagebox return 0 on yes
	    if os.path.exists(file):
		overwrite = QtGui.QMessageBox.question(self, "Overwrite File?", "A file called %s already exists. Do you want to overwrite it?" % file, "&Yes", "&No", "", 0, 1)
		print "OVERWRITE: %s" % overwrite
	    if overwrite == 0:
		print "Exporting to %s" % (file)
		io.exportXML(self.selection, file)
	    else:
		print "Export aborted - file exists"
	else:
	    print "Export citations aborted"

    def createActions(self):
	""" menu action to work on references """
	self.newAct = QtGui.QAction("New", self)
	self.connect(self.newAct, QtCore.SIGNAL("triggered()"),
		     self.newRef)
	self.deleteAct = QtGui.QAction("Delete", self)
	self.connect(self.deleteAct, QtCore.SIGNAL("triggered()"),
		     self.deleteRef)
	self.editAct = QtGui.QAction("Edit", self)
	self.connect(self.editAct, QtCore.SIGNAL("triggered()"),
		     self.editCitation)
        self.exportAct = QtGui.QAction("Export", self)
        self.connect(self.exportAct, QtCore.SIGNAL("triggered()"),
                     self.exportCitations)

    def createMenus(self):
	# the menu bar
	self.refMenu = QtGui.QMenu("Reference")
	self.refMenu.addAction(self.newAct)
	self.refMenu.addAction(self.editAct)
	self.refMenu.addAction(self.deleteAct)
        self.refMenu.addAction(self.exportAct)

    def contextMenuEvent(self, event):
	""" executed on right-click anywhere """
	self.refMenu.exec_(event.globalPos())

    def mousePressEvent(self, event):
        """ for dragging and dropping """
        if (event.button() == QtCore.Qt.LeftButton):
            print "Left button pressed"
            # line below fails due to pythons copy by reference mechanism
            #self.dragStartPosition = event.pos()
            self.dragStartPosition = QtCore.QPoint(event.pos().x(), event.pos().y())

        # handle normal events
        QtGui.QTableView.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        """ for dragging and dropping """
        if event.buttons() & QtCore.Qt.LeftButton:
            print "yup"
            print QtGui.QApplication.startDragDistance()
            print self.dragStartPosition.x()
            print event.pos().x()
            if QtCore.QPoint(event.pos() - self.dragStartPosition).manhattanLength() > QtGui.QApplication.startDragDistance():
                print "not so nyuck"
                drag = QtGui.QDrag(self)
                mimeData = QtCore.QMimeData()
                mimeData.setData("text/citekeys", self.selection.getCitekeys())
                drag.setMimeData(mimeData)
                drag.start()

                
        print "Nyuck"
        #QtGui.QTableView.mouseMoveEvent(self, event)
        
            
