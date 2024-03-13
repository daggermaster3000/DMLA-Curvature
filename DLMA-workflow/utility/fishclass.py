from utility.fishutil import *
import numpy as np

class Zebrafish():

    def __init__(self, info):
        self.info = info
        self.curvature_plot = None

    def islarva(self):
        return self.info['dead'] == [] and self.info['unhatched embryo'] == []

    def isdead(self):
        return self.info['dead'] != []

    def isembryo(self):
        return self.info['unhatched embryo'] != []

    def isbent(self):
        return self.info['bent spine'] != []

    def isjawmal(self):
        return self.info['jaw malformation'] != []

    def ispedema(self):
        return self.info['pericardial edema'] != []

    def isyedema(self):
        return self.info['yolk edema'] != []

    def isheadamage(self):
        return self.info['head hemorrhage'] != []

    def isabsence(self):
        return self.info['swim bladder absence'] != []

    def haseye(self):
        return self.info['eye'] != []

    def hastail(self):
        return self.info['tail'] != []

    def haspine(self):
        return self.info['spine'] != [] or self.info['bent spine'] != []

    def getlength(self):
        if self.islarva() and self.haseye():
            return get_body(self.info)
        else:
            return np.nan

    def getcurve(self):
        if self.haspine():
            angle, curvature, self.curvature_plot = get_curve(self.info)
            return angle, curvature
        else:
            return np.nan, np.nan
        
    def gethead(self):
        if self.islarva():
            if self.info['head'] != []:
                return self.info['head'][0]
            elif self.info['head hemorrhage'] != []:
                return self.info['head hemorrhage'][0]
            else:
                return np.nan
        else:
            return np.nan

    def geteye(self):
        if self.haseye():
            return self.info['eye'][0]
        else:
            return np.nan

    def getheart(self):
        if self.islarva():
            if self.info['heart'] != []:
                return self.info['heart'][0]
            elif self.info['pericardial edema'] != []:
                return self.info['pericardial edema'][0]
            else:
                return np.nan
        else:
            return np.nan

    def getyolk(self):
        if self.islarva():
            if self.info['yolk'] != []:
                return self.info['yolk'][0]
            elif self.info['yolk edema'] != []:
                return self.info['yolk edema'][0]
            else:
                return np.nan
        else:
            return np.nan

    def getail(self):
        if self.hastail():
            return get_tail_length(self.info)
        else:
            return np.nan

    def getspine(self):
        if self.haspine():
            return get_spine_length(self.info)
        else:
            return np.nan

    def getbladder(self):
        if self.islarva():
            if self.info['swim bladder'] != []:
                return self.info['swim bladder'][0]
            elif self.info['swim bladder absence'] != []:
                return self.info['swim bladder absence'][0]
            else:
                return np.nan
        else:
            return np.nan

    def getjaw(self):
        if self.islarva():
            if self.info['lower jaw'] != []:
                return self.info['lower jaw'][0]
            elif self.info['jaw malformation'] != []:
                return self.info['jaw malformation'][0]
            else:
                return np.nan
        else:
            return np.nan