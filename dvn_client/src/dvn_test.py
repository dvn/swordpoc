# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="peterbull"
__date__ ="$Aug 21, 2013 2:56:25 PM$"

import os
import sys
import unittest


#local modules
from study import Study
from connection import DvnConnection
    
class TestStudyOperations(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # LOAD TEST DATA
        
        print "Loading test data."
        testModulePath = os.path.dirname(__file__)
        execfile(os.path.join(testModulePath, "config.py"), globals())    #CREDS - This file is not committed.
        execfile(os.path.join(testModulePath, "tests.py"), globals())     #TEST DATA
        
        print "Connecting to DVN."
        self.dvc = DvnConnection(username=DEFAULT_USERNAME,
                        password=DEFAULT_PASSWORD, 
                        host=DEFAULT_HOST, 
                        cert=DEFAULT_CERT)
                        
        print "Getting Dataverse"
        self.dv = self.dvc.get_dataverses()[0]
        
        print "Removing any existing studies."
        self.dv.delete_all_studies()
        
    def setUp(self):
        #runs before each test method
        
        #create a study for the test
        s = Study.CreateStudyFromDict(PICS_OF_CATS_STUDY)
        self.dv.add_study(s)
        
        # get the study back from the dataverse
        self.s = self.dv.get_study_by_string_in_entry(PICS_OF_CATS_STUDY["title"])
        self.assertTrue(self.s)
        
        return
    
    def tearDown(self):
        #runs after each test method
        self.dv.delete_all_studies()
        return
        
    def test_add_files_to_study(self):
        self.s.add_files([INGEST_FILES])
        print self.s.get_list_of_files()
        
    def test_release_study(self):
        s = self.dv.get_study_by_string_in_entry(PICS_OF_CATS_STUDY["title"])
        s.release()
        self.dv.delete_study(s)

if __name__ == "__main__":
    __file__ = sys.argv[0]
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStudyOperations)
    unittest.TextTestRunner(verbosity=2).run(suite)

