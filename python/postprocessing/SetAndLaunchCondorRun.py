import os
import optparse
import sys

cshname = "condorrun.csh"

usage = 'python SetAndLaunchCondorRun.py -y year -j wp_jet -m wp_mu -e wp_ele'
parser = optparse.OptionParser(usage)
parser.add_option('-y', dest='year', type=str, default = '2017', help='Please enter a year, default is 2017')
parser.add_option('-j', dest='jetwp', type=str, default = '', help='Please enter a TauID WP for vsJet')
parser.add_option('-m', dest='muwp', type=str, default = '', help='Please enter a TauID WP for vsMu')
parser.add_option('-e', dest='elewp', type=str, default = '', help='Please enter a TauID WP for vsEle')

(opt, args) = parser.parse_args()

vsJet_dict = {"VVVL": '1',
              "VVL": '2',
              "VL": '4',
              "L": '8',
              "M": '16',
              "T": '32',
              "VT": '64',
              "VVT": '128',
}

vsMu_dict = {"VL": '1',
             "L": '2',
             "M": '4',
             "T": '8'
}

vsEle_dict = {"VVVL": '1',
              "VVL": '2',
              "VL": '4',
              "L": '8',
              "M": '16',
              "T": '32',
              "VT": '64',
              "VVT": '128',
}

username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])

folder = "Eff_Jet" + opt.jetwp + "_Mu" + opt.muwp + "_Ele" + opt.elewp
path = "/eos/user/" + inituser + "/" + username + "/VBS/nosynch/" + folder + "/"
print folder, path
'''
if not os.path.exists(path):
    os.makedirs(path)
'''

f = open(cshname, "w")
print f
#f.write("set folder='" + folder + "'\n")
#f.write("set year='"+ opt.year + "'\n")
f.write("python submit_condor.py -d TT_" + opt.year + " -f " + folder + " --wp " + str(opt.jetwp + opt.muwp + opt.elewp) + "\n")
f.write("python submit_condor.py -d WJets_" + opt.year + " -f " + folder + " --wp " + str(opt.jetwp + opt.muwp + opt.elewp) + "\n")
f.write("python submit_condor.py -d WZ_" + opt.year + " -f " + folder + " --wp " + str(opt.jetwp + opt.muwp + opt.elewp) + "\n")
f.write("python submit_condor.py -d DYJetsToLL_" + opt.year + " -f " + folder + " --wp " + str(opt.jetwp + opt.muwp + opt.elewp) + "\n")
f.write("python submit_condor.py -d WpWpJJ_EWK_" + opt.year + " -f " + folder + " --wp " + str(opt.jetwp + opt.muwp + opt.elewp) + "\n")
f.write("python submit_condor.py -d WpWpJJ_QCD_" + opt.year + " -f " + folder + " --wp " + str(opt.jetwp + opt.muwp + opt.elewp) + "\n")
f.close()

t = open("CutsAndValues_bu.py", "w")
t.write("# In this file values for cuts and constant will be stored and then recalled from the whole analysis function\n")
t.write("#Using nanoAOD version 102X\n")
t.write("ONLYELE=1\n")
t.write("ONLYMU=0\n\n")

t.write("PT_CUT_MU=  35\n")
t.write("ETA_CUT_MU= 2.4\n")
t.write("ISO_CUT_MU= 0.15\n\n")

t.write("PT_CUT_ELE=  35\n")
t.write("ETA_CUT_ELE= 2.4\n")
t.write("ISO_CUT_ELE= 0.08\n\n")

t.write("REL_ISO_CUT_LEP_VETO_ELE=   0.0994\n")
t.write("PT_CUT_LEP_VETO_ELE=        15\n")
t.write("ETA_CUT_LEP_VETO_ELE=       2.4\n")
t.write("REL_ISO_CUT_LEP_VETO_MU=    0.25\n")
t.write("PT_CUT_LEP_VETO_MU=         10\n")
t.write("ETA_CUT_LEP_VETO_MU=        2.4\n\n")

t.write("DR_OVERLAP_CONE_TAU=        0.5\n")
t.write("DR_OVERLAP_CONE_OTHER=      0.4\n\n")

t.write("PT_CUT_JET= 30\n")
t.write("ETA_CUT_JET=5\n\n")

t.write("DELTAETA_JJ_CUT=2.5\n\n")

#t.write("#btag info: l 13 skimtree_utils.BTAG_ALGO='CSVv2'   #CSVv2, DeepCSV, DeepFLV\n")
t.write("BTAG_PT_CUT =   30\n")
t.write("BTAG_ETA_CUT=   5\n")
t.write("BTAG_ALGO   =   'DeepFlv'\n")
t.write("BTAG_WP     =   'M'\n")
t.write("ID_TAU_RECO_DEEPTAU_VSJET=  " + vsJet_dict[opt.jetwp] + " #byDeepTau2017v2p1VSjet ID working points (deepTau2017v2p1): bitmask 1 = VVVLoose, 2 = VVLoose, 4 = VLoose, 8 = Loose, 16 = Medium, 32 = Tight, 64 = VTight, 128 = VVTight\n")
t.write("ID_TAU_RECO_DEEPTAU_VSELE=  " + vsEle_dict[opt.elewp] + "  #byDeepTau2017v2p1VSe ID working points (deepTau2017v2p1): bitmask 1 = VVVLoose, 2 = VVLoose, 4 = VLoose, 8 = Loose, 16 = Medium, 32 = Tight, 64 = VTight, 128 = VVTight\n")
t.write("ID_TAU_RECO_DEEPTAU_VSMU=   " + vsMu_dict[opt.muwp] + "  #byDeepTau2017v2p1VSmu ID working points (deepTau2017v2p1): bitmask 1 = VLoose, 2 = Loose, 4 = Medium, 8 = Tight\n")
t.write("ID_TAU_RECO_MVA=            8 #IsolationMVArun2v1DBoldDMwLT ID working point (2017v1): bitmask 1 = VVLoose, 2 = VLoose, 4 = Loose, 8 = Medium, 16 = Tight, 32 = VTight, 64 = VVTight\n")
t.write("ID_TAU_ANTIMU=              1 #Anti-muon discriminator V3: : bitmask 1 = Loose, 2 = Tight\n")
t.write("ID_TAU_ANTIELE=             2 #Anti-electron MVA discriminator V6 (2015): bitmask 1 = VLoose, 2 = Loose, 4 = Medium, 8 = Tight, 16 = VTight\n")
t.write("PT_CUT_TAU=30\n")
t.write("ETA_CUT_TAU=2.4\n")
t.write("M_JJ_CUT=   500\n")
t.write("MET_CUT=    40\n")
t.close()

os.system("source ./" + cshname)

