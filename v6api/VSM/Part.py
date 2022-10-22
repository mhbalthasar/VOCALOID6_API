import sys
import os
sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0],".."))
import v6loader
from ctypes import *

#功能：轨道操作器
#作用：调度管理工程的一切进展
#描述：一个被更上层操作函数调用的函数。
class VIS_Part:
    def __init__(self,partPtr):
        self.vocaloid_dir=v6loader.get_vocaloid_dir()
        self.api=v6loader.load_library(self.vocaloid_dir,"vsm.dll")
        self.cPointer=partPtr
        self.__setup_Part_Type()
        pass

    def __del__(self):
        v6loader.free_library(self.api)
        pass
    
    def __setup_Part_Type(self):
        self.IsAudioPart=False
        self.IsDSEPart=False
        self.IsAIPart=False
        if self.cPointer==0:
            return
        slot=self.api.VIS_VSM_WIVSMPart_type
        slot.argtypes = [c_void_p]
        slot.restype = c_int
        ret=slot(self.cPointer)
        self.PartType=ret
        self.IsDSEPart=True if ret==0 else False
        self.IsAudioPart=True if ret==1 else False
        self.IsAIPart=True if ret==2 else False

    #功能：返回句柄
    def GetPointer(self):
        return self.cPointer

    #功能：获取轨道类型
    #返回值：int, 值：0:DSETrack, 1.WAVAudio, 2:DNN/AITrack
    def Get_Type(self):
        return self.PartType

    #功能：获取名称
    def Get_Name(self):
        slot=self.api.VIS_VSM_WIVSMPart_name
        slot.argtypes = [c_void_p]
        slot.restype = c_wchar_p
        return slot(self.cPointer)


    #功能：获取posTick
    def Get_PosTick(self):
        slot=self.api.VIS_VSM_WIVSMPart_posTick
        slot.argtypes = [c_void_p]
        slot.restype = c_int
        return slot(self.cPointer)

    #功能：设置名称
    #输入参数：要设置的名称
    #返回值：Part句柄
    def Set_Name(self,name):
        slot=self.api.VIS_VSM_WIVSMPart_setName
        slot.argtypes = [c_void_p,c_wchar_p]
        slot.restype = c_bool
        return slot(self.cPointer,c_wchar_p(name))

    #功能：渲染模块
    #输入参数：输出路径
    #返回值：VSMResult
    def Render(self,filepath):
        if self.IsAudioPart:
            return -1
        slot=self.api.VIS_VSM_WIVSMMidiPart_render
        slot.argtypes = [c_void_p,c_wchar_p]
        slot.restype = c_int
        return slot(self.cPointer,c_wchar_p(filepath))

    def LastError(self):
        slot=self.api.VIS_VSM_WIVSMPart_lastError
        slot.argtypes = []
        slot.restype = c_int
        return slot()

    def __get_parent_sequence(self):
        slot=self.api.VIS_VSM_WIVSMPart_sequence
        slot.argtypes = [c_void_p]
        slot.restype = c_void_p
        return slot(self.cPointer)