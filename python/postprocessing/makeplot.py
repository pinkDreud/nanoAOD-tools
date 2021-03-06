import os 
#import commands
import sys
import optparse
import ROOT
import math
from variabile import variabile
import copy as copy
from CMS_lumi import CMS_lumi
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from array import array
import pandas as pd
import uproot
import pickle
import numpy as np

#print TT_2017
#ciao

ROOT.ROOT.EnableThreadSafety()

usage = 'python3 makeplot.py'# -y year --lep lepton -d dataset --merpart --lumi --mertree --sel --cut cut_string -p -s'
usageToCopyPaste= "python3 makeplot.py -y 2017 --lep muon --bveto --user apiccine -f v4 -p"

parser = optparse.OptionParser(usage)
parser.add_option('--merpart', dest='merpart', default = False, action='store_true', help='Default parts are not merged')
parser.add_option('--mertree', dest='mertree', default = False, action='store_true', help='Default make no file is merged')
parser.add_option('--lumi', dest='lumi', default = False, action='store_true', help='Default do not write the normalization weights')
parser.add_option('--sel', dest='sel', default = False, action='store_true', help='Default do not apply any selection')
parser.add_option('--bveto', dest='bveto', default = False, action='store_true', help='Default do not apply any selection')
parser.add_option('--sr', dest='sr', default = False, action='store_true', help='Default do not apply any selection')
parser.add_option('--bdt', dest='bdt', default = False, action='store_true', help='Default do not apply any selection')
parser.add_option('--ebdt', dest='ebdt', default = False, action='store_true', help='Default do not apply any selection')
parser.add_option('--mubdt', dest='mubdt', default = False, action='store_true', help='Default do not apply any selection')
parser.add_option('-p', '--plot', dest='plot', default = False, action='store_true', help='Default make no plots')
parser.add_option('-s', '--stack', dest='stack', default = False, action='store_true', help='Default make no stacks')
parser.add_option('-N', '--notstacked', dest='tostack', default = True, action='store_false', help='Default make plots stacked')
parser.add_option('-L', '--lep', dest='lep', type='string', default = 'incl', help='Default make incl analysis')
parser.add_option('-S', '--syst', dest='syst', type='string', default = 'all', help='Default all systematics added')
parser.add_option('-C', '--cut', dest='cut', type='string', default = '1.', help='Default no cut')
parser.add_option('-y', '--year', dest='year', type='string', default = '2017', help='Default 2016, 2017 and 2018 are included')
parser.add_option('-f', '--folder', dest='folder', type='string', default = 'v7', help='Default folder is v0')
parser.add_option('-d', '--dat', dest='dat', type='string', default = 'all', help="")
parser.add_option('--user', dest='user', type='string', default=str(os.environ.get('USER')), help='User')
parser.add_option('--ttbar', dest='ttbar', default = False, action='store_true', help='Enable ttbar CR, default disabled')
parser.add_option('--count', dest='count', default = False, action='store_true', help='Enable countings')
parser.add_option('--HT', dest='HT', default = False, action='store_true', help='Enable CTHT')
parser.add_option('--wfake', dest='wfake', type='string', default = 'nofake', help='Enable stackplots with data-driven fake leptons, default disabled')
parser.add_option('--wjets', dest='wjets', default = False, action='store_true', help='Enable WJets CR, default disabled')
parser.add_option('--qcd', dest='qcd', default = False, action='store_true', help='Enable QCD CR, default disabled')
parser.add_option('--blinded', dest='blinded', default = False, action='store_true', help='Activate blinding')
parser.add_option('--signal', dest='signal', default = False, action='store_true', help='Activate only signal')
#parser.add_option('--model', dest='model', default = '/eos/user/t/ttedesch/SWAN_projects/VBS_ML/gradBDT.p', type='string', help='Path to ML model')
#parser.add_option('--model', dest='model', default = '/afs/cern.ch/user/t/ttedesch/public/gradBDT.p', type='string', help='Path to ML model for all events')
#parser.add_option('--model_ele', dest='model_ele', default = '/afs/cern.ch/user/t/ttedesch/public/gradBDT_ele.p', type='string', help='Path to ML model for electron events')
#parser.add_option('--model_mu', dest='model_mu', default = '/afs/cern.ch/user/t/ttedesch/public/gradBDT_mu.p', type='string', help='Path to ML model for muon events')
parser.add_option('--model_SM', dest='model_SM', default = '/afs/cern.ch/user/t/ttedesch/public/gradBDT_SM.p', type='string', help='Path to ML model for SM analysis')
parser.add_option('--model_dim6', dest='model_dim6', default = '/afs/cern.ch/user/t/ttedesch/public/gradBDT_dim6.p', type='string', help='Path to ML model for dim6 analysis')
parser.add_option('--model_dim8', dest='model_dim8', default = '/afs/cern.ch/user/t/ttedesch/public/gradBDT_dim8.p', type='string', help='Path to ML model for dim8 analysis')
parser.add_option('--ch', dest='channel', type=str, default = 'ltau', help='Select final state, default is h_tau + lepton')


(opt, args) = parser.parse_args()
#print (opt, args)
print("to stack?", opt.tostack)

def cutToTag(cut):
    newstring = cut.replace("-", "neg").replace(">=","_GE_").replace(">","_G_").replace(" ","").replace("&&","_AND_").replace("||","_OR_").replace("<=","_LE_").replace("<","_L_").replace(".","p").replace("(","").replace(")","").replace("==","_EQ_").replace("!=","_NEQ_").replace("=","_EQ_").replace("*","_AND_").replace("+","_OR_")
    return newstring

folder = opt.folder + "/" + opt.channel
pfolder = opt.folder

filerepo = '/eos/home-'+opt.user[0]+'/'+opt.user+'/VBS/nosynch/' + folder + '/'
plotrepo = '/eos/home-'+opt.user[0]+'/'+opt.user+'/VBS/nosynch/' + pfolder + '/'

print(filerepo, plotrepo)

FRtag = opt.wfake.split("_")[-1]
print("FRtag:", FRtag)

ROOT.gROOT.SetBatch() # don't pop up canvases
if opt.lep != 'incl':
    lepstr = 'plot/' + opt.lep
else:
    if opt.channel == 'emu':
        lepstr = 'plot/' + opt.channel
    else:
        lepstr = 'plot/' + opt.lep

cut = opt.cut #default cut must be obvious, for example 1.

if opt.channel=="ltau":
    epdgstr = "lepton"
    mpdgstr = "lepton"
elif opt.channel=="emu":
    epdgstr = "electron"
    mpdgstr = "muon"

if opt.bveto:
    cut_dict = {'muon':"(abs(" + mpdgstr + "_pdgid)==13&&pass_upToBVeto==1)*(" + cut + ")", 
                 'electron':"(abs(" + epdgstr + "_pdgid)==11&&pass_upToBVeto==1)*(" + cut + ")", 
                 'incl':"((abs(" + mpdgstr + "_pdgid)==13||abs(" + epdgstr + "_pdgid)==11)&&pass_upToBVeto==1)*(" + cut + ")", 
    }
    cut_tag = 'selection_upto_bveto'
    if opt.cut != "1.":
        cut_tag = cut_tag+ '_AND_' + cutToTag(opt.cut) 

elif opt.sr:
    cut_dict = {'muon':"(abs(" + mpdgstr + "_pdgid)==13&&pass_upToBVeto==1&&m_jj>500.&&MET_pt>40.)*(" + cut + ")", 
                'electron':"(abs(" + epdgstr + "_pdgid)==11&&pass_upToBVeto==1&&m_jj>500.&&MET_pt>40.)*(" + cut + ")", 
                'incl':"((abs(" + mpdgstr + "_pdgid)==13||abs(" + epdgstr + "_pdgid)==11)&&pass_upToBVeto==1&&m_jj>500.&&MET_pt>40.)*(" + cut + ")", 
            }
    cut_tag = 'SR'
    if opt.cut != "1.":
        cut_tag = cut_tag+ '_AND_' + cutToTag(opt.cut) 

elif opt.ttbar:
    cut_dict = {'muon':"(abs(" + mpdgstr + "_pdgid)==13&&pass_lepton_selection==1&&pass_tau_selection==1&&pass_lepton_veto==1&&pass_charge_selection==0&&pass_b_veto==0&&pass_jet_selection==1&&MET_pt>50.)*(" + cut + ")", 
                'electron':"(abs(" + epdgstr + "_pdgid)==11&&pass_lepton_selection==1&&pass_tau_selection==1&&pass_lepton_veto==1&&pass_charge_selection==0&&pass_b_veto==0&&pass_jet_selection==1&MET_pt>50.)*(" + cut + ")", 
                'incl':"((abs(" + mpdgstr + "_pdgid)==13||abs(" + epdgstr + "_pdgid)==11)&&pass_lepton_selection==1&&pass_lepton_veto==0&&pass_charge_selection==0&&pass_jet_selection==1&&pass_b_veto==0&&pass_tau_veto==1&&MET_pt>50.)*(" + cut + ")", 
            }
    cut_tag = 'ttbar_CR'
    if opt.cut != "1.":
        cut_tag = cut_tag+ '_AND_' + cutToTag(opt.cut)           
elif opt.wjets:
    cut_dict = {'muon':"(abs(" + mpdgstr + "_pdgid)==13&&pass_lepton_selection==1&&pass_tau_selection==1&&pass_lepton_veto==1&&pass_charge_selection==1&&pass_b_veto==1&&pass_jet_selection==1&&MET_pt<=50.&&mT_lep_MET>50.)*(" + cut + ")", 
                'electron':"(abs(" + epdgstr + "_pdgid)==11&&pass_lepton_selection==1&&pass_tau_selection==1&&pass_lepton_veto==1&&pass_charge_selection==1&&pass_b_veto==1&&pass_jet_selection==1&&MET_pt<=50.&&mT_lep_MET>50.)*(" + cut + ")",
                'incl':"((abs(" + mpdgstr + "_pdgid)==13||abs(" + epdgstr + "_pdgid)==11)&&pass_lepton_selection==1&&pass_lepton_veto==1&&pass_charge_selection==1&&pass_jet_selection==1&&pass_b_veto==1&&pass_tau_veto==1&&MET_pt<=50.&&mT_lep_MET>50.)*(" + cut + ")",
            }
    cut_tag = 'wjets_CR'
    if opt.cut != "1.":
        cut_tag = cut_tag+ '_AND_' + cutToTag(opt.cut)           
elif opt.qcd:
    cut_dict = {'muon':"(abs(" + mpdgstr + "_pdgid)==13&&pass_lepton_selection==1&&pass_tau_selection==1&&pass_lepton_veto==1&&pass_charge_selection==1&&pass_jet_selection==1&&MET_pt<=50.&&mT_lep_MET<50.)*(" + cut + ")", 
                'electron':"(abs(" + epdgstr + "_pdgid)==11&&pass_lepton_selection==1&&pass_tau_selection==1&&pass_lepton_veto==1&&pass_charge_selection==1&&pass_jet_selection==1&&MET_pt<=50.&&mT_lep_MET<50.)*(" + cut + ")",
                'incl':"((abs(" + mpdgstr + "_pdgid)==13||abs(" + epdgstr + "_pdgid)==11)&&pass_lepton_selection==1&&pass_tau_selection==1&&pass_lepton_veto==1&&pass_charge_selection==1&&pass_jet_selection==1&&pass_tau_veto==1&&MET_pt<=50.&&mT_lep_MET<50.)*(" + cut + ")",
            }
    cut_tag = 'QCD_CR'
    if opt.cut != "1.":
        cut_tag = cut_tag+ '_AND_' + cutToTag(opt.cut)           
elif opt.sel:
    cut_dict = {'muon':"(abs(" + mpdgstr + "_pdgid)==13)*(" + cut + ")*(pass_lepton_selection==1&&pass_lepton_veto==1&&pass_tau_selection==1&&pass_charge_selection==1&&pass_jet_selection==1&&pass_b_veto==1&&pass_mjj_cut==1&&pass_MET_cut==1)", 
                'electron':"(abs(" + epdgstr + "_pdgid)==11)*(" + cut + ")*(pass_lepton_selection==1&&pass_lepton_veto==1&&pass_tau_selection==1&&pass_charge_selection==1&&pass_jet_selection==1&&pass_b_veto==1&&pass_mjj_cut==1&&pass_MET_cut==1)", 
                'incl':"((abs(" + mpdgstr + "_pdgid)==13||abs(" + epdgstr + "_pdgid)==11))*(" + cut + ")*(pass_lepton_selection==1&&pass_lepton_veto==1&&pass_charge_selection==1&&pass_jet_selection==1&&pass_b_veto==1&&pass_tau_veto==1)", 
            }
    cut_tag = "selection"
    if opt.cut != "1.":
        cut_tag = cut_tag + '_AND_' + cutToTag(opt.cut) 
        
else:
    cut_dict = {'muon':"abs(" + mpdgstr + "_pdgid)==13&&(" + cut + ")",
                'electron':"abs(" + epdgstr + "_pdgid)==11&&(" + cut + ")",
                'incl':"(abs(" + mpdgstr + "_pdgid)==13||abs(" + epdgstr + "_pdgid)==11)&&(" + cut + ")",
            }
    cut_tag = cutToTag(opt.cut)

if opt.bdt or opt.ebdt or opt.mubdt:
    bdt_cut = "*(BDT_output"
    if opt.ebdt:
        bdt_cut = bdt_cut + "_ele"
    elif opt.mubdt:
        bdt_cut = bdt_cut + "_mu"

    tresh_bdt = ""
    if opt.bdt:
        tresh_bdt = "-0.425"
    elif opt.ebdt:
        tresh_bdt = "-0.536"
    elif opt.mubdt:
        tresh_bdt = "-0.399"

    sign_bdt = ""
    if opt.bveto or opt.sr:
        sign_bdt = ">"
    elif opt.ttbar or opt.wjets:
        sign_bdt = "<"

    bdt_cut = bdt_cut + sign_bdt + tresh_bdt + ")"

    for k, v in cut_dict.items():
        cut_dict[k] = v + bdt_cut

    if opt.bdt:
        cut_tag = cut_tag + "_BDTcut"
    elif opt.ebdt or opt.mubdt:
        cut_tag = cut_tag + "_lepBDTcut"        


lumi = {'2016': 35.9, "2017": 41.53, "2018": 59.7}

print(cut_tag)

pathplot = plotrepo + lepstr  + "/" # + "_" + str(FRtag) + "/"
pathstack = plotrepo + "stack" + "/" + cut_tag + "/"
#pathstack = plotrepo + "stack_" + str(FRtag) + "/" + cut_tag + "/"

if opt.plot:
    if not os.path.exists(pathplot):
        os.makedirs(pathplot)

if opt.stack:
    if not os.path.exists(plotrepo + 'stack'):
        os.makedirs(plotrepo + 'stack')
    if not os.path.exists(pathstack):
        os.makedirs(pathstack)

if not (opt.wfake=='nofake' or opt.wfake.startswith('incl') or opt.wfake.startswith('sep')):
    raise ValueError('Specify a value for --wfake between nofake, incl*, and sep*')

def mergepart(dataset):
    samples = []
    if hasattr(dataset, 'components'): # How to check whether this exists or not
        samples = [sample for sample in dataset.components]# Method exists and was used.
    else:
        samples.append(dataset)

        # merge files 
        add = "hadd -f " + filerepo + sample.label + "/"  + sample.label + "_merged.root " + filerepo + sample.label + "/"  + sample.label + "_part*.root" 
        print(add)
        os.system(str(add))
        check = ROOT.TFile.Open(filerepo + sample.label + "/"  + sample.label + "_merged.root ")
        print("Number of entries of the file %s are %s" %(filerepo + sample.label + "/"  + sample.label + "_merged.root", (check.Get("events_all")).GetEntries()))
        
        print("-------- ", opt.folder, " --------")
        print("so scem? ", not 'Fake' in opt.folder)
        
        startWFR = folder.startswith('FR')
        isltau = opt.channel=='ltau'
        hasFakeInside = 'Fake' in opt.folder
        
        if isltau and not(startWFR or hasFakeInside):
              
            # insert BDT output value into merged file
            print("Processing events with Tommaso's BDT...")
            file_path = filerepo + sample.label + "/"  + sample.label + "_merged.root"
            file_path_cp = filerepo + sample.label + "/"  + sample.label + "_merged_bu.root"
            os.system("cp " + file_path + " " + file_path_cp)
            #print(file_path)
          
            model_SM_path = opt.model_SM
            model_dim6_path = opt.model_dim6
            model_dim8_path = opt.model_dim8
            #model_mu_path = opt.model_mu
            #model_ele_path = opt.model_ele
            #model_mu_path = opt.model_mu
            #print(model_path)
            #print(model_ele_path)
            #print(model_mu_path)

            # load model 
            file = open(model_SM_path,'rb')
            clf_SM = pickle.load(file)
            file.close()

            file = open(model_dim6_path,'rb')
            clf_dim6 = pickle.load(file)
            file.close()
               
            file = open(model_dim8_path,'rb')
            clf_dim8 = pickle.load(file)
            file.close()
               
            # load model 
            #file = open(model_path,'rb')
            #clf = pickle.load(file)
            #file.close()
            
            #file = open(model_ele_path,'rb')
            #clf_ele = pickle.load(file)
            #file.close()
               
            #file = open(model_mu_path,'rb')
            #clf_mu = pickle.load(file)
            #file.close()
               
            # open root file
            file = uproot.open(file_path)
            tree = file["events_all"]
            df = tree.arrays(library="pd")
            df = df.fillna(0)
               
            '''
            to_drop = ['w_nominal','lepSF[0]', 'lepUp[0]', 'lepDown[0]', 'puSF[0]', 'puUp[0]',
            'puDown[0]', 'PFSF[0]', 'PFUp[0]', 'PFDown[0]', 'q2Up[0]', 'q2Down[0]','w_PDF[0]',
            'SF_Fake[0]', 'tau_vsjet_SF[0]', 'tau_vsele_SF[0]', 'tau_vsmu_SF[0]', 'tau_vsjet_Up[0]', 'tau_vsjet_Down[0]', 'tau_vsele_Up[0]', 'tau_vsele_Down[0]', 'tau_vsmu_Up[0]', 'tau_vsmu_Down[0]',
            'tauSF[0]','tauUp[0]','tauDown[0]','TESSF[0]','TESUp[0]','TESDown[0]','FESSF[0]','FESUp[0]','FESDown[0]',
            'event_SFFake_vsjet2[0]', 'event_SFFake_vsjet4[0]','lepton_SFFake_vsjet2[0]', 'lepton_SFFake_vsjet4[0]', 'tau_SFFake_vsjet2[0]', 'tau_SFFake_vsjet4[0]',
            'tau_DeepTau_WP[0]','tau_DeepTauVsJet_WP[0]', 'tau_DeepTauVsMu_WP[0]','tau_DeepTauVsEle_WP[0]', 
            'HLT_effLumi[0]', 'pass_lepton_selection[0]','pass_tau_selection[0]', 'pass_tau_vsJetWP[0]','pass_jet_selection[0]', 'pass_upToBVeto[0]', 'pass_lepton_iso[0]','pass_lepton_veto[0]', 
            'pass_charge_selection[0]', 'pass_b_veto[0]', 'pass_mjj_cut[0]','pass_MET_cut[0]', 'pass_everyCut[0]', 'nBJets[0]',
            'event_Zeppenfeld[0]','tau_Zeppenfeld[0]','lepton_Zeppenfeld[0]', 
            'lepton_LnTRegion[0]', 'tau_LnTRegion[0]',  'tau_isolation[0]', 'lepton_TightRegion[0]','tau_TightRegion[0]','tau_isPrompt[0]','lepton_isPrompt[0]', 
            'tau_GenMatch[0]',
            'leadjet_CSVv2_b[0]', 'subleadjet_CSVv2_b[0]',] 
            '''



            #X = df.drop(columns=to_drop)
            
            new_columns = []
            for i in df.columns:
                new_columns.append(i.split('[')[0])
            df.columns = new_columns
            
            to_keep = ['lepton_pt',
                       'lepton_eta',
                       'lepton_phi',
                       'lepton_mass',
                       'lepton_pdgid',
                       'lepton_pfRelIso04',
                       'tau_pt',
                       'tau_eta',
                       'tau_phi',
                       'tau_mass',
                       'tau_DecayMode',
                       'tau_DeepTauVsEle_raw',
                       'tau_DeepTauVsMu_raw',
                       'tauleadTk_ptOverTau',
                       'tauleadTk_deltaPhi',
                       'tauleadTk_deltaEta',
                       'tauleadTk_Gamma',
                       'taujet_relpt',
                       'taujet_deltaPhi',
                       'taujet_deltaEta',
                       'taujet_HadGamma',
                       'taujet_EmGamma',
                       'taujet_HEGamma',
                       'leadjet_pt',
                       'leadjet_eta',
                       'leadjet_phi',
                       'leadjet_mass',
                       'leadjet_DeepFlv_b',
                       'leadjet_DeepCSVv2_b',
                       'AK8leadjet_pt',
                       'AK8leadjet_eta',
                       'AK8leadjet_phi',
                       'AK8leadjet_mass',
                       'AK8leadjet_tau21',
                       'AK8leadjet_tau32',
                       'AK8leadjet_tau43',
                       'leadjet_dRAK48',
                       'subleadjet_pt',
                       'subleadjet_eta',
                       'subleadjet_phi',
                       'subleadjet_mass',
                       'subleadjet_DeepFlv_b',
                       'subleadjet_DeepCSVv2_b',
                       'AK8subleadjet_pt',
                       'AK8subleadjet_eta',
                       'AK8subleadjet_phi',
                       'AK8subleadjet_mass',
                       'AK8subleadjet_tau21',
                       'AK8subleadjet_tau32',
                       'AK8subleadjet_tau43',
                       'subleadjet_dRAK48',
                       'nJets',
                       'MET_pt',
                       'MET_phi',
                       'm_jj',
                       'mT_lep_MET',
                       'mT_tau_MET',
                       'mT_leptau_MET',
                       'm_taulep',
                       'm_jjtau',
                       'm_jjtaulep',
                       'deltaPhi_jj',
                       'deltaPhi_taulep',
                       'deltaPhi_tauj1',
                       'deltaPhi_tauj2',
                       'deltaPhi_lepj1',
                       'deltaPhi_lepj2',
                       'deltaEta_jj',
                       'deltaEta_taulep',
                       'deltaEta_tauj1',
                       'deltaEta_tauj2',
                       'deltaEta_lepj1',
                       'deltaEta_lepj2',
                       'deltaTheta_jj',
                       'deltaTheta_taulep',
                       'deltaTheta_tauj1',
                       'deltaTheta_tauj2',
                       'deltaTheta_lepj1',
                       'deltaTheta_lepj2',
                       'ptRel_jj',
                       'ptRel_taulep',
                       'ptRel_tauj1',
                       'ptRel_tauj2',
                       'ptRel_lepj1',
                       'ptRel_lepj2',
                       'lepton_Zeppenfeld_over_deltaEta_jj',
                       'tau_Zeppenfeld_over_deltaEta_jj',
                       'event_Zeppenfeld_over_deltaEta_jj',
                       'event_RT',
            ]
            
            X = df[to_keep].to_numpy()

            '''
            X = df[['lepton_pt', 'lepton_eta', 'lepton_phi', 'lepton_mass', 'lepton_pdgid',
            'lepton_pfRelIso04', 'tau_pt', 'tau_eta', 'tau_phi', 'tau_mass',
            'tau_DeepTauVsEle_raw', 'tau_DeepTauVsMu_raw', 'leadjet_pt',
            'leadjet_eta', 'leadjet_phi', 'leadjet_mass', 'leadjet_CSVv2_b',
            'leadjet_DeepFlv_b', 'leadjet_DeepCSVv2_b', 'AK8leadjet_pt',
            'AK8leadjet_eta', 'AK8leadjet_phi', 'AK8leadjet_mass',
            'AK8leadjet_tau21', 'AK8leadjet_tau32', 'AK8leadjet_tau43',
            'leadjet_dRAK48', 'subleadjet_pt', 'subleadjet_eta', 'subleadjet_phi',
            'subleadjet_mass', 'subleadjet_CSVv2_b', 'subleadjet_DeepFlv_b',
            'subleadjet_DeepCSVv2_b', 'AK8subleadjet_pt', 'AK8subleadjet_eta',
            'AK8subleadjet_phi', 'AK8subleadjet_mass', 'AK8subleadjet_tau21',
            'AK8subleadjet_tau32', 'AK8subleadjet_tau43', 'subleadjet_dRAK48',
            'nJets', 'MET_pt', 'MET_phi', 'm_jj', 'mT_lep_MET', 'mT_tau_MET',
            'mT_leptau_MET', 'deltaPhi_jj', 'deltaPhi_taulep', 'deltaPhi_tauj1',
            'deltaPhi_tauj2', 'deltaPhi_lepj1', 'deltaPhi_lepj2', 'deltaEta_jj',
            'lepton_Zeppenfeld', 'tau_Zeppenfeld', 'event_Zeppenfeld',
            'pass_mjj_cut', 'pass_MET_cut', 'pass_everyCut']].to_numpy() 
            '''

            # update root file with BDT branch
            BDT_output_SM_array = clf_SM.predict_proba(X)[:,1]
            BDT_output_dim6_array = clf_dim6.predict_proba(X)[:,1]
            BDT_output_dim8_array = clf_dim8.predict_proba(X)[:,1]

            #BDT_output_SM_array = clf_SM.decision_function(X)
            #BDT_output_dim6_array = clf_dim6.decision_function(X)
            #BDT_output_dim8_array = clf_dim8.decision_function(X)

            myfile = ROOT.TFile(file_path, 'update')
            mytree = myfile.Get("events_all")
            listOfNewBranches = []
            BDT_output_SM   = array('d', [0.5] )
            BDT_output_dim6   = array('d', [0.5] )
            BDT_output_dim8   = array('d', [0.5] )
            #BDT_output   = array('d', [0.5] )
            #BDT_output_ele   = array('d', [0.5] )
            #BDT_output_mu   = array('d', [0.5] )
            listOfNewBranches.append(mytree.Branch("BDT_output_SM", BDT_output_SM, "BDT_output_SM/D") )
            listOfNewBranches.append(mytree.Branch("BDT_output_dim6", BDT_output_dim6, "BDT_output_dim6/D") )
            listOfNewBranches.append(mytree.Branch("BDT_output_dim8", BDT_output_dim8, "BDT_output_dim8/D") )
            #listOfNewBranches.append(mytree.Branch("BDT_output", BDT_output, "BDT_output/D") )
            #listOfNewBranches.append(mytree.Branch("BDT_output_ele", BDT_output_ele, "BDT_output_ele/D") )
            #listOfNewBranches.append(mytree.Branch("BDT_output_mu", BDT_output_mu, "BDT_output_mu/D") )
            numOfEvents = mytree.GetEntries()
            for n in range(numOfEvents):
                BDT_output_SM[0] = BDT_output_SM_array[n]
                BDT_output_dim6[0] = BDT_output_dim6_array[n]
                BDT_output_dim8[0] = BDT_output_dim8_array[n]
                #BDT_output[0] = BDT_output_array[n]
                #BDT_output_ele[0] = BDT_output_ele_array[n]
                #BDT_output_mu[0] = BDT_output_mu_array[n]
                #if n%1000 == 0:
                    #print(BDT_output[0])
                mytree.GetEntry(n)
                for newBranch in sorted(listOfNewBranches):
                    newBranch.Fill()
            mytree.Write("", ROOT.TFile.kOverwrite)
            myfile.Close()       

def mergetree(sample):
    if not os.path.exists(filerepo + sample.label):
        os.makedirs(filerepo + sample.label)
    if hasattr(sample, 'components'): # How to check whether this exists or not
        add = "hadd -f " + filerepo + sample.label + "/"  + sample.label + ".root" 
        for comp in sample.components:
            add+= " " + filerepo + comp.label + "/"  + comp.label + ".root" 
        print(add)
        os.system(str(add))

def lumi_writer(dataset, lumi):
    samples = []
    if hasattr(dataset, 'components'): # How to check whether this exists or not
        samples = [sample for sample in dataset.components]# Method exists and was used.
    else:
        samples.append(dataset)
    #print(samples)
    for sample in samples:
        if not ('Data' in sample.label):# or 'TT_dilep' in sample.label):
            infile =  ROOT.TFile.Open(filerepo + sample.label + "/"  + sample.label + "_merged.root")
            isthere_gen = bool(infile.GetListOfKeys().Contains("h_genweight"))
            isthere_pdf = bool(infile.GetListOfKeys().Contains("h_PDFweight"))
            tree = infile.Get('events_all')
            tree.SetBranchStatus('w_nominal', 0)
            tree.SetBranchStatus('w_PDF', 0)
            outfile =  ROOT.TFile.Open(filerepo + sample.label + "/"  + sample.label + ".root","RECREATE")
            tree_new = tree.CloneTree(0)
            print("Getting the histos from %s" %(infile))
            h_genw_tmp = ROOT.TH1F(infile.Get("h_genweight"))
            #print("h_genweight first bin content is %f and h_PDFweight has %f bins" %(h_genw_tmp.GetBinContent(1), nbins))
            w_nom = array('f', [0.]) 
            tree_new.Branch('w_nominal', w_nom, 'w_nominal/F')
            tree.SetBranchStatus('w_nominal', 1)
            if isthere_pdf:# ("WZ" in sample.label):
                h_pdfw_tmp = ROOT.TH1F(infile.Get("h_PDFweight"))
                nbins = h_pdfw_tmp.GetXaxis().GetNbins()
                #print(nbins)
                w_PDF = array('f', [0.]*nbins)
            else:
                w_PDF = array('f', [1.])
                    
            print('len w_PDF:', len(w_PDF))
            tree_new.Branch('w_PDF', w_PDF, 'w_PDF[' + str(int(len(w_PDF))) + ']/F')
               
            for event in range(0, tree.GetEntries()):
                tree.GetEntry(event)
                if event%10000==1:
                    #print("Processing event %s     complete %s percent" %(event, 100*event/tree.GetEntries()))
                    sys.stdout.write("\rProcessing event {}     complete {} percent".format(event, 100*event/tree.GetEntries()))
                w_nom[0] = tree.w_nominal * sample.sigma * tree.HLT_effLumi * 1000./float(h_genw_tmp.GetBinContent(1))
                if isthere_pdf: #not ("WZ" in sample.label):
                    for i in range(1, nbins):
                        w_PDF[i] = h_pdfw_tmp.GetBinContent(i+1)/h_genw_tmp.GetBinContent(2) 
                tree_new.Fill()
            tree_new.Write()
            outfile.Close()
            print('\n')
        else:
            os.popen("mv " + filerepo + sample.label + "/"  + sample.label + "_merged.root " + filerepo + sample.label + "/"  + sample.label + ".root")


def plot(lep, reg, variable, sample, cut_tag, syst=""):
     print("in plotf")
     IsDim8 = False
     if sample.label.startswith("VBS_SSWW_F"):
         IsDim8 = True
     print("IsDim8?:", IsDim8)
     print("in plot function")
     print("plotting ", variable._name, " for sample ", sample.label, " with cut ", cut_tag, "with FR", FRtag)#, " ", syst,
     ROOT.TH1.SetDefaultSumw2()
     cutbase = variable._taglio
     cut = ''

     print("count? ", opt.count)
     if opt.count:
          countf = open(pathplot + 'countings/' + cut_tag + "/" + variable._name + ".txt", "a")
          countf.write(sample.label)
          countf.write("\nBin\tContent\tError")

     if opt.channel=="ltau":
         l1fstr = "lepton"
         l2fstr = "tau"
     elif opt.channel=="emu":
         l1fstr = "electron"
         l2fstr = "muon"

     if 'Fake' in str(sample.label):
          if not opt.folder.startswith('CTHT'):
               f1 = ROOT.TFile.Open(filerepo + sample.components[0].label + "/"  + sample.components[0].label + ".root")
          else:
               f1 = ROOT.TFile.Open(filerepo + sample.components[1].label + "/"  + sample.components[1].label + ".root")
          if str(sample.label).startswith('FakeEle_') or str(sample.label).startswith('FakeMu_'):
               cut = cutbase + "*(" + l1fstr + "_LnTRegion==1||" + l2fstr + "_LnTRegion==1)*(event_SFFake_" + str(FRtag)  + ")*(event_SFFake_" + str(FRtag)  + ">-1.)"
          elif str(sample.label).startswith('FakeElePromptTau') or str(sample.label).startswith('FakeMuPromptTau'):
               cut = cutbase + "*(" + l1fstr + "_LnTRegion==1&&" + l2fstr + "_LnTRegion==0)*(event_SFFake_" + str(FRtag)  + ")*(event_SFFake_" + str(FRtag)  + ">-1.)"
          elif str(sample.label).startswith('PromptEleFakeTau') or str(sample.label).startswith('PromptMuFakeTau'):
               cut = cutbase + "*(" + l1fstr + "_LnTRegion==0&&" + l2fstr + "_LnTRegion==1)*(event_SFFake_" + str(FRtag)  + ")*(event_SFFake_" + str(FRtag)  + ">-1.)"
          elif str(sample.label).startswith('FakeEleFakeTau') or str(sample.label).startswith('FakeMuFakeTau'):
               cut = cutbase + "*(" + l1fstr + "_LnTRegion==1&&" + l2fstr + "_LnTRegion==1)*(event_SFFake_" + str(FRtag)  + ")*(event_SFFake_" + str(FRtag)  + ">-1.)"

     else:
          f1 = ROOT.TFile.Open(filerepo + sample.label + "/"  + sample.label + ".root")
          cut = cutbase + "*(" + l1fstr + "_TightRegion==1&&" + l2fstr + "_TightRegion==1)"

     if not ('Fake' in str(sample.label) or 'Data' in str(sample.label)):
        cut = cut + "*((" + l1fstr + "_isPrompt==1||" + l1fstr + "_isPrompt==15)&&" + l2fstr + "_isPrompt==5)"

     nbins = variable._nbins
     histoname = "h_" + variable._name + "_" + cut_tag

     #print(variable._iscustom)
     if not variable._iscustom:
          h1 = ROOT.TH1F(histoname, variable._name + "_" + reg, variable._nbins, variable._xmin, variable._xmax)
     else:
          h1 = ROOT.TH1F(histoname, variable._name + "_" + reg, variable._nbins, variable._xmin)

     h1.Sumw2()

     if IsDim8:
         cut = "(w_dim8[0])*" + cut

     '''
     else:
          if(syst==""):
            taglio = variable._taglio+"*w_nominal"
            foutput = "Plot/"+lep+"/"+channel+"_"+lep+".root"
        elif(syst.startswith("jer") or syst.startswith("jes")):
            taglio = variable._taglio+"*w_nominal"
            treename = "events_"+reg+"_"+syst
            foutput = "Plot/"+lep+"/"+channel+"_"+lep+"_"+syst+".root"
            if(channel == "WJets_ext" and lep.startswith("electron")):
                taglio = variable._taglio+"*w_nominal*(abs(w)<10)"
     '''
     vartoproject = ''
     if variable._name == 'countings':
         print("name", variable._name, "histname:", h1.GetName())
         vartoproject = 'm_jj'
         #f1.Get("events_all").Project(histoname,"m_jj",cut)
     elif variable._name.startswith("lepBDT_"):
         vartoproject = "BDT_output_"
         if lep == 'muon':
             vartoproject = vartoproject + "mu"
         elif lep == 'electron':
             vartoproject = vartoproject + "ele"
         elif lep == 'incl':
             vartoproject = "BDT_output_ele*(abs(lepton_pdgid)==11)+BDT_output_mu*(abs(lepton_pdgid)==13)"
     else:
         vartoproject = variable._name

     #if not variable._name == 'countings':
     if 'MC' in variable._name:
         cut = cut + "*(" + str(vartoproject) + "!-100.)"
     else:
         cut = cut + "*(" + str(vartoproject) + ">-10.)"
     #else:
         #cut = cut + '*(1.)'
     #if "WpWpJJ_EWK" in sample.label or 'VBS_SSWW' in sample.label:
          #cut = cut + "*10."

     print('cut:', str(cut))
     foutput = pathplot + sample.label + "_" + lep + ".root"

     f1.Get("events_all").Project(histoname,vartoproject,cut)

     h1.SetBinContent(1, h1.GetBinContent(0) + h1.GetBinContent(1))
     h1.SetBinError(1, math.sqrt(pow(h1.GetBinError(0),2) + pow(h1.GetBinError(1),2)))
     #if not (opt.blinded and (variable._name == 'MET_pt' or variable._name == 'm_jj')):
     h1.SetBinContent(nbins, h1.GetBinContent(nbins) + h1.GetBinContent(nbins+1))
     h1.SetBinError(nbins, math.sqrt(pow(h1.GetBinError(nbins),2) + pow(h1.GetBinError(nbins+1),2)))


     for bidx in range(nbins):          
          bidx_l = bidx + 1
          if str(sample.label).startswith('Fake') or str(sample.label).startswith('Prompt'):
               h1.SetBinError(bidx_l, 0.3*h1.GetBinContent(bidx_l))

          if not opt.count:
               continue

          minedge = str(round(h1.GetBinLowEdge(bidx_l), 3))
          maxedge = str(round(h1.GetBinLowEdge(bidx_l) + h1.GetBinWidth(bidx_l), 3))
          bincont = str(round(h1.GetBinContent(bidx_l), 3))
          binerrcont = str(round(h1.GetBinError(bidx_l), 3))

          countf.write("\n[" + minedge + ", " + maxedge +")\t" + bincont + "\t" + binerrcont)

     print("int:", h1.Integral())
     #print(h1.Integral())
     for i in range(0, nbins+1):
          content = h1.GetBinContent(i)
          if(content<0.):
               h1.SetBinContent(i, 0.)
     
     fout = ROOT.TFile.Open(foutput, "UPDATE")
     fout.cd()
     h1.Write()
     fout.Close()
     f1.Close()

     if opt.count:
          countf.write("\n\n")
          countf.close()

def makestack(lep_, reg_, variabile_, samples_, cut_tag_, syst_, lumi):
     #os.system('set LD_PRELOAD=libtcmalloc.so')

    if reg_ == 'ltau':
        if str(lep_).strip('[]') == "muon":
            lep_tag = "#mu+"
        elif str(lep_).strip('[]') == "electron":
            lep_tag = "e+"
        cmsreg = reg_.replace("ltau", "#tau_{h}")
    else:
        lep_tag = "e+#mu"
        cmsreg = ""

    cmsreg = lep_tag + cmsreg 
    
    blind = False
    infile = {}
    histo = []
    tmp = ROOT.TH1F()
    h = ROOT.TH1F()
    if not variabile_._iscustom:
        hdata = ROOT.TH1F('h','h', variabile_._nbins, variabile_._xmin, variabile_._xmax)
    else:
        hdata = ROOT.TH1F('h','h', variabile_._nbins, variabile_._xmin)
    h_sig = []
    h_err = ROOT.TH1F()
    h_bkg_err = ROOT.TH1F()
    print("Variabile:", variabile_._name)
    ROOT.gROOT.SetStyle('Plain')
    ROOT.gStyle.SetPalette(1)
    ROOT.gStyle.SetOptStat(0)
    ROOT.TH1.SetDefaultSumw2()
    if(cut_tag_ == ""):
        histoname = "h_" + variabile_._name
        stackname = "stack_" + reg_ + "_" + variabile_._name
        canvasname = "stack_" + reg_ + "_" + variabile_._name + "_" + lep_ + "_" + str(samples_[0].year)
    else:
        histoname = "h_" + variabile_._name + "_" + cut_tag_
        stackname = "stack_" + reg_ + "_" + variabile_._name + "_" + cut_tag_
        canvasname = "stack_" + reg_ + "_" + variabile_._name+ "_" + cut_tag_ + "_" + lep_ + "_" + str(samples_[0].year)
    if opt.wfake != 'nofake':
        stackname += "_wFakes_" + str(opt.wfake.split('_')[0])
        canvasname += "_wFakes_" + str(opt.wfake.split('_')[0])
    if opt.sr:
        blind = True
    stack = ROOT.THStack(stackname, variabile_._name)
    leg_stack = ROOT.TLegend(0.32,0.58,0.93,0.87)
    signal = False

    #print(samples_)
    for s in samples_:
        if opt.wfake != 'nofake':
            if s.label.startswith('WJets') or s.label.startswith('QCD') or s.label.startswith('DY') or s.label.startswith('TT_'):
                continue
            elif 'Fake' in s.label:
                if opt.wfake.startswith('incl') and not (s.label.startswith('FakeEle_') or s.label.startswith('FakeMu_')):
                    continue
                elif opt.wfake.startswith('sep') and (s.label.startswith('FakeEle_') or s.label.startswith('FakeMu_')):
                    continue
        else:
            if s.label.startswith('Fake'):
                continue
        if('WpWpJJ_EWK' in s.label or 'VBS_SSWW' in s.label) and not opt.signal:
            signal = True
            #print(s.label)
        if(syst_ == ""):
            #outfile = plotrepo + "stack_" + str(lep_).strip('[]') + ".root"
            infile[s.label] = ROOT.TFile.Open(pathplot + s.label + "_" + lep + ".root")

        else:
            #outfile = plotrepo + "stack_"+syst_+"_"+str(lep_).strip('[]')+".root"
            infile[s.label] = ROOT.TFile.Open(pathplot + s.label + "_" + lep + "_" + syst_ + ".root")
    i = 0

    for s in samples_:
        if opt.wfake != 'nofake':
            if s.label.startswith('WJets') or s.label.startswith('QCD') or s.label.startswith('DY') or s.label.startswith('TT_'):
                continue
            elif 'Fake' in s.label:
                if opt.wfake.startswith('incl') and not (s.label.startswith('FakeEle_') or s.label.startswith('FakeMu_')):
                    continue
                elif opt.wfake.startswith('sep') and (s.label.startswith('FakeEle_') or s.label.startswith('FakeMu_')):
                    continue

        else:
            if s.label.startswith('Fake'):# or s.label.startswith('QCD'):
                continue
          
        infile[s.label].cd()
        print("opening file: ", infile[s.label].GetName())
        if('Data' in s.label):
            if ("GenPart" in variabile_._name) or ("MC_" in variabile_._name):
                continue
            if 'DataHT' in s.label or 'DataMET' in s.label:
                continue

        tmp = (ROOT.TH1F)(infile[s.label].Get(histoname))
        tmp.SetLineColor(ROOT.kBlack)
        tmp.SetName(s.leglabel)
        if('Data' in s.label):
            if ("GenPart" in variabile_._name) or ("MC_" in variabile_._name):
                continue
            hdata.Add(ROOT.TH1F(tmp.Clone("")))
            hdata.SetMarkerStyle(20)
            hdata.SetMarkerSize(0.9)
            if(i == 0 and not blind): # trick to add Data flag to legend only once
                leg_stack.AddEntry(hdata, "Data", "ep")
            i += 1
        elif('WpWpJJ_EWK' in s.label or 'VBS_SSWW' in s.label) and not opt.signal:
            #tmp.SetLineStyle(9)
            if opt.tostack:
                tmp.SetLineColor(s.color)
                tmp.SetLineWidth(2)
            else:
                tmp.SetLineColor(s.color)
                tmp.SetLineWidth(2)
            #tmp.SetLineWidth(3)
            tmp.SetMarkerSize(0.)
            tmp.SetMarkerColor(s.color)
            h_sig.append(ROOT.TH1F(tmp.Clone("")))
            tmp.SetOption("HIST SAME")
        else:
            tmp.SetOption("HIST SAME")
            tmp.SetTitle("")
            if opt.tostack:
                tmp.SetFillColor(s.color)
                tmp.SetLineColor(s.color)
            else:
                tmp.SetLineColor(s.color)
            histo.append(tmp.Clone(""))
            stack.Add(tmp.Clone(""))
        tmp.Reset("ICES")

    for hist in reversed(histo):
        if not ('Data' in hist.GetName()):
            leg_stack.AddEntry(hist, hist.GetName(), "f")
    #style options
    print("Is it blind? " + str(blind))
    leg_stack.SetNColumns(2)
    leg_stack.SetFillColor(0)
    leg_stack.SetFillStyle(0)
    leg_stack.SetTextFont(42)
    leg_stack.SetBorderSize(0)
    leg_stack.SetTextSize(0.035)
    c1 = ROOT.TCanvas(canvasname,"c1",50,50,700,600)
    c1.SetFillColor(0)
    c1.SetBorderMode(0)
    c1.SetFrameFillStyle(0)
    c1.SetFrameBorderMode(0)
    c1.SetLeftMargin( 0.12 )
    c1.SetRightMargin( 0.9 )
    c1.SetTopMargin( 1 )
    c1.SetBottomMargin(-1)
    c1.SetTickx(1)
    c1.SetTicky(1)
    c1.cd()
    
    pad1= ROOT.TPad("pad1", "pad1", 0, 0.31 , 1, 1)
    pad1.SetTopMargin(0.1)
    pad1.SetBottomMargin(0.02)
    pad1.SetLeftMargin(0.12)
    pad1.SetRightMargin(0.05)
    pad1.SetBorderMode(0)
    pad1.SetTickx(1)
    pad1.SetTicky(1)
    pad1.Draw()
    pad1.cd()
    if not blind:
        maximum = max(stack.GetMaximum(),hdata.GetMaximum())
    else:
        maximum = stack.GetMaximum()
    logscale = True # False #
    if(logscale):
        pad1.SetLogy()
        stack.SetMaximum(maximum*10000)
    else:
        stack.SetMaximum(maximum*1.6)
    stack.SetMinimum(0.01)
    if opt.tostack:
        stack.Draw("HIST")
    else:
        stack.Draw("HIST NOSTACK")
    if not variabile_._iscustom:
        step = float(variabile_._xmax - variabile_._xmin)/float(variabile_._nbins)
        #print(str(step))
        if "GeV" in variabile_._title:
            if step.is_integer():
                ytitle = "Events/ %.0f GeV" %step
            else:
                ytitle = "Events / %.2f GeV" %step
        else:
            if step.is_integer():
                ytitle = "Events / %.0f units" %step
            else:
                ytitle = "Events / %.2f units" %step
    else:
        if "GeV" in variabile_._title:
            ytitle = "Events / GeV"
        else:
            ytitle = "Events / a.u"
     
    print(stack)
    stack.GetYaxis().SetTitle(ytitle)
    stack.GetYaxis().SetTitleFont(42)
    stack.GetXaxis().SetLabelOffset(1.8)
    stack.GetYaxis().SetTitleOffset(0.85)
    stack.GetXaxis().SetLabelSize(0.15)
    stack.GetYaxis().SetLabelSize(0.07)
    stack.GetYaxis().SetTitleSize(0.07)
    stack.SetTitle("")
    if(signal):
        for hsig in h_sig:
            #hsig.Scale(1000)
            hsig.Draw("hist same")
            leg_stack.AddEntry(hsig, hsig.GetName(), "l")
    h_err = stack.GetStack().Last().Clone("h_err")
    h_err.SetLineWidth(100)
    h_err.SetFillStyle(3154)
    h_err.SetMarkerSize(0)
    h_err.SetFillColor(ROOT.kGray+2)
    h_err.Draw("e2same0")
    leg_stack.AddEntry(h_err, "Stat. Unc.", "f")

    if not blind: 
        print(hdata.Integral())
        hdata.Draw("eSAMEpx0")
    else:
        hdata = stack.GetStack().Last().Clone("h_data")
    leg_stack.Draw("same")

    CMS_lumi.writeExtraText = 1
    CMS_lumi.extraText = ""
         
    print("lep_tag: ", lep_tag)
    lumi_sqrtS = "%s fb^{-1}  (13 TeV)"%(lumi)
    
    iPeriod = 0
    iPos = 11
    CMS_lumi(pad1, lumi_sqrtS, iPos, str(cmsreg))
    hratio = stack.GetStack().Last()
     
    c1.cd()
    pad2= ROOT.TPad("pad2", "pad2", 0, 0.01 , 1, 0.30)
    pad2.SetTopMargin(0.05)
    pad2.SetBottomMargin(0.45)
    pad2.SetLeftMargin(0.12)
    pad2.SetRightMargin(0.05)
    ROOT.gStyle.SetHatchesSpacing(2)
    ROOT.gStyle.SetHatchesLineWidth(2)
    c1.cd()
    pad2.Draw()
    pad2.cd()
    ratio = hdata.Clone("ratio")
    ratio.SetLineColor(ROOT.kBlack)
    ratio.SetMaximum(10)
    ratio.SetMinimum(0)
    ratio.Sumw2()
    ratio.SetStats(0)
    
    ratio.Divide(hratio)
    ratio.SetMarkerStyle(20)
    ratio.SetMarkerSize(0.9)
    ratio.Draw("epx0e0")
    ratio.SetTitle("")
    
    h_bkg_err = hratio.Clone("h_err")
    h_bkg_err.Reset()
    h_bkg_err.Sumw2()
    for i in range(1,hratio.GetNbinsX()+1):
        h_bkg_err.SetBinContent(i,1)
        if(hratio.GetBinContent(i)):
            h_bkg_err.SetBinError(i, (hratio.GetBinError(i)/hratio.GetBinContent(i)))
        else:
            h_bkg_err.SetBinError(i, 10^(-99))
    h_bkg_err.SetLineWidth(100)
    
    h_bkg_err.SetMarkerSize(0)
    h_bkg_err.SetFillColor(ROOT.kGray+1)
    #if not opt.tostack:
    h_bkg_err.Draw("e20same")
     
    if not variabile_._iscustom:
        xmin = variabile_._xmin
    else:
        xmin = variabile_._xmin[0]
    f1 = ROOT.TLine(xmin, 1., variabile_._xmax,1.)
    f1.SetLineColor(ROOT.kBlack)
    f1.SetLineStyle(ROOT.kDashed)
    f1.Draw("same")
     
    ratio.GetYaxis().SetTitle("Data / Bkg")
    ratio.GetYaxis().SetNdivisions(503)
    ratio.GetXaxis().SetLabelFont(42)
    ratio.GetYaxis().SetLabelFont(42)
    ratio.GetXaxis().SetTitleFont(42)
    ratio.GetYaxis().SetTitleFont(42)
    ratio.GetXaxis().SetTitleOffset(1.1)
    ratio.GetYaxis().SetTitleOffset(0.35)
    ratio.GetXaxis().SetLabelSize(0.15)
    ratio.GetYaxis().SetLabelSize(0.15)
    ratio.GetXaxis().SetTitleSize(0.16)
    ratio.GetYaxis().SetTitleSize(0.16)
    ratio.GetYaxis().SetRangeUser(0,1.5)
    ratio.GetXaxis().SetTitle(variabile_._title)
    ratio.GetXaxis().SetLabelOffset(0.04)
    ratio.GetYaxis().SetLabelOffset(0.02)
    ratio.Draw("epx0e0same")

    c1.cd()
    #ROOT.TGaxis.SetMaxDigits(3)
    c1.RedrawAxis()
    pad2.RedrawAxis()
    c1.Update()
    #c1.Print("stack/"+canvasname+".pdf")
    c1.Print(pathstack + canvasname + ".png")
    del histo
    tmp.Delete()
    h.Delete()
    del tmp
    del h
    del h_sig
    h_err.Delete()
    del h_err
    h_bkg_err.Delete()
    del h_bkg_err
    hratio.Delete()
    del hratio
    stack.Delete()
    del stack
    pad1.Delete()
    del pad1
    pad2.Delete()
    del pad2
    c1.Delete()
    del c1
    for kf in infile.keys():
        #infile[s.label].Close()
        infile[kf].Close()
        #infile[s.label].Delete()
        infile[kf].Delete()
    #os.system('set LD_PRELOAD=libtcmalloc.so')

leptons = opt.lep.split(',')

#dataset_dict = {'2016':[],'2017':[],'2018':[]}
dataset_dict = {'2017':[],'2018':[]}

#print(class_list)

if(opt.dat != 'all'):
     print(opt.dat)
     if not(opt.dat in sample_dict.keys()):
          print("dataset not found!")
          print(sample_dict.keys())
     #print(opt.dat)
     if 'DataMET' in str(opt.dat):
          raise Exception("Not interesting dataset")
     elif not opt.folder.startswith('CTHT') and 'DataHT' in str(opt.dat) and (opt.plot or opt.stack):
          raise Exception("Not interesting dataset")
     dataset_names = opt.dat.strip('[]').split(',')
     #print(dataset_names)
     samples = []
     [samples.append(sample_dict[dataset_name]) for dataset_name in dataset_names]
     [dataset_dict[str(sample.year)].append(sample) for sample in samples]
else:
     for v in class_list:
          #print(v)
          if opt.signal and not ('WpWpJJ_EWK' in v.label or 'VBS_SSWW' in v.label):
               continue
          if 'DataMET' in v.label:
               continue
          elif ('DataHT' in v.label and not opt.folder.startswith('CTHT')):
               continue
          elif (opt.folder.startswith('CTHT') and ('DataEle' in v.label or 'DataMu' in v.label or 'QCD' in v.label)):
               continue
          elif 'electron' in leptons:
               if 'DataMu' in v.label or 'FakeMu' in v.label or 'PromptMu' in v.label:
                    continue
          elif 'muon' in leptons:
               if 'DataEle' in v.label or 'FakeEle' in v.label or 'PromptEle' in v.label:
                    continue
          dataset_dict[str(v.year)].append(v)

for v in dataset_dict.values():
     print([o.label for o in v])
#print(dataset_dict.keys())

years = []
if(opt.year!='all'):
     years = opt.year.strip('[]').split(',')
else:
     years = ['2016','2017','2018']

for year in years:
    for sample in dataset_dict[year]:
          if(opt.merpart):
               mergepart(sample)
          if(opt.lumi):
               lumi_writer(sample, lumi[year])
          if(opt.mertree):
               mergetree(sample)

print("\nStarting")
for year in years:
    print(year)
    for lep in leptons:
        print(lep)
        dataset_new = dataset_dict[year]
        print([h.label for h in dataset_new])
        #dataset_new.remove(sample_dict['DataMET_'+str(year)])
        if lep == 'muon' and sample_dict['DataEle_'+str(year)] in dataset_new:
            dataset_new.remove(sample_dict['DataEle_'+str(year)])
            dataset_new.remove(sample_dict['FakeEle_'+str(year)])
        elif lep == 'electron' and sample_dict['DataMu_'+str(year)] in dataset_new:
            dataset_new.remove(sample_dict['DataMu_'+str(year)])
            dataset_new.remove(sample_dict['FakeMu_'+str(year)])

        variables = []
        
        lep1 = ["", ""]
        lep2 = ["", ""]
        lep12 = ["", ""]
        
        if opt.channel == "ltau":
            lep1 = ["lepton", "lepton"]
            lep2 = ["tau", "#tau"]
            lep12 = ["taulep", "#tau l"]
        
        elif opt.channel == "emu":
            lep1 = ["electron", "e"]
            lep2 = ["muon", "#mu"]
            lep12 = ["electronmuon", "e #mu"]
              
        
        if opt.channel == 'ltau':
            wzero = 'w_nominal*PFSF*puSF*lepSF*tau_vsjet_SF*tau_vsele_SF*tau_vsmu_SF'
        elif opt.channel == 'emu':
            wzero = 'w_nominal*PFSF*puSF*lepSF'

        cutbase = cut_dict[lep]

        variables.append(variabile('countings', 'countings', wzero+'*('+cutbase+')', 1, -0.5, 0.5))


        variables.append(variabile('BDT_output_SM', 'SM BDT output', wzero+'*('+cutbase+')', 10, 0., 1.))
        variables.append(variabile('BDT_output_dim6', 'dim6 BDT output', wzero+'*('+cutbase+')', 10, 0., 1.))
        variables.append(variabile('BDT_output_dim8', 'dim8 BDT output', wzero+'*('+cutbase+')', 10, 0., 1.))


        #variables.append(variabile('BDT_output_ele', 'eleBDT output', wzero+'*('+cutbase+')', 8, -2., 2.))
        #variables.append(variabile('BDT_output_mu', '#muBDT output', wzero+'*('+cutbase+')', 8, -2., 2.))
        
        #variables.append(variabile('lepBDT_output', 'lepBDT output', wzero+'*('+cutbase+')', 8, -2., 2.))

        variables.append(variabile(lep1[0] + '_eta', lep1[1] + ' #eta', wzero+'*('+cutbase+')', 20, -5., 5.))


        variables.append(variabile(lep1[0] + '_phi', lep1[1] + ' #phi',  wzero+'*('+cutbase+')', 14, -3.50, 3.50))
        
        
        bin_lepton_pt = array("f", [0., 30., 45., 60., 80., 100., 200., 300., 500.])
        nbin_lepton_pt = len(bin_lepton_pt)-1
        variables.append(variabile(lep1[0] + '_pt',  lep1[1] + ' p_{T} [GeV]',  wzero+'*('+cutbase+')', nbin_lepton_pt, bin_lepton_pt))#30, 1500))
        
        #variables.append(variabile(lep1[0] + '_pdgid', lep1[1] + ' pdgid',  wzero+'*('+cutbase+')', 31, -15.5, 15.5))
        #variables.append(variabile(lep1[0] + '_pfRelIso04', lep1[1] + ' rel iso',  wzero+'*('+cutbase+')', 15, 0, 0.15))
        #variables.append(variabile(lep1[0] + '_Zeppenfeld', lep1[1] + ' Zeppenfeld',  wzero+'*('+cutbase+')', 24, -6, 6))
        #variables.append(variabile('event_Zeppenfeld', 'event Zeppenfeld',  wzero+'*('+cutbase+')', 24, -6, 6))
        variables.append(variabile(lep1[0] + '_Zeppenfeld_over_deltaEta_jj', 'z_{l}',  wzero+'*('+cutbase+')', 12, -1.5, 1.5))
        

        bin_taupt = array("f", [0., 50., 100., 200., 300., 500.])
        nbin_taupt = len(bin_taupt) - 1
        variables.append(variabile(lep2[0] + '_pt',  lep2[1] + ' p_{T} [GeV]',  wzero+'*('+cutbase+')', nbin_taupt, bin_taupt))

        variables.append(variabile(lep2[0] + '_mass',  lep2[1] + ' mass [GeV]',  wzero+'*('+cutbase+')', 20, 0., 2.))

        variables.append(variabile(lep2[0] + '_eta', lep2[1] + ' #eta',  wzero+'*('+cutbase+')', 12, -3., 3.))


        #variables.append(variabile(lep2[0] + '_Zeppenfeld', lep2[1] + ' Zeppenfeld',  wzero+'*('+cutbase+')', 20, -5, 5))
        variables.append(variabile(lep2[0] + '_Zeppenfeld_over_deltaEta_jj', 'z_{#tau}',  wzero+'*('+cutbase+')', 12, -1.5, 1.5))
        variables.append(variabile(lep2[0] + '_phi', lep2[1] + ' #Phi',  wzero+'*('+cutbase+')',  14, -3.50, 3.50))

        if opt.channel == "ltau":
            variables.append(variabile(lep2[0] + '_DecayMode', '#tau decay mode',  wzero+'*('+cutbase+')', 12, -0.5, 11.5))
            
            variables.append(variabile('tauleadTk_ptOverTau',  '#tau LeadTk relative p_{T}',  wzero+'*('+cutbase+')', 10, 0, 1))
            variables.append(variabile('tauleadTk_deltaPhi',  '#tau LeadTk relative #Delta#phi',  wzero+'*('+cutbase+')', 4, -0.5, 0.5))
            variables.append(variabile('tauleadTk_deltaEta',  '#tau LeadTk relative #Delta#eta',  wzero+'*('+cutbase+')', 4, -0.5, 0.5))
            variables.append(variabile('tauleadTk_Gamma',  '#tau LeadTk #Upsilon',  wzero+'*('+cutbase+')', 12, -1., 1.2))
            
            variables.append(variabile('taujet_relpt',  '#tau jet relative p_{T}',  wzero+'*('+cutbase+')', 10, 0.2, 1.2))
            variables.append(variabile('taujet_deltaPhi',  '#tau jet relative #Delta#phi',  wzero+'*('+cutbase+')', 8, -1., 1.))
            variables.append(variabile('taujet_deltaEta',  '#tau jet relative #Delta#eta',  wzero+'*('+cutbase+')', 4, -0.5, 0.5))
            variables.append(variabile('taujet_HadGamma',  '#tau jet #Upsilon',  wzero+'*('+cutbase+')', 12, -1., 1.2))
            #variables.append(variabile('taujet_EmGamma',  '#tau jet em#Gamma',  wzero+'*('+cutbase+')', 16, -1., 3.))
            #variables.append(variabile('taujet_HEGamma',  '#tau jet hem#Gamma',  wzero+'*('+cutbase+')', 16, -1., 3.))
            
            #variables.append(variabile('tau_DeepTauVsEle_raw', '#tau DeepTauVsEle raw',  wzero+'*('+cutbase+')',  10, 0.35, 1.35))
            #variables.append(variabile('tau_DeepTauVsMu_raw', '#tau DeepTauVsMu raw',  wzero+'*('+cutbase+')',  10, 0.2, 1.2))
            #variables.append(variabile('tau_DeepTauVsJet_raw', '#tau DeepTauVsJet raw',  wzero+'*('+cutbase+')',  10, 0., 1.))
            
            #variables.append(variabile('tau_DeepTauVsEle_WP', '#tau DeepTauVsEle WP',  wzero+'*('+cutbase+')',  11, -0.5, 10.5))
            #variables.append(variabile('tau_DeepTauVsMu_WP', '#tau DeepTauVsMu WP',  wzero+'*('+cutbase+')',  11, -0.5, 10.5))
            #variables.append(variabile('tau_DeepTauVsJet_WP', '#tau DeepTauVsJet WP',  wzero+'*('+cutbase+')',  11, -0.5, 10.5))
          
        bin_leadjet_pt = array("f", [0., 100., 200., 300., 400., 600., 1000.])
        nbin_leadjet_pt = len(bin_leadjet_pt)-1
        variables.append(variabile('leadjet_pt',  'Lead jet p_{T} [GeV]',  wzero+'*('+cutbase+')', nbin_leadjet_pt, bin_leadjet_pt))#30, 1500))

        variables.append(variabile('leadjet_eta', 'Lead jet #eta',  wzero+'*('+cutbase+')', 10, -2.5, 2.5))
        variables.append(variabile('leadjet_phi', 'Lead jet #Phi',  wzero+'*('+cutbase+')',  14, -3.50, 3.50))
        '''

        bin_ak8leadjet_pt = array("f", [0., 100., 200., 300., 400., 500., 600., 800., 1200.])
        nbin_ak8leadjet_pt = len(bin_ak8leadjet_pt)-1
        variables.append(variabile('AK8leadjet_pt',  'AK8 Lead jet p_{T} [GeV]',  wzero+'*('+cutbase+')', nbin_ak8leadjet_pt, bin_ak8leadjet_pt))#30, 1500))
        
        bin_ak8leadjet_mass = array("f", [0., 50., 100., 150., 300.])
        nbin_ak8leadjet_mass = len(bin_ak8leadjet_mass)-1
        variables.append(variabile('AK8leadjet_mass',  'AK8 Lead jet mass [GeV]',  wzero+'*('+cutbase+')', nbin_ak8leadjet_mass, bin_ak8leadjet_mass))#30, 1500))
        
        variables.append(variabile('AK8leadjet_eta', 'AK8 Lead jet #eta',  wzero+'*('+cutbase+')', 20, -5., 5.))
        variables.append(variabile('AK8leadjet_phi', 'AK8 Lead jet #Phi',  wzero+'*('+cutbase+')',  14, -3.50, 3.50))
        variables.append(variabile('AK8leadjet_tau21', 'AK8 Lead jet #tau_{21}',  wzero+'*('+cutbase+')',  10, 0., 1.))
        variables.append(variabile('AK8leadjet_tau32', 'AK8 Lead jet #tau_{32}',  wzero+'*('+cutbase+')',  10, 0., 1.))
        variables.append(variabile('AK8leadjet_tau43', 'AK8 Lead jet #tau_{43}',  wzero+'*('+cutbase+')',  10, 0., 1.))
        
        bin_ak8subleadjet_pt = array("f", [0., 100., 200., 300., 400., 500., 600., 800., 1200.])
        nbin_ak8subleadjet_pt = len(bin_ak8subleadjet_pt)-1
        variables.append(variabile('AK8subleadjet_pt',  'AK8 Sublead jet p_{T} [GeV]',  wzero+'*('+cutbase+')', nbin_ak8subleadjet_pt, bin_ak8subleadjet_pt))#30, 1500))
        
        bin_ak8subleadjet_mass = array("f", [0., 50., 100., 150., 300.])#, 500., 600., 700., 800., 1000., 1200., 1400., 1600., 2000.])
        nbin_ak8subleadjet_mass = len(bin_ak8subleadjet_mass)-1
        variables.append(variabile('AK8subleadjet_mass',  'AK8 Sublead jet mass [GeV]',  wzero+'*('+cutbase+')', nbin_ak8subleadjet_mass, bin_ak8subleadjet_mass))#30, 1500))
        
        variables.append(variabile('AK8subleadjet_eta', 'AK8 Sublead jet #eta',  wzero+'*('+cutbase+')', 20, -5., 5.))
        variables.append(variabile('AK8subleadjet_phi', 'AK8 Sublead jet #Phi',  wzero+'*('+cutbase+')',  14, -3.50, 3.50))
        variables.append(variabile('AK8subleadjet_tau21', 'AK8 Sublead jet #tau_{21}',  wzero+'*('+cutbase+')',  10, 0., 1.))
        variables.append(variabile('AK8subleadjet_tau32', 'AK8 Sublead jet #tau_{32}',  wzero+'*('+cutbase+')',  10, 0., 1.))
        variables.append(variabile('AK8subleadjet_tau43', 'AK8 Sublead jet #tau_{43}',  wzero+'*('+cutbase+')',  10, 0., 1.))

        '''
        bin_subleadjet_pt = array("f", [0., 100., 250., 500.])
        nbin_subleadjet_pt = len(bin_subleadjet_pt) - 1
        variables.append(variabile('subleadjet_pt', 'Sublead jet p_{T} [GeV]',  wzero+'*('+cutbase+')', nbin_subleadjet_pt, bin_subleadjet_pt))#40, 30, 1000))
        variables.append(variabile('subleadjet_eta', 'Sublead jet #eta',  wzero+'*('+cutbase+')', 20, -5., 5.))
        variables.append(variabile('subleadjet_phi', 'Sublead jet #Phi',  wzero+'*('+cutbase+')',  14, -3.50, 3.50))
        
        variables.append(variabile('nJets', 'n jets',  wzero+'*('+cutbase+')',  11, -0.5, 10.5))
        variables.append(variabile('nBJets', 'n bjets (DeepJet M)',  wzero+'*('+cutbase+')',  6, -0.5, 5.5))

        if opt.blinded:
            bin_metpt = array("f", [0., 10., 20., 30., 40.])
        else:
            bin_metpt = array("f", [0., 20., 50., 100., 150., 200., 300., 500.])
        nbin_metpt = len(bin_metpt) - 1
        variables.append(variabile('MET_pt', 'p_{T}^{miss} [GeV]',  wzero+'*('+cutbase+')', nbin_metpt, bin_metpt))

        if opt.sr:
            bin_mjj = array("f", [500., 600., 800., 1000., 1200., 2000.])
        else:
            bin_mjj = array("f", [0., 100., 200., 300., 400., 500., 600., 800., 1000., 1200., 2000.])
            #bin_mjj = array("f", [0., 100., 200., 300., 400., 500., 600., 700., 800., 900., 1000., 1100., 1200., 1400., 1600., 2000., 2500., 3500., 4500.])
        nbin_mjj = len(bin_mjj) - 1 
        variables.append(variabile('m_jj', 'invariant mass j_{1} j_{2} [GeV]',  wzero+'*('+cutbase+')', nbin_mjj, bin_mjj))# 20, 500, 2000))

        if not opt.sr:
            bin_invm = array("f", [0., 150., 300., 450., 600., 750., 900., 1200., 1500., 2000.])
        else:
            bin_invm = array("f", [500., 700., 900., 1100., 1500., 2000.])
        nbin_invm = len(bin_invm) - 1 
        variables.append(variabile('m_jj' + lep2[0], 'invariant mass j_{1} j_{2} ' + lep2[1] + ' [GeV]',  wzero+'*('+cutbase+')', nbin_invm, bin_invm))# 20, 500, 2000))
        variables.append(variabile('m_jj' + lep12[0], 'invariant mass j_{1} j_{2} ' + lep12[1] + ' [GeV]',  wzero+'*('+cutbase+')', nbin_invm, bin_invm))# 20, 500, 2000))

        bin_invmtl = array("f", [0., 50., 100., 150., 200., 300., 500.])#, 1000.])
        nbin_invmtl = len(bin_invmtl) - 1 
          
        variables.append(variabile('m_' + lep12[0], 'invariant mass ' + lep12[1] + ' [GeV]',  wzero+'*('+cutbase+')', nbin_invmtl, bin_invmtl))

        bin_m1 = array("f", [0., 150., 300., 500., 1000.])
        nbin_m1 = len(bin_m1) - 1 
        variables.append(variabile('m_1T', 'M_{1T} [GeV]',  wzero+'*('+cutbase+')', nbin_m1, bin_m1))
        variables.append(variabile('m_o1', 'M_{o1} [GeV]',  wzero+'*('+cutbase+')', nbin_m1, bin_m1))

        bin_mTs = array("f", [0., 25., 50., 75., 100., 125., 150., 200., 300., 500.])
        nbin_mTs = len(bin_mTs) - 1

        variables.append(variabile('mT_lep_MET', 'M_{T}(lep, MET) [GeV]',  wzero+'*('+cutbase+')', nbin_mTs, bin_mTs))
        variables.append(variabile('mT_tau_MET', 'M_{T}( ' + lep2[1] + ', MET) [GeV]',  wzero+'*('+cutbase+')', nbin_mTs, bin_mTs))
        if opt.channel == "ltau":
            variables.append(variabile('mT_leptau_MET', 'M_{T}(l,  ' + lep2[1] + ', MET) [GeV]',  wzero+'*('+cutbase+')', nbin_mTs, bin_mTs))
        elif opt.channel == "emu":
            variables.append(variabile('mT_' + lep12[0] + '_MET', 'M_{T}(' + lep12[1] + ', MET) [GeV]',  wzero+'*('+cutbase+')', nbin_mTs, bin_mTs))


        #bin_deltaeta_jj = array("f", [0., 0.5, 1., 1.5, 2., 2.5, 3., 3.5, 4., 4.5, 5., 5.5, 6., 6.5, 7., 8., 9., 10.])
        #nbin_deltaeta_jj = len(bin_deltaeta_jj) - 1
        variables.append(variabile('deltaEta_jj', '#Delta #eta_{jj}',  wzero+'*('+cutbase+')', 32, -8., 8.))#nbin_deltaeta_jj, bin_deltaeta_jj))#


        variables.append(variabile('deltaPhi_jj', '#Delta #phi_{jj}',  wzero+'*('+cutbase+')',  16, -4., 4.))
        variables.append(variabile('deltaPhi_' + lep12[0], '#Delta #phi_{' + lep12[1] + '}',  wzero+'*('+cutbase+')',  16, -4., 4.))
        variables.append(variabile('deltaPhi_tauj1', '#Delta #phi_{#tau j_{1}}',  wzero+'*('+cutbase+')',  16, -4., 4.))
        variables.append(variabile('deltaPhi_tauj2', '#Delta #phi_{#tau j_{2}}',  wzero+'*('+cutbase+')',  16, -4., 4.))
        variables.append(variabile('deltaPhi_lepj1', '#Delta #phi_{l j_{1}}',  wzero+'*('+cutbase+')', 16, -4., 4.))
        variables.append(variabile('deltaPhi_lepj2', '#Delta #phi_{l j_{2}}',  wzero+'*('+cutbase+')', 16, -4., 4.))
        

        variables.append(variabile('deltaEta_' + lep12[0], '#Delta #eta_{' + lep12[1] + '}',  wzero+'*('+cutbase+')',  16, -8., 8.))
        variables.append(variabile('deltaEta_tauj1', '#Delta #eta_{#tau j_{1}}',  wzero+'*('+cutbase+')',  16, -8., 8.))
        variables.append(variabile('deltaEta_tauj2', '#Delta #eta_{#tau j_{2}}',  wzero+'*('+cutbase+')',  16, -8., 8.))
        variables.append(variabile('deltaEta_lepj1', '#Delta #eta_{l j_{1}}',  wzero+'*('+cutbase+')', 16, -8., 8.))
        variables.append(variabile('deltaEta_lepj2', '#Delta #eta_{l j_{2}}',  wzero+'*('+cutbase+')', 16, -8., 8.))
        
        bin_deltaeta_jj = array("f", [-1., -0.8, -0.4, 0.4, 0.8, 1.])
        nbin_deltaeta_jj = len(bin_deltaeta_jj) - 1
        '''

        variables.append(variabile('deltaTheta_jj', 'cos(#Delta#theta_{jj})',  wzero+'*('+cutbase+')',  nbin_deltaeta_jj, bin_deltaeta_jj))
        variables.append(variabile('deltaTheta_' + lep12[0], 'cos(#Delta#theta_{' + lep12[1] + '})',  wzero+'*('+cutbase+')',  10, 0., 1.))
        variables.append(variabile('deltaTheta_tauj1', 'cos(#Delta#theta_{#tau j_{1}})',  wzero+'*('+cutbase+')',  10, 0., 1.))
        variables.append(variabile('deltaTheta_tauj2', 'cos(#Delta#theta_{#tau j_{2}})',  wzero+'*('+cutbase+')',  10, 0., 1.))
        variables.append(variabile('deltaTheta_lepj1', 'cos(#Delta#theta_{l j_{1}})',  wzero+'*('+cutbase+')', 10, 0., 1.))
        variables.append(variabile('deltaTheta_lepj2', 'cos(#Delta#theta_{l j_{2}})',  wzero+'*('+cutbase+')', 10, 0., 1.))

        '''
        bin_ptRel = array("f", [0., 25., 50., 75., 100., 125, 150., 200., 250., 300., 400., 500.])
        nbin_ptRel = len(bin_ptRel) - 1
        
        variables.append(variabile('ptRel_jj', 'relative p_{T} j_{1} j_{2}',  wzero+'*('+cutbase+')', nbin_ptRel, bin_ptRel))
        variables.append(variabile('ptRel_' + lep12[0], 'relative p_{T} ' + lep12[1],  wzero+'*('+cutbase+')', nbin_ptRel, bin_ptRel))
        variables.append(variabile('ptRel_tauj1', 'relative p_{T} #tau j_{1}',  wzero+'*('+cutbase+')', nbin_ptRel, bin_ptRel))
        variables.append(variabile('ptRel_tauj2', 'relative p_{T} #tau j_{2}',  wzero+'*('+cutbase+')', nbin_ptRel, bin_ptRel))
        variables.append(variabile('ptRel_lepj1', 'relative p_{T} l j_{1}',  wzero+'*('+cutbase+')', nbin_ptRel, bin_ptRel))
        variables.append(variabile('ptRel_lepj2', 'relative p_{T} l j_{2}',  wzero+'*('+cutbase+')', nbin_ptRel, bin_ptRel))
        
        variables.append(variabile('event_RT', 'R_{T}',  wzero+'*('+cutbase+')', 30, 0., 3.))

        for sample in dataset_new:
            print(sample)
            if ('DataHT' in sample.label or 'DataMET' in sample.label) and not opt.folder.startswith("CTHT"):# or "WJets" in sample.label:
                continue
            elif ('DataMu' in sample.label or 'DataEle' in sample.label or 'DataMET' in sample.label or 'QCD' in sample.label) and opt.folder.startswith("CTHT"):
                continue
                    
            if(opt.plot):
                for var in variables:
                    if opt.count:
                        if not os.path.exists(pathplot + 'countings/'):
                            os.makedirs(pathplot + 'countings/')
                        if not os.path.exists(pathplot + 'countings/' + cut_tag):
                            os.makedirs(pathplot + 'countings/' + cut_tag)
                        if not os.path.exists(pathplot + 'countings/' + cut_tag + "/" + var._name + ".txt"):
                            tmp_f = open(pathplot + 'countings/' + cut_tag + "/" + var._name + ".txt", "w")
                            tmp_f.close()
                    if (("GenPart" in var._name) or ("MC_" in var._name)) and "Data" in sample.label:
                        continue
                    plot(lep, opt.channel, var, sample, cut_tag, "")

        if(opt.stack):
            for var in variables:
                print(var._xmax)
                #os.system('set LD_PRELOAD=libtcmalloc.so')
                makestack(lep, opt.channel, var, dataset_new, cut_tag, "", lumi[str(year)])
                #os.system('set LD_PRELOAD=libtcmalloc.so')

        if lep == 'muon':
            dataset_new.append(sample_dict['DataEle_'+str(year)])
        elif lep == 'electron':
            dataset_new.append(sample_dict['DataMu_'+str(year)])
