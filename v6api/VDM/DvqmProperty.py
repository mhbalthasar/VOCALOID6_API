from re import A
import sys
import os
sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0],".."))
import v6loader
from ctypes import *

#功能：解析Dvqm预制参数内容结构体
class VIS_DvqmProperty:
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
    def DvqmPropertyToObject(self,pDvqmProp):
        ret={}
        ret["ID"]=self.Get_ID(pDvqmProp)
        ret["IsAttack"]=self.Get_IsAttack(pDvqmProp)
        ret["HasVibrato"]=self.Get_HasVibrato(pDvqmProp)
        ret["CanSpeedControl"]=self.Get_CanSpeedControl(pDvqmProp)
        ret["Keywords"]=self.Get_Keywords(pDvqmProp)
        ret["LevelNames"]=self.Get_LevelNames(pDvqmProp)
        return ret

    #功能：是否是音头
    def Get_IsAttack(self,pDvqmProp):
        slot=self.api.VDM_DvqmProperty_isAttack
        slot.argtypes = [c_void_p]
        slot.restype = c_bool
        return slot(pDvqmProp)

    #功能：是否有颤音
    def Get_HasVibrato(self,pDvqmProp):
        slot=self.api.VDM_DvqmProperty_hasVibrato
        slot.argtypes = [c_void_p]
        slot.restype = c_bool
        return slot(pDvqmProp)

    #功能：是否能调速
    def Get_CanSpeedControl(self,pDvqmProp):
        slot=self.api.VDM_DvqmProperty_canSpeedControl
        slot.argtypes = [c_void_p]
        slot.restype = c_bool
        return slot(pDvqmProp)

    #功能：获取ID
    def Get_ID(self,pDvqmProp):
        slot=self.api.VDM_DvqmProperty_id
        slot.argtypes = [c_void_p]
        slot.restype = c_int
        return slot(pDvqmProp)

    #功能：获取关键字
    #返回值：数组，元素关键字字符串
    def Get_Keywords(self,pDvqmProp):
        ret=[]
        num=self.__get_Keywords_Count(pDvqmProp)
        for i in range(0,num):
            ret.append(self.__get_Keyword_ByIndex(pDvqmProp,i))
        return ret

    #功能：获取多层名
    #返回值：数组，层次名
    def Get_LevelNames(self,pDvqmProp):
        ret=[]
        num=self.__get_LevelName_Count(pDvqmProp)
        for i in range(0,num):
            ret.append(self.__get_LevelName(pDvqmProp,i))
        return ret

    def __get_Keywords_Count(self,pDvqmProp):
        slot=self.api.VDM_DvqmProperty_numKeywords
        slot.argtypes = [c_void_p]
        slot.restype = c_ulong
        return slot(pDvqmProp)

    def __get_Keyword_ByIndex(self,pDvqmProp,vP_Index):
        slot=self.api.VDM_DvqmProperty_keyword
        slot.argtypes = [c_void_p,c_int]
        slot.restype = c_wchar_p
        return slot(pDvqmProp,vP_Index)

    def __get_LevelName_Count(self,pDvqmProp):
        slot=self.api.VDM_DvqmProperty_numLevelNames
        slot.argtypes = [c_void_p]
        slot.restype = c_ulong
        return slot(pDvqmProp)

    def __get_LevelName(self,pDvqmProp,level):
        pSize=self.__get_LevelNameWord_Count(pDvqmProp,level)
        return self.__get_LevelNameWord(pDvqmProp,level,pSize)

    def __get_LevelNameWord_Count(self,pDvqmProp,level):
        slot=self.api.VDM_DvqmProperty_levelNameWordCount
        slot.argtypes = [c_void_p,c_int]
        slot.restype = c_ulong
        return slot(pDvqmProp,level)

    def __get_LevelNameWord(self,pDvqmProp,level,size):
        sbuffer=(c_wchar*size)()
        mbuffer=cast(sbuffer,c_wchar_p)
        slot=self.api.VDM_DvqmProperty_levelName
        slot.argtypes = [c_void_p,c_int,c_wchar_p,c_int]
        slot.restype = c_bool
        ret=slot(pDvqmProp,level,mbuffer,size)
        if ret:
            return wstring_at(mbuffer)
        else:
            return ""

    #功能：获取音源名
    #返回值：String
    def Get_CompID(self,pDvqmProp):
        slot=self.api.VDM_DvqmProperty_compID
        slot.argtypes = [c_void_p]
        slot.restype = c_wchar_p
        return slot(pDvqmProp)

    #功能：获取安装路径
    #返回值：String
    def Get_InstallPath(self,pDvqmProp):
        slot=self.api.VDM_DvqmProperty_path
        slot.argtypes = [c_void_p]
        slot.restype = c_wchar_p
        return slot(pDvqmProp)

    #功能：适配语种
    #返回值：Int,0:日语，1.英语，2.韩语，3.西班牙语，4.汉语
    def Get_LangID(self,pDvqmProp):
        slot=self.api.VDM_DvqmProperty_langID
        slot.argtypes = [c_void_p]
        slot.restype = c_int
        return slot(pDvqmProp)

    #功能：参数库编号
    #返回值：Int
    def Get_ID(self,pDvqmProp):
        slot=self.api.VDM_DvqmProperty_id
        slot.argtypes = [c_void_p]
        slot.restype = c_int
        return slot(pDvqmProp)

    #功能：获取绑定声库的CompID
    #返回值：数组，元素为声库的CompID
    def Get_Binded_VoiceBank_CompIDs(self,pDvqmProp):
        ret=[]
        num=self.__get_VoiceBankIDs_Count(pDvqmProp)
        for i in range(0,num):
            ret.append(self.__get_VoiceBankIDs_ByIndex(pDvqmProp,i))
        return ret

    #功能：获取发音属性的句柄
    #返回值：数组，元素为发音属性声库句柄
    def Get_Properties(self,pDvqmProp,isAttrack=True):
        ret=[]
        num=self.__get_Properties_Count(pDvqmProp,isAttrack)
        for i in range(0,num):
            ret.append(self.__get_Property_ByIndex(pDvqmProp,i,isAttrack))
        return ret

    #功能：根据ID获取发音属性的句柄
    #返回值：发音属性声库句柄
    def Get_Property_ByID(self,pDvqmProp,ID,isAttrack=True):
        slot=self.api.VDM_DvqmProperty_dvqmPropertyByIndex
        slot.argtypes = [c_void_p,c_char,c_int]
        slot.restype = c_wchar_p
        return slot(pDvqmProp,1 if isAttrack else 0,ID)

    def __get_VoiceBankIDs_Count(self,pDvqmProp):
        slot=self.api.VDM_DvqmProperty_numVoiceBankIDs
        slot.argtypes = [c_void_p]
        slot.restype = c_ulong
        return slot(pDvqmProp)

    def __get_VoiceBankIDs_ByIndex(self,pDvqmProp,vP_Index):
        slot=self.api.VDM_DvqmProperty_voiceBankID
        slot.argtypes = [c_void_p,c_int]
        slot.restype = c_wchar_p
        return slot(pDvqmProp,vP_Index)

    def __get_Properties_Count(self,pDvqmProp,isAttrack=True):
        slot=self.api.VDM_DvqmProperty_numDvqmProperties
        slot.argtypes = [c_void_p,c_char]
        slot.restype = c_ulong
        return slot(pDvqmProp,1 if isAttrack else 0)

    def __get_Property_ByIndex(self,pDvqmProp,vP_Index,isAttrack=True):
        slot=self.api.VDM_DvqmProperty_dvqmPropertyByIndex
        slot.argtypes = [c_void_p,c_char,c_int]
        slot.restype = c_int
        return slot(pDvqmProp,1 if isAttrack else 0,vP_Index)





 
