from db_connection import DbConnection
from bibItem import bibItem, invalidDBKeyException
from bibArray import bibArray
from PyQt4 import QtCore, QtGui, QtSql
from optparse import OptionParser
import sys
import re
import tempfile
import shutil
import os

class documentFormatter:
    """ base class for formatting bibliographies """
    def __init__(self, db=None, style="numbered", sortRefs=False):
	self.citekeys = []
	self.sortRefs = sortRefs
	self.style = style
	self.references = bibArray(style)
	self.uniqueCitekeys = []
        self.missingRefs = []
        self.inTextRefs = {}

	self.opening = "["
	self.closing = "]"

	if style == "parenthetical":
	    self.opening = "("
	    self.closing = ")"

	if db:
	    self.db = db
	else:
	    self.db = DbConnection()
	    self.db.guiPrompt()

    def getUniqueCitekeys(self):
	""" return just the unique citekeys """
	if len(self.citekeys) > 1:
	    u = {}
	    for key in self.citekeys: u[key] = key
	    #self.uniqueCitekeys = u.keys()
	    for k in u.keys():
		print "Key: %s" % k
		# remove duplicates here
		if (self.citekeys.count(k) > 1): # if ref occurs more than once
		    indices = []
		    print "Before: %i" % len(self.citekeys)
		    for i in range(0, len(self.citekeys)):
			if self.citekeys[i] == k: # find where this ref occurs
			    indices.append(i)
		    counter = 0
		    for i in range(1, len(indices)): # remove all but first
			print "indices: %s" % indices
			self.citekeys.pop(indices[i] - counter)
			counter += 1 # counter needed since size of array is changing
		    print "After: %i" % len(self.citekeys)
		
	#else:
	#    self.uniqueCitekeys = self.citekeys
		
    def getReferences(self):
	""" attempts to retrieve all the references from the DB """
        for key in self.citekeys:
            try:
                b = bibItem(db=self.db, key=key)
            except invalidDBKeyException:
                self.missingRefs.append(key)
            else:
		if key:
		    print "Inserting key %s" % key
		    self.references.append(b)

	if self.sortRefs == True:
	    self.references.sort()
	self.references.changeInTextCounts()
	print "Citations: %s" % self.references.getInTextCitations()
        self.formatReferences()
	for i in self.references: print i
        print self.inTextRefs
        
    def printMissingRefs(self):
        """ prints a list of missing references to the screen """
        print "Missing keys: "
        for r in self.missingRefs:
            print "   %s" % r

    def formatReferences(self):
	""" creates dict of formatted in text references """
        #self.references.modifyDuplicates()
        for k in self.inTextRefs.keys():
            formatted = ""
            formattedRefs = []
            refs = self.refsInCitation(k)
            for r in refs:
                try:
                    c = self.references.inTextCitation(r)
                except KeyError:
                    formattedRefs.append("MISSING: %s" % r)
                else:
                    formattedRefs.append("%s" % self.references.inTextCitation(r))
            if len(refs) > 1:
                print "FR: %s" % formattedRefs
                s = ", ".join(formattedRefs)
                formatted = "%s%s%s" % (self.opening, s, self.closing)
            else:
                formatted = "%s%s%s" % (self.opening, formattedRefs[0], self.closing)
            self.inTextRefs[k] = formatted
    
    
    def removeColons(self, reference):
	"""quick hack to replace Doe:2001 with Doe2001"""
	p = re.compile(r':')
	return p.sub('', reference)

    def refsInCitation(self, citation):
        """ get the citekeys inside an unformatted inText citation """
        refs = []
        spaceRemover = re.compile(r'^\s+')
	squiqqlyRemover = re.compile(r'[\{\}]')
        citation = squiqqlyRemover.sub('', citation)
        print "List: %s" % citation
        for reference in citation.split(","):
            reference = spaceRemover.sub('', reference)
	    reference = self.removeColons(reference)
            refs.append(reference)
        return(refs)

    def openFile(self, fileName):
        """ an empty method that needs to be subclassed """
        pass

    def getCitekeys(self):
	""" an empty method that needs to be subclassed """
	pass
    
    def replaceCitekeys(self):
	""" an empty method that needs to be subclassed """
	pass

    def formatBibliography(self):
	""" an empty method that needs to be subclassed """
	pass

    def writeFile(self, output):
	""" an empty method that needs to be subclassed """
	pass

    def formatDocument(self, input=None, output=None):
        """ formats a document - replacing references and creating a ref list"""
        if input:
            self.filename = input
        # open the file - this method needs to be subclassed.
        self.openFile(self.filename)

	# extract the citekeys from the document (handled by the subclass)
        self.getCitekeys()
	# get just the unique citekeys
        self.getUniqueCitekeys()
        print "Unique: %s" % self.uniqueCitekeys
	# get the references from the database
        self.getReferences()
	# replace the citekeys inside the document (handled by subclass)
        self.replaceCitekeys()
	# format the bibliography (handled by subclass)
        self.formatBibliography()
	# write to file (handled by subclass)
        if output:
            self.writeFile(output)
        self.printMissingRefs()
        
class ooFormatter(documentFormatter):
    """ formats OpenOffice 1 and 2 documents """
    def __init__(self, fileName=None, db=None, style="numbered", sortRefs=False):
	documentFormatter.__init__(self, db, style=style, sortRefs=sortRefs)

	self.filename = None
	self.fileHandle = None
	self.fileContents = None
        self.tmpdir = None

    	if fileName:
	    self.openFile(fileName)

    def __del__(self):
        """ deletes temporary files """
        if self.tmpdir:
            print "removing tempdir: %s" % self.tmpdir
            shutil.rmtree(self.tmpdir)

    def openFile(self, fileName):
	""" read the input file """
        self.tmpdir = tempfile.mkdtemp()
	self.filename = fileName
        self.contentName = os.path.join(self.tmpdir, "content.xml")
        cwd = os.getcwd()
        os.chdir(self.tmpdir)
        os.system("unzip %s" % fileName)
	self.fileHandle = open(self.contentName, 'r')
	self.fileContents = self.fileHandle.read()

    def writeFile(self, fileName):
        self.fileHandle.close()
        self.fileHandle = open(self.contentName, 'w')
        self.fileHandle.write(self.fileContents)
        self.fileHandle.write("\n")
        self.fileHandle.close()
        os.system("zip -r %s *" % fileName)
        
    def getCitekeys(self):
	""" returns array of all citekeys used in document """
	p = re.compile(r'\{.*?\}')
	refList = p.findall(self.fileContents)
	for citations in refList:
            self.inTextRefs[citations] = None
            for r in self.refsInCitation(citations):
                self.citekeys.append(r)


    def replaceCitekeys(self):
	""" replaces in-text versions of citekey """
	
	# BUG: if the in text reference has characters with special regex meaning
	# such as a + this will produce unpredictable results.
        for k in self.inTextRefs.keys():
            p = re.compile(k)
            self.fileContents = p.sub(self.inTextRefs[k], self.fileContents)

    def formatBibliography(self):
        self.formattedBibliography = r'<text:h text:style-name="Heading 1" text:level="1">References</text:h>'
        counter = 1
        for r in self.references:
	    if self.style == "numbered":
		self.formattedBibliography += "<text:p text:style-name=\"Standard\">[%s] %s</text:p>" % (counter , r)
	    else:
		self.formattedBibliography += "<text:p text:style-name=\"Standard\">%s</text:p>" % r
            counter += 1

        documentEnd = r'(</office:text>)?</office:body></office:document-content>'
        p = re.compile(documentEnd)
        realEnd = p.findall(self.fileContents)[0]
        print "Doc ending was: %s" % realEnd
        self.formattedBibliography += realEnd

        self.fileContents = p.sub(self.formattedBibliography, self.fileContents)


if __name__ == "__main__":

    # command line options
    parser = OptionParser()
    parser.add_option("--numbered", action="store_const", 
		      const="numbered", dest="style", default="numbered")
    parser.add_option("--parenthetical", action="store_const", 
		      const="parenthetical", dest="style")
    parser.add_option("-s", "--sort", action="store_true", default=False,
		      dest="sort")

    (options, args) = parser.parse_args()

    print "Style: %s"  % options.style
    print "Args: %s" % args

    print "Starting document Formatter"

    app = QtGui.QApplication(sys.argv)

    file = args[0]
    out = None
    if len(args) == 2: 
	out = args[1]

    ooF = ooFormatter(style=options.style, sortRefs=options.sort)
    ooF.formatDocument(file, out)
#    ooF.getCitekeys()
#    ooF.getUniqueCitekeys()
#    print "Unique: %s" % ooF.uniqueCitekeys
#    ooF.getReferences()
#    ooF.replaceCitekeys()
#    ooF.formatBibliography()
#    if len(sys.argv) == 3: ooF.writeFile(sys.argv[2])
#    ooF.printMissingRefs()

