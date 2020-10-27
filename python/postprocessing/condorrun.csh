set folder='tageff'
set year='2017'
python submit_condor.py -d TT_$year -f $folder
#python submit_condor.py -d WJets_$year -f $folder
python submit_condor.py -d WZ_$year -f $folder
#python submit_condor.py -d DYJetsToLL_$year -f $folder
#python submit_condor.py -d WpWpJJ_EWK_$year -f $folder
#python submit_condor.py -d WpWpJJ_QCD_$year -f $folder 
