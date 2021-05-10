import ROOT
import ROOT.TMath as TMath
import math
import cmath
import copy as copy
from os import path
import array
import types
from CutsAndValues_bu import *

ROOT.PyConfig.IgnoreCommandLineOptions = True

WP_btagger = {
  "CSVv2":{
    "L": 0.5803,
    "M": 0.8838,
    "T": 0.9693,
  },
  "DeepCSV":{
    "L": 0.1522,
    "M": 0.4941,
    "T": 0.8001,
  },
  "DeepFlv":{
    "L": 0.0521,
    "M": 0.3033,
    "T": 0.7489,
  },
}

effLumi_2017 = {
        "HT" : {
            "PFHT250"                       : 0.0147,
            "PFHT350"                       : 0.17,
            },
        "Ele" : {
            "Ele35_WPTight_Gsf"                     : 41.54,
            "Ele32_WPTight_Gsf_L1DoubleEG"          : 41.54,
            "Photon200"                             : 41.54,
            "Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30"   : 0.0038,
            "Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30"  : 0.0276,
            "Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30"  : 0.0434,
            },
        "Mu" : {
            "IsoMu27"                       : 41.54,
            "Mu50"                          : 41.54,
            "Mu8_TrkIsoVVL"                 : 0.0027,
            "Mu17_TrkIsoVVL"                : 0.0658,
            },
        }

sqrt = lambda x : TMath.Power(x, 0.5)
squared = lambda x : TMath.Power(x, 2.)

def lumiFinder(particleTrig, vTrigger):
    lumi=0
    for trigtype in effLumi_2017:
        if particleTrig==trigtype:
            for trig in vTrigger:
                effLumi=effLumi_2017[trigtype][trig]
                if effLumi>lumi: lumi=effLumi
    return lumi

def trig_finder(HLT, year, samplename):
    vTrigEle = []
    vTrigMu = []
    vTrigHT = []

    if (year == 2017):
        if HLT.IsoMu27:                                 vTrigMu.append("IsoMu27")
        if HLT.Mu50:                                    vTrigMu.append("Mu50")
        if HLT.Mu8_TrkIsoVVL:                           vTrigMu.append("Mu8_TrkIsoVVL")
        if HLT.Mu17_TrkIsoVVL:                          vTrigMu.append("Mu17_TrkIsoVVL")
        if HLT.Ele35_WPTight_Gsf:                       vTrigEle.append("Ele35_WPTight_Gsf")
        if HLT.Ele32_WPTight_Gsf_L1DoubleEG:            vTrigEle.append("Ele32_WPTight_Gsf_L1DoubleEG")
        if not ('DataMuB' in samplename or 'DataEleB' in samplename or 'DataHTB' in samplename):
            if HLT.Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30:     vTrigEle.append("Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30")
            if HLT.Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30:    vTrigEle.append("Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30")
            if HLT.Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30:    vTrigEle.append("Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30")
        if HLT.Photon200:                               vTrigEle.append("Photon200")
        if HLT.PFHT250:                                 vTrigHT.append("PFHT250")
        if HLT.PFHT350:                                 vTrigHT.append("PFHT350")
    
    else:
        print('Wrong year! Please enter 2017')
   
    return vTrigEle, vTrigMu, vTrigHT
    
       


def Chi_TopMass(mT):
  sigma = 28.8273
  mST = 174.729
  chi = ( TMath.Power((mST-mT), 2.) ) / ( TMath.Power(sigma, 2.))
  return chi

def Chi_W(mT):
  sigma = 0.012
  mST = 80.379
  chi = ( TMath.Power((mST-mT), 2.) ) / ( TMath.Power(sigma, 2.))
  return chi

###############################################
###         Begin of generic utils          ###   
###############################################
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch()        # don't pop up canvases                                                                                                                                              
ROOT.TH1.SetDefaultSumw2()
ROOT.TGaxis.SetMaxDigits(3)

colors = [ROOT.kBlue,
          ROOT.kBlack,
          ROOT.kRed,
          ROOT.kGreen+2,
          ROOT.kMagenta+2,
          ROOT.kAzure+6
]

#### ========= UTILITIES =======================
def deltaPhi(phi1,phi2):
    ## Catch if being called with two objects
    if type(phi1) != float and type(phi1) != int:
        phi1 = phi1.phi
    if type(phi2) != float and type(phi2) != int:
        phi2 = phi2.phi
    ## Otherwise
    dphi = (phi1-phi2)
    while dphi >  math.pi: dphi -= 2*math.pi
    while dphi < -math.pi: dphi += 2*math.pi
    return dphi

def deltaR(eta1,phi1,eta2=None,phi2=None):
    ## catch if called with objects
    if eta2 == None:
        return deltaR(eta1.eta,eta1.phi,phi1.eta,phi1.phi)
    ## otherwise
    return math.hypot(eta1-eta2, deltaPhi(phi1,phi2))

def doesOverlap(eta1, phi1, eta2, phi2):
    if deltaR(eta1, phi1, eta2, phi2)<0.4: return False
    return True

def FindSecondJet(jet, jetCollection, GoodTau, GoodMu):
    for k in range(len(jetCollection)):
        if abs(jetCollection[k].eta)>ETA_CUT_JET: continue
        if jetCollection[k].pt<PT_CUT_JET or jetCollection[k].jetId<2:
            return -1
        if abs(jet.eta-jetCollection[k].eta)>DELTAETA_JJ_CUT:
            if deltaR(jet.eta, jet.phi, GoodTau.eta, GoodTau.phi)>DR_OVERLAP_CONE_TAU or deltaR(jet.eta, jet.phi, GoodMu.eta, GoodMu.phi)>DR_OVERLAP_CONE_OTHER:
                return k
    return -1

def get_ptrel(lepton, jet):
    lepjet_tv = (jet.p4()+lepton.p4()).Vect()
    lep_tv = lepton.p4().Vect()
    ptrel = (lepjet_tv.Cross(lep_tv)).Mag()/(lepjet.Mag())
    return ptrel

def SelectLepton(lepCollection, isMu): #isMu==True -> muons else Ele 
    pT_cut=-999
    eta_cut=-999
    if isMu:
        pT_cut=PT_CUT_MU
        eta_cut=ETA_CUT_MU
    else:
        pT_cut=PT_CUT_ELE
        eta_cut=ETA_CUT_ELE
    for i in range(len(lepCollection)):
        if isMu:
            if not (lepCollection[i].tightId and (lepCollection[i].pfRelIso04_all<ISO_CUT_MU and lepCollection[i].pfRelIso04_all>=0.)):
                continue
        else:
            if not (lepCollection[i].mvaFall17V2Iso_WP90 and (lepCollection[i].jetRelIso<ISO_CUT_ELE and lepCollection[i].jetRelIso>=0.)):
                continue    
        if lepCollection[i].pt<pT_cut:
            continue
        if abs(lepCollection[i].eta)>eta_cut:
            continue 
        if not isMu and(abs(lepCollection[i].eta)>1.4442 and abs(lepCollection[i].eta)<1.566):
            continue
        return i, 1
    
    for i in range(len(lepCollection)):
        if abs(lepCollection[i].pdgId) == 13:
            if not (lepCollection[i].pfRelIso04_all>=ISO_CUT_MU and lepCollection[i].pfRelIso04_all<=1. and (not lepCollection[i].tightId and lepCollection[i].looseId)):
                continue
            if lepCollection[i].pt<PT_CUT_MU: continue
            if abs(lepCollection[i].eta)>ETA_CUT_MU: continue 
            return i, 0
        elif abs(lepCollection[i].pdgId) == 11:
            if not (lepCollection[i].mvaFall17V2Iso_WPL and not(lepCollection[i].mvaFall17V2Iso_WP90) and lepCollection[i].jetRelIso>=ISO_CUT_ELE and lepCollection[i].jetRelIso<=1.):
                continue
            if (abs(lepCollection[i].eta)>1.4442 and abs(lepCollection[i].eta)<1.566): continue
            if lepCollection[i].pt<PT_CUT_MU: continue
            if abs(lepCollection[i].eta)>ETA_CUT_ELE: continue 
            return i, 0
    return -1, -1


def SelectLooseLepton(lepCollection, isMu): #isMu==True -> muons else Ele 
    pT_cut=-999
    eta_cut=-999
    if isMu:
        pT_cut=PT_CUT_MU
        eta_cut=ETA_CUT_MU
    else:
        pT_cut=PT_CUT_ELE
        eta_cut=ETA_CUT_ELE
    for i in range(len(lepCollection)):
        if isMu:
          if not (lepCollection[i].looseId and not(lepCollection[i].tightId) and lepCollection[i].pfRelIso04_all<1 and lepCollection[i].pfRelIso04_all>=ISO_CUT_MU): continue
        else:
          if not (lepCollection[i].mvaFall17V2Iso_WPL and lepCollection[i].jetRelIso>=ISO_CUT_ELE and lepCollection[i].jetRelIso<1): continue    
        if lepCollection[i].pt<pT_cut: continue
        if abs(lepCollection[i].eta)>eta_cut: continue 
        if not isMu and(abs(lepCollection[i].eta)>1.4442 and abs(lepCollection[i].eta)<1.566): continue
        return i
    return -1

def SelectTau(tauCollection, GoodMuon, vsEleWP, vsMuWP, vsJetWP):
    #print('len taucollection : ', len(tauCollection))
    if len(tauCollection)<1:
        return -1, -999
    for i in range(len(tauCollection)):
        #print(i, "deltaR(tightlep):", deltaR(tauCollection[i].eta, tauCollection[i].phi, GoodMuon.eta, GoodMuon.phi), "DTvse:", tauCollection[i].idDeepTau2017v2p1VSe, "DTvsmu:", tauCollection[i].idDeepTau2017v2p1VSmu, "DTvsjet:", tauCollection[i].idDeepTau2017v2p1VSjet, "tau pt:", tauCollection[i].pt, "tau eta:", tauCollection[i].eta)
        if deltaR(tauCollection[i].eta, tauCollection[i].phi, GoodMuon.eta, GoodMuon.phi)<DR_OVERLAP_CONE_TAU:
            continue
        if not (tauCollection[i].idDeepTau2017v2p1VSe>=vsEleWP and tauCollection[i].idDeepTau2017v2p1VSmu>=vsMuWP and tauCollection[i].idDeepTau2017v2p1VSjet>=vsJetWP and tauCollection[i].idDecayModeNewDMs):   
            continue
        if tauCollection[i].pt<PT_CUT_TAU:
            continue
        if abs(tauCollection[i].eta)>ETA_CUT_TAU:
            continue
        return i, 1

    for i in range(len(tauCollection)):
        if deltaR(tauCollection[i].eta, tauCollection[i].phi, GoodMuon.eta, GoodMuon.phi)<DR_OVERLAP_CONE_TAU:
            continue
        if not (tauCollection[i].idDeepTau2017v2p1VSe>=vsEleWP and tauCollection[i].idDeepTau2017v2p1VSmu>=vsMuWP and tauCollection[i].idDeepTau2017v2p1VSjet>=4 and tauCollection[i].idDeepTau2017v2p1VSjet<vsJetWP and tauCollection[i].idDecayModeNewDMs):
            continue
        if tauCollection[i].pt<PT_CUT_TAU:
            continue
        if abs(tauCollection[i].eta)>ETA_CUT_TAU:
            continue
        return i, 0
     
    return -1, -999

def SelectAndVetoTaus(taus, lepton):
    nTau=0
    idxl = []
    if len(taus)==0:
        return 0, idxl
    for i, tau in enumerate(taus):
        #print(i, "deltaR(tightlep):", deltaR(tau.eta, tau.phi, lepton.eta, lepton.phi), "DTvse:", tau.idDeepTau2017v2p1VSe, "DTvsmu:", tau.idDeepTau2017v2p1VSmu, "DTvsjet:", tau.idDeepTau2017v2p1VSjet, "tau pt:", tau.pt, "tau eta:", tau.eta)
        #print(deltaR(tau.eta, tau.phi, lepton.eta, lepton.phi)>DR_OVERLAP_CONE_TAU, tau.idDeepTau2017v2p1VSe>=ID_TAU_RECO_DEEPTAU_VSELE, tau.idDeepTau2017v2p1VSmu>=ID_TAU_RECO_DEEPTAU_VSMU, tau.idDeepTau2017v2p1VSjet>=ID_TAU_RECO_DEEPTAU_VSJET_LOOSE, tau.pt>=PT_CUT_TAU, abs(tau.eta)<=ETA_CUT_TAU, tau.idDecayModeNewDMs)
        if abs(lepton.pdgId)==11:
            cutloose_vsjet = ID_TAU_RECO_DEEPTAU_VSJET_LOOSE_ELE
        elif abs(lepton.pdgId)==13:
            cutloose_vsjet = ID_TAU_RECO_DEEPTAU_VSJET_LOOSE_MU

        if (tau.idDeepTau2017v2p1VSjet>=cutloose_vsjet and tau.idDeepTau2017v2p1VSe>=ID_TAU_RECO_DEEPTAU_VSELE and tau.idDeepTau2017v2p1VSmu>=ID_TAU_RECO_DEEPTAU_VSMU and tau.idDecayModeNewDMs) and deltaR(tau.eta, tau.phi, lepton.eta, lepton.phi)>DR_OVERLAP_CONE_TAU and tau.pt>=PT_CUT_TAU and abs(tau.eta)<=ETA_CUT_TAU:
            nTau+=1

            if tau.idDeepTau2017v2p1VSjet>=ID_TAU_RECO_DEEPTAU_VSJET:
                idxl.append([i, "T"])
            else:
                idxl.append([i, "L"])
    if nTau!=1:
        return 0, idxl                                                                                                       
    else:
        return 1, idxl

def BVeto(jetCollection):
    veto = False
    for k in range(len(jetCollection)):
        if (jetCollection[k].btagDeepFlavB>=WP_btagger[BTAG_ALGO][BTAG_WP])*(jetCollection[k].pt>BTAG_PT_CUT)*abs(jetCollection[k].eta<BTAG_ETA_CUT):
            veto = True
            break
        else: continue
    return veto
        #if jetCollection[k].btagCSVV2<0.5803: continue #b-tag WP from https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X
        #if jetCollection[k].pt>30.: return True
    #return False

def CountBJets(jetCollection):
    nb=0
    #for k in range(len(jetCollection)):
    for jet in jetCollection:
        if jet.btagDeepFlavB>=WP_btagger[BTAG_ALGO][BTAG_WP] and jet.pt>BTAG_PT_CUT and abs(jet.eta)<BTAG_ETA_CUT: 
          nb+=1
    return nb


def IsNotTheSameObject(obj1, obj2):
    if obj1==obj2: return False
    return True
    

def LepVetoOneCollection(GoodLepton, collection, relIsoCut, ptCut, etaCut, isMu):
    i=0
    #print("relisocut:", relIsoCut)
    for i in range(len(collection)):
        lep=collection[i]
        veto = False
        '''
        if IsNotTheSameObject(GoodLepton, lep): 
            if isMu:
                print(i, "pdgId:", abs(lep.pdgId), "pt:", lep.pt, "iso", lep.pfRelIso04_all, "eta", lep.eta)
                if lep.pfRelIso04_all>=relIsoCut:#passa al prossimo se non passa la selezione loose su iso
                    continue
            else:
                print(i, "pdgId:", abs(lep.pdgId), "pt:", lep.pt, "iso", lep.jetRelIso, "eta", lep.eta)
                if lep.jetRelIso>=relIsoCut:#passa al prossimo se non passa la selezione loose su iso
                    continue
            if lep.pt<ptCut:#passa al prossimo se non passa la selezione loose su pt
                continue
            if abs(lep.eta)>etaCut:#passa al prossimo se non passa la selezione loose su eta
                continue
            veto = False
            return veto
        '''
        if IsNotTheSameObject(GoodLepton, lep): 
            if isMu:
                #print(i, "pdgId:", abs(lep.pdgId), "pt:", lep.pt, "iso", lep.pfRelIso04_all, "eta", lep.eta)
                if not (lep.pfRelIso04_all<relIsoCut and lep.pt>ptCut and abs(lep.eta)<etaCut and lep.looseId):
                    continue
            else:
                #print(i, "pdgId:", abs(lep.pdgId), "pt:", lep.pt, "iso", lep.jetRelIso, "eta", lep.eta)
                if not (lep.jetRelIso<relIsoCut and lep.pt>ptCut and abs(lep.eta)<etaCut and lep.mvaFall17V2Iso_WPL):
                    continue

            veto = False
            return veto

    veto = True
    return veto


    

def LepVeto(GoodLepton, ElectronCollection, MuonCollection):
    eleveto = LepVetoOneCollection(GoodLepton, ElectronCollection, REL_ISO_CUT_LEP_VETO_ELE, PT_CUT_LEP_VETO_ELE, ETA_CUT_LEP_VETO_ELE, False)
    muveto = LepVetoOneCollection(GoodLepton, MuonCollection, REL_ISO_CUT_LEP_VETO_MU, PT_CUT_LEP_VETO_MU, ETA_CUT_LEP_VETO_MU, True)
    print("eleveto:", eleveto, "muveto:", muveto)
    return bool(eleveto and muveto)

#semplifica la macro
def SelectJet(jetCollection, GoodTau, GoodMu):
    if len(jetCollection)<2:
        return -999
    if jetCollection[0].pt<PT_CUT_JET or jetCollection[0].jetId<2: return -999
    if jetCollection==None: return -999
    #select higher pT jet
    GoodJet=jetCollection[0]
    #if the jet matches in dR one of the previously selected particles (e, tau), than it searches in the other jets
    if deltaR(GoodJet.eta, GoodJet.phi, GoodTau.eta, GoodTau.phi)<DR_OVERLAP_CONE_TAU or deltaR(GoodJet.eta, GoodJet.phi, GoodMu.eta, GoodMu.phi)<DR_OVERLAP_CONE_OTHER: 
        jetCollection.remove(GoodJet)
        if len(jetCollection)==1:
             return -999
        return SelectJet(jetCollection, GoodTau, GoodMu)
    
    #searches for the best second jet
    secondJetIndex=FindSecondJet(GoodJet, jetCollection, GoodTau, GoodMu)
    if secondJetIndex>0: return GoodJet, jetCollection[secondJetIndex]
    else:
        jetCollection.remove(GoodJet)
        if len(jetCollection)==1:
            return -999
        else: return SelectJet(jetCollection, GoodTau, GoodMu)


def JetCut(jet1, jet2):
    if (jet1+jet2).M()<M_JJ_CUT: return True
    return False

def metCut(met):
    if met.pt<MET_CUT: return True
    return False

def mTlepMet(MET, lepton):
        return math.sqrt(2*lepton.Pt()*MET.pt*(1-math.cos(lepton.Phi()-MET.phi)))

def M1T(lep, tau, MET):
    leptau_p4 = lep.p4() + tau.p4()
    leptau_pt2 = leptau_p4.Perp2()
    leptau_px = leptau_p4.Px()
    leptau_py = leptau_p4.Py()
    leptau_mass2 = leptau_p4.M2()
    leptau_et = sqrt(leptau_mass2 + leptau_pt2)

    MET_px = MET.pt*TMath.Cos(MET.phi)
    MET_py = MET.pt*TMath.Sin(MET.phi)

    sys_et2 = squared(leptau_et + MET.pt)
    sys_pt2 = squared(leptau_px + MET_px) + squared(leptau_py + MET_py)
    M1T2 = sys_et2 - sys_pt2
    sign_M1T2 = M1T2/abs(M1T2)

    return sign_M1T2*sqrt(sign_M1T2*M1T2)

def Mo1(lep, tau, MET):
    leptau_p4 = lep.p4() + tau.p4()
    lep_pt = lep.pt
    tau_pt = tau.pt

    leptau_px = leptau_p4.Px()
    leptau_py = leptau_p4.Py()

    MET_px = MET.pt*TMath.Cos(MET.phi)
    MET_py = MET.pt*TMath.Sin(MET.phi)

    sys_eo2 = squared(lep_pt + tau_pt + MET.pt)
    sys_pt2 = squared(leptau_px + MET_px) + squared(leptau_py + MET_py)
    Mo12 = sys_eo2 - sys_pt2
    sign_Mo12 = Mo12/abs(Mo12)

    return sign_Mo12*sqrt(sign_Mo12*Mo12)

def Zeppenfeld(lep_eta, tau_eta, ljet_eta, sljet_eta):
    zepp_lepjj = lep_eta - 0.5*(ljet_eta+sljet_eta)
    zepp_taujj = tau_eta - 0.5*(ljet_eta+sljet_eta)
    zepp_event = 0.5*(zepp_lepjj+zepp_taujj)
    return zepp_lepjj, zepp_taujj, zepp_event

def closest(obj,collection,presel=lambda x,y: True):
    ret = None; drMin = 999
    for x in collection:
        if not presel(obj,x): continue
        dr = deltaR(obj,x)
        if dr < drMin: 
            ret = x; drMin = dr
    return (ret,drMin)

def matchObjectCollection(objs,collection,dRmax=0.4,presel=lambda x,y: True):
    pairs = {}
    if len(objs)==0:
        return pairs
    if len(collection)==0:
        return dict( list(zip(objs, [None]*len(objs))) )
    for obj in objs:
        ( bm, dR ) = closest(obj, [ mobj for mobj in collection if presel(obj,mobj) ])
        if dR < dRmax:
            pairs[obj] = bm
        else:
            pairs[obj] = None
    return pairs

def matchObjectCollectionMultiple(objs,collection,dRmax=0.4,presel=lambda x,y: True):
    pairs = {}
    if len(objs)==0:
        return pairs
    if len(collection)==0:
        return dict( list(zip(objs, [None]*len(objs))) )
    for obj in objs:
        matched = [] 
        for c in collection :
            if presel(obj,c) and deltaR( obj, c ) < dRmax :
                matched.append( c )
        pairs[obj] = matched
    return pairs

def pass_MET(flag): #returns the True if the event pass the MET Filter requiriments otherwise False
    return flag.goodVertices and flag.globalSuperTightHalo2016Filter and flag.HBHENoiseFilter and flag.HBHENoiseIsoFilter and flag.EcalDeadCellTriggerPrimitiveFilter and flag.BadPFMuonFilter

def bjet_filter(jets, tagger, WP): #returns collections of b jets and no b jets (discriminated with btaggers)
    # b-tag working points: mistagging efficiency tight = 0.1%, medium 1% and loose = 10% 
    WPbtagger = {'DeepFlv_T': 0.7264, 'DeepFlv_M': 0.2770, 'DeepFlv_L': 0.0494, 'DeepCSV_T': 0.7527, 'DeepCSV_M': 0.4184, 'DeepCSV_L': 0.1241}
    if(tagger == 'DeepFlv'):
        threshold = WPbtagger[str(tagger) + '_' + str(WP)]
        return list(filter(lambda x : x.btagDeepFlavB >= threshold, jets)), list(filter(lambda x : x.btagDeepFlavB < threshold, jets))
    elif(tagger == 'DeepCSV'):
        threshold = WPbtagger[str(tagger) + '_' + str(WP)]
        return list(filter(lambda x : x.btagDeepB >= threshold, jets)), list(filter(lambda x : x.btagDeepB < threshold, jets))
    else:
        print('Only DeepFlv and DeepCSV accepted! Pleae implement other taggers if you want them.')

def mcbjet_filter(jets): #returns a collection of only b-gen jets (to use only for MC samples)
    return list(filter(lambda x : x.partonFlavour == -5 or x.partonFlavour == 5, jets))

def sameflav_filter(jets, flav): #returns a collection of only b-gen jets (to use only forMC samples)                       
    return list(filter(lambda x : x.partonFlavour == flav, jets))

def get_HT(jets):
    HT = 0.
    for jet in jets:
        HT += jet.pt
    return HT

def trig_map(HLT, PV, year, runPeriod):
    isGoodPV = True#(PV.ndof>4 and abs(PV.z)<20 and math.hypot(PV.x, PV.y)<2) #basic requirements on the PV's goodness
    passMu = False#(PV.ndof>4 and abs(PV.z)<20 and math.hypot(PV.x, PV.y)<2) #basic requirements on the PV's goodness
    passEle = False#(PV.ndof>4 and abs(PV.z)<20 and math.hypot(PV.x, PV.y)<2) #basic requirements on the PV's goodness
    passHT = False#(PV.ndof>4 and abs(PV.z)<20 and math.hypot(PV.x, PV.y)<2) #basic requirements on the PV's goodness
    noTrigger = False#not(PV.ndof>4 and abs(PV.z)<20 and math.hypot(PV.x, PV.y)<2) #basic requirements on the PV's goodness
    
    if(year == 2016):# and runPeriod != 'H'):
        if(HLT.IsoMu24 or HLT.IsoTkMu24):
            passMu = True
        if(HLT.Ele27_WPTight_Gsf or HLT.Ele32_WPTight_Gsf):
            passEle = True
        if(HLT.PFHT250 or HLT.PFHT300):
            passHT = True
        if not(passMu or passEle) and not isGoodPV:
            noTrigger = True
    elif(year == 2017):#and runPeriod != 'B'):
        if(HLT.IsoMu27 or HLT.Mu50):#HLT.IsoMu24 or 
            passMu = True
        if(HLT.Ele35_WPTight_Gsf or HLT.Ele32_WPTight_Gsf_L1DoubleEG):# or HLT.Photon200):#HLT.Ele27_WPTight_Gsf or 
            passEle = True  
        if(HLT.PFHT250 or HLT.PFHT350 or HLT.PFHT370 or HLT.PFHT430 or HLT.PFHT510 or HLT.PFHT590 or HLT.PFHT680 or HLT.PFHT780 or HLT.PFHT890):
            passHT = True
        if not(passMu or passEle) and not isGoodPV:
            noTrigger = True
    elif(year == 2018):
        if(HLT.IsoMu24):
            passMu = True
        if(HLT.Ele32_WPTight_Gsf_L1DoubleEG):
            passEle = True  
        if not(passMu or passEle) and not isGoodPV:
            noTrigger = True
        if(HLT.PFHT250 or HLT.PFHT350):
            passHT = True
            
    else:
        print('Wrong year! Please enter 2016, 2017, or 2018')
   
    return (passMu and isGoodPV), (passEle and isGoodPV), (passHT and isGoodPV), noTrigger

def trig_map_all(HLT, PV, year, runPeriod):
    isGoodPV = True#(PV.ndof>4 and abs(PV.z)<20 and math.hypot(PV.x, PV.y)<2) #basic requirements on the PV's goodness
    passMu = False#(PV.ndof>4 and abs(PV.z)<20 and math.hypot(PV.x, PV.y)<2) #basic requirements on the PV's goodness
    passEle = False#(PV.ndof>4 and abs(PV.z)<20 and math.hypot(PV.x, PV.y)<2) #basic requirements on the PV's goodness
    passHT = False#(PV.ndof>4 and abs(PV.z)<20 and math.hypot(PV.x, PV.y)<2) #basic requirements on the PV's goodness
    noTrigger = False#not(PV.ndof>4 and abs(PV.z)<20 and math.hypot(PV.x, PV.y)<2) #basic requirements on the PV's goodness
    
    if(year == 2016):# and runPeriod != 'H'):
        if(HLT.IsoMu24 or HLT.IsoTkMu24):
            passMu = True
        if(HLT.Ele27_WPTight_Gsf or HLT.Ele32_WPTight_Gsf):
            passEle = True
        if(HLT.PFHT250 or HLT.PFHT300):
            passHT = True
        if not(passMu or passEle) and not isGoodPV:
            noTrigger = True
    elif(year == 2017):#and runPeriod != 'B'):
        if(HLT.IsoMu24 or HLT.IsoMu27 or HLT.IsoMu30 or HLT.Mu50):
            passMu = True
        if(HLT.Ele115_CaloIdVT_GsfTrkIdT or HLT.Ele27_WPTight_Gsf or HLT.Ele32_WPTight_Gsf or HLT.Ele35_WPTight_Gsf or HLT.Ele32_WPTight_Gsf_L1DoubleEG):# or HLT.Photon200):
            passEle = True  
        if(HLT.PFHT250 or HLT.PFHT350):
            passHT = True
        if not(passMu or passEle) and not isGoodPV:
            noTrigger = True
    elif(year == 2018):
        if(HLT.IsoMu24):
            passMu = True
        if(HLT.Ele32_WPTight_Gsf_L1DoubleEG):
            passEle = True  
        if not(passMu or passEle) and not isGoodPV:
            noTrigger = True
        if(HLT.PFHT250 or HLT.PFHT350):
            passHT = True
            
    else:
        print('Wrong year! Please enter 2016, 2017, or 2018')
   
    return (passMu and isGoodPV), (passEle and isGoodPV), (passHT and isGoodPV), noTrigger


def get_ptrel(lepton, jet):
    ptrel = ((jet.p4()-lepton.p4()).Vect().Cross(lepton.p4().Vect())).Mag()/(jet.p4().Vect().Mag())
    return ptrel

def print_hist(infile, plotpath, hist, option = "HIST", log = False, stack = False, title = ""):
    if not(isinstance(hist, list)):
        c1 = ROOT.TCanvas(infile + "_" + hist.GetName(), "c1", 50,50,700,600)
        hist.Draw(option)            
        c1.Print(plotpath + "/" + infile + "_" + hist.GetName() + ".png")
        c1.Print(plotpath + "/" + infile + "_" + hist.GetName() + ".root")
    elif isinstance(hist, list):
        c1 = ROOT.TCanvas(infile + "_" + hist[0].GetName(), "c1", 50,50,700,600)
        if not (infile == "") or len(hist) > 1:
            c1 = ROOT.TCanvas(infile + "_" + hist[0].GetName() + '_comparison', "c1", 50,50,700,600)
        else:
            c1_name = str(hist[0].GetName) + "_comparison"
            c1 = ROOT.TCanvas('comparison', "c1", 50,50,700,600)

        if isinstance(hist[0], ROOT.TGraph) or isinstance(hist[0], ROOT.TGraphAsymmErrors):
            i = 0
            mg = ROOT.TMultiGraph('mg', hist[0].GetTitle()+';'+hist[0].GetXaxis().GetTitle()+';'+hist[0].GetYaxis().GetTitle())
            for h in hist:
                h.SetLineColor(colors[i])
                mg.Add(h)
                i += 1
            print( mg)
            
            #cap = hist[0].GetXaxis().GetTitle()
            mg.SetMinimum(0.001)
            mg.Draw(option)
            Low = hist[0].GetXaxis().GetBinLowEdge(1)
            Nbin = hist[0].GetXaxis().GetNbins()
            High = hist[0].GetXaxis().GetBinUpEdge(Nbin)
            mg.GetXaxis().Set(Nbin, Low, High)
            
            for i in range(hist[0].GetXaxis().GetNbins()):
                u = i + 1
                mg.GetXaxis().SetBinLabel(u, hist[0].GetXaxis().GetBinLabel(u))
            
        elif isinstance(hist[0], ROOT.TEfficiency):
            i = 0
            mg = ROOT.TMultiGraph('mg', hist[0].GetTitle()+';'+hist[0].CreateGraph().GetXaxis().GetTitle()+';'+hist[0].CreateGraph().GetYaxis().GetTitle())

            for h in hist:
                print( h)
                h.SetLineColor(colors[i])
                mg.Add(h.CreateGraph())
                i += 1
            mg.SetMaximum(1.1)
            mg.SetMinimum(0.001)
            mg.Draw(option)
            
        elif isinstance(hist[0], ROOT.TH1F):
            mg = ROOT.THStack()
            i = 0
            print(hist[0].GetTitle(), hist[0].GetXaxis().GetTitle(), hist[0].GetYaxis().GetTitle())
            for h in hist:
                #h.SetLineColor(colors[i])
                if stack:
                    #h.SetFillColor(colors[i])
                    mg.Add(h)
                    i += 1
                else:
                  for h in hist:
                    h.Draw(option+'SAME')
            mg.Draw(option)
            mg.GetXaxis().SetTitle(hist[0].GetXaxis().GetTitle())
            mg.GetYaxis().SetTitle(hist[0].GetYaxis().GetTitle())
            if title == "":
                mg.SetTitle(hist[0].GetTitle()) 
            else:
                mg.SetTitle(title)
                
        #c1.Modified()
        #c1.Update()
        if log:
            c1.SetLogy(1)
        c1.Pad().Modified()
        c1.Pad().Update()
        c1.BuildLegend(0.7, 0.65, 0.95, 0.9)
        #c1.Modified()
        #c1.Update()
        c1.Pad().Modified()
        c1.Pad().Update()
        
        if not (infile == ""):
            c1.Print(plotpath + "/" + infile + "_" + hist[0].GetName() + '_comparison.png')
            c1.Print(plotpath + "/" + infile + "_" + hist[0].GetName() + '_comparison.root')
        else:
            c1.Print(plotpath + "/" + str(hist[0].GetName()) + '_comparison.png')
            c1.Print(plotpath + "/" + str(hist[0].GetName()) + '_comparison.root')

def save_hist(infile, plotpath, hist, option = "HIST"):
     fout = ROOT.TFile.Open(plotpath + "/" + infile +".root", "UPDATE")
     fout.cd()
     hist.Write()
     fout.Close()

def miniisoscan(isMu,threshold, lepton):
    for lepton in leptons:
        if(isMC and (lepton.genPartFlav == 1 or lepton.genPartFlav == 15)):
            totalMClep += 1.
            if (lepton.miniPFRelIso_all < threshold):
                if (lepton.pt > 50):
                    lepmatch_iso0p1_pt_50 += 1.
                if (lepton.pt > 75):
                    lepmatch_iso0p1_pt_75 += 1.
                if (lepton.pt > 100):
                    lepmatch_iso0p1_pt_100 += 1.
                if (lepton.pt > 125):
                    lepmatch_iso0p1_pt_125 += 1.
        if not(isMC and (lepton.genPartFlav == 1 or lepton.genPartFlav == 15)):
            totalnoMClep += 1.
            if (lepton.miniPFRelIso_all < threshold):
                if (lepton.pt > 50):
                    lepnomatch_iso0p1_pt_50 += 1.
                if (lepton.pt > 75):
                    lepnomatch_iso0p1_pt_75 += 1.
                if (lepton.pt > 100):
                    lepnomatch_iso0p1_pt_100 += 1.
                if (lepton.pt > 125):
                    lepnomatch_iso0p1_pt_125 += 1.
    return totalMClep,lepmatch_iso0p1_pt_50,lepmatch_iso0p1_pt_75,lepmatch_iso0p1_pt_100,lepmatch_iso0p1_pt_125,totalnoMClep,lepnomatch_iso0p1_pt_50,lepnomatch_iso0p1_pt_75,lepnomatch_iso0p1_pt_100,lepnomatch_iso0p1_pt_125

def HEMveto(jets, electrons):
  hemvetoetaup = -3.05
  hemvetoetadown = -1.35
  hemvetophiup = -1.62
  hemvetophidown = -0.82;
  passesMETHEMVeto = True

  for jet in jets:
    if(jet.eta>hemvetoetaup and jet.eta<hemvetoetadown and jet.phi>hemvetophiup and jet.phi<hemvetophidown):
      passesMETHEMVeto = False

  for ele in electrons:
    if(ele.eta>hemvetoetaup and ele.eta<hemvetoetadown and ele.phi>hemvetophiup and ele.phi<hemvetophidown):
      passesMETHEMVeto = False
 
  return passesMETHEMVeto

###############################################
###          End of generic utils           ###   
###############################################

###############################################
###         Begin of topreco_utils          ###   
###############################################
def EqSolv(a1, a2, a3, a4):
    if type(a1) != float and type(a1) != int:
        if type(a1) == list:
            a = a1[0]
            b = a1[1]
            c = a1[2]
            d = a1[3]
            result = []
        elif type(a1) == dict:
            a = a1['a']
            b = a1['b']
            c = a1['c']
            d = a1['d']
            result = {}
    else:
        a = a1
        b = a2
        c = a3
        d = a4
        result = []
    #print " a = %f, b = %f, c = %f, d = %f " %(a, b, c, d)
    if a != 0.:
        q = (3.*a*c - b*b)/(9.*a*a)
        r = (9.*a*b*c - 27.*a*a*d - 2.*b**3.)/(54.*a**3.)
        Delta = q**3. + r**2.
    
        #print " q = %f, r = %f, Delta = %f " %(q, r, Delta)
          
        if Delta <= 0: #da testare
            rho = (-(q**(3)))**(0.5)
            theta = math.acos(r/rho)
            s = cmath.rect((-q)**(0.5), theta/3.0)
            t = cmath.rect((-q)**(0.5), -theta/3.0)
        if Delta > 0:
            args = r+(Delta)**(0.5)
            argt = r-(Delta)**(0.5)
            signs = math.copysign(1, args)
            signt = math.copysign(1, argt)
            s = complex(signs*TMath.Power(abs(args), 1./3), 0)
            t = complex(signt*TMath.Power(abs(argt), 1./3), 0)
        
        rpar = b/(3.*a)
        x1 = s + t + complex(-rpar, 0)
        x2 = (s+t)*complex(-0.5, 0) - complex(rpar, 0) + (s-t)*(1j)*complex((3.**(0.5))/2., 0)
        x3 = (s+t)*complex(-0.5, 0) - complex(rpar, 0) - (s-t)*(1j)*complex((3.**(0.5))/2., 0)
        #print "  x1 = " + str(x1) + ", x2 = " + str(x2) + ", x3 =  " + str(x3)
        if abs(x1.imag)<0.0001:
            if type(a1)==dict:
                result.update({'x1': x1.real})
            else:
                result.append(x1.real)
        if abs(x2.imag)<0.0001:
            if type(a1)==dict:
                result.update({'x2': x2.real})
            else:
                result.append(x2.real)
        if abs(x3.imag)<0.0001:
            if type(a1)==dict:
                result.update({'x3': x3.real})
            else:
                result.append(x3.real)            
    else:
        result = None
    #print result
    return result

class TopUtilities():
    def __init__(self):
        if False:
            print('ok')

    def NuMomentum(self,  leptonPx, leptonPy, leptonPz, leptonPt, leptonE, metPx, metPy):
      mW = 80.379
      #print "\tutils NuMomentum: lPx=", leptonPx, " lPy=", leptonPy, " lPz", leptonPz, " lPt", leptonPt, " lE=", leptonE, " METPx=", metPx, " METPy=", metPy
      MisET2 = (metPx**2. + metPy**2.)
      mu = (mW**2.)/2. + metPx*leptonPx + metPy*leptonPy # this is the lambda factor
      a = mu*leptonPz/leptonPt**2
      a2 = a**2.
      b = (leptonE**2.*MisET2 - mu**2.)/leptonPt**2
      #print "+++++++++++++++++++++ MET2 is %f, mu is %f" %(MisET2, mu)
      #print "+++++++++++++++++++++ a is %f, a2 is %f and b is %f "%(a, a2, b)
      IsNegative = False
      
      p4nu_rec = None#ROOT.TLorentzVector()
      p4W_rec = ROOT.TLorentzVector()
      p4b_rec = ROOT.TLorentzVector()
      p4Top_rec = ROOT.TLorentzVector()
      p4lep_rec = ROOT.TLorentzVector()
      neutrino = None#ROOT.TLorentzVector()
      
      p4lep_rec.SetPxPyPzE(leptonPx, leptonPy, leptonPz, leptonE)
      p40_rec = ROOT.TLorentzVector(0.0, 0.0, 0.0, 0.0)
      
      delta = a2 - b
      #print "+++++++++++++++++++++ delta is %f" %delta

      if delta >= 0:
        root = cmath.sqrt((a2-b))
        pzs = []
        pzs.append((a + root).real)
        pzs.append((a - root).real)
        chi2w = 100000000.**2.
        
        for pz in pzs:
          Enu = TMath.Power((MisET2 + pz**2), 0.5)
          #Enu = TMath.Power((MisET2 + pznu**2), 0.5)
          p4nu = ROOT.TLorentzVector()
          p4nu.SetPxPyPzE(metPx, metPy, pz, Enu)
          #p4nu_rec.SetPxPyPzE(metPx, metPy, pznu, Enu)
          p4W = p4nu + p4lep_rec
          if Chi_W(p4W.M()) < chi2w:
            chi2w = Chi_W(p4W.M())
            p4nu_rec = copy.deepcopy(p4nu)
          
        neutrino = copy.deepcopy(p4nu_rec)
        
      elif delta < 0:
        IsNegative = True
        #print "negative delta"
        EquationCoeff1 = [1,
                          (-3 * leptonPy * mW / leptonPt),
                          (((mW**2.) * (2. * leptonPy**2.) / (leptonPt**2)) + mW**2. - (4. * leptonPx**3. * metPx / leptonPt**2) - (4. * leptonPx**2. * leptonPy * metPy / leptonPt**2)),
                          ((4. * leptonPx**2. * mW * metPy / leptonPt) - leptonPy * mW**3. / leptonPt)
                        ]

        EquationCoeff2 = copy.deepcopy(EquationCoeff1)
        EquationCoeff2[1] = - EquationCoeff2[1]
        EquationCoeff2[3] = - EquationCoeff2[3]
        #print " EquationCoeff1 is " + str(EquationCoeff1) + " and EquationCoeff2 is " + str(EquationCoeff2)
        solutions = [EqSolv(EquationCoeff1,'','',''), EqSolv(EquationCoeff2,'','','')]
        #print str(solutions)
        deltaMin = 14000.**2.
        zeroValue = - mW**2./(4.*leptonPx)
        minPx = 0.
        minPy = 0.

        ncoeff = ['x1', 'x2', 'x3']
        
        for j in range(2):
          for value in solutions[j]:
            if value < 0.:
              continue
            #usePxPlusSolutions_
            p_x = (value**2. - mW**2.) / (4.*leptonPx)
            p_y = ((mW**2.)*leptonPy + 2.*leptonPx*leptonPy*p_x - mW*leptonPt*value) / (2*leptonPx**2.)
            Delta2 = (p_x - metPx)**2. + (p_y - metPy)**2.
            #print "Solutions 1 p_x = %f, p_y = %f, Delta2 = %f" %(p_x, p_y, Delta2)
            if Delta2 < deltaMin and Delta2 > 0:
              deltaMin = copy.deepcopy(Delta2)
              minPx = copy.deepcopy(p_x)
              minPy = copy.deepcopy(p_y)

            #usePxMinusSolutions_
            p_x = (value**2. - mW**2.) / (4.*leptonPx)
            p_y = ((mW**2.)*leptonPy + 2.*leptonPx*leptonPy*p_x + mW*leptonPt*value) / (2*leptonPx**2.)
            Delta2 = (p_x - metPx)**2. + (p_y - metPy)**2.
            #print "Solutions 2 p_x = %f, p_y = %f, Delta2 = %f" %(p_x, p_y, Delta2)
            if Delta2 < deltaMin and Delta2 > 0:
              deltaMin = copy.deepcopy(Delta2)
              minPx = copy.deepcopy(p_x)
              minPy = copy.deepcopy(p_y)
            #print " Used solutions minp_x = %f, minp_y = %f, Delta2 = %f" %(minPx, minPy, deltaMin)
        pyZeroValue = mW**2.*leptonPx + 2.*leptonPx*leptonPy*zeroValue
        delta2ZeroValue = (zeroValue - metPx)**2. + (pyZeroValue - metPy)**2.

        #print "minp_x = %f, minp_y = %f, Deltamin = %f" %(minPx, minPy, deltaMin)
        #print " pyZeroValue = %f and delta2ZeroValue %f "%(pyZeroValue, delta2ZeroValue)
        if deltaMin == 14000.**2. :
          #neutrino = copy.deepcopy(p4nu_rec)
          #print "\tDelta2 too high!"
          neutrino = None
          #print "problem with neutrino reco!"
          return neutrino, IsNegative
          
        elif delta2ZeroValue < deltaMin :
              #print "\tDelta2 not so high!"
              deltaMin = copy.deepcopy(delta2ZeroValue)
              minPx = copy.deepcopy(zeroValue)
              minPy = copy.deepcopy(pyZeroValue)

        if not abs(leptonE) == abs(leptonPz):
          #print "\tleptonE != leptonPz"
          mu_Minimum = mW**2./2. + minPx*leptonPx + minPy*leptonPy
          a_Minimum = (mu_Minimum*leptonPz) / (leptonE**2. - leptonPz**2.)
          pznu = a_Minimum
          Enu = TMath.Power((minPx**2. + minPy**2. + pznu**2.), 0.5)
          p4nu = ROOT.TLorentzVector()
          #print " mu_Minimum = %f, a_Minimum = %f, pznu = %f, Enu= %f" %(mu_Minimum, a_Minimum, pznu, Enu )
          p4nu.SetPxPyPzE(minPx, minPy, pznu, Enu)
          p4nu_rec = copy.deepcopy(p4nu)
          neutrino = copy.deepcopy(p4nu_rec)
          #p4nu.SetPxPyPzE(minPx, minPy, pznu, Enu)
        else:
          #print "\tleptonE == leptonPz"
          neutrino = None#copy.deepcopy(p4nu_rec)
      #print " ********************* neutrino 4-momentum is (%f,%f,%f,%f) " %(neutrino.Pt(), neutrino.Eta(), neutrino.Phi(), neutrino.E())
      return neutrino, IsNegative

    def top4Momentum(self, lepton, jet, metPx, metPy):
        #topMt = self.topMtw(lepton, jet, metPx, metPy)
        '''
        if topMt == None:
        self.reco_topqv = None
        self.neutrino = None
        return None
        '''
        dR_lepjet = None
        dR_lepjet = deltaR(jet.Eta(), jet.Phi(), lepton.Eta(), lepton.Phi())
        #print "lepton inside top4momentum(begin) is (%f,%f,%f,%f) " %(lepton.Pt(),lepton.Eta(),lepton.Phi(),lepton.Energy())
        neutrino, IsNeg = self.NuMomentum(lepton.Px(), lepton.Py(), lepton.Pz(), lepton.Pt(), lepton.E(), metPx, metPy)
        besttop = None
        #recochi = []
        rtop = ROOT.TLorentzVector()

        if isinstance(neutrino, list):
          chi2 = 100000000.**2.
          for i in range(len(neutrino)):
            if dR_lepjet > 0.4:
              rtop = lepton + jet + neutrino[i]
            else:
              rtop = jet + neutrino[i]
            
            rchi = Chi_TopMass(rtop.M())
            if rchi < chi2:
              besttop = copy.deepcopy(rtop)
              chi2 = copy.deepcopy(rchi)
              dR_lepjet_top = copy.deepcopy(dR_lepjet)

        elif isinstance(neutrino, ROOT.TLorentzVector):
          if dR_lepjet > 0.4:
            rtop = lepton + jet + neutrino
            #print " lepton outside the jet!!!! its mass is %f" %rtop.M()
          else:
            rtop = jet + neutrino
            #print " lepton inside the jet!!!! its mass is %f" %rtop.M()
          rchi = Chi_TopMass(rtop.M())
          besttop = copy.deepcopy(rtop)
          dR_lepjet_top = copy.deepcopy(dR_lepjet)

        elif neutrino is None:
          besttop = None
          dR_lepjet_top = None
        #print "lepton inside top4momentum(end) is (%f,%f,%f,%f) " %(lepton.Pt(),lepton.Eta(),lepton.Phi(),lepton.Energy())

        return besttop, IsNeg, dR_lepjet_top

    def topMtw(self, lepton, jet, metPx, metPy):
        lb = lepton + jet
        mlb2 = lb.M2()
        ptlb = lb.Pt()
        pxlb = lb.Px()
        pylb = lb.Py() 
        '''
        if mlb2 < 0.:
            self.reco_topMt = None
            self.IsParticle = False
            return None
        '''
        etlb = TMath.Power((mlb2 + ptlb**2.), 0.5)
        metPt = TMath.Power((metPx**2. + metPy**2.), 0.5)

        return TMath.Power((mlb2 + 2.*(etlb*metPt - pxlb*metPx - pylb*metPy)), 0.5)

    def costhetapol(self, lepton, jet, top):
      #print "lepton inside costhetapol(begin) is (%f,%f,%f,%f) " %(lepton.Pt(),lepton.Eta(),lepton.Phi(),lepton.Energy())
      top_1 = ROOT.TLorentzVector()
      jet_copy = copy.deepcopy(jet)
      lepton_copy = copy.deepcopy(lepton)
      top_1.SetPxPyPzE(-top.Px(), -top.Py(), -top.Pz(), top.E())
      jet_copy.Boost(top.BoostVector())
      lepton_copy.Boost(top_1.BoostVector())
      costheta = (jet_copy.Vect()*lepton_copy.Vect())/((jet_copy.Vect()).Mag()*(lepton_copy.Vect()).Mag())
      #print "lepton inside costhetapol(end) is (%f,%f,%f,%f) " %(lepton.Pt(),lepton.Eta(),lepton.Phi(),lepton.Energy())
      return costheta

    def costhetapollep(self, lepton, top):
      #print "lepton inside costhetapollep(begin) is (%f,%f,%f,%f) " %(lepton.Pt(),lepton.Eta(),lepton.Phi(),lepton.Energy())
      lepton_copy = copy.deepcopy(lepton)
      top_1 = ROOT.TLorentzVector()
      top_1.SetPxPyPzE(-top.Px(), -top.Py(), -top.Pz(), top.E())
      lepton_copy.Boost(top_1.BoostVector())
      costheta = (top.Vect()*lepton_copy.Vect())/((top.Vect()).Mag()*(lepton_copy.Vect()).Mag())
      #print "lepton inside costhetapollep(end) is (%f,%f,%f,%f) " %(lepton.Pt(),lepton.Eta(),lepton.Phi(),lepton.Energy())
      return costheta

###############################################
###          End of topreco_utils           ###   
###############################################

###############################################
### Begin of framework/treeReaderArrayTools ###   
###############################################
def InputTree(tree,entrylist=ROOT.nullptr):
    """add to the PyROOT wrapper of a TTree a TTreeReader and methods readBranch, arrayReader, valueReader""" 
    if hasattr(tree, '_ttreereader'): return tree # don't initialize twice
    tree.entry = -1
    tree._entrylist = entrylist
    tree._ttreereader = ROOT.TTreeReader(tree,tree._entrylist)
    tree._ttreereader._isClean = True
    tree._ttrvs = {}
    tree._ttras = {}
    tree._leafTypes = {}
    tree._ttreereaderversion = 1
    tree.arrayReader = types.MethodType(getArrayReader, tree)
    tree.valueReader = types.MethodType(getValueReader, tree)
    tree.readBranch = types.MethodType(readBranch, tree)
    tree.gotoEntry = types.MethodType(_gotoEntry, tree)
    tree.readAllBranches = types.MethodType(_readAllBranches, tree)
    tree.entries = tree._ttreereader.GetEntries(False)
    tree._extrabranches={}
    return tree

def getArrayReader(tree, branchName):
    """Make a reader for branch branchName containing a variable-length value array."""
    if branchName not in tree._ttras:
       if not tree.GetBranch(branchName): raise RuntimeError("Can't find branch '%s'" % branchName)
       leaf = tree.GetBranch(branchName).GetLeaf(branchName)
       if not bool(leaf.GetLeafCount()): raise RuntimeError("Branch %s is not a variable-length value array" % branchName)
       typ = leaf.GetTypeName()
       tree._ttras[branchName] = _makeArrayReader(tree, typ, branchName)
    return tree._ttras[branchName]

def getValueReader(tree, branchName):
    """Make a reader for branch branchName containing a single value."""
    if branchName not in tree._ttrvs:
       if not tree.GetBranch(branchName): raise RuntimeError("Can't find branch '%s'" % branchName)
       leaf = tree.GetBranch(branchName).GetLeaf(branchName)
       if bool(leaf.GetLeafCount()) or leaf.GetLen()!=1 : raise RuntimeError("Branch %s is not a value" % branchName)
       typ = leaf.GetTypeName()
       tree._ttrvs[branchName] = _makeValueReader(tree, typ, branchName)
    return tree._ttrvs[branchName]

def clearExtraBranches(tree):
    tree._extrabranches = {}

def setExtraBranch(tree,name,val):
    tree._extrabranches[name] = val

def readBranch(tree, branchName):
    """Return the branch value if the branch is a value, and a TreeReaderArray if the branch is an array"""
    if tree._ttreereader._isClean: raise RuntimeError("readBranch must not be called before calling gotoEntry")
    if branchName in tree._extrabranches:
        return tree._extrabranches[branchName]
    elif branchName in tree._ttras:
        return tree._ttras[branchName]
    elif branchName in tree._ttrvs: 
        ret = tree._ttrvs[branchName].Get()[0]
        return ord(ret) if type(ret)==str else ret
    else:
        branch = tree.GetBranch(branchName)
        if not branch: raise RuntimeError("Unknown branch %s" % branchName)
        leaf = branch.GetLeaf(branchName)
        typ = leaf.GetTypeName()
        if leaf.GetLen() == 1 and not bool(leaf.GetLeafCount()): 
            _vr = _makeValueReader(tree, typ, branchName)
            tree.gotoEntry(tree.entry,forceCall=True) # force calling SetEntry as a new ValueReader was created
            ret = _vr.Get()[0]
            return ord(ret) if type(ret)==str else ret
        else:
            _ar = _makeArrayReader(tree, typ, branchName)
            tree.gotoEntry(tree.entry,forceCall=True) # force calling SetEntry as a new ArrayReader was created
            return _ar

####### PRIVATE IMPLEMENTATION PART #######

def _makeArrayReader(tree, typ, nam):
    if not tree._ttreereader._isClean: _remakeAllReaders(tree)
    ttra = ROOT.TTreeReaderArray(typ)(tree._ttreereader, nam)
    tree._leafTypes[nam] = typ
    tree._ttras[nam] = ttra;
    return tree._ttras[nam]

def _makeValueReader(tree, typ, nam):
    if not tree._ttreereader._isClean: _remakeAllReaders(tree)
    ttrv = ROOT.TTreeReaderValue(typ)(tree._ttreereader, nam)
    tree._leafTypes[nam] = typ
    tree._ttrvs[nam] = ttrv
    return tree._ttrvs[nam]

def _remakeAllReaders(tree):
    _ttreereader = ROOT.TTreeReader(tree, getattr(tree, '_entrylist', None))
    _ttreereader._isClean = True
    _ttrvs = {}
    for k in tree._ttrvs.keys():
        _ttrvs[k] = ROOT.TTreeReaderValue(tree._leafTypes[k])(_ttreereader,k)
    _ttras = {}
    for k in tree._ttras.keys():
        _ttras[k] = ROOT.TTreeReaderArray(tree._leafTypes[k])(_ttreereader,k)
    tree._ttrvs = _ttrvs
    tree._ttras = _ttras
    tree._ttreereader = _ttreereader
    tree._ttreereaderversion += 1

def _readAllBranches(tree):
    tree.GetEntry(_currentTreeEntry(tree))

def _currentTreeEntry(tree):
    if tree._entrylist:
        return tree._entrylist.GetEntry(tree.entry)
    else:
        return tree.entry

def _gotoEntry(tree, entry, forceCall=False):
    tree._ttreereader._isClean = False
    if tree.entry != entry or forceCall:
        if (tree.entry == entry-1 and entry!=0):
            tree._ttreereader.Next()
        else:
            tree._ttreereader.SetEntry(entry)
        tree.entry = entry
###############################################
###  End of framework/treeReaderArrayTools  ###
###############################################

###############################################
###      Begin of framework/datamodel       ###
###############################################
class Event:
    """Class that allows seeing an entry of a PyROOT TTree as an Event"""
    def __init__(self,tree,entry):
        self._tree = tree
        self._entry = entry
        self._tree.gotoEntry(entry)
    def __getattr__(self,name):
        if name in self.__dict__: return self.__dict__[name]
        return self._tree.readBranch(name)
    def __getitem__(self,attr):
        return self.__getattr__(attr)
    def eval(self,expr):
        """Evaluate an expression, as TTree::Draw would do. 

           This is added for convenience, but it may perform poorly and the implementation is not bulletproof,
           so it's better to rely on reading values, collections or objects directly
        """ 
        if not hasattr(self._tree, '_exprs'):
            self._tree._exprs = {}
            # remove useless warning about EvalInstance()
            import warnings
            warnings.filterwarnings(action='ignore', category=RuntimeWarning, 
                                    message='creating converter for unknown type "const char\*\*"$')
            warnings.filterwarnings(action='ignore', category=RuntimeWarning, 
                                    message='creating converter for unknown type "const char\*\[\]"$')
        if expr not in self._tree._exprs:
            formula = ROOT.TTreeFormula(expr,expr,self._tree)
            if formula.IsInteger():
                formula.go = formula.EvalInstance64
            else:
                formula.go = formula.EvalInstance
            self._tree._exprs[expr] = formula
            # force sync, to be safe
            self._tree.GetEntry(self._entry)
            self._tree.entry = self._entry
            #self._tree._exprs[expr].SetQuickLoad(False)
        else:
            self._tree.gotoEntry(entry)
            formula = self._tree._exprs[expr]
        if "[" in expr: # unclear why this is needed, but otherwise for some arrays x[i] == 0 for all i > 0
            formula.GetNdata()
        return formula.go()

class Object:
    """Class that allows seeing a set branches plus possibly an index as an Object"""
    def __init__(self,event,prefix,index=None):
        self._event = event
        if not (prefix == 'LHEPdfWeight' or prefix == 'LHEScaleWeight' or prefix == 'PSWeight'):
            self._prefix = prefix+"_"
        else:
            self._prefix = prefix
        self._index = index
    def __getattr__(self,name):
        if name in self.__dict__: return self.__dict__[name]
        if name[:2] == "__" and name[-2:] == "__":
            raise AttributeError
        val = getattr(self._event,self._prefix+name)
        if self._index != None:
            val = val[self._index]
        val = ord(val) if type(val)==str else val # convert char to integer number
        self.__dict__[name] = val ## cache
        return val
    def __getitem__(self,attr):
        return self.__getattr__(attr)
    def p4(self):
        ret = ROOT.TLorentzVector()
        ret.SetPtEtaPhiM(self.pt,self.eta,self.phi,self.mass)
        return ret
    def DeltaR(self,other):
        if isinstance(other,ROOT.TLorentzVector):
          deta = abs(other.Eta()-self.eta)
          dphi = abs(other.Phi()-self.phi)
        else:
          deta = abs(other.eta-self.eta)
          dphi = abs(other.phi-self.phi)
        while dphi > math.pi:
          dphi = abs(dphi - 2*math.pi)
        return math.sqrt(dphi**2+deta**2)
    def subObj(self,prefix):
        return Object(self._event,self._prefix+prefix)
    def __repr__(self):
        return ("<%s[%s]>" % (self._prefix[:-1],self._index)) if self._index != None else ("<%s>" % self._prefix[:-1])
    def __str__(self):
        return self.__repr__()

class Collection:
    def __init__(self,event,prefix,lenVar=None):
        self._event = event
        self._prefix = prefix
        if lenVar != None:
            self._len = getattr(event,lenVar)
        else:
            self._len = getattr(event,"n"+prefix)
        self._cache = {}
    def __getitem__(self,index):
        if type(index) == int and index in self._cache: return self._cache[index]
        if index >= self._len: raise IndexError("Invalid index %r (len is %r) at %s" % (index,self._len,self._prefix))
        ret = Object(self._event,self._prefix,index=index)
        if type(index) == int: self._cache[index] = ret
        return ret
    def __len__(self):
        return self._len
###############################################
###        End of framework/datamodel       ###
###############################################

###############################################
###       Begin of tree_skimmer_utlis       ###
###############################################
def pytocpptypes(typ):
    if type(typ) == int:
        return "/I"
    elif type(typ) == float:
        return "/F"
    elif type(typ) == str:
        return "/C"
    elif type(typ) == array.array:
        single = pytocpptypes(typ[0])
        return "[" + str(len(typ)) + "]" + single

class systWeights(object):

    def __init__(self):
        self.onlyNominal = True
        self.addPDF = False
        self.addQ2 = False
        self.addTopPt = False
        self.addVHF = False
        self.addTTSplit = False
        self.maxSysts = 0
        self.maxSystsNonPDF = 0
        self.shortPDFFiles = False
        self.isData = False
        self.nPDF = 0
        self.nCategories = 0
        self.nSelections = 0
        self.nEventBasedSysts = 0
        self.weightedSysts = []
        for i in range(150):
            self.weightedSysts.append(array.array('f', [0.]))
        self.eventBasedScenario = ""
        self.wCats = []
        for i in range(10):
            self.wCats.append(array.array('f', [0.]))
        self.eventBasedNames = []
        for i in range(10):
            self.eventBasedNames.append("")
        self.baseSelections = []
        for i in range(20):
            self.baseSelections.append(array.array('i', [0]))
        self.weightedNames = []
        for i in range(150):
            self.weightedNames.append("")
        self.selectionsNames = []
        for i in range(20):
            self.selectionsNames.append("")
        self.categoriesNames = []
        for i in range(10):
            self.categoriesNames.append("")

    def initTreesSysts(self, trees, tfile):
        tfile.cd()

        for s in range(self.nSelections):
            trees[s] = ROOT.TTree(str("events_"+self.selectionsNames[s]), "")
            isEventBasedSelection = self.isEventBasedSelection(s)
            #print trees[s], isEventBasedSelection
            self.initTreesSysts2S(trees[s], isEventBasedSelection)
            
    def initTreesSysts2S(self, tree, isEventBasedSyst):
        isEventBasedSyst = False
        Max = self.maxSysts
        if self.shortPDFFiles:
            Max = self.maxSystsNonPDF
        for sy in range(Max):
            if isEventBasedSyst and sy > 0:
                continue
            ns = str(self.weightedNames[sy])
            if sy == 0:
                ns = "w_nominal"
            #print "Branch: ", ns
            tystring = str(ns + pytocpptypes(self.weightedSysts[int(sy)]))
            tree.Branch(ns, self.weightedSysts[int(sy)], tystring)
        for c in range(self.nCategories):         
            cname = str(self.categoriesNames[c])
            tystring = str(cname + pytocpptypes(self.wCats[c]))
            #print "Branch: ", ns
            if c > 1: tree.Branch(cname, self.wCats[c], tystring)

    def addSelection(self, selection):
        self.selectionsNames[self.nSelections] = (str(selection))
        initSelection = self.nSelections
        self.nSelections += 1
        for sc in range(self.nEventBasedSysts):
            self.selectionsNames[self.nSelections] = (str(selection) + "_" + str(self.eventBasedNames[sc]))
            self.baseSelections[self.nSelections][0] = initSelection
            self.nSelections += 1

    def setSelectionsNames(self, selections):
        for s in range(self.nSelections):
            if s < (len(self.selectionNames) - 1):
                self.selectionsNames[s] = copy.deepcopy(selections[s])
            else:
                self.selectionsNames[s] = copy.deepcopy(selections[s])

    def branchTreesSysts(self, trees, selection, name, tfile, f):
        tfile.cd()
        tname = ROOT.TString(name)
        for s in range(self.nSelections):
            #print " selection # ", str(s), " name ", str(self.selectionsNames[s]), " name ", str(tname)
            #print " tree is ", str(trees[s])
            tystring = str(name + pytocpptypes(f))
            if selection == self.selectionsNames[s]:
                trees[s].Branch(name, f, tystring)
            if self.isEventBasedSelection(s):
                if selection == self.selectionNames[self.baseSelections[s][0]] :
                    trees[s].Branch(name, f, tystring)

    def fillTreesSysts(self, trees, selection):
        for s in range(self.nSelections):
            if selection == self.selectionsNames[s] and not self.isEventBasedSelection(s) and self.eventBasedScenario == "nominal" :
                if isinstance(trees[s], ROOT.TTree):
                    trees[s].Fill()
            if self.isEventBasedSelection(s):
                if self.eventBasedScenario in self.selectionsNames[s] and selection == self.selectionsNames[self.baseSelections[s][0]]:
                    if isinstance(trees[s], ROOT.TTree):
                        trees[s].Fill()

    def writeTreesSysts(self, trees, tfile):
        tfile.cd()
        for s in range(self.nSelections):
            if isinstance(trees[s], ROOT.TTree):
                trees[s].Write()

    def prepareDefault(self, addDefault, addPDF, addQ2, addTopPt, addVHF, addTTSplit, numPDF=102):
        self.addPDF = copy.deepcopy(addPDF)
        self.addQ2 = copy.deepcopy(addQ2)
        self.addTopPt = copy.deepcopy(addTopPt)
        self.addVHF = copy.deepcopy(addVHF)
        self.addTTSplit = copy.deepcopy(addTTSplit)
        self.nPDF = copy.deepcopy(numPDF)
        self.nCategories = 1
        self.categoriesNames[0] = ""
        self.wCats[0] = array.array('f', [1.0])
        self.nSelections = 0 
        self.eventBasedScenario = "nominal"

        if addDefault:
            self.weightedNames[0] = "w_nominal"
            self.weightedNames[1] = "lepSF"
            self.weightedNames[2] = "lepUp"
            self.weightedNames[3] = "lepDown"
            self.weightedNames[4] = "puSF"
            self.weightedNames[5] = "puUp"
            self.weightedNames[6] = "puDown"
            self.weightedNames[7] = "PFSF"
            self.weightedNames[8] = "PFUp"
            self.weightedNames[9] = "PFDown"
            self.weightedNames[10] = "tau_vsjet_SF"
            self.weightedNames[11] = "tau_vsjet_Up"
            self.weightedNames[12] = "tau_vsjet_Down"
            self.weightedNames[13] = "tau_vsele_SF"
            self.weightedNames[14] = "tau_vsele_Up"
            self.weightedNames[15] = "tau_vsele_Down"
            self.weightedNames[16] = "tau_vsmu_SF"
            self.weightedNames[17] = "tau_vsmu_Up"
            self.weightedNames[18] = "tau_vsmu_Down"
            self.weightedNames[19] = "tauSF"
            self.weightedNames[20] = "tauUp"
            self.weightedNames[21] = "tauDown"
            self.weightedNames[22] = "TESSF"
            self.weightedNames[23] = "TESUp"
            self.weightedNames[24] = "TESDown"
            self.weightedNames[25] = "FESSF"
            self.weightedNames[26] = "FESUp"
            self.weightedNames[27] = "FESDown"
            '''
            self.weightedNames[10] = "btagSF"
            self.weightedNames[11] = "btagUp"
            self.weightedNames[12] = "btagDown"            
            self.weightedNames[13] = "btagShape"
            self.weightedNames[14] = "btagShapeUpCferr1"
            self.weightedNames[15] = "btagShapeUpCferr2"
            self.weightedNames[16] = "btagShapeUpJes"
            self.weightedNames[17] = "btagShapeUpLf"
            self.weightedNames[18] = "btagShapeUpLfStats1"
            self.weightedNames[19] = "btagShapeUpLfStats2"
            self.weightedNames[21] = "btagShapeUpHf"
            self.weightedNames[22] = "btagShapeUpHfStats1"
            self.weightedNames[23] = "btagShapeUpHfStats2"
            self.weightedNames[24] = "btagShapeDownCferr1"
            self.weightedNames[25] = "btagShapeDownCferr2"
            self.weightedNames[26] = "btagShapeDownJes"
            self.weightedNames[27] = "btagShapeDownLf"
            self.weightedNames[28] = "btagShapeDownLfStats1"
            self.weightedNames[29] = "btagShapeDownLfStats2"
            self.weightedNames[30] = "btagShapeDownHf"
            self.weightedNames[31] = "btagShapeDownHfStats1"
            self.weightedNames[32] = "btagShapeDownHfStats2"
            '''
            #self.weightedNames[1] = "btagUp"
            #self.weightedNames[2] = "btagDown"
            #self.weightedNames[3] = "mistagUp"
            #self.weightedNames[4] = "mistagDown"
            #self.weightedNames[10] = "isoDown"
            #self.weightedNames[11] = "trigUp"
            #self.weightedNames[12] = "trigDown"
            self.setMax(28)
            self.setMaxNonPDF(27)
            self.weightedNames[self.maxSysts] = ""

        if addQ2: 
            self.weightedNames[self.maxSysts] = "q2Up"
            self.weightedNames[self.maxSysts+1] = "q2Down"
            self.setMax(self.maxSysts+2)
            self.setMaxNonPDF(self.maxSystsNonPDF+2) 
            self.weightedNames[self.maxSysts] = ""

        if addTopPt:
            self.weightedNames[self.maxSysts] = "topPtWeightUp"
            self.weightedNames[self.maxSysts+1] = "topPtWeightDown"
            self.setMax(self.maxSysts+2)
            self.setMaxNonPDF(self.maxSystsNonPDF+2)
            self.weightedNames[self.maxSysts] = ""

        if addVHF:
            self.weightedNames[self.maxSysts]="VHFWeightUp"
            self.weightedNames[self.maxSysts+1] = "VHFWeightDown"
            self.setMax(self.maxSysts+2)
            self.setMaxNonPDF(self.maxSystsNonPDF+2)
            self.weightedNames[self.maxSysts] = ""

        if addTTSplit:
            self.nCategories = 4
            categoriesNames[1] = "TT0lep"
            categoriesNames[2] = "TT1lep"
            categoriesNames[3] = "TT2lep"
            self.wCats[1] = array.array('f', [1.0])
            self.wCats[2] = array.array('f', [1.0])
            self.wCats[3] = array.array('f', [1.0])

        if addPDF:
            self.weightedNames[self.maxSysts] = "pdf_totalUp"
            self.weightedNames[self.maxSysts+1] = "pdf_totalDown"
            self.weightedNames[self.maxSysts+2] = "pdf_asUp"
            self.weightedNames[self.maxSysts+3] = "pdf_asDown"
            self.weightedNames[self.maxSysts+4] = "pdf_zmUp"
            self.weightedNames[self.maxSysts+5] = "pdf_zmDown"
            self.setMax(self.maxSysts+6)
            self.setMaxNonPDF(self.maxSystsNonPDF+6)
            nPDF = self.nPDF
            for i in range(nPDF):
                ss = str(i+1)
                self.weightedNames[i+self.maxSysts] = "pdf" + str(ss)

            self.setMax(maxSysts+nPDF)
            self.weightedNames[self.maxSysts] = ""

    def addSyst(self, name):
        self.weightedNames[self.maxSysts] = copy.deepcopy(name)
        self.setMax(maxSysts+1)
        if "pdf" in name:
            self.setMaxNonPDF(maxSysts+1)
        self.weightedNames[self.maxSysts] = ""

    def addSystNonPDF(self, name):
        self.weightedNames[self.maxSystsNonPDF] = copy.deepcopy(name)
        self.setMaxNonPDF(self.maxSystsNonPDF+1)
        nPDF = self.nPDF
        for i in range(nPDF):
            ss = str(i+1)
            self.weightedNames[i+self.maxSystsNonPDF] = "pdf" + str(ss)
        self.setMax(self.maxSystsNonPDF+nPDF)
        self.weightedNames[self.maxSysts] = ""

    def addTopTagSF(self, name):
        up = name + "Up"
        down = name + "Down"
        self.addSystNonPDF(up)
        self.addSystNonPDF(down)

    def addWTagSF(self, name):
        up = name + "Up"
        down = name + "Down"
        self.addSystNonPDF(up)
        self.addSystNonPDF(down)

    def addTrigSF(self, name):
        up = name + "Up"
        down = name + "Down"
        self.addSystNonPDF(up)
        self.addSystNonPDF(down)

    def setTopTagSF(self, name, SF_nom, SF_up, SF_down, mult=True):
        zerofact = array.array('f', [1.0])
        if mult:
            zerofact = self.weightedSysts[0]
        up = name + "Up"
        down = name + "Down"
        valueup = SF_up/SF_nom
        valuedown = SF_down/SF_nom
        
        self.setSystValue(up, valueup*zerofact[0])
        self.setSystValue(down, valuedown*zerofact[0])

    def setWTagSF(self, name, SF_nom, SF_up, SF_down, mult=True):
        zerofact = array.array('f', [1.0])
        if mult:
           zerofact = self.weightedSysts[0]
        up = name+"Up"
        down = name+"Down"
        valueup = SF_up/SF_nom
        valuedown = SF_down/SF_nom

        self.setSystValue(up, valueup*zerofact[0])
        self.setSystValue(down, valuedown*zerofact[0])

    def setTrigSF(self, name, SF_nom, SF_up, SF_down, mult=True):
        zerofact = array.array('f', [1.0])
        if mult:
            zerofact = self.weightedSysts[0]
        up = name+"Up"
        down = name+"Down"
        valueup = SF_up/SF_nom
        valuedown = SF_down/SF_nom
        if SF_nom == 0:
            valueup = 0
            valuedown = 0

        self.setSystValue(up, valueup*zerofact[0])
        self.setSystValue(down, valuedown*zerofact[0])

    def setPDFWeights(self, wpdfs, xsections, numPDFs, wzero=1.0, mult=True):
        zerofact = array.array('f', [1.0])
        rms, mean = 0., 0.
        if mult:
            zerofact = self.weightedSysts[0]
        for i in range(numPDFs+1):
            if wzero != 0 and xsections[i] != 0:
                try:
                    pvalue = wpdfs[i] / (wzero*xsections[i])
                except math.isnan(pvalue):
                    pvalue = 1.
                self.setPDFValue(i, zerofact[0]*wpdfs[i]/(wzero*xsections[i]) )
                mean += pvalue
            else:
                self.setPDFValue(i, wzero)
        mean = mean / numPDFs

        for i in range(numPDFs):
            if wzero != 0 and xsections[i] != 0:
                try:
                    pvalue = wpdfs[i] / (wzero*xsections[i])
                except math.isnan(pvalue):
                    pvalue = 1.
                rms += (mean-pvalue) * (mean-pvalue)
            else:
                rms += 0.

        if self.shortPDFFiles:
            self.setSystValue("pdf_asUp", self.getPDFValue(self.nPDF-2.)/wzero)
            self.setSystValue("pdf_asDown", zerofact[0])
            self.setSystValue("pdf_zmUp", self.getPDFValue(self.nPDF-1.)/wzero)
            self.setSystValue("pdf_zmDown", zerofact[0])
            if math.isnan(rms):
                rms += 0.
            self.setSystValue("pdf_totalUp", zerofact[0]*(1.+rms))
            self.setSystValue("pdf_totalDown", zerofact[0]*(1.-rms))

    def setTWeight(self, tweight, wtotsample=1.0, mult=True):
        zerofact = array.array('f', [1.0])
        if mult:
            zerofact = self.weightedSysts[0]
        self.setSystValue("topPtWeightUp", zerofact[0]*tweight/wtotsample)
        self.setSystValue("topPtWeightDown", zerofact[0]/tweight*wtotsample)

    def setVHFWeight(self, vhf, mult=True, shiftval=0.65):
        zerofact = array.array('f', [1.0])
        w_shift = 0.0
        if vhf > 1:
            w_shift = shiftval
        if mult: 
            zerofact[0] = self.weightedSysts[0]
        
        self.setSystValue("VHFWeightUp", zerofact[0]*(1+w_shift))
        self.setSystValue("VHFWeightDown", zerofact[0]*(1-w_shift))

    def setQ2Weights(self, q2up, q2down, wzero=1.0, mult=True):
        zerofact = array.array('f', [1.0])
        if mult:
            zerofact[0] = self.weightedSysts[0]
  
        self.setSystValue("q2Up", zerofact[0]*q2up/wzero)
        self.setSystValue("q2Down", zerofact[0]*q2down/wzero)

    def getPDFValue(self, numPDF):
        if not self.addPDF:
            print("error! No PDF used, this will do nothing.")
            return 0.
        MIN = self.maxSystsNonPDF
        return float(self.weightedSysts[numPDF+MIN][0])

    def setPDFValue(self, numPDF, w):
        if not self.addPDF:
            print( "error! No PDF used, this will do nothing.")
            return
        MIN = self.maxSystsNonPDF
        self.weightedSysts[numPDF+MIN][0] = w

    
    def calcPDFHisto(self, histo, singleHisto, scalefactor=1.0, c=0):
        #EXPERIMENTAL                                                                     
        if not addPDF:
            print( "error! No PDF used, this will do nothing.")
            return
        MAX = self.maxSysts
        MIN = self.maxSystsNonPDF + (MAX+1)*c
        for b in range(singleHisto.GetNbinsX()):
            val = singleHisto.GetBinContent(b)
            mean = 0
            devst = 0
            for i in range(self.nPDF):
                mean = mean + histo[i+MIN].GetBinContent(b)
            mean = mean/self.nPDF
  
            for i in range(self.nPDF):
                devst += (mean-histo[i+MIN].GetBinContent(b))*(mean-histo[i+MIN].GetBinContent(b))
            devst= sqrt(devst/self.nPDF)
            singleHisto.SetBinContent(b,val+devst*scalefactor)
    
    def isEventBasedSelection(self, sy):
        isEventBased = False
        for e in range(self.nEventBasedSysts):
            if self.eventBasedNames[e] in self.selectionsNames[sy]:
                isEventBased = True
                return True
        return isEventBased

    def initHistogramsSysts(self, histo, name, title, nbins, Min, Max):
        for c in range(nCategories):
            MAX = self.maxSysts
            useOnlyNominal = self.onlyNominal
            cname = ROOT.TString(str(self.categoriesNames[c]))
            for sy in range(MAX):
                ns = ROOT.TSring(str(self.weightedNames[sy]))
                if sy == 0:
                    if c == 0:
                        histo[sy+((MAX+1)*c)] = ROOT.TH1F(name, title, nbins, Min, Max)
                    else:
                        histo[sy+((MAX+1)*c)] = ROOT.TH1F(name+"_"+cname, title, nbins, Min, Max)
      
                if sy != 0 and not useOnlyNominal:
                    if c == 0:
                        histo[sy+((MAX+1)*c)] = ROOT.TH1F(name+"_"+ns,title,nbins,Min,Max)
                    else:
                        histo[sy+((MAX+1)*c)] = ROOT.TH1F(name+"_"+ns+"_"+cname,title,nbins,Min,Max)
    
    def setOnlyNominal(self, useOnlyNominal=False):
        self.onlyNominal = copy.deepcopy(useOnlyNominal)
  
    def setWCats(self, wcats):
        for i in range(self.nCategories):
            arwcats = array.array('f', [wcats[i]])
            self.wCats[i] = copy.deepcopy(arwcats)
                
    def fillHistogramsSysts(self, histo, v, w, systWeights=[], wcats=None):
        nFirstSysts = len(systWeights)
        if wcats == None:
            wcats = copy.deecopy(self.wCats)
        for c in range(self.nCategories):
            MAX = self.maxSysts
            useOnlyNominal = self.onlyNominal
            for sy in range(MAX):
                if sy != 0 and useOnlyNominal:
                    continue
                ws = 1.0
                if sy < nFirstSysts:
                    wcats[c] = array.array('f', 1.0)
                    ws = systWeights[sy]*wcats[c][0]
                else:
                    if nFirstSysts != 0:
                        wcats[c] = array.array('f', 1.0)
                    ws = self.weightedSysts[sy][0]*wcats[c][0]

                histo[sy+(MAX+1)*(c)].Fill(v, w * ws)
                            
    def createFilesSysts(self, allFiles, basename, opt="RECREATE"):
        for c in range(self.nCategories):
            MAX = self.maxSystsNonPDF
            MAXTOT = self.maxSystsNonPDF
            useOnlyNominal = self.onlyNominal
            cname = str(self.categoriesNames[c])

            if c != 0:
                cname = "_" + cname
            for sy in range(MAX):
                ns = str(self.weightedNames[sy])
                print( " creating file for syst ", ns)

                if c != 0:
                    print( " category is ", str(c))
                    print( "onlynominal is ", useOnlyNominal)
                
                if sy == 0:
                    allFiles[sy+(MAX+1)*c] = ROOT.TFile.Open((basename+ns+cname+".root"), opt)
                else:
                    if not useOnlyNominal:
                        print( " filename is ", basename, ns, cname, ".root")
                        allFiles[sy+(MAX+1)*c] = ROOT.TFile.Open((basename+"_"+ns+cname+".root"), opt)
                        print( "ESCO dal create Sys ")

            if self.addPDF:
                if not useOnlyNominal:
                   allFiles[MAX+((MAX+1)*c)]= ROOT.TFile.Open((basename+"_pdf"+cname+".root"), opt)

    def writeHistogramsSysts(self, histo, filesout):
        MAX = self.maxSystsNonPDF
        MAXTOT = self.maxSysts
        useOnlyNominal = self.onlyNominal
        for c in range(self.nCategories):
            cname = ROOT.TString(str(self.categoriesNames[c]))
            if c != 0:
                cname = "_" + cname
                for sy in range(MAX):
                    if not (not useOnlyNominal or sy==0):
                        continue
                    filesout[sy+(MAX+1)*(c)].cd()
                    if self.addPDF:
                        if self.weightedNames[sy] == "pdf_totalUp":
                            calcPDFHisto(histo, histo[sy+(MAXTOT+1)*(c)], 1.0, c)
                        if self.weightedNames[sy] == "pdf_totalDown":
                           calcPDFHisto(histo, histo[sy+(MAXTOT+1)*(c)], -1.0, c)
                    histo[sy+(MAXTOT+1)*c].Write(histo[0].GetName())
                if self.addPDF:
                    if not useOnlyNominal:
                        filesout[MAX+(MAX+1)*(c)].cd()
                        MAXPDF = self.maxSysts
                        for sy in range(MAXPDF):
                            histo[sy+(MAXTOT+1)*(c)].Write()

    def writeSingleHistogramSysts(self, histo, filesout):
        MAX= self.maxSystsNonPDF
        useOnlyNominal = self.onlyNominal
        for c in range(self.nCategories):
            cname = ROOT.TString(str(self.categoriesNames[c]))
            if c != 0:
                cname= "_"+cname
            for sy in range(MAX):
                if not (not useOnlyNominal or sy == 0):
                    continue
                filesout[sy+(MAX+1)*c].cd()
                histo.Write()
            if self.addPDF:
                if not useOnlyNominal:
                    filesout[MAX+(MAX+1)*c].cd()
                    MAXPDF = self.maxSysts
                    for sy in range(MAXPDF):
                        histo.Write()

    def setMax(self, Max):
        self.maxSysts = copy.deepcopy(Max)

    def setMaxNonPDF(self, Max):
        self.maxSystsNonPDF = copy.deepcopy(Max)

    def setSystValueName(self, name, value, mult=False):
        zerofact = array.array('f', [1.0])
        if mult:
            zerofact = self.weightedSysts[0]
        MAX = self.maxSysts
        for sy in range(MAX):
            if self.weightedNames[sy] == name:
                self.weightedSysts[sy][0] = value*zerofact[0]

    def setSystValuePlace(self, place, value, mult=False):
        zerofact = array.array('f', [1.0])
        if mult:
            zerofact = self.weightedSysts[0]
        self.weightedSysts[place][0] = value*zerofact[0]

    def setWeightName(self, name, value, mult=False):
        self.setSystValueName(name, value, mult)

    def setWeightPlace(self, place, value, mult=False):
        self.setSystValuePlace(place, value, mult)

    def closeFilesSysts(self, filesout):
        MAX = self.maxSystsNonPDF
        useOnlyNominal = self.onlyNominal
        for c in range(self.nCategories):
            cname = ROOT.TString(str(self.categoriesNames[c]))
            if c != 0:
                cname = "_" + cname

            for sy in range(MAX):
                if not (not useOnlyNominal or sy==0):
                    continue
                filesout[sy+(MAX+1)*(c)].Close()
            
            addPDF = self.addPDF
            if addPDF:
                if not useOnlyNominal:
                    filesout[MAX+(MAX+1)*(c)].Close()

###############################################
###        End of tree_skimmer_utlis        ###
###############################################

def Lepton_IDIso_SF(lepton):
    if abs(lepton.pdgId)==13:
        #print "It's a muon!"
        #f_muon_id = ROOT.TFile.Open("./data/leptonSF/Muon_RunBCDEF_SF_ID_2017.root", "READ")
        f_muon_id = ROOT.TFile.Open("Muon_RunBCDEF_SF_ID_2017.root", "READ")
        #f_muon_iso = ROOT.TFile.Open("./data/leptonSF/Muon_RunBCDEF_SF_ISO_2017.root", "READ")
        f_muon_iso = ROOT.TFile.Open("Muon_RunBCDEF_SF_ISO_2017.root", "READ")

        h_muon_id = ROOT.TH2D(f_muon_id.Get("NUM_TightID_DEN_genTracks_pt_abseta"))
        h_muon_iso = ROOT.TH2D(f_muon_iso.Get("NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta"))
      
        pt = lepton.pt
        abseta = abs(lepton.eta)
        binx_id = h_muon_id.GetXaxis().FindBin(pt)
        biny_id = h_muon_id.GetYaxis().FindBin(abseta)
        nxbins_id = h_muon_id.GetXaxis().GetNbins()
        nybins_id = h_muon_id.GetYaxis().GetNbins()
        if binx_id > nxbins_id:
            binx_id = copy.deepcopy(nxbins_id)
        elif binx_id <= 0:
            binx_id = 1
        if biny_id > nybins_id:
            biny_id = copy.deepcopy(nybins_id)
        elif biny_id <= 0:
            biny_id = 1

        binx_iso = h_muon_iso.GetXaxis().FindBin(pt)
        biny_iso = h_muon_iso.GetYaxis().FindBin(abseta)
        nxbins_iso = h_muon_iso.GetXaxis().GetNbins()
        nybins_iso = h_muon_iso.GetYaxis().GetNbins()
        if binx_iso > nxbins_iso:
            binx_iso = copy.deepcopy(nxbins_iso)
        elif binx_iso <= 0:
            binx_iso = 1
        if biny_iso > nybins_iso:
            biny_iso = copy.deepcopy(nybins_iso)
        elif biny_iso <= 0:
            biny_iso = 1
        
        SF_muon_id = copy.deepcopy(h_muon_id.GetBinContent(binx_id, biny_id))
        SF_muon_iso = copy.deepcopy(h_muon_iso.GetBinContent(binx_iso, biny_iso))

        f_muon_id.Close()
        f_muon_iso.Close()

        return SF_muon_id*SF_muon_iso

    elif abs(lepton.pdgId)==11:
        #print "It's a electron!"
        #f_electron_id = ROOT.TFile.Open("./data/leptonSF/Electron_MVA90_2017.root", "READ")
        f_electron_id = ROOT.TFile.Open("Electron_MVA90_2017.root", "READ")
        h_electron_id = ROOT.TH2F(f_electron_id.Get("EGamma_SF2D"))

        if lepton.pt < 20.:
            #f_electron_reco = ROOT.TFile.Open("./data/leptonSF/EGM2D_2017_passingRECO_lowEt.root", "READ")
            f_electron_reco = ROOT.TFile.Open("EGM2D_2017_passingRECO_lowEt.root", "READ")
        elif lepton.pt >= 20.:
            #f_electron_reco = ROOT.TFile.Open("./data/leptonSF/EGM2D_2017_passingRECO_highEt.root", "READ")
            f_electron_reco = ROOT.TFile.Open("EGM2D_2017_passingRECO_highEt.root", "READ")
        h_electron_reco = ROOT.TH2F(f_electron_reco.Get("EGamma_SF2D"))

        pt = lepton.pt
        eta = lepton.eta
        biny_id = h_electron_id.GetXaxis().FindBin(pt)
        binx_id = h_electron_id.GetYaxis().FindBin(eta)
        nxbins_id = h_electron_id.GetXaxis().GetNbins()
        nybins_id = h_electron_id.GetYaxis().GetNbins()
        if binx_id > nxbins_id:
            binx_id = copy.deepcopy(nxbins_id)
        elif binx_id <= 0:
            binx_id = 1
        if biny_id > nybins_id:
            biny_id = copy.deepcopy(nybins_id)
        elif biny_id <= 0:
            biny_id = 1

        biny_reco = h_electron_reco.GetXaxis().FindBin(pt)
        binx_reco = h_electron_reco.GetYaxis().FindBin(eta)
        nxbins_reco = h_electron_reco.GetXaxis().GetNbins()
        nybins_reco = h_electron_reco.GetYaxis().GetNbins()
        if binx_reco > nxbins_reco:
            binx_reco = copy.deepcopy(nxbins_reco)
        elif binx_reco <= 0:
            binx_reco = 1
        if biny_reco > nybins_reco:
            biny_reco = copy.deepcopy(nybins_reco)
        elif biny_reco <= 0:
            biny_reco = 1


        SF_electron_id = copy.deepcopy(h_electron_id.GetBinContent(binx_id, biny_id))
        SF_electron_reco = copy.deepcopy(h_electron_reco.GetBinContent(binx_reco, biny_reco))

        f_electron_id.Close()
        f_electron_reco.Close()

        return SF_electron_id*SF_electron_reco

    else:
        print("I dunno what to do with this particle :/")
        return -1.

def SFFakeRatio_ele_calc(pT, eta, wp = 'vsjet2'):
    #inFile = ROOT.TFile.Open("FR_vsjet2.root")
    if wp == 'vsjet2':
        inFile = ROOT.TFile.Open("FR_vsjet2_vsmuT.root")
    elif wp == 'vsjet4':
        inFile = ROOT.TFile.Open("FR_vsjet4_vsmuT.root")
    #if prompt:
    histo=ROOT.TH2F(inFile.Get("hFRDataeledif"))
    #else:
    #histo=ROOT.TH2F(inFile.Get("hFRDataele"))
    FR=0

    binx = histo.GetXaxis().FindBin(pT)
    biny = histo.GetYaxis().FindBin(eta)
    nxbins = histo.GetXaxis().GetNbins()
    nybins = histo.GetYaxis().GetNbins()
    if binx > nxbins:
        binx = copy.deepcopy(nxbins)
    elif binx <= 0:
        binx = 1
    if biny > nybins:
        biny = copy.deepcopy(nybins)
    elif biny <= 0:
        biny = 1

    FR = copy.deepcopy(histo.GetBinContent(binx, biny))

    '''
    if(pT<=20):
        if(abs(eta)<1):         FR=histo.GetBinContent(1,1)
        elif(abs(eta)<1.5):     FR=histo.GetBinContent(1,2)
        elif(abs(eta)<2):       FR=histo.GetBinContent(1,3)
        elif(abs(eta)<2.4):     FR=histo.GetBinContent(1,4)
    elif(pT<=30):
        if(abs(eta)<1):         FR=histo.GetBinContent(2,1)
        elif(abs(eta)<1.5):     FR=histo.GetBinContent(2,2)
        elif(abs(eta)<2):       FR=histo.GetBinContent(2,3)
        elif(abs(eta)<2.4):     FR=histo.GetBinContent(2,4)
    elif(pT<=40):
        if(abs(eta)<1):         FR=histo.GetBinContent(3,1)
        elif(abs(eta)<1.5):     FR=histo.GetBinContent(3,2)
        elif(abs(eta)<2):       FR=histo.GetBinContent(3,3)
        elif(abs(eta)<2.4):     FR=histo.GetBinContent(3,4)
    elif(pT<=50):
        if(abs(eta)<1):         FR=histo.GetBinContent(4,1)
        elif(abs(eta)<1.5):     FR=histo.GetBinContent(4,2)
        elif(abs(eta)<2):       FR=histo.GetBinContent(4,3)
        elif(abs(eta)<2.4):     FR=histo.GetBinContent(4,4)
    elif(pT>50):
        if(abs(eta)<1):         FR=histo.GetBinContent(5,1)
        elif(abs(eta)<1.5):     FR=histo.GetBinContent(5,2)
        elif(abs(eta)<2):       FR=histo.GetBinContent(5,3)
        elif(abs(eta)<2.4):     FR=histo.GetBinContent(5,4)
    else: FR=0
    '''

    return FR/(1-FR)

def SFFakeRatio_tau_calc(pT, eta, wp ='vsjet2'):
    histo = ROOT.TH2F()
    #inFile = ROOT.TFile.Open("FR_vsjet2.root")
    if wp == 'vsjet2':
        inFile = ROOT.TFile.Open("FR_vsjet2_vsmuT.root")
    elif wp == 'vsjet4':
        inFile = ROOT.TFile.Open("FR_vsjet4_vsmuT.root")
    #if prompt:
    histo=(ROOT.TH2F)(inFile.Get("hFRDatataudif"))
    #else:
    #histo=(ROOT.TH2F)(inFile.Get("hFRDatatau"))

    FR=0

    binx = histo.GetXaxis().FindBin(pT)
    biny = histo.GetYaxis().FindBin(abs(eta))
    nxbins = histo.GetXaxis().GetNbins()
    nybins = histo.GetYaxis().GetNbins()
    if binx > nxbins:
        binx = copy.deepcopy(nxbins)
    elif binx <= 0:
        binx = 1
    if biny > nybins:
        biny = copy.deepcopy(nybins)
    elif biny <= 0:
        biny = 1

    FR = copy.deepcopy(histo.GetBinContent(binx, biny))

    '''
    if(pT<=20):
        if(abs(eta)<1):         FR=histo.GetBinContent(1,1)
        elif(abs(eta)<1.5):     FR=histo.GetBinContent(1,2)
        elif(abs(eta)<2):       FR=histo.GetBinContent(1,3)
        elif(abs(eta)<2.4):     FR=histo.GetBinContent(1,4)
    elif(pT<=30):
        if(abs(eta)<1):         FR=histo.GetBinContent(2,1)
        elif(abs(eta)<1.5):     FR=histo.GetBinContent(2,2)
        elif(abs(eta)<2):       FR=histo.GetBinContent(2,3)
        elif(abs(eta)<2.4):     FR=histo.GetBinContent(2,4)
    elif(pT<=40):
        if(abs(eta)<1):         FR=histo.GetBinContent(3,1)
        elif(abs(eta)<1.5):     FR=histo.GetBinContent(3,2)
        elif(abs(eta)<2):       FR=histo.GetBinContent(3,3)
        elif(abs(eta)<2.4):     FR=histo.GetBinContent(3,4)
    elif(pT<=50):
        if(abs(eta)<1):         FR=histo.GetBinContent(4,1)
        elif(abs(eta)<1.5):     FR=histo.GetBinContent(4,2)
        elif(abs(eta)<2):       FR=histo.GetBinContent(4,3)
        elif(abs(eta)<2.4):     FR=histo.GetBinContent(4,4)
    elif(pT>50):
        if(abs(eta)<1):         FR=histo.GetBinContent(5,1)
        elif(abs(eta)<1.5):     FR=histo.GetBinContent(5,2)
        elif(abs(eta)<2):       FR=histo.GetBinContent(5,3)
        elif(abs(eta)<2.4):     FR=histo.GetBinContent(5,4)
    else: FR=0    
    '''

    return FR/(1-FR)

def SFFakeRatio_mu_calc(pT, eta, wp = 'vsjet2'):
    histo = ROOT.TH2F()
    #inFile = ROOT.TFile.Open("FR_vsjet2.root")
    if wp == 'vsjet2':
        inFile = ROOT.TFile.Open("FR_vsjet2_vsmuT.root")
    elif wp == 'vsjet4':
        inFile = ROOT.TFile.Open("FR_vsjet4_vsmuT.root")
    #if prompt:
    histo=(ROOT.TH2F)(inFile.Get("hFRDatamudif"))
    #else:
    #histo=(ROOT.TH2F)(inFile.Get("hFRDatamu"))
    FR=0

    binx = histo.GetXaxis().FindBin(pT)
    biny = histo.GetYaxis().FindBin(abs(eta))
    nxbins = histo.GetXaxis().GetNbins()
    nybins = histo.GetYaxis().GetNbins()
    if binx > nxbins:
        binx = copy.deepcopy(nxbins)
    elif binx <= 0:
        binx = 1
    if biny > nybins:
        biny = copy.deepcopy(nybins)
    elif biny <= 0:
        biny = 1

    FR = copy.deepcopy(histo.GetBinContent(binx, biny))

    '''
    if(pT<=20):
        if(abs(eta)<1):         FR=histo.GetBinContent(1,1)
        elif(abs(eta)<1.5):     FR=histo.GetBinContent(1,2)
        elif(abs(eta)<2):       FR=histo.GetBinContent(1,3)
        elif(abs(eta)<2.4):     FR=histo.GetBinContent(1,4)
    elif(pT<=30):
        if(abs(eta)<1):         FR=histo.GetBinContent(2,1)
        elif(abs(eta)<1.5):     FR=histo.GetBinContent(2,2)
        elif(abs(eta)<2):       FR=histo.GetBinContent(2,3)
        elif(abs(eta)<2.4):     FR=histo.GetBinContent(2,4)
    elif(pT<=40):
        if(abs(eta)<1):         FR=histo.GetBinContent(3,1)
        elif(abs(eta)<1.5):     FR=histo.GetBinContent(3,2)
        elif(abs(eta)<2):       FR=histo.GetBinContent(3,3)
        elif(abs(eta)<2.4):     FR=histo.GetBinContent(3,4)
    elif(pT<=50):
        if(abs(eta)<1):         FR=histo.GetBinContent(4,1)
        elif(abs(eta)<1.5):     FR=histo.GetBinContent(4,2)
        elif(abs(eta)<2):       FR=histo.GetBinContent(4,3)
        elif(abs(eta)<2.4):     FR=histo.GetBinContent(4,4)
    elif(pT>50):
        if(abs(eta)<1):         FR=histo.GetBinContent(5,1)
        elif(abs(eta)<1.5):     FR=histo.GetBinContent(5,2)
        elif(abs(eta)<2):       FR=histo.GetBinContent(5,3)
        elif(abs(eta)<2.4):     FR=histo.GetBinContent(5,4)
    else: FR=0    
    '''

    return FR/(1-FR)

