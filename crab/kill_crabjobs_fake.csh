set year = '2017'
reset
python submit_crab_fake.py -d WJets_$year -p -t HT 
python submit_crab_fake.py -d DYJetsToLL_$year -p -t HT  
python submit_crab_fake.py -d DataHT_$year -p -t HT
 
