# -*- coding: utf-8 -*-

"""
Created on 16.06.2014
CSFB_MO

Description:
        1. Master changes network mode to Auto if not attached to LTE
        2. If LTE not supported or not in coverage area, test is skipped
        2. Master video calls SIMMan_internationalNumber saved in stp.properties
        3. Checks if CSFB was performed(current network is not LTE)
"""

from Lib.RunInThreads import performTestCase


class CSFB_MO(object):
    def samplesNeededToExecute(self):
        """
        Indicating how many devices is needed for the test
        """
        return 1

    def checkPreconditions(self, dev):
        """
        Checking the preconditions for all connected devices
        :type dev: Lib.Devices.Device
        """
        return {"checkIsSIMInserted": dev.checkIsSIMInserted(),
                "checkIsVTSupported": dev.helpers.calls.checkIsVTSupported(),
                }

    def setUpMaster(self, dev):
        """
        Setting up the environment for Master device before the test
        :type dev: Lib.Devices.Device
        """
        dev.helpers.ims.toggleVoLTE(action="disable")

    def setUpSlaves(self, dev):
        """
        Setting up the environment for Slave devices before the test
        :type dev: Lib.Devices.Device
        """
        pass

    def doTest(self, devices):
        """
        :type devices: Lib.Devices.Device
        """
        devM = devices[0]
        devM.secondsWaitedForCSFB = 0
        devM.internationalNumber = devM.stpPropertiesFileManager.getProperty("SIMMan_internationalNumber")

        devM.logger.LogStep("Going to LTE")
        if not devM.helpers.network.goAndWaitForLTE():
            devM.testSkipped("LTE not supported or not in coverage area")

        devM.logger.LogStep("Video calling standard number to perform CSFB")
        devM.helpers.calls.VTcallNumber(devM.internationalNumber)
        while devM.checkIfNetworkTypeIsActive("LTE") and (devM.secondsWaitedForCSFB < 10):
            devM.sleep(1000, "Waiting for CSFB")
            devM.secondsWaitedForCSFB += 1

        if not (devM.secondsWaitedForCSFB < 10):
            devM.testFailed("CSFB not performed. Failing - DUT waited over 10s")
        else:
            devM.makeScreenCapture("CSFB_MO_VideoCall_performed_True")
            devM.testSucceeded("CSFB_MO performed properly in %s s" % devM.secondsWaitedForCSFB)

    def cleanUp(self, dev):
        """
        Cleaning up after the test
        :type dev: Lib.Devices.Device
        """
        dev.logger.LogInfo("Disconnecting ongoing video calls")
        dev.helpers.calls.disconnectCall()


performTestCase(CSFB_MO)
