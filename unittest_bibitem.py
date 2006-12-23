import sys
from xml.dom import minidom, ext
from PyQt4 import QtGui, QtCore
from bibItem import *
from bibImporter import *
from bibItem_edit import bibItemEdit
from db_connection import DbConnection
import unittest

class testGoodData(unittest.TestCase):
    """ docstring for the class """
    xmldoc = minidom.parse("test.xml")
    refTypes = ( (3, "book"),
                 (1, "article"))
    citeKeys = ( (1, "KHC+05"),
		 (2, "CKL+06"))

    def testReferenceType(self):
        """ test whether the correct reference type is reported """
        for index,refType in self.refTypes:
            entry = self.xmldoc.getElementsByTagName("mods")[index]
            ref = bibItem()
            ref.buildEntryFromMods(entry)
            self.assertEqual(ref["type"], refType)

    def testCiteKey(self):
	""" test to ensure citeky was translated correctly """
	for index,key in self.citeKeys:
            entry = self.xmldoc.getElementsByTagName("mods")[index]
            ref = bibItem()
            ref.buildEntryFromMods(entry)
	    self.assertEqual(ref["citekey"], key)

    def testConversionCycle(self):
        """ test for article converted from MODS back to MODS """
        pass

    def testEntryElements(self):
        """ test to make sure all values in references are correct """
        pass
    
class testPubMed(unittest.TestCase):
    """ tests retrieval of PubMed ID """
    app = QtGui.QApplication(sys.argv)

    db = DbConnection()
    db.connect("QSQLITE", "refdb")
    v = {"title" : "Morphometry of the amusic brain: a two-site study.",
	 "year" : "2006",
	 "authors" : ["Hyde KL", "Zatorre RJ", "Griffiths TD", "Lerch JP",
		      "Peretz I"],
	 "type" : "article",
	 "journal" : "Brain",
	 "citekey" : "Hyde2006" }

    v2 = {"title" : "Mapping anatomical correlations across cerebral cortex (MACACC) using cortical thickness from MRI.",
	 "year" : "2006",
	 "authors" : ["Lerch JP", "Worsley K", "Shaw WP", "Greenstein DK", "Lenroot RK", "Giedd J", "Evans AC"],
	 "type" : "article",
	 "journal" : "Neuroimage",
	  "volume" : "31",
	  "number" : "3",
	  "pages" : "993-1003",
	 "citekey" : "Lerch2006" }

    def testPubMedRetrieval(self):
	""" make sure in press PMID can be retrieved """
	ref = bibItem()
	ref.buildEntryFromPMID(16931534)
	for k in self.v.keys():
	    self.assertEqual(self.v[k], ref[k])

    def testFullRecordRetrieval(self):
	""" make sure PMID can be retrieved """
	ref = bibItem()
	ref.buildEntryFromPMID(16624590)
	for k in self.v2.keys():
	    self.assertEqual(self.v2[k], ref[k])

class testInsertIntoDatabase(unittest.TestCase):
    """ goes through several steps to create a new entry in the database """
    app = QtGui.QApplication(sys.argv)

    xmldoc = minidom.parse("test.xml")
    entry = xmldoc.getElementsByTagName("mods")[1]

    testKeys = ["title", "authors", "volume", "number", "pages", "citekey",
                "year", "journal"]

    db = DbConnection()
    db.connect("QSQLITE", "refdb")


    def testArticleInsertIntoDB(self):
        """ test insertion of new reference into DB """
        ref = bibItem(db=self.db.db)
        ref.buildEntryFromMods(self.entry)
        citekey = ref["citekey"]
        ref.insertIntoDB()
        
        ref2 = bibItem()
        ref2.buildEntryFromDB(citekey)
	
	# clean up
	ref.deleteFromDB()

        for k in self.testKeys: self.assertEqual(ref[k], ref2[k])

    def testErrorOnDuplicateKey(self):
        """ test for error when citekey already exists """
	ref = bibItem(db=self.db.db)
	ref.buildEntryFromMods(self.entry)
	# insert first time
	ref.insertIntoDB()
	# second time should raise error
	self.assertRaises(duplicateKeyException, ref.insertIntoDB)
	# clean up
	ref.deleteFromDB()

class testBookImport(unittest.TestCase):
    """ Test importing of a book. """

    app = QtGui.QApplication(sys.argv)

    xmldoc = minidom.parse("large-bib.xml")
    entry = xmldoc.getElementsByTagName("mods")[1]
    db = DbConnection()
    db.connect("QSQLITE", "refdb")

    v = {"booktitle":
	 "Cerebral Cortex: Cellular Components of the Cerebral Cortex",
	 "title" : "Architectonics as Seen by Lipofuscin Stains",
	 "year" : "1984",
	 "authors" : ["Braak Heiko"],
	 "editors" : ["Peters Alan", "Jones Edward G"],
	 "publisher" : "Plenum Press",
	 "type" : "collection",
	 "citekey" : "B84" }

    def testBook(self):
	""" ensure imported values of an article are correct """
	ref = bibItem()
	ref.buildEntryFromMods(self.entry)
	for k in self.v.keys():
	    self.assertEqual(self.v[k], ref[k])
      
    def testBookInsertIntoDB(self):
	""" ensure that an article can be imported and still be correct """
	ref = bibItem(db=self.db.db)
	ref.buildEntryFromMods(self.entry)
	ref.insertIntoDB()
	ref2 = bibItem(self.v["citekey"])
	ref.deleteFromDB()
	for k in self.v.keys():
	    self.assertEqual(self.v[k], ref2[k])


class testModsExport(unittest.TestCase):
    """Test exporting of a reference to a MODS xml file"""
    v = {"title" : "Mapping anatomical correlations across cerebral cortex (MACACC) using cortical thickness from MRI.",
	 "year" : "2006",
	 "authors" : ["Lerch JP", "Worsley K", "Shaw WP", "Greenstein DK", "Lenroot RK", "Giedd J", "Evans AC"],
	 "type" : "article",
	 "journal" : "Neuroimage",
	  "volume" : "31",
	  "number" : "3",
	  "pages" : "993-1003",
	 "citekey" : "Lerch2006" }
    v_pmid = 16624590
    
    def testArticle(self):
        """go through write/read/write MODS cycle"""

        # create a reference from pubmed
        baseref = bibItem()
        baseref.buildEntryFromPMID(self.v_pmid)

        io = bibImporter(None)
        
        array = bibArray()
        array.append(baseref)

        io.exportXML(array, "/tmp/test.xml")

        # reload file from xml
        reloadref = bibItem()
        xmldoc = minidom.parse("/tmp/test.xml")
        entry = xmldoc.getElementsByTagName("mods")[0]
        reloadref.buildEntryFromMods(entry)

        for k in self.v.keys():
            self.assertEqual(baseref[k], reloadref[k])

    def testBook(self):
        """go through read/write MODS cycle for a book"""
        xmldoc = minidom.parse("large-bib.xml")
        entry = xmldoc.getElementsByTagName("mods")[101]
        ref = bibItem()
        ref.buildEntryFromMods(entry)

        io = bibImporter()
        array = bibArray()
        array.append(ref)
        io.exportXML(array, "/tmp/test-book.xml")

        reloadref = bibItem()
        xmldoc = minidom.parse("/tmp/test-book.xml")
        entry = xmldoc.getElementsByTagName("mods")[0]
        reloadref.buildEntryFromMods(entry)

        for k in ref.keys():
            self.assertEqual(ref[k], reloadref[k])

    def testCollection(self):
        """go through read/write MODS cycle for a collection"""
        xmldoc = minidom.parse("large-bib.xml")
        entry = xmldoc.getElementsByTagName("mods")[2]
        ref = bibItem()
        ref.buildEntryFromMods(entry)

        io = bibImporter()
        array = bibArray()
        array.append(ref)
        io.exportXML(array, "/tmp/test-collection.xml")

        reloadref = bibItem()
        xmldoc = minidom.parse("/tmp/test-collection.xml")
        entry = xmldoc.getElementsByTagName("mods")[0]
        reloadref.buildEntryFromMods(entry)

        
        for k in ref.keys():
            self.assertEqual(ref[k], reloadref[k])
            
class testArticleImport(unittest.TestCase):
    """ Test importing of a book. """

    print "INSIDE TEST SUITE"
    app = QtGui.QApplication(sys.argv)


    xmldoc = minidom.parse("large-bib.xml")
    entry = xmldoc.getElementsByTagName("mods")[3]
    db = DbConnection()
    db.connect("QSQLITE", "refdb")
    #db.guiPrompt()

    v = {"title" : "A voxel-based method for the statistical analysis of gray and white matter density applied to schizophrenia",
	 "year" : "1995",
	 "authors" : ["Wright IC", "McGuire PK", "Poline JB", "Travere JM",
		      "Murray RM", "Frith CD", "Frackowiak RS", "Friston KJ"],
	 "type" : "article",
	 "journal" : "Neuroimage",
	 "volume" : "2",
	 "number" : "4",
	 "pages" : "244-52",
	 "citekey" : "WMP+95" }

    def testArticle(self):
	""" ensure imported values of a book are correct """
	ref = bibItem()
	ref.buildEntryFromMods(self.entry)
	for k in self.v.keys():
	    self.assertEqual(self.v[k], ref[k])
      
    def testArticleInsertIntoDB(self):
	""" ensure that a book can be imported and still be correct """
	ref = bibItem(db=self.db.db)
	ref.buildEntryFromMods(self.entry)
	ref.insertIntoDB()
	ref2 = bibItem(self.v["citekey"])
	ref.deleteFromDB()
	for k in self.v.keys():
	    self.assertEqual(self.v[k], ref2[k])

	

    
    
    
        

if __name__ == "__main__":

    unittest.main()
    


