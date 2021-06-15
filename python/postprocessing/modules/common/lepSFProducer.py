from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True


class lepSFProducer(Module):
    def __init__(self, muonSelectionTag, electronSelectionTag):

        '''
        if muonSelectionTag == "LooseWP_2016":
            mu_f = ["Mu_Trg.root", "Mu_ID.root", "Mu_Iso.root"]
            mu_h = [
                "IsoMu24_OR_IsoTkMu24_PtEtaBins/pt_abseta_ratio",
                "MC_NUM_LooseID_DEN_genTracks_PAR_pt_eta/pt_abseta_ratio",
                "LooseISO_LooseID_pt_eta/pt_abseta_ratio"
            ]
        if electronSelectionTag == "GPMVA90_2016":
            el_f = ["EGM2D_eleGSF.root", "EGM2D_eleMVA90.root"]
            el_h = ["EGamma_SF2D", "EGamma_SF2D"]
        '''

        if muonSelectionTag == "TightWP_2016":
            mu_f = ["Mu_RunBCDEFGH_SF_ID_2016_syst.root"]
            mu_h = ["NUM_TightID_DEN_genTracks_eta_pt"]

        if electronSelectionTag == "NoIsoMVA90_2016":
            el_f = ["EGM2D_RECO_SF_2016.root", "2016LegacyReReco_ElectronMVA90noiso_Fall17V2.root"]
            el_h = ["EGamma_SF2D", "EGamma_SF2D"]

        if muonSelectionTag == "TightWP_2017":
            mu_f = ["Muon_RunBCDEF_SF_ID_2017.root", "Muon_RunBCDEF_SF_ISO_2017.root"]
            mu_h = ["NUM_TightID_DEN_genTracks_pt_abseta", 'NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta']

        if electronSelectionTag == "IsoMVA90_2017":
            el_f = ["EGM2D_2017_passingRECO_highEt.root", "Electron_MVA90_2017.root"]
            el_h = ["EGamma_SF2D", "EGamma_SF2D"]

        if muonSelectionTag == "TightWP_2018":
            mu_f = ["Mu_RunABCD_SF_ID_2018_syst.root"]
            mu_h = ["NUM_TightID_DEN_TrackerMuons_pt_abseta_syst"]

        if electronSelectionTag == "IsoMVA90_2018":
            el_f = ["EGM2D_RECO_SF_2018.root", "2018_ElectronMVA90noiso.root"]
            el_h = ["EGamma_SF2D", "EGamma_SF2D"]


        mu_f = [
            "%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/leptonSF/"
            % os.environ['CMSSW_BASE'] + f for f in mu_f
        ]
        el_f = [
            "%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/leptonSF/"
            % os.environ['CMSSW_BASE'] + f for f in el_f
        ]
        
        self.mu_f = ROOT.std.vector(str)(len(mu_f))
        self.mu_h = ROOT.std.vector(str)(len(mu_f))
        for i in range(len(mu_f)):
            self.mu_f[i] = mu_f[i]
            self.mu_h[i] = mu_h[i]
        self.el_f = ROOT.std.vector(str)(len(el_f))
        self.el_h = ROOT.std.vector(str)(len(el_f))
        for i in range(len(el_f)):
            self.el_f[i] = el_f[i]
            self.el_h[i] = el_h[i]

        if "/LeptonEfficiencyCorrector_cc.so" not in ROOT.gSystem.GetLibraries():
            print("Load C++ Worker")
            ROOT.gROOT.ProcessLine(".L %s/src/PhysicsTools/NanoAODTools/python/postprocessing/helpers/LeptonEfficiencyCorrector.cc+" % os.environ['CMSSW_BASE'])

    def beginJob(self):
        self._worker_mu = ROOT.LeptonEfficiencyCorrector(self.mu_f, self.mu_h)
        self._worker_el = ROOT.LeptonEfficiencyCorrector(self.el_f, self.el_h)

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("Muon_effSF", "F", lenVar="nMuon")
        self.out.branch("Electron_effSF", "F", lenVar="nElectron")
        self.out.branch("Muon_effSF_errUp", "F", lenVar="nMuon")
        self.out.branch("Electron_effSF_errUp", "F", lenVar="nElectron")
        self.out.branch("Muon_effSF_errDown", "F", lenVar="nMuon")
        self.out.branch("Electron_effSF_errDown", "F", lenVar="nElectron")
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        muons = Collection(event, "Muon")
        electrons = Collection(event, "Electron")
        sf_el = [
            self._worker_el.getSF(el.pdgId, el.pt, el.eta) for el in electrons
        ]
        sf_mu = [
            self._worker_mu.getSF(mu.pdgId, mu.pt, mu.eta) for mu in muons
        ]
        sferr_el = [ self._worker_el.getSFErr(el.pdgId,el.pt,el.eta) for el in electrons ]
        sferr_mu = [ self._worker_mu.getSFErr(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
        self.out.fillBranch("Muon_effSF", sf_mu)
        self.out.fillBranch("Electron_effSF", sf_el)
        self.out.fillBranch("Muon_effSF_errUp", [errsf + sf for errsf, sf in zip(sferr_mu, sf_mu)])
        self.out.fillBranch("Electron_effSF_errUp", [errsf + sf for errsf, sf in zip(sferr_el, sf_el)])
        self.out.fillBranch("Muon_effSF_errDown", [errsf - sf for errsf, sf in zip(sferr_mu, sf_mu)])
        self.out.fillBranch("Electron_effSF_errDown", [errsf - sf for errsf, sf in zip(sferr_el, sf_el)])
        return True


# define modules using the syntax 'name = lambda : constructor' to avoid
# having them loaded when not needed

lepSF_2016 = lambda : lepSFProducer("TightWP_2016", "NoIsoMVA90_2016")
lepSF_2017 = lambda : lepSFProducer("TightWP_2017", "IsoMVA90_2017")
lepSF_2018 = lambda : lepSFProducer("TightWP_2018", "NoIsoMVA90_2018")

#lepSF = lambda: lepSFProducer("LooseWP_2016", "GPMVA90_2016")
