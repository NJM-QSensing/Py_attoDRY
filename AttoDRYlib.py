# This is a Python script for direct control of the AttoDRY2200 cryostat.
# It depends on the .dll files provided by Attocube (attoDRYLib64bit.dll) which
# has to be referred to in the dll_directory variable. Not all functions
# are implemented in the given code, since control is still maintained with
# the attoDRY labview interface. All additional function names are found in the dll_list.txt
# file. 
# You need to install the 2016 labview runtime engine. Additinally, the 
# script will only work with a 64 bit python version. 
#
# AttoDRY2100.py and PyAttoDRY.py are written by 
# Christoph Murer
# Magnetism and interface Physics, ETH Zurich
# christoph.murer@mat.ethz.ch or chmurer@gmail.com
# script started on 04-Sep-2020
# inspired by the ANC350 scrips written by Rob Heath and Brian Schaefer (https://github.com/Laukei/pyanc350)

# This code has been edited by Nathan McLaughlin for 64-bit versions of the DLL and python interpreter

# define the path to the AttoDRY DLL:
dll_path = 'C:\\Users\\nmclaughlin7\\Documents\\attoDRY_DLL\\DLL\\attoDRYLib64bit.dll'

import ctypes
import os

# error code (EC) as described by 
EC_Ok = 0                      # No error
EC_Error = -1                  # Unknown / other error
# all other error codes are implemented in checkError directly...

#checks the errors returned from the dll
def checkError(code,func,args):
    if code == EC_Ok:
        return
    elif code == 1:
    	raise Exception('Error 1: High liquid helium reservoir temperature. Action: Wait for it to cool.')
    elif code == 2:
    	raise Exception('Error 2: High pressure. Action: Wait for it to drop.')
    elif code == 3:
    	raise Exception('Error 3: The temperature monitor has not initialised properly. Action: Turn the AttoDRY off and on.')
    elif code == 4:
    	raise Exception('Error 4: There is a fault with channel A on the temperature Monitor. Action: Turn the attoDRY off and on. If this error occurs repeatedly, contact attocube.')
    elif code == 5:
    	raise Exception('Error 5: There is a fault with channel B on the temperature Monitor. Action: Turn the attoDRY off and on. If this error occurs repeatedly, contact attocube.')
    elif code == 6:
    	raise Exception('Error 6: There is a fault with channel C on the temperature Monitor. Action: Turn the attoDRY off and on. If this error occurs repeatedly, contact attocube.')
    elif code == 7:
    	raise Exception('Error 7: There is a fault with channel D on the temperature Monitor. Action: Turn the attoDRY off and on. If this error occurs repeatedly, contact attocube.')
    elif code == 8:
    	raise Exception('Error 8: The temperature monitor has not responded within a ceratin amount of time. Action: Lower the error. If the error occurs again, try restarting the attoDRY. If this occurs again, contact attocube.')
    elif code == 9:
    	raise Exception('Error 9: Excessive pump link voltage. Action: Turn off the attoDRY, switch the pump on and off again. Turn the attoDRY on. If this occurs again, contact attocube.')
    elif code == 10:
    	raise Exception('Error 10: Excessive pump motor current. Action: Turn off the attoDRY, switch the pump on and off again. Turn the attoDRY on. If this occurs again, contact attocube.')
    elif code == 11:
    	raise Exception('Error 11: Excessive pump controller temperature. Action: Turn off the attoDRY, switch the pump on and off again. Turn the attoDRY on. If this occurs again, contact attocube. Make sure the pump is in a well-ventilated area.')
    elif code == 12:
    	raise Exception('Error 12: Pump controller temp sensor failure. Action: Turn off the attoDRY, switch the pump on and off again. Turn the attoDRY on. If this occurs again, contact attocube.')
    elif code == 13:
    	raise Exception('Error 13: Pump power stage failure. Action: Turn off the attoDRY, switch the pump on and off again. Turn the attoDRY on. If this occurs again, contact attocube.')
    elif code == 17:
    	raise Exception('Error 17: Critical pump EEPROM problem. Action: Turn off the attoDRY, switch the pump on and off again. Turn the attoDRY on. If this occurs again, contact attocube.')
    elif code == 19:
    	raise Exception('Error 19: Pump parameter set upload required. Action: Turn off the attoDRY, switch the pump on and off again. Turn the attoDRY on. If this occurs again, contact attocube.')
    elif code == 20:
    	raise Exception('Error 20: Pump self-test fault (invalid pump software code). Action: Turn off the attoDRY, switch the pump on and off again. Turn the attoDRY on. If this occurs again, contact attocube.')
    elif code == 21:
    	raise Exception('Error 21: Pump serial enable input went inactive whilst operating with a serial start command. Action: Turn off the attoDRY, switch the pump on and off again. Turn the attoDRY on. If this occurs again, contact attocube. Ensure the cable between the pump and the attoDRY is plugged in properly.')
    elif code == 22:
    	raise Exception('Error 22: Pump output frequency dropped below threshold for too long. Action: Turn off the attoDRY, switch the pump on and off again. Turn the attoDRY on. If this occurs again, contact attocube. This error may occur if the pressure suddenly increases in the pumping line.')
    elif code == 23:
    	raise Exception('Error 23: Pump output frequency did not reach threshold in allowable time. Action: Turn off the attoDRY, switch the pump on and off again. Turn the attoDRY on. If this occurs again, contact attocube.')
    elif code == 24:
    	raise Exception('Error 24: Error processing pump response. Action: Try to send the command again.')
    elif code == 29:
    	raise Exception('Error 29: Error with pump inlet pressure gauge. Action: Check the light on top of the pressure gauge. If it is off, ensure everything is plugged correctly. If it is red or green, try switching the power on and off. Contact attocube if the light stays off or red.')
    elif code == 30:
    	raise Exception('Error 30: Error with the pump outlet pressure gauge. Action: Check the light on top of the pressure gauge. If it is off, ensure everything is plugged in correctly. If it is red or green, try switching the power on and off. Contact attocube if the light stays off or red.')
    elif code == 31:
    	raise Exception('Error 31: Error with the helium dump pressure gauge. Action: Check the light on top of the pressure gauge. If it is off, ensure everything is plugged in correctly. If it is red or green, try switching the power on and off. Contact attocube if the light stays off or red.')
    elif code == 32:
    	raise Exception('Error 32: Error with compressor. Action: Check the compressor display for more information.')
    elif code == 33:
    	raise Exception('Error 33: VTI temperature is too high; everything is stopped to prefent damage. Action: Wait for the temperature to drop. If this occurs repeatedly, contact attocube.')
    elif code == 34:
    	raise Exception('Error 34: The temperature monitor has given invalid temperatures for too long. Unable to control the temperature. This can occur when changing temperature monitor settings e.g. sensor exictation ranges. Action: Check all temperature sensor cables are connected and try again. If the error occurs again, restart the attoDRY. If you changed a setting on the temperature monitor, wait a few seconds and start controlling again.')
    elif code == 35:
    	raise Exception('Error 35: An operation has been requested that requires the magnet controller and there is not one connected. Action: Ensure magnet controller is connected, switched on, and communication is configured. Restart attoDRY.')
    elif code == 36:
    	raise Exception('Error 36: An operation with the magnet controller requires it to be in remote mode when it is not. Action: The magnet controller must be in remote mode. Ensure the magnet controller is not in local mode.')
    elif code == 37:
    	raise Exception('Error 37: Magnet quenched. Action: Let magnet cool. Try again.')
    elif code == 38:
    	raise Exception('Error 38: Magnet controller power module failure. Action: Contact attocube.')
    elif code == 39:
    	raise Exception('Error 39: Error with chip 1 on motor driver 1. Action: Restart attoDRY. Contact attocube if problem persists.')
    elif code == 40:
    	raise Exception('Error 40: Error with chip 1 on motor driver 2. Action: Restart attoDRY. Contact attocube if problem persists.')
    elif code == 41:
    	raise Exception('Error 41: Error with chip 1 on motor driver 3. Action: Restart attoDRY. Contact attocube if problem persists.')
    elif code == 42:
    	raise Exception('Error 42: Error with chip 1 on motor driver 4. Action: Restart attoDRY. Contact attocube if problem persists.')
    elif code <= EC_Error:             
        raise Exception('Error: unspecific in'+str(func.__name__)+'with parameters:'+str(args))
    else:                    
        raise Exception('Error: unknown Error code: '+str(code))
    return code


# load attoDRYLib...
attoDRYLib = ctypes.WinDLL(dll_path)
#############################################################################################################
##### aliases for the DLL functions (only selected ones; we want to change field and temperature only):
#############################################################################################################

##### communication
getActionMessage = getattr(attoDRYLib,'GetActionMessage')
begin = getattr(attoDRYLib,'Begin')
Cancel = getattr(attoDRYLib,'Cancel')
Confirm = getattr(attoDRYLib,'Confirm')
Connect = getattr(attoDRYLib,'Connect')
Main = getattr(attoDRYLib,'Main')
Disconnect = getattr(attoDRYLib,'Disconnect')
end = getattr(attoDRYLib,'End')
getAttodryErrorMessage = getattr(attoDRYLib,'GetAttodryErrorMessage')
getAttodryErrorStatus = getattr(attoDRYLib,'GetAttodryErrorStatus')
goToBaseTemperature = getattr(attoDRYLib,'GoToBaseTemperature')
lowerError = getattr(attoDRYLib,'LowerError')
LVDLLStatus = getattr(attoDRYLib,'LVDLLStatus')
startLogging = getattr(attoDRYLib,'StartLogging')
startSampleExchange = getattr(attoDRYLib,'StartSampleExchange')
stopLogging = getattr(attoDRYLib,'StopLogging')
sweepFieldToZero = getattr(attoDRYLib,'SweepFieldToZero')
downloadSampleTemperatureSensorCalibrationCurve = getattr(attoDRYLib,'DownloadSampleTemperatureSensorCalibrationCurve')
downloadTemperatureSensorCalibrationCurve = getattr(attoDRYLib,'DownloadTemperatureSensorCalibrationCurve')
uploadSampleTemperatureCalibrationCurve = getattr(attoDRYLib,'UploadSampleTemperatureCalibrationCurve')
uploadTemperatureCalibrationCurve = getattr(attoDRYLib,'UploadTemperatureCalibrationCurve')

##### asking questions
isControllingField = getattr(attoDRYLib,'IsControllingField')
isControllingTemperature = getattr(attoDRYLib,'IsControllingTemperature')
isDeviceConnected = getattr(attoDRYLib,'IsDeviceConnected')
isDeviceInitialised = getattr(attoDRYLib,'IsDeviceInitialised')
isGoingToBaseTemperature = getattr(attoDRYLib,'IsGoingToBaseTemperature')
isExchangeHeaterOn = getattr(attoDRYLib,'IsExchangeHeaterOn')
isPersistentModeSet = getattr(attoDRYLib,'IsPersistentModeSet')
isPumping = getattr(attoDRYLib,'IsPumping')
isSampleExchangeInProgress = getattr(attoDRYLib,'IsSampleExchangeInProgress')
isSampleHeaterOn = getattr(attoDRYLib,'IsSampleHeaterOn')
isSampleReadyToExchange = getattr(attoDRYLib,'IsSampleReadyToExchange')
isSystemRunning = getattr(attoDRYLib,'IsSystemRunning')
isPumping = getattr(attoDRYLib,'IsPumping')
isZeroingField = getattr(attoDRYLib,'IsZeroingField')

##### queries
queryReservoirTsetColdSample = getattr(attoDRYLib,'QueryReservoirTsetColdSample') 
queryReservoirTsetWarmMagnet = getattr(attoDRYLib,'QueryReservoirTsetWarmMagnet')
queryReservoirTsetWarmSample = getattr(attoDRYLib,'QueryReservoirTsetWarmSample')
querySampleHeaterMaximumPower = getattr(attoDRYLib,'QuerySampleHeaterMaximumPower')
querySampleHeaterResistance = getattr(attoDRYLib,'QuerySampleHeaterResistance')
querySampleHeaterWireResistance = getattr(attoDRYLib,'QuerySampleHeaterWireResistance')

##### toggle commands
toggleCryostatInValve = getattr(attoDRYLib,'ToggleCryostatInValve')
toggleCryostatOutValve = getattr(attoDRYLib,'ToggleCryostatOutValve')
toggleDumpInValve = getattr(attoDRYLib,'ToggleDumpInValve')
toggleDumpOutValve = getattr(attoDRYLib,'ToggleDumpOutValve')
toggleExchangeHeaterControl = getattr(attoDRYLib,'ToggleExchangeHeaterControl')
toggleFullTemperatureControl = getattr(attoDRYLib,'ToggleFullTemperatureControl')
toggleHeliumValve = getattr(attoDRYLib,'ToggleHeliumValve')
toggleInnerVolumeValve = getattr(attoDRYLib,'ToggleInnerVolumeValve')
toggleOuterVolumeValve = getattr(attoDRYLib,'ToggleOuterVolumeValve')
toggleMagneticFieldControl = getattr(attoDRYLib,'ToggleMagneticFieldControl')
togglePersistentMode = getattr(attoDRYLib,'TogglePersistentMode')
togglePump = getattr(attoDRYLib,'TogglePump')
togglePumpValve = getattr(attoDRYLib,'TogglePumpValve')
toggleSampleTemperatureControl = getattr(attoDRYLib,'ToggleSampleTemperatureControl') 
toggleStartUpShutdown = getattr(attoDRYLib,'ToggleStartUpShutdown') 

##### get values
getCryostatInPressure = getattr(attoDRYLib,'GetCryostatInPressure')
getCryostatInValve = getattr(attoDRYLib,'GetCryostatInValve')
getCryostatOutPressure = getattr(attoDRYLib,'GetCryostatOutPressure')
getCryostatOutValve = getattr(attoDRYLib,'GetCryostatOutValve')
getDumpInValve = getattr(attoDRYLib,'GetDumpInValve')
getDumpOutValve = getattr(attoDRYLib,'GetDumpOutValve')
getDumpPressure = getattr(attoDRYLib,'GetDumpPressure')
getHeliumValve = getattr(attoDRYLib,'GetHeliumValve')
getInnerVolumeValve = getattr(attoDRYLib,'GetInnerVolumeValve')
getOuterVolumeValve = getattr(attoDRYLib,'GetOuterVolumeValve')
getReservoirHeaterPower = getattr(attoDRYLib,'GetReservoirHeaterPower')
getReservoirTemperature = getattr(attoDRYLib,'GetReservoirTemperature')
getReservoirTsetColdSample = getattr(attoDRYLib,'GetReservoirTsetColdSample')
getReservoirTsetWarmMagnet = getattr(attoDRYLib,'GetReservoirTsetWarmMagnet')
getReservoirTsetWarmSample = getattr(attoDRYLib,'GetReservoirTsetWarmSample')
getPressure = getattr(attoDRYLib,'GetPressure')
get40KStageTemperature = getattr(attoDRYLib,'Get40KStageTemperature')
get4KStageTemperature = getattr(attoDRYLib,'Get4KStageTemperature')
getDerivativeGain = getattr(attoDRYLib,'GetDerivativeGain')
getIntegralGain = getattr(attoDRYLib,'GetIntegralGain')
getMagneticField = getattr(attoDRYLib,'GetMagneticField')
getMagneticFieldSetPoint = getattr(attoDRYLib,'GetMagneticFieldSetPoint')
getProportionalGain = getattr(attoDRYLib,'GetProportionalGain')
getSampleHeaterMaximumPower = getattr(attoDRYLib,'GetSampleHeaterMaximumPower')
getSampleHeaterPower = getattr(attoDRYLib,'GetSampleHeaterPower')
getSampleHeaterResistance = getattr(attoDRYLib,'GetSampleHeaterResistance')
getSampleHeaterWireResistance = getattr(attoDRYLib,'GetSampleHeaterWireResistance')
getSampleTemperature = getattr(attoDRYLib,'GetSampleTemperature')
getUserTemperature = getattr(attoDRYLib,'GetUserTemperature')
getVtiHeaterPower = getattr(attoDRYLib,'GetVtiHeaterPower')
getVtiTemperature = getattr(attoDRYLib,'GetVtiTemperature')
getPumpValve = getattr(attoDRYLib,'GetPumpValve')
getTurbopumpFrequency = getattr(attoDRYLib,'GetTurbopumpFrequency')

##### set values
setDerivativeGain = getattr(attoDRYLib,'SetDerivativeGain')
setIntegralGain = getattr(attoDRYLib,'SetIntegralGain')
setProportionalGain = getattr(attoDRYLib,'SetProportionalGain')
setReservoirTsetColdSample = getattr(attoDRYLib,'SetReservoirTsetColdSample')
setReservoirTsetWarmMagnet = getattr(attoDRYLib,'SetReservoirTsetWarmMagnet')
setReservoirTsetWarmSample = getattr(attoDRYLib,'SetReservoirTsetWarmSample')
setSampleHeaterMaximumPower = getattr(attoDRYLib,'SetSampleHeaterMaximumPower')
setSampleHeaterPower = getattr(attoDRYLib,'SetSampleHeaterPower')
setSampleHeaterResistance = getattr(attoDRYLib,'SetSampleHeaterResistance')
setSampleHeaterWireResistance = getattr(attoDRYLib,'SetSampleHeaterWireResistance')
setUserMagneticField = getattr(attoDRYLib,'SetUserMagneticField')
setUserTemperature = getattr(attoDRYLib,'SetUserTemperature')
setVTIHeaterPower = getattr(attoDRYLib,'SetVTIHeaterPower')



#############################################################################################################
##### error checking and handling...
#############################################################################################################

##### communication
getActionMessage.errcheck = checkError
begin.errcheck = checkError
Cancel.errcheck = checkError
Confirm.errcheck = checkError
Connect.errcheck = checkError
Main.errcheck = checkError
Disconnect.errcheck = checkError
end.errcheck = checkError
getAttodryErrorMessage.errcheck = checkError
getAttodryErrorStatus.errcheck = checkError
goToBaseTemperature.errcheck = checkError
lowerError.errcheck = checkError
startLogging.errcheck = checkError
startSampleExchange.errcheck = checkError
stopLogging.errcheck = checkError
sweepFieldToZero.errcheck = checkError
downloadSampleTemperatureSensorCalibrationCurve.errcheck = checkError
downloadTemperatureSensorCalibrationCurve.errcheck = checkError
uploadSampleTemperatureCalibrationCurve.errcheck = checkError
uploadTemperatureCalibrationCurve.errcheck = checkError
LVDLLStatus.errcheck = checkError

##### asking questions
isControllingField.errcheck = checkError
isControllingTemperature.errcheck = checkError
isDeviceConnected.errcheck = checkError
isDeviceInitialised.errcheck = checkError
isGoingToBaseTemperature.errcheck = checkError
isExchangeHeaterOn.errcheck = checkError
isPersistentModeSet.errcheck = checkError
isPumping.errcheck = checkError
isSampleExchangeInProgress.errcheck = checkError
isSampleHeaterOn.errcheck = checkError
isSampleReadyToExchange.errcheck = checkError
isSystemRunning.errcheck = checkError
isPumping.errcheck = checkError
isZeroingField.errcheck = checkError

##### queries
queryReservoirTsetColdSample.errcheck = checkError 
queryReservoirTsetWarmMagnet.errcheck = checkError
queryReservoirTsetWarmSample.errcheck = checkError
querySampleHeaterMaximumPower.errcheck = checkError
querySampleHeaterResistance.errcheck = checkError
querySampleHeaterWireResistance.errcheck = checkError

##### toggle commands
toggleCryostatInValve.errcheck = checkError
toggleCryostatOutValve.errcheck = checkError
toggleDumpInValve.errcheck = checkError
toggleDumpOutValve.errcheck = checkError
toggleExchangeHeaterControl.errcheck = checkError
toggleFullTemperatureControl.errcheck = checkError
toggleHeliumValve.errcheck = checkError
toggleInnerVolumeValve.errcheck = checkError
toggleOuterVolumeValve.errcheck = checkError
toggleMagneticFieldControl.errcheck = checkError
togglePersistentMode.errcheck = checkError
togglePump.errcheck = checkError
togglePumpValve.errcheck = checkError
toggleSampleTemperatureControl.errcheck = checkError
toggleStartUpShutdown.errcheck = checkError

##### get values
getCryostatInPressure.errcheck = checkError
getCryostatInValve.errcheck = checkError
getCryostatOutPressure.errcheck = checkError
getCryostatOutValve.errcheck = checkError
getDumpInValve.errcheck = checkError
getDumpOutValve.errcheck = checkError
getDumpPressure.errcheck = checkError
getHeliumValve.errcheck = checkError
getInnerVolumeValve.errcheck = checkError
getOuterVolumeValve.errcheck = checkError
getReservoirHeaterPower.errcheck = checkError
getReservoirTemperature.errcheck = checkError
getReservoirTsetColdSample.errcheck = checkError
getReservoirTsetWarmMagnet.errcheck = checkError
getReservoirTsetWarmSample.errcheck = checkError
getPressure.errcheck = checkError
get40KStageTemperature.errcheck = checkError
get4KStageTemperature.errcheck = checkError
getDerivativeGain.errcheck = checkError
getIntegralGain.errcheck = checkError
getMagneticField.errcheck = checkError
getMagneticFieldSetPoint.errcheck = checkError
getProportionalGain.errcheck = checkError
getSampleHeaterMaximumPower.errcheck = checkError
getSampleHeaterPower.errcheck = checkError
getSampleHeaterResistance.errcheck = checkError
getSampleHeaterWireResistance.errcheck = checkError
getSampleTemperature.errcheck = checkError
getUserTemperature.errcheck = checkError
getVtiHeaterPower.errcheck = checkError
getVtiTemperature.errcheck = checkError
getPumpValve.errcheck = checkError
getTurbopumpFrequency.errcheck = checkError

##### set values
setDerivativeGain.errcheck = checkError
setIntegralGain.errcheck = checkError
setProportionalGain.errcheck = checkError
setReservoirTsetColdSample.errcheck = checkError
setReservoirTsetWarmMagnet.errcheck = checkError
setReservoirTsetWarmSample.errcheck = checkError
setSampleHeaterMaximumPower.errcheck = checkError
setSampleHeaterPower.errcheck = checkError
setSampleHeaterResistance.errcheck = checkError
setSampleHeaterWireResistance.errcheck = checkError
setUserMagneticField.errcheck = checkError
setUserTemperature.errcheck = checkError
setVTIHeaterPower.errcheck = checkError