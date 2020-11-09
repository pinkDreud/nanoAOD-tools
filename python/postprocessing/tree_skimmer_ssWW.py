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
from skimtree_utils import *

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

Cut_dict = {}

#if Debug:
Cut_dict = {1: ['Trigger             ', 0, 0.0, 0.0, 0.0, 0.0],
            2: ['Lepton selection    ', 0, 0.0, 0.0, 0.0, 0.0],
            3: ['Lepton Veto         ', 0, 0.0, 0.0, 0.0, 0.0],
            4: ['Tau selection       ', 0, 0.0, 0.0, 0.0, 0.0],
            5: ['Same charge tau lep ', 0, 0.0, 0.0, 0.0, 0.0],
            6: ['Jet Selection       ', 0, 0.0, 0.0, 0.0, 0.0],
            7: ['BVeto               ', 0, 0.0, 0.0, 0.0, 0.0],
            8: ['M_jj>500 GeV        ', 0, 0.0, 0.0, 0.0, 0.0],
            9: ['MET>40 GeV          ', 0, 0.0, 0.0, 0.0, 0.0],
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
#lepton variables
lepton_pt               =   array.array('f', [-999.])
lepton_eta              =   array.array('f', [-999.])
lepton_phi              =   array.array('f', [-999.])
lepton_mass             =   array.array('f', [-999.])
lepton_pdgid            =   array.array('i', [-999])
lepton_pfRelIso03       =   array.array('f', [-999.])
var_list.append(lepton_pt)
var_list.append(lepton_eta)
var_list.append(lepton_phi)
var_list.append(lepton_mass)
var_list.append(lepton_pdgid)
var_list.append(lepton_pfRelIso03)

#tau variables
tau_pt                  =   array.array('f', [-999.])
tau_eta                 =   array.array('f', [-999.])
tau_phi                 =   array.array('f', [-999.])
tau_charge              =   array.array('i', [-999])
tau_mass                =   array.array('f', [-999.])
tau_DeepTau_WP       =   array.array('f', [-999.])
var_list.append(tau_pt)
var_list.append(tau_eta)
var_list.append(tau_phi)
var_list.append(tau_charge)
var_list.append(tau_mass)
var_list.append(tau_DeepTau_WP)

#jet variables
Leadjet_pt                  =   array.array('f', [-999.])
Leadjet_eta                 =   array.array('f', [-999.])
Leadjet_phi                 =   array.array('f', [-999.])
Leadjet_mass                =   array.array('f', [-999.])
Leadjet_CSVv2_b             =   array.array('f', [-999.])
Leadjet_DeepFlv_b           =   array.array('f', [-999.])
Leadjet_DeepCSVv2_b         =   array.array('f', [-999.])
var_list.append(Leadjet_pt)
var_list.append(Leadjet_eta)
var_list.append(Leadjet_phi)
var_list.append(Leadjet_mass)
var_list.append(Leadjet_CSVv2_b)
var_list.append(Leadjet_DeepFlv_b)
var_list.append(Leadjet_DeepCSVv2_b)

Subleadjet_pt               =   array.array('f', [-999.])
Subleadjet_eta              =   array.array('f', [-999.])
Subleadjet_phi              =   array.array('f', [-999.])
Subleadjet_mass             =   array.array('f', [-999.])
Subleadjet_CSVv2_b          =   array.array('f', [-999.])
Subleadjet_DeepFlv_b        =   array.array('f', [-999.])
Subleadjet_DeepCSVv2_b      =   array.array('f', [-999.])
var_list.append(Subleadjet_pt)
var_list.append(Subleadjet_eta)
var_list.append(Subleadjet_phi)
var_list.append(Subleadjet_mass)
var_list.append(Subleadjet_CSVv2_b)
var_list.append(Subleadjet_DeepFlv_b)
var_list.append(Subleadjet_DeepCSVv2_b)

#MET
MET_pt                      =   array.array('f', [-999.])
MET_phi                     =   array.array('f', [-999.])
var_list.append(MET_pt)
var_list.append(MET_phi)

Mjj                         =   array.array('f', [-999.])
var_list.append(Mjj)

#cut variables
pass_lepton_selection       =   array.array('i', [0])
pass_lepton_veto            =   array.array('i', [0])
pass_tau_selection          =   array.array('i', [0])
pass_charge_selection       =   array.array('i', [0])
pass_jet_selection          =   array.array('i', [0])
pass_b_veto                 =   array.array('i', [0])
pass_mjj_cut                =   array.array('i', [0])
pass_MET_cut                =   array.array('i', [0])
var_list.append(pass_lepton_selection)
var_list.append(pass_lepton_veto)
var_list.append(pass_tau_selection)
var_list.append(pass_charge_selection)
var_list.append(pass_jet_selection)
var_list.append(pass_b_veto)
var_list.append(pass_mjj_cut)
var_list.append(pass_MET_cut)

w_PDF_all = array.array('f', [0.]*110) #capisci a cosa serve
w_nominal_all = array.array('f', [0.])

#branches added for ssWW analysis
#lepton
systTree.branchTreesSysts(trees, "all", "lepton_pt",            outTreeFile, lepton_pt)
systTree.branchTreesSysts(trees, "all", "lepton_eta",           outTreeFile, lepton_eta)
systTree.branchTreesSysts(trees, "all", "lepton_phi",           outTreeFile, lepton_phi)
systTree.branchTreesSysts(trees, "all", "lepton_mass",          outTreeFile, lepton_mass)
systTree.branchTreesSysts(trees, "all", "lepton_pdgid",         outTreeFile, lepton_pdgid)
systTree.branchTreesSysts(trees, "all", "lepton_pfRelIso03",    outTreeFile, lepton_pfRelIso03)
#tau variables
systTree.branchTreesSysts(trees, "all", "tau_pt",               outTreeFile, tau_pt)
systTree.branchTreesSysts(trees, "all", "tau_eta",              outTreeFile, tau_eta)
systTree.branchTreesSysts(trees, "all", "tau_phi",              outTreeFile, tau_phi)
systTree.branchTreesSysts(trees, "all", "tau_mass",             outTreeFile, tau_mass)
systTree.branchTreesSysts(trees, "all", "tau_DeepTau_WP",             outTreeFile, tau_DeepTau_WP)
#jet variables
systTree.branchTreesSysts(trees, "all", "Leadjet_pt",           outTreeFile, Leadjet_pt)
systTree.branchTreesSysts(trees, "all", "Leadjet_eta",          outTreeFile, Leadjet_eta)
systTree.branchTreesSysts(trees, "all", "Leadjet_phi",          outTreeFile, Leadjet_phi)
systTree.branchTreesSysts(trees, "all", "Leadjet_mass",         outTreeFile, Leadjet_mass)
systTree.branchTreesSysts(trees, "all", "Leadjet_CSVv2_b",      outTreeFile, Leadjet_CSVv2_b)
systTree.branchTreesSysts(trees, "all", "Leadjet_DeepFlv_b",    outTreeFile, Leadjet_DeepFlv_b)
systTree.branchTreesSysts(trees, "all", "Leadjet_DeepCSVv2_b",  outTreeFile, Leadjet_DeepCSVv2_b)

systTree.branchTreesSysts(trees, "all", "Subleadjet_pt",           outTreeFile, Subleadjet_pt)
systTree.branchTreesSysts(trees, "all", "Subleadjet_eta",          outTreeFile, Subleadjet_eta)
systTree.branchTreesSysts(trees, "all", "Subleadjet_phi",          outTreeFile, Subleadjet_phi)
systTree.branchTreesSysts(trees, "all", "Subleadjet_mass",         outTreeFile, Subleadjet_mass)
systTree.branchTreesSysts(trees, "all", "Subleadjet_CSVv2_b",      outTreeFile, Subleadjet_CSVv2_b)
systTree.branchTreesSysts(trees, "all", "Subleadjet_DeepFlv_b",    outTreeFile, Subleadjet_DeepFlv_b)
systTree.branchTreesSysts(trees, "all", "Subleadjet_DeepCSVv2_b",  outTreeFile, Subleadjet_DeepCSVv2_b)

#MET

systTree.branchTreesSysts(trees, "all", "MET_pt",               outTreeFile, MET_pt)
systTree.branchTreesSysts(trees, "all", "MET_phi",              outTreeFile, MET_phi)

systTree.branchTreesSysts(trees, "all", "Mjj",                  outTreeFile, Mjj)

#cut variables
systTree.branchTreesSysts(trees, "all", "pass_lepton_selection",    outTreeFile, pass_lepton_selection)
systTree.branchTreesSysts(trees, "all", "pass_lepton_veto",         outTreeFile, pass_lepton_veto)
systTree.branchTreesSysts(trees, "all", "pass_tau_selection",       outTreeFile, pass_tau_selection)
systTree.branchTreesSysts(trees, "all", "pass_charge_selection",    outTreeFile, pass_charge_selection)
systTree.branchTreesSysts(trees, "all", "pass_jet_selection",       outTreeFile, pass_jet_selection)
systTree.branchTreesSysts(trees, "all", "pass_b_veto",              outTreeFile, pass_b_veto)
systTree.branchTreesSysts(trees, "all", "pass_mjj_cut",             outTreeFile, pass_mjj_cut)
systTree.branchTreesSysts(trees, "all", "pass_MET_cut",             outTreeFile, pass_MET_cut)


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
contagood=0
#++++++++++++++++++++++++++++++++++
#++   looping over the events    ++
#++++++++++++++++++++++++++++++++++
for i in range(tree.GetEntries()):
    #reinizializza tutte le variabili a 0, per sicurezza
    for j, var in enumerate(var_list):
        if j<len(var_list)-8:
            var_list[j][0] = -999
        else:
            var_list[j][0] = 0
    
    w_nominal_all[0] = 1.
    #++++++++++++++++++++++++++++++++++
    #++        taking objects        ++
    #++++++++++++++++++++++++++++++++++
    '''
    if Debug:
        print("evento n. " + str(i))
        if i > 2000:
            break
    
    if not Debug and i%5000 == 0:
    '''
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
    
    #h_eff_mu.Fill('Total', 1)
    #h_eff_ele.Fill('Total', 1)

    if isMC:
        genpart = Collection(event, "GenPart")
        if not ("WZ" in sample.label):
            LHE = Collection(event, "LHEPart")
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
    #VetoMu = get_LooseMu(muons)
    #goodMu = get_Mu(muons)
    #VetoEle = get_LooseEle(electrons)
    #goodEle = get_Ele(electrons)
    year = sample.year
    if(isMC):
        runPeriod = ''
    else:
        runPeriod = sample.runP
    
    #print "------ ", i
    passMu, passEle, noTrigger = trig_map(HLT, year, runPeriod)

    ###### Dobbiamo personalizzare a tempo debito goodMu/Ele e vetoEle/Mu, per ora commentiamo
    #isMuon = (len(goodMu) == 1) and (len(goodEle) == 0) and len(VetoMu) == 0 and len(VetoEle) == 0 and (passMu)
    #isElectron = (len(goodMu) == 0) and (len(goodEle) == 1) and len(VetoMu) == 0 and len(VetoEle) == 0 and (passEle)
    ######


    if noTrigger: continue
    doublecounting = True
    if(isMC):
        doublecounting = False
    #Double counting removal
    if('DataMu' in sample.label and passMu):
        doublecounting = False
    if('DataEle' in sample.label and (not passMu and passEle)):
        doublecounting = False

    if doublecounting:
        continue

    SingleEle=False
    SingleMu=False
    ElMu=False

    HighestLepPt=-999.
    LeadLepFamily="not selected"
    
    if passEle and not HLT.Ele32_WPTight_Gsf_L1DoubleEG:
        print("Errore")#Questo ora non dovrebbe succedere
    
    if passEle or passMu:
        if len(electrons)<1 and len(muons)<1:         continue
    else: continue
    

    if passEle and not passMu and len(electrons)>0:  
        SingleEle=True
        LeadLepFamily="electrons"
        HighestLepPt=electrons[0].pt
    
    if passMu and not passEle and len(muons)>0:
        SingleMu=True
        LeadLepFamilu="muons"
        HighestLepPt=muons[0].pt

    if passMu and passEle:
        ElMu=True

    if ElMu:
        for mu in muons:
            if mu.pt>HighestLepPt:
                HighestLepPt=mu.pt
        for ele in electrons:
            if ele.pt>HighestLepPt:
                SingleEle=True
                break
    
    if SingleEle==False and HighestLepPt>0: SingleMu=True
    
    if SingleEle==True: leptons=electrons
    if SingleMu==True:  leptons=muons

    if (SingleEle or SingleMu): Cut_dict[1][1]+=1
    
    MET_pt[0]   =   met.pt  
    MET_phi[0]  =   met.phi

    indexGoodLep=SelectLepton(leptons, SingleMu)

    if indexGoodLep<0 or indexGoodLep>=len(leptons): 
        systTree.setWeightName("w_nominal",copy.deepcopy(w_nominal_all[0]))
        systTree.fillTreesSysts(trees, "all")
        continue
    

    pass_lepton_selection[0]       =   1
    

    if (SingleEle==1 or SingleMu==1) and pass_lepton_selection[0]==1: Cut_dict[2][1]+=1

    lepton_pt[0]                =   leptons[indexGoodLep].pt
    lepton_eta[0]               =   leptons[indexGoodLep].eta
    lepton_phi[0]               =   leptons[indexGoodLep].phi
    lepton_mass[0]              =   leptons[indexGoodLep].mass
    lepton_pdgid[0]             =   leptons[indexGoodLep].pdgId
    lepton_pfRelIso03[0]        =   leptons[indexGoodLep].pfRelIso03_all
    
    GoodLep=leptons[indexGoodLep]
    pass_lepton_veto[0]=LepVeto(GoodLep, electrons, muons)
    
    if (SingleEle or SingleMu) and pass_lepton_selection[0]==1 and pass_lepton_veto[0]==1: Cut_dict[3][1]+=1    
    
    UseDeepTau=True
    indexGoodTau=SelectTau(taus, GoodLep, UseDeepTau)

    if indexGoodTau<0:
        systTree.setWeightName("w_nominal",copy.deepcopy(w_nominal_all[0]))
        systTree.fillTreesSysts(trees, "all")
        continue      

    pass_tau_selection[0]=1
    
    if (SingleEle or SingleMu) and pass_lepton_selection[0]==1 and pass_lepton_veto[0]==1 and pass_tau_selection[0]==1: Cut_dict[4][1]+=1

    GoodTau=taus[indexGoodTau]
    tau_pt[0]               =   GoodTau.pt
    tau_eta[0]              =   GoodTau.eta
    tau_phi[0]              =   GoodTau.phi
    tau_mass[0]             =   GoodTau.mass
    tau_charge[0]           =   GoodTau.charge

    tau_DeepTau_WP[0] = GoodTau.idDeepTau2017v2p1VSjet*1000.**2. + GoodTau.idDeepTau2017v2p1VSmu*1000. + GoodTau.idDeepTau2017v2p1VSe

    if GoodTau.charge==GoodLep.charge:
        pass_charge_selection[0]=1

    if (SingleEle or SingleMu) and pass_lepton_selection[0]==1 and pass_lepton_veto[0]==1 and pass_tau_selection[0]==1 and pass_charge_selection[0]==1: Cut_dict[5][1]+=1

    outputJetSel=JetSelection(list(jets), GoodTau, GoodLep)
    
    if outputJetSel==-999:
        systTree.setWeightName("w_nominal",copy.deepcopy(w_nominal_all[0]))
        systTree.fillTreesSysts(trees, "all")
        continue  

    jet1, jet2=outputJetSel
    
    Leadjet_pt[0]               =   jet1.pt
    Leadjet_eta[0]              =   jet1.eta
    Leadjet_phi[0]              =   jet1.phi
    Leadjet_mass[0]             =   jet1.mass
    Leadjet_DeepFlv_b[0]        =   jet1.btagDeepFlavB
    Leadjet_DeepCSVv2_b[0]      =   jet1.btagDeepB
    Leadjet_CSVv2_b[0]          =   jet1.btagCSVV2
    
    Subleadjet_pt[0]            =   jet2.pt
    Subleadjet_eta[0]           =   jet2.eta
    Subleadjet_phi[0]           =   jet2.phi
    Subleadjet_mass[0]          =   jet2.mass
    Subleadjet_DeepFlv_b[0]     =   jet2.btagDeepFlavB
    Subleadjet_DeepCSVv2_b[0]   =   jet2.btagDeepB
    Subleadjet_CSVv2_b[0]       =   jet2.btagCSVV2
    
    


    pass_jet_selection[0]=1

    if (SingleEle or SingleMu) and pass_lepton_selection[0]==1 and pass_lepton_veto[0]==1 and pass_tau_selection[0]==1 and pass_charge_selection[0]==1 and pass_jet_selection[0]==1: Cut_dict[6][1]+=1

    if not BVeto(jets): pass_b_veto[0]=1

    if (SingleEle or SingleMu) and pass_lepton_selection[0]==1 and pass_lepton_veto[0]==1 and pass_tau_selection[0]==1 and pass_charge_selection[0]==1 and pass_jet_selection[0]==1 and pass_b_veto[0]==1: Cut_dict[7][1]+=1


    LeadJet=ROOT.TLorentzVector()
    SubleadJet=ROOT.TLorentzVector()
    LeadJet.SetPtEtaPhiM(jet1.pt, jet1.eta, jet1.phi, jet1.mass)
    SubleadJet.SetPtEtaPhiM(jet2.pt, jet2.eta, jet2.phi, jet2.mass) 
    
    if not JetCut(LeadJet, SubleadJet): pass_mjj_cut[0]=1

    if pass_mjj_cut[0]==1: Mjj[0]=(LeadJet+SubleadJet).M()

    if (SingleEle or SingleMu) and pass_lepton_selection[0]==1 and pass_lepton_veto[0]==1 and pass_tau_selection[0]==1 and pass_charge_selection[0]==1 and pass_jet_selection[0]==1 and pass_b_veto[0]==1 and pass_mjj_cut[0]==1: Cut_dict[8][1]+=1

    if not metCut(met): pass_MET_cut[0]=1

    if (SingleEle or SingleMu) and pass_lepton_selection[0]==1 and pass_lepton_veto[0]==1 and pass_tau_selection[0]==1 and pass_charge_selection[0]==1 and pass_jet_selection[0]==1 and pass_b_veto[0]==1 and pass_mjj_cut[0]==1 and pass_MET_cut[0]==1: Cut_dict[9][1]+=1

    #######################################
    ## Removing events with HEM problem  ##
    #######################################
    passesMETHEMVeto = HEMveto(jets, electrons)
    if(sample.year == 2018 and not passesMETHEMVeto):
        if(not isMC and chain.run > 319077.):
            continue
        elif(isMC):
            w_nominal_all[0] *= 0.354

    '''
    if len(goodMu) == 1:
        h_eff_mu.Fill('Good Mu', 1)
        if len(goodEle) == 0:
            h_eff_mu.Fill('Good Ele', 1)
        if len(VetoMu) == 0:
            h_eff_mu.Fill('Veto Mu', 1)
        if len(VetoEle) == 0:
            h_eff_mu.Fill('Veto Ele', 1)
    if len(goodEle) == 1:
        h_eff_ele.Fill('Good Ele', 1)
        if len(goodMu) == 0:
            h_eff_ele.Fill('Good Mu', 1)
        if len(VetoMu) == 0:
            h_eff_ele.Fill('Veto Mu', 1)
        if len(VetoEle) == 0:
            h_eff_ele.Fill('Veto Ele', 1)
    '''
    systTree.setWeightName("w_nominal",copy.deepcopy(w_nominal_all[0]))
    systTree.fillTreesSysts(trees, "all")

#trees[0].Print()
outTreeFile.cd()
if(isMC):
    #print("h_genweight first bin content is %f and h_PDFweight has %f bins" %(h_genweight.GetBinContent(1), h_PDFweight.GetNbinsX()))
    h_genweight.Write()
    if not ("WZ" in sample.label):
        h_PDFweight.Write()
    #h_eff_mu.Write()
    #h_eff_ele.Write()
'''
if Debug:
    for i in range(1,10):
        if i==1:
            Cut_dict[i][2]=Cut_dict[i][1]*1.0/nEntriesTotal
            Cut_dict[i][3]=Cut_dict[i][1]*1.0/nEntriesTotal
            Cut_dict[i][4]=math.sqrt(Cut_dict[i][2]*(1-Cut_dict[i][2])/nEntriesTotal)
            Cut_dict[i][5]=math.sqrt(Cut_dict[i][3]*(1-Cut_dict[i][2])/nEntriesTotal)
        else:
            if Cut_dict[i-1][1]<=0 or Cut_dict[i][1]==0:
                Cut_dict[i][2]=-999
                Cut_dict[i][3]=Cut_dict[i][1]*1.0/nEntriesTotal
                Cut_dict[i][4]=-999
                Cut_dict[i][5]=-999
            else:
                Cut_dict[i][2]=Cut_dict[i][1]*1.0/Cut_dict[i-1][1]
                Cut_dict[i][3]=Cut_dict[i][1]*1.0/nEntriesTotal
                Cut_dict[i][4]=math.sqrt(Cut_dict[i][2]*(1-Cut_dict[i][2])/Cut_dict[i][1]*1.0)
                Cut_dict[i][5]=math.sqrt(Cut_dict[i][3]*(1-Cut_dict[i][2])/nEntriesTotal)
'''
if Debug:
    for cutname, counts in Cut_dict.items():
        print(counts[0], round(counts[1], 4))


systTree.writeTreesSysts(trees, outTreeFile)
print("Number of events in output tree " + str(trees[0].GetEntries()))

endTime = datetime.datetime.now()
print("Ending running at " + str(endTime))
