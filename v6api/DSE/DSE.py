import sys
import os
sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0],".."))
import v6loader
from ctypes import *

#功能：声音合成引擎及声库解析管理器
#作用：对拼接声库(DSE)和AI声库(DNN)进行最底层的合成操作以及YAMAHA组件管理
#描述：一个被更上层库调用的函数。
class VIS_DSE:
    def __init__(self):
        self.vocaloid_dir=v6loader.get_vocaloid_dir()
        self.api=v6loader.load_library(self.vocaloid_dir,"dse.dll")
        self.cPointer=0
        pass

    def __del__(self):
        v6loader.free_library(self.api)
        pass

    #功能：返回引擎句柄
    def GetPointer(self):
        return self.cPointer

    #功能：创建对象
    def Create(self):
        slot = self.api.VIS_DSE_CreateManager
        slot.argtypes = []
        slot.restype = c_void_p
        self.cPointer=slot()
        return self.cPointer

    #功能：销毁对象
    def Destroy(self):
        if self.cPointer==0:
            return
        slot = self.api.VIS_DSE_DestroyManager
        slot.argtypes = [c_void_p]
        slot.restype = None
        slot(self.cPointer)

    #功能：判断是否可用
    #返回值：BOOL
    def Has(self):
        slot=self.api.VIS_DSE_HasManager
        slot.argtypes = [c_void_p]
        slot.restype = c_bool
        return slot(self.cPointer)

    #功能：初始化管理器
    #传入参数：VDM声库管理器句柄
    #返回值：BOOL
    def Initialize(self,ptrVDM):
        slot=self.api.VIS_DSE_InitializeManager
        slot.argtypes = [c_void_p,c_void_p]
        slot.restype = c_int
        ret=slot(self.cPointer,ptrVDM)
        return False if ret==-1 else True

    #功能：结束释放管理器
    #返回值：BOOL
    def Terminate(self):
        slot=self.api.VIS_DSE_TerminateManager
        slot.argtypes = [c_void_p]
        slot.restype = c_int
        ret=slot(self.cPointer)
        return False if ret==-1 else True

    #功能：获取许可证数量（注册组件数量）
    #返回值：组件数量（long）
    def NumLicenses(self):
        slot=self.api.VIS_DSE_NumLicenses
        slot.argtypes = [c_void_p]
        slot.restype = c_ulong
        return slot(self.cPointer)

    #功能：获取许可证（注册组件）
    #返回值：组件结构体数组，JSON
    #结构体：CompID：组件序列号
    #        CompName: 组件名
    #        CompType: 组件类型,1:编辑器/应用程序 2:声库
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


