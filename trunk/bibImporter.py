import sys
from xml.dom import minidom, ext
from bibItem import *
from bibArray import *

class bibImporter:
    def __init__(self, db=None):
	self.db = db

    def importXML(self, filename):
	xmldoc = minidom.parse(str(filename))
	success = 0
	failure = 0
	for entry in xmldoc.getElementsByTagName("mods"):
	    ref = bibItem()

	    try:
		ref.buildEntryFromMods(entry)
		ref.insertIntoDB(self.db)
	    except insufficientDataException:
		print "Not enough data in %s" % ref
	    except duplicateKeyException:
		print "Duplicate key: %s" % ref
	    except:
		print "Unexpected error"

    def exportXML(self, references, filename):
        """export a bibArray to a MODS xml file"""

        # create the xml file
        xmlfile = minidom.Document()
        root_element = xmlfile.createElementNS("http://www.loc.gov/mods/v3", "modsCollection")
        xmlfile.appendChild(root_element)

        for ref in references:
            mods = ref.createModsEntry(xmlfile)
            root_element.appendChild(mods)

        output_file = open(filename, "wb")
        ext.PrettyPrint(xmlfile, output_file)
        output_file.close()
		
