import os
import sys
import ROOT
import math
import datetime
import copy
from array import array
from skimtree_utils_ssWW_wFakes import *

usage = "python tree_skimmer_CT.py [nome_del_sample_in_samples.py] 0 [file_in_input] local [chosen_trigger]"

if sys.argv[4] == 'remote':
    from samples import *
    Debug = False
else:
    from samples.samples import *
    Debug = False
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

#++++++++++++++++++++++++++++++++++
#++   branching the new trees    ++
#++++++++++++++++++++++++++++++++++
outTreeFile = ROOT.TFile(sample.label+"_part"+str(part_idx)+".root", "RECREATE") # output file


trees = []
for i in range(10):
    trees.append(None)
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
#lepton#
lepton_pt               =   array.array('f', [-999.])
lepton_eta              =   array.array('f', [-999.])
lepton_phi              =   array.array('f', [-999.])
lepton_mass             =   array.array('f', [-999.])
lepton_pdgid            =   array.array('i', [-999])
lepton_pfRelIso04       =   array.array('f', [-999.])
lepton_TightRegion      =   array.array('i', [-999])
lepton_LnTRegion        =   array.array('i', [-999])
lepton_SFFake           =   array.array('f', [-999.])
lepton_isPrompt           =   array.array('i', [-999])
lepton_Zeppenfeld           =   array.array('f', [-999])
lepton_Zeppenfeld_over_deltaEta_jj           =   array.array('f', [-999])
var_list.append(lepton_pt)
var_list.append(lepton_eta)
var_list.append(lepton_phi)
var_list.append(lepton_mass)
var_list.append(lepton_pdgid)
var_list.append(lepton_pfRelIso04)
var_list.append(lepton_TightRegion)
var_list.append(lepton_LnTRegion)
var_list.append(lepton_SFFake)
var_list.append(lepton_isPrompt)
var_list.append(lepton_Zeppenfeld)
var_list.append(lepton_Zeppenfeld_over_deltaEta_jj)
#tau#
tau_pt                  =   array.array('f', [-999.])
tau_eta                 =   array.array('f', [-999.])
tau_phi                 =   array.array('f', [-999.])
tau_charge              =   array.array('i', [-999])
tau_mass                =   array.array('f', [-999.])
tau_DeepTau_WP          =   array.array('f', [-999.])
tau_isolation           =   array.array('f', [-999.])
tau_DeepTauVsEle_WP     =   array.array('f', [-999.])
tau_DeepTauVsEle_raw    =   array.array('f', [-999.])
tau_DeepTauVsMu_WP      =   array.array('f', [-999.])
tau_DeepTauVsMu_raw     =   array.array('f', [-999.])
tau_DeepTauVsJet_WP     =   array.array('f', [-999.])
tau_DeepTauVsJet_raw    =   array.array('f', [-999.])
tau_TightRegion         =   array.array('i', [-999])
tau_LnTRegion           =   array.array('i', [-999])
tau_SFFake              =   array.array('f', [-999.])
tau_isPrompt           =   array.array('i', [-999])
tau_Zeppenfeld           =   array.array('f', [-999])
tau_Zeppenfeld_over_deltaEta_jj           =   array.array('f', [-999])
var_list.append(tau_isolation)
var_list.append(tau_pt)
var_list.append(tau_eta)
var_list.append(tau_phi)
var_list.append(tau_charge)
var_list.append(tau_mass)
var_list.append(tau_DeepTau_WP)
var_list.append(tau_DeepTauVsEle_raw)#
var_list.append(tau_DeepTauVsMu_WP)#
var_list.append(tau_DeepTauVsMu_raw)#
var_list.append(tau_DeepTauVsJet_WP)#
var_list.append(tau_DeepTauVsJet_raw)#
var_list.append(tau_TightRegion)#
var_list.append(tau_LnTRegion)#
var_list.append(tau_SFFake)#
var_list.append(tau_isPrompt)#
var_list.append(tau_Zeppenfeld)
var_list.append(tau_Zeppenfeld_over_deltaEta_jj)

event_Zeppenfeld           =   array.array('f', [-999])
event_Zeppenfeld_over_deltaEta_jj           =   array.array('f', [-999])
var_list.append(event_Zeppenfeld)
var_list.append(event_Zeppenfeld_over_deltaEta_jj)

#event SFFake
event_SFFake              =   array.array('f', [-999.])
var_list.append(event_SFFake)

#jet#
leadjet_pt                  =   array.array('f', [-999.])
leadjet_eta                 =   array.array('f', [-999.])
leadjet_phi                 =   array.array('f', [-999.])
leadjet_mass                =   array.array('f', [-999.])
leadjet_DeepFlv_b           =   array.array('f', [-999.])
nJets                       =   array.array('f', [-999.])#
nBJets                      =   array.array('f', [-999.])#
var_list.append(leadjet_pt)
var_list.append(leadjet_eta)
var_list.append(leadjet_phi)
var_list.append(leadjet_mass)
var_list.append(leadjet_DeepFlv_b)
var_list.append(nJets)#
var_list.append(nBJets)#
subleadjet_pt               =   array.array('f', [-999.])
subleadjet_eta              =   array.array('f', [-999.])
subleadjet_phi              =   array.array('f', [-999.])
subleadjet_mass             =   array.array('f', [-999.])
subleadjet_DeepFlv_b        =   array.array('f', [-999.])
var_list.append(subleadjet_pt)
var_list.append(subleadjet_eta)
var_list.append(subleadjet_phi)
var_list.append(subleadjet_mass)
var_list.append(subleadjet_DeepFlv_b)

#MET
MET_pt                      =   array.array('f', [-999.])
MET_phi                     =   array.array('f', [-999.])
var_list.append(MET_pt)
var_list.append(MET_phi)

mjj                         =   array.array('f', [-999.])
m_leptau                    =   array.array('f', [-999.])
mT_lep_MET                  =   array.array('f', [-999.])
var_list.append(mjj)
var_list.append(m_leptau)
var_list.append(mT_lep_MET)

#deltaPhi#                                                                      
deltaPhi_jj                 =   array.array('f', [-999.])#
var_list.append(deltaPhi_jj)#

#other#
SF_Fake                     =   array.array('f', [1.])
var_list.append(SF_Fake)
HLT_effLumi                 =   array.array('f', [-999.])
var_list.append(HLT_effLumi)
deltaEta_jj                 =   array.array('f', [-999.])#
var_list.append(deltaEta_jj)

#cut variables
pass_lepton_selection       =   array.array('i', [0])
pass_lepton_iso             =   array.array('i', [0])
pass_lepton_veto            =   array.array('i', [0])
pass_tau_selection          =   array.array('i', [0])
pass_tau_vsJetWP            =   array.array('i', [0])
pass_charge_selection       =   array.array('i', [0])
pass_jet_selection          =   array.array('i', [0])
pass_b_veto                 =   array.array('i', [0])
pass_mjj_cut                =   array.array('i', [0])
pass_MET_cut                =   array.array('i', [0])
pass_upToBVeto              =   array.array('i', [0])
#pass_upToBVeto_ML           =   array.array('i', [0])#
#pass_tau_selection_ML       =   array.array('i', [0])#
pass_everyCut               =   array.array('i', [0])
var_list.append(pass_lepton_selection)
var_list.append(pass_lepton_veto)
var_list.append(pass_lepton_iso)
var_list.append(pass_tau_selection)
#var_list.append(pass_tau_selection_ML)#
var_list.append(pass_tau_vsJetWP)
var_list.append(pass_charge_selection)
var_list.append(pass_jet_selection)
var_list.append(pass_b_veto)
var_list.append(pass_mjj_cut)
var_list.append(pass_MET_cut)
var_list.append(pass_upToBVeto)
#var_list.append(pass_upToBVeto_ML)#
var_list.append(pass_everyCut)

#wieghts#
w_PDF_all = array.array('f', [0.]*110)#
w_nominal_all = array.array('f', [0.])

#branches added for ssWW analysis
#lepton
systTree.branchTreesSysts(trees, "all", "lepton_pt",            outTreeFile, lepton_pt)
systTree.branchTreesSysts(trees, "all", "lepton_eta",           outTreeFile, lepton_eta)
systTree.branchTreesSysts(trees, "all", "lepton_phi",           outTreeFile, lepton_phi)
systTree.branchTreesSysts(trees, "all", "lepton_mass",          outTreeFile, lepton_mass)
systTree.branchTreesSysts(trees, "all", "lepton_pdgid",         outTreeFile, lepton_pdgid)
systTree.branchTreesSysts(trees, "all", "lepton_pfRelIso04",    outTreeFile, lepton_pfRelIso04)
systTree.branchTreesSysts(trees, "all", "lepton_TightRegion",   outTreeFile, lepton_TightRegion)
systTree.branchTreesSysts(trees, "all", "lepton_LnTRegion",     outTreeFile, lepton_LnTRegion)
systTree.branchTreesSysts(trees, "all", "lepton_SFFake",        outTreeFile, lepton_SFFake)
systTree.branchTreesSysts(trees, "all", "lepton_isPrompt",        outTreeFile, lepton_isPrompt)

#tau variables
systTree.branchTreesSysts(trees, "all", "tau_pt",               outTreeFile, tau_pt)
systTree.branchTreesSysts(trees, "all", "tau_eta",              outTreeFile, tau_eta)
systTree.branchTreesSysts(trees, "all", "tau_phi",              outTreeFile, tau_phi)
systTree.branchTreesSysts(trees, "all", "tau_mass",             outTreeFile, tau_mass)
systTree.branchTreesSysts(trees, "all", "tau_DeepTau_WP",             outTreeFile, tau_DeepTau_WP)
systTree.branchTreesSysts(trees, "all", "tau_isolation",             outTreeFile, tau_isolation)
systTree.branchTreesSysts(trees, "all", "tau_DeepTauVsEle_WP",      outTreeFile, tau_DeepTauVsEle_WP)#
systTree.branchTreesSysts(trees, "all", "tau_DeepTauVsEle_raw",     outTreeFile, tau_DeepTauVsEle_raw)#
systTree.branchTreesSysts(trees, "all", "tau_DeepTauVsMu_WP",       outTreeFile, tau_DeepTauVsMu_WP)#
systTree.branchTreesSysts(trees, "all", "tau_DeepTauVsMu_raw",      outTreeFile, tau_DeepTauVsMu_raw)#
systTree.branchTreesSysts(trees, "all", "tau_DeepTauVsJet_WP",      outTreeFile, tau_DeepTauVsJet_WP)#
systTree.branchTreesSysts(trees, "all", "tau_TightRegion",          outTreeFile, tau_TightRegion)#
systTree.branchTreesSysts(trees, "all", "tau_LnTRegion",            outTreeFile, tau_LnTRegion)#
systTree.branchTreesSysts(trees, "all", "tau_SFFake",               outTreeFile, tau_SFFake)#
systTree.branchTreesSysts(trees, "all", "tau_isPrompt",               outTreeFile, tau_isPrompt)#
systTree.branchTreesSysts(trees, "all", "event_SFFake",               outTreeFile, event_SFFake)#
#jet variables
systTree.branchTreesSysts(trees, "all", "leadjet_pt",           outTreeFile, leadjet_pt)
systTree.branchTreesSysts(trees, "all", "leadjet_eta",          outTreeFile, leadjet_eta)
systTree.branchTreesSysts(trees, "all", "leadjet_phi",          outTreeFile, leadjet_phi)
systTree.branchTreesSysts(trees, "all", "leadjet_mass",         outTreeFile, leadjet_mass)
systTree.branchTreesSysts(trees, "all", "leadjet_DeepFlv_b",    outTreeFile, leadjet_DeepFlv_b)
systTree.branchTreesSysts(trees, "all", "subleadjet_pt",           outTreeFile, subleadjet_pt)
systTree.branchTreesSysts(trees, "all", "subleadjet_eta",          outTreeFile, subleadjet_eta)
systTree.branchTreesSysts(trees, "all", "subleadjet_phi",          outTreeFile, subleadjet_phi)
systTree.branchTreesSysts(trees, "all", "subleadjet_mass",         outTreeFile, subleadjet_mass)
systTree.branchTreesSysts(trees, "all", "subleadjet_DeepFlv_b",    outTreeFile, subleadjet_DeepFlv_b)
systTree.branchTreesSysts(trees, "all", "nJets",  outTreeFile, nJets)
systTree.branchTreesSysts(trees, "all", "nBJets", outTreeFile, nBJets)#
#MET
systTree.branchTreesSysts(trees, "all", "MET_pt",               outTreeFile, MET_pt)
systTree.branchTreesSysts(trees, "all", "MET_phi",              outTreeFile, MET_phi)
#masses#
systTree.branchTreesSysts(trees, "all", "mjj",                  outTreeFile, mjj)
systTree.branchTreesSysts(trees, "all", "mT_lep_MET",                  outTreeFile, mT_lep_MET)
#deltaPhi#
systTree.branchTreesSysts(trees, "all", "deltaPhi_jj",              outTreeFile, deltaPhi_jj)#
#other                                                                                    
systTree.branchTreesSysts(trees, "all", "deltaEta_jj",              outTreeFile, deltaEta_jj)#
systTree.branchTreesSysts(trees, "all", "SF_Fake",                  outTreeFile, SF_Fake)#
systTree.branchTreesSysts(trees, "all", "HLT_effLumi",              outTreeFile, HLT_effLumi)#
#zeppenfeld
systTree.branchTreesSysts(trees, "all", "lepton_Zeppenfeld",              outTreeFile, lepton_Zeppenfeld)#
systTree.branchTreesSysts(trees, "all", "lepton_Zeppenfeld_over_deltaEta_jj",              outTreeFile, lepton_Zeppenfeld_over_deltaEta_jj)#
systTree.branchTreesSysts(trees, "all", "tau_Zeppenfeld",              outTreeFile, tau_Zeppenfeld)#
systTree.branchTreesSysts(trees, "all", "tau_Zeppenfeld_over_deltaEta_jj",              outTreeFile, tau_Zeppenfeld_over_deltaEta_jj)#
systTree.branchTreesSysts(trees, "all", "event_Zeppenfeld",              outTreeFile, event_Zeppenfeld)#
systTree.branchTreesSysts(trees, "all", "event_Zeppenfeld_over_deltaEta_jj",              outTreeFile, event_Zeppenfeld_over_deltaEta_jj)#
#cut variables
systTree.branchTreesSysts(trees, "all", "pass_lepton_selection",    outTreeFile, pass_lepton_selection)
systTree.branchTreesSysts(trees, "all", "pass_lepton_iso",          outTreeFile, pass_lepton_iso)
systTree.branchTreesSysts(trees, "all", "pass_lepton_veto",         outTreeFile, pass_lepton_veto)
systTree.branchTreesSysts(trees, "all", "pass_tau_selection",       outTreeFile, pass_tau_selection)
#systTree.branchTreesSysts(trees, "all", "pass_tau_selection_ML",       outTreeFile, pass_tau_selection_ML)#
systTree.branchTreesSysts(trees, "all", "pass_tau_vsJetWP",         outTreeFile, pass_tau_vsJetWP)
systTree.branchTreesSysts(trees, "all", "pass_charge_selection",    outTreeFile, pass_charge_selection)
systTree.branchTreesSysts(trees, "all", "pass_jet_selection",       outTreeFile, pass_jet_selection)
systTree.branchTreesSysts(trees, "all", "pass_b_veto",              outTreeFile, pass_b_veto)
systTree.branchTreesSysts(trees, "all", "pass_mjj_cut",             outTreeFile, pass_mjj_cut)
systTree.branchTreesSysts(trees, "all", "pass_MET_cut",             outTreeFile, pass_MET_cut)
systTree.branchTreesSysts(trees, "all", "pass_upToBVeto",           outTreeFile, pass_upToBVeto)
#systTree.branchTreesSysts(trees, "all", "pass_upToBVeto_ML",           outTreeFile, pass_upToBVeto_ML)#
systTree.branchTreesSysts(trees, "all", "pass_everyCut",            outTreeFile, pass_everyCut)


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

trigtype = sys.argv[5]

if not isMC:
    if 'DataEle' in sample.label or 'DataMu' in sample.label:
        trigtype = 'Lep'
    elif 'DataHT' in sample.label:
        trigtype = 'HT'

contagood=0
#++++++++++++++++++++++++++++++++++
#++   looping over the events    ++
#++++++++++++++++++++++++++++++++++
for i in range(tree.GetEntries()):
    #reinizializza tutte le variabili a 0, per sicurezza
    for j, var in enumerate(var_list):
        if j<len(var_list)-12:#
            var_list[j][0] = -999
        else:
            var_list[j][0] = 0
    SF_Fake[0]=1

    w_nominal_all[0] = 1.
    #++++++++++++++++++++++++++++++++++
    #++        taking objects        ++
    #++++++++++++++++++++++++++++++++++
    
    if Debug:
        print("evento n. " + str(i))
        if i > 2000:
            break
    
    if not Debug and i%500 == 0:#
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
        if not ("WZ" in sample.label or "WWTo2L2Nu_DoubleScattering"):
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

    dataEle = False
    dataMu = False
    dataHT = False
    if 'DataMu' in sample.label:
        dataMu = True
    elif 'DataEle' in sample.label:
        dataEle = True
    elif 'DataHT' in sample.label:
        dataHT = True

    if not isMC:
        if not Flag.eeBadScFilter:
            continue

    #print "------ ", i
    passMu, passEle, passHT, noTrigger = trig_map(HLT, PV, year, runPeriod)

    if noTrigger: continue

    if trigtype == 'HT' and not passHT:
        continue
    
    if trigtype == 'Lep' and not (passEle or passMu):
        continue

    SingleEle=False
    SingleMu=False
    ElMu=False

    HighestLepPt=-999.
    LeadLepFamily="not selected"
    
    if trigtype == 'Lep':
        if passEle and not passMu:
            if len(electrons)>0:  
                SingleEle=True
                LeadLepFamily="electrons"
                HighestLepPt=copy.deepcopy(electrons[0].pt)
                #print("HighestLepPt:", HighestLepPt)
            else:
                continue

        elif passMu and not passEle:
            if len(muons)>0:
                SingleMu=True
                LeadLepFamily="muons"
                HighestLepPt=copy.deepcopy(muons[0].pt)
            else:
                continue

        elif passMu and passEle:
            ElMu=True

        if ElMu:
            for mu in muons:
                if abs(mu.pt)>HighestLepPt:
                    HighestLepPt=copy.deepcopy(mu.pt)
                    SingleEle = False
                    SingleMu = True
                    break
            for ele in electrons:
                if abs(ele.pt)>HighestLepPt:
                    HighestLepPt=copy.deepcopy(ele.pt)
                    SingleEle = True
                    SingleMu = False
                    break

    elif trigtype == 'HT':
        ElMu = True
        for mu in muons:
            if abs(mu.pt)>HighestLepPt:
                HighestLepPt=copy.deepcopy(mu.pt)
                SingleEle = False
                SingleMu = True
                break
        for ele in electrons:
            if abs(ele.pt)>HighestLepPt:
                HighestLepPt=copy.deepcopy(ele.pt)
                SingleEle = True
                SingleMu = False
                break

    leptons = None

    vTrigEle, vTrigMu, vTrigHT = trig_finder(HLT, sample.year, sample.label)


    if SingleEle==True:
        if isMC:
            if trigtype == 'Lep':
                HLT_effLumi[0] = lumiFinder("Ele", vTrigEle)
            elif trigtype == 'HT':
                HLT_effLumi[0] = lumiFinder("HT", vTrigEle)
        leptons = electrons
    elif SingleMu==True:
        if isMC:
            if trigtype == 'Lep':
                HLT_effLumi[0] = lumiFinder("Mu", vTrigMu)
            elif trigtype == 'HT':
                HLT_effLumi[0] = lumiFinder("HT", vTrigEle)
        leptons = muons
    
    elif not (SingleMu or SingleEle):
        continue

    if SingleEle and dataMu:
        continue
    if SingleMu and dataEle:
        continue
 
    MET_pt[0]   =   met.pt  
    MET_phi[0]  =   met.phi

    indexGoodLep, lepton_TightRegion[0] = SelectLepton(leptons, SingleMu) 
    
    if lepton_TightRegion[0]==1:    lepton_LnTRegion[0] = 0
    elif lepton_TightRegion[0]==0:  lepton_LnTRegion[0] = 1
    else: lepton_LnTRegion[0] = -999


    if indexGoodLep<0 or indexGoodLep>=len(leptons) or (lepton_TightRegion[0]<0 and lepton_LnTRegion[0]<0): 
        #systTree.setWeightName("w_nominal",copy.deepcopy(w_nominal_all[0]))
        #systTree.fillTreesSysts(trees, "all")
        continue

    if lepton_TightRegion[0]==1 or lepton_LnTRegion[0]==1:
        pass_lepton_selection[0] = 1
    else:
        pass_lepton_selection[0] = 0

    tightlep = leptons[indexGoodLep]

    lepton_pt[0]                =   tightlep.pt
    lepton_eta[0]               =   tightlep.eta
    lepton_phi[0]               =   tightlep.phi
    lepton_mass[0]              =   tightlep.mass
    lepton_pdgid[0]             =   tightlep.pdgId
    if SingleMu==1:
        lepton_pfRelIso04[0]        =   tightlep.pfRelIso04_all
    elif SingleEle==1:
        lepton_pfRelIso04[0]        =   tightlep.jetRelIso


    lepton_SFFake[0] = SFFakeRatio_ele_calc(lepton_pt[0], lepton_eta[0])

    if isMC:
        lepton_isPrompt[0] = tightlep.genPartFlav

    GoodLep=tightlep
    
    mT_lep_MET[0]=mTlepMet(met, tightlep.p4())

    if isMC:
        tightlep_SF = tightlep.effSF
        tightlep_SFUp = tightlep.effSF_errUp
        tightlep_SFDown = tightlep.effSF_errDown
        systTree.setWeightName("lepSF", copy.deepcopy(tightlep_SF))
        systTree.setWeightName("lepUp", copy.deepcopy(tightlep_SFUp))
        systTree.setWeightName("lepDown", copy.deepcopy(tightlep_SFDown))

        PF_SF = chain.PrefireWeight
        PF_SFUp = chain.PrefireWeight_Up
        PF_SFDown = chain.PrefireWeight_Down
        systTree.setWeightName("PFSF", copy.deepcopy(PF_SF))
        systTree.setWeightName("PFUp", copy.deepcopy(PF_SFUp))
        systTree.setWeightName("PFDown", copy.deepcopy(PF_SFDown))

        PU_SF = chain.puWeight
        PU_SFUp = chain.puWeightUp
        PU_SFDown = chain.puWeightDown
        systTree.setWeightName("puSF", copy.deepcopy(PU_SF))
        systTree.setWeightName("puUp", copy.deepcopy(PU_SFUp))
        systTree.setWeightName("puDown", copy.deepcopy(PU_SFDown))

    if abs(lepton_pdgid[0])==11 and lepton_pfRelIso04[0]<ISO_CUT_ELE:   pass_lepton_iso[0]=1
    elif abs(lepton_pdgid[0])==13 and lepton_pfRelIso04[0]<ISO_CUT_MU:  pass_lepton_iso[0]=1
    else: pass_lepton_iso[0]=0
    
    pass_lepton_veto[0]=LepVeto(GoodLep, electrons, muons)
    
    DeepTauVsEle = ID_TAU_RECO_DEEPTAU_VSELE#
    DeepTauVsMu = ID_TAU_RECO_DEEPTAU_VSMU#
    DeepTauVsJet = ID_TAU_RECO_DEEPTAU_VSJET#
    
    indexGoodTau, tau_TightRegion[0] = SelectTau(list(taus), tightlep, DeepTauVsEle, DeepTauVsMu, DeepTauVsJet)
    if tau_TightRegion[0] == 1 : tau_LnTRegion[0] = 0
    elif tau_TightRegion[0] == 0 : tau_LnTRegion[0] = 1
    else:
        tau_LnTRegion[0] = -999


    if indexGoodTau<0 or indexGoodTau>=len(taus) or (tau_TightRegion[0]<0 and tau_LnTRegion[0]<0): 
        #systTree.setWeightName("w_nominal",copy.deepcopy(w_nominal_all[0]))
        #systTree.fillTreesSysts(trees, "all")
        continue      
    

    GoodTau=taus[indexGoodTau]
    #pass_tau_selection_ML[0]=1#

    if tau_TightRegion[0]==1 or tau_LnTRegion[0]==1:
        pass_tau_selection[0] = 1
    else:
        pass_tau_selection[0] = 0
    
    tau_pt[0]               =   GoodTau.pt
    tau_eta[0]              =   GoodTau.eta
    tau_phi[0]              =   GoodTau.phi
    tau_mass[0]             =   GoodTau.mass
    tau_charge[0]           =   GoodTau.charge

    tau_SFFake[0] = SFFakeRatio_tau_calc(tau_pt[0], tau_eta[0])

    if isMC:
        tau_isPrompt[0] = GoodTau.genPartFlav

    tau_DeepTau_WP[0] = GoodTau.idDeepTau2017v2p1VSjet*1000.**2. + GoodTau.idDeepTau2017v2p1VSmu*1000. + GoodTau.idDeepTau2017v2p1VSe
    if GoodTau.idDeepTau2017v2p1VSe+1 > 0.:
        tau_DeepTauVsEle_WP[0]  =   math.log(GoodTau.idDeepTau2017v2p1VSe+1, 2)#
    else:
        tau_DeepTauVsEle_WP[0]  =  0.
    tau_DeepTauVsEle_raw[0] =   GoodTau.rawDeepTau2017v2p1VSe#

    if GoodTau.idDeepTau2017v2p1VSmu+1 > 0.:
        tau_DeepTauVsMu_WP[0]   =   math.log(GoodTau.idDeepTau2017v2p1VSmu+1, 2)#
    else:
        tau_DeepTauVsMu_WP[0]   =   0.
    tau_DeepTauVsMu_raw[0]  =   GoodTau.rawDeepTau2017v2p1VSmu#

    if GoodTau.idDeepTau2017v2p1VSjet+1 > 0.:
        tau_DeepTauVsJet_WP[0]  =   math.log(GoodTau.idDeepTau2017v2p1VSjet+1, 2)#
    else:
        tau_DeepTauVsJet_WP[0]  =   0.
    tau_DeepTauVsJet_raw[0] =   GoodTau.rawDeepTau2017v2p1VSjet#

    tau_isolation[0]=   GoodTau.neutralIso
    m_leptau=(GoodTau.p4() + tightlep.p4()).M()

    if lepton_LnTRegion[0]==1 and tau_LnTRegion[0]==0:
        event_SFFake[0] = lepton_SFFake[0]
    elif lepton_LnTRegion[0]==0 and tau_LnTRegion[0]==1:
        event_SFFake[0] = tau_SFFake[0]
    elif lepton_LnTRegion[0]==1 and tau_LnTRegion[0]==1:
        event_SFFake[0] = lepton_SFFake[0]*tau_SFFake[0]
    elif lepton_LnTRegion[0]==0 and tau_LnTRegion[0]==0:
        event_SFFake[0] = 0.

    if GoodTau.charge==GoodLep.charge:
        pass_charge_selection[0]=1

    nJets[0] = len(jets)
    nBJets[0] = CountBJets(jets)#

    outputJetSel=SelectJet(list(jets), GoodTau, GoodLep)
    
    if outputJetSel==-999:
        #systTree.setWeightName("w_nominal",copy.deepcopy(w_nominal_all[0]))
        #systTree.fillTreesSysts(trees, "all")
        continue  

    jet1, jet2 = outputJetSel
    
    leadjet_pt[0]               =   jet1.pt
    leadjet_eta[0]              =   jet1.eta
    leadjet_phi[0]              =   jet1.phi
    leadjet_mass[0]             =   jet1.mass
    leadjet_DeepFlv_b[0]        =   jet1.btagDeepFlavB
    subleadjet_pt[0]            =   jet2.pt
    subleadjet_eta[0]           =   jet2.eta
    subleadjet_phi[0]           =   jet2.phi
    subleadjet_mass[0]          =   jet2.mass
    subleadjet_DeepFlv_b[0]     =   jet2.btagDeepFlavB
    
    pass_jet_selection[0]=1

    #calculating deltaPhi                                                                                                      
    deltaPhi_jj[0]      =   deltaPhi(jet1, jet2)#

    lepton_Zeppenfeld[0], tau_Zeppenfeld[0], event_Zeppenfeld[0] = Zeppenfeld(lepton_eta[0], tau_eta[0], leadjet_eta[0], subleadjet_eta[0])

    if not BVeto(jets): pass_b_veto[0]=1

    if (SingleEle or SingleMu) and pass_lepton_selection[0]==1 and pass_lepton_veto[0]==1 and pass_tau_selection[0]==1 and pass_charge_selection[0]==1 and pass_jet_selection[0]==1 and pass_b_veto[0]==1: pass_upToBVeto[0]=1#

    leadJet=ROOT.TLorentzVector()
    subleadJet=ROOT.TLorentzVector()
    leadJet.SetPtEtaPhiM(jet1.pt, jet1.eta, jet1.phi, jet1.mass)
    subleadJet.SetPtEtaPhiM(jet2.pt, jet2.eta, jet2.phi, jet2.mass) 
    
    if not JetCut(leadJet, subleadJet): pass_mjj_cut[0]=1

    mjj[0]=(leadJet+subleadJet).M()
    deltaEta_jj[0]=abs(leadJet.Eta()-subleadJet.Eta())
    lepton_Zeppenfeld_over_deltaEta_jj[0] = lepton_Zeppenfeld[0]/deltaEta_jj[0]
    tau_Zeppenfeld_over_deltaEta_jj[0] = tau_Zeppenfeld[0]/deltaEta_jj[0]
    lepton_Zeppenfeld_over_deltaEta_jj[0] = event_Zeppenfeld[0]/deltaEta_jj[0]

    if not metCut(met): pass_MET_cut[0]=1

    if (SingleEle or SingleMu) and pass_lepton_selection[0]==1 and pass_lepton_veto[0]==1 and pass_tau_selection[0]==1 and pass_charge_selection[0]==1 and pass_jet_selection[0]==1 and pass_b_veto[0]==1 and pass_mjj_cut[0]==1 and pass_MET_cut[0]==1:
        pass_everyCut[0]=1

    #######################################
    ## Removing events with HEM problem  ##
    #######################################
    passesMETHEMVeto = HEMveto(jets, electrons)
    if(sample.year == 2018 and not passesMETHEMVeto):
        if(not isMC and chain.run > 319077.):
            continue
        elif(isMC):
            w_nominal_all[0] *= 0.354

    systTree.setWeightName("w_nominal",copy.deepcopy(w_nominal_all[0]))
    systTree.fillTreesSysts(trees, "all")


outTreeFile.cd()
if(isMC):
    h_genweight.Write()
    if isthere_pdf:
        h_PDFweight.Write()

systTree.writeTreesSysts(trees, outTreeFile)
print("Number of events in output tree " + str(trees[0].GetEntries()))

endTime = datetime.datetime.now()
print("Ending running at " + str(endTime) + "\n Goodbye")
