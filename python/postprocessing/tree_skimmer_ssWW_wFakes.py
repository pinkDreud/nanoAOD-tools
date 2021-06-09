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
from skimtree_utils_ssWW_wFakes import *
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

usage = "python tree_skimmer_ssWW_wFakes.py [nome_del_sample_in_samples.py] 0 [file_in_input] local wpvsjet wpvsele wpvsmu"

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
if sys.argv[5] == 'prompt':
    fakewithprompt = True
elif sys.argv[5] == 'noprompt':
    fakewithprompt = False

print(fakewithprompt)
'''

vsjetWP = vsJet[sys.argv[5]]
vseleWP = vsEle[sys.argv[6]]
vsmuWP = vsMu[sys.argv[7]]

act_camp = ''
for cam in campaigns:
    if str(sample.year) in cam:
        act_camp = copy.deepcopy(cam)
        break

#print(cam, vsjetWP, vseleWP, vsmuWP)
tauSFTool_vsjet = TauIDSFTool(act_camp, 'DeepTau2017v2p1VSjet', vsjetWP)
tauSFTool_vsele = TauIDSFTool(act_camp, 'DeepTau2017v2p1VSe', vseleWP)
tauSFTool_vsmu = TauIDSFTool(act_camp, 'DeepTau2017v2p1VSmu', vsmuWP)
tesTool = TauESTool(act_camp, 'DeepTau2017v2p1VSjet')
fesTool = TauFESTool(act_camp, 'DeepTau2017v2p1VSe')

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

#Cut_dict = {}

#if Debug:
#Cut_dict = {1: ['Trigger             ', 0, 0.0, 0.0, 0.0, 0.0],
#2: ['Lepton selection    ', 0, 0.0, 0.0, 0.0, 0.0],
#            3: ['Lepton Veto         ', 0, 0.0, 0.0, 0.0, 0.0],
#            4: ['Tau selection       ', 0, 0.0, 0.0, 0.0, 0.0],
#            5: ['Same charge tau lep ', 0, 0.0, 0.0, 0.0, 0.0],
#            6: ['Jet Selection       ', 0, 0.0, 0.0, 0.0, 0.0],
#            7: ['BVeto               ', 0, 0.0, 0.0, 0.0, 0.0],
#            8: ['M_jj>500 GeV        ', 0, 0.0, 0.0, 0.0, 0.0],
#            9: ['MET>40 GeV          ', 0, 0.0, 0.0, 0.0, 0.0],
#}

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
    w_dim8             =   array.array('f', [-999.])
    w_neg              =   array.array('f', [-999.])
    w_pos              =   array.array('f', [-999.])
    var_list.append(w_dim8)
    var_list.append(w_neg)
    var_list.append(w_pos)
    
#++++++++++++++++++++++++++++++++++
#++         All category         ++
#++++++++++++++++++++++++++++++++++

#ssWW variables

#lepton#
lepton_pt               =   array.array('f', [-999.])
lepton_eta              =   array.array('f', [-999.])
lepton_phi              =   array.array('f', [-999.])
lepton_mass             =   array.array('f', [-999.])
lepton_pdgid            =   array.array('i', [-999])
lepton_pfRelIso04       =   array.array('f', [-999.])
lepton_TightRegion      =   array.array('i', [-999])
lepton_LnTRegion        =   array.array('i', [-999])
lepton_SFFake_vsjet2           =   array.array('f', [-999.])
lepton_SFFake_vsjet4           =   array.array('f', [-999.])
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
var_list.append(lepton_SFFake_vsjet2)
var_list.append(lepton_SFFake_vsjet4)
var_list.append(lepton_isPrompt)
var_list.append(lepton_Zeppenfeld)
var_list.append(lepton_Zeppenfeld_over_deltaEta_jj)
#tau#
tau_pt                  =   array.array('f', [-999.])
tau_relleadtkpt         =   array.array('f', [-999.])
tau_eta                 =   array.array('f', [-999.])
tau_phi                 =   array.array('f', [-999.])
tau_charge              =   array.array('i', [-999])
tau_mass                =   array.array('f', [-999.])
tau_GenMatch            =   array.array('f', [-999.])
tau_DecayMode           =   array.array('f', [-999.])
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
tau_SFFake_vsjet2              =   array.array('f', [-999.])
tau_SFFake_vsjet4              =   array.array('f', [-999.])
tau_isPrompt           =   array.array('i', [-999])
tau_Zeppenfeld           =   array.array('f', [-999])
tau_Zeppenfeld_over_deltaEta_jj           =   array.array('f', [-999])
var_list.append(tau_isolation)
var_list.append(tau_pt)
var_list.append(tau_relleadtkpt)
var_list.append(tau_eta)
var_list.append(tau_phi)
var_list.append(tau_charge)
var_list.append(tau_mass)
var_list.append(tau_GenMatch)
var_list.append(tau_DecayMode)
var_list.append(tau_DeepTau_WP)
var_list.append(tau_DeepTauVsEle_raw)#
var_list.append(tau_DeepTauVsMu_WP)#
var_list.append(tau_DeepTauVsMu_raw)#
var_list.append(tau_DeepTauVsJet_WP)#
var_list.append(tau_DeepTauVsJet_raw)#
var_list.append(tau_TightRegion)#
var_list.append(tau_LnTRegion)#
var_list.append(tau_SFFake_vsjet2)#
var_list.append(tau_SFFake_vsjet4)#
var_list.append(tau_isPrompt)#
var_list.append(tau_Zeppenfeld)
var_list.append(tau_Zeppenfeld_over_deltaEta_jj)

event_Zeppenfeld           =   array.array('f', [-999])
event_Zeppenfeld_over_deltaEta_jj           =   array.array('f', [-999])
var_list.append(event_Zeppenfeld)
var_list.append(event_Zeppenfeld_over_deltaEta_jj)

event_RT = array.array('f', [-999])
var_list.append(event_RT)

#tau leadTk                        #
tauleadTk_ptOverTau     =   array.array('f', [-999.])#
tauleadTk_deltaPhi      =   array.array('f', [-999.])#
tauleadTk_deltaEta      =   array.array('f', [-999.])#
tauleadTk_Gamma      =   array.array('f', [-999.])#
var_list.append(tauleadTk_ptOverTau)#
var_list.append(tauleadTk_deltaPhi)#
var_list.append(tauleadTk_deltaEta)#
var_list.append(tauleadTk_Gamma)#

#taujet
taujet_RelPt       = array.array('f', [-999.])#
taujet_deltaPhi    = array.array('f', [-999.])#
taujet_deltaEta    = array.array('f', [-999.])#
taujet_HadGamma    = array.array('f', [-999.])#
taujet_EmGamma     = array.array('f', [-999.])#
taujet_HEGamma      = array.array('f', [-999.])#
var_list.append(taujet_RelPt)
var_list.append(taujet_deltaPhi)
var_list.append(taujet_deltaEta)
var_list.append(taujet_HadGamma)
var_list.append(taujet_HEGamma)

#event SFFake
event_SFFake_vsjet2              =   array.array('f', [-999.])
event_SFFake_vsjet4              =   array.array('f', [-999.])
var_list.append(event_SFFake_vsjet2)
var_list.append(event_SFFake_vsjet4)

#jet#
leadjet_pt                  =   array.array('f', [-999.])
leadjet_eta                 =   array.array('f', [-999.])
leadjet_phi                 =   array.array('f', [-999.])
leadjet_mass                =   array.array('f', [-999.])
leadjet_CSVv2_b             =   array.array('f', [-999.])
leadjet_DeepFlv_b           =   array.array('f', [-999.])
leadjet_DeepCSVv2_b         =   array.array('f', [-999.])
nJets                       =   array.array('f', [-999.])#
nBJets                      =   array.array('f', [-999.])#
AK8leadjet_pt                  =   array.array('f', [-999.])
AK8leadjet_eta                 =   array.array('f', [-999.])
AK8leadjet_phi                 =   array.array('f', [-999.])
AK8leadjet_mass                =   array.array('f', [-999.])
AK8leadjet_tau21               =   array.array('f', [-999.])
AK8leadjet_tau32               =   array.array('f', [-999.])
AK8leadjet_tau43               =   array.array('f', [-999.])
leadjet_dRAK48               =   array.array('f', [-999.])

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

subleadjet_pt               =   array.array('f', [-999.])
subleadjet_eta              =   array.array('f', [-999.])
subleadjet_phi              =   array.array('f', [-999.])
subleadjet_mass             =   array.array('f', [-999.])
subleadjet_CSVv2_b          =   array.array('f', [-999.])
subleadjet_DeepFlv_b        =   array.array('f', [-999.])
subleadjet_DeepCSVv2_b      =   array.array('f', [-999.])
AK8subleadjet_pt                  =   array.array('f', [-999.])
AK8subleadjet_eta                 =   array.array('f', [-999.])
AK8subleadjet_phi                 =   array.array('f', [-999.])
AK8subleadjet_mass                =   array.array('f', [-999.])
AK8subleadjet_tau21               =   array.array('f', [-999.])
AK8subleadjet_tau32               =   array.array('f', [-999.])
AK8subleadjet_tau43               =   array.array('f', [-999.])
subleadjet_dRAK48               =   array.array('f', [-999.])

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
MET_pt                      =   array.array('f', [-999.])
MET_phi                     =   array.array('f', [-999.])
var_list.append(MET_pt)
var_list.append(MET_phi)


#inv and transv masses
m_jjtau = array.array('f', [-999.])#
m_jjtaulep = array.array('f', [-999.])#
m_jj                        =   array.array('f', [-999.])
m_1T                        =   array.array('f', [-999.])
m_o1                        =   array.array('f', [-999.])
m_taulep                    =   array.array('f', [-999.])
mT_lep_MET                  =   array.array('f', [-999.])
mT_tau_MET                  =   array.array('f', [-999.])
mT_leptau_MET               =   array.array('f', [-999.])
var_list.append(m_jjtau)
var_list.append(m_jjtaulep)
var_list.append(m_jj)
var_list.append(m_1T)
var_list.append(m_o1)
var_list.append(m_taulep)
var_list.append(mT_lep_MET)
var_list.append(mT_tau_MET)
var_list.append(mT_leptau_MET)

#deltaPhi#                                                                      
deltaPhi_jj                 =   array.array('f', [-999.])#
deltaPhi_taulep             =   array.array('f', [-999.])#
deltaPhi_tauj1              =   array.array('f', [-999.])#
deltaPhi_tauj2              =   array.array('f', [-999.])#
deltaPhi_lepj1              =   array.array('f', [-999.])#
deltaPhi_lepj2              =   array.array('f', [-999.])#
var_list.append(deltaPhi_jj)#
var_list.append(deltaPhi_taulep)#
var_list.append(deltaPhi_tauj1)#
var_list.append(deltaPhi_tauj2)#
var_list.append(deltaPhi_lepj1)#
var_list.append(deltaPhi_lepj2)#

#deltaTheta
deltaTheta_jj                 =   array.array('f', [-999.])#
deltaTheta_taulep             =   array.array('f', [-999.])#
deltaTheta_tauj1              =   array.array('f', [-999.])#
deltaTheta_tauj2              =   array.array('f', [-999.])#
deltaTheta_lepj1              =   array.array('f', [-999.])#
deltaTheta_lepj2              =   array.array('f', [-999.])#
var_list.append(deltaTheta_jj)#
var_list.append(deltaTheta_taulep)#
var_list.append(deltaTheta_tauj1)#
var_list.append(deltaTheta_tauj2)#
var_list.append(deltaTheta_lepj1)#
var_list.append(deltaTheta_lepj2)#

#ptRel
ptRel_jj                 =   array.array('f', [-999.])#
ptRel_taulep             =   array.array('f', [-999.])#
ptRel_tauj1              =   array.array('f', [-999.])#
ptRel_tauj2              =   array.array('f', [-999.])#
ptRel_lepj1              =   array.array('f', [-999.])#
ptRel_lepj2              =   array.array('f', [-999.])#
var_list.append(ptRel_jj)#
var_list.append(ptRel_taulep)#
var_list.append(ptRel_tauj1)#
var_list.append(ptRel_tauj2)#
var_list.append(ptRel_lepj1)#
var_list.append(ptRel_lepj2)#

#other#
SF_Fake                     =   array.array('f', [1.])
var_list.append(SF_Fake)
HLT_effLumi                 =   array.array('f', [-999.])
var_list.append(HLT_effLumi)

#deltaEta#                                                                      
deltaEta_jj                 =   array.array('f', [-999.])#
deltaEta_taulep             =   array.array('f', [-999.])#
deltaEta_tauj1              =   array.array('f', [-999.])#
deltaEta_tauj2              =   array.array('f', [-999.])#
deltaEta_lepj1              =   array.array('f', [-999.])#
deltaEta_lepj2              =   array.array('f', [-999.])#
var_list.append(deltaEta_jj)#
var_list.append(deltaEta_taulep)#
var_list.append(deltaEta_tauj1)#
var_list.append(deltaEta_tauj2)#
var_list.append(deltaEta_lepj1)#
var_list.append(deltaEta_lepj2)#

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

#weights#
w_PDF_all = array.array('f', [0.]*110)#
w_nominal_all = array.array('f', [0.])

#w_dim8
if IsDim8:
    systTree.branchTreesSysts(trees, "all", "w_dim8",            outTreeFile, w_dim8)
    systTree.branchTreesSysts(trees, "all", "w_pos",            outTreeFile, w_pos)
    systTree.branchTreesSysts(trees, "all", "w_neg",            outTreeFile, w_neg)

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
systTree.branchTreesSysts(trees, "all", "lepton_SFFake_vsjet2",        outTreeFile, lepton_SFFake_vsjet2)
systTree.branchTreesSysts(trees, "all", "lepton_SFFake_vsjet4",        outTreeFile, lepton_SFFake_vsjet4)
systTree.branchTreesSysts(trees, "all", "lepton_isPrompt",        outTreeFile, lepton_isPrompt)

#tau variables
systTree.branchTreesSysts(trees, "all", "tau_pt",               outTreeFile, tau_pt)
systTree.branchTreesSysts(trees, "all", "tau_eta",              outTreeFile, tau_eta)
systTree.branchTreesSysts(trees, "all", "tau_phi",              outTreeFile, tau_phi)
systTree.branchTreesSysts(trees, "all", "tau_mass",             outTreeFile, tau_mass)
systTree.branchTreesSysts(trees, "all", "tau_GenMatch",             outTreeFile, tau_GenMatch)
systTree.branchTreesSysts(trees, "all", "tau_DecayMode",             outTreeFile, tau_DecayMode)
systTree.branchTreesSysts(trees, "all", "tau_DeepTau_WP",             outTreeFile, tau_DeepTau_WP)
systTree.branchTreesSysts(trees, "all", "tau_isolation",             outTreeFile, tau_isolation)
systTree.branchTreesSysts(trees, "all", "tau_DeepTauVsEle_WP",      outTreeFile, tau_DeepTauVsEle_WP)#
systTree.branchTreesSysts(trees, "all", "tau_DeepTauVsEle_raw",     outTreeFile, tau_DeepTauVsEle_raw)#
systTree.branchTreesSysts(trees, "all", "tau_DeepTauVsMu_WP",       outTreeFile, tau_DeepTauVsMu_WP)#
systTree.branchTreesSysts(trees, "all", "tau_DeepTauVsMu_raw",      outTreeFile, tau_DeepTauVsMu_raw)#
systTree.branchTreesSysts(trees, "all", "tau_DeepTauVsJet_WP",      outTreeFile, tau_DeepTauVsJet_WP)#
systTree.branchTreesSysts(trees, "all", "tau_TightRegion",          outTreeFile, tau_TightRegion)#
systTree.branchTreesSysts(trees, "all", "tau_LnTRegion",            outTreeFile, tau_LnTRegion)#
systTree.branchTreesSysts(trees, "all", "tau_SFFake_vsjet2",               outTreeFile, tau_SFFake_vsjet2)#
systTree.branchTreesSysts(trees, "all", "tau_SFFake_vsjet4",               outTreeFile, tau_SFFake_vsjet4)#
systTree.branchTreesSysts(trees, "all", "tau_isPrompt",               outTreeFile, tau_isPrompt)#
systTree.branchTreesSysts(trees, "all", "event_SFFake_vsjet2",               outTreeFile, event_SFFake_vsjet2)#
systTree.branchTreesSysts(trees, "all", "event_SFFake_vsjet4",               outTreeFile, event_SFFake_vsjet4)#
systTree.branchTreesSysts(trees, "all", "tauleadTk_ptOverTau",      outTreeFile, tauleadTk_ptOverTau)
systTree.branchTreesSysts(trees, "all", "tauleadTk_deltaPhi",      outTreeFile, tauleadTk_deltaPhi)
systTree.branchTreesSysts(trees, "all", "tauleadTk_deltaEta",      outTreeFile, tauleadTk_deltaEta)
systTree.branchTreesSysts(trees, "all", "tauleadTk_Gamma",      outTreeFile, tauleadTk_Gamma)
systTree.branchTreesSysts(trees, "all", "taujet_relpt",               outTreeFile, taujet_RelPt)
systTree.branchTreesSysts(trees, "all", "taujet_deltaPhi",               outTreeFile, taujet_deltaPhi)
systTree.branchTreesSysts(trees, "all", "taujet_deltaEta",               outTreeFile, taujet_deltaEta)
systTree.branchTreesSysts(trees, "all", "taujet_HadGamma",               outTreeFile, taujet_HadGamma)
systTree.branchTreesSysts(trees, "all", "taujet_EmGamma",               outTreeFile, taujet_EmGamma)
systTree.branchTreesSysts(trees, "all", "taujet_HEGamma",               outTreeFile, taujet_HEGamma)
#jet variables
systTree.branchTreesSysts(trees, "all", "leadjet_pt",           outTreeFile, leadjet_pt)
systTree.branchTreesSysts(trees, "all", "leadjet_eta",          outTreeFile, leadjet_eta)
systTree.branchTreesSysts(trees, "all", "leadjet_phi",          outTreeFile, leadjet_phi)
systTree.branchTreesSysts(trees, "all", "leadjet_mass",         outTreeFile, leadjet_mass)
systTree.branchTreesSysts(trees, "all", "leadjet_CSVv2_b",      outTreeFile, leadjet_CSVv2_b)
systTree.branchTreesSysts(trees, "all", "leadjet_DeepFlv_b",    outTreeFile, leadjet_DeepFlv_b)
systTree.branchTreesSysts(trees, "all", "leadjet_DeepCSVv2_b",  outTreeFile, leadjet_DeepCSVv2_b)
systTree.branchTreesSysts(trees, "all", "AK8leadjet_pt",           outTreeFile, AK8leadjet_pt)
systTree.branchTreesSysts(trees, "all", "AK8leadjet_eta",          outTreeFile, AK8leadjet_eta)
systTree.branchTreesSysts(trees, "all", "AK8leadjet_phi",          outTreeFile, AK8leadjet_phi)
systTree.branchTreesSysts(trees, "all", "AK8leadjet_mass",         outTreeFile, AK8leadjet_mass)
systTree.branchTreesSysts(trees, "all", "AK8leadjet_tau21",         outTreeFile, AK8leadjet_tau21)
systTree.branchTreesSysts(trees, "all", "AK8leadjet_tau32",         outTreeFile, AK8leadjet_tau32)
systTree.branchTreesSysts(trees, "all", "AK8leadjet_tau43",         outTreeFile, AK8leadjet_tau43)
systTree.branchTreesSysts(trees, "all", "leadjet_dRAK48",         outTreeFile, leadjet_dRAK48)
systTree.branchTreesSysts(trees, "all", "subleadjet_pt",           outTreeFile, subleadjet_pt)
systTree.branchTreesSysts(trees, "all", "subleadjet_eta",          outTreeFile, subleadjet_eta)
systTree.branchTreesSysts(trees, "all", "subleadjet_phi",          outTreeFile, subleadjet_phi)
systTree.branchTreesSysts(trees, "all", "subleadjet_mass",         outTreeFile, subleadjet_mass)
systTree.branchTreesSysts(trees, "all", "subleadjet_CSVv2_b",      outTreeFile, subleadjet_CSVv2_b)
systTree.branchTreesSysts(trees, "all", "subleadjet_DeepFlv_b",    outTreeFile, subleadjet_DeepFlv_b)
systTree.branchTreesSysts(trees, "all", "subleadjet_DeepCSVv2_b",  outTreeFile, subleadjet_DeepCSVv2_b)
systTree.branchTreesSysts(trees, "all", "AK8subleadjet_pt",           outTreeFile, AK8subleadjet_pt)
systTree.branchTreesSysts(trees, "all", "AK8subleadjet_eta",          outTreeFile, AK8subleadjet_eta)
systTree.branchTreesSysts(trees, "all", "AK8subleadjet_phi",          outTreeFile, AK8subleadjet_phi)
systTree.branchTreesSysts(trees, "all", "AK8subleadjet_mass",         outTreeFile, AK8subleadjet_mass)
systTree.branchTreesSysts(trees, "all", "AK8subleadjet_tau21",         outTreeFile, AK8subleadjet_tau21)
systTree.branchTreesSysts(trees, "all", "AK8subleadjet_tau32",         outTreeFile, AK8subleadjet_tau32)
systTree.branchTreesSysts(trees, "all", "AK8subleadjet_tau43",         outTreeFile, AK8subleadjet_tau43)
systTree.branchTreesSysts(trees, "all", "subleadjet_dRAK48",         outTreeFile, subleadjet_dRAK48)

systTree.branchTreesSysts(trees, "all", "nJets",  outTreeFile, nJets)
systTree.branchTreesSysts(trees, "all", "nBJets", outTreeFile, nBJets)#
#MET
systTree.branchTreesSysts(trees, "all", "MET_pt",               outTreeFile, MET_pt)
systTree.branchTreesSysts(trees, "all", "MET_phi",              outTreeFile, MET_phi)
#masses#
systTree.branchTreesSysts(trees, "all", "m_jj",                  outTreeFile, m_jj)
systTree.branchTreesSysts(trees, "all", "m_1T",                  outTreeFile, m_1T)
systTree.branchTreesSysts(trees, "all", "m_o1",                  outTreeFile, m_o1)
systTree.branchTreesSysts(trees, "all", "mT_lep_MET",                  outTreeFile, mT_lep_MET)
systTree.branchTreesSysts(trees, "all", "mT_tau_MET",                  outTreeFile, mT_tau_MET)
systTree.branchTreesSysts(trees, "all", "mT_leptau_MET",                  outTreeFile, mT_leptau_MET)
systTree.branchTreesSysts(trees, "all", "m_taulep",                  outTreeFile, m_taulep)
systTree.branchTreesSysts(trees, "all", "m_jjtau",                  outTreeFile, m_jjtau)
systTree.branchTreesSysts(trees, "all", "m_jjtaulep",                  outTreeFile, m_jjtaulep)
#deltaPhi#
systTree.branchTreesSysts(trees, "all", "deltaPhi_jj",              outTreeFile, deltaPhi_jj)#
systTree.branchTreesSysts(trees, "all", "deltaPhi_taulep",          outTreeFile, deltaPhi_taulep)#
systTree.branchTreesSysts(trees, "all", "deltaPhi_tauj1",           outTreeFile, deltaPhi_tauj1)#
systTree.branchTreesSysts(trees, "all", "deltaPhi_tauj2",           outTreeFile, deltaPhi_tauj2)#
systTree.branchTreesSysts(trees, "all", "deltaPhi_lepj1",           outTreeFile, deltaPhi_lepj1)#
systTree.branchTreesSysts(trees, "all", "deltaPhi_lepj2",           outTreeFile, deltaPhi_lepj2)#
#deltaEta#
systTree.branchTreesSysts(trees, "all", "deltaEta_jj",              outTreeFile, deltaEta_jj)#
systTree.branchTreesSysts(trees, "all", "deltaEta_taulep",          outTreeFile, deltaEta_taulep)#
systTree.branchTreesSysts(trees, "all", "deltaEta_tauj1",           outTreeFile, deltaEta_tauj1)#
systTree.branchTreesSysts(trees, "all", "deltaEta_tauj2",           outTreeFile, deltaEta_tauj2)#
systTree.branchTreesSysts(trees, "all", "deltaEta_lepj1",           outTreeFile, deltaEta_lepj1)#
systTree.branchTreesSysts(trees, "all", "deltaEta_lepj2",           outTreeFile, deltaEta_lepj2)#
#deltaTheta#
systTree.branchTreesSysts(trees, "all", "deltaTheta_jj",              outTreeFile, deltaTheta_jj)#
systTree.branchTreesSysts(trees, "all", "deltaTheta_taulep",          outTreeFile, deltaTheta_taulep)#
systTree.branchTreesSysts(trees, "all", "deltaTheta_tauj1",           outTreeFile, deltaTheta_tauj1)#
systTree.branchTreesSysts(trees, "all", "deltaTheta_tauj2",           outTreeFile, deltaTheta_tauj2)#
systTree.branchTreesSysts(trees, "all", "deltaTheta_lepj1",           outTreeFile, deltaTheta_lepj1)#
systTree.branchTreesSysts(trees, "all", "deltaTheta_lepj2",           outTreeFile, deltaTheta_lepj2)#
#ptRel#
systTree.branchTreesSysts(trees, "all", "ptRel_jj",              outTreeFile, ptRel_jj)#
systTree.branchTreesSysts(trees, "all", "ptRel_taulep",          outTreeFile, ptRel_taulep)#
systTree.branchTreesSysts(trees, "all", "ptRel_tauj1",           outTreeFile, ptRel_tauj1)#
systTree.branchTreesSysts(trees, "all", "ptRel_tauj2",           outTreeFile, ptRel_tauj2)#
systTree.branchTreesSysts(trees, "all", "ptRel_lepj1",           outTreeFile, ptRel_lepj1)#
systTree.branchTreesSysts(trees, "all", "ptRel_lepj2",           outTreeFile, ptRel_lepj2)#
#other                                                                                    
systTree.branchTreesSysts(trees, "all", "SF_Fake",                  outTreeFile, SF_Fake)#
systTree.branchTreesSysts(trees, "all", "HLT_effLumi",              outTreeFile, HLT_effLumi)#
#zeppenfeld
systTree.branchTreesSysts(trees, "all", "lepton_Zeppenfeld",              outTreeFile, lepton_Zeppenfeld)#
systTree.branchTreesSysts(trees, "all", "lepton_Zeppenfeld_over_deltaEta_jj",              outTreeFile, lepton_Zeppenfeld_over_deltaEta_jj)#
systTree.branchTreesSysts(trees, "all", "tau_Zeppenfeld",              outTreeFile, tau_Zeppenfeld)#
systTree.branchTreesSysts(trees, "all", "tau_Zeppenfeld_over_deltaEta_jj",              outTreeFile, tau_Zeppenfeld_over_deltaEta_jj)#
systTree.branchTreesSysts(trees, "all", "event_Zeppenfeld",              outTreeFile, event_Zeppenfeld)#
systTree.branchTreesSysts(trees, "all", "event_Zeppenfeld_over_deltaEta_jj",              outTreeFile, event_Zeppenfeld_over_deltaEta_jj)#
systTree.branchTreesSysts(trees, "all", "event_RT",              outTreeFile, event_RT)#
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
contagood=0
#++++++++++++++++++++++++++++++++++
#++   looping over the events    ++
#++++++++++++++++++++++++++++++++++
taucont = 0
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
        print("\nevento n. " + str(i))
        if i > 1000:
            break
    
    if i%500 == 0 and not Debug:#
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
        if IsDim8:
            LHEDim8 = Collection(event, "LHEReweightingWeight")

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
    if 'DataMu' in sample.label:
        dataMu = True
    if 'DataEle' in sample.label:
        dataEle = True

    if not isMC:
        if not Flag.eeBadScFilter:
            continue

    #print "------ ", i
    passMu, passEle, passHT, noTrigger = trig_map(HLT, PV, year, runPeriod)

    if noTrigger: continue

    '''
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
    '''

    SingleEle=False
    SingleMu=False
    ElMu=False

    HighestLepPt=-999.
    LeadLepFamily="not selected"
    
    #if passEle and not HLT.Ele32_WPTight_Gsf_L1DoubleEG:
    #print("Errore")#Questo ora non dovrebbe succedere

    #print("n ele:", len(electrons), "n mu:", len(muons)) 
    

    if 'DataHT' not in sample.label:
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

    else:
        if passHT:
            ElMu=True
        else:
            continue

    #print("HighestLepPt:", HighestLepPt)
    #print("passEle:", passEle, "\tpassMu:", passMu)

    if ElMu:
        #if not isMC:
            #if dataMu:
                #SingleEle = False
                #SingleMu = True
            #elif dataEle:
                #SingleEle = True
                #SingleMu = False
        if True:#else:
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

    #if SingleEle==False and HighestLepPt>0: SingleMu=True
    vTrigEle, vTrigMu, vTrigHT = trig_finder(HLT, sample.year, sample.label)
    
    if SingleEle==True:
        if isMC: HLT_effLumi[0] = lumiFinder("Ele", vTrigEle)
        leptons = electrons
    elif SingleMu==True:
        if isMC: HLT_effLumi[0] = lumiFinder("Mu", vTrigMu)
        leptons = muons
    
    elif not (SingleMu or SingleEle):
        continue
    if SingleEle and dataMu:
        continue
    if SingleMu and dataEle:
        continue

    #print("SingleEle:", SingleEle, "\tSingleMu:", SingleMu)
    #print("lepton id:", leptons[0].pdgId)
    #if (SingleEle or SingleMu): Cut_dict[1][1]+=1
    
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

    #if (SingleEle==1 or SingleMu==1) and pass_lepton_selection[0]==1: Cut_dict[2][1]+=1
    tightlep = leptons[indexGoodLep]

    if abs(tightlep.pdgId)==13:
        lepton_pt[0]                =   tightlep.corrected_pt
    elif abs(tightlep.pdgId)==11:
        lepton_pt[0]                =   tightlep.pt
    lepton_eta[0]               =   tightlep.eta
    lepton_phi[0]               =   tightlep.phi
    lepton_mass[0]              =   tightlep.mass
    lepton_pdgid[0]             =   tightlep.pdgId
    if SingleMu==1:
        lepton_pfRelIso04[0]        =   tightlep.pfRelIso04_all
    elif SingleEle==1:
        lepton_pfRelIso04[0]        =   tightlep.jetRelIso

    #if not isMC:
    if abs(tightlep.pdgId)==11:
        lepton_SFFake_vsjet4[0] = SFFakeRatio_ele_calc(lepton_pt[0], lepton_eta[0], 'vsjet4')
        lepton_SFFake_vsjet2[0] = SFFakeRatio_ele_calc(lepton_pt[0], lepton_eta[0], 'vsjet2')
    elif abs(tightlep.pdgId)==13:
        lepton_SFFake_vsjet4[0] = SFFakeRatio_mu_calc(lepton_pt[0], lepton_eta[0], 'vsjet4')
        lepton_SFFake_vsjet2[0] = SFFakeRatio_mu_calc(lepton_pt[0], lepton_eta[0], 'vsjet2')
    #else:
    if isMC:
        lepton_isPrompt[0] = tightlep.genPartFlav

    GoodLep=tightlep
    
    mT_lep_MET[0]=mTlepMet(met, tightlep.p4())

    if isMC:
        tightlep_SF = tightlep.effSF
        #tightlep_SF = Lepton_IDIso_SF(tightlep)
        #tightlep_SFUp = tightlep.effSF_errUp
        #tightlep_SFDown = tightlep.effSF_errDown
        systTree.setWeightName("lepSF", copy.deepcopy(tightlep_SF))
        #systTree.setWeightName("lepUp", copy.deepcopy(tightlep_SFUp))
        #systTree.setWeightName("lepDown", copy.deepcopy(tightlep_SFDown))

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
    
    ThereIsOneTau, ltau_list = SelectAndVetoTaus(list(taus), tightlep)

    if ThereIsOneTau:
        taucont = taucont + 1
        indexGoodTau = ltau_list[0][0]
        if ltau_list[0][1] == 'T':
            tau_TightRegion[0] = 1
            tau_LnTRegion[0] = 0
        elif ltau_list[0][1] == 'L':
            tau_TightRegion[0] = 0
            tau_LnTRegion[0] = 1            
    else:
        continue

    GoodTau=taus[indexGoodTau]

    if tau_TightRegion[0]==1 or tau_LnTRegion[0]==1:
        pass_tau_selection[0] = 1
    else:
        pass_tau_selection[0] = 0
    

    tau_pt[0]               =   GoodTau.pt
    tau_relleadtkpt[0]      =   GoodTau.leadTkPtOverTauPt
    tau_eta[0]              =   GoodTau.eta
    tau_phi[0]              =   GoodTau.phi
    tau_mass[0]             =   GoodTau.mass
    tau_charge[0]           =   GoodTau.charge
    if isMC:
        tau_GenMatch[0]         =   GoodTau.genPartFlav
    tau_DecayMode[0]        =   GoodTau.decayMode

    #if not isMC:
    tau_SFFake_vsjet4[0] = SFFakeRatio_tau_calc(tau_pt[0], tau_eta[0], 'vsjet4')
    tau_SFFake_vsjet2[0] = SFFakeRatio_tau_calc(tau_pt[0], tau_eta[0], 'vsjet2')
    #else:
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



    deltaEta_taulep[0] = GoodTau.eta - GoodLep.eta
    deltaTheta_taulep[0] = (GoodTau.p4() - GoodLep.p4()).CosTheta()

    tauleadTk_ptOverTau[0]  =   GoodTau.leadTkPtOverTauPt#
    tauleadTk_deltaPhi[0]   =   GoodTau.leadTkDeltaPhi#
    tauleadTk_deltaEta[0]   =   GoodTau.leadTkDeltaEta#
    if not isMC:
        tauleadTk_Gamma[0] = 2.*GoodTau.leadTkPtOverTauPt - 1.
 
    #variables related to tau-associated jet
    if GoodTau.jetIdx > -1:
        taujet = jets[GoodTau.jetIdx]
        taujet_RelPt[0] = taujet.pt/GoodTau.pt
        taujet_deltaPhi[0] = deltaPhi(GoodTau, taujet)
        taujet_deltaEta[0] = taujet.eta - GoodTau.eta
        taujet_HadGamma[0] = taujet.chHEF - taujet.neHEF
        taujet_EmGamma[0] = taujet.chEmEF - taujet.neEmEF
        taujet_HEGamma[0] = taujet.chHEF - taujet.neHEF + taujet.chEmEF - taujet.neEmEF

    if isMC:
        #print('Tau genmatch:', GoodTau.genPartFlav)

        #print('pt, mass before tes&fes:', tau_pt[0], tau_mass[0])

        #real had tau
        GoodTau_vsjet_Down, GoodTau_vsjet_SF, GoodTau_vsjet_Up = tauSFTool_vsjet.getSFvsPT(GoodTau.pt, GoodTau.genPartFlav, unc='All')
        #print('vsJet SFs:', GoodTau_vsjet_Down, GoodTau_vsjet_SF, GoodTau_vsjet_Up)
        systTree.setWeightName("tau_vsjet_SF", copy.deepcopy(GoodTau_vsjet_SF))
        systTree.setWeightName("tau_vsjet_Up", copy.deepcopy(GoodTau_vsjet_Up))
        systTree.setWeightName("tau_vsjet_Down", copy.deepcopy(GoodTau_vsjet_Down))

        tes_Down, tes, tes_Up = tesTool.getTES(GoodTau.eta, GoodTau.decayMode, GoodTau.genPartFlav, unc='All')
        systTree.setWeightName("TESSF", copy.deepcopy(tes))
        systTree.setWeightName("TESUp", copy.deepcopy(tes_Up))
        systTree.setWeightName("TESDown", copy.deepcopy(tes_Down))
        #print('tes:', tes_Down, tes, tes_Up)
        tau_pt[0] *= tes
        tau_mass[0] *= tes
        tauleadTk_ptOverTau[0] *= 1/(tes)

        #ele faking tau
        GoodTau_vsele_Down, GoodTau_vsele_SF, GoodTau_vsele_Up = tauSFTool_vsele.getSFvsEta(GoodTau.eta, GoodTau.genPartFlav, unc='All')
        #print('vsEle SFs:', GoodTau_vsele_Down, GoodTau_vsele_SF, GoodTau_vsele_Up)
        systTree.setWeightName("tau_vsele_SF", copy.deepcopy(GoodTau_vsele_SF))
        systTree.setWeightName("tau_vsele_Up", copy.deepcopy(GoodTau_vsele_Up))
        systTree.setWeightName("tau_vsele_Down", copy.deepcopy(GoodTau_vsele_Down))

        fes_Down, fes, fes_Up = fesTool.getFES(GoodTau.eta, GoodTau.decayMode, GoodTau.genPartFlav, unc='All')
        systTree.setWeightName("FESSF", copy.deepcopy(fes))
        systTree.setWeightName("FESUp", copy.deepcopy(fes_Up))
        systTree.setWeightName("FESDown", copy.deepcopy(fes_Down))
        #print('fes:', fes_Down, fes, fes_Up)
        tau_pt[0] *= fes
        tau_mass[0] *= fes
        tauleadTk_ptOverTau[0] *= 1/(fes)

        if GoodTau.jetIdx > -1:
            taujet_RelPt[0] *= 1/(fes*tes)

        tauleadTk_Gamma[0] = 2.*GoodTau.leadTkPtOverTauPt/(fes*tes) - 1.

        #mu faking tau
        GoodTau_vsmu_Down, GoodTau_vsmu_SF, GoodTau_vsmu_Up = tauSFTool_vsmu.getSFvsEta(GoodTau.eta, GoodTau.genPartFlav, unc='All')
        #print('vsEle SFs:', GoodTau_vsmu_Down, GoodTau_vsmu_SF, GoodTau_vsmu_Up)
        systTree.setWeightName("tau_vsmu_SF", copy.deepcopy(GoodTau_vsmu_SF))
        systTree.setWeightName("tau_vsmu_Up", copy.deepcopy(GoodTau_vsmu_Up))
        systTree.setWeightName("tau_vsmu_Down", copy.deepcopy(GoodTau_vsmu_Down))
    
        #print('pt, mass after tes&fes:', tau_pt[0], tau_mass[0])

    if GoodTau.jetIdx > -1:
        taujet = jets[GoodTau.jetIdx]
        if isMC:
            taujet_RelPt[0] = taujet.pt/(GoodTau.pt * fes*tes)
        else:
            taujet_RelPt[0] = taujet.pt/(GoodTau.pt)
        taujet_deltaPhi[0] = deltaPhi(GoodTau, taujet)
        taujet_deltaEta[0] = taujet.eta - GoodTau.eta
        taujet_HadGamma[0] = taujet.chHEF - taujet.neHEF
        taujet_EmGamma[0] = taujet.chEmEF - taujet.neEmEF
        taujet_HEGamma[0] = taujet.chHEF - taujet.neHEF + taujet.chEmEF - taujet.neEmEF

    GoodTau_p4 = ROOT.TLorentzVector()
    if isMC:
        GoodTau_p4.SetPtEtaPhiM(GoodTau.pt*fes*tes, GoodTau.eta, GoodTau.phi, GoodTau.mass*fes*tes)
    else:
        GoodTau_p4.SetPtEtaPhiM(GoodTau.pt, GoodTau.eta, GoodTau.phi, GoodTau.mass)

    m_taulep[0]=(GoodTau_p4 + GoodLep.p4()).M()

    mT_tau_MET[0]=mTlepMet(met, GoodTau_p4)
    mT_leptau_MET[0]=mTlepMet(met, GoodTau_p4+GoodLep.p4())
    if isMC:
        m_1T[0] = M1T(GoodLep, GoodTau, met, fes*tes)
        m_o1[0] = Mo1(GoodLep, GoodTau, met, fes*tes)
    else:
        m_1T[0] = M1T(GoodLep, GoodTau, met, 1.)
        m_o1[0] = Mo1(GoodLep, GoodTau, met, 1.)


    #if not isMC:
    if lepton_LnTRegion[0]==1 and tau_LnTRegion[0]==0:
        event_SFFake_vsjet4[0] = lepton_SFFake_vsjet4[0]
        event_SFFake_vsjet2[0] = lepton_SFFake_vsjet2[0]
    elif lepton_LnTRegion[0]==0 and tau_LnTRegion[0]==1:
        event_SFFake_vsjet4[0] = tau_SFFake_vsjet4[0]
        event_SFFake_vsjet2[0] = tau_SFFake_vsjet2[0]
    elif lepton_LnTRegion[0]==1 and tau_LnTRegion[0]==1:
        event_SFFake_vsjet4[0] = lepton_SFFake_vsjet4[0]*tau_SFFake_vsjet4[0]
        event_SFFake_vsjet2[0] = lepton_SFFake_vsjet2[0]*tau_SFFake_vsjet2[0]
    elif lepton_LnTRegion[0]==0 and tau_LnTRegion[0]==0:
        event_SFFake_vsjet4[0] = 0.
        event_SFFake_vsjet2[0] = 0.

    if isMC:
        if event_SFFake_vsjet4[0]>0.:
            if abs(lepton_isPrompt[0])==1 or abs(tau_isPrompt[0])==5:
                event_SFFake_vsjet4[0] = -1.*event_SFFake_vsjet4[0]
            else:
                event_SFFake_vsjet4[0] = 0.
        if event_SFFake_vsjet2[0]>0.:
            if abs(lepton_isPrompt[0])==1 or abs(tau_isPrompt[0])==5:
                event_SFFake_vsjet2[0] = -1.*event_SFFake_vsjet2[0]
            else:
                event_SFFake_vsjet2[0] = 0.
        

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
    leadjet_DeepCSVv2_b[0]      =   jet1.btagDeepB
    leadjet_CSVv2_b[0]          =   jet1.btagCSVV2
    subleadjet_pt[0]            =   jet2.pt
    subleadjet_eta[0]           =   jet2.eta
    subleadjet_phi[0]           =   jet2.phi
    subleadjet_mass[0]          =   jet2.mass
    subleadjet_DeepFlv_b[0]     =   jet2.btagDeepFlavB
    subleadjet_DeepCSVv2_b[0]   =   jet2.btagDeepB
    subleadjet_CSVv2_b[0]       =   jet2.btagCSVV2
    
    pass_jet_selection[0]=1

    #calculating deltaPhi                                                                                                      
    deltaPhi_jj[0]      =   deltaPhi(jet1, jet2)#
    deltaPhi_taulep[0]  =   deltaPhi(GoodTau, GoodLep)#
    deltaPhi_tauj1[0]   =   deltaPhi(GoodTau, jet1)#
    deltaPhi_tauj2[0]   =   deltaPhi(GoodTau, jet2)#
    deltaPhi_lepj1[0]   =   deltaPhi(GoodLep, jet1)#
    deltaPhi_lepj2[0]   =   deltaPhi(GoodLep, jet2)#

    #calculating deltaEta                                                                                                      
    deltaEta_jj[0]      =   jet1.eta - jet2.eta#
    deltaEta_taulep[0]  =   GoodTau.eta - GoodLep.eta#
    deltaEta_tauj1[0]   =   GoodTau.eta - jet1.eta#
    deltaEta_tauj2[0]   =   GoodTau.eta - jet2.eta#
    deltaEta_lepj1[0]   =   GoodLep.eta - jet1.eta#
    deltaEta_lepj2[0]   =   GoodLep.eta - jet2.eta#

    #calculating deltaTheta                                                                                                      
    deltaTheta_jj[0]      =   (jet1.p4() - jet2.p4()).CosTheta()
    deltaTheta_taulep[0]  =   (GoodTau_p4 - GoodLep.p4()).CosTheta()
    deltaTheta_tauj1[0]   =   (GoodTau_p4 - jet1.p4()).CosTheta()
    deltaTheta_tauj2[0]   =   (GoodTau_p4 - jet2.p4()).CosTheta()
    deltaTheta_lepj1[0]   =   (GoodLep.p4() - jet1.p4()).CosTheta()
    deltaTheta_lepj2[0]   =   (GoodLep.p4() - jet2.p4()).CosTheta()


    #calculating ptRel                                                                                                      
    ptRel_jj[0]      =   get_ptrel(jet1, jet2, 1.)
    if isMC:
        ptRel_taulep[0]  =   get_ptrel(GoodTau, GoodLep, (fes*tes))
        ptRel_tauj1[0]   =   get_ptrel(GoodTau, jet1, (fes*tes))
        ptRel_tauj2[0]   =   get_ptrel(GoodTau, jet2, (fes*tes))
    else:
        ptRel_taulep[0]  =   get_ptrel(GoodTau, GoodLep, 1.)
        ptRel_tauj1[0]   =   get_ptrel(GoodTau, jet1, 1.)
        ptRel_tauj2[0]   =   get_ptrel(GoodTau, jet2, 1.)
    ptRel_lepj1[0]   =   get_ptrel(GoodLep, jet1, 1.)
    ptRel_lepj2[0]   =   get_ptrel(GoodLep, jet2, 1.)

    lepton_Zeppenfeld[0], tau_Zeppenfeld[0], event_Zeppenfeld[0] = Zeppenfeld(lepton_eta[0], tau_eta[0], leadjet_eta[0], subleadjet_eta[0])

    AK8jet1, dR_jet1AK48 = closest(jet1, fatjets)
    AK8jet2, dR_jet2AK48 = closest(jet1, fatjets)
    
    if dR_jet1AK48 < 0.8:
        AK8leadjet_pt[0]               =   AK8jet1.pt
        AK8leadjet_eta[0]              =   AK8jet1.eta
        AK8leadjet_phi[0]              =   AK8jet1.phi
        AK8leadjet_mass[0]             =   AK8jet1.msoftdrop
    
        AK8leadjet_tau21[0]             =   AK8jet1.tau2/((AK8jet1.tau1==0.)*1 + (AK8jet1.tau1!=0.)*AK8jet1.tau1)
        AK8leadjet_tau32[0]             =   AK8jet1.tau3/((AK8jet1.tau2==0.)*1 + (AK8jet1.tau2!=0.)*AK8jet1.tau2)
        AK8leadjet_tau43[0]             =   AK8jet1.tau4/((AK8jet1.tau3==0.)*1 + (AK8jet1.tau3!=0.)*AK8jet1.tau3)
        leadjet_dRAK48[0] = copy.deepcopy(dR_jet1AK48)

    if dR_jet2AK48 < 0.8:
        AK8subleadjet_pt[0]               =   AK8jet2.pt
        AK8subleadjet_eta[0]              =   AK8jet2.eta
        AK8subleadjet_phi[0]              =   AK8jet2.phi
        AK8subleadjet_mass[0]             =   AK8jet2.msoftdrop
        
        AK8subleadjet_tau21[0]             =   AK8jet2.tau2/((AK8jet2.tau1==0.)*1 + (AK8jet2.tau1!=0.)*AK8jet2.tau1)
        AK8subleadjet_tau32[0]             =   AK8jet2.tau3/((AK8jet2.tau2==0.)*1 + (AK8jet2.tau2!=0.)*AK8jet2.tau2)
        AK8subleadjet_tau43[0]             =   AK8jet2.tau4/((AK8jet2.tau3==0.)*1 + (AK8jet2.tau3!=0.)*AK8jet2.tau3)
        subleadjet_dRAK48[0] = copy.deepcopy(dR_jet2AK48)


    if not BVeto(jets): pass_b_veto[0]=1

    #if (SingleEle or SingleMu) and pass_lepton_selection[0]==1 and pass_lepton_iso[0]==1 and pass_tau_vsJetWP[0]==1 and pass_lepton_veto[0]==1 and pass_tau_selection[0]==1 and pass_charge_selection[0]==1 and pass_jet_selection[0]==1 and pass_b_veto[0]==1:
    #Cut_dict[7][1]+=1

    #if (SingleEle or SingleMu) and pass_lepton_selection[0]==1 and pass_lepton_veto[0]==1 and pass_tau_selection_ML[0]==1 and pass_charge_selection[0]==1 and pass_jet_selection[0]==1 and pass_b_veto[0]==1:  pass_upToBVeto_ML[0]=1#

    if (SingleEle or SingleMu) and pass_lepton_selection[0]==1 and pass_lepton_veto[0]==1 and pass_tau_selection[0]==1 and pass_charge_selection[0]==1 and pass_jet_selection[0]==1 and pass_b_veto[0]==1: pass_upToBVeto[0]=1#

    leadJet=ROOT.TLorentzVector()
    subleadJet=ROOT.TLorentzVector()
    leadJet.SetPtEtaPhiM(jet1.pt, jet1.eta, jet1.phi, jet1.mass)
    subleadJet.SetPtEtaPhiM(jet2.pt, jet2.eta, jet2.phi, jet2.mass) 
    
    if not JetCut(leadJet, subleadJet): pass_mjj_cut[0]=1

    m_jj[0]=(leadJet + subleadJet).M()
    m_jjtau[0]=(leadJet + subleadJet + GoodTau_p4).M()
    m_jjtaulep[0]=(leadJet + subleadJet + GoodTau_p4 + GoodLep.p4()).M()

    lepton_Zeppenfeld_over_deltaEta_jj[0] = lepton_Zeppenfeld[0]/deltaEta_jj[0]
    tau_Zeppenfeld_over_deltaEta_jj[0] = tau_Zeppenfeld[0]/deltaEta_jj[0]
    lepton_Zeppenfeld_over_deltaEta_jj[0] = event_Zeppenfeld[0]/deltaEta_jj[0]

    if isMC:
        event_RT[0] = (GoodLep.pt * GoodTau.pt*(fes*tes)) / (jet1.pt * jet2.pt)
    else:
        event_RT[0] = (GoodLep.pt * GoodTau.pt) / (jet1.pt * jet2.pt)

    #if (SingleEle or SingleMu) and pass_lepton_iso[0]==1 and pass_tau_vsJetWP[0]==1 and  pass_lepton_selection[0]==1 and pass_lepton_veto[0]==1 and pass_tau_selection[0]==1 and pass_charge_selection[0]==1 and pass_jet_selection[0]==1 and pass_b_veto[0]==1 and pass_mjj_cut[0]==1: Cut_dict[8][1]+=1

    if not metCut(met): pass_MET_cut[0]=1

    #if (SingleEle or SingleMu) and pass_lepton_selection[0]==1 and pass_lepton_iso[0]==1 and pass_tau_vsJetWP[0]==1 and pass_lepton_veto[0]==1 and pass_tau_selection[0]==1 and pass_charge_selection[0]==1 and pass_jet_selection[0]==1 and pass_b_veto[0]==1 and pass_mjj_cut[0]==1 and pass_MET_cut[0]==1:
    #Cut_dict[9][1]+=1

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
                        #print("opn:", opn, "opmax:", opmax, "step:", step, "epoint:", epoint)
                        #print('index:', EFT_operator[opn]["idx"], 'eidx:', eidx)
                        idxpos = int((EFT_operator[opn]["idx"])*11 - (eidx + 1))
                        idxneg = int((EFT_operator[opn]["idx"] - 1)*11 + eidx)
                        if IsZero and idxneg != idxpos:
                            print("Something went wrong with dim8 weights assignment")
                            #break
                        wpos = LHEitem(LHEDim8[idxpos])
                        wneg = LHEitem(LHEDim8[idxneg])
                        #print('idxneg:', idxneg, 'wneg:', wneg)
                        #print('idxpos:', idxpos, 'wpos:', wpos)

                        w_pos[0] = copy.deepcopy(wpos)
                        w_neg[0] = copy.deepcopy(wneg)

                        wsign = 0
                        kpow = 0
                        #print(sample.label, "_BSM_" in sample.label, "_0_" in sample.label, "_INT_" in sample.label)
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
                            
                        #print("wsign:", wsign, "kpow:", kpow)

                        w_coeff = (wpos + wsign * wneg) / kpow
                        #print("w_coeff:", w_coeff)
                        w_dim8[0] = copy.deepcopy(w_coeff)
        

                        break
                break
        #print("w_dim8:", w_dim8[0])

    systTree.fillTreesSysts(trees, "all")

#trees[0].Print()
outTreeFile.cd()
if(isMC):
    #print("h_genweight first bin content is %f and h_PDFweight has %f bins" %(h_genweight.GetBinContent(1), h_PDFweight.GetNbinsX()))
    h_genweight.Write()
    if isthere_pdf:
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

if Debug:
    for cutname, counts in Cut_dict.items():
        print(counts[0], round(counts[1], 4))
'''

systTree.writeTreesSysts(trees, outTreeFile)
print("Number of events in output tree " + str(trees[0].GetEntries()))

endTime = datetime.datetime.now()
print("Ending running at " + str(endTime) + "\n Goodbye")

print("events with one only at-least-loose tau:", taucont)
