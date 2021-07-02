set year = '2018'
reset
##python submit_crab_fake.py -d WJets_$year -s -t Lep
##python submit_crab_fake.py -d WJets_$year -s -t Tau
#python submit_crab_fake.py -d WJets_$year -r -t HT
##python submit_crab_fake.py -d DYJetsToLL_$year -s -t Lep
##python submit_crab_fake.py -d DYJetsToLL_$year -s -t Tau
#python submit_crab_fake.py -d DYJetsToLL_$year -r -t HT
##python submit_crab_fake.py -d DataEle_$year -s -t Lep
##python submit_crab_fake.py -d DataMu_$year -s -t Lep
##python submit_crab_fake.py -d DataTau_$year -s -t Tau
#python submit_crab_fake.py -d DataHTB_$year -s -t HT
#python submit_crab_fake.py -d DataHT_$year --status -t HT
#python submit_crab_fake.py -d ZZtoLep_$year -s -t HT
#python submit_crab_fake.py -d TT_$year --status -t HT

set year = '2017'
#python submit_crab_fake.py -d ZZtoLep_$year --status -t HT
#python submit_crab_fake.py -d OtherWS_$year --status -t HT
python submit_crab_fake.py -d DataHT_$year --status -t HT
