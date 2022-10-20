import sys
import os
sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0],".."))
import v6loader
from ctypes import *

class VIS_VoiceBank:
    def __init__(self):
        self.vocaloid_dir=v6loader.get_vocaloid_dir()
        self.api=v6loader.load_library(self.vocaloid_dir,"vdm.dll")
        pass

    def __del__(self):
        v6loader.free_library(self.api)
        pass
 
    def VoiceBankToObject(self,pVoiceBank):
        ret={}
        ret["CompID"]=self.Get_CompID(pVoiceBank)
        ret["CompName"]=self.Get_CompName(pVoiceBank)
        ret["VoiceName"]=self.Get_VoiceName(pVoiceBank)
        ret["StyleID"]=self.Get_StyleID(pVoiceBank)
        ret["Drp"]=self.Get_Drp(pVoiceBank)
        ret["SingerID"]=self.Get_SingerID(pVoiceBank)
        ret["GroupName"]=self.Get_Drp(pVoiceBank)
        ret["DefaultLangID"]=self.Get_DefaultLangID(pVoiceBank)
        ret["SupportLangIDs"]=self.Get_SupportLangIDs(pVoiceBank)
        ret["TimbreIndex"]=self.Get_TimbreIndex(pVoiceBank)
        ret["InstallPath"]=self.Get_InstallPath(pVoiceBank)
        ret["VoiceParameters"]=self.GetVoiceParameters(pVoiceBank)
        return ret

    def Get_CompID(self,pVoiceBank):
        slot=self.api.VDM_VoiceBank_compID
        slot.argtypes = [c_void_p]
        slot.restype = c_wchar_p
        return slot(pVoiceBank)

    def Get_CompName(self,pVoiceBank):
        slot=self.api.VDM_VoiceBank_componentName
        slot.argtypes = [c_void_p]
        slot.restype = c_wchar_p
        return slot(pVoiceBank)

    def Get_VoiceName(self,pVoiceBank):
        slot=self.api.VDM_VoiceBank_name
        slot.argtypes = [c_void_p]
        slot.restype = c_wchar_p
        return slot(pVoiceBank)

    def Get_StyleID(self,pVoiceBank):
        slot=self.api.VDM_VoiceBank_defaultStyleID
        slot.argtypes = [c_void_p]
        slot.restype = c_wchar_p
        return slot(pVoiceBank)

    def Get_InstallPath(self,pVoiceBank):
        slot=self.api.VDM_VoiceBank_path
        slot.argtypes = [c_void_p]
        slot.restype = c_wchar_p
        return slot(pVoiceBank)

    def Get_SingerID(self,pVoiceBank):
        slot=self.api.VDM_VoiceBank_singerID
        slot.argtypes = [c_void_p]
        slot.restype = c_int
        return slot(pVoiceBank)

    def Get_DefaultLangID(self,pVoiceBank):
        slot=self.api.VDM_VoiceBank_nativeLangID
        slot.argtypes = [c_void_p]
        slot.restype = c_int
        return slot(pVoiceBank)

    def Get_TimbreIndex(self,pVoiceBank):
        slot=self.api.VDM_VoiceBank_timbreIndex
        slot.argtypes = [c_void_p]
        slot.restype = c_int
        return slot(pVoiceBank)

    def Get_Drp(self,pVoiceBank):
        slot=self.api.VDM_VoiceBank_drp
        slot.argtypes = [c_void_p]
        slot.restype = c_wchar_p
        return slot(pVoiceBank)

    def Get_GroupName(self,pVoiceBank):
        slot=self.api.VDM_VoiceBank_groupName
        slot.argtypes = [c_void_p]
        slot.restype = c_wchar_p
        return slot(pVoiceBank)

    def __get_LangIDSize(self,pVoiceBank):
        slot=self.api.VDM_VoiceBank_langIDSize
        slot.argtypes = [c_void_p]
        slot.restype = c_int
        return slot(pVoiceBank)

    def __get_LangIDByIndex(self,pVoiceBank,Index):
        slot=self.api.VDM_VoiceBank_langIDByIndex
        slot.argtypes = [c_void_p,c_int]
        slot.restype = c_int
        return slot(pVoiceBank,Index)

    def Get_SupportLangIDs(self,pVoiceBank):
        ret=[]
        for i in range(0,self.__get_LangIDSize(pVoiceBank)):
            ret.append(self.__get_LangIDByIndex(pVoiceBank,i))
        return ret

    def __get_VoiceParameter_Count(self,pVoiceBank):
        slot=self.api.VDM_VoiceBank_numParameters
        slot.argtypes = [c_void_p]
        slot.restype = c_ulong
        return slot(pVoiceBank)

    def __get_VoiceParameter_ByIndex(self,pVoiceBank,vP_Index):
        slot=self.api.VDM_VoiceBank_parameter
        slot.argtypes = [c_void_p,c_int]
        slot.restype = c_void_p
        return slot(pVoiceBank,vP_Index)

    def __get_VoiceParameter_Name(self,pParameter):
        slot=self.api.VDM_VoiceParameter_name
        slot.argtypes = [c_void_p]
        slot.restype = c_wchar_p
        return slot(pParameter)

    def __get_VoiceParameter_Value(self,pParameter):
        slot=self.api.VDM_VoiceParameter_valueInt
        slot.argtypes = [c_void_p]
        slot.restype = c_int
        return slot(pParameter)

    def GetVoiceParameters(self,pVoiceBank):
        ret=[]
        for i in range(0,self.__get_VoiceParameter_Count(pVoiceBank)):
            pPtr=self.__get_VoiceParameter_ByIndex(pVoiceBank,i)
            ret.append({self.__get_VoiceParameter_Name(pPtr):self.__get_VoiceParameter_Value(pPtr)})
        return ret

