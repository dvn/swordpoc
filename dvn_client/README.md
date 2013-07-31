##Requirements for dvn-client
----------------------------
1. Python 2.7 (already on OSX)
2. gcc compiler (xcode + command line tools, or [standalone install](https://github.com/kennethreitz/osx-gcc-installer#readme)
3. Get the lxml module for python:
    sudo easy_install lxml
4.	Forked sword2 module for python:
a. Clone LINK forked repo python-client-sword2
b. navigate to root folder for python-client sword2
    sudo python setup.py install
	
##Setting up a config
------------------------
You need a config.py file to run.  It needs the following lines at the moment:
    DEFAULT_USERNAME = ""
    DEFAULT_PASSWORD = ""
    DEFAULT_HOST = ""
    DEFAULT_CERT = "../resources/dvn-build.hmdc.harvard.edu" #see below for info on the cert
	
##Executing the Client from the Command Line
------------------------------------------
Right now, we only run with settings from the tests.py file. Feel free to edit that.
1. Navigate to dvn\_client/src in the terminal
2. Run the client
    python dvn_client.py --config config.py --runTests tests.py


##Setup the Python Project in NetBeans (7.3.1)
------------------------------
This is optional. You can edit the source with whatever you please, but the NetBeans project is included for your convenience.
1.  Install and open NetBeans	
2.  Tools > Plugins
3.	Settings > Add
4.	Name: Deadlock
URL: http://deadlock.netbeans.org/hudson/job/nbms-and-javadoc/lastSuccessfulBuild/artifact/nbbuild/nbms/updates.xml.gz

4.	Available Plugins > Search > “Python”
5.	Check the following three projects:
a.	Python
b.	Jython Distribution
c.	Sample Python/Jython Projects
6.	Install
7.	Restart NetBeans

##Get PEM Certificate for the server you care about:
-----------------------------------
If you are using a self-signed certificate, you may see an SSL error when you try to hit the server. In that case, follow these instructions.

1. Open private/incognito window (in case you have already added a security exception) in FireFox (instructions will be slightly different for other browsers)
2. Go to: https://{SERVER}/dvn/api/data-deposit/swordv2/service-document
3. Add Exception > View > Details > Export
4. Save the PEM to the “resources” folder of the dvn\_client project
5. When calling the Dataverse.connect() or Dataverse() constructor, pass a path to this file as cert=\[PATH\_TO\_CERTIFICATE\]
