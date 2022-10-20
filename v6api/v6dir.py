import os
import platform

def __get_win_v6dir():
    try:
        import winreg
        hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\VOCALOID6\Application\Components\BCSPB2X3L62LZCD4", access = winreg.KEY_READ + winreg.KEY_WOW64_64KEY)
        (regValue,regType)=winreg.QueryValueEx(hkey,"Path")
        winreg.CloseKey(hkey)
        return regValue
    except:
        return None


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


