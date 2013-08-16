__author__="peterbull"
__date__ ="$Aug 16, 2013 12:32:24 PM$"

# python base lib modules


#downloaded modules
import sword2

#local modules
from dataverse import Dataverse

class DvnConnection(object):
    def __init__(self, username, password, host, cert=None):
        # Connection Properties
        self.username = username
        self.password = password
        self.host = host
        self.sdUri = "https://{host}/dvn/api/data-deposit/v1/swordv2/service-document".format(host=self.host)
        self.cert = cert
        
        # Connection Status and SWORD Properties
        self.swordConnection = None
        self.connected = False
        self.serviceDocument = None
        
        # DVN Properties
        self.dataverses = None
        
        self._connect()
        
    def _connect(self):
        self.swordConnection = sword2.Connection(self.sdUri, 
                      user_name = self.username,
                      user_pass = self.password, 
                      ca_certs = self.cert)
        
        self.serviceDocument = self.swordConnection.get_service_document()
        self.connected = True
        
    def get_dataverses(self):
        # TODO peterbull: Do we need to call the API again to make sure
        # we get the latest set of collections?
        _, collections = self.swordConnection.workspaces[0]
        
        dvs = []
        for col in collections:
            dvs.append(Dataverse(self, col))
        
        return dvs