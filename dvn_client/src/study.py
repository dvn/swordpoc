# To change this template, choose Tools | Templates
# and open the template in the editor.
__author__="peterbull"
__date__ ="$Jul 30, 2013 12:21:28 PM$"

# python base lib modules

#downloaded modules
import lxml
import pprint
import sword2

#local modules

class Study(object):
    def __init__(self, id, title, author=None, abstract=None, editUri=None):
            # Create SWORD Entry with Metadata for study
            self.entry = sword2.Entry(id=id, 
                      title=title,
                      author=author,
                      dcterms_abstract = abstract,
                      dcterms_title=title,
                      dcterms_creator=author)
                      
            # deposit receipt is added when Dataverse.addStudy() is called on
            # this study
            self.lastDepositReceipt = None 
            
            self.editUri = editUri
            
    def __repr__(self):
        return pprint.pformat(self.__dict__)
                
    @classmethod
    def CreateStudyFromDict(cls, dict):
        return cls(dict["id"],
                   dict["title"],
                   dict["author"],
                   dict["abstract"])
                    
    @classmethod
    def CreateStudyFromEntryElement(cls, entryElement):
        return cls(entryElement[0].text,
                   entryElement[1].text,
                   editUri=entryElement.base)
