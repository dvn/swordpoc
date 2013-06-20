package edu.harvard.iq.swordpoc;

import java.util.Arrays;
import org.apache.log4j.Logger;
import org.swordapp.server.AuthCredentials;
import org.swordapp.server.ServiceDocument;
import org.swordapp.server.ServiceDocumentManager;
import org.swordapp.server.SwordAuthException;
import org.swordapp.server.SwordConfiguration;
import org.swordapp.server.SwordError;
import org.swordapp.server.SwordServerException;

public class ServiceDocumentManagerImpl implements ServiceDocumentManager {

    private static Logger log = Logger.getLogger(ServiceDocumentManagerImpl.class);

    @Override
    public ServiceDocument getServiceDocument(String sdUri, AuthCredentials authCredentials, SwordConfiguration config)
            throws SwordError, SwordServerException, SwordAuthException {
        ServiceDocument service = new ServiceDocument();
        service.setMaxUploadSize(config.getMaxUploadSize());
//        SwordWorkspace workspace = new SwordWorkspace();
//        workspace.setTitle("Main Site");
//        SwordCollection swordCollection = new SwordCollection();
        String uuid = "a4f21cdc-f20c-4c82-b63e-5df81f809417";
//        swordCollection.setHref("http://localhost:8080/JavaServer2.0/servicedocument/col-uri/" + uuid);
//        swordCollection.setTitle("Collection " + uuid);
//        swordCollection.setAccept("*/*");
//        swordCollection.setCollectionPolicy("Collection Policy");
//        swordCollection.setAbstract("Collection Description");
//        swordCollection.setTreatment("Treatment Description");
//        swordCollection.setAcceptPackaging(Arrays.asList(UriRegistry.PACKAGE_SIMPLE_ZIP));
//        workspace.addCollection(swordCollection);
//        service.addWorkspace(workspace);
        return service;

    }
}
