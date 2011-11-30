import json

class ParseSauceURL:
    def __init__(self, url):
        self.url = url

        self.fields = {}
        fields = self.url.split(':')[1][1:].split('&')
        for field in fields:
            [key, value] = field.split('=')    
            self.fields[key] = value

    def getValue(self, key):
        if key in self.fields:
            return self.fields[key]
        else:
            return ""

    def getUserName(self):
        return self.getValue("username")

    def getAccessKey(self):
        return self.getValue("access-key")

    def getJobName(self):
        return self.getValue("job-name")

    def getOS(self):
        return self.getValue("os")
    
    def getBrowser(self):
        return self.getValue('browser')

    def getBrowserVersion(self):
        return self.getValue('browser-version')
    
    def getFirefoxProfileURL(self):
        return self.getValue('firefox-profile-url')

    def getMaxDuration(self):
        try:
            return int(self.getValue('max-duration'))
        except:
            return 0

    def getIdleTimeout(self):
        try:
            return int(self.getValue('idle-timeout'))
        except:
            return 0

    def getUserExtensionsURL(self):
        return self.getValue('user-extensions-url')

    def toJSON(self):
        return json.dumps(self.fields, sort_keys=False)