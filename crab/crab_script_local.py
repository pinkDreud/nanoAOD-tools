#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
from PhysicsTools.NanoAODTools.postprocessing.examples.MCweight_writer import *
from PhysicsTools.NanoAODTools.postprocessing.examples.MET_HLT_Filter import *
from PhysicsTools.NanoAODTools.postprocessing.examples.preselection import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.lepSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *

metCorrector = createJMECorrector(isMC=True, dataYear=2017, jesUncert='All', redojec=True)
fatJetCorrector = createJMECorrector(isMC=True, dataYear=2017, jesUncert='All', redojec=True, jetType = 'AK8PFchs')

p = PostProcessor('.', ['root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAODv7/WZ_TuneCP5_13TeV-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano02Apr2020_PU2017_EXT_102X_mc2017_realistic_v8-v1/130000/64130768-224A-F945-AF0D-85352D905EDE.root'], '', modules=[MCweight_writer('WZ')],#MET_HLT_Filter_2017(), preselection(), PrefCorr(), metCorrector(), fatJetCorrector(), lepSF_2017(), btagSF2017()],
outputbranchsel=os.path.abspath('../scripts/keep_and_drop.txt'), histFileName="histOut.root", histDirName="plots", maxEntries=10000, provenance=True, fwkJobReport=True)
p.run()
print 'DONE'
#, PrefCorr(), metCorrector(), fatJetCorrector()
