#SequenceManager = WVSMModuleIF.CreateManager(Yamaha.VOCALOID.Identifier.Application.AppID, Assembly.GetExecutingAssembly().GetName().Version!.ToString());
#if (SequenceManager == null)
#{#
#	MessageBoxDeliverer.GeneralError(splash, Yamaha.VOCALOID.Properties.Resources.MsgBox_VSMInitialization_Error);
#	return ModuleResult.Fail;
#}
#SequenceManager.SetDatabaseManager(DatabaseManager);
#SequenceManager.SetDSEManager(DSEManager);
#if (SequenceManager != null)
#{#
#	SequenceManager.CacheCapacity = CacheCapacity.GetBytes(CacheCapacity.OptionFromUserSettings);
#}

import sys
import os
sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0],".."))
import v6loader
from ctypes import *

import zipfile
from tempfile import TemporaryDirectory

#功能：工程序列管理器（工程序列指V5、V6的工程文件中的实际内容体）
#作用：调度管理工程的一切进展
#描述：一个被更上层操作函数调用的函数。
class VIS_VSM:
    #定义结构体类型
    class __struct_SequenceData(Structure):
        _fields_ = [("SamplingRate",c_int),("MaxNumTracks",c_ulong),("MaxUndoCount",c_ulong)]

    def __init__(self):
        self.vocaloid_dir=v6loader.get_vocaloid_dir()
        self.api=v6loader.load_library(self.vocaloid_dir,"vsm.dll")
        self.cPointer=0
        pass

    def __del__(self):
        v6loader.free_library(self.api)
        pass

    #功能：返回引擎句柄
    def GetPointer(self):
        return self.cPointer

    #功能：创建对象
    #输入参数：appID(string),appVersion(string)，均可使用默认值
    #返回值：BOOL
    def Create(self,appID="VOCALOID6",appVersion="6.0.1"):
        slot = self.api.VIS_VSM_WVSMModuleIF_createManager
        slot.argtypes = [c_wchar_p,c_wchar_p]
        slot.restype = c_void_p
        self.cPointer = slot(c_wchar_p(appID),c_wchar_p(appVersion))
        return False if self.cPointer==0 else True

    #功能：销毁对象
    def Destroy(self):
        if self.cPointer==0:
            return
        slot = self.api.VIS_VSM_WIVSMSequenceManager_destroy
        slot.argtypes = [c_void_p]
        slot.restype = None
        slot(self.cPointer)

    #功能：映射VDM管理器
    #传入参数：VDM声库管理器句柄
    #返回值：BOOL
    def SetVDM(self,ptrVDM):
        slot=self.api.VIS_VSM_WIVSMSequenceManager_setDatabaseManager
        slot.argtypes = [c_void_p,c_void_p]
        slot(self.cPointer,ptrVDM)
        return False if self.__getVDM()==0 else True

    def __getVDM(self):
        slot=self.api.VIS_VSM_WIVSMSequenceManager_databaseManager
        slot.argtypes = [c_void_p]
        slot.restype = c_void_p
        return slot(self.cPointer)

    #功能：映射DSE管理器
    #传入参数：DSE引擎句柄
    #返回值：BOOL
    def SetDSE(self,ptrDSE):
        slot=self.api.VIS_VSM_WIVSMSequenceManager_setDSEManager
        slot.argtypes = [c_void_p,c_void_p]
        slot(self.cPointer,ptrDSE)
        return False if self.__getDSE()==0 else True

    def __getDSE(self):
        slot=self.api.VIS_VSM_WIVSMSequenceManager_dseManager
        slot.argtypes = [c_void_p]
        slot.restype = c_int
        return slot(self.cPointer)

    #功能：判断是否可用
    #返回值：BOOL
    def Has(self):
        slot=self.api. VIS_VSM_WVSMModuleIF_hasManager
        slot.argtypes = [c_void_p]
        slot.restype = c_bool
        return slot(self.cPointer)

    #功能：获取上一个错误代码
    #返回值：int,枚举取值如下：
    #NoError=0,OutOfMemory=1,InvalidArgument=2,FailedToCreateEditCommand,ObjectNotFound,ParentNotFound,InvalidPath,FailedToCopyFile,FileAlreadyExists,ObjectIsProtected,FailedToLoadVSM,CannotFindUid,
	#FailedToGetHomeDir,FailedToCreateTempDir,FailedToCreateCachesDir,FailedToCreateTempProject,FailedToMoveTempProject,FailedToCreateOutputDir,FailedToCreateSequenceUUID,FailedToCreateSequenceTempDir,InvalidSamplingRate,FailedToRemoveSameTimeEvent,
	#MaxNumTrack,InvalidTrackType,InvalidTrackName,MidiPartStartAbsolutePosTooSmall,MidiPartStartAbsolutePosTooLarge,MidiPartEndAbsolutePosTooLarge,MidiPartDurationTooShort,MidiPartDurationTooLong,InvalidDivideMidiPartPos,JoinMidiPartOfDifferentParent,EditCommandsStaging,
	#InvalidPartName,ControllerRelativePosTooSmall,ControllerRelativePosTooLarge,ControllerAbsolutePosTooSmall,ControllerAbsolutePosTooLarge,CannotFindTargetTrack,CannotFindTopController,InvalidControllerType,NoteStartRelativePosTooSmall,NoteStartRelativePosTooLarge,
	#NoteStartAbsolutePosTooSmall,NoteStartAbsolutePosTooLarge,NoteEndRelativePosTooLarge,NoteEndAbsolutePosTooLarge,
	#NoteDurationTooShort,NoteDurationTooLong,InvalidNoteNumber,InvalidNoteVelocity,InvalidLyric,InvalidPhoneme,InvalidLangID,VibratoDurationTooShort,VibratoDurationTooLong,VibratoEventRelativePosTooSmall,VibratoEventRelativePosTooLarge,InvalidVibratoEventType,NoteEventsNotFound,MidiPartIsDisable,
	#SequenceNotFound,SequenceTempDirPathNotFound,DatabaseManagerNotFound,VoiceBankNotFound,FailedToCreateVVoiceTable,FailedToGetDseModule,FailedToCreateDSE,FailedToStartDSE,FailedToOpenRenderedFile,FailedToCreateDseMidiEventsBuffer,FailedToCreateDseWaveBuffer,
	#FailedToDseDoStepSynthesis,FailedToDseDoExportScore,FailedToCreateNRPN_Singer,PartialRendererNotCreated,DsePartialSynthNotStarted,FailedToResetDsePartialSynth,DuplicatedEffectID,DuplicatedEffectValueName,MidiEffectIsDisabled,FailedToInitVsqParserModule,FailedToCreateVsqParser,
	#InvalidVsqxSchemaDirPath,FailedToParseVsqx,VsqObjTreeNotFound,InvalidVsqFormat,VsqRootNodeNotFound,VsqSequenceNotFound,VsqMasterTrackNotFound,VsqTempoNotFound,VsqTimeSigNotFound,VsqMixerNotFound,FailedToCreateJsonDoc,FailedToOpenJsonFile,
	#FailedToParseJson,InvalidJsonDocRootType
    def LastError(self):
        slot=self.api. VIS_VSM_WVSMModuleIF_lastError
        slot.argtypes = []
        slot.restype = c_int
        return slot()

    #功能：创建一个空白的序列
    #传入参数：SEQ基本属性：采样率、最大轨道数、最大撤销数
    #返回值：序列句柄
    def CreateSequence(self,SeqSamplingRate=44100,SeqMaxNumTracks=99,SeqMaxUndoCount=99):
        SeqData=[SeqSamplingRate,SeqMaxNumTracks,SeqMaxUndoCount]
        ptrSeqData=self.__struct_SequenceData(*SeqData)
        slot=self.api.VIS_VSM_WIVSMSequenceManager_createSequence
        slot.argtypes = [c_void_p,POINTER(self.__struct_SequenceData)]
        ret=slot(self.cPointer,ptrSeqData)
        return ret

    #功能：打开一个V5/V6的序列
    #传入参数：文件地址[必须]，SEQ基本属性-采样率、SEQ基本属性-最大轨道数、SEQ基本属性-最大撤销数
    #返回值：序列句柄
    def OpenSequenceVPR(self,FilePath,SeqSamplingRate=44100,SeqMaxNumTracks=32,SeqMaxUndoCount=0):
        ret=0
        with TemporaryDirectory() as tempdir:
            seqZip=zipfile.ZipFile(FilePath, 'r', zipfile.ZIP_DEFLATED)
            seqZip.extractall(tempdir)
            seqZip.close()
            file=os.path.join(tempdir,'Project','sequence.json')
            if os.path.exists(file):
                ret=self.OpenSequenceVSQX(file,"",SeqSamplingRate,SeqMaxNumTracks,SeqMaxUndoCount)
        return ret

    #功能：打开一个V3/V4的序列
    #传入参数：文件地址[必须]，VSQX解析Schema文件路径，SEQ基本属性-采样率、SEQ基本属性-最大轨道数、SEQ基本属性-最大撤销数
    #返回值：序列句柄
    def OpenSequenceVSQX(self,FilePath,vsqxSchemaDirPath="",SeqSamplingRate=44100,SeqMaxNumTracks=32,SeqMaxUndoCount=0):
        if vsqxSchemaDirPath=="":
            vsqxSchemaDirPath=self.vocaloid_dir;
        SeqData=[SeqSamplingRate,SeqMaxNumTracks,SeqMaxUndoCount]
        ptrSeqData=self.__struct_SequenceData(*SeqData)
        slot=self.api.VIS_VSM_WIVSMSequenceManager_openSequence
        slot.argtypes = [c_void_p,c_wchar_p,c_wchar_p,POINTER(self.__struct_SequenceData)]
        ret=slot(self.cPointer,c_wchar_p(FilePath),c_wchar_p(vsqxSchemaDirPath),ptrSeqData)
        return ret
        
    #功能：打开一个V1的Midi的序列，SMF
    #传入参数：文件地址[必须]，VSQX解析Schema文件路径，SEQ基本属性-采样率、SEQ基本属性-最大轨道数、SEQ基本属性-最大撤销数
    #返回值：序列句柄
    def OpenLegacySequence(self,FilePath,codePage=932,channelAsTrack=True,SeqSamplingRate=44100,SeqMaxNumTracks=32,SeqMaxUndoCount=0):
        SeqData=[SeqSamplingRate,SeqMaxNumTracks,SeqMaxUndoCount]
        ptrSeqData=self.__struct_SequenceData(*SeqData)
        slot=self.api.VIS_VSM_WIVSMSequenceManager_openLegacySequence
        slot.argtypes = [c_void_p,c_wchar_p,POINTER(self.__struct_SequenceData),c_uint,c_bool]
        ret=slot(self.cPointer,c_wchar_p(FilePath),ptrSeqData,codePage,channelAsTrack)
        return ret
        