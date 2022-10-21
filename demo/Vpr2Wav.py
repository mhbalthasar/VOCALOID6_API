import sys
sys.path.append("..")
import argparse

from v6api.DSE import DSE
from v6api.VDM import VDM
from v6api.VSM import VSM

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

def RendFileToWav(inputfile,outputfile):
    print("Rendering {}".format(inputfile))
    seqPtr=gObj["SequenceManager"].OpenSequenceVPR(inputfile)
    if seqPtr==0:
        print("SequenceManager打开工程失败")
        return False
    print("工程打开成功")
    ##TODO:RENDWORK
    return True
#========================================
#主入口函数
#========================================
def main(cmds):
    if Initalize():
        RendFileToWav(cmds.inputfile,cmds.outputfile)
    Terminal()
    pass

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input",dest="inputfile",help="the vpr file",required=True)
    parser.add_argument("-o","--output",dest="outputfile",help="the wav file",required=True)
    cmdarg=parser.parse_args()
    main(cmdarg)

