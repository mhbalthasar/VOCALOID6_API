import sys
import os
sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0],".."))
import v6loader
from ctypes import *

#功能：轨道操作器
#作用：调度管理工程的一切进展
#描述：一个被更上层操作函数调用的函数。
class VIS_Track:
    def __init__(self,trackPtr):
        self.vocaloid_dir=v6loader.get_vocaloid_dir()
        self.api=v6loader.load_library(self.vocaloid_dir,"vsm.dll")
        self.cPointer=trackPtr
        self.__setup_Track_Type()
        pass

    def __del__(self):
        v6loader.free_library(self.api)
        pass
    
    def __setup_Track_Type(self):
        self.IsAudioTrack=False
        self.IsDSETrack=False
        self.IsAITrack=False
        if self.cPointer==0:
            return
        slot=self.api.VIS_VSM_WIVSMTrack_type
        slot.argtypes = [c_void_p]
        slot.restype = c_int
        ret=slot(self.cPointer)
        self.TrackType=ret
        self.IsDSETrack=True if ret==0 else False
        self.IsAudioTrack=True if ret==1 else False
        self.IsAITrack=True if ret==2 else False

    #功能：返回句柄
    def GetPointer(self):
        return self.cPointer

    #功能：获取轨道类型
    #返回值：int, 值：0:DSETrack, 1.WAVAudio, 2:DNN/AITrack
    def Get_Type(self):
        return self.TrackType

    #功能：获取名称
    #输入参数：PartID
    #返回值：Part句柄
    def Get_Name(self):
        slot=self.api.VIS_VSM_WIVSMTrack_name
        slot.argtypes = [c_void_p]
        slot.restype = c_wchar_p
        return slot(self.cPointer)

    #功能：获取Part列表
    #返回值：数组，元素为Part句柄
    def Get_Parts(self):
        ret=[]
        num=self.__get_Part_Count()
        for i in range(0,num):
            ret.append(self.__get_Part_ByIndex(i))
        return ret

    #功能：获取Part
    #输入参数：PartID
    #返回值：Part句柄
    def Get_Part(self,TrackIndex):
        ret=[]
        num=self.__get_Part_Count()
        if TrackIndex<0 or TrackIndex>=num:
            return 0
        return self.__get_Part_ByIndex(TrackIndex)

    #功能：判断Part是否在序列内
    #输入值：Part句柄
    #返回值：BOOL
    def IsPartInTrack(self,ptrPart):
        slot=self.api.VIS_VSM_WIVSMMidiTrack_hasPart
        slot.argtypes = [c_void_p,c_void_p]
        slot.restype = c_bool
        return slot(self.cPointer,ptrPart)

    def __get_Part_Count(self):
        slot=self.api.VIS_VSM_WIVSMTrack_numPart
        slot.argtypes = [c_void_p]
        slot.restype = c_int
        return slot(self.cPointer)

    def __get_Part_ByIndex(self,Index):
        if self.IsAudioTrack:
            slot=self.api.VIS_VSM_WIVSMAudioTrack_part
        else:
            slot=self.api.VIS_VSM_WIVSMMidiTrack_part
        slot.argtypes = [c_void_p,c_int]
        slot.restype = c_void_p
        return slot(self.cPointer,Index)
