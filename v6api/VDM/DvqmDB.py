import sys
import os
sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0],".."))
import v6loader
from ctypes import *

#功能：解析Dvqm预制参数数据结构体
#备注：Dvqm控制声库的Attrack（音头）和Release（音尾）的效果和唱腔
class VIS_DvqmDB:
    def __init__(self):
        self.vocaloid_dir=v6loader.get_vocaloid_dir()
        self.api=v6loader.load_library(self.vocaloid_dir,"vdm.dll")
        pass

    def __del__(self):
        v6loader.free_library(self.api)
        pass

    #功能:解析颤音句柄到JSON
    #输入参数：颤音库句柄
    #返回值：JSON，字段定义见具体函数功能介绍
    def DvqmDBToObject(self,pDvqmDB):
        ret={}
        ret["ID"]=self.Get_ID(pDvqmDB)
        ret["CompID"]=self.Get_CompID(pDvqmDB)
        ret["InstallPath"]=self.Get_InstallPath(pDvqmDB)
        ret["LangID"]=self.Get_LangID(pDvqmDB)
        ret["Binded_VoiceBank_CompIDs"]=self.Get_Binded_VoiceBank_CompIDs(pDvqmDB)
        ret["Properties"]={"Attrack":[],"Release":[]}
        ret["Properties"]["Attrack"]=self.Get_Properties(pDvqmDB,True)
        ret["Properties"]["Release"]=self.Get_Properties(pDvqmDB,False)
        return ret

    #功能：获取音源名
    #返回值：String
    def Get_CompID(self,pDvqmDB):
        slot=self.api.VDM_DvqmDB_compID
        slot.argtypes = [c_void_p]
        slot.restype = c_wchar_p
        return slot(pDvqmDB)

    #功能：获取安装路径
    #返回值：String
    def Get_InstallPath(self,pDvqmDB):
        slot=self.api.VDM_DvqmDB_path
        slot.argtypes = [c_void_p]
        slot.restype = c_wchar_p
        return slot(pDvqmDB)

    #功能：适配语种
    #返回值：Int,0:日语，1.英语，2.韩语，3.西班牙语，4.汉语
    def Get_LangID(self,pDvqmDB):
        slot=self.api.VDM_DvqmDB_langID
        slot.argtypes = [c_void_p]
        slot.restype = c_int
        return slot(pDvqmDB)

    #功能：参数库编号
    #返回值：Int
    def Get_ID(self,pDvqmDB):
        slot=self.api.VDM_DvqmDB_id
        slot.argtypes = [c_void_p]
        slot.restype = c_int
        return slot(pDvqmDB)

    #功能：获取绑定声库的CompID
    #返回值：数组，元素为声库的CompID
    def Get_Binded_VoiceBank_CompIDs(self,pDvqmDB):
        ret=[]
        num=self.__get_VoiceBankIDs_Count(pDvqmDB)
        for i in range(0,num):
            ret.append(self.__get_VoiceBankIDs_ByIndex(pDvqmDB,i))
        return ret

    #功能：获取发音属性的句柄
    #返回值：数组，元素为发音属性声库句柄
    def Get_Properties(self,pDvqmDB,isAttrack=True):
        ret=[]
        num=self.__get_Properties_Count(pDvqmDB,isAttrack)
        for i in range(0,num):
            ret.append(self.__get_Property_ByIndex(pDvqmDB,i,isAttrack))
        return ret

    #功能：根据ID获取发音属性的句柄
    #返回值：发音属性声库句柄
    def Get_Property_ByID(self,pDvqmDB,ID,isAttrack=True):
        slot=self.api.VDM_DvqmDB_dvqmPropertyByIndex
        slot.argtypes = [c_void_p,c_char,c_int]
        slot.restype = c_wchar_p
        return slot(pDvqmDB,1 if isAttrack else 0,ID)

    def __get_VoiceBankIDs_Count(self,pDvqmDB):
        slot=self.api.VDM_DvqmDB_numVoiceBankIDs
        slot.argtypes = [c_void_p]
        slot.restype = c_ulong
        return slot(pDvqmDB)

    def __get_VoiceBankIDs_ByIndex(self,pDvqmDB,vP_Index):
        slot=self.api.VDM_DvqmDB_voiceBankID
        slot.argtypes = [c_void_p,c_int]
        slot.restype = c_wchar_p
        return slot(pDvqmDB,vP_Index)

    def __get_Properties_Count(self,pDvqmDB,isAttrack=True):
        slot=self.api.VDM_DvqmDB_numDvqmProperties
        slot.argtypes = [c_void_p,c_char]
        slot.restype = c_ulong
        return slot(pDvqmDB,1 if isAttrack else 0)

    def __get_Property_ByIndex(self,pDvqmDB,vP_Index,isAttrack=True):
        slot=self.api.VDM_DvqmDB_dvqmPropertyByIndex
        slot.argtypes = [c_void_p,c_char,c_int]
        slot.restype = c_int
        return slot(pDvqmDB,1 if isAttrack else 0,vP_Index)





 
