#this fake PSET is needed for local test and for crab to figure the output filename
#you do not need to edit it unless you want to do a local test using a different input file than
#the one marked below
import FWCore.ParameterSet.Config as cms
process = cms.Process('NANO')
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(),
#	lumisToProcess=cms.untracked.VLuminosityBlockRange("254231:1-254231:24")
)
process.source.fileNames = [
	'root://cms-xrd-global.cern.ch//store/user/apiccine/VBS/JetHT/DataHTB_2017/201111_134952/0000/tree_hadd_378.root'#'../../NanoAOD/test/lzma.root' ##you can change only this line
]
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))
#process.options.numberOfThreads=cms.untracked.uint32(8)
process.output = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string('tree_hadd.root'))
process.out = cms.EndPath(process.output)

