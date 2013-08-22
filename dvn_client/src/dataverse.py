__author__="peterbull"
__date__ ="$Jul 30, 2013 12:32:24 PM$"

# python base lib modules
import pprint

#downloaded modules

#local modules
from study import Study
import utils

class Dataverse(object):
    def __init__(self, connection, collection):
        self.connection = connection
        self.collection = collection
        
    def __repr__(self):
        return pprint.saferepr(self.__dict__)
    
    def is_released(self):
         collectionInfo = self.connection.swordConnection.get_resource(self.collection.href).content
         status = utils.get_elements(collectionInfo, namespace="", tag="dataverseHasBeenReleased", numberOfElements=1).text
         return bool(status)

    def add_study(self, study):        
        depositReceipt = self.connection.swordConnection.create(metadata_entry = study.entry,
                                                     col_iri=self.collection.href)
                                                     
        study.hostDataverse = self
        study._refresh(dr=depositReceipt)
        
    def delete_study(self, study):
        depositReceipt = self.connection.swordConnection.delete(study.editUri)
        study.isDeleted = True
        
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
    
    def get_study_by_string_in_entry(self, string):
        studies = self.get_studies()
        
        for s in studies:
            if string in s.entry.pretty_print():
                return s
        return None
    