set year = '2017'
reset
#python submit_crab.py -d TT_$year -k 
#python submit_crab.py -d WJets_$year -k 
#python submit_crab.py -d WZ_$year -k 
##python submit_crab.py -d DYJetsToLL_$year -k 
#python submit_crab.py -d VG_$year -k 
#python submit_crab.py -d TVX_$year -k 
#python submit_crab.py -d WrongSign_$year -k 
#python submit_crab.py -d TTTo2L2Nu_$year -k
#python submit_crab.py -d Other_$year -k
#python submit_crab.py -d ZZtoLep_$year -k
python submit_crab.py -d WpWpJJ_EWK_$year -p 
python submit_crab.py -d WpWpJJ_QCD_$year -p
python submit_crab.py -d VBS_SSWW_BSM_SM_2017 -p
python submit_crab.py -d DataEle_$year -p
python submit_crab.py -d DataMu_$year -p
