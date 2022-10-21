import sys
import os
sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0],".."))
import v6loader
from ctypes import *

#功能：解析VoiceBank结构体
class VIS_VoiceBank:
    def __init__(self):
        self.vocaloid_dir=v6loader.get_vocaloid_dir()
        self.api=v6loader.load_library(self.vocaloid_dir,"vdm.dll")
        pass

    def __del__(self):
        v6loader.free_library(self.api)
        pass

    #功能:解析声库句柄到JSON
    #输入参数：声库句柄
    #返回值：JSON，字段定义见具体函数功能介绍
    def VoiceBankToObject(self,pVoiceBank):
        ret={}
        ret["CompID"]=self.Get_CompID(pVoiceBank)
        ret["CompName"]=self.Get_CompName(pVoiceBank)
        ret["VoiceName"]=self.Get_VoiceName(pVoiceBank)
        ret["StyleID"]=self.Get_StyleID(pVoiceBank)
        ret["Drp"]=self.Get_Drp(pVoiceBank)
        ret["VoiceIndex"]=self.Get_VoiceIndex(pVoiceBank)
        ret["GroupName"]=self.Get_Drp(pVoiceBank)
        ret["DefaultLangID"]=self.Get_DefaultLangID(pVoiceBank)
        ret["SupportLangIDs"]=self.Get_SupportLangIDs(pVoiceBank)
        ret["TimbreIndex"]=self.Get_TimbreIndex(pVoiceBank)
        ret["InstallPath"]=self.Get_InstallPath(pVoiceBank)
        ret["VoiceParameters"]=self.GetVoiceParameters(pVoiceBank)
        return ret

    #功能：获取声库组件序列号
    #返回值：String
    def Get_CompID(self,pVoiceBank):
        slot=self.api.VDM_VoiceBank_compID
        slot.argtypes = [c_void_p]
        slot.restype = c_wchar_p
        return slot(pVoiceBank)

    #功能：获取声库名
    #返回值：String
    def Get_CompName(self,pVoiceBank):
        slot=self.api.VDM_VoiceBank_componentName
        slot.argtypes = [c_void_p]
        slot.restype = c_wchar_p
        return slot(pVoiceBank)

    #功能：获取音源名
    #返回值：String
    def Get_VoiceName(self,pVoiceBank):
        slot=self.api.VDM_VoiceBank_name
        slot.argtypes = [c_void_p]
        slot.restype = c_wchar_p
        return slot(pVoiceBank)

    #功能：获取演唱风格
    #返回值：UUID串,String，对应演唱风格ID
    def Get_StyleID(self,pVoiceBank):
        slot=self.api.VDM_VoiceBank_defaultStyleID
        slot.argtypes = [c_void_p]
        slot.restype = c_wchar_p
        return slot(pVoiceBank)

    #功能：获取声库安装路径
    #返回值：String,拼接声库指向ddb文件，AI声库指向模型所在文件夹
    def Get_InstallPath(self,pVoiceBank):
        slot=self.api.VDM_VoiceBank_path
        slot.argtypes = [c_void_p]
        slot.restype = c_wchar_p
        return slot(pVoiceBank)

    #功能：歌手序号
    #返回值：Int,同语种下歌手的Index(这个值是默认语种的)
    def Get_VoiceIndex(self,pVoiceBank):
        slot=self.api.VDM_VoiceBank_singerID
        slot.argtypes = [c_void_p]
        slot.restype = c_int
        return slot(pVoiceBank)

    #功能：歌手语种
    #返回值：Int,0:日语，1.英语，2.韩语，3.西班牙语，4.汉语
    def Get_DefaultLangID(self,pVoiceBank):
        slot=self.api.VDM_VoiceBank_nativeLangID
        slot.argtypes = [c_void_p]
        slot.restype = c_int
        return slot(pVoiceBank)

    #功能：音色序号
    #返回值：Int
    def Get_TimbreIndex(self,pVoiceBank):
        slot=self.api.VDM_VoiceBank_timbreIndex
        slot.argtypes = [c_void_p]
        slot.restype = c_int
        return slot(pVoiceBank)

    #功能：获取声库的发布编号
    #返回值：String,与厂商、批号相关。同一个包里的声库是一样的
    def Get_Drp(self,pVoiceBank):
        slot=self.api.VDM_VoiceBank_drp
        slot.argtypes = [c_void_p]
        slot.restype = c_wchar_p
        return slot(pVoiceBank)

    #功能：获取声库的组名
    #返回值：String,例如Miku的多个音色组名都是Miku
    def Get_GroupName(self,pVoiceBank):
        slot=self.api.VDM_VoiceBank_groupName
        slot.argtypes = [c_void_p]
        slot.restype = c_wchar_p
        return slot(pVoiceBank)

    #功能：获取声库支持的语言
    #返回值：数组，每个元素的内容和默认语种返回值一样。主要是跨语种AI声库有这个。
    def Get_SupportLangIDs(self,pVoiceBank):
        ret=[]
        for i in range(0,self.__get_LangIDSize(pVoiceBank)):
            ret.append(self.__get_LangIDByIndex(pVoiceBank,i))
        return ret

    #功能：获取音源支持的初始参数，编辑器内调节的参数都是在这个基础上加减的
    #返回值：数组，每个元素以{参数名：值}方式返回键值对。已知的参数有：gen,cle,ope,bre,bri
    def GetVoiceParameters(self,pVoiceBank):
        ret=[]
        for i in range(0,self.__get_VoiceParameter_Count(pVoiceBank)):
            pPtr=self.__get_VoiceParameter_ByIndex(pVoiceBank,i)
            ret.append({self.__get_VoiceParameter_Name(pPtr):self.__get_VoiceParameter_Value(pPtr)})
        return ret

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


