import sys
sys.path.append("..")
from v6api.DSE import DSE
from v6api.VDM import VDM
from v6api.VDM import VoiceBank

dse=DSE.VIS_DSE()
vdm=VDM.VIS_VDM()
vdb=VoiceBank.VIS_VoiceBank()

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

def get_vb_detial(lic_arr):
    ret=[]
    vb_Num_AI=vdm.NumVoiceBanks(True)
#   vb_Num_SE=vdm.NumVoiceBanks(False)
    for vb_Index in range(0,vb_Num_AI):
        print(vdb.VoiceBankToObject(vdm.GetVoiceBankByIndex(vb_Index,True)))
    pass


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

    #GetVB_Licenses
    Licenses=get_vb_licenses()
    echo_vb_licenses(Licenses)

    #GetVB_Detial
    License_Details=get_vb_detial(Licenses)

    #Halt DSE
    dse.Terminate()
    #Destroy
    destroy()

def destroy():
    dse.Destroy()
    vdm.Destroy()

main()
