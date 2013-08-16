__author__="peterbull"
__date__ ="$Jul 30, 2013 12:32:24 PM$"

# python base lib modules
from lxml import etree
import os
import pprint

#downloaded modules
import sword2

#local modules
from study import Study
import utils

class Dataverse(object):
    def __init__(self, connection, collection):
        self.connection = connection
        self.collection = collection

    def add_study(self, study):        
        depositReceipt = self.connection.swordConnection.create(metadata_entry = study.entry,
                                                     col_iri=self.collection.href)
                                                     
        study.hostDataverse = self
        study.lastDepositReceipt = depositReceipt
        print depositReceipt
        
    def delete_study(self, study):
        depositReceipt = self.connection.swordConnection.delete(study.editUri)
        study.lastDepositReceipt = depositReceipt
        
    def delete_all_studies(self):
        studies = self.get_studies()
        for s in studies:
            self.delete_study(s)
        
    def get_studies(self):
        studiesResponse = self.connection.swordConnection.get_resource(self.collection.href)
        
        # get all the entry nodes and parse them into study objects
        studies = []
        for element in utils.get_elements(studiesResponse.content, tag="entry"):
            s = Study.CreateStudyFromEntryElement(element, hostDataverse=self)
            studies.append(s)
            
        return studies
    
    def get_study_by_hdl(self, hdl):
        studies = self.get_studies()
        
        #TODO peterbull: Regex hdl to make sure it is a valid handle
        
        for s in studies:
            if hdl in s.editUri:
                return s
            
        return None