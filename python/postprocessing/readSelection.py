from skimtree_utils import *
import ROOT
import os
import optparse
import sys
from samples.samples import *

def outSandB(directory="/eos/user/m/mmagheri/VBS/nosynch/Eff_JetM_MuL_EleL/DY1JetsToLL_2017/DY1JetsToLL_2017_part0.root"):
    chain = ROOT.TChain('events_all')
    chain.Add(directory)
    #print chain
    tree = InputTree(chain)
    #print tree.GetEntries()

    infile = ROOT.TFile(directory, "READ")
    nev = infile.Get("h_genweight").GetBinContent(1)

    isSignal=False
    if "WpWpJJ_EWK" in directory: isSignal=True
    else: isSignal=False
    
    passEvents = [nev,0,0,0,0,0,0,0,0,0]
    
    
    passEvents[1]=tree.GetEntries()
    
    for i in range(tree.GetEntries()):
        if i%100000==0: print "Processing event ----- ",i 
        event = Event(tree,i)
        passed = Object(event, "pass")
        if passed.lepton_selection: passEvents[2]+=1
        if passed.lepton_selection and passed.lepton_veto: passEvents[3]+=1
        if passed.lepton_selection and passed.lepton_veto and passed.tau_selection: passEvents[4]+=1
        if passed.lepton_selection and passed.lepton_veto and passed.tau_selection and passed.charge_selection: passEvents[5]+=1
        if passed.lepton_selection and passed.lepton_veto and passed.tau_selection and passed.charge_selection and passed.jet_selection: passEvents[6]+=1
        if passed.lepton_selection and passed.lepton_veto and passed.tau_selection and passed.charge_selection and passed.jet_selection and passed.b_veto: passEvents[7]+=1
        if passed.lepton_selection and passed.lepton_veto and passed.tau_selection and passed.charge_selection and passed.jet_selection and passed.b_veto and passed.mjj_cut: passEvents[8]+=1
        if passed.lepton_selection and passed.lepton_veto and passed.tau_selection and passed.charge_selection and passed.jet_selection and passed.b_veto and passed.mjj_cut and passed.MET_cut: passEvents[9]+=1
    
    return passEvents, isSignal



def NormalizeToxSecTimesLumi(entries, xSec, lumi):
    outevents=[0,0,0,0,0,0,0,0,0,0]
    totalEvents=entries[0]
    k=xSec*lumi*1000/totalEvents
    for i in range(len(entries)):
        outevents[i]=entries[i]*k
    
    return outevents



usage = 'python SetAndLaunchCondorRun.py -y year'
parser = optparse.OptionParser(usage)
parser.add_option('-y', dest='year', type=str, default = '2017', help='Please enter a year, default is 2017')

(opt, args) = parser.parse_args()

authors_dict = {'a': 'apiccine',
                'm': 'mmagheri',
}

wpset_dict = {'a': [('M', 'VL', 'VVL'),
                    ('T', 'VL', 'VVL'),
                    ('VT', 'VL', 'VVL'),
                    ('M', 'L', 'VVL'),
                    ('T', 'L', 'VVL'),
                    ('VT', 'L', 'VVL'),
                    ('M', 'VL', 'VL'),
                    ('T', 'VL', 'VL'),
                    ('VT', 'VL', 'VL'),
                    ],
              'm': [('M', 'L', 'VL'),
                    ('T', 'L', 'VL'),
                    ('VT', 'L', 'VL'),
                    ('M', 'VL', 'L'),
                    ('T', 'VL', 'L'),
                    ('VT', 'VL', 'L'),
                    ('M', 'L', 'L'),
                    ('T', 'L', 'L'),
                    ('VT', 'L', 'L'),
                    ],
}

#username = str(os.environ.get('USER'))
#inituser = str(os.environ.get('USER')[0])

OutFile = open("OutCuts_AllWP.txt","w") 
OutSignif = open("OutSignificance.txt", "w")

for aut, wpconfs in wpset_dict.items():
    #carica autore e wp config
    seppiawp=0
    for wpconf in wpconfs:
        #scrive la path a seconda di chi ha prodotto una certa wp config
        if wpconf==wpconfs[0] or wpconf==wpconfs[1] or wpconf==wpconfs[2]: continue
        print "Starting to work --- \n \n"
        
        path = "/eos/user/" + aut + "/" + authors_dict[aut] + "/VBS/nosynch/Eff_Jet" + wpconf[0] + "_Mu" + wpconf[1] + "_Ele" + wpconf[2] + "/"
        print path
        print "WP done till now ", seppiawp*1.0/len(wpconfs)*100, "%"
        print "WP tauvsJet: ", wpconf[0], " WP tauvsMu: ", wpconf[1], " WP tauvsEle: ", wpconf[2]
        OutFile.writelines(["WP tauvsJet: ", wpconf[0], " WP tauvsMu: ", wpconf[1], " WP tauvsEle: ", wpconf[2], "/n"])
        OutSignif.writelines(["WP tauvsJet: ", wpconf[0], " WP tauvsMu: ", wpconf[1], " WP tauvsEle: ", wpconf[2], "/n"])
        #se non esiste, va avanti
        if not os.path.exists(path):
            continue

        #carica le cartelle dei sample
        dirlist = [dirs for dirs in os.listdir(path)]

        #sample_dict
        s=[0,0,0,0,0,0,0,0,0,0]
        b=[0,0,0,0,0,0,0,0,0,0]
        
        lentot=len(dirlist)
        seppiasample=0
        for dirn in dirlist:
            print "directories done: ", seppiasample*1.0/lentot*100, "%"
            #carica il _merged.root
            xSec=sample_dict[dirn].sigma
            mergedfile = path + dirn + "/" + dirn + "_merged.root"
            OutFile.writelines(["Working on sample ", dirn, "\n"])
            print "Working on sample ", dirn
            
            CutFlow, isSignal=outSandB(mergedfile)

            outNormalized=NormalizeToxSecTimesLumi(CutFlow, xSec, 41.3)
            
            for nNorm in outNormalized:
                print nNorm
                OutFile.writelines([str(nNorm), "\n"])
            
            for j in range(len(outNormalized)):
                if isSignal:    s[j]+=outNormalized[j]
                else:           b[j]+=outNormalized[j]
            
            seppiasample+=1

        seppiawp+=1

        signif=999
        ratio=999
        print  "il numero di eventi di segnale:  ", s[len(s)-1], "\t numero eventi di fondo: ", b[len(s)-1]
        if s[len(s)-1]+b[len(s)-1]!=0:
            signif = s[len(s)-1] / (s[len(s)-1]+b[len(s)-1])**0.5
        else: 
            signif=999
            print "ERORRE, il numero di eventi di segnale:  ", str([len(s)-1]), "\t numero eventi di fondo: ", str(b[len(s)-1])
            OutFile.writelines(["ERORRE, il numero di eventi di segnale:  ", str(s[len(s)-1]), "\t numero eventi di fondo: ", str(b[len(s)-1]), "\n"])
        if b[len(s)-1]!=0: ratio = s[len(s)-1] / b[len(s)-1]
        else:
            ratio=999
            print "ERORRE, il numero di eventi di segnale:  ", s[len(s)-1], "\t numero eventi di fondo: ", b[len(s)-1]
            OutFile.writelines(["ERORRE, il numero di eventi di segnale:  ", str(s[len(s)-1]), "\t numero eventi di fondo: ", str(b[len(s)-1]), "\n"] )
        
        OutFile.writelines(["significance: ", str(signif), "\n"])
        
        print "significance: ", signif
        OutFile.writelines(["ratio:        ", str(ratio), "\n"])
        print "ratio:        ", ratio
        OutFile.write("\n \n")
        OutSignif.writelines(["significance: ", str(signif), "\n","ratio:        ", str(ratio), "\n"])
        print "\n \n"

OutFile.close()
