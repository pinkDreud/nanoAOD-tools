import os
import optparse
import sys
from samples.samples import *

cshname = "condorrun_tauwp.csh"
split = 50

def CondoredList(samplename):
    try:
        condlist = os.listdir(path+samplename)
    except:
        condlist = []

    if len(condlist) > 0:
        for condfile in condlist:
            if os.stat(path+samplename+"/"+condfile).st_size < 1024.:
                print("Something went wrong during condoring", samplename, "fix it and relaunch")
                os.system("rm -r "+ path + samplename + "/*")            
                return CondoredList(samplename)

    return condlist

def DoesSampleExist(samplename):
    if samplename+".txt" not in os.listdir("../../crab/macros/files/"):
        return False
    else:
        return True
                
def AreAllCondored(crabname, condorname):
    storelist = [line for line in open("../../crab/macros/files/"+crabname+".txt")]

    condoredlist = CondoredList(condorname)

    if condorname+"_merged.root" in condoredlist:
        condoredlist.remove(condorname+"_merged.root")
    if condorname+".root" in condoredlist:
        condoredlist.remove(condorname+".root")

    lenstore = len(storelist)

    if 'Data' in crabname:
        remainder = int(lenstore%split)
        lenstore = int(lenstore/split)
        if remainder > 0:
            lenstore += 1

    if len(condoredlist) < lenstore:
        print("condored: ", len(condoredlist), "\tlenstore: ", lenstore)
        return False
    elif lenstore==0 and len(condoredlist)==0:
        print("Warning for", samplename, "False flag for crabbed files! need to recrab them")
        return True
    else:
        return True
        
usage = 'python SetAndLaunchCondorRun.py -y year -j wp_jet -m wp_mu -e wp_ele -f folder --max max_jobs -c -d dataset'
parser = optparse.OptionParser(usage)
parser.add_option('-y', dest='year', type=str, default = '2017', help='Please enter a year, default is 2017')
parser.add_option('-j', dest='jetwp', type=str, default = 'VT', help='Please enter a TauID WP for vsJet')
parser.add_option('-m', dest='muwp', type=str, default = 'T', help='Please enter a TauID WP for vsMu')
parser.add_option('-e', dest='elewp', type=str, default = 'VL', help='Please enter a TauID WP for vsEle')
parser.add_option('-f', dest='fold', type=str, default = 'v30', help='Please enter a folder')
parser.add_option('--max', dest='maxj', type=int, default = 0, help='Please enter a maximum for number of condor jobs')
parser.add_option('-c', dest='check', default = False, action='store_true', help='Default executes condorrun')
parser.add_option('-d', dest='dat', type=str, default = 'all', help='Default is all')
parser.add_option('--rw', dest='rw', default = False, action='store_true', help='Rewrite the files if not are all condored for a specific sample')
parser.add_option('--try', dest='tryy', default = False, action='store_true', help='Rewrite the files if not are all condored for a specific sample')
parser.add_option('--nodata', dest='nodata', default = False, action='store_true', help='Not processing Data files')
parser.add_option('--ch', dest='channel', type=str, default = 'ltau', help='Select final state, default is h_tau + lepton')


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

print(username)
print(opt.dat)

if opt.fold == '':
    folder = "Eff_Jet" + opt.jetwp + "_Mu" + opt.muwp + "_Ele" + opt.elewp
else:
    folder = opt.fold + "/" + opt.channel

path = "/eos/home-" + inituser + "/" + username + "/VBS/nosynch/" + folder + "/" + opt.channel + "/"
print(path)

subpy = ""
optstring = " -f " + folder # + " --wpjet " + str(opt.jetwp) + " --wpele " + str(opt.elewp) + " --wpmu " + str(opt.muwp)# + " --wop"

if opt.tryy:
    subpy = "submit_condor_try.py"
    if opt.channel == "ltau":
        optstring += " --wpjet " + str(opt.jetwp) + " --wpele " + str(opt.elewp) + " --wpmu " + str(opt.muwp)
elif opt.channel == "ltau":
    subpy = "submit_condor.py"
    optstring += " --wpjet " + str(opt.jetwp) + " --wpele " + str(opt.elewp) + " --wpmu " + str(opt.muwp)
elif opt.channel == "emu":
    subpy = "diet_submit_condor.py"

if not os.path.exists(path):
    os.makedirs(path)

if opt.maxj > 0:
    optstring = optstring + " --max " + str(opt.maxj)
optstring = optstring + "\n"

f = open(cshname, "w")

dirlist = [dirs for dirs in os.listdir(path) if os.path.isdir(path+dirs)]

#print(condor_dict.items())

for prname, proc in condor_dict.items():

    if opt.year not in prname:
        continue
    if "Fake" in prname or prname.startswith("DataMET") or prname.startswith('DataHT') or '_BSM_INT_' in prname:# or prname.startswith('DY'):
        continue
        
    toLaunch = True

    if hasattr(proc, 'components'):
        for sample in proc.components:
            if "Fake" in sample.label:
                continue
            elif opt.nodata and 'Data' in sample.label:
                continue
            if opt.dat != 'all':
                if not (str(sample.label).startswith(opt.dat) or prname.startswith(opt.dat)):
                    continue

            if not DoesSampleExist(sample.name):
                continue
                #if sample.label in dirlist:
            if os.path.exists(path+sample.label):
                if opt.rw:
                    print('Relaunching all the jobs for', sample.label)
                    os.system("rm -r "+ path + sample.label + "/*")
            if not AreAllCondored(sample.name, sample.label):
                if opt.check:
                    print(sample.label, "not completely condored")
                    print("python " + subpy + " -d " + sample.label+ " " + optstring)
                else:
                    if os.path.exists(path+sample.label):
                        print("Setting jobs for missing condored files...")
                    print("Writing " + sample.label + " in csh...")
                    f.write("python " + subpy + " -d " + sample.label+ " " + optstring)
            else:
                print(sample.label, " completely condored")

    else:

        if opt.dat != 'all':
            if not prname.startswith(opt.dat):
                continue

        if not DoesSampleExist(proc.name):
            continue
        if os.path.exists(path+proc.label):
            if opt.rw:
                print('Relaunching all the jobs for', proc.label)
                os.system("rm -f "+ path + proc.label + "/*")
        if not AreAllCondored(proc.name, proc.label):
            if opt.check:
                print(proc.label, "not completely condored")
                print("python " + subpy + " -d " + proc.label + " " + optstring)
            else:
                if os.path.exists(path+proc.label):
                        print("Setting jobs for missing condored files...")

                print("Writing " + proc.label + " in csh...")  
                f.write("python " + subpy + " -d " + proc.label+ " " + optstring)

        else:
            print(proc.label, " completely condored")

f.close()

if not opt.check:
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
    
    t.write("REL_ISO_CUT_LEP_VETO_ELE=   0.2\n")
    t.write("PT_CUT_LEP_VETO_ELE=        15\n")
    t.write("ETA_CUT_LEP_VETO_ELE=       2.4\n")
    t.write("REL_ISO_CUT_LEP_VETO_MU=    0.4\n")
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
    t.write("ID_TAU_RECO_DEEPTAU_VSJET_LOOSE_ELE = 8" + " #byDeepTau2017v2p1VSjet ID working points (deepTau2017v2p1): bitmask 1 = VVVLoose, 2 = VVLoose, 4 = VLoose, 8 = Loose, 16 = Medium, 32 = Tight, 64 = VTight, 128 = VVTight\n")
    t.write("ID_TAU_RECO_DEEPTAU_VSJET_LOOSE_MU = 4" + " #byDeepTau2017v2p1VSjet ID working points (deepTau2017v2p1): bitmask 1 = VVVLoose, 2 = VVLoose, 4 = VLoose, 8 = Loose, 16 = Medium, 32 = Tight, 64 = VTight, 128 = VVTight\n")
    t.write("ID_TAU_RECO_DEEPTAU_VSJET=  " + vsJet_dict[opt.jetwp] + " #byDeepTau2017v2p1VSjet ID working points (deepTau2017v2p1): bitmask 1 = VVVLoose, 2 = VVLoose, 4 = VLoose, 8 = Loose, 16 = Medium, 32 = Tight, 64 = VTight, 128 = VVTight\n")
    t.write("ID_TAU_RECO_DEEPTAU_VSELE=  " + vsEle_dict[opt.elewp] + "  #byDeepTau2017v2p1VSe ID working points (deepTau2017v2p1): bitmask 1 = VVVLoose, 2 = VVLoose, 4 = VLoose, 8 = Loose, 16 = Medium, 32 = Tight, 64 = VTight, 128 = VVTight\n")
    t.write("ID_TAU_RECO_DEEPTAU_VSMU=   " + vsMu_dict[opt.muwp] + "  #byDeepTau2017v2p1VSmu ID working points (deepTau2017v2p1): bitmask 1 = VLoose, 2 = Loose, 4 = Medium, 8 = Tight\n")
    t.write("ID_TAU_RECO_MVA=            8 #IsolationMVArun2v1DBoldDMwLT ID working point (2017v1): bitmask 1 = VVLoose, 2 = VLoose, 4 = Loose, 8 = Medium, 16 = Tight, 32 = VTight, 64 = VVTight\n")
    t.write("ID_TAU_ANTIMU=              1 #Anti-muon discriminator V3: : bitmask 1 = Loose, 2 = Tight\n")
    t.write("ID_TAU_ANTIELE=             2 #Anti-electron MVA discriminator V6 (2015): bitmask 1 = VLoose, 2 = Loose, 4 = Medium, 8 = Tight, 16 = VTight\n")
    t.write("PT_CUT_TAU=30\n")
    t.write("ETA_CUT_TAU=2.3\n")
    t.write("M_JJ_CUT=   500\n")
    t.write("MET_CUT=    40\n")
    t.close()
    
    print("Launching jobs on condor...")
    os.system("source ./" + cshname)
    print("Done! Goodbye my friend :D")
