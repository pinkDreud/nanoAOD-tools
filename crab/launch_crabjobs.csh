set year = '2018'
reset
python submit_crab.py -d TT_$year -r
python submit_crab.py -d WJets_$year -r
#python submit_crab.py -d WZ_$year --status #
python submit_crab.py -d DYJetsToLL_$year -r
#python submit_crab.py -d VG_$year --status #
python submit_crab.py -d TVX_$year -r
python submit_crab.py -d WrongSign_$year -r
python submit_crab.py -d TTTo2L2Nu_$year -r
#python submit_crab.py -d Other_$year --status #
python submit_crab.py -d ZZtoLep_$year -r
#python submit_crab.py -d VBS_SSWW_aQGC_$year --status #
#python submit_crab.py -d WpWpJJ_EWK_$year --status #
#python submit_crab.py -d WpWpJJ_QCD_$year --status #
python submit_crab.py -d VBS_SSWW_DIM6_SM_$year -r
#python submit_crab.py -d DataEle_$year --status #
#python submit_crab.py -d DataMu_$year --status #

#set year = '2017'
#python submit_crab.py -d DataEle_$year --status
#python submit_crab.py -d DataMu_$year --status
