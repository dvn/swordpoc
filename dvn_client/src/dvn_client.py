# DVN client for SWORD API
# Prereqs: Python, sword2 Module (available using easy_install)
# Adapted from: https://bitbucket.org/beno/python-sword2/wiki/Quickstart

__author__="peterbull"
__date__ ="$Jul 29, 2013 1:38:57 PM$"

# enable logging for sword commands
import logging
logging.basicConfig()

# python base lib modules
import argparse
import json
import pprint
from time import sleep
import traceback

#downloaded modules

#local modules
from study import Study
from dataverse import Dataverse
from connection import DvnConnection

def parseArguments():
    parser = argparse.ArgumentParser(description='dvn_client exercises the APIs available for a DataVerse Network')
    
    # TODO peterbull: add arguments 
    # For manual connection
#    parser.add_argument('action', choices=['create','upload'], default=None, help='Description for foo argument')
#    parser.add_argument('-u','--username', default=None, help='Description for foo argument')
#    parser.add_argument('-p','--password', default=None, help='Description for bar argument')
    
    parser.add_argument('--runTests', action="store", help='Path to a file with test definitions.')
    parser.add_argument('--config', action="store", help="Path to a file that contains configuration information.")
    return parser.parse_args()

def main():
    # Get the command line arguments.
    args = parseArguments()
    
    # TODO peterbull: only do this if running tests
    # Load configuration values, e.g., DEFAULT_USERNAME stored in separate .py 
    # file.
    execfile(args.config, globals())
    execfile(args.runTests, globals())
    
    dv = None #declare outside so except clause has access
    try:
        dvc = DvnConnection(username=DEFAULT_USERNAME,
                        password=DEFAULT_PASSWORD, 
                        host=DEFAULT_HOST, 
                        cert=DEFAULT_CERT)
                        
        
        dv = dvc.get_dataverses()[0]
      
        dv.delete_all_studies()
        
        #s = Study.CreateStudyFromDict(PICS_OF_CATS_STUDY)
        s = Study.CreateStudyFromAtomEntryXmlFile("/Users/peterbull/NetBeansProjects/dvn/tools/scripts/data-deposit-api/atom-entry-study.xml")
        dv.add_study(s)
        s.add_files([ADD_PIC_OF_CAT], replaceStudyContents=True)
        
        #firstStudy = dv.get_study_by_hdl("PA0CT")
        #print firstStudy
        #print firstStudy.get_list_of_files()
        #dv.delete_study(firstStudy)
        #dv.deleteStudy(firstStudy)
        #dv.addFileToStudy(firstStudy, ADD_PIC_OF_CAT)
        #dv.addFileToStudy(s, ADD_PIC_OF_CAT)
        
        #print json.dumps(dv.swordConnection.history, indent=True)
        print "\n\ndvn_client succeeded"
        #raise Exception("")
        
    except Exception as e:
        sleep(1)
        traceback.print_exc()
        sleep(1)
        if dv:
            try:
                dv.swordConnection.history = json.dumps(dv.connection.swordConnection.history, indent=True)
            except:
                pass
            print "Call History:\n", dv.connection.swordConnection.history

if __name__ == "__main__":
    main()
