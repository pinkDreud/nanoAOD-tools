from skimtree_utils import *
import ROOT
import os
import optparse
import sys
from samples.samples import *

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

for aut, wpconfs in wpset_dict.items():
    #carica autore e wp config
    for wpconf in wpconfs:
        #scrive la path a seconda di chi ha prodotto una certa wp config
        path = "/eos/user/" + aut + "/" + authors_dict[aut] + "/VBS/nosynch/Eff_Jet" + wpconf[0] + "_Mu" + wpconf[1] + "_Ele" + wpconf[2] + "/"

        #se non esiste, va avanti
        if not os.path.exists(path):
            continue

        #s = 0
        #b = 0

        #carica le cartelle dei sample
        dirlist = [dirs for dirs in os.listdir(path)]

        sample_dict
        
        for dirn in dirlist:
            #carica il _merged.root
            
            mergedfile = path + dirn + "/" + dirn + "_merged.root"

            count = 0

            #if "WpWpJJ_EWK" in mergedfile

            #carica il tree events_all
            chain = ROOT.TChain('events_all')
            chain.Add(mergedfile)

            print chain
            
            tree = InputTree(chain)
            print tree.GetEntries()
            
            for i in range(tree.GetEntries()):
                event = Event(tree,i)
                passed = Object(event, "pass")#cosi carico tutti i pass_* in unico object
                #print passed.lepton_selection# cosi ottengo pass_lepton_selection

        #signif = s / (s+b)**0.5
        #ratio = s / b

        
