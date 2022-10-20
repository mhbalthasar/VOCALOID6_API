import sys
import os
sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0],".."))
import v6loader
from ctypes import *

class VIS_DSE:
    def __init__(self):
        self.vocaloid_dir=v6loader.get_vocaloid_dir()
        self.api=v6loader.load_library(self.vocaloid_dir,"dse.dll")
        self.cPointer=0
        pass

    def __del__(self):
        v6loader.free_library(self.api)
        pass
    
    def GetPointer(self):
        return self.cPointer

    def Create(self):
        slot = self.api.VIS_DSE_CreateManager
        slot.argtypes = []
        slot.restype = c_void_p
        self.cPointer=slot()
        return self.cPointer

    def Destroy(self):
        if self.cPointer==0:
            return
        slot = self.api.VIS_DSE_DestroyManager
        slot.argtypes = [c_void_p]
        slot.restype = None
        slot(self.cPointer)

    def Has(self):
        slot=self.api.VIS_DSE_HasManager
        slot.argtypes = [c_void_p]
        slot.restype = c_char
        ret=slot(self.cPointer)
        return False if ret==0 else True

    def Initialize(self,ptrVDM):
        slot=self.api.VIS_DSE_InitializeManager
        slot.argtypes = [c_void_p,c_void_p]
        slot.restype = c_int
        ret=slot(self.cPointer,ptrVDM)
        #Error==-1
        return False if ret==-1 else True

    def Terminate(self):
        slot=self.api.VIS_DSE_TerminateManager
        slot.argtypes = [c_void_p]
        slot.restype = c_int
        ret=slot(self.cPointer)
        return False if ret==-1 else True

    def NumLicenses(self):
        slot=self.api.VIS_DSE_NumLicenses
        slot.argtypes = [c_void_p]
        slot.restype = c_ulong
        return slot(self.cPointer)

    def GetLicense(self,LicenseIndex):
        slot=self.api.VIS_DSE_GetLicense
        slot.argtypes = [c_void_p,c_int]
        slot.restype = c_void_p
        return self.__FillLicenseObject(slot(self.cPointer,LicenseIndex))

    def __FillLicenseObject(self,pLicense):
        ret={
                "CompID":self.__GetCompIDFromLicense(pLicense),
                "CompName":self.__GetCompNameFromLicense(pLicense),
                "CompType":self.__GetCompTypeFromLicense(pLicense)
                }
        return ret

    def __GetCompIDFromLicense(self,pLicense):
        slot=self.api.VIS_DSE_GetCompIDFromLicense
        slot.argtypes = [c_void_p]
        slot.restype = c_wchar_p
        return slot(pLicense)

    def __GetCompNameFromLicense(self,pLicense):
        slot=self.api.VIS_DSE_GetCompNameFromLicense
        slot.argtypes = [c_void_p]
        slot.restype = c_wchar_p
        return slot(pLicense)

    def __GetCompTypeFromLicense(self,pLicense):
        slot=self.api.VIS_DSE_GetCompTypeFromLicense
        slot.argtypes = [c_void_p]
        slot.restype = c_int
        return slot(pLicense)


