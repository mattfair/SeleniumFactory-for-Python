import os
from selenium import webdriver
from selenium import selenium

from ParseSauceURL import *

"""
  Simple interface factory to create Selenium objects, inspired by the SeleniumFactory interface 
  from https://github.com/infradna/selenium-client-factory for Java.
 
  <p>
  Compared to directly initializing {@link com.thoughtworks.selenium.DefaultSelenium}, this additional indirection
  allows the build script or a CI server to control how you connect to the selenium.
  This makes it easier to run the same set of tests in different environments without
  modifying the test code.
 
  <p>
  This is analogous to how you connect to JDBC &mdash; you normally don't directly
  instantiate a specific driver, and instead you do {@link DriverManager#getConnection(String)}.
"""
class SeleniumFactory:
    
    def __init__(self):
        pass
    
    """
     Uses a driver specified by the 'SELENIUM_DRIVER' environment variable,
     and run the test against the domain specified in 'SELENIUM_URL' system property or the environment variable.
     If no variables exist, a local Selenium driver is created.
    """
    def create(self):
        if 'SELENIUM_STARTING_URL' not in os.environ:
            startingUrl = "http://saucelabs.com"
        else:
            startingUrl = os.environ['SELENIUM_STARTING_URL']
        
        if 'SELENIUM_DRIVER' in os.environ and  'SELENIUM_HOST' in os.environ and 'SELENIUM_PORT' in os.environ:
            parse = ParseSauceURL(os.environ["SELENIUM_DRIVER"])  
            driver = selenium(os.environ['SELENIUM_HOST'], os.environ['SELENIUM_PORT'], parse.toJSON(), startingUrl)
            driver.start()
            driver.set_timeout(90000)
            
            return driver
        else:
            driver = selenium("localhost", 4444, "*firefox", startingUrl)
            driver.start()
            driver.set_timeout(90000)
            
            return driver

    """
     Uses a driver specified by the 'SELENIUM_DRIVER' system property or the environment variable,
     and run the test against the domain specified in 'SELENIUM_STARTING_URL' system property or the environment variable.
     If no variables exist, a local Selenium web driver is created.
    """
    def createWebDriver(self):
        
        if 'SELENIUM_STARTING_URL' not in os.environ:
            startingUrl = "http://saucelabs.com"
        else:
            startingUrl = os.environ['SELENIUM_STARTING_URL']
        
        if 'SELENIUM_DRIVER' in os.environ and 'SELENIUM_HOST' in os.environ and 'SELENIUM_PORT' in os.environ:            
            parse = ParseSauceURL(os.environ["SELENIUM_DRIVER"])    
  
            desired_capabilities = {}
            if parse.getBrowser() == 'android':
                desired_capabilities = webdriver.DesiredCapabilities.ANDROID
            elif parse.getBrowser() == 'googlechrome':
                desired_capabilities = webdriver.DesiredCapabilities.CHROME
            elif parse.getBrowser() == 'firefox':
                desired_capabilities = webdriver.DesiredCapabilities.FIREFOX
            elif parse.getBrowser() == 'htmlunit':
                desired_capabilities = webdriver.DesiredCapabilities.HTMLUNIT
            elif parse.getBrowser() == 'iexplorer':
                desired_capabilities = webdriver.DesiredCapabilities.INTERNETEXPLORER
            elif parse.getBrowser() == 'iphone':
                desired_capabilities = webdriver.DesiredCapabilities.IPHONE
            else:
                desired_capabilities = webdriver.DesiredCapabilities.FIREFOX
                      
            desired_capabilities['version'] = parse.getBrowserVersion()
            
            if 'SELENIUM_PLATFORM' in os.environ:
                desired_capabilities['platform'] = os.environ['SELENIUM_PLATFORM']
            else:
                #work around for name issues in Selenium 2
                if 'Windows 2003' in parse.getOS():
                    desired_capabilities['platform'] = 'XP'
                elif 'Windows 2008' in parse.getOS():
                    desired_capabilities['platform'] = 'VISTA'
                elif 'Linux' in parse.getOS():
                    desired_capabilities['platform'] = 'LINUX'
                else:
                    desired_capabilities['platform'] = parse.getOS()
                
            desired_capabilities['name'] = parse.getJobName()
                        
            command_executor="http://%s:%s@%s:%s/wd/hub"%(parse.getUserName(), parse.getAccessKey(), os.environ['SELENIUM_HOST'],os.environ['SELENIUM_PORT'])
            print desired_capabilities
            print command_executor
            
            driver=webdriver.Remote(desired_capabilities=desired_capabilities, command_executor=command_executor)
            driver.get(startingUrl)
            
            return driver
            
        else:
            return webdriver.Firefox()
