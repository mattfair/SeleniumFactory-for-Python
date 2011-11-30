SeleniumFactory for Python
---------------------------

Simple interface factory to create Selenium objects, inspired by SeleniumFactory interface 
from https://github.com/infradna/selenium-client-factory.  The main objective is to be able to have an automatic interface to easily run tests under the Bamboo Sauce Ondemand plugin as well as local tests.  The factory object reads environments variables setup by the Bamboo plugin and creates a remote Sauce OnDemand session accordingly, otherwise it creates a local selenium configuration.

Simple setup:
from SeleniumFactory import *

For selenium 2 webDriver:
webDriver = SeleniumFactory().createWebDriver()

For selenium 1 RC:
browser = SeleniumFactory().create()

Current state of code:

Please note that the code is very new and still being developed.  Please look at the code and make any improvements you feel fit.

