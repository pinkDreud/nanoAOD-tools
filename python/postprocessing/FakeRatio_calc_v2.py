import os, commands
import sys
import optparse
import ROOT
import math
from datetime import date

from FakeRatio_utils import *
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *



MET_cut=40
mt_lepMET_cut=40
evs=0

usage = 'python FakeRatio_calc_v2.py -b -o --promptFakeTau'
parser = optparse.OptionParser(usage)
parser.add_option('-f', '--folder', dest='folder', type=str, default = '', help='Please enter a destination folder')
parser.add_option('-b', '--bkg', dest='bkg', default = False,action='store_true', help='Eliminate contribution from W+Jets && DY+Jets, default false')
parser.add_option('-o', '--onlybkg', dest='onlybkg', default = False,action='store_true', help='Only MC contribution, default false')
parser.add_option('-d', '--debug', dest='debug', default = False, action='store_true', help='Debug mode, only runs in a file')
parser.add_option('--promptFakeTau', dest='promptFakeTau', default = False,action='store_true', help='Only MC contribution, default false')

parser.add_option('--input', dest='infolder', type=str, default = 'FR_v8/HT', help='Please enter an input folder folder')
(opt, args) = parser.parse_args()
input_folder="/eos/user/m/mmagheri/VBS/nosynch/"+opt.infolder+"/"

bkg_files= ["DYJetsToLL_2017/DYJetsToLL_2017.root", "WJets_2017/WJets_2017.root"]

Fake_dicti_ele = {
            '1A': ['|n|<1,     pT<20    ',  0,  0, 0.0],
            '1B': ['1<|n|<1.5, pT<20    ',  0,  0, 0.0],
            '1C': ['1.5<|n|<2, pT<20    ',  0,  0, 0.0],
            '1D': ['2<|n|<2.4, pT<20    ',  0,  0, 0.0],
            '2A': ['|n|<1,     20<pT<30 ',  0,  0, 0.0],
            '2B': ['1<|n|<1.5, 20<pT<30 ',  0,  0, 0.0],
            '2C': ['1.5<|n|<2, 20<pT<30 ',  0,  0, 0.0],
            '2D': ['2<|n|<2.4, 20<pT<30 ',  0,  0, 0.0],
            '3A': ['|n|<1,     30<pT<40 ',  0,  0, 0.0],
            '3B': ['1<|n|<1.5, 30<pT<40 ',  0,  0, 0.0],
            '3C': ['1.5<|n|<2, 30<pT<40 ',  0,  0, 0.0],
            '3D': ['2<|n|<2.4, 30<pT<40 ',  0,  0, 0.0],
            '4A': ['|n|<1,     40<pT<50 ',  0,  0, 0.0],
            '4B': ['1<|n|<1.5, 40<pT<50 ',  0,  0, 0.0],
            '4C': ['1.5<|n|<2, 40<pT<50 ',  0,  0, 0.0],
            '4D': ['2<|n|<2.4, 40<pT<50 ',  0,  0, 0.0],
            '5A': ['|n|<1,     pT>50    ',  0,  0, 0.0],
            '5B': ['1<|n|<1.5, pT>50    ',  0,  0, 0.0],
            '5C': ['1.5<|n|<2, pT>50    ',  0,  0, 0.0],
            '5D': ['2<|n|<2.4, pT>50    ',  0,  0, 0.0],
}


Fake_dicti_mu = {
            '1A': ['|n|<1,     pT<20    ',  0,  0, 0.0],
            '1B': ['1<|n|<1.5, pT<20    ',  0,  0, 0.0],
            '1C': ['1.5<|n|<2, pT<20    ',  0,  0, 0.0],
            '1D': ['2<|n|<2.4, pT<20    ',  0,  0, 0.0],
            '2A': ['|n|<1,     20<pT<30 ',  0,  0, 0.0],
            '2B': ['1<|n|<1.5, 20<pT<30 ',  0,  0, 0.0],
            '2C': ['1.5<|n|<2, 20<pT<30 ',  0,  0, 0.0],
            '2D': ['2<|n|<2.4, 20<pT<30 ',  0,  0, 0.0],
            '3A': ['|n|<1,     30<pT<40 ',  0,  0, 0.0],
            '3B': ['1<|n|<1.5, 30<pT<40 ',  0,  0, 0.0],
            '3C': ['1.5<|n|<2, 30<pT<40 ',  0,  0, 0.0],
            '3D': ['2<|n|<2.4, 30<pT<40 ',  0,  0, 0.0],
            '4A': ['|n|<1,     40<pT<50 ',  0,  0, 0.0],
            '4B': ['1<|n|<1.5, 40<pT<50 ',  0,  0, 0.0],
            '4C': ['1.5<|n|<2, 40<pT<50 ',  0,  0, 0.0],
            '4D': ['2<|n|<2.4, 40<pT<50 ',  0,  0, 0.0],
            '5A': ['|n|<1,     pT>50    ',  0,  0, 0.0],
            '5B': ['1<|n|<1.5, pT>50    ',  0,  0, 0.0],
            '5C': ['1.5<|n|<2, pT>50    ',  0,  0, 0.0],
            '5D': ['2<|n|<2.4, pT>50    ',  0,  0, 0.0],
}


Fake_dicti_tau = {
            '1A': ['|n|<1,     pT<20    ',  0,  0, 0.0],
            '1B': ['1<|n|<1.5, pT<20    ',  0,  0, 0.0],
            '1C': ['1.5<|n|<2, pT<20    ',  0,  0, 0.0],
            '1D': ['2<|n|<2.4, pT<20    ',  0,  0, 0.0],
            '2A': ['|n|<1,     20<pT<30 ',  0,  0, 0.0],
            '2B': ['1<|n|<1.5, 20<pT<30 ',  0,  0, 0.0],
            '2C': ['1.5<|n|<2, 20<pT<30 ',  0,  0, 0.0],
            '2D': ['2<|n|<2.4, 20<pT<30 ',  0,  0, 0.0],
            '3A': ['|n|<1,     30<pT<40 ',  0,  0, 0.0],
            '3B': ['1<|n|<1.5, 30<pT<40 ',  0,  0, 0.0],
            '3C': ['1.5<|n|<2, 30<pT<40 ',  0,  0, 0.0],
            '3D': ['2<|n|<2.4, 30<pT<40 ',  0,  0, 0.0],
            '4A': ['|n|<1,     40<pT<50 ',  0,  0, 0.0],
            '4B': ['1<|n|<1.5, 40<pT<50 ',  0,  0, 0.0],
            '4C': ['1.5<|n|<2, 40<pT<50 ',  0,  0, 0.0],
            '4D': ['2<|n|<2.4, 40<pT<50 ',  0,  0, 0.0],
            '5A': ['|n|<1,     pT>50    ',  0,  0, 0.0],
            '5B': ['1<|n|<1.5, pT>50    ',  0,  0, 0.0],
            '5C': ['1.5<|n|<2, pT>50    ',  0,  0, 0.0],
            '5D': ['2<|n|<2.4, pT>50    ',  0,  0, 0.0],
}
today = date.today()


if evs<10: numberOfEvs="all"
filename="FakeRatio_calcs/FakeRatios"+opt.infolder+"_MetCUT_"+str(MET_cut)+"_mTLepMetCUT_"+str(mt_lepMET_cut)+"_nEv_"+numberOfEvs+"_"+str(today)
if(opt.bkg): filename="FakeRatio_calcs/FakeRatios_MetCUT_"+str(MET_cut)+"_mTLepMetCUT_"+str(mt_lepMET_cut)+"_removeBKG"+"_"+str(today)
if opt.onlybkg: filename+="_onlyBKG"

print("saving events in: ", filename)


def FakeCalc(sample, isData, nev):
    print "sample: ", sample
    isMC=not isData
    if not os.path.exists(sample): 
        print "path doesn't exist"
        return 0
    print "\n"
    chain = ROOT.TChain('events_all')
    chain.Add(sample)
    print (chain)
    tree = InputTree(chain)
    
    sign=1
    if isMC: sign=-1
    if nev<10: nev=tree.GetEntries()

    for i in range(nev):
        if i%1000000==0: print "Processing event: ",i+1 
        
        event           =   Event(tree,i)
        isFake          =   Object(event, "isFake")

        FakeLepton      =   Object(event, "FakeLepton")
        FakeTau         =   Object(event, "FakeTau")
        
        Met             =   Object(event, "MET_pt")
        mT              =   Object(event, "mT_lepMET")
        w               =   Object(event, "w")
        veto            =   Object(event, "Veto")
        
        SF=1
        if isMC: SF=w.nominal*sign*event.PFSF*event.puSF*0.17/41.53 #last two numbers are to scale to the lumi of PFHT350

        if Met>MET_cut or mT>mt_lepMET_cut: continue
        
        isMC_and_haspromptLepton = isMC and FakeLepton.isPrompt==1 and isFake.lepton==1
        isMC_and_haspromptTau=False
        if opt.promptFakeTau: 
            isMC_and_haspromptTau=isMC and FakeTau.isPrompt==5 and isFake.tau==1 and opt.promptFakeTau

        if isMC_and_haspromptLepton and isMC_and_haspromptTau:
            isMC_and_hasprompTau=False

        pTbin = 0
        etaBin = 0
        pos = 0
        
        if isMC_and_haspromptLepton or isData:    
            if veto.LightLeptons==1: continue
            if abs(FakeLepton.eta)<2.4:
                pTbin =  pTCalculator(FakeLepton.pt)
                etaBin = etaCalculator(FakeLepton.eta)
                pos =    str(pTbin)+etaBin
                
                if isMC and not(FakeLepton.isPrompt==1): SF=0
            
                if abs(FakeLepton.pdgid)==11:
                    Fake_dicti_ele[pos][1]+=SF
                    if FakeLepton.pfRelIso04<0.08:
                        Fake_dicti_ele[pos][2]+=SF
                
                if abs(FakeLepton.pdgid)==13:
                    Fake_dicti_mu[pos][1]+=SF
                    if FakeLepton.pfRelIso04<0.15:
                        Fake_dicti_mu[pos][2]+=SF
        
        if isMC_and_haspromptTau or isData:
            if veto.TauLeptons==1: continue
            if abs(FakeTau.eta)<2.4:
                pTbin=  pTCalculator(FakeTau.pt)
                etaBin= etaCalculator(FakeTau.eta)

                if isMC and not(FakeTau.isPrompt==5): SF=0
                
                pos =    str(pTbin)+etaBin
                        
                Fake_dicti_tau[pos][1]+=SF
                if isFake.tauAndPassCuts==1:#FakeTau.DeepTauWP>=64: #isFake.tauAndPassCuts==1:
                    Fake_dicti_tau[pos][2]+=SF



if not opt.debug:
    dataSample="/eos/user/m/mmagheri/VBS/nosynch/FR_v8/HT/DataHT_2017/DataHT_2017.root"
    print("working on data sample: ", dataSample)
    FakeCalc(dataSample,True, evs)
    if opt.bkg or opt.onlybkg:
        for bkg in bkg_files:
            FakeCalc(input_folder+bkg, False, evs)

    print("Electrons")
    for pos in Fake_dicti_ele:
        Fake_dicti_ele[pos][3]=Fake_dicti_ele[pos][2]*1.0/Fake_dicti_ele[pos][1]
        print pos, Fake_dicti_ele[pos][0], ": nTot ", Fake_dicti_ele[pos][1], " nGood ", Fake_dicti_ele[pos][2], " FR: ", Fake_dicti_ele[pos][3]

    print("Muons:")
    for pos in Fake_dicti_mu:
        Fake_dicti_mu[pos][3]=Fake_dicti_mu[pos][2]*1.0/Fake_dicti_mu[pos][1]
        print pos, Fake_dicti_mu[pos][0], ": nTot ", Fake_dicti_mu[pos][1], " nGood ", Fake_dicti_mu[pos][2], " FR: ", Fake_dicti_mu[pos][3]

    if not(opt.onlybkg) or opt.promptFakeTau:
        print("Taus:")
        for pos in Fake_dicti_tau:
            Fake_dicti_tau[pos][3]=Fake_dicti_tau[pos][2]*1.0/Fake_dicti_tau[pos][1]
            print pos, Fake_dicti_tau[pos][0], ": nTot ", Fake_dicti_tau[pos][1], " nGood ", Fake_dicti_tau[pos][2], " FR: ", Fake_dicti_tau[pos][3]

    numberOfEvs=str(evs)
    if evs<10: numberOfEvs="all"
    filename="FakeRatio_calcs/FakeRatios"+opt.infolder+"_MetCUT_"+str(MET_cut)+"_mTLepMetCUT_"+str(mt_lepMET_cut)+"_nEv_"+numberOfEvs+"_"+str(today)
    if(opt.bkg): filename="FakeRatio_calcs/FakeRatios_MetCUT_"+str(MET_cut)+"_mTLepMetCUT_"+str(mt_lepMET_cut)+"_removeBKG"+"_"+str(today)
    if opt.onlybkg: filename+="_onlyBKG"

    outFile=open(filename+".txt", "w")

    outFile.write("Electrons \n")
    for pos in Fake_dicti_ele:
        L=[str(Fake_dicti_ele[pos][0]), "\t : nTot \t", str(Fake_dicti_ele[pos][1]), "\t nGood \t", str(Fake_dicti_ele[pos][2]), "\t FR:\t ", str(Fake_dicti_ele[pos][3]), "\n"]
        outFile.writelines(L)

    outFile.write("Muons \n")
    for pos in Fake_dicti_mu:
        L=[str(Fake_dicti_mu[pos][0]), "\t : nTot \t", str(Fake_dicti_mu[pos][1]), "\t nGood \t", str(Fake_dicti_mu[pos][2]), "\t FR:\t ", str(Fake_dicti_mu[pos][3]), "\n"]
    outFile.writelines(L)

    if not(opt.onlybkg) or opt.promptFakeTau:
        print("Taus:")
 
        outFile.write("Tau \n")
        for pos in Fake_dicti_tau:
            L=[str(Fake_dicti_tau[pos][0]), "\t : nTot \t", str(Fake_dicti_tau[pos][1]), "\t nGood \t", str(Fake_dicti_tau[pos][2]), "\t FR:\t ", str(Fake_dicti_tau[pos][3]), "\n"]
            outFile.writelines(L)


    outFile.close()

else:
    littleSample="/eos/user/m/mmagheri/VBS/nosynch/FR_v8/HT/DataHTB_2017/DataHTB_2017.root"
    print("working on little sample:", littleSample)
    FakeCalc(littleSample, True, 1000000)

    print("Electrons")
    for pos in Fake_dicti_ele:
        Fake_dicti_ele[pos][3]=Fake_dicti_ele[pos][2]*1.0/Fake_dicti_ele[pos][1]
        print pos, Fake_dicti_ele[pos][0], ": nTot ", Fake_dicti_ele[pos][1], " nGood ", Fake_dicti_ele[pos][2], " FR: ", Fake_dicti_ele[pos][3]

    print("Muons:")
    for pos in Fake_dicti_mu:
        Fake_dicti_mu[pos][3]=Fake_dicti_mu[pos][2]*1.0/Fake_dicti_mu[pos][1]
        print pos, Fake_dicti_mu[pos][0], ": nTot ", Fake_dicti_mu[pos][1], " nGood ", Fake_dicti_mu[pos][2], " FR: ", Fake_dicti_mu[pos][3]

    if not(opt.onlybkg) or opt.promptFakeTau:
        print("Taus:")
        for pos in Fake_dicti_tau:
            Fake_dicti_tau[pos][3]=Fake_dicti_tau[pos][2]*1.0/Fake_dicti_tau[pos][1]
            print pos, Fake_dicti_tau[pos][0], ": nTot ", Fake_dicti_tau[pos][1], " nGood ", Fake_dicti_tau[pos][2], " FR: ", Fake_dicti_tau[pos][3]





