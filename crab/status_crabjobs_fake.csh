set year = '2017'
reset
#python submit_crab_fake.py -d WJets_$year --status -t Lep
#python submit_crab_fake.py -d WJets_$year --status -t Tau#
python submit_crab_fake.py -d WJets_$year --status -t HT
#python submit_crab_fake.py -d DYJetsToLL_$year --status -t Lep#
#python submit_crab_fake.py -d DYJetsToLL_$year --status -t Tau#
python submit_crab_fake.py -d DYJetsToLL_$year --status -t HT
#python submit_crab_fake.py -d DataEle_$year --status -t Lep#
#python submit_crab_fake.py -d DataMu_$year --status -t Lep#
python submit_crab_fake.py -d TT_$year --status -t HT
python submit_crab_fake.py -d DataHT_$year --status -t HT


