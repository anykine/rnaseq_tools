#!/bin/env python

import os
import json
import sys



class SiteconfigBase(object):
    """Base class for defining a installation site-specific parameters.
       JSON file provides base path for :
        1. aligner index paths
        2. software install paths

       The JSON parameters are stored in a dict()
       getProperty(param) will search for the param and return it

        reference
        https://www.hackerearth.com/practice/notes/samarthbhargav/a-design-pattern-for-configuration-management-in-python/
    """

    def __init__(self, configFile="siteconfig.json"):
        """Load JSON file of config into a dict
           Assume the siteconfig.json is in the same
           directory as these class files
        """
        configFilePath = os.path.dirname(os.path.abspath(__file__))
        configFilePath = os.path.join(configFilePath, configFile)
        with open(configFilePath, 'r') as f:
                data = f.read()
                config = json.loads(data)
                self._config = config

        #self.indexBasePath = self._config['indexBasePath']
        #self.appBasePath = self._config['appBasePath']

    def getProperty(self, propertyName):
        """Get property values from the self._config dict"""
        if propertyName not in self._config.keys():
            return None
        return self._config[propertyName]


    @property
    def indexBasePath(self):
        return self.getProperty('indexBasePath')

    @property
    def appBasePath(self):
        return self.getProperty('appBasePath')


class Appconfig(SiteconfigBase):
    """
    This object specifies the location of executables. 
    Derived from SiteconfigBase
    appconfig.json specifies app name with is binary executable path

    appName must match whatever is in appconfig.json
    """

    def __init__(self, appName, appFileConfig="appconfig.json"):
        """
        Read in appconfig.json and set
         self.app = name of software
         self.exe = path to executable
        """
        # call base class to set site paths
        #SiteconfigBase.__init__(self, "siteconfig.json" )
        SiteconfigBase.__init__(self)

        appFileConfigPath = os.path.dirname(os.path.abspath(__file__))
        appFileConfigPath = os.path.join(appFileConfigPath, appFileConfig)
        print appFileConfigPath
        # load binary executable path
        with open(appFileConfigPath, 'r') as f:
                data = f.read()
                config = json.loads(data)
                self._config.update(config)

        if appName not in self._config.keys():
            return None
        else:
            self.exe = os.path.join(self.appBasePath, self._config[appName])
            self.app = appName
        
    #@property
    #def kallistoExe(self):
    #    return os.path.join(self.appBasePath, self.getProperty('kallisto'))

    def test(self):
        print "test siteconfig"
