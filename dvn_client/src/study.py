# To change this template, choose Tools | Templates
# and open the template in the editor.
__author__="peterbull"
__date__ ="$Jul 30, 2013 12:21:28 PM$"

# python base lib modules

#downloaded modules
import sword2

#local modules


class Study(object):
    def __init__(self, id, title, author, abstract):
            print "Adding Metadata: id={0},title={1},author={2},abstract={3}".format(id, title, author, abstract)
            
            # Create SWORD Entry with Metadata for study
            self.entry = sword2.Entry(id=id, 
                      title=title,
                      dcterms_abstract = abstract,
                      dcterms_title=title,
                      dcterms_creator=author)
                      
            # deposit receipt is added when Dataverse.addStudy() is called on
            # this study
            self.lastDepositReceipt = None 

def CreateStudyFromDict(dict):
    return Study(  dict["id"],
                dict["title"],
                dict["author"],
                dict["abstract"])
