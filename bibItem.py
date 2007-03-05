import sys, re, exceptions
from PyQt4 import QtSql, QtCore, QtGui
from Bio import PubMed, Medline
from bibentry_form import Ui_bibEntryForm

class invalidDBKeyException(Exception):
    """ Tried to retrieve a non-existent DB key """
    def __init__(self, key):
        self.key = key
    def __str__(self):
        return "Key %s does not exist in database." % self.key

class insufficientDataException(Exception):
    """ Error raised on commit to db """
    def __init__(self, info):
	self.info = info
    def __str__(self):
	return "Insufficent Data: %s needs to be defined" % self.info

class duplicateKeyException(Exception):
    """ Raised when duplicate key encountered upon insert into DB """
    def __init__(self, key):
	self.key = key
    def __str__(self):
	return "Key %s already exists in DB" % self.key

class bibItem(dict):
    def __init__(self, key=None, db=None):
	# default attribute values - everything should be blank
	self.clearVariables()

	self.db = db

	# init pubmed stuff
	self.recParser = Medline.RecordParser()
	self.medline = PubMed.Dictionary(parser = self.recParser)

	if key:
	    self.buildEntryFromDB(key)

    def clearVariables(self):
        """clears all variables used to represent bibItem info"""
	self["citekey"] = ""
	self["authors"] = []
	self["editors"] = []
	self["year"] = ""
	self["title"] = ""
	self["journal"] = ""
	self["volume"] = ""
	self["number"] = ""
	self["pages"] = ""
        self["type"] = ""
	self["publisher"] = ""
	self["booktitle"] = ""
	self["abstract"] = ""

	self.modify = False

    def buildEntryFromPMID(self, PMID):
	""" retrieve a record from PubMed given the PubMed ID """
	record = self.medline[PMID]
	if record.publication_types[0] == "Journal Article" or record.publication_types[0] == "JOURNAL ARTICLE":
	    self["type"] = "article"
	else:
	    print "Unknown type encountered: %s" % record.publication_types

	# replace newlines with spaces in title and abstract.
	e = re.compile('\n')

	year_re = re.compile('\d{4}')

	self["authors"] = record.authors
	self["title"] = e.sub(' ', record.title)
	self["year"] = year_re.findall(record.publication_date)[0]
	self["pages"] = record.pagination
	self["journal"] = record.title_abbreviation
	self["volume"] = record.volume_issue
	self["number"] = record.issue_part_supplement
	self["abstract"] = e.sub(' ', record.abstract)
	
	self.generateCitekey()

    def guiEdit(self):
	""" show a GUI to edit the entry """
	self.window = QtGui.QDialog()
	self.ui = Ui_bibEntryForm()
	self.ui.setupUi(self.window)

	self.ui.typeBox.insertItem(0, "article")
	self.ui.typeBox.insertItem(1, "collection")
	self.ui.typeBox.insertItem(2, "book")

	if self["type"] == "article":
	    self.ui.typeBox.setCurrentIndex(0)
	elif self["type"] == "collection":
	    self.ui.typeBox.setCurrentIndex(1)
	elif self["type"] == "book":
	    self.ui.typeBox.setCurrentIndex(2)

	self.ui.citekeyEdit.insert(self["citekey"])
	self.ui.titleEdit.insertPlainText(self["title"])
	for author in self["authors"]:
	    self.ui.authorsEdit.insertPlainText("%s\n" % author)
	self.ui.numberEdit.insert(self["number"])
	self.ui.volumeEdit.insert(self["volume"])
	self.ui.pagesEdit.insert(self["pages"])
	self.ui.yearEdit.insert(self["year"])
	self.ui.collectionTitleEdit.insertPlainText(self["booktitle"])
        self.ui.abstractEdit.insertPlainText(self["abstract"])

	for editor in self["editors"]:
	    self.ui.editorsEdit.insertPlainText("%s\n" % editor)

	self.changeJournalLabel(self["type"])

	# signal slot connections go here
	QtCore.QObject.connect(self.ui.cancelButton, QtCore.SIGNAL("clicked()"),
			       self.window.close)
	QtCore.QObject.connect(self.ui.submitButton, QtCore.SIGNAL("clicked()"),
			       self.updateFromGUI)
	QtCore.QObject.connect(self.ui.typeBox, 
			       QtCore.SIGNAL("currentIndexChanged(QString)"),
			       self.changeJournalLabel)
	print "inside GUI Edit"
	self.window.exec_()

    def changeJournalLabel(self, typeString):
	""" toggles journal label between journal and publisher """
	self.ui.journalEdit.clear()
	if typeString == "collection" or typeString == "book":
	    self.ui.journalLabel.setText("Publisher:")
	    self.ui.journalEdit.insert(self["publisher"])
	else:
	    self.ui.journalLabel.setText("Journal:")
	    self.ui.journalEdit.insert(self["journal"])

    def updateFromGUI(self):
	""" update entry from GUI edit window """
	
	print "inside GUI edit 2: modify = %s" % self.modify

	modifyThisRecord = self.modify
	oldCitekey = self["citekey"]
	
	self.clearVariables()

	#self.db.transaction()

	auths = self.ui.authorsEdit.toPlainText().split("\n")
	for a in auths: 
	    if a:
		self.addAuthor(a)

	eds = self.ui.editorsEdit.toPlainText().split("\n")
	for e in eds: 
	    if e:
		self.addEditor(e)

	self["citekey"] = self.ui.citekeyEdit.text()
	self["title"] = self.ui.titleEdit.toPlainText()
	self["number"] = self.ui.numberEdit.text()
	self["volume"] = self.ui.volumeEdit.text()
	self["pages"] = self.ui.pagesEdit.text()
	self["type"] = self.ui.typeBox.currentText()
	self["year"] = self.ui.yearEdit.text()
	self["booktitle"] = self.ui.collectionTitleEdit.toPlainText()
        self["abstract"] = self.ui.abstractEdit.toPlainText()
	if self["type"] == "collection":
	    self["publisher"] = self.ui.journalEdit.text()
	else:
	    self["journal"] = self.ui.journalEdit.text()

	try:
	    self.minimumDataCheck()
	except insufficientDataException:
	    print "Not enough data to commit to DB - aborting"
	    #self.db.rollback()
	else:
	    if oldCitekey and modifyThisRecord == True:
		b = bibItem(db=self.db)
		b["citekey"] = oldCitekey
		print "deleting %s from citekey" % oldCitekey
		b.deleteFromDB()

	    self.insertIntoDB()
	    self.window.close()
	    #self.db.commit()

    def buildEntryFromDB(self, key):
        """builds the bibItem from a key which exists in database"""
	print "Obtaining key %s" % key
	query = QtSql.QSqlQuery("SELECT name, role FROM author WHERE citekey = '%s' ORDER BY number" % key)
	query.exec_()
        

	print "Query size: %d" % query.size()
        if query.size() == 0:
            raise invalidDBKeyException(key)

	# get all the authors
	self["authors"] = []
	while query.next():
	    role = str(query.value(1).toString())
	    if role == "author":
		self["authors"].append(str(query.value(0).toString()))
	    elif role == "editor":
		self["editors"].append(str(query.value(0).toString()))

	# get rest of the fields.
	self["citekey"] = key
	query = QtSql.QSqlQuery("SELECT year,title,journal,volume,number,pages,publisher,booktitle,type,abstract FROM ref WHERE citekey = '%s'" % key)
	query.exec_()
	query.next()
	
	# some error checking should go here
	self["year"] = str(query.value(0).toString())
	self["title"] = str(query.value(1).toString())
	self["journal"] = str(query.value(2).toString())
	self["volume"] = str(query.value(3).toString())
	self["number"] = str(query.value(4).toString())
	self["pages"] = str(query.value(5).toString())
	self["publisher"] = str(query.value(6).toString())
	self["booktitle"] = str(query.value(7).toString())
	self["type"] = str(query.value(8).toString())
        self["abstract"] = str(query.value(9).toString())

    def getAuthorLastName(self, author):
        """return just the last name of given author"""
	parts = author.split(" ")
	parts.pop()
	return " ".join(parts)

    def getAuthorFirstNames(self, author):
        """return array of first names of given author"""
        # assumes that everything which isn't last name
        # is first name, and that it is formatted like so:
        # J Doe.
        # Full first names (e.g. John Doe) are going to cause trouble
        parts = author.split(" ")
        fName = parts.pop()
        fNameArray = []
        for i in range(0, len(fName)):
            fNameArray.append(fName[i])
        return(fNameArray)
        

    def inTextCitation(self):
	""" get in text citation, i.e. (Smith et al., 2005) """
	formatted = ""
	if len(self["authors"]) == 2:
	    formatted = "%s and %s, %s" % (self.getAuthorLastName(self["authors"][0]),self.getAuthorLastName(self["authors"][1]),
					   self["year"])
	    
	elif len(self["authors"]) > 2:
	    formatted = "%s et al., %s" % (self.getAuthorLastName(self["authors"][0]),
					   self["year"])
	else:
	    formatted = "%s %s" % (self.getAuthorLastName(self["authors"][0]),
				   self["year"])
	return formatted

    def citation(self):
        """returns citation string"""
	self["formattedAuthors"] = ", ".join(self["authors"])
	self["formattedEditors"] = ", ".join(self["editors"])

	if self["type"] == "book":
	    s = "%s. (%s) %s. %s." % (self["formattedAuthors"],
				     self["year"],
				     self["title"],
				     self["publisher"])
	elif self["type"] == "collection":
	    s = "%s. (%s) %s in %s, %s (eds). %s." % (self["formattedAuthors"],
						      self["year"],
						      self["title"],
						      self["booktitle"],
						      self["formattedEditors"],
						      self["publisher"])

	else:
	    s = "%s. (%s) %s. %s. %s:%s %s\n\n%s" % (self["formattedAuthors"], 
                                                     self["year"], 
                                                     self["title"],
                                                     self["journal"], 
                                                     self["volume"],
                                                     self["number"],
                                                     self["pages"],
                                                     self["abstract"])
	    
	# remove duplicate periods
	p = re.compile('\.{2,}')
	s = p.sub('.', s)
	return s

    def __repr__(self):
	return self.citation()
    
    def addAuthor(self, authorName):
        """add an author to the bibItem"""
	self["authors"].append(authorName)
    
    def addEditor(self, editorName):
        """add an editor to the bibItem"""
	self["editors"].append(editorName)

    def deleteFromDB(self):
	""" 
	deletes all bits associated with key from DB.
	Note that it only needs the citekey to have been specified.
	"""
	if not self["citekey"]:
	    raise insufficientDataException("citekey")
	
	
	self.db.transaction()
	query = QtSql.QSqlQuery()
	query.prepare(QtCore.QString("DELETE FROM author WHERE citekey = ?"))
	query.bindValue(0, QtCore.QVariant(self["citekey"]))
	query.exec_()
        query.prepare(QtCore.QString("DELETE FROM tags_ref WHERE citekey = ?"))
        query.bindValue(0, QtCore.QVariant(self["citekey"]))
        query.exec_()
	query.prepare(QtCore.QString("DELETE FROM ref WHERE citekey = ?"))
	query.bindValue(0, QtCore.QVariant(self["citekey"]))
	query.exec_()
	self.db.commit()

    def minimumDataCheck(self):
	# sanity check - needs to have these items at minimum
	minimumKeys = ["citekey", "type", "title", "authors", "year"]
	for k in minimumKeys:
	    if not self[k]:
		raise insufficientDataException(k)

    def addToTag(self, tagName):
        """add this reference to a particular tag"""

        if not self["citekey"]:
            raise insufficientDataException("citekey")

        # TODO: add check to create tag if it does not exist?
        query = QtSql.QSqlQuery()
        query.prepare(QtCore.QString("INSERT INTO tags_ref (tag, citekey) VALUES (?, ?)"))
        query.bindValue(0, QtCore.QVariant(tagName))
        query.bindValue(1, QtCore.QVariant(self["citekey"]))
        query.exec_()

    def insertIntoDB(self):
	""" Insert the current bibEntry into the database """

	self.minimumDataCheck()
	self.db.transaction()
	# type specific sanity checks should go here
	query = QtSql.QSqlQuery()
	query.prepare(QtCore.QString("INSERT INTO ref (citekey, type, title, journal, volume, number, pages, publisher, booktitle, year, abstract) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"))

        print "before binding of values"
	query.bindValue(0, QtCore.QVariant(self["citekey"]))
	query.bindValue(1, QtCore.QVariant(self["type"]))
	query.bindValue(2, QtCore.QVariant(self["title"]))
	query.bindValue(3, QtCore.QVariant(self["journal"]))
	if self["volume"]:
	    query.bindValue(4, QtCore.QVariant(self["volume"]))
	if self["number"]:
	    query.bindValue(5, QtCore.QVariant(self["number"]))
	if self["pages"]:
	    query.bindValue(6, QtCore.QVariant(self["pages"]))
	if self["publisher"]:
	    query.bindValue(7, QtCore.QVariant(self["publisher"]))
	if self["booktitle"]:
	    query.bindValue(8, QtCore.QVariant(self["booktitle"]))
	query.bindValue(9, QtCore.QVariant(self["year"]))
        if self["abstract"]:
            query.bindValue(10, QtCore.QVariant(self["abstract"]))
        print "after binding of values"

	print "query was: %s" % query
	if not query.exec_():
	    self.db.rollback() #end the transaction
	    print "ERROR WAS: %s" % query.lastError().text()
	    if query.lastError().type() == QtSql.QSqlError.StatementError or query.lastError().type() == QtSql.QSqlError.ConnectionError:
		print "Error raised"
		raise duplicateKeyException(self["citekey"])
	print "actual query: %s" % query.executedQuery()

	# insert the authors
	i = 0
	for author in self["authors"]:
	    authorquery = QtSql.QSqlQuery()
	    authorquery.prepare(QtCore.QString("INSERT INTO author (citekey, name, number,role) VALUES (?, ?, ?, ?)"))
	    authorquery.bindValue(0, QtCore.QVariant(self["citekey"]))
	    authorquery.bindValue(1, QtCore.QVariant(author))
	    authorquery.bindValue(2, QtCore.QVariant(i))
	    authorquery.bindValue(3, QtCore.QVariant("author"))
	    authorquery.exec_()
	    i = i+1
	i = 0
	for author in self["editors"]:
	    authorquery = QtSql.QSqlQuery()
	    authorquery.prepare(QtCore.QString("INSERT INTO author (citekey, name, number,role) VALUES (?, ?, ?, ?)"))
	    authorquery.bindValue(0, QtCore.QVariant(self["citekey"]))
	    authorquery.bindValue(1, QtCore.QVariant(author))
	    authorquery.bindValue(2, QtCore.QVariant(i))
	    authorquery.bindValue(3, QtCore.QVariant("editor"))
	    authorquery.exec_()
	    i = i+1
	self.db.commit()

    def checkCitekey(self):
	""" 
	check if citekey exists in db. Modify until it does not 

	Still don't know how to avoid race-condition here ...

	"""
	pass

    def generateCitekey(self):
	""" generate key based on First Author Year """
	# keep all but the last part of the name
	names = self["authors"][0].split(" ")
	names.pop()
	name = "".join(names)
	
	self["citekey"] = "%s%s" % (name, self["year"])

    def createModsEntry(self, xmlfile):
        """create MODS xml structure for bibItem"""

        # the root entry element
        element = xmlfile.createElementNS(None, "mods")
        element.setAttributeNS(None, "ID", self["citekey"])

        # the title
        titleInfo = xmlfile.createElementNS(None, "titleInfo")
        element.appendChild(titleInfo)
        title = xmlfile.createElementNS(None, "title")
        titleInfo.appendChild(title)
        titleText = xmlfile.createTextNode(self["title"])
        title.appendChild(titleText)

        # the authors
        for a in self["authors"]:
            authorRole = self._createModsAuthor(a, "author", xmlfile)
            element.appendChild(authorRole)
            

        # origin info (year and publisher)
        originInfo = xmlfile.createElementNS(None, "originInfo")
        dateIssued = xmlfile.createElementNS(None, "dateIssued")
        dateIssuedText = xmlfile.createTextNode(self["year"])
        dateIssued.appendChild(dateIssuedText)
        originInfo.appendChild(dateIssued)
        if self["publisher"]:
            publisher = xmlfile.createElementNS(None, "publisher")
            publisherText = xmlfile.createTextNode(self["publisher"])
            publisher.appendChild(publisherText)
            originInfo.appendChild(publisher)
        element.appendChild(originInfo)

        # type of resource
        typeOfResource = xmlfile.createElementNS(None, "typeOfResource")
        typeOfResourceText = xmlfile.createTextNode("text")
        typeOfResource.appendChild(typeOfResourceText)
        element.appendChild(typeOfResource)

        # related Item info
        relatedItem = xmlfile.createElementNS(None, "relatedItem")
        relatedItem.setAttributeNS(None, "type", "host")
        titleInfo = xmlfile.createElementNS(None, "titleInfo")
        title = xmlfile.createElementNS(None, "title")
        if self["type"] == "article":
            titleText = xmlfile.createTextNode(self["journal"])
        else:
            titleText = xmlfile.createTextNode(self["booktitle"])
        title.appendChild(titleText)
        titleInfo.appendChild(title)
        relatedItem.appendChild(titleInfo)

        for e in self["editors"]:
            editorRole = self._createModsAuthor(e, "editor", xmlfile)
            relatedItem.appendChild(editorRole)

                    
        originInfo = xmlfile.createElementNS(None, "originInfo")
        issuance = xmlfile.createElementNS(None, "issuance")
        issuanceText = xmlfile.createTextNode("continuing")
        issuance.appendChild(issuanceText)
        originInfo.appendChild(issuance)
        relatedItem.appendChild(originInfo)

        marcGenre = xmlfile.createElementNS(None, "genre")
        marcGenre.setAttributeNS(None, "authority", "marc")
        genre = xmlfile.createElementNS(None, "genre")

        if self["type"] == "article":
            marcGenreText = xmlfile.createTextNode("periodical")
            genreText = xmlfile.createTextNode("academic journal")
            genre.appendChild(genreText)
            marcGenre.appendChild(marcGenreText)
        elif self["type"] == "collection":
            marcGenreText = xmlfile.createTextNode("collection")
            genreText = xmlfile.createTextNode("collection")
            genre.appendChild(genreText)
            marcGenre.appendChild(marcGenreText)
        elif self["type"] == "book":
            marcGenreText = xmlfile.createTextNode("book")
            genreText = xmlfile.createTextNode("book")
            genre.appendChild(genreText)
            marcGenre.appendChild(marcGenreText)

        relatedItem.appendChild(marcGenre)
        relatedItem.appendChild(genre)
        element.appendChild(relatedItem)

        # the identifier
        identifier = xmlfile.createElementNS(None, "identifier")
        identifier.setAttributeNS(None, "type", "citekey")
        identifierText = xmlfile.createTextNode(self["citekey"])
        identifier.appendChild(identifierText)
        element.appendChild(identifier)

        # the part info
        part = xmlfile.createElementNS(None, "part")
        date = xmlfile.createElementNS(None, "date")
        dateText = xmlfile.createTextNode(self["year"])
        date.appendChild(dateText)
        part.appendChild(date)

        if self["volume"]:
            volumeDetail = xmlfile.createElementNS(None, "detail")
            volumeDetail.setAttributeNS(None, "type", "volume")
            number = xmlfile.createElementNS(None, "number")
            numberText = xmlfile.createTextNode(self["volume"])
            number.appendChild(numberText)
            volumeDetail.appendChild(number)
            part.appendChild(volumeDetail)

        if self["number"]:
            numberDetail = xmlfile.createElementNS(None, "detail")
            numberDetail.setAttributeNS(None, "type", "number")
            number = xmlfile.createElementNS(None, "number")
            numberText = xmlfile.createTextNode(self["number"])
            number.appendChild(numberText)
            numberDetail.appendChild(number)
            part.appendChild(numberDetail)

        if self["pages"]:
            pages = self["pages"].split("-")
            extent = xmlfile.createElementNS(None, "extent")
            extent.setAttributeNS(None, "unit", "page")
            start = xmlfile.createElementNS(None, "start")
            startText = xmlfile.createTextNode(pages[0])
            start.appendChild(startText)
            extent.appendChild(start)
            end = xmlfile.createElementNS(None, "end")
            endText = xmlfile.createTextNode(pages[1])
            end.appendChild(endText)
            extent.appendChild(end)
            part.appendChild(extent)

        element.appendChild(part)
        return(element)
        

    def buildEntryFromMods(self, entry):
	# translation from MODS types to bibtex/bibItem types
	typeTranslation = {"academic journal" : "article",
			   "periodical" : "article"}


	# get the citekey
	self["citekey"] = entry.attributes["ID"].value

        # get the type of reference
	# try to get the marc authority first
	genres = entry.getElementsByTagName("genre")
        for genre in genres:
            for k in genre.attributes.keys():
                if k == "authority": self["type"] = genre.firstChild.nodeValue
	# if that has failed, get the base value without any keys
	if not self["type"]:
	    self["type"] = genres[0].firstChild.nodeValue

	# do any type translations from MODS-speak
	if self["type"] in typeTranslation.keys():
	    print "translation found"
	    self["type"] = typeTranslation[self["type"]]
        print "Type: %s" % self["type"]
	print "Keys: %s" % typeTranslation.keys()

        # get the authors:
        for author in entry.getElementsByTagName("name"):
            fname = ""
            lname = ""
	    roleTerm = author.getElementsByTagName("roleTerm")[0]
	    role = roleTerm.firstChild.nodeValue
	    fnameCounter = 0
	    fnames = []
	    fname = ""
	    fullFirstNames = False
            for name in author.getElementsByTagName("namePart"):
                if name.attributes["type"].value == "given":
		    newFName = name.firstChild.nodeValue
		    if len(newFName) > 1:
			# if first name has more than one character,
			# ensure that there are spaces between names
			fullFirstNames = True
		    fnames.append(newFName)
                elif name.attributes["type"].value == "family":
                    lname = lname + name.firstChild.nodeValue
                else:
                    print "ERROR - unkown name attribute"
	    if fullFirstNames: 
		fname = " ".join(fnames)
	    else:
		fname = "".join(fnames)
            author = " ".join((lname, fname))
            print "Author: %s" % (author)
            if role == "author": self.addAuthor(author)
	    elif role == "editor": self.addEditor(author)
                    
        # get the title
        titleInfo = entry.getElementsByTagName("titleInfo")[0]
        title = titleInfo.getElementsByTagName("title")[0].firstChild.nodeValue
        # note: should add search for subtitles here.
        self["title"] = title
                    
        # get the publication date
        originInfo = entry.getElementsByTagName("originInfo")[0]
        dateIssued = originInfo.getElementsByTagName("dateIssued")[0].firstChild.nodeValue
	# make sure that year contains only digits
	p = re.compile('\D')
	self["year"] = p.sub('', dateIssued)

                    
        # get the journal or collection title
	if self["type"] == "collection" or self["type"] == "article":

	    relatedItem = entry.getElementsByTagName("relatedItem")[0]
	    titleInfo = relatedItem.getElementsByTagName("titleInfo")[0]
	    title = titleInfo.getElementsByTagName("title")[0]
	    subTitle = titleInfo.getElementsByTagName("subTitle")

	    fullTitle = title.firstChild.nodeValue
	    if subTitle:
		fullTitle = ": ".join( (fullTitle, 
					subTitle[0].firstChild.nodeValue) )
        
	    if self["type"] == "article":
		self["journal"] = fullTitle
	    elif self["type"] == "collection":
		self["booktitle"] = fullTitle
            
	    if self["type"] == "article":
		# journal volume and number info
		for node in entry.getElementsByTagName("detail"):
		    if node.attributes["type"].value == "volume":
			self["volume"] = node.getElementsByTagName("number")[0].firstChild.nodeValue
		    elif node.attributes["type"].value == "number":
			self["number"] = node.getElementsByTagName("number")[0].firstChild.nodeValue
			# should handle single pages correctly here

	# get information about the book
	if self["type"] == "book" or self["type"] == "collection":
	    # the publisher
	    publisher = entry.getElementsByTagName("publisher")[0]
	    self["publisher"] = publisher.firstChild.nodeValue
	    print "Publisher: %s" % self["publisher"]

	    # the book title
                
        # search for pages
        for node in entry.getElementsByTagName("extent"):
            if node.attributes["unit"].value == "page":
                start = node.getElementsByTagName("start")[0]
                end = node.getElementsByTagName("end")[0]
                startValue = start.firstChild.nodeValue
                endValue = end.firstChild.nodeValue
                self["pages"] = "%s-%s" % (startValue, endValue)
	
	# missing still: abstract, URL, publisher info
    
	print "Citation: %s" % self.citation()


    def _createModsAuthor(self, authorName, roleName, xmlfile):
        """creats a MODS xml entry for author or editor"""
        name = xmlfile.createElementNS(None, "name")
        name.setAttributeNS(None, "type", "personal")
        #element.appendChild(name)

        # first names
        fNames = self.getAuthorFirstNames(authorName)
        for fname in fNames:
            namePart = xmlfile.createElementNS(None, "namePart")
            namePart.setAttributeNS(None, "type", "given")
            nameText = xmlfile.createTextNode(fname)
            namePart.appendChild(nameText)
            name.appendChild(namePart)

        # last name
        namePart = xmlfile.createElementNS(None, "namePart")
        namePart.setAttributeNS(None, "type", "family")
        nameText = xmlfile.createTextNode(self.getAuthorLastName(authorName))
        namePart.appendChild(nameText)
        name.appendChild(namePart)
        
        # role
        role = xmlfile.createElementNS(None, "role")
        name.appendChild(role)
        roleTerm = xmlfile.createElementNS(None, "roleTerm")
        roleTerm.setAttributeNS(None, "type", "text")
        roleTerm.setAttributeNS(None, "authority", "marcrelator")
        roleTermText = xmlfile.createTextNode(roleName)
        roleTerm.appendChild(roleTermText)
        role.appendChild(roleTerm)
        return(name)
