import configparser
import os
from SWANi.utils.APPLABELS import APPLABELS

class SWANiConfig(configparser.ConfigParser):

    INPUTLIST=['mr_t13d',
                            'mr_flair3d',
                            'mr_mdc',
                            'mr_venosa',
                            'mr_venosa2',
                            'mr_dti',
                            'mr_asl',
                            'ct_brain',
                            'mr_fmri',
                            'pet_brain',
                            'op_mr_flair2d_tra',
                            'op_mr_flair2d_cor',
                            'op_mr_flair2d_sag']

    TRACTS={}
    TRACTS["af"]=['Arcuate Fasciculus','true']
    TRACTS["cst"]=['Corticospinal Tract','true']
    TRACTS["or"]=['Optic Radiation','true']
    TRACTS["ar"]=['Acoustic Radiation','false']
    TRACTS["fa"]=['Frontal Aslant','false']
    TRACTS["fx"]=['Fornix','false']
    TRACTS["ifo"]=['Inferior Fronto-Occipital Fasciculus','false']
    TRACTS["ilf"]=['Inferior Longitudinal Fasciculus','false']
    TRACTS["uf"]=['Uncinate Fasciculus','false']

    def __init__(self, ptFolder=None):
        super(SWANiConfig,self).__init__()
        

        if ptFolder!=None:
            #NEL CASO STIA GESTENDO LE IMPOSTAZIONI SPECIFICHE DI UN UTENTE COPIO ALCUNI VALORI DALLE IMPOSTAZIONI GLOBALI
            self.globalConfig=False
            self.configFile=os.path.join(os.path.join(ptFolder,".config"))
        else:
            #NEL CASO STIA GESTENDO LE IMPOSTAZIONI GLOBALI DELL'APP
            self.globalConfig=True    
            self.configFile=os.path.abspath(os.path.join(os.path.expanduser("~"),"."+APPLABELS.APPNAME+"config"))

        self.createDefaultConfig()
        
        if os.path.exists(self.configFile):
            self.read(self.configFile)
            

        self.save()

    def reLoad(self):
        self.read(self.configFile)        

    def createDefaultConfig(self):
        if self.globalConfig:
            self['MAIN'] = {'patientsfolder': '',
                            'patientsprefix': 'pt_',
                            'slicerPath':'',
                            'shortcutPath':'',
                            'lastPID':'-1',
                            'maxPt':'1',
                            'maxPtCPU':'-1',  
                            'slicerSceneExt':'0',
                            }
            
            self['WF_OPTION'] = {
                            'wfType':'0',
                            'freesurfer':'true',
                            'hippoAmygLabels':'true',
                            'domap':'true',
                            'ai':'true',
                            }
    
            self['OPTIONAL_SERIES'] = {'mr_flair2d':'false'}
    
            self['DEFAULTFOLDERS']={}
            for this in self.INPUTLIST:
                self['DEFAULTFOLDERS']['default_'+this+'_folder']='dicom/'+this+'/'
    
            self['DEFAULTNAMESERIES'] = {}
            for name in self.INPUTLIST:
                self['DEFAULTNAMESERIES']["Default_"+name+"_name"]=""
    
            self['DEFAULTTRACTS'] = {}
    
            for index,key in enumerate(self.TRACTS):
                self['DEFAULTTRACTS'][key]= self.TRACTS[key][1]
        else:
            tmpConfig=SWANiConfig()
            self['WF_OPTION']=tmpConfig['WF_OPTION']
            self['DEFAULTTRACTS']=tmpConfig['DEFAULTTRACTS']


    def save(self):
        with open(self.configFile,"w") as openedFile:
            self.write(openedFile)

    def getPatientsFolder(self):
        return self["MAIN"]["PatientsFolder"]
