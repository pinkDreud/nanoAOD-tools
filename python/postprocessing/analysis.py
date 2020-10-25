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
chain.Add("/eos/user/m/mmagheri/SampleVBS_nanoAOD/WpWp_EWK_2017_nanoAOD_file_prova.root")
#chain.Add("/eos/user/m/mmagheri/SampleVBS_nanoAOD/TTTo2L2Nu_102X_prova.root")
#chain.Add("/eos/user/m/mmagheri/SampleVBS_nanoAOD/TTToSemileptonic_102X_prova.root")
#chain.Add("/eos/user/m/mmagheri/SampleVBS_nanoAOD/WJets2017_102X/WJets_1.root")
#chain.Add("/eos/user/m/mmagheri/SampleVBS_nanoAOD/WJets2017_102X/WJets_2.root")
#chain.Add("/eos/user/m/mmagheri/SampleVBS_nanoAOD/WJets2017_102X/WJets_3.root")

print("Number of events in chain " + str(chain.GetEntries()))
print("Number of events in tree from chain " + str((chain.GetTree()).GetEntries()))
print("Type of tree from chain " + str(type(chain.GetTree())))


tree = InputTree(chain)
print("Number of entries: " +str(tree.GetEntries()))
print("tree: ", tree)


Cut_dict = {1: ['Trigger             ', 0, 0.0, 0.0, 0.0, 0.0],
            2: ['Lepton selection    ', 0, 0.0, 0.0, 0.0, 0.0],
            3: ['Lepton Veto         ', 0, 0.0, 0.0, 0.0, 0.0],
            4: ['Tau selection       ', 0, 0.0, 0.0, 0.0, 0.0],
            5: ['Same charge tau lep ', 0, 0.0, 0.0, 0.0, 0.0],
            6: ['Jet Selection       ', 0, 0.0, 0.0, 0.0, 0.0],
            7: ['BVeto               ', 0, 0.0, 0.0, 0.0, 0.0],
            8: ['M_jj>500 GeV        ', 0, 0.0, 0.0, 0.0, 0.0],
            9: ['MET>40 GeV          ', 0, 0.0, 0.0, 0.0, 0.0],
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

    if i%10000==0: print("Processing event n. ---- "+str(i))

    
    #better trigger management?
    Trigger_SingleEle=HLT.Ele32_WPTight_Gsf_L1DoubleEG
    Trigger_SingleMu=HLT.IsoMu27
    
    Trigger=Trigger_SingleEle or Trigger_SingleMu
    
    SingleEle=False
    SingleMu=False
    MuEle=False

    if Trigger_SingleEle and not Trigger_SingleMu: SingleEle=True
    if Trigger_SingleMu and not Trigger_SingleEle: SingleMu=True
    if Trigger_SingleEle and Trigger_SingleMu: MuEle=True
    
    HighestLepPt=-999
    LeadLepFamily="not selected"

    if MuEle:
        for mu in muons:
            if mu.pt>HighestLepPt:
                HighestLepPt=mu.pt
        for ele in electrons:
            if ele.pt>HighestLepPt:
                SingleEle=True
                break
        if SingleEle==False and HighestLepPt>0: SingleMu=True


    if not Trigger: continue
    
    leptons=muons
    if SingleEle==True: leptons=electrons
    if SingleMu==True:  leptons=muons
    
    Cut_dict[1][1]+=1  

    #TODO cuts as lambda expression to have a much cleaner code

    #lepton selection -- only muons in this phase, just not to bother with double counting events
    if len(leptons)<1: continue
    indexGoodLep=SelectLepton(leptons, SingleMu)
    if indexGoodLep<0: continue

    GoodLep=leptons[indexGoodLep]
    Cut_dict[2][1]+=1  

    #veto on additional loosely isolated leptons
    if not LepVeto(GoodLep, electrons, muons): continue
    Cut_dict[3][1]+=1  
    
    #tau selection
    if len(taus)<1: continue
    UseDeepTau=True
    indexGoodTau=SelectTau(taus, GoodLep, UseDeepTau) #it takes as arguments the collection of taus, the selected muon and a boolean to decide if the reco happens with the MVA (false) or DeepTau (true)
    if indexGoodTau<0: continue
    GoodTau=taus[indexGoodTau]
    Cut_dict[4][1]+=1  
    
    #Same sign tau & lepton
    if not GoodTau.charge==GoodLep.charge: continue
    Cut_dict[5][1]+=1
    
    #jet selection
    if len(jets)<2: continue
    if jets[0].pt<PT_CUT_JET or abs(jets[0].eta)>ETA_CUT_JET: continue
    outputJetSel=JetSelection(list(jets), GoodTau, GoodLep)
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

for cutname, counts in Cut_dict.items():
    print round(counts[1], 4)



