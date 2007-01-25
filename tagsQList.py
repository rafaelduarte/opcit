import sys, re
from PyQt4 import QtCore, QtGui, QtSql
from bibItem import *

class tagsListModel(QtSql.QSqlQueryModel):
    """subclass of SqlQueryModel to allow for dragging and dropping"""
    def __init__(self, parent=None):
        QtSql.QSqlQueryModel.__init__(self, parent)

    def supportedDropActions(self):
        return (QtCore.Qt.CopyAction)

    def mimeTypes(self):
        """set allowable mime-types to be citekeys only"""
        types = QtCore.QStringList()
        types << "text/citekeys"
        return types
    
    def flags(self,index):
        if index.isValid():
            return (QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
                  | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled)

        return (QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDropEnabled)

    def dropMimeData(self, data, action, row, column, parent):
        print "does this nyuck?"
        return True

    def addToTag(self, data, index):
        """called when a citekey(s) is dropped onto a tag"""
        tagName = self.data(index).toString()
        citekeysList = data.split(",")
        spaceRemover = re.compile(r'^\s+')
        for citekey in citekeysList:
            citekey = spaceRemover.sub("", str(citekey))
            print "Data: %s dropped onto tag: %s" % (citekey, tagName)
            b = bibItem()
            b["citekey"] = citekey
            b.addToTag(tagName)


class tagsQList(QtGui.QListView):
    """
    a reimplemented QListWidget for reference Tags
    """

    def __init__(self, parent=None, db=None):
        """constructor"""
	QtGui.QListView.__init__(self, parent)

        # set up the database connection
        #self.model = QtSql.QSqlQueryModel(self)
        self.model = tagsListModel(self)
	self.defaultQuery = "SELECT tag FROM tags"
	currentQuery = "%s;" % self.defaultQuery
	self.model.setQuery(self.defaultQuery)
	print "Number of tags: %i" % self.model.rowCount()
        self.setModel(self.model)

        # create menus and actions
        self.createActions()
        self.createMenus()
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)

    def dragMoveEvent(self, event):
        """highlight the tag the mouse is hovering over when dragging"""
        dragIndex = self.indexAt(event.pos())

        if dragIndex.isValid():
            self.setCurrentIndex(dragIndex)

    def newTag(self):
        """add a new tag"""
        tagName = QtGui.QInputDialog.getText(self, "New tag Name",
					     "Tag:")[0]
        
        if not tagName.isEmpty():
            print "Tag was: %s" % str(tagName)
            query = QtSql.QSqlQuery()
            query.prepare(QtCore.QString("INSERT INTO tags (tag) VALUES (?)"))
            query.bindValue(0, QtCore.QVariant(tagName))
            query.exec_()

    def deleteTag(self):
        # do nothing
        pass

    def editTag(self):
        # do nothing
        pass

    def createActions(self):
	""" menu action to work on references """
	self.newAct = QtGui.QAction("New", self)
	self.connect(self.newAct, QtCore.SIGNAL("triggered()"),
		     self.newTag)
	self.deleteAct = QtGui.QAction("Delete", self)
	self.connect(self.deleteAct, QtCore.SIGNAL("triggered()"),
		     self.deleteTag)
	self.editAct = QtGui.QAction("Edit", self)
	self.connect(self.editAct, QtCore.SIGNAL("triggered()"),
		     self.editTag)

    def createMenus(self):
	# the menu bar
	self.tagsMenu = QtGui.QMenu("Tags")
	self.tagsMenu.addAction(self.newAct)
	self.tagsMenu.addAction(self.editAct)
	self.tagsMenu.addAction(self.deleteAct)

    def dragEnterEvent(self, event):
        """for drag and drop"""
        if event.mimeData().hasFormat("text/citekeys"):
            event.acceptProposedAction()
            print "nyuck nyuck"
        else:
            print "ignoring nyuck"
            event.ignore()
        #QtGui.QListView.dragEnterEvent(self, event)

    def dropEvent(self, event):
        """for drag and drop"""
        print "got a nyuck"
        dropIndex = self.indexAt(event.pos())

        if dropIndex.isValid():
            mimeData = event.mimeData().data("text/citekeys")
            self.model.addToTag(mimeData, dropIndex)
            event.acceptProposedAction()
        else:
            event.ignore()
