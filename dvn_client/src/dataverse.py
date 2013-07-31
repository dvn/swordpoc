__author__="peterbull"
__date__ ="$Jul 30, 2013 12:32:24 PM$"

# python base lib modules
import mimetypes
import os

#downloaded modules
import sword2

#local modules

class Dataverse(object):
    def __init__(self, username=None, password=None, host=None, cert=None):
        self.swordConnection = None
        self.connected = False
        self.serviceDocument = None
        
        #Constructor can shortcut to connect
        if (username and password and host):
            self.connect(username, password, host, cert)
        
    def connect(self, username, password, host, cert=None):
        self.username = username
        self.password = password
        self.host = host
        self.sdUri = "https://{host}/dvn/api/data-deposit/swordv2/service-document".format(host=self.host)
        self.cert = cert
            
#        print "Connecting to ", testSdUri
#        print "\t user: ", testUser
#        print "\t pass: ", testPass
#        print

        self.swordConnection = sword2.Connection(self.sdUri, 
                      user_name = self.username,
                      user_pass=self.password, 
                      ca_certs=self.cert)
        
        self.serviceDocument = self.swordConnection.get_service_document()

        # TODO peterbull: Do we really always want to first collection & workspace?
        _, workspace_1_collections = self.swordConnection.workspaces[0]
        self.collection = workspace_1_collections[0]
        
        self.connected = True
    
    def addStudy(self, study):
        if not self.connected:
            raise Exception("Cannot add a study until you call connect() on the Dataverse")
        
        depositReceipt = self.swordConnection.create(metadata_entry = study.entry,
                                                     col_iri=self.collection.href)
        study.lastDepositReceipt = depositReceipt
            
    def addFileToStudy(self, study, filepath):
        if not self.connected:
            raise Exception("Cannot add a file to a study until you call connect() on the Dataverse")
        
        # cannot add a file if the study has never been created on the dataverse
        if not study.lastDepositReceipt:
            self.addStudy(study)
        
        print "Uploading file: ", filepath

        fileMimetype = mimetypes.guess_type(filepath, strict=True)
        print "MimeType: ", fileMimetype

        filename = os.path.basename(filepath)
        print "FileName: ", filename
        
        with open(filepath, "rb") as pkg:
            depositReceipt = self.swordConnection.update(dr = study.lastDepositReceipt,
                            payload = pkg,
                            mimetype = fileMimetype,
                            filename = filename,
                            packaging = 'http://purl.org/net/sword/package/SimpleZip')

            study.lastDepositReceipt = depositReceipt
        
