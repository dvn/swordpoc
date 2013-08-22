#WARNING: The Data Deposit API is currently unstable. Use this client at your own risk. :)

###Requirements for dvn-client
----------------------------
Note: you can also run this using the Vagrant file in the root of this repo. The init.pp includes steps 1-5 below, so if you use that image you can skip to "Setting up a config"


1. Python 2.6+
2. gcc compiler (xcode + command line tools, or [standalone install](https://github.com/kennethreitz/osx-gcc-installer#readme))
3. Get the lxml module for python: 

    `sudo easy_install lxml`

4. If your version of python < 2.7 get the argparse module: 

    `sudo easy_install argparse`

5. Forked sword2 module for python:
    1. Clone [forked repo python-client-sword2](https://github.com/pjbull/python-client-sword2)
    
        `git clone https://github.com/pjbull/python-client-sword2.git`
    
    2. navigate to root folder for python-client-sword2
    
       `sudo python setup.py install`
	
###Setting up a config
------------------------
You need a config.py file to run.  It needs the following lines at the moment:

```python

    DEFAULT_USERNAME = ""
    DEFAULT_PASSWORD = ""
    DEFAULT_HOST = ""
    DEFAULT_CERT = "../resources/dvn-build.hmdc.harvard.edu" #see below for info on the cert
    
```
	
###Executing the Client from the Command Line
------------------------------------------
Right now, we only run with settings from the tests.py file. Feel free to edit that.

1. Navigate to dvn\_client/src in the terminal
2. Run the client:

    `python dvn_client.py --config config.py --runTests tests.py`
    
3. To run the tests, run this command (for more options see [unittest](http://docs.python.org/2/library/unittest.html#assert-methods))

    `python dvn_test.py`


###Setup the Python Project in NetBeans (7.3.1)
------------------------------
This is optional. You can edit the source with whatever you please, but the NetBeans project is included for your convenience.

1. Install and open NetBeans	
2. Tools > Plugins
3. Settings > Add
    a. Name: Deadlock
    b. URL: http://deadlock.netbeans.org/hudson/job/nbms-and-javadoc/lastSuccessfulBuild/artifact/nbbuild/nbms/updates.xml.gz

4. Available Plugins > Search > "Python"
5. Check the following three projects:
    a. Python
    b. Jython Distribution
    c. Sample Python/Jython Projects
6. Install
7. Restart NetBeans

###Get PEM Certificate (optional):
-----------------------------------
If you are using a self-signed certificate, you may see an SSL error when you try to hit the server. In that case, follow these instructions.

1. Open private/incognito window (in case you have already added a security exception) in FireFox (instructions will be slightly different for other browsers)
2. Go to: https://{SERVER}/dvn/api/data-deposit/swordv2/service-document
3. Add Exception > View > Details > Export
4. Save the PEM to the “resources” folder of the dvn\_client project
5. When calling `Dataverse.connect()` or `Dataverse()` constructor, pass a path to this file as `cert=[PATH_TO_CERTIFICATE]`


###Examples:
---------------------------------
Prereq for all of these is to get a dataverse:
```python

    dvc = DvnConnection(username=DEFAULT_USERNAME,
                        password=DEFAULT_PASSWORD, 
                        host=DEFAULT_HOST, 
                        cert=DEFAULT_CERT)
                        
        
    dvs = dvc.get_dataverses()
    dv = dvs[0]    
```

Create a study:
```python

    PICS_OF_CATS_STUDY = {
    "title" : "This Study is about Pictures of Cats",
    "author" : "Peter Bull",
    "abstract" : "In this study we prove that there can be pictures of cats passed through the intertubes.",
    }
    
    s = Study.CreateStudyFromDict(PICS_OF_CATS_STUDY)
    dv.add_study(s)
    
```

Add files to a study with a zip file

```python

    study = dv.get_studies()[0]
    study.add_file("path_to_zip")
    
```

Display a study atom entry (contains data citation (bibliographicCitation) statement uri, latestVersionState)

```python

    study = dv.get_studies()[0]
    study.add_file("path_to_zip")
    
```

Display a study statement (contains feed of file entries)

```python

    study = dv.get_studies()[0]
    study.get_statement()
    
```

Delete a file by database id

```python

    study = dv.get_studies()[0]
    file = study.get_files()[0]
    study.delete_file(file)
    
```

Replacing cataloging information (title, author, etc.) for a study

List studies in a dataverse

```python

    for s in dv.get_studies():
    	print s
    
```

Delete a study (non-released studies only)

```python

    study = dv.get_studies()[0]
	dv.delete_study(study)
    
```

Deaccession a study (released studies only)

```python

    study = dv.get_studies()[0]
    study.release()
	dv.delete_study(study)
    
```

Release a study

```python

    study = dv.get_studies()[0]
    study.release()
    
```

Determine if a dataverse has been released (dataverseHasBeenReleased boolean)
```python

    dv.is_released()
    
```
