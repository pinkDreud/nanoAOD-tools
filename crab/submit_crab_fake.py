from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
import os
import optparse
import sys

usage = 'python submit_crab.py'
parser = optparse.OptionParser(usage)
parser.add_option('-d', '--dat', dest='dat', type=str, default = '', help='Please enter a dataset name')
parser.add_option('-t', '--trig', dest='trig', type=str, default = 'Lep', help='Please enter a trigger path')
parser.add_option('--status', dest = 'status', default = False, action = 'store_true', help = 'Default do not check the status')
parser.add_option('--verb', dest = 'verb', default = False, action = 'store_true', help = 'Default do not verbosely check the status')
parser.add_option('-s', '--sub', dest = 'sub', default = False, action = 'store_true', help = 'Default do not submit')
parser.add_option('-k', '--kill', dest = 'kill', default = False, action = 'store_true', help = 'Default do not kill')
parser.add_option('-r', '--resub', dest = 'resub', default = False, action = 'store_true', help = 'Default do not resubmit')
parser.add_option('-g', '--gout', dest = 'gout', default = False, action = 'store_true', help = 'Default do not do getoutput')
parser.add_option('-p', '--purge', dest = 'purge', default = False, action = 'store_true', help = 'Default do not kill')
(opt, args) = parser.parse_args()

print opt.dat

if not (opt.trig == "Lep" or opt.trig == "Tau" or opt.trig == "HT"):
    raise ValueError

dirtag = "_Fake" + opt.trig
print dirtag

def cfg_writer(sample, isMC, outdir):
    f = open("crab_cfg_fake.py", "w")
    f.write("from WMCore.Configuration import Configuration\n")
    #f.write("from CRABClient.UserUtilities import config, getUsernameFromSiteDB\n")
    f.write("\nconfig = Configuration()\n")
    f.write("config.section_('General')\n")
    f.write("config.General.requestName = '"+sample.label + dirtag +"'\n")
    if not isMC:
        f.write("config.General.instance = 'preprod'\n") #needed to solve a bug with Oracle server... 
    f.write("config.General.transferLogs=True\n")
    f.write("config.section_('JobType')\n")
    f.write("config.JobType.pluginName = 'Analysis'\n")
    f.write("config.JobType.psetName = 'PSet_fake.py'\n")
    f.write("config.JobType.scriptExe = 'crab_script_fake.sh'\n")
    f.write("config.JobType.allowUndistributedCMSSW = True\n")
    f.write("config.JobType.inputFiles = ['crab_script_fake.py','../scripts/haddnano.py', '../scripts/keep_and_drop.txt']\n") #hadd nano will not be needed once nano tools are in cmssw
    f.write("config.JobType.sendPythonFolder = True\n")
    if isMC:
        f.write("config.JobType.maxMemoryMB = 5000\n")         
        f.write("config.JobType.maxJobRuntimeMin = 3000\n")
        #f.write("config.JobType.numCores = 8\n")
    f.write("config.section_('Data')\n")
    f.write("config.Data.inputDataset = '"+sample.dataset+"'\n")
    f.write("config.Data.allowNonValidInputDataset = True\n")
    #f.write("config.Data.inputDBS = 'phys03'")
    f.write("config.Data.inputDBS = 'global'\n")
    if not isMC:
        f.write("config.Data.splitting = 'LumiBased'\n")
        if sample.year == '2016':
            f.write("config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt'\n")
        elif sample.year == '2017':
            f.write("config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt'\n")
        elif sample.year == '2018':
            f.write("config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt'\n")
        f.write("config.Data.unitsPerJob = 50\n")
    #elif(('WJetsHT' in sample.label and not ('HT70to100' in sample.label or 'HT100to200' in sample.label or 'HT400to600' in sample.label)) or 'QCDHT' in sample.label):
        #f.write("config.Data.splitting = 'EventAwareLumiBased'\n")                            
        #f.write("config.Data.unitsPerJob = 50000\n")
    else:
        f.write("config.Data.splitting = 'FileBased'\n")
        f.write("config.Data.unitsPerJob = 1\n")
    #config.Data.runRange = ''
    #f.write("config.Data.splitting = 'EventAwareLumiBased'")
    #f.write("config.Data.totalUnits = 10\n")
    f.write("config.Data.outLFNDirBase = '/store/user/%s/%s' % ('"+str(os.environ.get('USER'))+"', '" +outdir+"')\n")
    f.write("config.Data.publication = False\n")
    f.write("config.Data.outputDatasetTag = '"+sample.label + dirtag +"'\n")
    f.write("config.section_('Site')\n")
    f.write("config.Site.storageSite = 'T2_IT_Pisa'\n")
    #f.write("config.Site.storageSite = "T2_CH_CERN"
    #f.write("config.section_("User")
    #f.write("config.User.voGroup = 'dcms'
    f.close()

def crab_script_writer(sample, outpath, isMC, modules, presel):
    f = open("crab_script_fake.py", "w")
    f.write("#!/usr/bin/env python\n")
    f.write("import os\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.jme.htProducerCpp import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.jme.mht import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis\n")
    if isMC:
        f.write("from PhysicsTools.NanoAODTools.postprocessing.examples.MCweight_writer import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.examples.MET_HLT_Filter_Fake import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.examples.preselection import *\n")
    if isMC:
        f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *\n")
        f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *\n")
        f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.common.lepSFProducer import *\n")
        f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.common.hepmcDump import *\n")



    #f.write("infile = "+str(sample.files)+"\n")
    #f.write("outpath = '"+ outpath+"'\n")
    #Deafult PostProcessor(outputDir,inputFiles,cut=None,branchsel=None,modules=[],compression='LZMA:9',friend=False,postfix=None, jsonInput=None,noOut=False,justcount=False,provenance=False,haddFileName=None,fwkJobReport=False,histFileName=None,histDirName=None, outputbranchsel=None,maxEntries=None,firstEntry=0, prefetch=False,longTermCache=False)\n")
    if isMC:
        f.write("metCorrector = createJMECorrector(isMC="+str(isMC)+", dataYear="+str(sample.year)+", jesUncert='All', applyHEMfix=True)\n")
        f.write("fatJetCorrector = createJMECorrector(isMC="+str(isMC)+", dataYear="+str(sample.year)+", jesUncert='All', applyHEMfix=True, jetType = 'AK8PFPuppi')\n")
        #f.write("jmeCorrections = createJMECorrector(isMC="+str(isMC)+", dataYear="+str(sample.year)+", jesUncert='All', redojec=True, jetType = 'AK8PFchs')\n")
        f.write("p=PostProcessor('.', inputFiles(), '', modules=["+modules+"], provenance=True, fwkJobReport=True, histFileName='hist.root', histDirName='plots', outputbranchsel='keep_and_drop.txt')\n")# haddFileName='"+sample.label+".root'
    else:
        f.write("metCorrector = createJMECorrector(isMC="+str(isMC)+", dataYear="+str(sample.year)+", runPeriod='"+str(sample.runP)+"', applyHEMfix=True, jesUncert='All')\n")
        f.write("fatJetCorrector = createJMECorrector(isMC="+str(isMC)+", dataYear="+str(sample.year)+", runPeriod='"+str(sample.runP)+"', jesUncert='All', applyHEMfix=True, jetType = 'AK8PFPuppi')\n")
        #f.write("jmeCorrections = createJMECorrector(isMC="+str(isMC)+", dataYear="+str(sample.year)+", runPeriod='"+str(sample.runP)+"', jesUncert='All', redojec=True, jetType = 'AK8PFchs')\n")
        f.write("p=PostProcessor('.', inputFiles(), '"+presel+"', modules=["+modules+"], provenance=True, fwkJobReport=True, jsonInput=runsAndLumis(), haddFileName='tree_hadd.root', outputbranchsel='keep_and_drop.txt')\n")#
    f.write("p.run()\n")
    f.write("print 'DONE'\n")
    f.close()

    f_sh = open("crab_script_fake.sh", "w")
    f_sh.write("#!/bin/bash\n")
    f_sh.write("echo Check if TTY\n")
    f_sh.write("if [\"`tty`\" != \"not a tty\" ]; then\n")
    f_sh.write("  echo \"YOU SHOULD NOT RUN THIS IN INTERACTIVE, IT DELETES YOUR LOCAL FILES\"\n")
    f_sh.write("else\n\n")
    f_sh.write("echo \"ENV...................................\"\n")
    f_sh.write("env\n")
    f_sh.write("echo \"VOMS\"\n")
    f_sh.write("voms-proxy-info -all\n")
    f_sh.write("echo \"CMSSW BASE, python path, pwd\"\n")
    f_sh.write("echo $CMSSW_BASE\n")
    f_sh.write("echo $PYTHON_PATH\n")
    f_sh.write("echo $PWD\n")
    f_sh.write("rm -rf $CMSSW_BASE/lib/\n")
    f_sh.write("rm -rf $CMSSW_BASE/src/\n")
    f_sh.write("rm -rf $CMSSW_BASE/module/\n")
    f_sh.write("rm -rf $CMSSW_BASE/python/\n")
    f_sh.write("mv lib $CMSSW_BASE/lib\n")
    f_sh.write("mv src $CMSSW_BASE/src\n")
    f_sh.write("mv module $CMSSW_BASE/module\n")
    f_sh.write("mv python $CMSSW_BASE/python\n")

    f_sh.write("echo Found Proxy in: $X509_USER_PROXY\n")
    f_sh.write("python crab_script_fake.py $1\n")
    if isMC:
        f_sh.write("hadd tree_hadd.root tree.root hist.root\n")
    f_sh.write("fi\n")
    f_sh.close()

if not(opt.dat in sample_dict.keys()):
    print sample_dict.keys()
dataset = sample_dict[opt.dat]

samples = []

if hasattr(dataset, 'components'): # How to check whether this exists or not
    samples = [sample for sample in dataset.components]# Method exists and was used.  
else:
    print "You are launching a single sample and not an entire bunch of samples"
    samples.append(dataset)

submit = opt.sub
status = opt.status
verbose = opt.verb
kill = opt.kill
purge = opt.purge
resubmit = opt.resub
getout = opt.gout
#Writing the configuration file

for sample in samples:
    if ('DataEleB' in sample.label or 'DataMuB' in sample.label or ('DataHTB' in sample.label and opt.trig=="Lep") and sample.year == 2017):
        continue
    print 'Launching sample ' + sample.label + dirtag
    if submit:
        #Writing the script file 
        year = str(sample.year)
        #hepmc = 'hepmc'
        lep_mod = 'lepSF_'+year+'()'
        btag_mod = 'btagSF'+year+'()'
        met_hlt_mod = 'MET_HLT_Filter_Fake_'+year+'_'+opt.trig+'()'
        muon_pt_corr = 'muonScaleRes'+year+'()'
        pu_mod = 'puWeight_'+year+'()'
        ht_producer = 'ht()'
        mht_producer = 'mht()'
        if ('Data' in sample.label):
            isMC = False
            presel = "(Flag_goodVertices && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter) "
            if year == '2016':# and sample.runP != 'H':
                if 'DataHT' not in sample.label:
                    presel += " &&((HLT_Ele27_WPTight_Gsf || HLT_Ele32_WPTight_Gsf || HLT_IsoMu24 || HLT_IsoTkMu24) && Flag_globalSuperTightHalo2016Filter)"
                else:
                    presel += " && (HLT_PFHT250 || HLT_PFHT300)"
            elif year == '2017':# and sample.runP != 'B':
                if 'DataHT' not in sample.label:
                    if 'DataTau' not in sample.label:
                        presel += " && (HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30 || HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30 || HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 || HLT_Mu8_TrkIsoVVL || HLT_Mu17_TrkIsoVVL || HLT_Mu15_IsoVVVL_PFHT600)"
                    else:
                        presel += " && (HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1 || HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1 || HLT_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr)"
                else:
                    presel += " && (HLT_PFHT250 || HLT_PFHT350 || HLT_PFHT370 || HLT_PFHT430 || HLT_PFHT510 || HLT_PFHT590 || HLT_PFHT680 || HLT_PFHT780 || HLT_PFHT890)"
            elif year == '2018':
                if 'DataHT' not in sample.label:
                    presel += " && (HLT_IsoMu24 || HLT_Ele32_WPTight_Gsf_L1DoubleEG)"
                else:
                    presel += " && (HLT_PFHT250 || HLT_PFHT350)"
        else:
            isMC = True
            presel = ""
                
        print 'The flag isMC is: ' + str(isMC)

        print "Producing crab configuration file"

        cfg_writer(sample, isMC, "VBS_Fake")

        if isMC:
            modules = "MCweight_writer('" + sample.label + "'), " + met_hlt_mod + ", preselection(), " + lep_mod + ", " + pu_mod + ", " + btag_mod + ", PrefCorr(), metCorrector(), fatJetCorrector(), " + muon_pt_corr + ", " + ht_producer + ", " + mht_producer # Put here all the modules you want to be runned by crab
        else:
            modules = "preselection(), metCorrector(), fatJetCorrector(), " + muon_pt_corr + ", " + ht_producer + ", " + mht_producer # Put here all the modules you want to be runned by crab
        #print "modules:", modules
        print "Producing crab script"
        crab_script_writer(sample,'/eos/user/'+str(os.environ.get('USER')[0]) + '/'+str(os.environ.get('USER'))+'/Wprime/nosynch/', isMC, modules, presel)
        os.system("chmod +x crab_script_fake.sh")
        
        #Launching crab
        print "Submitting crab jobs..."
        os.system("crab submit -c crab_cfg_fake.py")

    if kill:
        print("Killing crab jobs...")
        os.system("crab kill -d crab_" + sample.label + dirtag)
        #os.system("rm -rf crab_" + sample.label  + dirtag)

    if purge:
        print("Purging crab jobs...")
        os.system("crab purge -d crab_" + sample.label + dirtag)
        os.system("rm -rf crab_" + sample.label + dirtag)

    if resubmit:
        print "Resubmitting crab jobs..."
        os.system("crab resubmit -d crab_" + sample.label + dirtag )

    if status:
        print "Checking crab jobs status..."
        if verbose:
            os.system("crab status --verboseErrors -d crab_" + sample.label + dirtag )
        else:
            os.system("crab status --verboseErrors -d crab_" + sample.label + dirtag )
        
    if getout:
        print "crab getoutput -d crab_" + sample.label + dirtag  + " --xrootd > ./macros/files/Fake/" + opt.trig + "/" + sample.label + ".txt"
        os.system("crab getoutput -d crab_" + sample.label + dirtag + " --xrootd > ./macros/files/Fake/" + opt.trig + "/" + sample.label + ".txt")
        #for i in xrange(1, 969):
        #os.system("crab getoutput -d crab_" + sample.label + " --outputpath=/eos/user/"+str(os.environ.get('USER')[0]) + "/"+str(os.environ.get('USER'))+"/Wprime/nosynch/" + sample.label + "/ --jobids="+str(i))
