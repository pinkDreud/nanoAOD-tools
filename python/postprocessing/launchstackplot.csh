set LD_PRELOAD=libtcmalloc.so
set year = 2017
set folder = v80

#rm -rf /eos/home-a/apiccine/VBS/nosynch/$folder/stack_vsjet2/ #countings
#rm -rf /eos/home-a/apiccine/VBS/nosynch/$folder/stack_vsjet4/ #countings

###### electron #######
python makeplot.py -y 2017 --lep electron --bveto -f $folder -s --wfake incl_vsjet4 
#python makeplot.py -y 2017 --lep electron --bveto -f $folder -s --wfake sep_vsjet4 

#python makeplot.py -y 2017 --lep electron --bveto -f $folder -s --wfake sep_vsjet4 --bdt #--blinded
#python makeplot.py -y 2017 --lep electron --bveto -f $folder -s --wfake incl_vsjet4 --bdt #--blinded

#python makeplot.py -y 2017 --lep electron --bveto -f $folder -s --wfake sep_vsjet4 --ebdt #--blinded
#python makeplot.py -y 2017 --lep electron --bveto -f $folder -s --wfake incl_vsjet4 --ebdt #--blinded

set LD_PRELOAD=libtcmalloc.so

#python makeplot.py -y 2017 --lep electron --sr -f $folder -s --wfake incl_vsjet4 
#python makeplot.py -y 2017 --lep electron --sr -f $folder -s --wfake sep_vsjet4 

#python makeplot.py -y 2017 --lep electron --sr -f $folder -s --wfake sep_vsjet4 --bdt #--blinded
#python makeplot.py -y 2017 --lep electron --sr -f $folder -s --wfake incl_vsjet4 --bdt #--blinded

#python makeplot.py -y 2017 --lep electron --sr -f $folder -s --wfake sep_vsjet4 --ebdt #--blinded
#python makeplot.py -y 2017 --lep electron --sr -f $folder -s --wfake incl_vsjet4 --ebdt #--blinded

set LD_PRELOAD=libtcmalloc.so

#python makeplot.py -y 2017 --lep electron --wjets -f $folder -s --wfake incl_vsjet4
#python makeplot.py -y 2017 --lep electron --wjets -f $folder -s --wfake sep_vsjet4

#python makeplot.py -y 2017 --lep electron --wjets -f $folder -s --wfake incl_vsjet4 --bdt 
#python makeplot.py -y 2017 --lep electron --wjets -f $folder -s --wfake sep_vsjet4 --bdt 

#python makeplot.py -y 2017 --lep electron --wjets -f $folder -s --wfake incl_vsjet4 --ebdt 
#python makeplot.py -y 2017 --lep electron --wjets -f $folder -s --wfake sep_vsjet4 --ebdt 

set LD_PRELOAD=libtcmalloc.so

#python makeplot.py -y 2017 --lep electron --ttbar -f $folder -s --wfake incl_vsjet4
#python makeplot.py -y 2017 --lep electron --ttbar -f $folder -s --wfake sep_vsjet4

#python makeplot.py -y 2017 --lep electron --ttbar -f $folder -s --wfake incl_vsjet4 --bdt 
#python makeplot.py -y 2017 --lep electron --ttbar -f $folder -s --wfake sep_vsjet4 --bdt 

#python makeplot.py -y 2017 --lep electron --ttbar -f $folder -s --wfake incl_vsjet4 --ebdt 
#python makeplot.py -y 2017 --lep electron --ttbar -f $folder -s --wfake sep_vsjet4 --ebdt 

set LD_PRELOAD=libtcmalloc.so

#python makeplot.py -y 2017 --lep electron --qcd -f $folder -s --wfake incl_vsjet4
#python makeplot.py -y 2017 --lep electron --qcd -f $folder -s --wfake sep_vsjet4

#python makeplot.py -y 2017 --lep electron --qcd -f $folder -s --wfake incl_vsjet4 --bdt 
#python makeplot.py -y 2017 --lep electron --qcd -f $folder -s --wfake sep_vsjet4 --bdt 

#python makeplot.py -y 2017 --lep electron --qcd -f $folder -s --wfake incl_vsjet4 --ebdt 
#python makeplot.py -y 2017 --lep electron --qcd -f $folder -s --wfake sep_vsjet4 --ebdt 

set LD_PRELOAD=libtcmalloc.so


###### muon #######
python makeplot.py -y 2017 --lep muon --bveto -f $folder -s --wfake incl_vsjet2 #--blinded
#python makeplot.py -y 2017 --lep muon --bveto -f $folder -s --wfake sep_vsjet2 #--blinded

#python makeplot.py -y 2017 --lep muon --bveto -f $folder -s --wfake incl_vsjet2 --bdt #--blinded
#python makeplot.py -y 2017 --lep muon --bveto -f $folder -s --wfake sep_vsjet2 --bdt #--blinded

#python makeplot.py -y 2017 --lep muon --bveto -f $folder -s --wfake incl_vsjet2 --mubdt #--blinded
#python makeplot.py -y 2017 --lep muon --bveto -f $folder -s --wfake sep_vsjet2 --mubdt #--blinded

set LD_PRELOAD=libtcmalloc.so

#python makeplot.py -y 2017 --lep muon --sr -f $folder -s --wfake incl_vsjet2 #--blinded
#python makeplot.py -y 2017 --lep muon --sr -f $folder -s --wfake sep_vsjet2 #--blinded

#python makeplot.py -y 2017 --lep muon --sr -f $folder -s --wfake incl_vsjet2 --bdt #--blinded
#python makeplot.py -y 2017 --lep muon --sr -f $folder -s --wfake sep_vsjet2 --bdt #--blinded

#python makeplot.py -y 2017 --lep muon --sr -f $folder -s --wfake incl_vsjet2 --mubdt #--blinded
#python makeplot.py -y 2017 --lep muon --sr -f $folder -s --wfake sep_vsjet2 --mubdt #--blinded

set LD_PRELOAD=libtcmalloc.so

#python makeplot.py -y 2017 --lep muon --wjets -f $folder -s --wfake incl_vsjet2
#python makeplot.py -y 2017 --lep muon --wjets -f $folder -s --wfake sep_vsjet2

#python makeplot.py -y 2017 --lep muon --wjets -f $folder -s --wfake incl_vsjet2 --bdt
#python makeplot.py -y 2017 --lep muon --wjets -f $folder -s --wfake sep_vsjet2 --bdt 

#python makeplot.py -y 2017 --lep muon --wjets -f $folder -s --wfake incl_vsjet2 --mubdt
#python makeplot.py -y 2017 --lep muon --wjets -f $folder -s --wfake sep_vsjet2 --mubdt

set LD_PRELOAD=libtcmalloc.so

#python makeplot.py -y 2017 --lep muon --ttbar -f $folder -s --wfake incl_vsjet2
#python makeplot.py -y 2017 --lep muon --ttbar -f $folder -s --wfake sep_vsjet2

#python makeplot.py -y 2017 --lep muon --ttbar -f $folder -s --wfake incl_vsjet2 --bdt
#python makeplot.py -y 2017 --lep muon --ttbar -f $folder -s --wfake sep_vsjet2 --bdt 

#python makeplot.py -y 2017 --lep muon --ttbar -f $folder -s --wfake incl_vsjet2 --mubdt
#python makeplot.py -y 2017 --lep muon --ttbar -f $folder -s --wfake sep_vsjet2 --mubdt

set LD_PRELOAD=libtcmalloc.so

#python makeplot.py -y 2017 --lep muon --qcd -f $folder -s --wfake incl_vsjet2
#python makeplot.py -y 2017 --lep muon --qcd -f $folder -s --wfake sep_vsjet2

#python makeplot.py -y 2017 --lep muon --qcd -f $folder -s --wfake incl_vsjet2 --bdt
#python makeplot.py -y 2017 --lep muon --qcd -f $folder -s --wfake sep_vsjet2 --bdt 

#python makeplot.py -y 2017 --lep muon --qcd -f $folder -s --wfake incl_vsjet2 --mubdt
#python makeplot.py -y 2017 --lep muon --qcd -f $folder -s --wfake sep_vsjet2 --mubdt

set LD_PRELOAD=libtcmalloc.so

