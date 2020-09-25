#!/bin/env python3
import os
#print(os.environ)
#print("**********************************************************************")
#print("**********************************************************************")
#print("**********************************************************************")
#print(str(os.environ.get('PYTHONPATH')))
#print(str(os.environ.get('PYTHON3PATH')))
import sys
#print("*************** This is system version info ***************************")
#print(sys.version_info)
#import platform
#print("*************** This is python version info ***************************")
#print(platform.python_version())
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
chain.Add("/eos/user/m/mmagheri/SampleVBS_nanoAOD/nanoAOD-tools/WpWp_EWK_2017_nanoAOD_file_prova.root")

print("Number of events in chain " + str(chain.GetEntries()))
print("Number of events in tree from chain " + str((chain.GetTree()).GetEntries()))
print("Type of tree from chain " + str(type(chain.GetTree())))


tree = InputTree(chain)
print("Number of entries: " +str(tree.GetEntries()))
print("tree: ", tree)


for i in range(tree.GetEntries()):
    
    event = Event(tree,i)
    electrons = Collection(event, "Electron")
    muons = Collection(event, "Muon")
    jets = Collection(event, "Jet")
    taus = Collection(event, "Tau")
    njets = len(jets)
    
    HLT = Object(event, "HLT.IsoMu27") #per ora provo il codice solo nel canale con i muoni
    
    if i%1000==0: print("Processing event n. ---- "+str(i))
    
    #trigger
    if not HLT: continue
    
    #selezione leptoni
    if len(muons)<1: continue
    indexGoodMu=SelectMuon(muons)
    GoodMu=muons[indexGoodMu]
    if indexGoodMu<0: continue
    
    #veto su leptoni poco isolati addizionali
    if not LepVeto(GoodMu, electrons, muons): continue

    #selezione tau
    if len(taus)<1: continue
    indexGoodTau=SelectTau(taus)
    if indexGoodTau<0: continue
    GoodTau=taus[indexGoodTau]
 
    #leptone e tau dello stesso segno
    if not GoodTau.charge==GoodMu.charge: continue

    #due jet da segnatura VBS
    if len(jets)<2: continue
    if jets[0].pt<30: continue
    indexSecondJet=FindSecondJet(jets[0], jets)
    if indexSecondJet<0: continue 
    LeadJet.SetPtEtaPhiM(jets[0].pt, jets[0].eta, jets[0].phi, jets[0].mass)
    print(LeadJet.Pt())
    #fin qui tutti i tagli applicati si possono implementare nella preselezione, solo selezione degli oggetti nello stato finale

    #bveto
    if BVeto(jets): continue

    #taglio massa invariante jet
      

















