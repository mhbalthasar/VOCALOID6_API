import sys
import os
sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0]))
import v6loader
from ctypes import *

class VIS_DSE:
    def __init__(self):
        self.vocaloid_dir=v6loader.get_vocaloid_dir()
        self.api=v6loader.load_library(self.vocaloid_dir,"dse.dll")
        self.__define_dll()
        pass

    def __del__(self):
        v6loader.free_library(self.api)
        pass

    def __define_dll(self):
        self.api.VIS_DSE_CreateManager.argtypes = []
        self.api.VIS_DSE_CreateManager.restype = c_void_p
        self.api.VIS_DSE_CreateManager.argtypes = []
        self.api.VIS_DSE_CreateManager.restype = c_void_p

    def CreateManager(self):
        cfunc=self.api.VIS_DSE_CreateManager
        #cfunc.restype = c_void_p
        print(cfunc())

