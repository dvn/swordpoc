package edu.harvard.iq.swordpoc;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import org.apache.abdera.i18n.iri.IRI;
import org.apache.log4j.Logger;
import org.swordapp.server.AuthCredentials;
import org.swordapp.server.CollectionDepositManager;
import org.swordapp.server.Deposit;
import org.swordapp.server.DepositReceipt;
import org.swordapp.server.SwordAuthException;
import org.swordapp.server.SwordConfiguration;
import org.swordapp.server.SwordError;
import org.swordapp.server.SwordServerException;

public class CollectionDepositManagerImpl implements CollectionDepositManager {

    private static Logger log = Logger.getLogger(ServiceDocumentManagerImpl.class);

    @Override
    public DepositReceipt createNew(String collectionUri, Deposit deposit, AuthCredentials authCredentials, SwordConfiguration config)
            throws SwordError, SwordServerException, SwordAuthException {

        String tempDirectory = config.getTempDirectory();
        String uploadDirPath = tempDirectory + File.separator + "uploads";
        File uploadDir = new File(uploadDirPath);
        try {
            uploadDir.mkdir();
            String filename = uploadDirPath + File.separator + deposit.getFilename();
            log.info("attempting write to " + filename);
            try {
                InputStream inputstream = deposit.getInputStream();
                OutputStream outputstream = new FileOutputStream(new File(filename));
                try {
                    byte[] buf = new byte[1024];
                    int len;
                    while ((len = inputstream.read(buf)) > 0) {
                        outputstream.write(buf, 0, len);
                    }
                } finally {
                    inputstream.close();
                    outputstream.close();
                    log.info("write to " + filename + " complete");
                }
            } catch (IOException e) {
                throw new SwordServerException(e);
            }
        } catch (Exception e) {
            log.info("unable to create directory: " + uploadDirPath);
            throw new SwordAuthException(e);
        }

        DepositReceipt fakeDepositReceipt = new DepositReceipt();
        IRI fakeIri = new IRI("fakeIri");
        fakeDepositReceipt.setLocation(fakeIri);
        fakeDepositReceipt.setEditIRI(fakeIri);
        return fakeDepositReceipt;
    }
}
