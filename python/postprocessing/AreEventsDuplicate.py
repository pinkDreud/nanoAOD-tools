import os, commands
import sys
import optparse
import ROOT
import math
import copy
import datetime
import time
from FakeRatio_utils_dev import *
#from samples.samples import *


usage = 'python FakeRatio_calculator_v3.py -b --met 50 --mt 50 --inf FR_24Gen_Ele --trig Ele'
parser = optparse.OptionParser(usage)

parser.add_option('--met', dest='met_cut', type=int, default = '30', help='insert met cut, default 30')
parser.add_option('--mt', dest='mt_lepMET_cut', type=int, default = '20', help='insert met cut, default 20')
parser.add_option('-b', '--bkg', dest='bkg', default = False, action='store_true', help='Eliminate contribution fromprompt W+Jets && DY+Jets events, default false')
parser.add_option('--onlybkg', dest='onlybkg', default = False,action='store_true', help='Only MC prompt contribution, default false')
parser.add_option('-d', '--debug', dest='debug', default = False, action='store_true', help='Debug mode, only runs in a file for 10000 events')
parser.add_option('--trig', dest='trig', type=str, default = 'all', help='trigger used, default all')
parser.add_option('--inf', dest='infolder', type=str, default = '', help='Please enter an input folder folder, default FR_v10/Ele')
parser.add_option('--user', dest='user', type=str, default = 'mmagheri', help='Enter user, default mmagheri')
(opt, args) = parser.parse_args()


input_folder = '/eos/user/'+ opt.user[0]+ '/'+opt.user+'/VBS/nosynch/' + opt.infolder + '/'
print(input_folder)

if not os.path.isdir(input_folder): raise NameError('ERROR, directory not found')

today = datetime.date.today()
time  = datetime.datetime.now()

print('Today is :' + str(today) + ' and the time is: '+ str(time))

def AreThereDuplicates(sample, isData, nev):
    print('workin on sample: ' + sample)
    print('is data?        : ', isData)
    print('workin on events: ', nev)
    
    print(sample)
    if not os.path.exists(sample):
        raise NameError('sample do not exists')
    
    print('\n')
    
    chain = ROOT.TChain('events_all')
    chain.Add(sample)
    print (chain)
 
    tree = InputTree(chain)
    
    isMC = not isData
    
    
    maxEvents = nev
    if maxEvents == 'all' or maxEvents>tree.GetEntries():
        maxEvents = tree.GetEntries()
        
    perc = 0

    for i in range(maxEvents):
            
        if i*1.0/maxEvents*100 > perc: 
            print('Processing at: ', perc, '%')
            perc +=1
        event       = Event(tree, i)
        lepton      = Object(event, "lepton")
        tau         = Object(event, "tau")
        met         = Object(event, "MET")
       
        lepList = []
        tauList = []
        
        if lepton.pt <0 or tau.pt<0: continue

        thisLep = [lepton.pdgid, lepton.pt, lepton.eta, lepton.phi]
        thisTau = [tau.DecayMode, tau.pt, tau.eta, tau.phi]

        if thisLep in lepList:
            print("We've found this exact lepton!", '\n', 'Insert 1/True if you want to search for the tau too, 0/False if you do not want')
            goForTau = Input()
            print('Searching for same tau: ', goForTau)
            if goForTau == 1 or goForTau == True:
                if thisTau in tauList:
                    print("We've found this exact TAU! HOLY CAPPERONI", '\n')
        lepList.append(thisLep)
        tauList.append(thisTau)






AreThereDuplicates("/eos/home-a/apiccine/VBS/nosynch/v90/ltau/DataMuB_2017/DataMuB_2017_part0.root", True, 'all')


