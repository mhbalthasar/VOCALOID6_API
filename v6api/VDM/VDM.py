import sys
import os
sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0],".."))
import v6loader
from ctypes import *

class VIS_VDM:
    def __init__(self):
        self.vocaloid_dir=v6loader.get_vocaloid_dir()
        self.api=v6loader.load_library(self.vocaloid_dir,"vdm.dll")
        self.cPointer=0
        pass

    def __del__(self):
        v6loader.free_library(self.api)
        pass
 
    def GetPointer(self):
        return self.cPointer

    def Create(self,expDBDirPath="",appID="VOCALOID6"):
        if expDBDirPath=="":
            expDBDirPath=os.path.join(v6loader.get_vocaloid_common_dir(),"Explib")
        ret=c_int(0)
        slot = self.api.VDM_createDatabaseManager
        slot.argtypes = [c_wchar_p,c_wchar_p,c_void_p]
        slot.restype = c_void_p
        self.cPointer = slot(c_wchar_p(appID),c_wchar_p(expDBDirPath),byref(ret))
        return ret

    def Destroy(self):
        if self.cPointer==0:
            return
        slot = self.api.VDM_DatabaseManager_destroy
        slot.argtypes = [c_void_p]
        slot.restype = None
        slot(self.cPointer)

    def Has(self):
        slot=self.api.VDM_hasDatabaseManager
        slot.argtypes = [c_void_p]
        slot.restype = c_char
        ret=slot(self.cPointer)
        return False if ret==0 else True

    def NumVoiceBanks(self,isAI=True):
        vbType=1 if isAI else 0
        slot=self.api.VDM_DatabaseManager_numVoiceBanks
        slot.argtypes = [c_void_p,c_int]
        slot.restype = c_ulong
        return slot(self.cPointer,vbType)

    def DefaultVoiceBank(self,isAI=True):
        vbType=1 if isAI else 0
        slot=self.api.VDM_DatabaseManager_defaultVoiceBank
        slot.argtypes = [c_void_p,c_int]
        slot.restype = c_void_p
        return slot(self.cPointer,LicenseIndex)

    def SetVoiceBankAsDefault(self,pVoiceBank,isAI=True):
        vbType=1 if isAI else 0
        slot=self.api.VDM_VoiceBank_setDefault
        slot.argtypes = [c_void_p,c_int]
        slot.restype = c_void_p
        ret=slot(pVoiceBank,vbType)
        return False if ret==0 else True

    def GetVoiceBankByIndex(self,VoiceBankIndex,isAI=True):
        vbType=1 if isAI else 0
        slot=self.api.VDM_DatabaseManager_voiceBankByIndex
        slot.argtypes = [c_void_p,c_int,c_int]
        slot.restype = c_void_p
        return slot(self.cPointer,VoiceBankIndex,vbType)
