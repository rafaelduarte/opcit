import sys
from PyQt4 import QtCore, QtGui
from bibItem import bibItem
from bibentry_form import Ui_bibEntryForm

class bibItemEdit(QtGui.QDialog, Ui_bibEntryForm):
    def __init__(self, reference=None):
	QtGui.QDialog.__init__(self)
    	# Set up the user interface from designer
	self.setupUi(self)

	if reference:
	    self.initFromBibItem(reference)
	else:
	    self.ref = bibItem()


	# connect signals and slots
	self.connect(self.cancelButton, QtCore.SIGNAL("clicked()"),
		     self.cancel)

	# execute
	self.exec_()

	
    def initFromBibItem(self, reference):
	self.ref = reference
	self.titleEdit.insertPlainText(reference["title"])
	for author in reference["authors"]:
	    self.authorsEdit.insertPlainText("%s\n" % author)
	self.journalEdit.insert(reference["journal"])
	self.numberEdit.insert(reference["number"])
	self.volumeEdit.insert(reference["volume"])
	self.pagesEdit.insert(reference["pages"])
    

    def cancel(self):
	print "Cancel pressed"
	self.done(1)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    bibFrom = bibItemEdit()
