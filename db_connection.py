
import sys, exceptions
from PyQt4 import QtCore, QtGui, QtSql
from ui_db_connect import Ui_dbConnectionDialog

class connectionError(exceptions.Exception):
    def __init__(self):
	pass
    def __str__(self):
	pass

class DbConnection(QtGui.QDialog, Ui_dbConnectionDialog):
    def __init__(self):
	pass
    
    def __del__(self):
	""" closes the database """
	print "Closing DB ..."
	self.db.close()

    def guiPrompt(self):
	QtGui.QDialog.__init__(self)
	
	# Set up the user interface from designer
	self.setupUi(self)
	self.dbDriver.addItem("QSQLITE")
	self.dbDriver.addItem("QPSQL")
	self.setModal(1)
	self.exec_()
	
    
    def reject(self):
        sys.exit()
	pass

    def accept(self):
	""" slot for accept button of GUI prompt """
	#db = "QPSQL"
        #db = "QSQLITE"
	#self.db.setDatabaseName(self.dbName.text())
	#self.db.setUserName(self.userName.text())
	#self.db.setHostName(self.dbHost.text())
	#self.db.setPassword(self.password.text())
	
	try:
	    self.connect(self.dbDriver.currentText(), 
			 self.dbName.text(), self.userName.text(),
			 self.dbHost.text(), self.password.text(),
			 self.dbPort.text())
	except connectionError:
	    e = self.db.lastError()
	    QtGui.QMessageBox.critical(None, 
				       self.tr("Cannot open database"),
				       e.text(), 
				       QtGui.QMessageBox.Cancel,
				       QtGui.QMessageBox.NoButton)
	self.hide()


    def connect(self, 
		db="QPSQL", 
		databaseName="refdb", 
		userName="", 
		hostName="", 
		password="",
		port=""):
	""" establish connection with the actual database """
	self.db = QtSql.QSqlDatabase.addDatabase(db)
	self.db.setDatabaseName(databaseName)
	self.db.setUserName(userName)
	self.db.setHostName(hostName)
	self.db.setPassword(password)
        if port:
            self.db.setPort(int(port))

	if not self.db.open():
	    raise connectionError()
	    self.connected = None
	else:
	    self.connected = 1

	print "Database name: %s" % self.db.databaseName()
	


if __name__ == "__main__":
#     app = QtGui.QApplication(sys.argv)
#     window = QtGui.QDialog()
#     ui = Ui_dbConnectionDialog()
#     ui.setupUi(window)
#     window.show()
#     sys.exit(app.exec_())
    app = QtGui.QApplication(sys.argv)
    #window = QtGui.QDialog()
    db = DbConnection()



