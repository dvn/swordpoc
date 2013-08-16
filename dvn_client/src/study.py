
# To change this template, choose Tools | Templates
# and open the template in the editor.
__author__="peterbull"
__date__ ="$Jul 30, 2013 12:21:28 PM$"

# python base lib modules
import mimetypes
import os
import pprint
from zipfile import ZipFile

#downloaded modules
from lxml import etree
import sword2

#local modules
import utils

class Study(object):
    def __init__(self, title, id=None, author=None, abstract=None, editUri=None, editMediaUri=None, hostDataverse=None, atomEntryXml=None):
            # Create SWORD Entry with Metadata for study
            self.entry = sword2.Entry(atomEntryXml=atomEntryXml,
                      id=id,
                      title=title,
                      author=author,
                      dcterms_abstract = abstract,
                      dcterms_title=title,
                      dcterms_creator=author)
                      
            # deposit receipt is added when Dataverse.addStudy() is called on
            # this study
            self.lastDepositReceipt = None 
            
            self.editUri = editUri
            self.editMediaUri = editMediaUri
            
            self.hostDataverse = hostDataverse # generally used for sword connection
            
    def __repr__(self):
        studyObject = pprint.pformat(self.__dict__)
        entryObject = self.entry.pretty_print()
        return """STUDY ========= "
        study=
{so}
        
        entry=
{eo}
/STUDY ========= """.format(so=studyObject,eo=entryObject)
                
    @classmethod
    def CreateStudyFromDict(cls, dict):
        return cls(dict["title"],
                   dict["author"],
                   dict["abstract"])
    
    @classmethod
    def CreateStudyFromAtomEntryXmlString(cls, xml):
        title = utils.get_elements(xml, tag="title", numberOfElements=1).text
        
        return cls(title, atomEntryXml=xml)
    
    @classmethod
    def CreateStudyFromAtomEntryXmlFile(cls, xmlFilePath):
        study = None
        with open(xmlFilePath) as f:
            xml = f.read()
            study = cls.CreateStudyFromAtomEntryXmlString(xml=xml)
            
        return study
                    
    @classmethod
    def CreateStudyFromEntryElement(cls, entryElement, hostDataverse=None):
        idElement = utils.get_elements(entryElement, 
                                       tag="id", 
                                       numberOfElements=1)
                                    
        titleElement = utils.get_elements(entryElement, 
                                       tag="title", 
                                       numberOfElements=1)
                                            
        editMediaLinkElement = utils.get_elements(entryElement, 
                                                  tag="link", 
                                                  attribute="rel", 
                                                  attributeValue="edit-media", 
                                                  numberOfElements=1)

        editMediaLink = editMediaLinkElement.get("href") if editMediaLinkElement is not None else None

        return cls(idElement.text,     
                   titleElement.text,        
                   editUri=entryElement.base,   # edit iri
                   editMediaUri=editMediaLink,
                   hostDataverse=hostDataverse)  # edit-media iri
                   
    def get_study_statement(self):
        studyStatement = self.hostDataverse.connection.swordConnection.get_resource(self.editUri).content
        return studyStatement
    
    def get_list_of_files(self):
        atomXml = self.get_study_statement()
        statementLink = utils.get_elements(atomXml, 
                                           tag="link", 
                                           attribute="rel", 
                                           attributeValue="http://purl.org/net/sword/terms/statement", 
                                           numberOfElements=1)
        studyStatementLink = statementLink.get("href")

        atomStatement = self.hostDataverse.connection.swordConnection.get_atom_sword_statement(studyStatementLink)
        
        for res in atomStatement.resources:
            print etree.tostring(res.dom, pretty_print=True)
        
        return atomStatement.resources

    def add_files(self, filepaths, replaceStudyContents=False):        
        print "Uploading files: ", filepaths
        
        deleteAfterUpload = False

        # if we have more than one file, or one file that is not a zip, we need to zip it
        if len(filepaths) != 1 or mimetypes.guess_type(filepaths[0], strict=True) != "application/zip":
            filepath = self._zipFiles(filepaths)
            deleteAfterUpload = True
        else:
            filepath = filepaths[0]
            
        fileMimetype = mimetypes.guess_type(filepath, strict=True)
        filename = os.path.basename(filepath)
        
        with open(filepath, "rb") as pkg:
            if not replaceStudyContents:
                depositReceipt = self.hostDataverse.connection.swordConnection.append(dr = self.lastDepositReceipt,
                                se_iri = self.editMediaUri,
                                payload = pkg,
                                mimetype = fileMimetype,
                                filename = filename,
                                packaging = 'http://purl.org/net/sword/package/SimpleZip')
            else:
                depositReceipt = self.hostDataverse.connection.swordConnection.update(dr = self.lastDepositReceipt,
                            #edit_iri = self.editUri,
                            #edit_media_iri = self.editMediaUri,
                            payload = pkg,
                            mimetype = fileMimetype,
                            filename = filename,
                            packaging = 'http://purl.org/net/sword/package/SimpleZip')

            self.lastDepositReceipt = depositReceipt
            pprint.pprint(depositReceipt, indent=3)
        
        if deleteAfterUpload:
            print "Deleting temporary zip file: ", filepath
            os.remove(filepath)    
            
    def _zipFiles(self, filesToZip, pathToStoreZip=None):
        zipFilePath = os.path.join(os.getenv("TEMP", "/tmp"),  "swordUploadPackage.zip") if not pathToStoreZip else pathToStoreZip
        
        with ZipFile(zipFilePath, 'w') as zipFile:
            for fileToZip in filesToZip:
                zipFile.write(fileToZip)
            
        return zipFilePath
                   
   
