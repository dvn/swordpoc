# SWORD (Simple Web-service Offering Repository Deposit) v2 Proof Of Concept

This repo is a Vagrant environment that supports spinning up two different implementations of SWORD v2 servers:

1. Simple Sword Server (SSS), the reference implementation written in Python
2. swordpoc, a very minimal implemention written in Java

## Spinning up the Vagrant VM

To use the Vagrant VM, install Vagrant from http://vagrantup.com and VirtualBox from http://virtualbox.org and run the following commands:

    git clone https://github.com/dvn/swordpoc.git
    git submodule init
    git submodule update
    vagrant up
    vagrant ssh

## Running Simple Sword Server (SSS) in Vagrant

In one of the steps below, we clone the code from https://github.com/swordapp/Simple-Sword-Server

The main point of this exercise is to deposit "example.zip" into the SWORD server using curl.

Please note that you'll need to replace the UUIDs and timestamp below based on the output you see.

    vagrant up
    vagrant ssh
    sudo su -
    git clone https://github.com/swordapp/Simple-Sword-Server.git
    cd Simple-Sword-Server
    python setup.py install
    mkdir /tmp/sss-server
    cd /tmp/sss-server
    cp /root/Simple-Sword-Server/sss/sss-1.0.py sss.py
    easy_install web.py
    easy_install lxml==2.3.4
    python sss.py &
    cd /tmp/sss-client
    curl -s -i -H "X-On-Behalf-Of: obo" http://sword:sword@localhost:8080/sd-uri | grep col-uri | head -1
    # note UUID from output above
    curl -i -H "X-On-Behalf-Of: obo" --http1.0 --data-binary "@example.zip" -H "Content-Disposition: filename=example.zip" -H "Content-Type: application/zip" sword:sword@localhost:8080/col-uri/f19ae45f-5455-4b10-96a4-25396bb8a228
    cd /tmp/sss-server/store/f19ae45f-5455-4b10-96a4-25396bb8a228/6d56e25c-c837-4138-b7c7-23e6a912d3eb
    unzip 2013-06-17T16\:52\:36Z_example.zip 
    cat example/hello.txt

### A more complicated SSS example: two step deposit

In the example above, "example.zip" is deposited into a SWORD collection, but let's imagine a more complicated example.

Let's say we want to perform the following steps:

1. Create a resource with an atom entry (i.e. an XML file): http://swordapp.github.io/SWORDv2-Profile/SWORDProfile.html#protocoloperations_creatingresource_entry
2. Upload example.zip to the newly created resource: http://swordapp.github.io/SWORDv2-Profile/SWORDProfile.html#protocoloperations_editingcontent_binary

These steps translate into two distinct HTTP request, as explained by the SWORDv2 spec lead, Richard Jones...

> It is my plan and hope to back all of the multipart OUT of the sword
> spec for a future version (like a 2.1), so I strongly recommend not
> using multipart deposit.  Instead do a POST of an Atom Entry and a PUT
> of the Media Resource in two distinct HTTP requests.

... at http://www.mail-archive.com/sword-app-tech@lists.sourceforge.net/msg00327.html

#### Retrieve a service document (GET)

(For brevity, we only include 2 of the 10 collections in the Service Document)

    [root@logus sss-client]# curl -s http://sword:sword@localhost:8080/sd-uri
    <service xmlns:dcterms="http://purl.org/dc/terms/" xmlns:sword="http://purl.org/net/sword/terms/" xmlns:atom="http://www.w3.org/2005/Atom" xmlns="http://www.w3.org/2007/app">
      <sword:version>2.0</sword:version>
      <sword:maxUploadSize>16777216</sword:maxUploadSize>
      <workspace>
        <atom:title>Main Site</atom:title>
        <collection href="http://localhost:8080/col-uri/4e1f7a9a-f8d4-4795-b230-195acb6680c9">
          <atom:title>Collection 4e1f7a9a-f8d4-4795-b230-195acb6680c9</atom:title>
          <accept>*/*</accept>
          <accept alternate="multipart-related">*/*</accept>
          <sword:collectionPolicy>Collection Policy</sword:collectionPolicy>
          <dcterms:abstract>Collection Description</dcterms:abstract>
          <sword:mediation>true</sword:mediation>
          <sword:treatment>Treatment description</sword:treatment>
          <sword:acceptPackaging>http://purl.org/net/sword/package/SimpleZip</sword:acceptPackaging>
          <sword:acceptPackaging>http://purl.org/net/sword/package/Binary</sword:acceptPackaging>
          <sword:acceptPackaging>http://purl.org/net/sword/package/METSDSpaceSIP</sword:acceptPackaging>
          <sword:service>http://localhost:8080/sd-uri/95234b85-c987-45f2-bbc6-05f79298db35</sword:service>
        </collection>
        <collection href="http://localhost:8080/col-uri/cf9ac85a-2f36-4843-af8f-e00d7b2a1ac5">
          <atom:title>Collection cf9ac85a-2f36-4843-af8f-e00d7b2a1ac5</atom:title>
          <accept>*/*</accept>
          <accept alternate="multipart-related">*/*</accept>
          <sword:collectionPolicy>Collection Policy</sword:collectionPolicy>
          <dcterms:abstract>Collection Description</dcterms:abstract>
          <sword:mediation>true</sword:mediation>
          <sword:treatment>Treatment description</sword:treatment>
          <sword:acceptPackaging>http://purl.org/net/sword/package/SimpleZip</sword:acceptPackaging>
          <sword:acceptPackaging>http://purl.org/net/sword/package/Binary</sword:acceptPackaging>
          <sword:acceptPackaging>http://purl.org/net/sword/package/METSDSpaceSIP</sword:acceptPackaging>
          <sword:service>http://localhost:8080/sd-uri/bd46dd22-420c-4606-abe4-8c6f5eccbb63</sword:service>
        </collection>
      </workspace>
    </service>

#### Create a resource from an atom entry (POST)

We POST (using --data-binary) our atom-entry-study.xml content...

    [root@logus sss-client]# cat atom-entry-study.xml
    <?xml version="1.0"?>
    <entry xmlns="http://www.w3.org/2005/Atom"
           xmlns:dcterms="http://purl.org/dc/terms/">
       <title>The first study for the New England Journal of Coffee dataverse</title>
       <id>urn:uuid:1225c695-cfb8-4ebb-aaaa-80da344efa6a</id>
       <updated>2005-10-07T17:17:08Z</updated>
       <author><name>Creator</name></author>
       <summary type="text">The abstract</summary>
       <dcterms:title>Roasting at Home</dcterms:title>
       <dcterms:creator>Peets, John</dcterms:creator>
       <dcterms:creator>Stumptown, Jane</dcterms:creator>
    </entry>
    [root@logus sss-client]# 

... to the first collection we saw in the service document ("4e1f7a9a-f8d4-4795-b230-195acb6680c9"):

    [root@logus sss-client]# curl --http1.0 --data-binary "@atom-entry-study.xml" -H "Content-Type: application/atom+xml" http://sword:sword@localhost:8080/col-uri/4e1f7a9a-f8d4-4795-b230-195acb6680c9
    <entry xmlns:dcterms="http://purl.org/dc/terms/" xmlns:sword="http://purl.org/net/sword/terms/" xmlns="http://www.w3.org/2005/Atom">
      <title>The first study for the New England Journal of Coffee dataverse</title>
      <id>tag:container@sss/4e1f7a9a-f8d4-4795-b230-195acb6680c9/70566b02-76a9-496d-b1bb-356ba9acc7f2</id>
      <updated>2013-07-17T15:40:32Z</updated>
      <author>
        <name>Creator</name>
      </author>
      <summary type="text">The abstract</summary>
      <generator uri="http://www.swordapp.org/sss" version="1.0"/>
      <dcterms:date>2005-10-07T17:17:08Z</dcterms:date>
      <dcterms:abstract>The abstract</dcterms:abstract>
      <dcterms:title>The first study for the New England Journal of Coffee dataverse</dcterms:title>
      <dcterms:title>Roasting at Home</dcterms:title>
      <dcterms:creator>Creator</dcterms:creator>
      <dcterms:creator>Peets, John</dcterms:creator>
      <dcterms:creator>Stumptown, Jane</dcterms:creator>
      <sword:verboseDescription>SSS has done this, that and the other to process the deposit</sword:verboseDescription>
      <sword:treatment>Treatment description</sword:treatment>
      <link rel="alternate" href="http://localhost:8080/html/4e1f7a9a-f8d4-4795-b230-195acb6680c9/70566b02-76a9-496d-b1bb-356ba9acc7f2"/>
      <content type="application/zip" src="http://localhost:8080/cont-uri/4e1f7a9a-f8d4-4795-b230-195acb6680c9/70566b02-76a9-496d-b1bb-356ba9acc7f2"/>
      <link rel="edit" href="http://localhost:8080/edit-uri/4e1f7a9a-f8d4-4795-b230-195acb6680c9/70566b02-76a9-496d-b1bb-356ba9acc7f2"/>
      <link rel="edit-media" href="http://localhost:8080/em-uri/4e1f7a9a-f8d4-4795-b230-195acb6680c9/70566b02-76a9-496d-b1bb-356ba9acc7f2"/>
      <link rel="edit-media" type="application/atom+xml;type=feed" href="http://localhost:8080/em-uri/4e1f7a9a-f8d4-4795-b230-195acb6680c9/70566b02-76a9-496d-b1bb-356ba9acc7f2.atom"/>
      <link rel="http://purl.org/net/sword/terms/add" href="http://localhost:8080/edit-uri/4e1f7a9a-f8d4-4795-b230-195acb6680c9/70566b02-76a9-496d-b1bb-356ba9acc7f2"/>
      <sword:packaging>http://purl.org/net/sword/package/SimpleZip</sword:packaging>
      <link rel="http://purl.org/net/sword/terms/statement" type="application/atom+xml;type=feed" href="http://localhost:8080/state-uri/4e1f7a9a-f8d4-4795-b230-195acb6680c9/70566b02-76a9-496d-b1bb-356ba9acc7f2.atom"/>
      <link rel="http://purl.org/net/sword/terms/statement" type="application/rdf+xml" href="http://localhost:8080/state-uri/4e1f7a9a-f8d4-4795-b230-195acb6680c9/70566b02-76a9-496d-b1bb-356ba9acc7f2.rdf"/>
    </entry>

This creates a number of files under the "4e1f7a9a-f8d4-4795-b230-195acb6680c9" collection:

    [root@logus sss-client]# cd /tmp/sss-server/store/4e1f7a9a-f8d4-4795-b230-195acb6680c9
    [root@logus 4e1f7a9a-f8d4-4795-b230-195acb6680c9]# ls -1d */*
    70566b02-76a9-496d-b1bb-356ba9acc7f2/atom.xml
    70566b02-76a9-496d-b1bb-356ba9acc7f2/sss_deposit-receipt.xml
    70566b02-76a9-496d-b1bb-356ba9acc7f2/sss_metadata.xml
    70566b02-76a9-496d-b1bb-356ba9acc7f2/sss_statement.atom.xml
    70566b02-76a9-496d-b1bb-356ba9acc7f2/sss_statement.xml

We can think of "70566b02-76a9-496d-b1bb-356ba9acc7f2" as the unique identifier for the resource we just created. It contains a number of files:

- `atom.xml` matches exactly the `atom-entry-study.xml` file we used to create the resource.
- `sss_deposit-receipt.xml` is the output we saw from the curl command when we created the resource.
- `sss_metadata.xml` is a simpler version of `atom.xml` (i.e. `<dcterms:creator>` becomes just `<creator>`).
- `sss_statement.atom.xml` shows the state of the resource, indicating the following: "The work has passed through review and is now in the archive".
- `sss_statement.xml` is similar to `sss_statement.atom.xml` in that it shows the state, but is longer and in RDF format.

#### Upload example.zip (PUT)

Next we upload example.zip to the resource we created ("70566b02-76a9-496d-b1bb-356ba9acc7f2").

We use --upload-file for this, which does a PUT.

    [root@logus 4e1f7a9a-f8d4-4795-b230-195acb6680c9]# cd /tmp/sss-client
    [root@logus sss-client]# curl --upload-file example.zip -H "Content-Disposition: filename=example.zip" -H "Content-Type: application/zip" http://sword:sword@localhost:8080/em-uri/4e1f7a9a-f8d4-4795-b230-195acb6680c9/70566b02-76a9-496d-b1bb-356ba9acc7f2
    [root@logus sss-client]# 

We don't see any output above but the console output indicates some activity...

    2013-07-17 16:14:23,311 - sss - INFO - Authentication required
    2013-07-17 16:14:23,311 - sss - INFO - Authentication details: sword:sword; On Behalf Of: None
    /tmp/sss-server/store
    2013-07-17 16:14:23,312 - sss - INFO - Received Binary deposit request
    2013-07-17 16:14:23,313 - sss - INFO - Replace request has file content - updating
    2013-07-17 16:14:23,314 - sss - INFO - Content replaced
    127.0.0.1:39706 - - [17/Jul/2013 16:14:23] "HTTP/1.1 PUT /em-uri/4e1f7a9a-f8d4-4795-b230-195acb6680c9/70566b02-76a9-496d-b1bb-356ba9acc7f2" - 204 No Content

... and the files in the directory for the resource have changed:

    [root@logus 70566b02-76a9-496d-b1bb-356ba9acc7f2]# git status
    # On branch master
    # Changed but not updated:
    #   (use "git add/rm <file>..." to update what will be committed)
    #   (use "git checkout -- <file>..." to discard changes in working directory)
    #
    #       deleted:    atom.xml
    #       modified:   sss_deposit-receipt.xml
    #       modified:   sss_statement.atom.xml
    #       modified:   sss_statement.xml
    #
    # Untracked files:
    #   (use "git add <file>..." to include in what will be committed)
    #
    #       2013-07-17T16:14:23Z_example.zip
    no changes added to commit (use "git add" and/or "git commit -a")
    [root@logus 70566b02-76a9-496d-b1bb-356ba9acc7f2]# 

The `atom.xml` file has been deleted, which was an exact copy of the `atom-entry-study.xml` file we used to create the resource. Some of the content from that file such as our `<dcterms:creator>` entries are still preserved in `sss_deposit-receipt.xml` and `sss_metadata.xml`.

## Running swordpoc in Vagrant

Build and deploy the SWORD v2 server implementation in Java with the commands below. Running java2.sh should upload a "example.zip" to /tmp/uploads

    vagrant up
    vagrant ssh
    cd /downloads
    ./download.sh
    /swordpoc/java
    unzip glassfish-3.1.2.2.zip
    /downloads/glassfish3/glassfish/bin/asadmin start-domain
    cd ~
    # FIXME: is org.swordapp:sword2-server:jar published anywhere?
    git clone https://github.com/swordapp/JavaServer2.0.git
    cd JavaServer2.0
    mvn install
    cd /swordpoc/java
    mvn package
    /downloads/glassfish3/glassfish/bin/asadmin deploy --force /swordpoc/java/target/swordpoc.war
    ./java1.sh
    ./java2.sh
