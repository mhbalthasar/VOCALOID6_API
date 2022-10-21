import sys
sys.path.append("..")
from v6api.DSE import DSE
from v6api.VDM import VDM
from v6api.VDM import VoiceBank
from v6api.VDM import VibratoBank

dse=DSE.VIS_DSE()
vdm=VDM.VIS_VDM()
vdb=VoiceBank.VIS_VoiceBank()
vib=VibratoBank.VIS_VibratoBank()

def get_vb_licenses():
    ret=[]
    vbNum=dse.NumLicenses()
    for vb_index in range(0,vbNum):
        vb_lic=dse.GetLicense(vb_index)
        ret.append(vb_lic)
    return ret

def echo_vb_licenses(lic_arr):
    print("已安装组件清单")
    print("==============")
    print("组件类型\t\t组件序列号\t\t组件名")
    for lic in lic_arr:
        print("{}\t\t{}\t\t{}".format("Application" if lic["CompType"]==1 else "VoiceBank",lic["CompID"],lic["CompName"]))

def get_vb_detials():
    ret=[]
    vb_Num=vdm.NumVoiceBanks(True)
    for vb_Index in range(0,vb_Num):
        dbA=vdb.VoiceBankToObject(vdm.GetVoiceBankByIndex(vb_Index,True))
        dbA["isAI"]=True
        ret.append(dbA)
    vb_Num=vdm.NumVoiceBanks(False)
    for vb_Index in range(0,vb_Num):
        dbA=vdb.VoiceBankToObject(vdm.GetVoiceBankByIndex(vb_Index,False))
        dbA["isAI"]=False
        ret.append(dbA)
    return ret

def echo_vb_detials(lic_arr):
    show_Lang=["日语","英语","韩语","西班牙语","汉语"]
    print("当前声库信息")
    print("==============")
    ret=[]
    for dbA in lic_arr:
        print("音源名：{}".format(dbA["VoiceName"]))
        print("音源类型：{}".format("AI声库" if dbA["isAI"] else "拼接声库"))
        print("声库名：{}".format(dbA["CompName"]))
        print("声库序列号：{}".format(dbA["CompID"]))
        print("演唱风格：{}".format(dbA["StyleID"]))
        print("安装路径：{}".format(dbA["InstallPath"]))
        print("音色序号：{}".format(dbA["TimbreIndex"]))
        print("默认语言：{}".format(show_Lang[dbA["DefaultLangID"]]))
        print("音源序号：{}".format(dbA["VoiceIndex"]))
        spL=[]
        for lid in dbA["SupportLangIDs"]:
            spL.append(show_Lang[lid])
        print("支持的语言：{}".format(spL))
        print("音源初始参数: {}".format(dbA["VoiceParameters"]))
        print("-----------------")


def get_vibratos():
    ret=[]
    return ret


def echo_vibratos(Vibratos):
    print(Vibratos)

def main():
    #Create VDM
    ret=vdm.Create()
    if ret==0:
        print("VDM声库管理器加载失败")
        return
    #Create DSE
    ptrDSE=dse.Create()
    if ptrDSE==0:
        print("DSE拼接合成引擎加载失败")
        return destroy()

    #Init DSE
    if not dse.Initialize(vdm.GetPointer()):
        print("DSE拼接合成引擎初始化失败")
        return destroy()

    #读取并显示全部YAMAHA组件
    Licenses=get_vb_licenses()
    echo_vb_licenses(Licenses)

    print("")
    #读取并显示全部可用声库
    VB_Detials=get_vb_detials()
    echo_vb_detials(VB_Detials)

    print("")
    #读取并显示全部颤音配置
    Vibratos=get_vibratos()
    echo_vibratos(Vibratos)

    #Halt DSE
    dse.Terminate()
    #Destroy
    destroy()

def destroy():
    dse.Destroy()
    vdm.Destroy()

main()
