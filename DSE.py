import v6dir
import os
import ctypes

class VIS_DSE:
    def __init__(self):
        self.vocaloid_dir=v6dir.get_vocaloid_dir()
        self.dllFile=os.path.join(self.vocaloid_dir,"dse.dll")
        self.api=ctypes.WinDLL(self.dllFile)        
        pass


if __name__=="__main__":
    #DEBUG
    API=VIS_DSE()
