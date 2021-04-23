set year = '2017'
reset
python submit_crab.py -d TT_$year -r 
#python submit_crab.py -d WJets_$year -r 
python submit_crab.py -d WZ_$year -r 
##python submit_crab.py -d DYJetsToLL_$year -r 
python submit_crab.py -d VG_$year -r 
python submit_crab.py -d TVX_$year -r 
python submit_crab.py -d WrongSign_$year -r 
python submit_crab.py -d TTTo2L2Nu_$year -r
python submit_crab.py -d Other_$year -r
python submit_crab.py -d ZZtoLep_$year -r
python submit_crab.py -d WpWpJJ_EWK_$year -r 
python submit_crab.py -d WpWpJJ_QCD_$year -r
python submit_crab.py -d VBS_SSWW_BSM_SM_2017 -r
#python submit_crab.py -d DataEle_$year -r
#python submit_crab.py -d DataMu_$year -r
