import sys
import os
sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0],".."))
import v6loader
from ctypes import *

#功能：解析VibratoBank颤音数据结构体
class VIS_VibratoBank:
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
    def VibratoBankToObject(self,pVibratoBank):
        ret={}
        ret["Name"]=self.Get_Name(pVibratoBank)
        ret["InstallPath"]=self.Get_InstallPath(pVibratoBank)
        ret["VibratoTemplates"]=self.GetVibratoTemplates(pVibratoBank)
        return ret

    #功能：获取音源名
    #返回值：String
    def Get_Name(self,pVibratoBank):
        slot=self.api.VDM_VibratoBank_name
        slot.argtypes = [c_void_p]
        slot.restype = c_wchar_p
        return slot(pVibratoBank)

    #功能：获取声库安装路径
    #返回值：String,拼接声库指向ddb文件，AI声库指向模型所在文件夹
    def Get_InstallPath(self,pVibratoBank):
        slot=self.api.VDM_VibratoBank_path
        slot.argtypes = [c_void_p]
        slot.restype = c_wchar_p
        return slot(pVibratoBank)

    def __get_VibratoTemplate_Count(self,pVibratoBank):
        slot=self.api.VDM_VibratoBank_numVibratoTemplates
        slot.argtypes = [c_void_p]
        slot.restype = c_ulong
        return slot(pVibratoBank)

    def __get_VibratoTemplate_ByIndex(self,pVibratoBank,vP_Index):
        slot=self.api.VDM_VibratoBank_vibratoTemplateByIndex
        slot.argtypes = [c_void_p,c_int]
        slot.restype = c_void_p
        return slot(pVibratoBank,vP_Index)

    def __get_VibratoTemplate_Type(self,pVibratoTemplate):
        slot=self.api.VDM_VibratoTemplate_type
        slot.argtypes = [c_void_p]
        slot.restype = c_ulong
        return slot(pVibratoTemplate)

    def __get_VibratoTemplate_Name(self,pVibratoTemplate):
        slot=self.api.VDM_VibratoTemplate_caption
        slot.argtypes = [c_void_p]
        slot.restype = c_wchar_p
        return slot(pVibratoTemplate)
 
    def __vibratoTemplateToObject(self,pVibratoTemplate):
        ret={}
        ret["Handle"]=pVibratoTemplate
        ret["Type"]=self.__get_VibratoTemplate_Type(pVibratoTemplate)
        ret["Name"]=self.__get_VibratoTemplate_Name(pVibratoTemplate)
        return ret

    #功能：根据类型获取颤音模板
    #输入值：颤音库句柄，颤音类型(int):
    #None=0,Normal1,Normal2,Normal3,Normal4,
    #       Extreme1,Extreme2,Extreme3,Extreme4,
    #       Fast1,Fast2,Fast3,Fast4,
    #       Slight1,Slight2,Slight3,Slight4
    #返回值：返回颤音模板句柄
    def GetVibratoTemplateByType(self,pVibratoBank,vbType):
        slot=self.api.VDM_VibratoBank_vibratoTemplateByType
        slot.argtypes = [c_void_p,c_int]
        slot.restype = c_void_p
        return self.__vibratoTemplateToObject(slot(pVibratoBank,vb_Type))

    #功能：获取颤音模板列表
    #返回值：数组，返回颤音模板句柄数组
    def GetVibratoTemplates(self,pVibratoBank):
        ret=[]
        for i in range(0,self.__get_VibratoTemplate_Count(pVibratoBank)):
            pPtr=self.__get_VibratoTemplate_ByIndex(pVibratoBank,i)
            ret.append(self.__vibratoTemplateToObject(pPtr))
        return ret
