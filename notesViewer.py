from PyQt4 import QtCore, QtGui, QtSql
from bibItem import *

class notesTable(QtGui.QTableView):
    def __init__(self, parent=None):
        QtGui.QTableView.__init__(self, parent)

        # default display options
	self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
	self.setAlternatingRowColors(True)
	#self.setShowGrid(False)

	# the column header
	#self.header = self.horizontalHeader()

	# a proxy filter to take care of sorting
	self.filterModel = QtGui.QSortFilterProxyModel()

        self.setupConnection()

        self.note = ""

	sm = self.selectionModel()
	# signal slot connections
        self.connect(sm,
                     QtCore.SIGNAL("selectionChanged(QItemSelection, QItemSelection)"),
                     self.newSelection)

    def newSelection(self, selected, deselected):
        record = self.model.record(selected.indexes()[0].row())
        recordCitation = str(record.value(0).toString())
        recordNote = str(record.value(1).toString())

        print "inside new selection"
        # check to see if note ends with a period
        periodRE = re.compile(r'\.$')

        if periodRE.search(recordNote):
            print "match found"
            recordNote = periodRE.sub('', recordNote)

        newlineRE = re.compile(r'\n')
        recordNote = newlineRE.sub(' ', recordNote)
            
        self.note = "%s {%s}." % (recordNote, recordCitation)


        

    def setNoteSelection(self, selection=""):
        self.model.setFilter(selection)
        self.model.select()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def setupConnection(self):
	""" establishes model to fill the table """

	# use the view created in the database for the data display
	#self.model = QtSql.QSqlQueryModel(self)
        self.model = QtSql.QSqlTableModel()
        self.model.setTable("note")
        self.model.select()
        self.model.removeColumn(0)
        self.model.removeColumn(2)

        
	#self.defaultQuery = "SELECT note FROM note"
	#currentQuery = "%s;" % self.defaultQuery
	#self.model.setQuery(self.defaultQuery)
	print "Rowcount: %i" % self.model.rowCount()

	
	# a filter model in between the query and the table view
	# this allows for non-sql based sorting
	self.filterModel.setSourceModel(self.model)
	self.setModel(self.filterModel)
        self.setNoteSelection()
        #t = QtGui.QLabel()
        #index = self.model.index(1,1, QtCore.QModelIndex())
        #self.setIndexWidget(index, t)
        #delegate = SpinBoxDelegate()
        #print delegate
        #self.setItemDelegate(delegate)

    def mousePressEvent(self, event):
        """ for dragging and dropping """
        if (event.button() == QtCore.Qt.LeftButton):
            print "Left button pressed"
            # line below fails due to pythons copy by reference mechanism
            #self.dragStartPosition = event.pos()
            self.dragStartPosition = QtCore.QPoint(event.pos().x(),
                                                   event.pos().y())

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
                mimeData.setData("text/plain", self.note)
                drag.setMimeData(mimeData)
                drag.start()

                
        print "Nyuck"
        #QtGui.QTableView.mouseMoveEvent(self, event)


class notesViewer(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.setModal(False)
        self.notesTable = notesTable()

        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.addWidget(self.notesTable)

        self.setLayout(self.mainLayout)
        self.setWindowTitle("Notes")
        self.resize(700,400)

    def newSelection(self, selection):
        print "inside newSelection"

        citekeys = []
        
        for s in selection:
            citekeys.append("citekey = '%s'" % s["citekey"])

        selectStatement = " OR ".join(citekeys)
        print selectStatement
        self.notesTable.setNoteSelection(selectStatement)
