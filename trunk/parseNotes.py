from db_connection import DbConnection
from PyQt4 import QtCore, QtGui, QtSql
import re, sys

# insert notes, but only if they are not already entered into system.
def insertNote(citekey, note):

    quoteescaper = re.compile(r'\'')

    escapednote = quoteescaper.sub("\\'", note)
    
    noteexistence = QtSql.QSqlQuery("SELECT citekey FROM note WHERE citekey = '%s' AND note = '%s'" % (citekey, escapednote))
    noteexistence.exec_()

    #print "NOTE: %i %s" % (noteexistence.size(), note)
    
    if noteexistence.size() == 0:
        notequery = QtSql.QSqlQuery()
        notequery.prepare(QtCore.QString("INSERT INTO note (citekey, note) VALUES (?, ?)"))
        notequery.bindValue(0, QtCore.QVariant(currentRef))
        notequery.bindValue(1, QtCore.QVariant(note))
        notequery.exec_()
        if notequery.lastError().type():
            print "Error inserting note: [%s] %s" % (citekey, note)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)


    fileHandle = open("/micehome/jlerch/Documents/MICE/articles/morris-water-maze/lit_notes.txt", 'r')
    fileContents = fileHandle.read()

    db = DbConnection()
    db.guiPrompt()


    starts = []
    ends = []

    refStarter = re.compile(r'^====')
    noteStarter = re.compile(r'^\*')
    spaceStarter = re.compile(r'^\s')

    lines = fileContents.split("\n")
    counter = 0
    note = None
    currentRef = None
    notecounter = 0
    for l in lines:
        if refStarter.match(l):
            #print lines[counter-1]
            starts.append(counter-1)
            notecounter = 0
            currentRef = lines[counter-1]
            if (counter -1) > 0:
                ends.append(counter-2)
            
            
        counter = counter + 1
    ends.append(counter)


    for i in range(0, len(starts)):
        currentRef = lines[starts[i]]
        for j in range(starts[i]+2, ends[i]):
            if noteStarter.match(lines[j]):
                lines[j] = noteStarter.sub('', lines[j])
                lines[j] = spaceStarter.sub('', lines[j])

                notecounter = notecounter + 1
                if note:
                    insertNote(currentRef, note)
                    #print "Previous note: [%s]: %s\n\n" % (currentRef, note)
                note = lines[j]
                
            else:
                if lines[j] and note:
                    note = note + "\n" + lines[j]
        #print "Previous note: [%s]: %s\n\n" % (currentRef, note)
        insertNote(currentRef, note)

        note = None



        
