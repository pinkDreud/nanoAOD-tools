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
#chain.Add("/eos/user/m/mmagheri/SampleVBS_nanoAOD/WpWp_EWK_2017_nanoAOD_file_prova.root")
chain.Add("/eos/user/m/mmagheri/SampleVBS_nanoAOD/WpWp_EWK_2017_nanoAOD_file_prova.root")

print("Number of events in chain " + str(chain.GetEntries()))
print("Number of events in tree from chain " + str((chain.GetTree()).GetEntries()))
print("Type of tree from chain " + str(type(chain.GetTree())))


tree = InputTree(chain)
print("Number of entries: " +str(tree.GetEntries()))
print("tree: ", tree)


Cut_dict = {1: ['Trigger             ', 0, 0.0, 0.0],
            2: ['Lepton selection    ', 0, 0.0, 0.0],
            3: ['Lepton Veto         ', 0, 0.0, 0.0],
            4: ['Tau selection       ', 0, 0.0, 0.0],
            5: ['Same charge tau lep ', 0, 0.0, 0.0],
            6: ['Jet Selection       ', 0, 0.0, 0.0],
            7: ['BVeto               ', 0, 0.0, 0.0],
            8: ['M_jj>500 GeV        ', 0, 0.0, 0.0],
            9: ['MET>40 GeV          ', 0, 0.0, 0.0],
        }


nEntriesTotal=tree.GetEntries()

for i in range(tree.GetEntries()):
  
    event = Event(tree,i)
    electrons = Collection(event, "Electron")
    muons = Collection(event, "Muon")
    jets = Collection(event, "Jet")
    taus = Collection(event, "Tau")
    njets = len(jets)
    met = Object(event, "MET") 
    HLT = Object(event, "HLT")

    if i%5000==0: print("Processing event n. ---- "+str(i))

    #better trigger management?
    TRIGGER_SINGLEELE=HLT.Ele32_WPTight_Gsf_L1DoubleEG
    TRIGGER_SINGLEMU=HLT.IsoMu27
    TRIGGER=TRIGGER_SINGLEELE or TRIGGER_SINGLEMU
    
    if not TRIGGER: continue
    
    Cut_dict[1][1]+=1  

    #TODO cuts as lambda expression to have a much cleaner code

    #lepton selection -- only muons in this phase, just not to bother with double counting events
    
    if len(muons)<1: continue
    indexGoodMu=SelectMuon(muons)
    if indexGoodMu<0: continue

    GoodMu=muons[indexGoodMu]
    Cut_dict[2][1]+=1  

    #veto on additional loosely isolated leptons
    if not LepVeto(GoodMu, electrons, muons): continue
    Cut_dict[3][1]+=1  
    
    #tau selection
    if len(taus)<1: continue
    indexGoodTau=SelectTau(taus, GoodMu)
    if indexGoodTau<0: continue
    GoodTau=taus[indexGoodTau]
    Cut_dict[4][1]+=1  
    
    #Same sign tau & lepton
    if not GoodTau.charge==GoodMu.charge: continue
    Cut_dict[5][1]+=1
    
    #jet selection
    if len(jets)<2: continue
    if jets[0].pt<PT_CUT_JET or abs(jets[0].eta)>ETA_CUT_JET: continue
    outputJetSel=JetSelection(list(jets), GoodTau, GoodMu)
    if outputJetSel==-999: continue
    jet1, jet2=outputJetSel
    Cut_dict[6][1]+=1 
    
    #All the cuts up to here can be implemented in the online preselection, they're just cuts for the selection of final state objects, maybe we can shift the additional lepton veto here.

    #veto on events with b-tagged jets (mainly for ttbar discrimination)

    if BVeto(jets): continue
    Cut_dict[7][1]+=1  
    LeadJet=ROOT.TLorentzVector()
    SubleadJet=ROOT.TLorentzVector()
    LeadJet.SetPtEtaPhiM(jet1.pt, jet1.eta, jet1.phi, jet1.mass)
    SubleadJet.SetPtEtaPhiM(jet2.pt, jet2.eta, jet2.phi, jet2.mass) 
    
    
    #taglio massa invariante jet
    if JetCut(LeadJet, SubleadJet): continue
    Cut_dict[8][1]+=1  
    #taglio sulla met
    if metCut(met): continue
    Cut_dict[9][1]+=1  

for i in range(1,10):
    if i==1:
        Cut_dict[i][2]=Cut_dict[i][1]*1.0/nEntriesTotal
        Cut_dict[i][3]=Cut_dict[i][1]*1.0/nEntriesTotal
    else:
        Cut_dict[i][2]=Cut_dict[i][1]*1.0/Cut_dict[i-1][1]
        Cut_dict[i][3]=Cut_dict[i][1]*1.0/nEntriesTotal

for cutname, counts in Cut_dict.items():
    print counts[0], "\tcountings: ", round(counts[1], 4), "\teff. wrt. previous: ", round(counts[2], 4), "\teff wrt. total: ", round(counts[3], 4)
