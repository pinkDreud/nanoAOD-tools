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
#chain.Add("/eos/user/m/mmagheri/SampleVBS_nanoAOD/WpWp_EWK_2017_nanoAOD_file_prova.root")
chain.Add("/eos/user/m/mmagheri/SampleVBS_nanoAOD/WpWp_EWK_2017_nanoAOD_file_prova.root")

print("Number of events in chain " + str(chain.GetEntries()))
print("Number of events in tree from chain " + str((chain.GetTree()).GetEntries()))
print("Type of tree from chain " + str(type(chain.GetTree())))


tree = InputTree(chain)
print("Number of entries: " +str(tree.GetEntries()))
print("tree: ", tree)

cut=[0 for i in range(9)]
badTau=0

for i in range(tree.GetEntries()):
    
    event = Event(tree,i)
    electrons = Collection(event, "Electron")
    muons = Collection(event, "Muon")
    jets = Collection(event, "Jet")
    taus = Collection(event, "Tau")
    njets = len(jets)
    met = Object(event, "MET")
     
    HLT = Object(event, "HLT") #per ora provo il codice solo nel canale con i muoni
    
    if i%1000==0: print("Processing event n. ---- "+str(i))
    
    #trigger
    if not (HLT.IsoMu27 or HLT.Ele32_WPTight_Gsf_L1DoubleEG): continue
    
    cut[0]+=1
    #reinserisci tagli con espressioni lambda
    #controlla lunghezza lista
    #prendi primo el. lista


    #selezione leptoni
    if len(muons)<1: continue
    indexGoodMu=SelectMuon(muons)
    if indexGoodMu<0: continue
    GoodMu=muons[indexGoodMu]
    cut[1]+=1

    #veto su leptoni poco isolati addizionali
    if not LepVeto(GoodMu, electrons, muons): continue
    cut[2]+=1
    #selezione tau
    if len(taus)<1: continue
    indexGoodTau=SelectTau(taus, GoodMu)
    if indexGoodTau<0: continue
    GoodTau=taus[indexGoodTau]
   
    cut[3]+=1
    
    #leptone e tau dello stesso segno
    if not GoodTau.charge==GoodMu.charge: continue
    cut[4]+=1
    #due jet da segnatura VBS
    #prova lista con funzione ricorsiva per scegliere i jet
    if len(jets)<2: continue
    if jets[0].pt<30: continue
    outputJetSel=JetSelection(list(jets), GoodTau, GoodMu)
    if outputJetSel==-999: continue
    jet1, jet2=outputJetSel
    cut[5]+=1
    #fin qui tutti i tagli applicati si possono implementare nella preselezione, solo selezione degli oggetti nello stato finale

    #bveto
    if BVeto(jets): continue
    cut[6]+=1
    LeadJet=ROOT.TLorentzVector()
    SubleadJet=ROOT.TLorentzVector()
    LeadJet.SetPtEtaPhiM(jet1.pt, jet1.eta, jet1.phi, jet1.mass)
    SubleadJet.SetPtEtaPhiM(jet2.pt, jet2.eta, jet2.phi, jet2.mass) 
    #taglio massa invariante jet
    if JetCut(LeadJet, SubleadJet): continue
    cut[7]+=1
    #taglio sulla met
    if metCut(met): continue
    cut[8]+=1

print("il numero di tau coincidenti con mu is"+ str(badTau))

print("numero di eventi selezionati: ")
for i in range (0,9):
    efficienza=0.0
    if i==0: efficienza=cut[i]*1.0/tree.GetEntries()
    else: efficienza=cut[i]*1.0/cut[i-1]
    print("taglio: " + str(i)+ " # eventi: "+ str(cut[i]) + " efficienza del taglio: "+ str(efficienza))

