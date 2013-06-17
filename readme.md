# SWORD (Simple Web-service Offering Repository Deposit) v2 Proof Of Concept

Based on https://github.com/swordapp/Simple-Sword-Server

Please note that you'll need to replace the UUIDs and timestamp below.

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
