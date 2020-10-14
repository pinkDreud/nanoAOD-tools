import os
import sys
import ROOT
print("Succesfully imported ROOT")
import math
import datetime
import copy
from array import array
from skimtree_utils import *

startTime = datetime.datetime.now()
print("Starting running at " + str(startTime))

ROOT.gROOT.SetBatch()

chain = ROOT.TChain('Events')
print(chain)
#chain.Add("/eos/user/m/mmagheri/SampleVBS_nanoAOD/WpWp_EWK_2017_nanoAOD_file_prova.root")
chain.Add("WpWpJJ_EWK_2017.root")

print("Number of events in chain " + str(chain.GetEntries()))
print("Number of events in tree from chain " + str((chain.GetTree()).GetEntries()))
print("Type of tree from chain " + str(type(chain.GetTree())))

pdg_dict = {'1': ['d', 0],
            '2': ['u', 0],
            '3': ['s', 0],
            '4': ['c', 0],
            '5': ['b', 0],
            '6': ['t', 0],
            '7': ["b'", 0],
            '8': ["t'", 0],
            '11': ["ele", 0],
            '12': ["nu_ele", 0],
            '13': ["mu", 0],
            '14': ["nu_mu", 0],
            '15': ["tau", 0],
            '16': ["nu_tau", 0],
            '17': ["tau'", 0],
            '18': ["nu_tau'", 0],
        }

W_dict = {
    '2': ['WW', 0],
    '3': ['WWW', 0],
}

tree = InputTree(chain)
print("Number of entries: " +str(tree.GetEntries()))
print("tree: ", tree)

lep = dict()
quark = dict()
d = dict()

for i in range(tree.GetEntries()):
   
    event = Event(tree,i)
    #electrons = Collection(event, "Electron")
    #muons = Collection(event, "Muon")
    #jets = Collection(event, "Jet")
    #taus = Collection(event, "Tau")
    #njets = len(jets)
    genparts = Collection(event, "GenPart")

    if i%1000==0: print("Processing event n. ---- "+str(i))

    w_count = 0
    
    for genp in genparts:
        if genp.genPartIdxMother > 0:
            if abs(genparts[genp.genPartIdxMother].pdgId) == 24:
                pdgid = str(abs(genp.pdgId))
                if abs(int(pdgid)) < 20:
                    pdg_dict[pdgid][1] += 1
        elif genp.genPartIdxMother == 0:
            if abs(genp.pdgId) == 24:
                w_count += 1
    
    W_dict[str(w_count)][1] += 1

print "\nFermions in which W decays"

for pdgid, counts in pdg_dict.items():
    if counts[1] != 0:
        print counts[0], "\tcountings: ", counts[1]

print "\nProcesses involved"

for wn, counts in W_dict.items():
    print counts[0], "\tcountings: ", counts[1]
