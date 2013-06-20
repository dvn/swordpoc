# SWORD (Simple Web-service Offering Repository Deposit) v2 Proof Of Concept

This repo is a Vagrant environment that supports spinning up two different implementations of SWORD v2 servers:

1. Simple Sword Server (SSS), the reference implementation written in Python
2. swordpoc, a very minimal implemention written in Java

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
