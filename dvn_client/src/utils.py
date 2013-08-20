__author__="peterbull"
__date__ ="$Aug 16, 2013 12:07:48 PM$"

import lxml
        
# factor out xpath operations so we don't have to look at its ugliness all
# over the place
def get_elements(rootElement, tag=None, namespace=None, attribute=None, attributeValue=None, numberOfElements=None):
    #except either an lxml.Element or a string of xml
    #if a string, convert to etree element
    if isinstance(rootElement, str):
        rootElement = lxml.etree.XML(rootElement)
    
    if not namespace:
        namespace = rootElement.nsmap[None]
    
    if not tag:
        xpath = "*"
    else:
        xpath = "{{{ns}}}{tg}".format(ns=namespace, tg=tag)
    
    if attribute and not attributeValue:
        xpath += "[@{att}]".format(att=attribute)
    elif not attribute and attributeValue:
        raise Exception("You must pass an attribute with attributeValue")
    elif attribute and attributeValue:
        xpath += "[@{att}='{attVal}']".format(att=attribute, attVal=attributeValue)
    
    elements = None
    try:
        #if we know we're looking for one, return that element instead of a list
        if numberOfElements == 1:
            elements = rootElement.find(xpath)
        else:
            elements = rootElement.findall(xpath)
        
        if numberOfElements and numberOfElements != 1 and len(elements) != numberOfElements:
            raise Exception("Wrong number of elements found. Expected {0} and found {1}.".format(numberOfElements, len(elements)))
        
    except Exception as e:
        print """
Exception thrown trying to get_elements with the following parameters:
exp='{e}'
xpath='{xp}'
xml=
{xml}""".format(e=e, xp=xpath, xml=lxml.etree.tostring(rootElement, pretty_print=True))
    
    return elements