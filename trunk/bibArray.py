from bibItem import bibItem
import sys


class bibArray(list):
    """ Holds an array of bibItems and provides various sorting methods """
    def __init__(self, inTextFormationStyle="numbered"):
	self.citations = {}
	self.inTextCitations = {}
        self.counter = 1
	self.inTextFormationStyle = inTextFormationStyle

    def append(self, ref):
	""" adds a new bibItem """
	super(bibArray, self).append(ref)
	self.citations[ref["citekey"]] = ref.citation()

	print "Formation style: %s" % self.inTextFormationStyle

	if self.inTextFormationStyle == "parenthetical":
	    self.inTextCitations[ref["citekey"]] = ref.inTextCitation()
	elif self.inTextFormationStyle == "numbered":
	    self.inTextCitations[ref["citekey"]] = self.counter
        self.counter += 1

    def removeCitekey(self, key):
        """ removes citekey from list - if it exists. Does nothing otherwise"""
        for i in range(0, len(self)):
            if self[i]["citekey"] == key:
                self.pop(i)
                break
        

    def modifyDuplicates(self):
        """modifies references that have duplicate in-text citations.

        Note that this sorts the bibArray in place first"""

        print "in modifyDuplicates"
        # use ascii codes to add letters
        ascii_offset = 97

        self.sort()
        listCopy = self[:]
        current_offset = 0
        for i in range(1, len(self)):
            if listCopy[i]["authors"][0] == listCopy[i-1]["authors"][0] \
                   and listCopy[i]["year"] == listCopy[i-1]["year"]:
                self.addLetterToYear(i-1, ascii_offset + current_offset)
                current_offset += 1
                self.addLetterToYear(i, ascii_offset + current_offset)
            else:
                current_offset = 0

        # walk through all references and replace the year field with
        # the modified year (if it exists)
        for i in range(0, len(self)):
            try:
                self[i]["year"] = self[i]["year_modified"]
            except KeyError:
                pass
            self.inTextCitations[self[i]["citekey"]] = self[i].inTextCitation()


        
    def addLetterToYear(self, index, asciiCode):
        """creates a year_modified field for the reference"""
        self[index]["year_modified"] = "%s%s" % (self[index]["year"], 
                                      chr(asciiCode))

    def getFullCitations(self):
        """returns newlines separated string of all references in list"""
        s = ""
        for ref in self:
            s = s + ref.citation() + "\n\n"

        return(s)

    def getInTextCitations(self):
	cites = []
	for i in self:
	    cites.append(self.inTextCitations[i["citekey"]])
	return cites

    def changeInTextCounts(self):
	""" update the counts for numbered references."""
	# only do this if the formation style makes sense
	if self.inTextFormationStyle == "numbered":
	    for i in range(0, len(self)):
		self.inTextCitations[self[i]["citekey"]] = i + 1

        
    def inTextCitation(self, key):
        return(self.inTextCitations[key])
