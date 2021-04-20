set year = '2017'
#python submit_crab_fake.py -d WJets_$year -r -t Lep
#python submit_crab_fake.py -d WJets_$year -r -t Tau
python submit_crab_fake.py -d WJets_$year -r -t HT
#python submit_crab_fake.py -d DYJetsToLL_$year -r -t Lep
#python submit_crab_fake.py -d DYJetsToLL_$year -r -t Tau
python submit_crab_fake.py -d DYJetsToLL_$year -r -t HT
#python submit_crab_fake.py -d DataEle_$year -r -t Lep
#python submit_crab_fake.py -d DataMu_$year -r -t Lep
#python submit_crab_fake.py -d DataTau_$year -r -t Tau
python submit_crab_fake.py -d DataHT_$year -r -t HT
