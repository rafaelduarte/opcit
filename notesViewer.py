from PyQt4 import QtCore, QtGui, QtSql
from bibItem import *

class SpinBoxDelegate(QtGui.QItemDelegate):
    def __init__(self, parent = None):
        QtGui.QItemDelegate.__init__(self, parent)
        print "constructor"
        
#     def createEditor(self, parent, option, index):
#         editor = QtGui.QTextEdit(parent)
#         #editor.setMinimum(0)
#         #editor.setMaximum(100)
#         editor.installEventFilter(self)
#         print "editor"
#         return editor

#     def setEditorData(self, spinBox, index):
#         #value, ok = index.model().data(index, QtCore.Qt.DisplayRole).toInt()
#         print "setEditorData"
#         spinBox.setValue("blah")
        

#     def setModelData(self, spinBox, model, index):
#         print "setModelData"
# #        spinBox.interpretText()
# #        value = spinBox.value()

#         #model.setData(index, QtCore.QVariant(value))
        
#     def updateEditorGeometry(self, editor, option, index):
#         print "geometry"
#         editor.setGeometry(option.rect)


class notesTable(QtGui.QTableView):
    def __init__(self, parent=None):
        QtGui.QTableView.__init__(self, parent)

        # default display options
	#self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
	self.setAlternatingRowColors(True)
	#self.setShowGrid(False)

	# the column header
	#self.header = self.horizontalHeader()

	# a proxy filter to take care of sorting
	self.filterModel = QtGui.QSortFilterProxyModel()

        self.setupConnection()


    def setSelection(self, selection=""):
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
        self.setSelection()
        #t = QtGui.QLabel()
        #index = self.model.index(1,1, QtCore.QModelIndex())
        #self.setIndexWidget(index, t)
        #delegate = SpinBoxDelegate()
        #print delegate
        #self.setItemDelegate(delegate)



class notesViewer(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.setModal(False)
        self.notesTable = notesTable()

        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.addWidget(self.notesTable)

        self.setLayout(self.mainLayout)
        self.setWindowTitle("Notes")

    def newSelection(self, selection):
        print "inside newSelection"

        citekeys = []
        
        for s in selection:
            citekeys.append("citekey = '%s'" % s["citekey"])

        selectStatement = " OR ".join(citekeys)
        print selectStatement
        self.notesTable.setSelection(selectStatement)
