import os
import sys
import ROOT
import math
import datetime
import copy
from array import array
import optparse
from FakeRatio_utils import *
usage = "python ControlGenStatus.py -l"

parser = optparse.OptionParser(usage)

parser.add_option('--ntuple', dest='ntuple', default = "DY4JetsToLL_prova.root", help='Set ntuple on which it should work. Default is DY4JetsToLL_prova_ntuple.root')
parser.add_option('-p', '--part', dest='part', default = "0", help='Number of the part. Default=0')
parser.add_option('-s', '--sample', dest='sample', default = "DY4JetsToLL_2017", help='Name of the sample in samples_local.py')
parser.add_option('-l', '--local', dest='local', default = False, action='store_true', help='Local execution')
parser.add_option('-d', '--dbg', dest='dbg', default = False, action='store_true', help='less events, just for debugging')

(opt, args) = parser.parse_args()

if not opt.local:
    from samples import *
    Debug = False
else:
    from samples.samplesLocal import *
    Debug = True

sample = sample_dict[opt.sample]
part_idx = opt.part

file_list = list(map(str, (opt.ntuple).strip('[]').split(',')))
print(file_list)

MCReco=True
startTime = datetime.datetime.now()
print("Starting running at " + str(startTime))

ROOT.gROOT.SetBatch()

chain = ROOT.TChain('Events')
#print(chain)
for infile in file_list: 
    print("Adding %s to the chain" %(infile))
    chain.Add(infile)
print(chain)

print("Number of events in chain " + str(chain.GetEntries()))
print("Number of events in tree from chain " + str((chain.GetTree()).GetEntries()))
tree = InputTree(chain)
isMC = True
if ('Data' in sample.label):
    isMC = False

MCReco = MCReco * isMC

isData= not isMC
#++++++++++++++++++++++++++++++++++
#++   branching the new trees    ++
#++++++++++++++++++++++++++++++++++
outTreeFile = ROOT.TFile(sample.label+"_part"+str(part_idx)+".root", "RECREATE") # output file


trees = []
for i in range(10):
    trees.append(None)
#systZero = systWeights()
# defining the operations to be done with the systWeights class
maxSysts = 0
addPDF = True
addQ2 = False
addTopPt = False
addVHF = False
addTTSplit = False
addTopTagging = False
addWTagging = False
addTrigSF = False
nPDF = 0

systTree = systWeights()
systTree.prepareDefault(True, addQ2, addPDF, addTopPt, addVHF, addTTSplit)
systTree.addSelection("all")
systTree.initTreesSysts(trees, outTreeFile)

systTree.setWeightName("w_nominal",1.)
systTree.setWeightName("puSF",1.)
systTree.setWeightName("puUp",1.)
systTree.setWeightName("puDown",1.)
systTree.setWeightName("lepSF",1.)
systTree.setWeightName("lepUp",1.)
systTree.setWeightName("lepDown",1.)
systTree.setWeightName("PFSF",1.)
systTree.setWeightName("PFUp",1.)
systTree.setWeightName("PFDown",1.)


#++++++++++++++++++++++++++++++++++
#++     variables to branch      ++
#++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++++++++++++++
#++         All category         ++
#++++++++++++++++++++++++++++++++++

#ssWW variables
var_list = []

#all leptons for fake
FakeLepton_pt               =   array.array('f', [-999.])
FakeLepton_eta              =   array.array('f', [-999.])
FakeLepton_phi              =   array.array('f', [-999.])
FakeLepton_mass             =   array.array('f', [-999.])
FakeLepton_pdgid            =   array.array('i', [-999])
FakeLepton_pfRelIso03       =   array.array('f', [-999.])
FakeLepton_isPrompt         =   array.array('f', [-999.])
var_list.append(FakeLepton_pt)
var_list.append(FakeLepton_isPrompt)
var_list.append(FakeLepton_eta)
var_list.append(FakeLepton_phi)
var_list.append(FakeLepton_mass)
var_list.append(FakeLepton_pdgid)
var_list.append(FakeLepton_pfRelIso03)

FakeTau_pt                  =   array.array('f', [-999.])
FakeTau_isPrompt            =   array.array('f', [-999.])
FakeTau_eta                 =   array.array('f', [-999.])
FakeTau_phi                 =   array.array('f', [-999.])
FakeTau_charge              =   array.array('i', [-999])
FakeTau_mass                =   array.array('f', [-999.])
FakeTau_DeepTauWP       =   array.array('f', [-999.])
var_list.append(FakeTau_pt)
var_list.append(FakeTau_isPrompt)
var_list.append(FakeTau_eta)
var_list.append(FakeTau_phi)
var_list.append(FakeTau_charge)
var_list.append(FakeTau_mass)
var_list.append(FakeTau_DeepTauWP)

#MET
MET_pt                      =   array.array('f', [-999.])
MET_phi                     =   array.array('f', [-999.])
mT_lepMET                     =   array.array('f', [-999.])
var_list.append(MET_pt)
var_list.append(MET_phi)
var_list.append(mT_lepMET)

isFake_tau                   =   array.array('i', [-999])
isFake_tauAndPassCuts       =   array.array('i', [-999])
isFake_lepton                =   array.array('i', [-999])
isFake_leptonAndPassCuts    =   array.array('i', [-999])
var_list.append(isFake_tau)
var_list.append(isFake_tauAndPassCuts)
var_list.append(isFake_lepton)

w_PDF_all = array.array('f', [0.]*110) #capisci a cosa serve
w_nominal_all = array.array('f', [0.])

#branches added for ssWW analysis
#all leptons for fake calculation
systTree.branchTreesSysts(trees, "all", "FakeLepton_pt",            outTreeFile, FakeLepton_pt)
systTree.branchTreesSysts(trees, "all", "FakeLepton_isPrompt",      outTreeFile, FakeLepton_isPrompt)
systTree.branchTreesSysts(trees, "all", "FakeLepton_eta",           outTreeFile, FakeLepton_eta)
systTree.branchTreesSysts(trees, "all", "FakeLepton_phi",           outTreeFile, FakeLepton_phi)
systTree.branchTreesSysts(trees, "all", "FakeLepton_mass",          outTreeFile, FakeLepton_mass)
systTree.branchTreesSysts(trees, "all", "FakeLepton_pdgid",         outTreeFile, FakeLepton_pdgid)
systTree.branchTreesSysts(trees, "all", "FakeLepton_pfRelIso03",    outTreeFile, FakeLepton_pfRelIso03)

#all taus for fake calculation
systTree.branchTreesSysts(trees, "all", "FakeTau_pt",               outTreeFile, FakeTau_pt)
systTree.branchTreesSysts(trees, "all", "FakeTau_isPrompt",      outTreeFile, FakeTau_isPrompt)
systTree.branchTreesSysts(trees, "all", "FakeTau_eta",              outTreeFile, FakeTau_eta)
systTree.branchTreesSysts(trees, "all", "FakeTau_phi",              outTreeFile, FakeTau_phi)
systTree.branchTreesSysts(trees, "all", "FakeTau_mass",             outTreeFile, FakeTau_mass)
systTree.branchTreesSysts(trees, "all", "FakeTau_DeepTauWP",        outTreeFile, FakeTau_DeepTauWP)
systTree.branchTreesSysts(trees, "all", "MET_pt",                   outTreeFile, MET_pt)
systTree.branchTreesSysts(trees, "all", "mT_lepMET",                outTreeFile, mT_lepMET)

#fake variables
systTree.branchTreesSysts(trees, "all", "isFake_lepton",                   outTreeFile, isFake_lepton)
systTree.branchTreesSysts(trees, "all", "isFake_tau",                   outTreeFile, isFake_tau)
systTree.branchTreesSysts(trees, "all", "isFake_leptonAndPassCuts",       outTreeFile, isFake_leptonAndPassCuts)
systTree.branchTreesSysts(trees, "all", "isFake_tauAndPassCuts",       outTreeFile, isFake_tauAndPassCuts)


#print("Is MC: " + str(isMC) + "      option addPDF: " + str(addPDF))
if(isMC and addPDF):
    systTree.branchTreesSysts(trees, "all", "w_PDF", outTreeFile, w_PDF_all)
####################################################################################################################################################################################################################################

#++++++++++++++++++++++++++++++++++
#++      taking MC weights       ++
#++++++++++++++++++++++++++++++++++
print("isMC: ", isMC)
if(isMC):
    newfile = ROOT.TFile.Open(file_list[0])
    dirc = ROOT.TDirectory()
    dirc = newfile.Get("plots")
    isthere_gen = bool(dirc.GetListOfKeys().Contains("h_genweight"))
    isthere_pdf = bool(dirc.GetListOfKeys().Contains("h_PDFweight"))
    print("gen?: ", isthere_gen, " pdf?: ", isthere_pdf)

    if isthere_gen or isthere_pdf:
        if isthere_gen:
            h_genweight = ROOT.TH1F()
            h_genweight.SetNameTitle('h_genweight', 'h_genweight')
            h_genw_tmp = ROOT.TH1F(dirc.Get("h_genweight"))
            if(ROOT.TH1F(h_genweight).Integral() < 1.):
                h_genweight.SetBins(h_genw_tmp.GetXaxis().GetNbins(), h_genw_tmp.GetXaxis().GetXmin(), h_genw_tmp.GetXaxis().GetXmax())
            h_genweight.Add(h_genw_tmp)
    
        if isthere_pdf:
            h_PDFweight = ROOT.TH1F()
            h_PDFweight.SetNameTitle("h_PDFweight","h_PDFweight")
            h_pdfw_tmp = ROOT.TH1F(dirc.Get("h_PDFweight"))
            if(ROOT.TH1F(h_PDFweight).Integral() < 1.):
                h_PDFweight.SetBins(h_pdfw_tmp.GetXaxis().GetNbins(), h_pdfw_tmp.GetXaxis().GetXmin(), h_pdfw_tmp.GetXaxis().GetXmax())
            h_PDFweight.Add(h_pdfw_tmp)
        else:
            addPDF = False
    newfile.Close()

#++++++++++++++++++++++++++++++++++
#++   looping over the events    ++
#++++++++++++++++++++++++++++++++++
entries=tree.GetEntries()
if opt.dbg: entries=entries/100

for i in range(entries):
    #reinizializza tutte le variabili a 0, per sicurezza
    for j, var in enumerate(var_list):
        if j<len(var_list):
            var_list[j][0] = -999
    
    w_nominal_all[0] = 1.
    #++++++++++++++++++++++++++++++++++
    #++        taking objects        ++
    #++++++++++++++++++++++++++++++++++
    '''
    if Debug:
        print("evento n. " + str(i))
        if i > 2000:
            break
    
    if not Debug and i%5000 == 0:
    '''
    #print("Event #", i+1, " out of ", tree.GetEntries())

    event       = Event(tree,i)
    electrons   = Collection(event, "Electron")
    muons       = Collection(event, "Muon")
    jets        = Collection(event, "Jet")
    njets       = len(jets)
    fatjets     = Collection(event, "FatJet")
    taus        = Collection(event, "Tau")
    HT          = Object(event, "HT")
    PV          = Object(event, "PV")
    HLT         = Object(event, "HLT")
    Flag        = Object(event, 'Flag')
    met         = Object(event, "MET")
    
    genpart = None
    
    if isMC:
        genpart = Collection(event, "GenPart")
        if not ("WZ" in sample.label):
            LHE = Collection(event, "LHEPart")
    
    if not isMC:
        if not Flag.eeBadScFilter:
            continue

    chain.GetEntry(i)


    #++++++++++++++++++++++++++++++++++
    #++      defining variables      ++
    #++++++++++++++++++++++++++++++++++
    tightlep = None
    tightlep_p4 = None
    tightlep_p4t = None
    tightlep_SF = None
    tightlep_SFUp = None
    tightlep_SFDown = None
    recomet_p4t = None
    PF_SF = None
    PF_SFUp = None
    PF_SFDown = None
    PU_SF = None
    PU_SFUp = None
    PU_SFDown = None
    #++++++++++++++++++++++++++++++++++
    #++    starting the analysis     ++
    #++++++++++++++++++++++++++++++++++
    year = sample.year
    if(isMC):
        runPeriod = ''
    else:
        runPeriod = sample.runP
    
    passMu, passEle, passHT, noTrigger = trig_map(HLT, PV, year, runPeriod)

    if not passEle: continue
    
    for ele in electrons:
        genIDX=ele.genPartIdx
        
        if genIDX<0 or genIDX>len(genpart): continue

        if genpart[genIDX].pdgId==ele.pdgId: 
            print("Event #", i+1, " out of ", tree.GetEntries())
            #print "ele infos: ", ele.pt, " ", ele.eta, " ", ele.pdgId
            #print "gen idx: ", genIDX
            print "gen part infos: ", genpart[genIDX].pt, " ", genpart[genIDX].eta, " ", genpart[genIDX].pdgId
            #print "difference genreco: ", deltaR(ele.eta, ele.phi, genpart[genIDX].eta, genpart[genIDX].phi)
            print "genpartFlav: ", ele.genPartFlav
            #print "status flag gen: ", genpart[genIDX].statusFlags
            if genpart[genIDX].genPartIdxMother>=0 and genpart[genIDX].genPartIdxMother<len(genpart): 
                print "gen part mother: ", genpart[genpart[genIDX].genPartIdxMother].pdgId













