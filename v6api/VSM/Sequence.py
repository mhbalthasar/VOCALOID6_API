import sys
import os
sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0],".."))
import v6loader
from ctypes import *

import zipfile
from tempfile import TemporaryDirectory

#功能：序列操作器
#作用：调度管理工程的一切进展
#描述：一个被更上层操作函数调用的函数。
class VIS_Sequence:
    def __init__(self,seqPtr):
        self.vocaloid_dir=v6loader.get_vocaloid_dir()
        self.api=v6loader.load_library(self.vocaloid_dir,"vsm.dll")
        self.cPointer=seqPtr
        pass

    def __del__(self):
        v6loader.free_library(self.api)
        pass

    #功能：返回引擎句柄
    def GetPointer(self):
        return self.cPointer

    #功能：关闭序列
    def CloseSequence(self):
        if self.cPointer==0:
            return
        slot = self.api.VIS_VSM_WIVSMSequence_close
        slot.argtypes = [c_void_p]
        slot.restype = c_bool
        ret=slot(self.cPointer)
        if ret:
            self.cPointer=0
        return ret

    #功能：保存一个SMFMidi文件
    #传入参数：文件目标地址[必须]，是否Utf8（非UTF8只能存ShiftJIS）
    #返回值：BOOL
    def SaveSMF(self,FilePath,isUtf8=True):
        VSMEnc=0 if isUtf8 else 1
        slot=self.api.VIS_VSM_WIVSMSequence_saveSMF
        slot.argtypes = [c_void_p,c_wchar_p,c_int]
        slot.restype = c_bool
        ret=slot(self.cPointer,c_wchar_p(FilePath),VSMEnc)
        return ret
    
    #功能：保存一个Seq序列文件
    #传入参数：文件组目标目录[必须]，是否可读性优化
    #返回值：BOOL
    def SaveJson(self,DirPath,isPrettify=True):
        slot=self.api.VIS_VSM_WIVSMSequence_save
        slot.argtypes = [c_void_p,c_wchar_p,c_bool]
        slot.restype = c_bool
        ret=slot(self.cPointer,c_wchar_p(DirPath),isPrettify)
        return ret

    #功能：保存一个V6的序列
    #传入参数：文件地址[必须]，是否可读性优化
    #返回值：序列句柄
    def SaveVPR(self,FilePath):
        ret=0
        with TemporaryDirectory() as tempdir:
            seqZip=zipfile.ZipFile(FilePath, 'w', zipfile.ZIP_DEFLATED)
            self.SaveJson(tempdir,False)
            for path,dirnames,filenames in os.walk(tempdir):
                fpath = path.replace(tempdir,'')
                for filename in filenames:
                    seqZip.write(os.path.join(path,filename),os.path.join(fpath,filename))
            seqZip.close()
        return ret

    #功能：获取Track列表
    #返回值：数组，元素为Track句柄
    def Get_Tracks(self):
        ret=[]
        num=self.__get_Track_Count()
        for i in range(0,num):
            ret.append(self.__get_Track_ByIndex(i))
        return ret

    #功能：获取Track
    #输入参数：TrackID
    #返回值：Track句柄
    def Get_Track(self,TrackIndex):
        ret=[]
        num=self.__get_Track_Count()
        if TrackIndex<0 or TrackIndex>=num:
            return 0
        return self.__get_Track_ByIndex(TrackIndex)

    #功能：判断Track是否在序列内
    #输入值：Track句柄
    #返回值：BOOL
    def IsTrackInSeq(self,ptrTrack):
        slot=self.api.VIS_VSM_WIVSMSequence_hasTrack
        slot.argtypes = [c_void_p,c_void_p]
        slot.restype = c_bool
        return slot(self.cPointer,ptrTrack)

    #功能：获取允许轨道数量
    #返回值：数量
    def GetMaxTrackNum(self):
        slot=self.api.VIS_VSM_WIVSMSequence_maxNumTrack
        slot.argtypes = [c_void_p]
        slot.restype = c_ulong
        return slot(self.cPointer)

    def __get_Track_Count(self):
        slot=self.api.VIS_VSM_WIVSMSequence_numTrack
        slot.argtypes = [c_void_p]
        slot.restype = c_ulong
        return slot(self.cPointer)

    def __get_Track_ByIndex(self,Index):
        slot=self.api.VIS_VSM_WIVSMSequence_track
        slot.argtypes = [c_void_p,c_int]
        slot.restype = c_void_p
        return slot(self.cPointer,Index)