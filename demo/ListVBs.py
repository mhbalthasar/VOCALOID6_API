import sys
sys.path.append("..")
from v6api.DSE import DSE
from v6api.VDM import VDM
from v6api.VDM import VoiceBank
from v6api.VDM import VibratoBank
from v6api.VDM import VibratoDetial
from v6api.VDM import DvqmDB
from v6api.VDM import DvqmProperty

dse=DSE.VIS_DSE()
vdm=VDM.VIS_VDM()
vdb=VoiceBank.VIS_VoiceBank()
vib=VibratoBank.VIS_VibratoBank()
vid=VibratoDetial.VIS_VibratoDetial()
vqm=DvqmDB.VIS_DvqmDB()
vqp=DvqmProperty.VIS_DvqmProperty()

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
    vb_List=vdm.GetVoiceBanks(True)
    for db_Handle in vb_List:
        dbA=vdb.VoiceBankToObject(db_Handle)
        dbA["isAI"]=True
        ret.append(dbA)
    vb_List=vdm.GetVoiceBanks(False)
    for db_Handle in vb_List:
        dbA=vdb.VoiceBankToObject(db_Handle)
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
    vb_List=vdm.GetVibratoBanks()
    for vb_Handle in vb_List:
        vib_c=vib.VibratoBankToObject(vb_Handle)
        vib_e=[]
        for vib_t_i in vib_c["VibratoTemplates"]:
            vib_e.append(vid.VibratoTemplateToObject(vib_t_i))
        vib_c["VibratoTemplates"]=vib_e
        ret.append(vib_c)
    return ret


def echo_vibratos(Vibratos):
    show_VTN=["None","Normal1","Normal2","Normal3","Normal4","Extreme1","Extreme2","Extreme3","Extreme4","Fast1","Fast2","Fast3","Fast4","Slight1","Slight2","Slight3","Slight4"]
    print("颤音模板库信息")
    print("==============")
    for dbA in Vibratos:
        print("模板库名称：{}".format(dbA["Name"]))
        print("安装路径：{}".format(dbA["InstallPath"]))
        for vtA in dbA["VibratoTemplates"]:
            print("\t颤音名:{}".format(vtA["Name"]))
            print("\t颤音类型:{}".format(show_VTN[vtA["Type"]]))
            print("\t颤音参数-幅度:{}个控制点".format(len(vtA["Data"]["VibratoDepth"])))
            print("\t颤音参数-幅度-控制点范例:{}".format(vtA["Data"]["VibratoDepth"][0]))
            print("\t颤音参数-频率:{}个控制点".format(len(vtA["Data"]["VibratoRate"])))
            print("\t颤音参数-频率-控制点范例:{}".format(vtA["Data"]["VibratoRate"][0]))
        print('---------------')

def get_dvqms():
    ret=[]
    vb_List=vdm.GetDvqmDBs()
    for vb_Handle in vb_List:
        vib_c=vqm.DvqmDBToObject(vb_Handle)
        vqm_A=[]
        vqm_R=[]
        for vq in vib_c["Properties"]["Attrack"]:
            vqm_A.append(vqp.DvqmPropertyToObject(vq))
        for vq in vib_c["Properties"]["Release"]:
            vqm_R.append(vqp.DvqmPropertyToObject(vq))
        vib_c["Properties"]["Attrack"]=vqm_A
        vib_c["Properties"]["Release"]=vqm_R
        ret.append(vib_c)
    return ret

def echo_dvqms(Dvqms):
    show_Lang=["日语","英语","韩语","西班牙语","汉语"]
    print("VQM预置参数库信息")
    print("==============")
    for dbA in Dvqms:
        print("\tAttrack/Release参数库ID：{}".format(dbA["ID"]))
        print("\t参数库组件序列号：{}".format(dbA["CompID"]))
        print("\t安装路径：{}".format(dbA["InstallPath"]))
        print("\t适配语言：{}".format(show_Lang[dbA["LangID"]]))
        print("\t绑定声库序列号：{}".format(dbA["Binded_VoiceBank_CompIDs"]))
        print("\t预置唱腔-音头(A):{}个".format(len(dbA["Properties"]["Attrack"])))
        print("\t预置唱腔-音头(A)范例:{}".format(dbA["Properties"]["Attrack"][0]))
        print("\t预置唱腔-音尾(R):{}个".format(len(dbA["Properties"]["Release"])))
        print("\t预置唱腔-音尾(R)范例:{}".format(dbA["Properties"]["Release"][0]))
        print('---------------')

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

    print("")
    #读取并显示全部VQM库配置
    #VQM控制声库的Attrack（音头）和Release（音尾）的效果和唱腔
    Dvqms=get_dvqms()
    echo_dvqms(Dvqms)

    #Halt DSE
    dse.Terminate()
    #Destroy
    destroy()

def destroy():
    dse.Destroy()
    vdm.Destroy()

main()
