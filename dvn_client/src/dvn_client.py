# DVN client for SWORD API
# Prereqs: Python, sword2 Module (available using easy_install)
# Adapted from: https://bitbucket.org/beno/python-sword2/wiki/Quickstart

__author__="peterbull"
__date__ ="$Jul 29, 2013 1:38:57 PM$"

# python base lib modules
import argparse
import json

#downloaded modules

#local modules
from study import CreateStudyFromDict
from dataverse import Dataverse

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
        dv = Dataverse( username=DEFAULT_USERNAME,
                        password=DEFAULT_PASSWORD, 
                        host=DEFAULT_HOST, 
                        cert=DEFAULT_CERT)
                        
        s = CreateStudyFromDict(PICS_OF_CATS_STUDY)
        dv.addStudy(s)
        dv.addFileToStudy(s, PICS_OF_CATS_FILEPATH)
        
    except Exception as e:
        print "Failed due to Exception: \n", e, e.args
        if dv:
            try:
                dv.swordConnection.history = json.dumps(sdv.swordConnection.history, indent=True)
            except:
                pass
            print "Call History:\n", dv.swordConnection.history
        raise e

if __name__ == "__main__":
    main()
