import sys
import os
sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0],".."))
import v6loader
from ctypes import *

#功能：解析VibratoTemplate颤音数据结构体
class VIS_VibratoDetial:
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
    def VibratoTemplateToObject(self,VibratoTemplateHandle):
        ret={}
        ret["Name"]=self.Get_Name(VibratoTemplateHandle)
        ret["Type"]=self.Get_Type(VibratoTemplateHandle)
        ret["Data"]=self.Get_Data(VibratoTemplateHandle)
        return ret

    #功能：获取颤音名
    #返回值：String
    def Get_Name(self,VibratoTemplateHandle):
        slot=self.api.VDM_VibratoTemplate_caption
        slot.argtypes = [c_void_p]
        slot.restype = c_wchar_p
        return slot(VibratoTemplateHandle)

    #功能：获取颤音类型
    def Get_Type(self,VibratoTemplateHandle):
        slot=self.api.VDM_VibratoTemplate_type
        slot.argtypes = [c_void_p]
        slot.restype = c_ulong
        return slot(VibratoTemplateHandle)

    #功能：获取颤音控制点参数
    #返回值：对象，分为{VibratoDepth,VibratoRate}两个元素。每个元素为一个数组，数组内存在Position:Value值对
    def Get_Data(self,VibratoTemplateHandle):
        ret={}
        ret["VibratoDepth"]=[]
        for i in range(0,self.__get_VibratoDepthCount(VibratoTemplateHandle)):
            ret["VibratoDepth"].append(self.__get_VibratoEvents(self.__get_VibratoDepth_ByIndex(VibratoTemplateHandle,i)))
        ret["VibratoRate"]=[]
        for i in range(0,self.__get_VibratoRateCount(VibratoTemplateHandle)):
            ret["VibratoRate"].append(self.__get_VibratoEvents(self.__get_VibratoRate_ByIndex(VibratoTemplateHandle,i)))
        return ret

    def __get_VibratoDepthCount(self,VibratoTemplateHandle):
        slot=self.api.VDM_VibratoTemplate_numDepths
        slot.argtypes = [c_void_p]
        slot.restype = c_ulong
        return slot(VibratoTemplateHandle)

    def __get_VibratoDepth_ByIndex(self,VibratoTemplateHandle,vP_Index):
        slot=self.api.VDM_VibratoTemplate_depth
        slot.argtypes = [c_void_p,c_int]
        slot.restype = c_void_p
        return slot(VibratoTemplateHandle,vP_Index)

    def __get_VibratoRateCount(self,VibratoTemplateHandle):
        slot=self.api.VDM_VibratoTemplate_numRates
        slot.argtypes = [c_void_p]
        slot.restype = c_ulong
        return slot(VibratoTemplateHandle)

    def __get_VibratoRate_ByIndex(self,VibratoTemplateHandle,vP_Index):
        slot=self.api.VDM_VibratoTemplate_rate
        slot.argtypes = [c_void_p,c_int]
        slot.restype = c_void_p
        return slot(VibratoTemplateHandle,vP_Index)

    def __get_VibratoEvent_Pos(self,VibratoEventHandle):
        slot=self.api.VDM_VibratoEvent_pos
        slot.argtypes = [c_void_p]
        slot.restype = c_double
        return slot(VibratoEventHandle)

    def __get_VibratoEvent_Value(self,VibratoEventHandle):
        slot=self.api.VDM_VibratoEvent_value
        slot.argtypes = [c_void_p]
        slot.restype = c_int
        return slot(VibratoEventHandle)

    def __get_VibratoEvents(self,pVibratoEvent):
        ret={}
        ret["Position"]=self.__get_VibratoEvent_Pos(pVibratoEvent)
        ret["Value"]=self.__get_VibratoEvent_Value(pVibratoEvent)
        return ret
