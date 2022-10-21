import sys
import os
sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0],".."))
import v6loader
from ctypes import *

#功能：声库管理与音源解析
#作用：管理声库及其衍生的音源参数,包括颤音、XSY等信息
#描述：一个被更上层库调用的函数。
class VIS_VDM:
    def __init__(self):
        self.vocaloid_dir=v6loader.get_vocaloid_dir()
        self.api=v6loader.load_library(self.vocaloid_dir,"vdm.dll")
        self.cPointer=0
        pass

    def __del__(self):
        v6loader.free_library(self.api)
        pass

    #功能：返回引擎句柄
    def GetPointer(self):
        return self.cPointer

    #功能：创建对象
    #输入参数：expDBDirPath 用于解析颤音、力度、演唱风格等信息的库路径，可留空自动填写。
    #          appID 声库宿主唯一标识符，默认VOCALOID6即可
    #返回值：VDM状态：
    #        0：无错误,1:内存溢出,2：模块错误
    #        3.符号未发现 4.appID无效 5.用户设置初始化失败 6.系统设置初始化失败
    #        7.数据库键未找到 8.无效的组件 9.组件已卸载 10.声库未找到
    #        11.expDB未找到 12.颤音类型错误 13.激活信息未找到 14.Dvqm未找到
    #        15.语言编码错误
    def Create(self,expDBDirPath="",appID="VOCALOID6"):
        if expDBDirPath=="":
            expDBDirPath=os.path.join(v6loader.get_vocaloid_common_dir(),"Explib")
        ret=c_int(0)
        slot = self.api.VDM_createDatabaseManager
        slot.argtypes = [c_wchar_p,c_wchar_p,c_void_p]
        slot.restype = c_void_p
        self.cPointer = slot(c_wchar_p(appID),c_wchar_p(expDBDirPath),byref(ret))
        return ret

    #功能：销毁对象
    def Destroy(self):
        if self.cPointer==0:
            return
        slot = self.api.VDM_DatabaseManager_destroy
        slot.argtypes = [c_void_p]
        slot.restype = None
        slot(self.cPointer)

    #功能：判断是否可用
    #返回值：BOOL
    def Has(self):
        slot=self.api.VDM_hasDatabaseManager
        slot.argtypes = [c_void_p]
        slot.restype = c_int
        ret=slot(self.cPointer)
        return False if ret==0 else True

    #功能：获取默认声库句柄
    #输入参数：是否是AI声库（BOOL）
    #返回值：声库句柄
    def DefaultVoiceBank(self,isAI=True):
        vbType=1 if isAI else 0
        slot=self.api.VDM_DatabaseManager_defaultVoiceBank
        slot.argtypes = [c_void_p]
        slot.restype = c_void_p
        return slot(self.cPointer)

    #功能：设置为默认声库
    #输入参数：声库句柄，是否是AI声库（BOOL）
    #返回值：BOOL
    def SetVoiceBankAsDefault(self,pVoiceBank,isAI=True):
        vbType=1 if isAI else 0
        slot=self.api.VDM_VoiceBank_setDefault
        slot.argtypes = [c_void_p,c_int]
        slot.restype = c_int
        ret=slot(pVoiceBank,vbType)
        return False if ret==0 else True

    #功能：获取声库句柄
    #输入参数：是否是AI声库（BOOL）
    #返回值：数组，元素为声库句柄
    def GetVoiceBanks(self,isAI=True):
        ret=[]
        num=self.__get_VoiceBanks_Count(isAI)
        for i in range(0,num):
            ret.append(self.__get_VoiceBank_ByIndex(i,isAI))
        return ret

    #功能：根据声库组件序列号获取声库句柄
    #输入参数：声库组件序列号，是否是AI声库（BOOL）
    #返回值：声库句柄
    def GetVoiceBankByCompID(self,VoiceBankCompID,isAI=True):
        vbType=1 if isAI else 0
        slot=self.api.VDM_DatabaseManager_voiceBankByCompID
        slot.argtypes = [c_void_p,c_wchar_p,c_int]
        slot.restype = c_void_p
        return slot(self.cPointer,c_wchar_p(VoiceBankCompID),vbType)

    #功能：根据音源语言及编号获取声库句柄
    #输入参数：音源语言(int)，音源编号(int)，是否是AI声库（BOOL）。
    #          音源语言：0.日语,1:英语,2.韩语,3.西班牙语,4.汉语
    #返回值：声库句柄
    def GetVoiceBankByLangID(self,LangID,VoiceIndex,isAI=True):
        vbType=1 if isAI else 0
        slot=self.api.VDM_DatabaseManager_voiceBankByBSPC
        slot.argtypes = [c_void_p,c_int,c_int,c_int]
        slot.restype = c_void_p
        return slot(self.cPointer,LangID,VoiceIndex,vbType)

    #功能：获取颤音库句柄
    #返回值：数组，元素为颤音库句柄
    def GetVibratoBanks(self):
        ret=[]
        num=self.__get_VibratoBanks_Count()
        for i in range(0,num):
            ret.append(self.__get_VibratoBank_ByIndex(i))
        return ret

    #功能：获取VQM参数库句柄
    #返回值：数组，元素为颤音库句柄
    def GetDvqmDBs(self):
        ret=[]
        num=self.__get_DvqmDBs_Count()
        for i in range(0,num):
            ret.append(self.__get_DvqmDB_ByIndex(i))
        return ret

    #功能：根据ID获取VQM参数库句柄
    #输入参数：ID(int)
    #返回值：声库句柄
    def GetDvqmDBByID(self,DvqmID):
        slot=self.api.VDM_DatabaseManager_dvqmDBByID
        slot.argtypes = [c_void_p,c_int]
        slot.restype = c_void_p
        return slot(self.cPointer,DvqmID)

    def __get_DvqmDBs_Count(self):
        slot=self.api.VDM_DatabaseManager_numDvqmDBs
        slot.argtypes = [c_void_p]
        slot.restype = c_ulong
        return slot(self.cPointer)

    def __get_DvqmDB_ByIndex(self,DvqmDBIndex):
        slot=self.api.VDM_DatabaseManager_dvqmDBByIndex
        slot.argtypes = [c_void_p,c_int]
        slot.restype = c_void_p
        return slot(self.cPointer,DvqmDBIndex)

    def __get_VoiceBanks_Count(self,isAI=True):
        vbType=1 if isAI else 0
        slot=self.api.VDM_DatabaseManager_numVoiceBanks
        slot.argtypes = [c_void_p,c_int]
        slot.restype = c_ulong
        return slot(self.cPointer,vbType)
    
    def __get_VoiceBank_ByIndex(self,VoiceBankIndex,isAI=True):
        vbType=1 if isAI else 0
        slot=self.api.VDM_DatabaseManager_voiceBankByIndex
        slot.argtypes = [c_void_p,c_int,c_int]
        slot.restype = c_void_p
        return slot(self.cPointer,VoiceBankIndex,vbType)

    def __get_VibratoBanks_Count(self):
        slot=self.api.VDM_DatabaseManager_numVibratoBanks
        slot.argtypes = [c_void_p]
        slot.restype = c_ulong
        return slot(self.cPointer)

    def __get_VibratoBank_ByIndex(self,VibratoBankIndex):
        slot=self.api.VDM_DatabaseManager_vibratoBank
        slot.argtypes = [c_void_p,c_int]
        slot.restype = c_void_p
        return slot(self.cPointer,VibratoBankIndex)
