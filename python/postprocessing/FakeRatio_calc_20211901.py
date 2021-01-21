import os, commands
import sys
import optparse
import math
from datetime import date
from ROOT import TH2F
from FakeRatio_utils import *
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *


MET_cut=30
mt_lepMET_cut=20
evs=0

usage = 'python FakeRatio_calc_20211901.py -b --promptFakeTau --met 50 --mt 50 --input FR_11/Ele -t Ele'
parser = optparse.OptionParser(usage)
parser.add_option('--met', dest='met_cut', type=int, default = '30', help='insert met cut, default 30')
parser.add_option('--mt', dest='mt_lepMET_cut', type=int, default = '20', help='insert met cut, default 20')
parser.add_option('-b', '--bkg', dest='bkg', default = False,action='store_true', help='Eliminate contribution from W+Jets && DY+Jets, default false')
parser.add_option('-o', '--onlybkg', dest='onlybkg', default = False,action='store_true', help='Only MC contribution, default false')
parser.add_option('-d', '--debug', dest='debug', default = False, action='store_true', help='Debug mode, only runs in a file')
parser.add_option('-t', '--trig', dest='trig', type=str, default = 'all', help='trigger used')
parser.add_option('--promptFakeTau', dest='promptFakeTau', default = False,action='store_true', help='Only MC contribution, default false')

parser.add_option('--input', dest='infolder', type=str, default = 'FR_v10/Ele', help='Please enter an input folder folder')
(opt, args) = parser.parse_args()


input_folder="/eos/user/m/mmagheri/VBS/nosynch/"+opt.infolder+"/"



print("Processing event with met cut: ", opt.met_cut, " and mt_lepMET cut: ", opt.mt_lepMET_cut)
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
filename="FakeRatio_calcs/v11/"+str(opt.trig)+"/FakeRatios_MetCUT_"+str(opt.met_cut)+"_mTLepMetCUT_"+str(opt.mt_lepMET_cut)+"_nEv_"+numberOfEvs+"_"+str(today)
if(opt.bkg): filename="FakeRatio_calcs/v11/"+str(opt.trig)+"/FakeRatios_MetCUT_"+str(opt.met_cut)+"_mTLepMetCUT_"+str(opt.mt_lepMET_cut)+"_removeBKG"+"_"+str(today)
if opt.onlybkg: filename+="_onlyBKG"


print("saving events in: ", filename)

f = ROOT.TFile(filename+".root", "RECREATE")

f.cd()
filename+=".txt"

lower_pt = [0, 20, 30, 40, 50, 60]
lower_eta = [0, 1, 1.4, 2, 2.4]


taele = ROOT.TH2F()

#hFRDataeledif = ROOT.TH2F("h2FRDataeledif", "Electron Data fake ratio", 5, array.array('d', lower_pt), 4, array.array('d', lower_eta))
#hFRDatamudif  = ROOT.TH2F("h2FRDatamudif",  "Muon Data fake ratio",     5, array.array('d', lower_pt), 4, array.array('d', lower_eta))
#hFRDatataudif = ROOT.TH2F("h2FRDatataudif", "Tau Data fake ratio",      5, array.array('d', lower_pt), 4, array.array('d', lower_eta))

hFRDataeledif = None
hFRDatamudif = None
hFRDatataudif = None

FRdiflist = [hFRDataeledif, hFRDatamudif, hFRDatataudif]
FRdifname = ["hFRDataeledif", "hFRDatamudif", "hFRDatataudif"]
FRdiftitle = ["Electron Data-MC fake ratio", "Muon Data-MC fake ratio", "Tau Data-MC fake ratio"]

#hFRDataele = ROOT.TH2F("h2FRDataele", "Electron Data fake ratio", 5, array.array('d', lower_pt), 4, array.array('d', lower_eta))
#hFRDatamu  = ROOT.TH2F("h2FRDatamu",  "Muon Data fake ratio",     5, array.array('d', lower_pt), 4, array.array('d', lower_eta))
#hFRDatatau = ROOT.TH2F("h2FRDatatau", "Tau Data fake ratio",      5, array.array('d', lower_pt), 4, array.array('d', lower_eta))

hFRDataele = None
hFRDatamu = None
hFRDatatau = None

FRDatalist  =   [hFRDataele, hFRDatamu, hFRDatatau]
FRDataname =   ["hFRDataele", "hFRDatamu", "hFRDatatau"]
FRDatatitle = ["Electron Data fake ratio", "Muon Data fake ratio", "Tau Data fake ratio"]

#hFRMCele = ROOT.TH2F("h2FRMCele", "Electron MC fake ratio", 5, array.array('d', lower_pt), 4, array.array('d', lower_eta))
#hFRMCmu  = ROOT.TH2F("h2FRMCmu",  "Muon MC fake ratio",     5, array.array('d', lower_pt), 4, array.array('d', lower_eta))
#hFRMCtau = ROOT.TH2F("h2FRMCtau", "Tau MC fake ratio",      5, array.array('d', lower_pt), 4, array.array('d', lower_eta))

hFRMCele = None
hFRMCmu = None
hFRMCtau = None 

FRMClist  = [hFRMCele, hFRMCmu, hFRMCtau]
FRMCname = ["hFRMCele", "hFRMCmu", "hFRMCtau"]
FRMCtitle = ["Electron MC fake ratio", "Muon MC fake ratio", "Tau MC fake ratio"]

hNLooseEle_Data = ROOT.TH2F("h2NLooseEle_data", "Electron #loose events", 5, array.array('d', lower_pt), 4, array.array('d', lower_eta))
hNLooseMu_Data  = ROOT.TH2F("h2NLooseMu_data",  "Muon #loose events",     5, array.array('d', lower_pt), 4, array.array('d', lower_eta))
hNLooseTau_Data = ROOT.TH2F("h2NLooseTau_data", "Tau #loose events",      5, array.array('d', lower_pt), 4, array.array('d', lower_eta))

looseDatalist = [hNLooseEle_Data, hNLooseMu_Data, hNLooseTau_Data]

hNTightEle_Data = ROOT.TH2F("h2NTightEle_data", "Electron #tight events", 5, array.array('d', lower_pt), 4, array.array('d', lower_eta))
hNTightMu_Data  = ROOT.TH2F("h2NTightMu_data",  "Muon #tight events",     5, array.array('d', lower_pt), 4, array.array('d', lower_eta))
hNTightTau_Data = ROOT.TH2F("h2NTightTau_data", "Tau #tight events",      5, array.array('d', lower_pt), 4, array.array('d', lower_eta))

tightDatalist = [hNTightEle_Data, hNTightMu_Data, hNTightTau_Data] 

hNLooseEle_MC = ROOT.TH2F("h2NLooseEle_MC", "Electron #loose events", 5, array.array('d', lower_pt), 4, array.array('d', lower_eta))
hNLooseMu_MC  = ROOT.TH2F("h2NLooseMu_MC",  "Muon #loose events",     5, array.array('d', lower_pt), 4, array.array('d', lower_eta))
hNLooseTau_MC = ROOT.TH2F("h2NLooseTau_MC", "Tau #loose events",      5, array.array('d', lower_pt), 4, array.array('d', lower_eta))

looseMClist = [hNLooseEle_MC, hNLooseMu_MC, hNLooseTau_MC]

hNTightEle_MC = ROOT.TH2F("h2NTightEle_MC", "Electron #tight events", 5, array.array('d', lower_pt), 4, array.array('d', lower_eta))
hNTightMu_MC  = ROOT.TH2F("h2NTightMu_MC",  "Muon #tight events",     5, array.array('d', lower_pt), 4, array.array('d', lower_eta))
hNTightTau_MC = ROOT.TH2F("h2NTightTau_MC", "Tau #tight events",      5, array.array('d', lower_pt), 4, array.array('d', lower_eta))

tightMClist = [hNTightEle_MC, hNTightMu_MC, hNTightTau_MC]

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
    if opt.onlybkg: sign=1
    if nev<10: nev=tree.GetEntries()
    contaEle=1
    contaMu=1
    contaTau=1
    for i in range(nev):

        if (nev-i)<=10:
            print("saving the last event #", i+1)
            dict_save(Fake_dicti_ele, Fake_dicti_mu, Fake_dicti_tau, filename)
        
        event           =   Event(tree,i)
        isFake          =   Object(event, "isFake")

        FakeLepton      =   Object(event, "FakeLepton")
        FakeTau         =   Object(event, "FakeTau")
        
        FakeElectron    =   Object(event, "FakeElectron")
        FakeMuon        =   Object(event, "FakeMuon")

        Met             =   Object(event, "MET")
        mT              =   Object(event, "mT")
        w               =   Object(event, "w")
        veto            =   Object(event, "Veto")

        if (i==0):
            print("saving events  ", i+1)
            dict_save(Fake_dicti_ele, Fake_dicti_mu, Fake_dicti_tau, filename)

        if(i%1000000==0): print("processing event ----- ", i, "\t \%: ", i*1.0/nev*100)

        SF=1
        
        if isMC: SF=w.nominal*sign*event.PFSF*event.puSF #last two numbers are to scale to the lumi of PFHT350
        if Met.pt>opt.met_cut or abs(mT.lepMET)>opt.mt_lepMET_cut: continue
        
        '''
        print "Processing event ------ ",i
        print("Met cut is : ", MET_cut,       " Met is : ", Met.pt)
        print("mt cut is  : ", mt_lepMET_cut, " Mt is  : ", mT.lepMET)
        print("event has passed", "\n\n")
        '''
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
            if abs(FakeLepton.eta)<2.4 and not (abs(FakeLepton.eta)>1.4442 and abs(FakeLepton.eta)<1.566):
                pTbin =  pTCalculator(FakeLepton.pt)
                etaBin, netaBin = etaCalculator(FakeLepton.eta)
                pos =    str(pTbin)+etaBin
                
                if isMC and not(FakeLepton.isPrompt==1): SF=0
            
                if abs(FakeLepton.pdgid)==11 and not(opt.trig=='HT' or opt.trig=='Mu'):
                    
                    contaEle+=1
                    Fake_dicti_ele[pos][1]+=SF
                    #print(isData)                    
                    if isData:  hNLooseEle_Data.Fill(FakeLepton.pt, abs(FakeLepton.eta), SF)
                    else:       hNLooseEle_MC.Fill(FakeLepton.pt, abs(FakeLepton.eta), -SF)
                    #print "eta : ", abs(FakeLepton.eta)
                    #print "pt : ", FakeLepton.pt
                    #print Fake_dicti_ele[pos][1], hNLooseEle_Data.GetBinContent(pTbin, netaBin), Fake_dicti_ele[pos][1]==hNLooseEle_Data.GetBinContent(pTbin, netaBin)


                    if FakeLepton.pfRelIso04<0.08 and FakeElectron.WP90==1:
                        if isData:  hNTightEle_Data.Fill(FakeLepton.pt, abs(FakeLepton.eta), SF)
                        else:       hNTightEle_MC.Fill(FakeLepton.pt, abs(FakeLepton.eta), -SF)
                        Fake_dicti_ele[pos][2]+=SF
                
                if abs(FakeLepton.pdgid)==13 and not(opt.trig=='HT' or opt.trig=='Ele'):
                    contaMu+=1
                    #print("Mu in teh loop ", contaMu)
                    Fake_dicti_mu[pos][1]+=SF
                    if isData:  hNLooseMu_Data.Fill(FakeLepton.pt, abs(FakeLepton.eta), SF)
                    else:       hNLooseMu_MC.Fill(FakeLepton.pt, abs(FakeLepton.eta), -SF)

                    if FakeLepton.pfRelIso04<0.15 and FakeMuon.TightId==1:
                        if isData:  hNTightMu_Data.Fill(FakeLepton.pt, abs(FakeLepton.eta), SF)
                        else:       hNTightMu_MC.Fill(FakeLepton.pt, abs(FakeLepton.eta), -SF)
                        Fake_dicti_mu[pos][2]+=SF
        
        #print("Mu outside teh loop ", contaMu)
        if isMC_and_haspromptTau or isData and not(opt.trig=='Ele' or opt.trig=='Mu'):
            if veto.TauLeptons==1: continue
            if abs(FakeTau.eta)<2.4 and not (abs(FakeTau.eta)>1.4442 and abs(FakeTau.eta)<1.566):
                contaTau+=1
                pTbin=  pTCalculator(FakeTau.pt)
                etaBin, netaBin= etaCalculator(FakeTau.eta)

                if isMC and not(FakeTau.isPrompt==5): SF=0
                
                pos =    str(pTbin)+etaBin
                        
                if isData:  hNLooseTau_Data.Fill(FakeTau.pt, abs(FakeTau.eta))
                else:       hNLooseTau_MC.Fill(FakeTau.pt, abs(FakeTau.eta), -SF) 
                
                
                Fake_dicti_tau[pos][1]+=SF
                if isFake.tauAndPassCuts==1:#FakeTau.DeepTauWP>=64: #isFake.tauAndPassCuts==1:
                    if isData:  hNTightTau_Data.Fill(FakeTau.pt, abs(FakeTau.eta), SF)
                    else:       hNTightTau_MC.Fill(FakeTau.pt, abs(FakeTau.eta), -SF)
                    Fake_dicti_tau[pos][2]+=SF
        
        
        
        if(contaEle%10000==0 or contaMu%100000==0 or contaTau%100000==0):
            if(opt.trig=='all' or opt.trig == 'Ele'):
                print("Electrons, nGood: ", contaEle)
                dict_print(Fake_dicti_ele)
                contaEle+=1
            if (opt.trig=='all' or opt.trig=='Mu'):
                print("Muons, nGood:     ", contaMu)
                dict_print(Fake_dicti_mu)
            if (opt.trig=='all' or opt.trig=='HT'):
                print("Tau, nGood        ", contaTau)
                dict_print(Fake_dicti_tau)

        if(contaEle%10000==0 or contaMu%10000==0 or contaTau%10000==0):
            print("saving events  ", i)
            dict_save(Fake_dicti_ele, Fake_dicti_mu, Fake_dicti_tau, filename)
        
        if (nev-i)<10:
            print("saving the last event #", i+1)
            dict_save(Fake_dicti_ele, Fake_dicti_mu, Fake_dicti_tau, filename)

        if(i==nev):
            print("saving events ", i)
            print("Electrons, nGood: ", contaEle)
            dict_print(Fake_dicti_ele)
            print("Muons, nGood:     ", contaMu)
            dict_print(Fake_dicti_mu)
            print("Tau, nGood        ", contaTau)
            dict_print(Fake_dicti_tau)
            dict_save(Fake_dicti_ele, Fake_dicti_mu, Fake_dicti_tau, filename)



DataToRun = None
if 'Ele' in input_folder: DataToRun = "DataEleFake_2017/DataEleFake_2017.root"
elif 'Mu' in input_folder: DataToRun = "DataMuFake_2017/DataMuFake_2017.root"
elif 'HT' in input_folder: DataToRun = "DataHT/DataHT_2017.root"

if not opt.debug and not opt.onlybkg:
    dataSample=input_folder+ DataToRun
    print("working on data sample: ", dataSample)
    FakeCalc(dataSample, True, evs)
    if opt.bkg or opt.onlybkg:
        for bkg in bkg_files:
            FakeCalc(input_folder+bkg, False, evs)
elif opt.debug:
    dataSample=input_folder+ DataToRun
    print("working on data sample: ", dataSample)
    FakeCalc(dataSample, True, evs)
    

hTotList = [looseDatalist, tightDatalist, looseMClist, tightMClist]

for l in hTotList:
    for h in l:
        h.Sumw2()


for i in range(3):
    j=1
    while j<5:
        looseDatalist[i].SetBinContent(5, j, looseDatalist[i].GetBinContent(5,j)+looseDatalist[i].GetBinContent(6,j))
        looseDatalist[i].SetBinError(5, j, math.sqrt(pow(looseDatalist[i].GetBinError(5,j),2) + pow(looseDatalist[i].GetBinError(6,j),2)))
        tightDatalist[i].SetBinContent(5, j, tightDatalist[i].GetBinContent(5,j)+tightDatalist[i].GetBinContent(6,j))
        tightDatalist[i].SetBinError(5, j, math.sqrt(pow(tightDatalist[i].GetBinError(5,j),2) + pow(tightDatalist[i].GetBinError(6,j),2)))

        looseMClist[i].SetBinContent(5, j, looseMClist[i].GetBinContent(5,j)+looseMClist[i].GetBinContent(6,j))
        looseMClist[i].SetBinError(5, j, math.sqrt(pow(looseMClist[i].GetBinError(5,j),2) + pow(looseMClist[i].GetBinError(6,j),2)))
        tightMClist[i].SetBinContent(5, j, tightMClist[i].GetBinContent(5,j)+tightMClist[i].GetBinContent(6,j))
        tightMClist[i].SetBinError(5, j, math.sqrt(pow(tightMClist[i].GetBinError(5,j),2) + pow(tightMClist[i].GetBinError(6,j),2)))
        j+=1


    FRDatalist[i] = tightDatalist[i].Clone(FRDataname[i])
    FRDatalist[i].SetName(FRDataname[i])
    FRDatalist[i].SetTitle(FRDatatitle[i])
    FRDatalist[i].Divide(looseDatalist[i])
    
    FRMClist[i] = tightMClist[i].Clone(FRMCname[i])
    FRMClist[i].SetName(FRMCname[i])
    FRMClist[i].SetTitle(FRMCtitle[i])
    FRMClist[i].Divide(looseMClist[i])

    FRdiflist[i] = tightDatalist[i].Clone(FRdifname[i])
    FRdiflist[i].SetName(FRdifname[i])
    FRdiflist[i].SetTitle(FRdiftitle[i])
    FRdiflist[i].Add(tightMClist[i], -1)

    htemp = looseDatalist[i].Clone("htemp")
    htemp.Add(looseMClist[i], -1)

    FRdiflist[i].Divide(htemp)

    #FRDatalist[i] = (hcloneData.Divide(tightDatalist[i])).Clone(FRDataname[i])
    #FRMClist[i]   = (hcloneMC.Divide(tightMClist[i])).Clone(FRMCname[i])
    

f.Write()

'''
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
    outFile.write("-------------------------")
    outFile.write("Muons \n")
    for pos in Fake_dicti_mu:
        L=[str(Fake_dicti_mu[pos][0]), "\t : nTot \t", str(Fake_dicti_mu[pos][1]), "\t nGood \t", str(Fake_dicti_mu[pos][2]), "\t FR:\t ", str(Fake_dicti_mu[pos][3]), "\n"]
        outFile.writelines(L)    
    outFile.write("-------------------------")
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

    if opt.promptFakeTau:
        print("Taus:")
        for pos in Fake_dicti_tau:
            Fake_dicti_tau[pos][3]=Fake_dicti_tau[pos][2]*1.0/Fake_dicti_tau[pos][1]
            print pos, Fake_dicti_tau[pos][0], ": nTot ", Fake_dicti_tau[pos][1], " nGood ", Fake_dicti_tau[pos][2], " FR: ", Fake_dicti_tau[pos][3]

'''



