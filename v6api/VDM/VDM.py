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
        slot.restype = c_char
        ret=slot(self.cPointer)
        return False if ret==0 else True

    #功能：获取声库数量
    #输入参数：是否是AI声库（BOOL）
    #返回值：组件数量（long）
    def NumVoiceBanks(self,isAI=True):
        vbType=1 if isAI else 0
        slot=self.api.VDM_DatabaseManager_numVoiceBanks
        slot.argtypes = [c_void_p,c_int]
        slot.restype = c_ulong
        return slot(self.cPointer,vbType)

    #功能：获取默认声库句柄
    #输入参数：是否是AI声库（BOOL）
    #返回值：声库句柄
    def DefaultVoiceBank(self,isAI=True):
        vbType=1 if isAI else 0
        slot=self.api.VDM_DatabaseManager_defaultVoiceBank
        slot.argtypes = [c_void_p,c_int]
        slot.restype = c_void_p
        return slot(self.cPointer,LicenseIndex)

    #功能：设置为默认声库
    #输入参数：声库句柄，是否是AI声库（BOOL）
    #返回值：BOOL
    def SetVoiceBankAsDefault(self,pVoiceBank,isAI=True):
        vbType=1 if isAI else 0
        slot=self.api.VDM_VoiceBank_setDefault
        slot.argtypes = [c_void_p,c_int]
        slot.restype = c_void_p
        ret=slot(pVoiceBank,vbType)
        return False if ret==0 else True

    #功能：根据序号获取声库句柄
    #输入参数：声库序号，是否是AI声库（BOOL）
    #返回值：声库句柄
    def GetVoiceBankByIndex(self,VoiceBankIndex,isAI=True):
        vbType=1 if isAI else 0
        slot=self.api.VDM_DatabaseManager_voiceBankByIndex
        slot.argtypes = [c_void_p,c_int,c_int]
        slot.restype = c_void_p
        return slot(self.cPointer,VoiceBankIndex,vbType)

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

    #功能：获取颤音库数量
    #返回值：组件数量（long）
    def NumVibratoBanks(self):
        slot=self.api.VDM_DatabaseManager_numVibratoBanks
        slot.argtypes = [c_void_p]
        slot.restype = c_ulong
        return slot(self.cPointer)

    #功能：根据序号获取颤音库句柄
    #输入参数：颤音库序号
    #返回值：颤音库句柄
    def GetVibratoBankByIndex(self,VibratoBankIndex):
        slot=self.api.VDM_DatabaseManager_vibratoBank
        slot.argtypes = [c_void_p,c_int]
        slot.restype = c_void_p
        return slot(self.cPointer,VibratoBankIndex)


