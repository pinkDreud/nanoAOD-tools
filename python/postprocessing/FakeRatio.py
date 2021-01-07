#!/bin/env python3
import os
##print(os.environ)
##print("**********************************************************************")
##print("**********************************************************************")
##print("**********************************************************************")
##print(str(os.environ.get('PYTHONPATH')))
##print(str(os.environ.get('PYTHON3PATH')))
import sys
##print("*************** This is system version info ***************************")
##print(sys.version_info)
#import platform
##print("*************** This is python version info ***************************")
##print(platform.python_version())
import ROOT
##print("Succesfully imported ROOT")
import math
import datetime
import copy
from array import array
from FakeRatio_utils import *

usage = "python FakeRatio.py [nome_dataset_come_salvato_in_samples.py] [indice, di default 0] [path_file_da_processare] local chosenTrigger"
#chosenTrigger can be: electron, muon, HT

usageCopyPaste="python FakeRatio.py DataHTC_2017 7 DataHTC_2017_ntuple.root local"

chosenTrigger="Depending on the sample"

if sys.argv[5]=="electron": chosenTrigger=sys.argv[5]
if sys.argv[5]=="muon": chosenTrigger=sys.argv[5]
if sys.argv[5]=="HT": chosenTrigger=sys.argv[5]


print("Saving events with: ", chosenTrigger)

if sys.argv[4] == 'remote':
    from samples import *
    Debug = False
else:
    from samples.samples import *
    Debug = True

sample = sample_dict[sys.argv[1]]
part_idx = sys.argv[2]
file_list = list(map(str, sys.argv[3].strip('[]').split(',')))
print(file_list)

MCReco = True
startTime = datetime.datetime.now()
print("Starting running at " + str(startTime))

ROOT.gROOT.SetBatch()

chain = ROOT.TChain('Events')
#print(chain)
for infile in file_list: 
    print("Adding %s to the chain" %(infile))
    chain.Add(infile)


print(chain)

print("Number of events in chain " + str(chain.GetEntries()))
print("Number of events in tree from chain " + str((chain.GetTree()).GetEntries()))
tree = InputTree(chain)
isMC = True
if ('Data' in sample.label):
    isMC = False

MCReco = MCReco * isMC

Fake_dict = {}


Fake_dict = {
            '1A': ['|n|<1,     pT<20    ',  0,  0, 0.0],
            '1B': ['1<|n|<1.5, pT<20    ',  0,  0, 0.0],
            '1C': ['1.5<|n|<2, pT<20    ',  0,  0, 0.0],
            '1D': ['2<|n|<2.4, pT<20    ',  0,  0, 0.0],
            '2A': ['|n|<1,     20<pT<30 ',  0,  0, 0.0],
            '2B': ['1<|n|<1.5, 20<pT<30 ',  0,  0, 0.0],
            '2C': ['1.5<|n|<2, 20<pT<30 ',  0,  0, 0.0],
            '2D': ['2<|n|<2.4, 20<pT<30 ',  0,  0, 0.0],
            '3A': ['|n|<1,     30<pT<40 ',  0,  0, 0.0],
            '3B': ['1<|n|<1.5, 30<pT<40 ',  0,  0, 0.0],
            '3C': ['1.5<|n|<2, 30<pT<40 ',  0,  0, 0.0],
            '3D': ['2<|n|<2.4, 30<pT<40 ',  0,  0, 0.0],
            '4A': ['|n|<1,     40<pT<50 ',  0,  0, 0.0],
            '4B': ['1<|n|<1.5, 40<pT<50 ',  0,  0, 0.0],
            '4C': ['1.5<|n|<2, 40<pT<50 ',  0,  0, 0.0],
            '4D': ['2<|n|<2.4, 40<pT<50 ',  0,  0, 0.0],
            '5A': ['|n|<1,     pT>50    ',  0,  0, 0.0],
            '5B': ['1<|n|<1.5, pT>50    ',  0,  0, 0.0],
            '5C': ['1.5<|n|<2, pT>50    ',  0,  0, 0.0],
            '5D': ['2<|n|<2.4, pT>50    ',  0,  0, 0.0],
}

#++++++++++++++++++++++++++++++++++
#++   branching the new trees    ++
#++++++++++++++++++++++++++++++++++
outTreeFile = ROOT.TFile(sample.label+"_part"+str(part_idx)+".root", "RECREATE") # output file


trees = []
for i in range(10):
    trees.append(None)
#systZero = systWeights()
# defining the operations to be done with the systWeights class
maxSysts = 0
addPDF = True
addQ2 = False
addTopPt = False
addVHF = False
addTTSplit = False
addTopTagging = False
addWTagging = False
addTrigSF = False
nPDF = 0

systTree = systWeights()
systTree.prepareDefault(True, addQ2, addPDF, addTopPt, addVHF, addTTSplit)
systTree.addSelection("all")
systTree.initTreesSysts(trees, outTreeFile)

systTree.setWeightName("w_nominal",1.)
systTree.setWeightName("puSF",1.)
systTree.setWeightName("puUp",1.)
systTree.setWeightName("puDown",1.)
systTree.setWeightName("lepSF",1.)
systTree.setWeightName("lepUp",1.)
systTree.setWeightName("lepDown",1.)
systTree.setWeightName("PFSF",1.)
systTree.setWeightName("PFUp",1.)
systTree.setWeightName("PFDown",1.)

#++++++++++++++++++++++++++++++++++
#++     variables to branch      ++
#++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++++++++++++++
#++         All category         ++
#++++++++++++++++++++++++++++++++++

#ssWW variables
var_list = []

#all leptons for fake
FakeLepton_pt               =   array.array('f', [-999.])
FakeLepton_eta              =   array.array('f', [-999.])
FakeLepton_phi              =   array.array('f', [-999.])
FakeLepton_mass             =   array.array('f', [-999.])
FakeLepton_pdgid            =   array.array('i', [-999])
FakeLepton_pfRelIso04       =   array.array('f', [-999.])
FakeLepton_isPrompt         =   array.array('f', [-999.])
var_list.append(FakeLepton_pt)
var_list.append(FakeLepton_isPrompt)
var_list.append(FakeLepton_eta)
var_list.append(FakeLepton_phi)
var_list.append(FakeLepton_mass)
var_list.append(FakeLepton_pdgid)
var_list.append(FakeLepton_pfRelIso04)

FakeElectron_pt             =   array.array('f', [-999.])
FakeElectron_relIso         =   array.array('f', [-999.])
FakeElectron_eta            =   array.array('f', [-999.])
FakeElectron_phi            =   array.array('f', [-999.])
FakeElectron_mass           =   array.array('f', [-999.])
FakeElectron_pdgid          =   array.array('i', [-999])
FakeElectron_pfRelIso04     =   array.array('f', [-999.])
FakeElectron_isPrompt       =   array.array('f', [-999.])
var_list.append(FakeElectron_pt)
var_list.append(FakeElectron_relIso)
var_list.append(FakeElectron_isPrompt)
var_list.append(FakeElectron_eta)
var_list.append(FakeElectron_phi)
var_list.append(FakeElectron_mass)
var_list.append(FakeElectron_pdgid)
var_list.append(FakeElectron_pfRelIso04)

mT_eleMET                   =   array.array('f', [-999.])
var_list.append(mT_eleMET)

FakeMuon_pt             =   array.array('f', [-999.])
FakeMuon_relIso         =   array.array('f', [-999.])
FakeMuon_eta            =   array.array('f', [-999.])
FakeMuon_phi            =   array.array('f', [-999.])
FakeMuon_mass           =   array.array('f', [-999.])
FakeMuon_pdgid          =   array.array('i', [-999])
FakeMuon_pfRelIso04     =   array.array('f', [-999.])
FakeMuon_isPrompt       =   array.array('f', [-999.])
var_list.append(FakeMuon_pt)
var_list.append(FakeMuon_relIso)
var_list.append(FakeMuon_isPrompt)
var_list.append(FakeMuon_eta)
var_list.append(FakeMuon_phi)
var_list.append(FakeMuon_mass)
var_list.append(FakeMuon_pdgid)
var_list.append(FakeMuon_pfRelIso04)

mT_muMET                   =   array.array('f', [-999.])
var_list.append(mT_muMET)

FakeTau_pt                  =   array.array('f', [-999.])
FakeTau_isPrompt            =   array.array('f', [-999.])
FakeTau_eta                 =   array.array('f', [-999.])
FakeTau_phi                 =   array.array('f', [-999.])
FakeTau_charge              =   array.array('i', [-999])
FakeTau_mass                =   array.array('f', [-999.])
FakeTau_DeepTauWP           =   array.array('f', [-999.])
var_list.append(FakeTau_pt)
var_list.append(FakeTau_isPrompt)
var_list.append(FakeTau_eta)
var_list.append(FakeTau_phi)
var_list.append(FakeTau_charge)
var_list.append(FakeTau_mass)
var_list.append(FakeTau_DeepTauWP)


Veto_LightLeptons           =   array.array('f', [-999.])
Veto_Electrons              =   array.array('f', [-999.])
Veto_Muons                  =   array.array('f', [-999.])
Veto_TauLeptons             =   array.array('f', [-999.])
Veto_TauZMass               =   array.array('f', [-999.])
var_list.append(Veto_LightLeptons)
var_list.append(Veto_Electrons)
var_list.append(Veto_Muons)
var_list.append(Veto_TauLeptons)
var_list.append(Veto_TauZMass)


#MET
MET_pt                      =   array.array('f', [-999.])
MET_phi                     =   array.array('f', [-999.])
mT_lepMET                   =   array.array('f', [-999.])

var_list.append(MET_pt)
var_list.append(MET_phi)
var_list.append(mT_lepMET)

isFake_tau                  =   array.array('i', [-999])
isFake_tauAndPassCuts       =   array.array('i', [-999])
isFake_lepton               =   array.array('i', [-999])
isFake_leptonAndPassCuts    =   array.array('i', [-999])


var_list.append(isFake_tau)
var_list.append(isFake_tauAndPassCuts)
var_list.append(isFake_lepton)
var_list.append(isFake_leptonAndPassCuts)

w_PDF_all = array.array('f', [0.]*110) #capisci a cosa serve
w_nominal_all = array.array('f', [0.])

#branches added for ssWW analysis
#all leptons for fake calculation
systTree.branchTreesSysts(trees, "all", "FakeLepton_pt",            outTreeFile, FakeLepton_pt)
systTree.branchTreesSysts(trees, "all", "FakeLepton_isPrompt",      outTreeFile, FakeLepton_isPrompt)
systTree.branchTreesSysts(trees, "all", "FakeLepton_eta",           outTreeFile, FakeLepton_eta)
systTree.branchTreesSysts(trees, "all", "FakeLepton_phi",           outTreeFile, FakeLepton_phi)
systTree.branchTreesSysts(trees, "all", "FakeLepton_mass",          outTreeFile, FakeLepton_mass)
systTree.branchTreesSysts(trees, "all", "FakeLepton_pdgid",         outTreeFile, FakeLepton_pdgid)
systTree.branchTreesSysts(trees, "all", "FakeLepton_pfRelIso04",    outTreeFile, FakeLepton_pfRelIso04)

systTree.branchTreesSysts(trees, "all", "FakeElectron_pt",          outTreeFile, FakeElectron_pt)
systTree.branchTreesSysts(trees, "all", "FakeElectron_relIso",      outTreeFile, FakeElectron_relIso)
systTree.branchTreesSysts(trees, "all", "FakeElectron_isPrompt",    outTreeFile, FakeElectron_isPrompt)
systTree.branchTreesSysts(trees, "all", "FakeElectron_eta",         outTreeFile, FakeElectron_eta)
systTree.branchTreesSysts(trees, "all", "FakeElectron_phi",         outTreeFile, FakeElectron_phi)
systTree.branchTreesSysts(trees, "all", "FakeElectron_mass",        outTreeFile, FakeElectron_mass)
systTree.branchTreesSysts(trees, "all", "FakeElectron_pdgid",       outTreeFile, FakeElectron_pdgid)
systTree.branchTreesSysts(trees, "all", "FakeElectron_pfRelIso04",  outTreeFile, FakeElectron_pfRelIso04)

systTree.branchTreesSysts(trees, "all", "FakeMuon_pt",              outTreeFile, FakeMuon_pt)
systTree.branchTreesSysts(trees, "all", "FakeMuon_relIso",          outTreeFile, FakeMuon_relIso)
systTree.branchTreesSysts(trees, "all", "FakeMuon_isPrompt",        outTreeFile, FakeMuon_isPrompt)
systTree.branchTreesSysts(trees, "all", "FakeMuon_eta",             outTreeFile, FakeMuon_eta)
systTree.branchTreesSysts(trees, "all", "FakeMuon_phi",             outTreeFile, FakeMuon_phi)
systTree.branchTreesSysts(trees, "all", "FakeMuon_mass",            outTreeFile, FakeMuon_mass)
systTree.branchTreesSysts(trees, "all", "FakeMuon_pdgid",           outTreeFile, FakeMuon_pdgid)
systTree.branchTreesSysts(trees, "all", "FakeMuon_pfRelIso04",      outTreeFile, FakeMuon_pfRelIso04)
#all taus for fake calculation
systTree.branchTreesSysts(trees, "all", "FakeTau_pt",               outTreeFile, FakeTau_pt)
systTree.branchTreesSysts(trees, "all", "FakeTau_isPrompt",         outTreeFile, FakeTau_isPrompt)
systTree.branchTreesSysts(trees, "all", "FakeTau_eta",              outTreeFile, FakeTau_eta)
systTree.branchTreesSysts(trees, "all", "FakeTau_phi",              outTreeFile, FakeTau_phi)
systTree.branchTreesSysts(trees, "all", "FakeTau_mass",             outTreeFile, FakeTau_mass)
systTree.branchTreesSysts(trees, "all", "FakeTau_DeepTauWP",        outTreeFile, FakeTau_DeepTauWP)
#Veto variables
systTree.branchTreesSysts(trees, "all", "Veto_LightLeptons",        outTreeFile, Veto_LightLeptons)
systTree.branchTreesSysts(trees, "all", "Veto_TauLeptons",          outTreeFile, Veto_TauLeptons)
systTree.branchTreesSysts(trees, "all", "Veto_TauZMass",            outTreeFile, Veto_TauZMass)
systTree.branchTreesSysts(trees, "all", "MET_pt",                   outTreeFile, MET_pt)
systTree.branchTreesSysts(trees, "all", "mT_lepMET",                outTreeFile, mT_lepMET)
systTree.branchTreesSysts(trees, "all", "mT_eleMET",                outTreeFile, mT_eleMET)
systTree.branchTreesSysts(trees, "all", "mT_muMET",                 outTreeFile, mT_muMET)

#fake variables
systTree.branchTreesSysts(trees, "all", "isFake_lepton",            outTreeFile, isFake_lepton)
systTree.branchTreesSysts(trees, "all", "isFake_tau",               outTreeFile, isFake_tau)
systTree.branchTreesSysts(trees, "all", "isFake_leptonAndPassCuts", outTreeFile, isFake_leptonAndPassCuts)
systTree.branchTreesSysts(trees, "all", "isFake_tauAndPassCuts",    outTreeFile, isFake_tauAndPassCuts)


#print("Is MC: " + str(isMC) + "      option addPDF: " + str(addPDF))
if(isMC and addPDF):
    systTree.branchTreesSysts(trees, "all", "w_PDF", outTreeFile, w_PDF_all)
####################################################################################################################################################################################################################################

#++++++++++++++++++++++++++++++++++
#++      taking MC weights       ++
#++++++++++++++++++++++++++++++++++
print("isMC: ", isMC)
if(isMC):
    newfile = ROOT.TFile.Open(file_list[0])
    dirc = ROOT.TDirectory()
    dirc = newfile.Get("plots")
    isthere_gen = bool(dirc.GetListOfKeys().Contains("h_genweight"))
    isthere_pdf = bool(dirc.GetListOfKeys().Contains("h_PDFweight"))
    print("gen?: ", isthere_gen, " pdf?: ", isthere_pdf)

    if isthere_gen or isthere_pdf:
        if isthere_gen:
            h_genweight = ROOT.TH1F()
            h_genweight.SetNameTitle('h_genweight', 'h_genweight')
            h_genw_tmp = ROOT.TH1F(dirc.Get("h_genweight"))
            if(ROOT.TH1F(h_genweight).Integral() < 1.):
                h_genweight.SetBins(h_genw_tmp.GetXaxis().GetNbins(), h_genw_tmp.GetXaxis().GetXmin(), h_genw_tmp.GetXaxis().GetXmax())
            h_genweight.Add(h_genw_tmp)
    
        if isthere_pdf:
            h_PDFweight = ROOT.TH1F()
            h_PDFweight.SetNameTitle("h_PDFweight","h_PDFweight")
            h_pdfw_tmp = ROOT.TH1F(dirc.Get("h_PDFweight"))
            if(ROOT.TH1F(h_PDFweight).Integral() < 1.):
                h_PDFweight.SetBins(h_pdfw_tmp.GetXaxis().GetNbins(), h_pdfw_tmp.GetXaxis().GetXmin(), h_pdfw_tmp.GetXaxis().GetXmax())
            h_PDFweight.Add(h_pdfw_tmp)
        else:
            addPDF = False
    newfile.Close()


'''
#++++++++++++++++++++++++++++++++++
#++      Efficiency studies      ++
#++++++++++++++++++++++++++++++++++
neutrino_failed = 0
nrecochi = 0
nrecoclosest = 0
nrecosublead = 0
nrecobest = 0
nbinseff = 10
h_eff_mu = ROOT.TH1D("h_eff_mu", "h_eff_mu", nbinseff, 0, nbinseff)
h_eff_ele = ROOT.TH1D("h_eff_ele", "h_eff_ele", nbinseff, 0, nbinseff)
'''
#++++++++++++++++++++++++++++++++++
#++   looping over the events    ++
#++++++++++++++++++++++++++++++++++
#for i in range(tree.GetEntries()):
for i in range(tree.GetEntries()):
    #reinizializza tutte le variabili a 0, per sicurezza
    for j, var in enumerate(var_list):
        if j<len(var_list):
            var_list[j][0] = -999
    
    w_nominal_all[0] = 1.
    #++++++++++++++++++++++++++++++++++
    #++        taking objects        ++
    #++++++++++++++++++++++++++++++++++

    if Debug:
        print("evento n. " + str(i))
        if i > 2000:
            break
    
    if not Debug and i%500 == 0:
        print("Event #", i+1, " out of ", tree.GetEntries())

    event       = Event(tree,i)
    electrons   = Collection(event, "Electron")
    muons       = Collection(event, "Muon")
    jets        = Collection(event, "Jet")
    njets       = len(jets)
    fatjets     = Collection(event, "FatJet")
    taus        = Collection(event, "Tau")
    HT          = Object(event, "HT")
    PV          = Object(event, "PV")
    HLT         = Object(event, "HLT")
    Flag        = Object(event, 'Flag')
    met         = Object(event, "MET")
    
    genpart = None
    
    if isMC:
        genpart = Collection(event, "GenPart")
        if not ("WZ" in sample.label):
            LHE = Collection(event, "LHEPart")
    
    if not isMC:
        if not Flag.eeBadScFilter:
            continue

    chain.GetEntry(i)
    #++++++++++++++++++++++++++++++++++
    #++      defining variables      ++
    #++++++++++++++++++++++++++++++++++
    tightlep = None
    tightlep_p4 = None
    tightlep_p4t = None
    tightlep_SF = None
    tightlep_SFUp = None
    tightlep_SFDown = None
    recomet_p4t = None
    PF_SF = None
    PF_SFUp = None
    PF_SFDown = None
    PU_SF = None
    PU_SFUp = None
    PU_SFDown = None
    #++++++++++++++++++++++++++++++++++
    #++    starting the analysis     ++
    #++++++++++++++++++++++++++++++++++
    year = sample.year
    if(isMC):
        runPeriod = ''
    else:
        runPeriod = sample.runP
    
    passMu, passEle, passHT, noTrigger, passMuLoose, passEleLoose = trig_map(HLT, PV, year, runPeriod)

    conditionToSave=False
    if chosenTrigger=="Depending on the sample":
        if "SingleElectron" in sample.dataset:  
            conditionToSave= passEleLoose
            waw="electron"
        if "SingleMuon" in sample.dataset:      
            conditionToSave= passMuLoose 
            waw="mu"
        if "JetHT" in sample.dataset:           
            conditionToSave= passHT 
            waw="other stuff"
    elif chosenTrigger=="electron":
        conditionToSave = passEleLoose
    elif chosenTrigger=="muon":
        conditionToSave = passMuLoose
    elif chosenTrigger=="HT":
        conditionToSave=passHT
   
    if not conditionToSave: continue
    
    SingleEle   =   False
    SingleMu    =   False
    ElMu        =   False

    HighestLepPt  = -999.
    LeadLepFamily = "not selected"
    
    if sys.argv[5]=="HT": #just to be sure that it selects the highest pt ele/mu in the case we're using HT triggers, principally because now the loose trigger paths have not been implemented
        passEle =   True
        passMu  =   True 


    if passEleLoose and not passMuLoose:
        if len(electrons)>0:  
            SingleEle=True
            LeadLepFamily="electrons"
            HighestLepPt=electrons[0].pt
            #print("HighestLepPt:", HighestLepPt)
        else:
            continue

    elif passMuLoose and not passEleLoose:
        if len(muons)>0:
            SingleMu=True
            LeadLepFamily="muons"
            HighestLepPt=muons[0].pt
        else:
            continue

    elif passMuLoose and passEleLoose:
        ElMu=True

    if ElMu:
        for mu in muons:
            if abs(mu.pt)>HighestLepPt:
                HighestLepPt=mu.pt
                SingleEle = False
                SingleMu = True
                break
        for ele in electrons:
            if abs(ele.pt)>HighestLepPt:
                HighestLepPt=ele.pt
                SingleEle = True
                SingleMu = False
                break
  
        
    MET_pt[0]=met.pt
    MET_phi[0]=met.phi
    
    if Veto_Tau_Leptons(taus, electrons, muons):    Veto_TauLeptons[0]=1
    else:                                           Veto_TauLeptons[0]=0

    if Veto_Tau_ZMass(taus, electrons, muons):      Veto_TauZMass[0]=1
    else:                                           Veto_TauZMass[0]=0

    eleGood=list(electrons)
    muGood=list(muons)
   
    if Veto_TauLeptons[0]==0 or Veto_TauZMass[0]==0: 
        for ele in eleGood:
            if deltaR(ele.eta, ele.phi, taus[0].eta, taus[0].phi)<0.5: eleGood.remove(ele)
        for mu in muGood:
            if deltaR(mu.eta, mu.phi, taus[0].eta, taus[0].phi)<0.5: muGood.remove(mu)
   

    if len(muGood)>0 and SingleMu:
        Veto_Muons[0]=Veto_muons(muGood)
        singleMuGood=None
        for mu in muGood:
            if mu.pfRelIso04_all<1 and mu.tightId:
                singleMuGood=mu
                break
        if singleMuGood!=None:
            mT_muMET[0]         =   mTlepMet(met, singleMuGood)
            FakeMuon_pt[0]      =   singleMuGood.pt
            FakeMuon_eta[0]     =   singleMuGood.eta
            FakeMuon_phi[0]     =   singleMuGood.phi
            FakeMuon_mass[0]    =   singleMuGood.mass
            FakeMuon_pdgid[0]   =   singleMuGood.pdgId
            FakeMuon_relIso[0]  =   singleMuGood.pfRelIso04_all
    
    if len(eleGood)>0 and SingleEle:
        Veto_Electrons[0]=Veto_electrons(eleGood)
        singleEleGood=None
        for ele in eleGood:
            if ele.jetRelIso<1 and ele.mvaFall17V2Iso_WP90: 
                singleEleGood=ele
                break
        if singleEleGood!=None:
            mT_eleMET[0]            =   mTlepMet(met, singleEleGood)
            FakeElectron_pt[0]      =   singleEleGood.pt
            FakeElectron_eta[0]     =   singleEleGood.eta
            FakeElectron_phi[0]     =   singleEleGood.phi
            FakeElectron_mass[0]    =   singleEleGood.mass
            FakeElectron_pdgid[0]   =   singleEleGood.pdgId
            FakeElectron_relIso[0]  =   singleEleGood.jetRelIso
    

    Veto_LightLeptons[0], isEle=Veto_Light_Leptons(eleGood, muGood)
       

    
    nLepGood=-999
    if isEle:   
        leptons     =   eleGood
        nLepGood    =   len(eleGood)
    else:       
        leptons     =   muGood
        nLepGood    =   len(muGood)
    
    if nLepGood>0:
         
        lepgood=None
        if isEle:
            for ele in eleGood:
                if ele.jetRelIso<1 and ele.mvaFall17V2Iso_WP90: 
                    lepgood=ele
                    break
        else:
            for mu in muGood:
                if mu.pfRelIso04_all<1 and mu.tightId:
                    lepgood=mu
                    break
        #print('Event n. ', i+1)
        #print('number of good leptons: ', nLepGood)
        #print('is it an electron?      ', isEle)
        #print('is it a muon?           ', not isEle)
        #print('does lepgood exist?     ', lepgood!=None)

        if lepgood!=None:
            
            mT_lepMET[0]=mTlepMet(met, lepgood)
            
            isFake_lepton[0]=1
            
            if abs(lepgood.pdgId)==11:
                if lepgood.jetRelIso<0.08:        isFake_leptonAndPassCuts[0]=1
            if abs(lepgood.pdgId)==13:
                if lepgood.pfRelIso04_all<0.15:         isFake_leptonAndPassCuts[0]=1

            FakeLepton_pt[0]                =   lepgood.pt
            FakeLepton_eta[0]               =   lepgood.eta
            FakeLepton_phi[0]               =   lepgood.phi
            FakeLepton_mass[0]              =   lepgood.mass
            FakeLepton_pdgid[0]             =   lepgood.pdgId
            FLrelIso04=-999
            
            if abs(lepgood.pdgId)==11:     FLrelIso04=lepgood.jetRelIso
            elif abs(lepgood.pdgId)==13:   FLrelIso04=lepgood.pfRelIso04_all

            FakeLepton_pfRelIso04[0]            =   FLrelIso04
            if isMC: FakeLepton_isPrompt[0]     =   lepgood.genPartFlav
            
    if len(taus)>0:
        mT_tauMET=mTlepMet(met, taus[0])
        isFake_tau[0]=1
        if taus[0].idDeepTau2017v2p1VSjet>=64: isFake_tauAndPassCuts[0]=1 #errore, prima >=16. Deve esser >=64 (VT taglio usato in analisi)
    
        FakeTau_pt[0]                   =   taus[0].pt
        FakeTau_eta[0]                  =   taus[0].eta
        FakeTau_phi[0]                  =   taus[0].phi
        FakeTau_mass[0]                 =   taus[0].mass
        FakeTau_charge[0]               =   taus[0].charge
        if isMC: FakeTau_isPrompt[0]    =   taus[0].genPartFlav
      

    systTree.setWeightName("w_nominal",copy.deepcopy(w_nominal_all[0]))
    systTree.fillTreesSysts(trees, "all")


outTreeFile.cd()
if(isMC):
    h_genweight.Write()
    if not ("WZ" in sample.label):
        h_PDFweight.Write()


systTree.writeTreesSysts(trees, outTreeFile)
print("Number of events in output tree " + str(trees[0].GetEntries()))

endTime = datetime.datetime.now()
print("Ending running at " + str(endTime))
