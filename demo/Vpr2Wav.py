import os
import sys
sys.path.append("..")
import argparse

from v6api.DSE import DSE
from v6api.VDM import VDM
from v6api.VSM import VSM
from v6api.VSM import Sequence
from v6api.VSM import Track
from v6api.VSM import Part

#工程进行中，未完成
#========================================
#VOCALOID处理函数区
#========================================
gObj={}
gData={}
def Initalize():
    vdm=VDM.VIS_VDM()
    if vdm.Create()==0:
        print("VDM声库管理器加载失败")
        return False
    gObj["DatabaseManager"]=vdm

    dse=DSE.VIS_DSE()
    if dse.Create()==0:
        print("DSE拼接合成引擎加载失败")
        return False
    gObj["DSEngine"]=dse

    if not dse.Initialize(vdm.GetPointer()):
        print("DSE拼接合成引擎初始化失败")
        return False        
    gData["DSEngine_Initialized"]=True
 
    vsm=VSM.VIS_VSM()
    if vsm.Create()==0:
        print("SequenceManager序列管理器加载失败")
        return False
    gObj["SequenceManager"]=vsm
    
    if not vsm.SetVDM(vdm.GetPointer()):
        print("SequenceManager关联VDM失败")
        return False
    if not vsm.SetDSE(vdm.GetPointer()):
        print("SequenceManager关联DSE失败")
        return False
    
    return True

def Terminal():
    if gData.get("DSEngine_Initalized",False):
        gObj["DSEngine"].Terminate()
    gObj["SequenceManager"].Destroy()
    gObj["DSEngine"].Destroy()
    gObj["DatabaseManager"].Destroy()

def RendFile(inputfile,outputfile,format,action):
    print("Rendering {}".format(inputfile))
    seqPtr=gObj["SequenceManager"].OpenSequenceVPR(inputfile)
    if seqPtr==0:
        print("SequenceManager打开工程失败")
        return False
    SeqObj=Sequence.VIS_Sequence(seqPtr)
    if format=="smf":
        if SeqObj.SaveSMF(outputfile):
            print("导出{}成功,格式{}".format(outputfile,format))
    elif format=="vpr":
        if SeqObj.SaveVPR(outputfile):
            print("导出{}成功,格式{}".format(outputfile,format))
    else:
        if action[2]:
            #显示列表
            v_Track=action[0]
            if v_Track==None:
                #显示声轨列表
                print("工程内声轨列表，请用-t参数选择需要渲染输出的声轨序号")
                print("--------------------------------------------")
                index=0
                type_str=["DSE","Audio","AI"]
                for ptrTrack in SeqObj.Get_Tracks():
                    TrackObj=Track.VIS_Track(ptrTrack)
                    if not TrackObj.IsAudioTrack:
                        print("序号:{}\t类别：{}\t轨道名：{}\t\t\t".format(
                                                    index,
                                                    type_str[TrackObj.Get_Type()],
                                                    TrackObj.Get_Name()
                                                    ))
                    index=index+1
            else:
                #显示声轨内分段列表
                ptrTrack=SeqObj.Get_Track(int(v_Track))
                if ptrTrack==0:
                    print("声轨打开失败")
                    return False
                TrackObj=Track.VIS_Track(ptrTrack)
                if TrackObj.IsAudioTrack:
                    print("纯音乐声轨目前无法处理")
                    return False
                type_str=["DSE","Audio","AI"]
                print("工程内声轨列表，请用-p参数选择需要渲染输出的声轨序号")
                print("当前声轨序号：{}，轨道类型：{}，轨道名：{}".format(
                                                    v_Track,
                                                    type_str[TrackObj.Get_Type()],
                                                    TrackObj.Get_Name()
                                                    ))
                print("--------------------------------------------")
                index=0
                
                for ptrPart in TrackObj.Get_Parts():
                    PartObj=Part.VIS_Part(ptrTrack)
                    PartName=PartObj.Get_Name()
                    print("序号:{}\t类别：{}\t段落名：{}\t起始时间:{}\t\t".format(
                                                    index,
                                                    type_str[PartObj.Get_Type()],
                                                    "(未命名)" if len(PartName)==0 else PartName,
                                                    PartObj.Get_PosTick()
                                                    ))
                    index=index+1
        else:
            v_Track=action[0]
            v_Part=action[1]
            if v_Track==None or v_Part==None:
                return False
            ptrTrack=SeqObj.Get_Track(int(v_Track))
            TrackObj=Track.VIS_Track(ptrTrack)
            ptrPart=TrackObj.Get_Part(int(v_Part))
            PartObj=Part.VIS_Part(ptrPart)
            ret=PartObj.Render(outputfile)
            if ret==0:
                print("导出{}成功,轨道{}区段{},格式{}".format(outputfile,v_Track,v_Part,format))
            else:
                print("发生错误，VSMResultID:{}".format(ret))
            pass

    SeqObj.CloseSequence()
    return True
#========================================
#主入口函数
#========================================
def main(cmds):
    if Initalize():
        RendFile(os.path.abspath(cmds.inputfile),
                 os.path.abspath(cmds.outputfile)
                 ,cmds.format,
                 [cmds.vpr_track,cmds.vpr_part,cmds.list_action]
                )
    Terminal()
    pass

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input",dest="inputfile",help="the vpr file",required=True)
    parser.add_argument("-o","--output",dest="outputfile",help="the output file",required=True)
    parser.add_argument("-f","--format",dest="format",help="setup the output file format",default="wav",choices=["wav","smf","vpr"])
    parser.add_argument("-t","--track",dest="vpr_track",help="setup the track index you want to rend,only wav format could use",default=None)
    parser.add_argument("-p","--part",dest="vpr_part",help="setup the part index of selected track you want to rend,only wav format could use",default=None)
    parser.add_argument("-l","--list",help="show list before rend",action="store_true",default=False,dest="list_action")
    cmdarg=parser.parse_args()
    main(cmdarg)

