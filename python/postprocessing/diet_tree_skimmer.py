#!/bin/env python3
import os
import sys
import ROOT
import math
import datetime
import copy
from array import array
from diet_skimtree_utils import *
from TauIDSFTool import TauIDSFTool, TauESTool, TauFESTool, campaigns
from EFTOperator_dict import *

dim8_points = [
    "20",
    "10",
    "0",
]

vsJet = {"VVVL": 'VVVLoose',
         "VVL": 'VVLoose',
         "VL": 'VLoose',
         "L": 'Loose',
         "M": 'Medium',
         "T": 'Tight',
         "VT": 'VTight',
         "VVT": 'VVTight',
}

vsMu = {"VL": 'VLoose',
        "L": 'Loose',
        "M": 'Medium',
        "T": 'Tight'
}

vsEle = {"VVVL": 'VVVLoose',
         "VVL": 'VVLoose',
         "VL": 'VLoose',
         "L": 'Loose',
         "M": 'Medium',
         "T": 'Tight',
         "VT": 'VTight',
         "VVT": 'VVTight',
}

usage = "python diet_tree_skimmer.py [nome_del_sample_in_samples.py] 0 [file_in_input] local wpvsjet wpvsele wpvsmu"

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
'''
vsjetWP = vsJet[sys.argv[5]]
vseleWP = vsEle[sys.argv[6]]
vsmuWP = vsMu[sys.argv[7]]
'''
act_camp = ''

for cam in campaigns:
    if str(sample.year) in cam:
        act_camp = copy.deepcopy(cam)
        break
'''
tauSFTool_vsjet = TauIDSFTool(act_camp, 'DeepTau2017v2p1VSjet', vsjetWP)
tauSFTool_vsele = TauIDSFTool(act_camp, 'DeepTau2017v2p1VSe', vseleWP)
tauSFTool_vsmu = TauIDSFTool(act_camp, 'DeepTau2017v2p1VSmu', vsmuWP)
tesTool = TauESTool(act_camp, 'DeepTau2017v2p1VSjet')
fesTool = TauFESTool(act_camp, 'DeepTau2017v2p1VSe')
'''
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

IsDim8 = False

if 'aQGC' in sample.name:
    IsDim8 = True

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
systTree.setWeightName("tau_vsjet_SF",1.)
systTree.setWeightName("tau_vsjet_Up",1.)
systTree.setWeightName("tau_vsjet_Down",1.)
systTree.setWeightName("tau_vsele_SF",1.)
systTree.setWeightName("tau_vsele_Up",1.)
systTree.setWeightName("tau_vsele_Down",1.)
systTree.setWeightName("tau_vsmu_SF",1.)
systTree.setWeightName("tau_vsmu_Up",1.)
systTree.setWeightName("tau_vsmu_Down",1.)
systTree.setWeightName("tauSF",1.)
systTree.setWeightName("tauUp",1.)
systTree.setWeightName("tauDown",1.)
systTree.setWeightName("TESSF",1.)
systTree.setWeightName("TESUp",1.)
systTree.setWeightName("TESDown",1.)
systTree.setWeightName("FESSF",1.)
systTree.setWeightName("FESUp",1.)
systTree.setWeightName("FESDown",1.)

#++++++++++++++++++++++++++++++++++
#++     variables to branch      ++
#++++++++++++++++++++++++++++++++++
var_list = []
#++++++++++++++++++++++++++++++++++
#++        dim8 operator         ++
#++++++++++++++++++++++++++++++++++

if IsDim8:
    w_dim8                              =   array.array('f', [-999.])
    w_neg                               =   array.array('f', [-999.])
    w_pos                               =   array.array('f', [-999.])
    var_list.append(w_dim8)
    var_list.append(w_neg)
    var_list.append(w_pos)
    
#++++++++++++++++++++++++++++++++++
#++         All category         ++
#++++++++++++++++++++++++++++++++++

#ssWW variables

#electron#
electron_pt                                 =   array.array('f', [-999.])
electron_eta                                =   array.array('f', [-999.])
electron_phi                                =   array.array('f', [-999.])
electron_mass                               =   array.array('f', [-999.])
electron_pdgid                              =   array.array('i', [-999])
electron_pfRelIso04                         =   array.array('f', [-999.])
electron_TightRegion                        =   array.array('i', [-999])
electron_LnTRegion                          =   array.array('i', [-999])
electron_SFFake_vsjet2                      =   array.array('f', [-999.])
electron_SFFake_vsjet4                      =   array.array('f', [-999.])
electron_isPrompt                           =   array.array('i', [-999])
electron_Zeppenfeld                         =   array.array('f', [-999])
electron_Zeppenfeld_over_deltaEta_jj        =   array.array('f', [-999])
var_list.append(electron_pt)
var_list.append(electron_eta)
var_list.append(electron_phi)
var_list.append(electron_mass)
var_list.append(electron_pdgid)
var_list.append(electron_pfRelIso04)
var_list.append(electron_TightRegion)
var_list.append(electron_LnTRegion)
var_list.append(electron_SFFake_vsjet2)
var_list.append(electron_SFFake_vsjet4)
var_list.append(electron_isPrompt)
var_list.append(electron_Zeppenfeld)
var_list.append(electron_Zeppenfeld_over_deltaEta_jj)

#muon#

muon_pt                                     =   array.array('f', [-999.])
muon_eta                                    =   array.array('f', [-999.])
muon_phi                                    =   array.array('f', [-999.])
muon_mass                                   =   array.array('f', [-999.])
muon_pdgid                                  =   array.array('i', [-999])
muon_pfRelIso04                             =   array.array('f', [-999.])
muon_TightRegion                            =   array.array('i', [-999])
muon_LnTRegion                              =   array.array('i', [-999])
muon_SFFake_vsjet2                          =   array.array('f', [-999.])
muon_SFFake_vsjet4                          =   array.array('f', [-999.])
muon_isPrompt                               =   array.array('i', [-999])
muon_Zeppenfeld                             =   array.array('f', [-999])
muon_Zeppenfeld_over_deltaEta_jj            =   array.array('f', [-999])
var_list.append(muon_pt)
var_list.append(muon_eta)
var_list.append(muon_phi)
var_list.append(muon_mass)
var_list.append(muon_pdgid)
var_list.append(muon_pfRelIso04)
var_list.append(muon_TightRegion)
var_list.append(muon_LnTRegion)
var_list.append(muon_SFFake_vsjet2)
var_list.append(muon_SFFake_vsjet4)
var_list.append(muon_isPrompt)
var_list.append(muon_Zeppenfeld)
var_list.append(muon_Zeppenfeld_over_deltaEta_jj)


event_Zeppenfeld                            =   array.array('f', [-999])
event_Zeppenfeld_over_deltaEta_jj           =   array.array('f', [-999])
var_list.append(event_Zeppenfeld)
var_list.append(event_Zeppenfeld_over_deltaEta_jj)

event_RT = array.array('f', [-999])
var_list.append(event_RT)

#event SFFake
event_SFFake_vsjet2                         =   array.array('f', [-999.])
event_SFFake_vsjet4                         =   array.array('f', [-999.])
var_list.append(event_SFFake_vsjet2)
var_list.append(event_SFFake_vsjet4)

#jet#
leadjet_pt                                  =   array.array('f', [-999.])
leadjet_eta                                 =   array.array('f', [-999.])
leadjet_phi                                 =   array.array('f', [-999.])
leadjet_mass                                =   array.array('f', [-999.])
leadjet_CSVv2_b                             =   array.array('f', [-999.])
leadjet_DeepFlv_b                           =   array.array('f', [-999.])
leadjet_DeepCSVv2_b                         =   array.array('f', [-999.])
nJets                                       =   array.array('f', [-999.])
nBJets                                      =   array.array('f', [-999.])
AK8leadjet_pt                               =   array.array('f', [-999.])
AK8leadjet_eta                              =   array.array('f', [-999.])
AK8leadjet_phi                              =   array.array('f', [-999.])
AK8leadjet_mass                             =   array.array('f', [-999.])
AK8leadjet_tau21                            =   array.array('f', [-999.])
AK8leadjet_tau32                            =   array.array('f', [-999.])
AK8leadjet_tau43                            =   array.array('f', [-999.])
leadjet_dRAK48                              =   array.array('f', [-999.])

var_list.append(leadjet_pt)
var_list.append(leadjet_eta)
var_list.append(leadjet_phi)
var_list.append(leadjet_mass)
var_list.append(leadjet_CSVv2_b)
var_list.append(leadjet_DeepFlv_b)
var_list.append(leadjet_DeepCSVv2_b)
var_list.append(nJets)#
var_list.append(nBJets)#
var_list.append(AK8leadjet_pt)
var_list.append(AK8leadjet_eta)
var_list.append(AK8leadjet_phi)
var_list.append(AK8leadjet_mass)
var_list.append(AK8leadjet_tau21)
var_list.append(AK8leadjet_tau32)
var_list.append(AK8leadjet_tau43)
var_list.append(leadjet_dRAK48)

subleadjet_pt                               =   array.array('f', [-999.])
subleadjet_eta                              =   array.array('f', [-999.])
subleadjet_phi                              =   array.array('f', [-999.])
subleadjet_mass                             =   array.array('f', [-999.])
subleadjet_CSVv2_b                          =   array.array('f', [-999.])
subleadjet_DeepFlv_b                        =   array.array('f', [-999.])
subleadjet_DeepCSVv2_b                      =   array.array('f', [-999.])
AK8subleadjet_pt                            =   array.array('f', [-999.])
AK8subleadjet_eta                           =   array.array('f', [-999.])
AK8subleadjet_phi                           =   array.array('f', [-999.])
AK8subleadjet_mass                          =   array.array('f', [-999.])
AK8subleadjet_tau21                         =   array.array('f', [-999.])
AK8subleadjet_tau32                         =   array.array('f', [-999.])
AK8subleadjet_tau43                         =   array.array('f', [-999.])
subleadjet_dRAK48                           =   array.array('f', [-999.])

var_list.append(subleadjet_pt)
var_list.append(subleadjet_eta)
var_list.append(subleadjet_phi)
var_list.append(subleadjet_mass)
var_list.append(subleadjet_CSVv2_b)
var_list.append(subleadjet_DeepFlv_b)
var_list.append(subleadjet_DeepCSVv2_b)
var_list.append(AK8subleadjet_pt)
var_list.append(AK8subleadjet_eta)
var_list.append(AK8subleadjet_phi)
var_list.append(AK8subleadjet_mass)
var_list.append(AK8subleadjet_tau21)
var_list.append(AK8subleadjet_tau32)
var_list.append(AK8subleadjet_tau43)
var_list.append(subleadjet_dRAK48)

#MET
MET_pt                                      =   array.array('f', [-999.])
MET_phi                                     =   array.array('f', [-999.])
var_list.append(MET_pt)
var_list.append(MET_phi)

#inv and transv masses
m_jjelectron                                =   array.array('f', [-999.])
m_jjmuon                                    =   array.array('f', [-999.])
m_jjleps                                    =   array.array('f', [-999.])
m_jj                                        =   array.array('f', [-999.])
m_1T                                        =   array.array('f', [-999.])
m_o1                                        =   array.array('f', [-999.])
m_electronmuon                              =   array.array('f', [-999.])
mT_electron_MET                             =   array.array('f', [-999.])
mT_muon_MET                                 =   array.array('f', [-999.])
mT_electronmuon_MET                         =   array.array('f', [-999.])
var_list.append(m_jjelectron)
var_list.append(m_jjmuon)
var_list.append(m_jjleps)
var_list.append(m_jj)
var_list.append(m_1T)
var_list.append(m_o1)
var_list.append(m_electronmuon)
var_list.append(mT_electron_MET)
var_list.append(mT_muon_MET)
var_list.append(mT_electronmuon_MET)

#deltaPhi#                                                                      
deltaPhi_jj                                 =   array.array('f', [-999.])
deltaPhi_electronmuon                       =   array.array('f', [-999.])
deltaPhi_electronj1                         =   array.array('f', [-999.])
deltaPhi_electronj2                         =   array.array('f', [-999.])
deltaPhi_muonj1                             =   array.array('f', [-999.])
deltaPhi_muonj2                             =   array.array('f', [-999.])
var_list.append(deltaPhi_jj)
var_list.append(deltaPhi_electronmuon)
var_list.append(deltaPhi_electronj1)
var_list.append(deltaPhi_electronj2)
var_list.append(deltaPhi_muonj1)
var_list.append(deltaPhi_muonj2)

#deltaTheta
deltaTheta_jj                               =   array.array('f', [-999.])
deltaTheta_electronmuon                     =   array.array('f', [-999.])
deltaTheta_electronj1                       =   array.array('f', [-999.])
deltaTheta_electronj2                       =   array.array('f', [-999.])
deltaTheta_muonj1                           =   array.array('f', [-999.])
deltaTheta_muonj2                           =   array.array('f', [-999.])
var_list.append(deltaTheta_jj)
var_list.append(deltaTheta_electronmuon)
var_list.append(deltaTheta_electronj1)
var_list.append(deltaTheta_electronj2)
var_list.append(deltaTheta_muonj1)
var_list.append(deltaTheta_muonj2)

#ptRel
ptRel_jj                                    =   array.array('f', [-999.])#
ptRel_electronmuon                          =   array.array('f', [-999.])#
ptRel_electronj1                            =   array.array('f', [-999.])#
ptRel_electronj2                            =   array.array('f', [-999.])#
ptRel_muonj1                                =   array.array('f', [-999.])#
ptRel_muonj2                                =   array.array('f', [-999.])#
var_list.append(ptRel_jj)
var_list.append(ptRel_electronmuon)
var_list.append(ptRel_electronj1)
var_list.append(ptRel_electronj2)
var_list.append(ptRel_muonj1)
var_list.append(ptRel_muonj2)

#deltaEta#                                                                      
deltaEta_jj                                 =   array.array('f', [-999.])#
deltaEta_electronmuon                       =   array.array('f', [-999.])#
deltaEta_electronj1                         =   array.array('f', [-999.])#
deltaEta_electronj2                         =   array.array('f', [-999.])#
deltaEta_muonj1                             =   array.array('f', [-999.])#
deltaEta_muonj2                             =   array.array('f', [-999.])#
var_list.append(deltaEta_jj)
var_list.append(deltaEta_electronmuon)
var_list.append(deltaEta_electronj1)
var_list.append(deltaEta_electronj2)
var_list.append(deltaEta_muonj1)
var_list.append(deltaEta_muonj2)

#other#
SF_Fake                                     =   array.array('f', [1.])
HLT_effLumi                                 =   array.array('f', [-999.])
var_list.append(SF_Fake)
var_list.append(HLT_effLumi)

#cut variables
pass_lepton_selection                       =   array.array('i', [0])
pass_lepton_iso                             =   array.array('i', [0])
pass_lepton_veto                            =   array.array('i', [0])
pass_tau_selection                          =   array.array('i', [0])
pass_tau_vsJetWP                            =   array.array('i', [0])
pass_charge_selection                       =   array.array('i', [0])
pass_jet_selection                          =   array.array('i', [0])
pass_b_veto                                 =   array.array('i', [0])
pass_tau_veto                               =   array.array('i', [0])
pass_mjj_cut                                =   array.array('i', [0])
pass_MET_cut                                =   array.array('i', [0])
pass_upToBVeto                              =   array.array('i', [0])
pass_everyCut                               =   array.array('i', [0])
var_list.append(pass_lepton_selection)
var_list.append(pass_lepton_veto)
var_list.append(pass_lepton_iso)
var_list.append(pass_tau_selection)
var_list.append(pass_tau_vsJetWP)
var_list.append(pass_charge_selection)
var_list.append(pass_jet_selection)
var_list.append(pass_b_veto)
var_list.append(pass_tau_veto)
var_list.append(pass_mjj_cut)
var_list.append(pass_MET_cut)
var_list.append(pass_upToBVeto)
var_list.append(pass_everyCut)

#weights#
w_PDF_all = array.array('f', [0.]*110)#
w_nominal_all = array.array('f', [0.])

#w_dim8
if IsDim8:
    systTree.branchTreesSysts(trees, "all", "w_dim8",                               outTreeFile, w_dim8)
    systTree.branchTreesSysts(trees, "all", "w_pos",                                outTreeFile, w_pos)
    systTree.branchTreesSysts(trees, "all", "w_neg",                                outTreeFile, w_neg)

#branches added for ssWW analysis
#leading lepton
systTree.branchTreesSysts(trees, "all", "electron_pt",                              outTreeFile, electron_pt)
systTree.branchTreesSysts(trees, "all", "electron_eta",                             outTreeFile, electron_eta)
systTree.branchTreesSysts(trees, "all", "electron_phi",                             outTreeFile, electron_phi)
systTree.branchTreesSysts(trees, "all", "electron_mass",                            outTreeFile, electron_mass)
systTree.branchTreesSysts(trees, "all", "electron_pdgid",                           outTreeFile, electron_pdgid)
systTree.branchTreesSysts(trees, "all", "electron_pfRelIso04",                      outTreeFile, electron_pfRelIso04)
systTree.branchTreesSysts(trees, "all", "electron_TightRegion",                     outTreeFile, electron_TightRegion)
systTree.branchTreesSysts(trees, "all", "electron_LnTRegion",                       outTreeFile, electron_LnTRegion)
systTree.branchTreesSysts(trees, "all", "electron_SFFake_vsjet2",                   outTreeFile, electron_SFFake_vsjet2)
systTree.branchTreesSysts(trees, "all", "electron_SFFake_vsjet4",                   outTreeFile, electron_SFFake_vsjet4)
systTree.branchTreesSysts(trees, "all", "electron_isPrompt",                        outTreeFile, electron_isPrompt)

#subleading lepton
systTree.branchTreesSysts(trees, "all", "muon_pt",                                  outTreeFile, muon_pt)
systTree.branchTreesSysts(trees, "all", "muon_eta",                                 outTreeFile, muon_eta)
systTree.branchTreesSysts(trees, "all", "muon_phi",                                 outTreeFile, muon_phi)
systTree.branchTreesSysts(trees, "all", "muon_mass",                                outTreeFile, muon_mass)
systTree.branchTreesSysts(trees, "all", "muon_pdgid",                               outTreeFile, muon_pdgid)
systTree.branchTreesSysts(trees, "all", "muon_pfRelIso04",                          outTreeFile, muon_pfRelIso04)
systTree.branchTreesSysts(trees, "all", "muon_TightRegion",                         outTreeFile, muon_TightRegion)
systTree.branchTreesSysts(trees, "all", "muon_LnTRegion",                           outTreeFile, muon_LnTRegion)
systTree.branchTreesSysts(trees, "all", "muon_SFFake_vsjet2",                       outTreeFile, muon_SFFake_vsjet2)
systTree.branchTreesSysts(trees, "all", "muon_SFFake_vsjet4",                       outTreeFile, muon_SFFake_vsjet4)
systTree.branchTreesSysts(trees, "all", "muon_isPrompt",                            outTreeFile, muon_isPrompt)

#jet variables
systTree.branchTreesSysts(trees, "all", "leadjet_pt",                               outTreeFile, leadjet_pt)
systTree.branchTreesSysts(trees, "all", "leadjet_eta",                              outTreeFile, leadjet_eta)
systTree.branchTreesSysts(trees, "all", "leadjet_phi",                              outTreeFile, leadjet_phi)
systTree.branchTreesSysts(trees, "all", "leadjet_mass",                             outTreeFile, leadjet_mass)
systTree.branchTreesSysts(trees, "all", "leadjet_CSVv2_b",                          outTreeFile, leadjet_CSVv2_b)
systTree.branchTreesSysts(trees, "all", "leadjet_DeepFlv_b",                        outTreeFile, leadjet_DeepFlv_b)
systTree.branchTreesSysts(trees, "all", "leadjet_DeepCSVv2_b",                      outTreeFile, leadjet_DeepCSVv2_b)
systTree.branchTreesSysts(trees, "all", "AK8leadjet_pt",                            outTreeFile, AK8leadjet_pt)
systTree.branchTreesSysts(trees, "all", "AK8leadjet_eta",                           outTreeFile, AK8leadjet_eta)
systTree.branchTreesSysts(trees, "all", "AK8leadjet_phi",                           outTreeFile, AK8leadjet_phi)
systTree.branchTreesSysts(trees, "all", "AK8leadjet_mass",                          outTreeFile, AK8leadjet_mass)
systTree.branchTreesSysts(trees, "all", "AK8leadjet_tau21",                         outTreeFile, AK8leadjet_tau21)
systTree.branchTreesSysts(trees, "all", "AK8leadjet_tau32",                         outTreeFile, AK8leadjet_tau32)
systTree.branchTreesSysts(trees, "all", "AK8leadjet_tau43",                         outTreeFile, AK8leadjet_tau43)
systTree.branchTreesSysts(trees, "all", "leadjet_dRAK48",                           outTreeFile, leadjet_dRAK48)
systTree.branchTreesSysts(trees, "all", "subleadjet_pt",                            outTreeFile, subleadjet_pt)
systTree.branchTreesSysts(trees, "all", "subleadjet_eta",                           outTreeFile, subleadjet_eta)
systTree.branchTreesSysts(trees, "all", "subleadjet_phi",                           outTreeFile, subleadjet_phi)
systTree.branchTreesSysts(trees, "all", "subleadjet_mass",                          outTreeFile, subleadjet_mass)
systTree.branchTreesSysts(trees, "all", "subleadjet_CSVv2_b",                       outTreeFile, subleadjet_CSVv2_b)
systTree.branchTreesSysts(trees, "all", "subleadjet_DeepFlv_b",                     outTreeFile, subleadjet_DeepFlv_b)
systTree.branchTreesSysts(trees, "all", "subleadjet_DeepCSVv2_b",                   outTreeFile, subleadjet_DeepCSVv2_b)
systTree.branchTreesSysts(trees, "all", "AK8subleadjet_pt",                         outTreeFile, AK8subleadjet_pt)
systTree.branchTreesSysts(trees, "all", "AK8subleadjet_eta",                        outTreeFile, AK8subleadjet_eta)
systTree.branchTreesSysts(trees, "all", "AK8subleadjet_phi",                        outTreeFile, AK8subleadjet_phi)
systTree.branchTreesSysts(trees, "all", "AK8subleadjet_mass",                       outTreeFile, AK8subleadjet_mass)
systTree.branchTreesSysts(trees, "all", "AK8subleadjet_tau21",                      outTreeFile, AK8subleadjet_tau21)
systTree.branchTreesSysts(trees, "all", "AK8subleadjet_tau32",                      outTreeFile, AK8subleadjet_tau32)
systTree.branchTreesSysts(trees, "all", "AK8subleadjet_tau43",                      outTreeFile, AK8subleadjet_tau43)
systTree.branchTreesSysts(trees, "all", "subleadjet_dRAK48",                        outTreeFile, subleadjet_dRAK48)
systTree.branchTreesSysts(trees, "all", "nJets",                                    outTreeFile, nJets)
systTree.branchTreesSysts(trees, "all", "nBJets",                                   outTreeFile, nBJets)

#MET
systTree.branchTreesSysts(trees, "all", "MET_pt",                                   outTreeFile, MET_pt)
systTree.branchTreesSysts(trees, "all", "MET_phi",                                  outTreeFile, MET_phi)

#masses#
systTree.branchTreesSysts(trees, "all", "m_jj",                                     outTreeFile, m_jj)
systTree.branchTreesSysts(trees, "all", "m_1T",                                     outTreeFile, m_1T)
systTree.branchTreesSysts(trees, "all", "m_o1",                                     outTreeFile, m_o1)
systTree.branchTreesSysts(trees, "all", "mT_electron_MET",                          outTreeFile, mT_electron_MET)
systTree.branchTreesSysts(trees, "all", "mT_muon_MET",                              outTreeFile, mT_muon_MET)
systTree.branchTreesSysts(trees, "all", "mT_electronmuon_MET",                      outTreeFile, mT_electronmuon_MET)
systTree.branchTreesSysts(trees, "all", "m_electronmuon",                           outTreeFile, m_electronmuon)
systTree.branchTreesSysts(trees, "all", "m_jjelectron",                             outTreeFile, m_jjelectron)
systTree.branchTreesSysts(trees, "all", "m_jjmuon",                                 outTreeFile, m_jjmuon)
systTree.branchTreesSysts(trees, "all", "m_jjleps",                                 outTreeFile, m_jjleps)

#deltaPhi
systTree.branchTreesSysts(trees, "all", "deltaPhi_jj",                              outTreeFile, deltaPhi_jj)
systTree.branchTreesSysts(trees, "all", "deltaPhi_electronmuon",                    outTreeFile, deltaPhi_electronmuon)
systTree.branchTreesSysts(trees, "all", "deltaPhi_electronj1",                      outTreeFile, deltaPhi_electronj1)
systTree.branchTreesSysts(trees, "all", "deltaPhi_electronj2",                      outTreeFile, deltaPhi_electronj2)
systTree.branchTreesSysts(trees, "all", "deltaPhi_muonj1",                          outTreeFile, deltaPhi_muonj1)
systTree.branchTreesSysts(trees, "all", "deltaPhi_muonj2",                          outTreeFile, deltaPhi_muonj2)

#deltaEta#
systTree.branchTreesSysts(trees, "all", "deltaEta_jj",                              outTreeFile, deltaEta_jj)
systTree.branchTreesSysts(trees, "all", "deltaEta_electronmuon",                    outTreeFile, deltaEta_electronmuon)
systTree.branchTreesSysts(trees, "all", "deltaEta_electronj1",                      outTreeFile, deltaEta_electronj1)
systTree.branchTreesSysts(trees, "all", "deltaEta_electronj2",                      outTreeFile, deltaEta_electronj2)
systTree.branchTreesSysts(trees, "all", "deltaEta_muonj1",                          outTreeFile, deltaEta_muonj1)
systTree.branchTreesSysts(trees, "all", "deltaEta_muonj2",                          outTreeFile, deltaEta_muonj2)

#deltaTheta#
systTree.branchTreesSysts(trees, "all", "deltaTheta_jj",                            outTreeFile, deltaTheta_jj)
systTree.branchTreesSysts(trees, "all", "deltaTheta_electronmuon",                  outTreeFile, deltaTheta_electronmuon)
systTree.branchTreesSysts(trees, "all", "deltaTheta_electronj1",                    outTreeFile, deltaTheta_electronj1)
systTree.branchTreesSysts(trees, "all", "deltaTheta_electronj2",                    outTreeFile, deltaTheta_electronj2)
systTree.branchTreesSysts(trees, "all", "deltaTheta_muonj1",                        outTreeFile, deltaTheta_muonj1)
systTree.branchTreesSysts(trees, "all", "deltaTheta_muonj2",                        outTreeFile, deltaTheta_muonj2)

#ptRel#
systTree.branchTreesSysts(trees, "all", "ptRel_jj",                                 outTreeFile, ptRel_jj)
systTree.branchTreesSysts(trees, "all", "ptRel_electronmuon",                       outTreeFile, ptRel_electronmuon)
systTree.branchTreesSysts(trees, "all", "ptRel_electronj1",                         outTreeFile, ptRel_electronj1)
systTree.branchTreesSysts(trees, "all", "ptRel_electronj2",                         outTreeFile, ptRel_electronj2)
systTree.branchTreesSysts(trees, "all", "ptRel_muonj1",                             outTreeFile, ptRel_muonj1)
systTree.branchTreesSysts(trees, "all", "ptRel_muonj2",                             outTreeFile, ptRel_muonj2)

#SFFake
systTree.branchTreesSysts(trees, "all", "event_SFFake_vsjet2",                      outTreeFile, event_SFFake_vsjet2)
systTree.branchTreesSysts(trees, "all", "event_SFFake_vsjet4",                      outTreeFile, event_SFFake_vsjet4)

#other                                                                                    
systTree.branchTreesSysts(trees, "all", "SF_Fake",                                  outTreeFile, SF_Fake)
systTree.branchTreesSysts(trees, "all", "HLT_effLumi",                              outTreeFile, HLT_effLumi)

#zeppenfeld
systTree.branchTreesSysts(trees, "all", "electron_Zeppenfeld",                      outTreeFile, electron_Zeppenfeld)
systTree.branchTreesSysts(trees, "all", "electron_Zeppenfeld_over_deltaEta_jj",     outTreeFile, electron_Zeppenfeld_over_deltaEta_jj)
systTree.branchTreesSysts(trees, "all", "muon_Zeppenfeld",                          outTreeFile, muon_Zeppenfeld)
systTree.branchTreesSysts(trees, "all", "muon_Zeppenfeld_over_deltaEta_jj",         outTreeFile, muon_Zeppenfeld_over_deltaEta_jj)
systTree.branchTreesSysts(trees, "all", "event_Zeppenfeld",                         outTreeFile, event_Zeppenfeld)
systTree.branchTreesSysts(trees, "all", "event_Zeppenfeld_over_deltaEta_jj",        outTreeFile, event_Zeppenfeld_over_deltaEta_jj)
systTree.branchTreesSysts(trees, "all", "event_RT",                                 outTreeFile, event_RT)

#cut variables
systTree.branchTreesSysts(trees, "all", "pass_lepton_selection",                    outTreeFile, pass_lepton_selection)
systTree.branchTreesSysts(trees, "all", "pass_lepton_iso",                          outTreeFile, pass_lepton_iso)
systTree.branchTreesSysts(trees, "all", "pass_lepton_veto",                         outTreeFile, pass_lepton_veto)
systTree.branchTreesSysts(trees, "all", "pass_tau_selection",                       outTreeFile, pass_tau_selection)
systTree.branchTreesSysts(trees, "all", "pass_tau_vsJetWP",                         outTreeFile, pass_tau_vsJetWP)
systTree.branchTreesSysts(trees, "all", "pass_charge_selection",                    outTreeFile, pass_charge_selection)
systTree.branchTreesSysts(trees, "all", "pass_jet_selection",                       outTreeFile, pass_jet_selection)
systTree.branchTreesSysts(trees, "all", "pass_b_veto",                              outTreeFile, pass_b_veto)
systTree.branchTreesSysts(trees, "all", "pass_tau_veto",                              outTreeFile, pass_tau_veto)
systTree.branchTreesSysts(trees, "all", "pass_mjj_cut",                             outTreeFile, pass_mjj_cut)
systTree.branchTreesSysts(trees, "all", "pass_MET_cut",                             outTreeFile, pass_MET_cut)
systTree.branchTreesSysts(trees, "all", "pass_upToBVeto",                           outTreeFile, pass_upToBVeto)
systTree.branchTreesSysts(trees, "all", "pass_everyCut",                            outTreeFile, pass_everyCut)

#print("Is MC: " + str(isMC) + "      option addPDF: " + str(addPDF))
if(isMC and addPDF):
    systTree.branchTreesSysts(trees, "all", "w_PDF", outTreeFile, w_PDF_all)

####################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################
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

#++++++++++++++++++++++++++++++++++
#++   looping over the events    ++
#++++++++++++++++++++++++++++++++++

for i in range(tree.GetEntries()):

    #init all variables to -999
    for j, var in enumerate(var_list):
        if j<len(var_list):
            var_list[j][0] = -999

    #init pass variables to 0
    pass_lepton_selection[0]    = 0
    pass_lepton_iso[0]          = 0
    pass_lepton_veto[0]         = 0
    pass_tau_selection[0]       = 0
    pass_tau_vsJetWP[0]         = 0
    pass_charge_selection[0]    = 0
    pass_jet_selection[0]       = 0
    pass_b_veto[0]              = 0 
    pass_tau_veto[0]            = 0 
    pass_mjj_cut[0]             = 0
    pass_MET_cut[0]             = 0
    pass_upToBVeto[0]           = 0
    pass_everyCut[0]            = 0
    SF_Fake[0]                  = 0      
    w_nominal_all[0]            = 1.
    muon_SFFake_vsjet2[0]       = 1.
    muon_SFFake_vsjet4[0]       = 1.
    electron_SFFake_vsjet2[0]   = 1.
    electron_SFFake_vsjet4[0]   = 1.
    
    #++++++++++++++++++++++++++++++++++
    #++        taking objects        ++
    #++++++++++++++++++++++++++++++++++
    
    if Debug:
        print("\nevent n. " + str(i))
        if i > 1000:
            break
    
    if i%1000 == 0 and not Debug:
        print("Event #", i+1, " out of ", tree.GetEntries())

    event       = Event(tree,i)
    electrons   = Collection(event, "Electron")
    muons       = Collection(event, "Muon")
    jets        = Collection(event, "Jet")
    fatjets     = Collection(event, "FatJet")
    taus        = Collection(event, "Tau")
    HT          = Object(event, "HT")
    PV          = Object(event, "PV")
    HLT         = Object(event, "HLT")
    Flag        = Object(event, 'Flag')
    met         = Object(event, "MET")
    
    njets       = len(jets)
    nJets[0]    = len(jets)
    nBJets[0]   = CountBJets(jets)

    genpart = None
    
    if isMC:
        genpart = Collection(event, "GenPart")
        if not ("WZ" in sample.label or "WWTo2L2Nu_DoubleScattering"):
            LHE = Collection(event, "LHEPart")
        if IsDim8:
            LHEDim8 = Collection(event, "LHEReweightingWeight")

    chain.GetEntry(i)
    #++++++++++++++++++++++++++++++++++
    #++      defining variables      ++
    #++++++++++++++++++++++++++++++++++
    tightele        = None
    tightmu         = None
    tightele_SF     = None
    tightmu_SF      = None
    tightele_SFUp   = None
    tightmu_SFUp    = None
    tightele_SFDown = None
    tightmu_SFDown  = None
    recomet_p4t     = None
    PF_SF           = None
    PF_SFUp         = None
    PF_SFDown       = None
    PU_SF           = None
    PU_SFUp         = None
    PU_SFDown       = None
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
    if 'DataMu' in sample.label:
        dataMu = True
    if 'DataEle' in sample.label:
        dataEle = True

    if not isMC:
        if not Flag.eeBadScFilter:
            continue

    #print "------ ", i
    passMu, passEle, passHT, noTrigger = trig_map(HLT, PV, year, runPeriod)

    EleTrig = False
    MuTrig  = False
    ElMu    = False

    HighestLepPt    = -999.
    LeadLepFamily   = "not selected"

    if 'DataHT' not in sample.label:
        if passEle and not passMu:
            if len(electrons)>0:  
                EleTrig=True
                LeadLepFamily="electrons"
                HighestLepPt=copy.deepcopy(electrons[0].pt)
                #print("HighestLepPt:", HighestLepPt)
            else:
                continue
        elif passMu and not passEle:
            if len(muons)>0:
                MuTrig=True
                LeadLepFamily="muons"
                HighestLepPt=copy.deepcopy(muons[0].pt)
            else:
                continue
        elif passMu and passEle:
            ElMu=True
    else:
        if passHT:
            ElMu=True
        else:
            continue

    if ElMu:
        for mu in muons:
            if abs(mu.pt)>HighestLepPt:
                HighestLepPt    = copy.deepcopy(mu.pt)
                EleTrig         = False
                MuTrig          = True
                break
        for ele in electrons:
            if abs(ele.pt)>HighestLepPt:
                HighestLepPt    = copy.deepcopy(ele.pt)
                EleTrig         = True
                MuTrig          = False
                break

    leptons = None

    vTrigEle, vTrigMu, vTrigHT = trig_finder(HLT, sample.year, sample.label)
    #print(EleTrig, ' ', MuTrig, ' ') 
    if EleTrig==True:
        if isMC:
            HLT_effLumi[0] = lumiFinder("Ele", vTrigEle)
    elif MuTrig==True:
        if isMC:
            HLT_effLumi[0] = lumiFinder("Mu", vTrigMu)
    elif not (MuTrig or EleTrig):
        continue
    if EleTrig and dataMu:
        continue
    if MuTrig and dataEle:
        continue

    #now you have:
    #MuTrig   == True if the highest pT lepton which fired the trigger is a muon
    #EleTrige == True if the highest pT lepton which fired the trigger is an electron

    MET_pt[0]   = met.pt  
    MET_phi[0]  = met.phi

    indexGoodEle, indexGoodMu, electron_TightRegion[0], muon_TightRegion[0], youOkay = diet_SelectLepton(electrons, muons, EleTrig, MuTrig)
    #print(indexGoodEle, ' ',indexGoodMu,' ', youOkay) 
    tightele = electrons[indexGoodEle]
    tightmu  = muons[indexGoodMu]
     
    if not youOkay: continue
    #print('Tight electron index is: ', indexGoodEle)
    #print('Tight muon index is:     ', indexGoodMu,  '  pT is: ', tightmu.pt)


    if electron_TightRegion[0]==1:          electron_LnTRegion[0] = 0
    elif electron_TightRegion[0]==0:        electron_LnTRegion[0] = 1
    else:                                   electron_LnTRegion[0] = -999

    if muon_TightRegion[0]==1:              muon_LnTRegion[0] = 0
    elif muon_TightRegion[0]==0:            muon_LnTRegion[0] = 1
    else:                                   muon_LnTRegion[0] = -999

    if (muon_LnTRegion[0] >= 0 or muon_LnTRegion[0] >= 0) and (electron_LnTRegion[0] >= 0 or electron_TightRegion[0] >= 0):
        pass_lepton_selection[0] = 1
    else:
        pass_lepton_selection[0] = 0
    
    if DietLepVeto(tightele, tightmu, muons, electrons):
        pass_lepton_veto[0] = 1
    else:
        pass_lepton_veto[0] = 0

    electron_pt[0]              =   tightele.pt
    electron_eta[0]             =   tightele.eta
    electron_phi[0]             =   tightele.phi
    electron_mass[0]            =   tightele.mass
    electron_pdgid[0]           =   tightele.pdgId
    electron_pfRelIso04[0]      =   tightele.jetRelIso
    electron_SFFake_vsjet2[0]   =   SFFakeRatio_ele_calc(electron_pt[0], electron_eta[0], 'vsjet2')
    electron_SFFake_vsjet4[0]   =   SFFakeRatio_ele_calc(electron_pt[0], electron_eta[0], 'vsjet4')

    muon_pt[0]                  =   tightmu.pt
    muon_eta[0]                 =   tightmu.eta
    muon_phi[0]                 =   tightmu.phi
    muon_mass[0]                =   tightmu.mass
    muon_pdgid[0]               =   tightmu.pdgId
    muon_pfRelIso04[0]          =   tightmu.jetRelIso
    muon_SFFake_vsjet2[0]       =   SFFakeRatio_mu_calc(muon_pt[0], muon_eta[0], 'vsjet2')
    muon_SFFake_vsjet4[0]       =   SFFakeRatio_mu_calc(muon_pt[0], muon_eta[0], 'vsjet4')

    if isMC:
        electron_isPrompt[0]    =   tightele.genPartFlav
        muon_isPrompt[0]        =   tightmu.genPartFlav

    mT_electron_MET[0]          =   mTlepMet(met, tightele.p4())
    mT_muon_MET[0]              =   mTlepMet(met, tightmu.p4())
    mT_electronmuon_MET[0]      =   mTlepMet(met, tightele.p4() + tightmu.p4())
    m_1T[0]                     =   M1T(tightele, tightmu, met, 1.)
    m_o1[0]                     =   Mo1(tightele, tightmu, met, 1.)

    if electron_LnTRegion[0] == 1 or muon_LnTRegion[0] == 1:
        event_SFFake_vsjet2[0]  =   electron_SFFake_vsjet2[0]*muon_SFFake_vsjet2[0]
        event_SFFake_vsjet4[0]  =   electron_SFFake_vsjet4[0]*muon_SFFake_vsjet4[0]
    elif electron_LnTRegion[0] == 0 and muon_LnTRegion[0] == 0:
        event_SFFake_vsjet2[0]  =   0
        event_SFFake_vsjet4[0]  =   0
    
    if isMC and event_SFFake_vsjet2[0] > 0 or event_SFFake_vsjet2[0] > 0:
        if abs(electron_isPrompt[0]) == 1 or abs(muon_isPrompt[0]) == 1:
            event_SFFake_vsjet4[0] = -1*event_SFFake_vsjet4[0]
            event_SFFake_vsjet2[0] = -1*event_SFFake_vsjet2[0]
        else:
            event_SFFake_vsjet4[0] = 0
            event_SFFake_vsjet2[0] = 0

    if tightele.charge == tightmu.charge:
        pass_charge_selection[0] = 1

    uOkay, jet1, jet2 = diet_SelectJet(list(jets), tightele, tightmu)

    if uOkay == False: continue

    tightele_p4 = ROOT.TLorentzVector()
    

    pass_jet_selection[0]       =   1

    leadjet_pt[0]               =   jet1.pt
    leadjet_eta[0]              =   jet1.eta
    leadjet_phi[0]              =   jet1.phi
    leadjet_mass[0]             =   jet1.mass
    leadjet_DeepFlv_b[0]        =   jet1.btagDeepFlavB
    leadjet_DeepCSVv2_b[0]      =   jet1.btagDeepB
    leadjet_CSVv2_b[0]          =   jet1.btagCSVV2
    subleadjet_pt[0]            =   jet2.pt
    subleadjet_eta[0]           =   jet2.eta
    subleadjet_phi[0]           =   jet2.phi
    subleadjet_mass[0]          =   jet2.mass
    subleadjet_DeepFlv_b[0]     =   jet2.btagDeepFlavB
    subleadjet_DeepCSVv2_b[0]   =   jet2.btagDeepB
    subleadjet_CSVv2_b[0]       =   jet2.btagCSVV2

    #calculating deltaPhi                                                                                                      
    deltaPhi_jj[0]              =   deltaPhi(jet1, jet2)
    deltaPhi_electronmuon[0]    =   deltaPhi(tightele, tightmu)
    deltaPhi_electronj1[0]      =   deltaPhi(tightele, jet1)
    deltaPhi_electronj2[0]      =   deltaPhi(tightele, jet2)
    deltaPhi_muonj1[0]          =   deltaPhi(tightmu, jet1)
    deltaPhi_muonj2[0]          =   deltaPhi(tightmu, jet2)

    #calculating deltaEta                                                                                                      
    deltaEta_jj[0]              =   jet1.eta        - jet2.eta
    deltaEta_electronmuon[0]    =   tightele.eta    - tightmu.eta
    deltaEta_electronj1[0]      =   tightele.eta    - jet1.eta
    deltaEta_electronj2[0]      =   tightele.eta    - jet2.eta
    deltaEta_muonj1[0]          =   tightmu.eta     - jet1.eta
    deltaEta_muonj2[0]          =   tightmu.eta     - jet2.eta

    #calculating deltaTheta                                                                                                      
    deltaTheta_jj[0]            =   (jet1.p4()      - jet2.p4()).CosTheta()
    deltaTheta_electronmuon[0]  =   (tightele.p4()  - tightmu.p4()).CosTheta()
    deltaTheta_electronj1[0]    =   (tightele.p4()  - jet1.p4()).CosTheta()
    deltaTheta_electronj2[0]    =   (tightele.p4()  - jet2.p4()).CosTheta()
    deltaTheta_muonj1[0]        =   (tightmu.p4()   - jet1.p4()).CosTheta()
    deltaTheta_muonj2[0]        =   (tightmu.p4()   - jet2.p4()).CosTheta()

    #calculating ptRel                                                                                                      
    ptRel_jj[0]      =   get_ptrel(jet1, jet2, 1.)

    ptRel_electronmuon[0]       =   get_ptrel(tightele, tightmu, 1.)
    ptRel_electronj1[0]         =   get_ptrel(tightele, jet1, 1.)
    ptRel_electronj2[0]         =   get_ptrel(tightele, jet2, 1.)
    ptRel_muonj1[0]             =   get_ptrel(tightmu,  jet1, 1.)
    ptRel_muonj2[0]             =   get_ptrel(tightmu,  jet2, 1.)

    electron_Zeppenfeld[0], muon_Zeppenfeld[0], event_Zeppenfeld[0] = Zeppenfeld(electron_eta[0], muon_eta[0], leadjet_eta[0], subleadjet_eta[0])

    AK8jet1, dR_jet1AK48 = closest(jet1, fatjets)
    AK8jet2, dR_jet2AK48 = closest(jet1, fatjets)


    if dR_jet1AK48 < 0.8:
        AK8leadjet_pt[0]                    =   AK8jet1.pt
        AK8leadjet_eta[0]                   =   AK8jet1.eta
        AK8leadjet_phi[0]                   =   AK8jet1.phi
        AK8leadjet_mass[0]                  =   AK8jet1.msoftdrop
    
        AK8leadjet_tau21[0]                 =   AK8jet1.tau2/((AK8jet1.tau1==0.)*1 + (AK8jet1.tau1!=0.)*AK8jet1.tau1)
        AK8leadjet_tau32[0]                 =   AK8jet1.tau3/((AK8jet1.tau2==0.)*1 + (AK8jet1.tau2!=0.)*AK8jet1.tau2)
        AK8leadjet_tau43[0]                 =   AK8jet1.tau4/((AK8jet1.tau3==0.)*1 + (AK8jet1.tau3!=0.)*AK8jet1.tau3)
        leadjet_dRAK48[0] = copy.deepcopy(dR_jet1AK48)

    if dR_jet2AK48 < 0.8:
        AK8subleadjet_pt[0]                 =   AK8jet2.pt
        AK8subleadjet_eta[0]                =   AK8jet2.eta
        AK8subleadjet_phi[0]                =   AK8jet2.phi
        AK8subleadjet_mass[0]               =   AK8jet2.msoftdrop
        
        AK8subleadjet_tau21[0]             =   AK8jet2.tau2/((AK8jet2.tau1==0.)*1 + (AK8jet2.tau1!=0.)*AK8jet2.tau1)
        AK8subleadjet_tau32[0]             =   AK8jet2.tau3/((AK8jet2.tau2==0.)*1 + (AK8jet2.tau2!=0.)*AK8jet2.tau2)
        AK8subleadjet_tau43[0]             =   AK8jet2.tau4/((AK8jet2.tau3==0.)*1 + (AK8jet2.tau3!=0.)*AK8jet2.tau3)
        subleadjet_dRAK48[0] = copy.deepcopy(dR_jet2AK48)

    if not(diet_AreThereAdditionalLooseTaus(taus, tightele, tightmu)):
        pass_tau_veto[0] = 1

    if not BVeto(jets):
        pass_b_veto[0] = 1

    if (EleTrig or MuTrig) and pass_lepton_selection[0]==1 and pass_lepton_veto[0]==1 and pass_charge_selection[0]==1 and pass_jet_selection[0]==1 and pass_b_veto[0]==1 and pass_tau_veto[0] == 1: pass_upToBVeto[0]=1#


    leadJet         =   ROOT.TLorentzVector()
    subleadJet      =   ROOT.TLorentzVector()
    leadJet.SetPtEtaPhiM(jet1.pt, jet1.eta, jet1.phi, jet1.mass)
    subleadJet.SetPtEtaPhiM(jet2.pt, jet2.eta, jet2.phi, jet2.mass) 
    
    if not JetCut(leadJet, subleadJet):
        pass_mjj_cut[0]=1

    m_jj[0]         =   (leadJet + subleadJet).M()
    m_jjelectron[0] =   (leadJet + subleadJet + tightele.p4()).M()
    m_jjmuon[0]     =   (leadJet + subleadJet + tightmu.p4()).M()
    m_jjleps[0]     =   (leadJet + subleadJet + tightele.p4() + tightmu.p4()).M()


    electron_Zeppenfeld_over_deltaEta_jj[0]     = electron_Zeppenfeld[0]/deltaEta_jj[0]
    muon_Zeppenfeld_over_deltaEta_jj[0]         = muon_Zeppenfeld[0]/deltaEta_jj[0]
    event_Zeppenfeld_over_deltaEta_jj[0]        = event_Zeppenfeld[0]/deltaEta_jj[0]

    event_RT[0] = (tightele.pt * tightmu.pt) / (jet1.pt * jet2.pt)

    if not metCut(met):
        pass_MET_cut[0]=1

    if (EleTrig or MuTrig) and pass_lepton_selection[0]==1 and pass_lepton_veto[0]==1 and pass_charge_selection[0]==1 and pass_jet_selection[0]==1 and pass_b_veto[0]==1 and pass_mjj_cut[0]==1 and pass_MET_cut[0]==1 and pass_tau_veto[0] == 1:
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

    #######################################
    #########    Setting weights    #######
    #######################################

    systTree.setWeightName("w_nominal",copy.deepcopy(w_nominal_all[0]))
    if IsDim8:
        opname = ""
        opmag = 0
        for opi, opn in enumerate(EFT_operator_names):
            if ("_" + opn + "_") in sample.label:
                opmax = EFT_operator[opn]["max"]
                step = opmax/5.

                for eidx in range(11):
                    epoint = opmax - step * eidx
                    IsZero = (epoint == 0.)
                    str_epoint = "_" + str(epoint).replace(".0", "").replace(".", "p") + "_"

                    if str_epoint in sample.label:
                        idxpos = int((EFT_operator[opn]["idx"])*11 - (eidx + 1))
                        idxneg = int((EFT_operator[opn]["idx"] - 1)*11 + eidx)
                        if IsZero and idxneg != idxpos:
                            print("Something went wrong with dim8 weights assignment")
                            #break
                        wpos = LHEitem(LHEDim8[idxpos])
                        wneg = LHEitem(LHEDim8[idxneg])

                        w_pos[0] = copy.deepcopy(wpos)
                        w_neg[0] = copy.deepcopy(wneg)

                        wsign = 0
                        kpow = 0

                        if "_BSM_" in sample.label:#
                            print("BSM")
                            wsign = +1.
                            kpow = 2.*(epoint**2.)
                        elif "_0_" in sample.label:
                            print("0")
                            wsign = +1.
                            kpow = +2.
                        elif "_INT_" in sample.label:
                            print("INT")
                            wsign = -1.
                            kpow = 2.*epoint
            
                        w_coeff = (wpos + wsign * wneg) / kpow
                        w_dim8[0] = copy.deepcopy(w_coeff)
                        break
                break

    #print('saviiing') 
    systTree.fillTreesSysts(trees, "all")

outTreeFile.cd()
if(isMC):
    h_genweight.Write()
    if isthere_pdf:
        h_PDFweight.Write()

systTree.writeTreesSysts(trees, outTreeFile)
print("Number of events in output tree " + str(trees[0].GetEntries()))

endTime = datetime.datetime.now()
print("Ending running at " + str(endTime) + "\n So long, and thanks for all the fish")
