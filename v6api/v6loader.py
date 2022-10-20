import os
import platform

import ctypes
import _ctypes

def __get_win_v6dir():
    try:
        import winreg
        hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\VOCALOID6\Application\Components\BCSPB2X3L62LZCD4", access = winreg.KEY_READ + winreg.KEY_WOW64_64KEY)
        (regValue,regType)=winreg.QueryValueEx(hkey,"Path")
        winreg.CloseKey(hkey)
        return regValue
    except:
        return None

def get_vocaloid_common_dir():
    vdir = os.environ.get("VOCALOID_COMMON_PATH","")
    exp_f=os.path.join(vdir,"Explib","expa2.ddi")
    if os.path.exists(exp_f):
        return vdir
    vdir = os.environ.get("CommonProgramFiles","")
    vdir = os.path.join(vdir,"VOCALOID6")
    exp_f=os.path.join(vdir,"Explib","expa2.ddi")
    if os.path.exists(exp_f):
        return vdir
    return ""

def get_vocaloid_dir():
    vdir = os.environ.get("VOCALOID_PATH",None)
    if vdir != None:
        return vdir
    else:
        plat = platform.system()
        if plat == 'Windows':
            vdir = __get_win_v6dir()
            if vdir != None:
                return vdir
    return None

def load_library(base_dir,file_name):
    dll_file=os.path.join(base_dir,file_name)
    return ctypes.CDLL(dll_file)

def free_library(dll_api):
    try:
        handle=dll_api._handle
        plat = platform.system()
        if plat == 'Windows':
            _ctypes.FreeLibrary(handle)
        else:
            _ctypes.dlclose(handle)
        return True
    except:
        return False
