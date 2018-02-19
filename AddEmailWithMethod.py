# -*- coding: utf-8 -*-

"""
Created on 07.02.2018
Test

Description:
        1. Test
"""
from Lib.RunInThreads import performTestCase


class Test:
    def samplesNeededToExecute(self):
        """
        Indicating how many devices is needed for the test
        """
        return 1

    def checkPreconditions(self, dev):
        """
        Checking the preconditions for all connected devices
        :type dev: Device
        """
        pass

    def setUpMaster(self, dev):
        """
        Setting up the environment for Master device before the test
        :type dev: Device
        """
        pass

    def setUpSlaves(self, dev):
        """
        Setting up the environment for Slave devices before the test
        :type dev: Device
        """
        pass
	
    def doTest(self, devices):
        """
        :type devices: Lib.Devices.Device
        """
        login = "testcase5428@gmail.com"
        password = "sarpwxm2"
		
        devM = devices[0]
        devM.helpers.account.addEmailAccount(username=login, password=password)
        
        """if devM.waitForObjectWith(text=".*Temat.*"):
            devM.testSucceeded("Pass")
        else:
		    devM.testSucceeded("Fail")"""
    def cleanUp(self, dev):
        
        """Cleaning up after the test
        :type dev: Lib.Devices.Device"""
        
        #dev.home()


performTestCase(Test)
