import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection,Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class MET_HLT_Filter_Fake(Module):
    def __init__(self, year, trig="Lep"):
        self.year = year
        self.trig = trig
        pass
    def endJob(self):
        pass
    def beginJob(self):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        HLT = Object(event, "HLT")
        L1 = Object(event, "L1")
        flag = Object(event, 'Flag')
        good_MET = flag.goodVertices and flag.HBHENoiseFilter and flag.HBHENoiseIsoFilter and flag.EcalDeadCellTriggerPrimitiveFilter and flag.BadPFMuonFilter
        
        if(self.year == 2016):
            good_HLT = (HLT.Ele27_WPTight_Gsf or HLT.Ele32_WPTight_Gsf or HLT.IsoMu24 or HLT.IsoTkMu24) and flag.globalSuperTightHalo2016Filter
        elif(self.year == 2017):
            if self.trig == "Lep":
                good_HLT = HLT.Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30 or HLT.Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30 or HLT.Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 or HLT.Mu8_TrkIsoVVL or HLT.Mu17_TrkIsoVVL or HLT.Mu15_IsoVVVL_PFHT600
            elif self.trig == "Tau":
                good_HLT = HLT.IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1 or HLT.Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1 or HLT.MediumChargedIsoPFTau50_Trk30_eta2p1_1pr
            elif self.trig == "HT":
                good_HLT = HLT.PFHT250 or HLT.PFHT350 or HLT.PFHT370 or HLT.PFHT430 or HLT.PFHT510 or HLT.PFHT590 or HLT.PFHT680 or HLT.PFHT780 or HLT.PFHT890

        elif(self.year == 2018):
            if self.trig == "Lep":
                good_HLT = HLT.Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30 or HLT.Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30 or HLT.Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 or HLT.Mu8_TrkIsoVVL or HLT.Mu17_TrkIsoVVL or HLT.Mu15_IsoVVVL_PFHT600
            elif self.trig == "Tau":
                good_HLT = HLT.IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1 or HLT.Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1 or HLT.MediumChargedIsoPFTau50_Trk30_eta2p1_1pr
            elif self.trig == "HT":
                good_HLT = HLT.PFHT250 or HLT.PFHT350 or HLT.PFHT370 or HLT.PFHT430 or HLT.PFHT510 or HLT.PFHT590 or HLT.PFHT680 or HLT.PFHT780 or HLT.PFHT890

        else:
            print "Please specify the year: possible choices are 2016, 2017 or 2018"
        return good_MET and good_HLT

MET_HLT_Filter_Fake_2016 = lambda : MET_HLT_Filter_Fake(2016)
MET_HLT_Filter_Fake_2017_Lep = lambda : MET_HLT_Filter_Fake(2017, "Lep")
MET_HLT_Filter_Fake_2017_Tau = lambda : MET_HLT_Filter_Fake(2017, "Tau")
MET_HLT_Filter_Fake_2017_HT = lambda : MET_HLT_Filter_Fake(2017, "HT")
MET_HLT_Filter_Fake_2018_Lep = lambda : MET_HLT_Filter_Fake(2018, "Lep")
MET_HLT_Filter_Fake_2018_Tau = lambda : MET_HLT_Filter_Fake(2018, "Tau")
MET_HLT_Filter_Fake_2018_HT = lambda : MET_HLT_Filter_Fake(2018, "HT")

