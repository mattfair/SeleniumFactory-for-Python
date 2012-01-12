import urllib2
import json
import base64

url = 'https://saucelabs.com/rest/%s/%s/%s'

"""
This class provides several helper methods to invoke the Sauce REST API.
"""
class SauceRest:
    def __init__(self, user, key):
        self.user = user
        self.key = key

    def buildUrl(self, version, suffix):
        return url %(version, self.user, suffix)

    """
    Updates a Sauce Job with the data contained in the attributes dict
    """
    def update(self, id, attributes):
        url = self.buildUrl("v1", "jobs/" + id)
        data = json.dumps(attributes)
        return self.invokePut(url, self.user, self.key, data)

    """
    Retrieves the details for a Sauce job in JSON format
    """
    def get(self, id):
        url = self.buildUrl("v1", "jobs/" + id)
        return self.invokeGet(url, self.user, self.key)

    def invokePut(self, theurl, username, password, data):
        request = urllib2.Request(theurl, data, {'content-type': 'application/json'})
        base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
        request.add_header("Authorization", "Basic %s" % base64string)
        request.get_method = lambda: 'PUT'
        htmlFile = urllib2.urlopen(request)
        return htmlFile.read()

    def invokeGet(self, theurl, username, password):
        request = urllib2.Request(theurl)
        base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
        request.add_header("Authorization", "Basic %s" % base64string)
        htmlFile = urllib2.urlopen(request)
        return htmlFile.read()