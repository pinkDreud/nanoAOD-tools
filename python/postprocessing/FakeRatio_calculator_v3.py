import os, commands
import sys
import optparse
import ROOT
import math
import copy
import datetime
import time
from FakeRatio_utils_dev import *
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *


usage = 'python FakeRatio_calculator_v3.py -b --met 50 --mt 50 --inf FR_24Gen_Ele --trig Ele'
parser = optparse.OptionParser(usage)

parser.add_option('--met', dest='met_cut', type=int, default = '30', help='insert met cut, default 30')
parser.add_option('--mt', dest='mt_lepMET_cut', type=int, default = '20', help='insert met cut, default 20')
parser.add_option('-b', '--bkg', dest='bkg', default = False, action='store_true', help='Eliminate contribution fromprompt W+Jets && DY+Jets events, default false')
parser.add_option('--onlybkg', dest='onlybkg', default = False,action='store_true', help='Only MC prompt contribution, default false')
parser.add_option('-d', '--debug', dest='debug', default = False, action='store_true', help='Debug mode, only runs in a file for 10000 events')
parser.add_option('--trig', dest='trig', type=str, default = 'all', help='trigger used, default all')
parser.add_option('--inf', dest='infolder', type=str, default = '', help='Please enter an input folder folder, default FR_v10/Ele')

(opt, args) = parser.parse_args()


input_folder = '/eos/user/m/mmagheri/VBS/nosynch/' + opt.infolder + '/'

if not os.path.isdir(input_folder): raise NameError('ERROR, directory not found')

print('Processing events with met cut: ' + str(opt.met_cut) + ' and mT(lep, MET) cut: ' + str(opt.mt_lepMET_cut))

FRdifname = {
        'Ele' : "hFRDataeledif",
        'Mu'  : "hFRDatamudif",
        'Tau' : "hFRDatataudif",
        }
FRdiftitle = {
        'Ele' : "Electron Data-MC fake ratio",
        'Mu'  : "Muon Data-MC fake ratio",
        'Tau' : "Tau Data-MC fake ratio",
        }
FRDataname = {
        'Ele' : "hFRDataele",
        'Mu'  : "hFRDatamu",
        'Tau' : "hFRDatatau",
        }
FRDatatitle = {
        'Ele' : "Electron Data fake ratio",
        'Mu'  : "Muon Data fake ratio",
        'Tau' : "Tau Data fake ratio",
        }
FRMCname = {
        'Ele' : "hFRMCele",
        'Mu'  : "hFRMCmu",
        'Tau' : "hFRMCtau",
        }
FRMCtitle = {
        'Ele' : "Electron MC fake ratio",
        'Mu'  : "Muon MC fake ratio",
        'Tau' : "Tau MC fake ratio",
        }


Fake_dicti_ele = {
            '11': ['|n|<1,     pT<20    ',  0,  0, 0.0],
            '12': ['1<|n|<1.5, pT<20    ',  0,  0, 0.0],
            '13': ['1.5<|n|<2, pT<20    ',  0,  0, 0.0],
            '14': ['2<|n|<2.4, pT<20    ',  0,  0, 0.0],
            '21': ['|n|<1,     20<pT<30 ',  0,  0, 0.0],
            '22': ['1<|n|<1.5, 20<pT<30 ',  0,  0, 0.0],
            '23': ['1.5<|n|<2, 20<pT<30 ',  0,  0, 0.0],
            '24': ['2<|n|<2.4, 20<pT<30 ',  0,  0, 0.0],
            '31': ['|n|<1,     30<pT<40 ',  0,  0, 0.0],
            '32': ['1<|n|<1.5, 30<pT<40 ',  0,  0, 0.0],
            '33': ['1.5<|n|<2, 30<pT<40 ',  0,  0, 0.0],
            '34': ['2<|n|<2.4, 30<pT<40 ',  0,  0, 0.0],
            '41': ['|n|<1,     40<pT<50 ',  0,  0, 0.0],
            '42': ['1<|n|<1.5, 40<pT<50 ',  0,  0, 0.0],
            '43': ['1.5<|n|<2, 40<pT<50 ',  0,  0, 0.0],
            '44': ['2<|n|<2.4, 40<pT<50 ',  0,  0, 0.0],
            '51': ['|n|<1,     pT>50    ',  0,  0, 0.0],
            '52': ['1<|n|<1.5, pT>50    ',  0,  0, 0.0],
            '53': ['1.5<|n|<2, pT>50    ',  0,  0, 0.0],
            '54': ['2<|n|<2.4, pT>50    ',  0,  0, 0.0],
}

Fake_dicti_mu = copy.deepcopy(Fake_dicti_ele)
Fake_dicti_tau = copy.deepcopy(Fake_dicti_ele)

lower_pt = [0, 20, 30, 40, 50, 60]
lower_eta = [0, 1, 1.4, 2, 2.4]

today = datetime.date.today()
time  = datetime.datetime.now()

print('Today is :' + str(today) + ' and the time is: '+ str(time))

outdir = 'FakeRatio_calcs/' + opt.infolder + '/'

if not os.path.isdir(outdir):
    try:
        os.mkdir(outdir)
    except OSError:
        print ('Creation of the directory %s failed ' % outdir)
    else:
        print ('Successfully created the directory %s ' % outdir)


filename =  str(opt.trig) + '_FakeRatio_METcut_' + str(opt.met_cut) + '_mt_lep_MET_cut_' + str(opt.mt_lepMET_cut) + '_DateTime_' + str(today)
if opt.bkg:     filename += '_MCpromptSUBTRACTED'
if opt.onlybkg: filename += '_onlymcprompt'

print('saving output in: ' + outdir + filename)


f = ROOT.TFile(outdir+filename+".root", "RECREATE")

filename += '.txt'

hNLooseEle_Data = ROOT.TH2F("h2NLooseEle_data", "Electron #loose events", 5, array.array('d', lower_pt), 4, array.array('d', lower_eta))
hNLooseMu_Data  = ROOT.TH2F("h2NLooseMu_data",  "Muon #loose events",     5, array.array('d', lower_pt), 4, array.array('d', lower_eta))
hNLooseTau_Data = ROOT.TH2F("h2NLooseTau_data", "Tau #loose events",      5, array.array('d', lower_pt), 4, array.array('d', lower_eta))

looseDatalist = {
        'Ele' : hNLooseEle_Data, 
        'Mu'  : hNLooseMu_Data, 
        'Tau' : hNLooseTau_Data,
        }

hNTightEle_Data = ROOT.TH2F("h2NTightEle_data", "Electron #tight events", 5, array.array('d', lower_pt), 4, array.array('d', lower_eta))
hNTightMu_Data  = ROOT.TH2F("h2NTightMu_data",  "Muon #tight events",     5, array.array('d', lower_pt), 4, array.array('d', lower_eta))
hNTightTau_Data = ROOT.TH2F("h2NTightTau_data", "Tau #tight events",      5, array.array('d', lower_pt), 4, array.array('d', lower_eta))

tightDatalist = {
        'Ele' : hNTightEle_Data, 
        'Mu'  : hNTightMu_Data,
        'Tau' : hNTightTau_Data,
        }

hNLooseEle_MC = ROOT.TH2F("h2NLooseEle_MC", "Electron #loose events", 5, array.array('d', lower_pt), 4, array.array('d', lower_eta))
hNLooseMu_MC  = ROOT.TH2F("h2NLooseMu_MC",  "Muon #loose events",     5, array.array('d', lower_pt), 4, array.array('d', lower_eta))
hNLooseTau_MC = ROOT.TH2F("h2NLooseTau_MC", "Tau #loose events",      5, array.array('d', lower_pt), 4, array.array('d', lower_eta))

looseMClist = {
        'Ele' : hNLooseEle_MC,
        'Mu'  : hNLooseMu_MC,
        'Tau' : hNLooseTau_MC,
        }

hNTightEle_MC = ROOT.TH2F("h2NTightEle_MC", "Electron #tight events", 5, array.array('d', lower_pt), 4, array.array('d', lower_eta))
hNTightMu_MC  = ROOT.TH2F("h2NTightMu_MC",  "Muon #tight events",     5, array.array('d', lower_pt), 4, array.array('d', lower_eta))
hNTightTau_MC = ROOT.TH2F("h2NTightTau_MC", "Tau #tight events",      5, array.array('d', lower_pt), 4, array.array('d', lower_eta))

tightMClist = {
        'Ele' : hNTightEle_MC,
        'Mu'  : hNTightMu_MC,
        'Tau' : hNTightTau_MC,
        
        }
def FakeCalc(sample, isData, nev):
    print('workin on sample: ' + sample)
    print('is data?        : ', isData)
    print('workin on events: ', nev)
    
    print(sample)
    if not os.path.exists(sample):
        raise NameError('sample do not exists')
    
    print('\n')
    
    looseList = looseDatalist
    tightList = tightDatalist

    chain = ROOT.TChain('events_all')
    chain.Add(sample)
    print (chain)
 
    tree = InputTree(chain)
    
    isMC = not isData
    
    if isMC:
        looseList = looseMClist
        tightlist = tightMClist
    
    if isData and opt.onlybkg:
        print('the sample: ', sample, 'is tagged as data sample, while you are running in only bkg mode, jumping the sample')
    
    sign = 1    
    if isMC and not opt.onlybkg: sign = -1
    
    maxEvents = nev
    if maxEvents == 'all' or maxEvents>tree.GetEntries():
        maxEvents = tree.GetEntries()
        
    nLooseEle = 0
    nLooseMu  = 0
    nLooseTau = 0
    nTightEle = 0
    
    perc = 0

    for i in range(maxEvents):
            
        if i*1.0/maxEvents*100 > perc: 
            print('Processing at: ', perc, '%')
            perc +=1
        event       = Event(tree, i)
        FakeLepton  = Object(event, "FakeLepton")
        FakeTau     = Object(event, "FakeTau")

        met         = Object(event, "MET")
        mT          = Object(event, "mT")
        w           = Object(event, "w")
        nleps       = Object(event, "nLeps")
        jets        = Object(event, "Jet")
        veto        = Object(event, "Veto")
        #if i%1000==0: print('event ---- ', i, '\n', FakeLepton.pt, ' ', FakeLepton.eta)
        SF = 1
        if isMC:
            SF = w.nominal*sign*event.PFSF*event.puSF
        
        if met.pt>opt.met_cut or mT.lepMET>opt.mt_lepMET_cut or mT.lepMET<0 or met.pt<0:
            continue

        #print('Checking met ', met.pt, 'checking mT: ', mT.lepMET)

        if opt.trig == 'Ele' or opt.trig == 'all' and abs(FakeLepton.pdgid) == 11 and nleps.LightLeptons < 2 and jets.numberSeparate >0 and  abs(FakeLepton.eta)<2.4 and not(abs(FakeLepton.eta)>1.4442 and abs(FakeLepton.eta)<1.566) and FakeLepton.pt>0 and FakeLepton.jetRelIso>=0:
            if isMC and (FakeLepton.isPrompt!=1): 
                SF = 0
                
            ptBin  = pTCalculator(FakeLepton.pt)
            etaBin = etaCalculator(FakeLepton.eta)
            dictPos = str(ptBin) +str(etaBin[1])
            Fake_dicti_ele[dictPos][1] += SF
               
            looseList['Ele'].Fill(FakeLepton.pt, abs(FakeLepton.eta), SF) 

            if FakeLepton.pfRelIso04<0.08 and FakeLepton.isTight:
                Fake_dicti_ele[dictPos][2] += SF
                tightList['Ele'].Fill(FakeLepton.pt, abs(FakeLepton.eta), SF) 
        
        elif opt.trig == 'Mu' or opt.trig == 'all' and abs(FakeLepton.pdgid) == 13 and nleps.LightLeptons < 2 and jets.numberSeparate > 0 and  abs(FakeLepton.eta)<2.4 and FakeLepton.pt>0 and FakeLepton.pfRelIso04>=0:
            if isMC and (FakeLepton.isPrompt!=1):
                SF = 0
                  
            ptBin  = pTCalculator(FakeLepton.pt)
            etaBin = etaCalculator(FakeLepton.eta)
                
            dictPos = str(ptBin) +str(etaBin[1])
            Fake_dicti_mu[dictPos][1] += SF
                
            looseList['Mu'].Fill(FakeLepton.pt, abs(FakeLepton.eta), SF) 
                
                #print(FakeLepton.pfRelIso04, FakeLepton.isTight)

            if abs(FakeLepton.pfRelIso04)<0.15 and FakeLepton.isTight:
                Fake_dicti_mu[dictPos][2] += SF
                tightList['Mu'].Fill(FakeLepton.pt, abs(FakeLepton.eta), SF) 
        
        if opt.trig == 'HT' or opt.trig == 'all':
            
            if veto.TauLeptons==1:
                continue

            if abs(FakeTau.eta)<2.4 and FakeTau.pt>0:
              
                if isMC and (FakeTau.isPrompt!=5): 
                    SF = 0
                  
                ptBin  = pTCalculator(FakeTau.pt)
                etaBin = etaCalculator(FakeTau.eta)
                
                dictPos = str(ptBin) +str(etaBin[1])
                Fake_dicti_tau[dictPos][1] += SF
                
                looseList['Tau'].Fill(FakeTau.pt, abs(FakeTau.eta), SF) 

                if FakeTau.DeepTauWP>=64:
                    Fake_dicti_tau[dictPos][2] += SF
                    tightList['Tau'].Fill(FakeTau.pt, abs(FakeTau.eta), SF) 
        
        if(i%10000000 == 0):
            
            if opt.trig == 'Ele' or opt.trig == 'all':
                print('Electrons')
                dict_print(Fake_dicti_ele)
                dict_save(Fake_dicti_ele, Fake_dicti_mu, Fake_dicti_tau, outdir+filename)
    
            if opt.trig == 'Mu' or opt.trig == 'all':
                print('Muons')
                dict_print(Fake_dicti_mu)
                dict_save(Fake_dicti_ele, Fake_dicti_mu, Fake_dicti_tau, outdir+filename)
    
            if opt.trig == 'HT' or opt.trig == 'all':
                print('Taus')
                dict_print(Fake_dicti_tau)
                dict_save(Fake_dicti_ele, Fake_dicti_mu, Fake_dicti_tau, outdir+filename)
 
 
    for k in Fake_dicti_tau:
        if Fake_dicti_tau[k][2] == 0: Fake_dicti_tau[k][2]=3.0000001
 
    for k in Fake_dicti_ele:
        if Fake_dicti_ele[k][2] == 0: Fake_dicti_ele[k][2]=3.0000001
 
    for k in Fake_dicti_mu:
        if Fake_dicti_mu[k][2] == 0: Fake_dicti_mu[k][2]=3.0000001




    if opt.trig == 'Ele' or opt.trig == 'all':
        print('Electrons')
        dict_print(Fake_dicti_ele)
        dict_save(Fake_dicti_ele, Fake_dicti_mu, Fake_dicti_tau, outdir+filename)
    
    if opt.trig == 'Mu' or opt.trig == 'all':
        print('Muons')
        dict_print(Fake_dicti_mu)
        dict_save(Fake_dicti_ele, Fake_dicti_mu, Fake_dicti_tau, outdir+filename)
    
    if opt.trig == 'HT' or opt.trig == 'all':
        print('Taus')
        dict_print(Fake_dicti_tau)
        dict_save(Fake_dicti_ele, Fake_dicti_mu, Fake_dicti_tau, outdir+filename)
    

    
    hTotList = [looseDatalist, tightDatalist, looseMClist, tightMClist]
   
    print('\n')

    for l in hTotList:
        for h in l:
            l[h].Sumw2()
    
    for i in looseDatalist:
        print i
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
        '''
        hFRData = copy.deepcopy(tightDatalist[i])
        hFRData.SetName(FRDataname[i])
        print(hFRData.GetTitle())
        hFRData.SetTitle(FRDatatitle[i])
        print(hFRData.GetTitle())
        hFRData.Divide(looseDatalist[i])
        print(hFRData.GetName())
        '''
        nX = 1
        nY = 1
        
        
        print("PARAPAAAAA",  tightDatalist[i].GetNbinsX())
        for nX in range(1,tightDatalist[i].GetNbinsX() + 1):
            for nY in range(1, tightDatalist[i].GetNbinsY() + 1):
                if (tightDatalist[i].GetBinContent(nX, nY) == 0):
                    tightDatalist[i].SetBinContent(nX, nY, 3.001)
                    tightDatalist[i].SetBinError(nX, nY, math.sqrt(3.001))
                    #print(tightDatalist[i].GetBinContent(nX, nY))

        
        hFRData = tightDatalist[i].Clone(FRDatatitle[i])
        hFRData.SetName(FRDataname[i])
        hFRData.SetTitle(FRDatatitle[i])
        
        for nX in range(1, hFRData.GetNbinsX() + 1):
            for nY in range(1, hFRData.GetNbinsY() + 1):
                if (hFRData.GetBinContent(nX, nY) == 0):
                    hFRData.SetBinContent(nX, nY, 3.001)
                    hFRData.SetBinError(nX, nY, math.sqrt(3.001))
                    #print(tightDatalist[i].GetBinContent(nX, nY))

                print nX, nY, hFRData.GetBinContent(nX, nY)
         
        hFRData.Divide(looseDatalist[i])
         
        if opt.bkg:
            hFRMC = tightMClist[i].Clone(FRMCtitle[i])
            hFRMC.SetName(FRMCname[i])
            hFRMC.SetTitle(FRMCtitle[i])
            hFRMC.Divide(looseMClist[i])

            hFRdif = tightDatalist[i].Clone(FRdiftitle[i])
            hFRdif.SetName(FRdifname[i])
            hFRdif.SetTitle(FRdiftitle[i])
            hFRdif.Add(tightMClist[i], -1)
    
            htmp = looseDatalist[i]
            htmp.Add(looseMClist[i], -1)

            hFRdif.Divide(htmp)
        f.Write()




DataDict = {
        'Ele' : "DataEleFake_2017/DataEleFake_2017.root",
        'Mu'  : "DataMuFake_2017/DataMuFake_2017.root",
        'Tau' : "DataHT_2017/DataHT_2017.root",
        'all' : "DataHT_2017/DataHT_2017.root",
        }

bkg_files = {
        'DYJetsToLL' : "DYJetsToLL_2017/DYJetsToLL_2017.root", 
        'WJets'      : "WJets_2017/WJets_2017.root",
        }


if opt.debug:
    file = input_folder + DataDict[opt.trig]
    print('\n')
    print('debug mode')
    FakeCalc(file, True, 100000)
    dict_print(Fake_dicti_ele)
    dict_print(Fake_dicti_ele)
    print('Muons onlyData')
    dict_print(Fake_dicti_mu)
    print('Tau onlyData')
    dict_print(Fake_dicti_tau)
 



else:
    file = input_folder + DataDict[opt.trig]
    FakeCalc(file, True, 'all')
    print('Electrons - onlyData')
    dict_print(Fake_dicti_ele)
    print('Muons onlyData')
    dict_print(Fake_dicti_mu)
    print('Tau onlyData')
    dict_print(Fake_dicti_tau)
    for pos in bkg_files:
        if not opt.bkg: continue
        bkg = input_folder + bkg_files[pos]
        FakeCalc(bkg, False, 'all')
        print('Electrons - wo ', pos)
        dict_print(Fake_dicti_ele)
        print('Muons - wo ', pos)
        dict_print(Fake_dicti_mu)
        print('Tau - wo ', pos)
        dict_print(Fake_dicti_tau)
    



FRData = copy.deepcopy(tightDatalist['Ele'])
FRData.Divide(looseDatalist['Ele'])
FRData.Draw("colz text")

