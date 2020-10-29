# In this file values for cuts and constant will be stored and then recalled from the whole analysis function
#Using nanoAOD version 102X

ONLYELE=1
ONLYMU=0


PT_CUT_MU=  35
ETA_CUT_MU= 2.4
ISO_CUT_MU= 0.15

PT_CUT_ELE=  35
ETA_CUT_ELE= 2.4
ISO_CUT_ELE= 0.08

REL_ISO_CUT_LEP_VETO_ELE=   0.0994
PT_CUT_LEP_VETO_ELE=        15
ETA_CUT_LEP_VETO_ELE=       2.4
REL_ISO_CUT_LEP_VETO_MU=    0.25
PT_CUT_LEP_VETO_MU=         10
ETA_CUT_LEP_VETO_MU=        2.4

DR_OVERLAP_CONE_TAU=        0.5
DR_OVERLAP_CONE_OTHER=      0.4

PT_CUT_JET= 30
ETA_CUT_JET=5

DELTAETA_JJ_CUT=2.5

#btag info: l 13 skimtree_utils.BTAG_ALGO="CSVv2"   #CSVv2, DeepCSV, DeepFLV
BTAG_PT_CUT =   30
BTAG_ETA_CUT=   5
BTAG_ALGO   =   "DeepFlv"
BTAG_WP     =   "M"

ID_TAU_RECO_DEEPTAU_VSJET=  32#byDeepTau2017v2p1VSjet ID working points (deepTau2017v2p1): bitmask 1 = VVVLoose, 2 = VVLoose, 4 = VLoose, 8 = Loose, 16 = Medium, 32 = Tight, 64 = VTight, 128 = VVTight

ID_TAU_RECO_DEEPTAU_VSELE=  2 #byDeepTau2017v2p1VSe ID working points (deepTau2017v2p1): bitmask 1 = VVVLoose, 2 = VVLoose, 4 = VLoose, 8 = Loose, 16 = Medium, 32 = Tight, 64 = VTight, 128 = VVTight

ID_TAU_RECO_DEEPTAU_VSMU=   2 #byDeepTau2017v2p1VSmu ID working points (deepTau2017v2p1): bitmask 1 = VLoose, 2 = Loose, 4 = Medium, 8 = Tight

ID_TAU_RECO_MVA=            8 #IsolationMVArun2v1DBoldDMwLT ID working point (2017v1): bitmask 1 = VVLoose, 2 = VLoose, 4 = Loose, 8 = Medium, 16 = Tight, 32 = VTight, 64 = VVTight
ID_TAU_ANTIMU=              1 #Anti-muon discriminator V3: : bitmask 1 = Loose, 2 = Tight
ID_TAU_ANTIELE=             2 #Anti-electron MVA discriminator V6 (2015): bitmask 1 = VLoose, 2 = Loose, 4 = Medium, 8 = Tight, 16 = VTight

PT_CUT_TAU=30
ETA_CUT_TAU=2.4

M_JJ_CUT=   500
MET_CUT=    40
