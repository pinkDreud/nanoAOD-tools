set LD_PRELOAD=libtcmalloc.so
set year = 2017
set folder = v60

#rm -rf /eos/home-a/apiccine/VBS/nosynch/$folder/plot_apc/electron/countings

#python makeplot.py -y 2017 --lep electron --bveto -f $folder -p --count #--blinded
#python makeplot.py -y 2017 --lep electron --bveto -f $folder -p --count --signal #--blinded
#python makeplot.py -y 2017 --lep electron --bveto -f $folder -p --count --cut "abs(lepton_Zeppenfeld)<2" #--blinded
#python makeplot.py -y 2017 --lep electron --bveto -f $folder -s #--blinded
#python makeplot.py -y 2017 --lep electron --bveto -f $folder -s --wfake #--blinded 
python makeplot.py -y 2017 --lep electron --bveto -f $folder -s --wfake --signal --notstacked #--blinded 
#python makeplot.py -y 2017 --lep electron --bveto -f $folder -s --wfake --cut "abs(lepton_Zeppenfeld)<2" #--blinded

#python makeplot.py -y 2017 --lep electron --wjets -f $folder -p --count 
#python makeplot.py -y 2017 --lep electron --wjets -f $folder -p --count --cut "abs(lepton_Zeppenfeld)<2"
##python makeplot.py -y 2017 --lep electron --wjets -f $folder -s
#python makeplot.py -y 2017 --lep electron --wjets -f $folder -s --wfake 
#python makeplot.py -y 2017 --lep electron --wjets -f $folder -s --wfake --cut "abs(lepton_Zeppenfeld)<2" 

#python makeplot.py -y 2017 --lep electron --ttbar -f $folder -p --count 
#python makeplot.py -y 2017 --lep electron --ttbar -f $folder -p --count --cut "abs(lepton_Zeppenfeld)<2"
##python makeplot.py -y 2017 --lep electron --ttbar -f $folder -s
#python makeplot.py -y 2017 --lep electron --ttbar -f $folder -s --wfake 
#python makeplot.py -y 2017 --lep electron --ttbar -f $folder -s --wfake --cut "abs(lepton_Zeppenfeld)<2"

set LD_PRELOAD=libtcmalloc.so

#rm -rf /eos/home-a/apiccine/VBS/nosynch/$folder/plot_apc/muon/countings
#python makeplot.py -y 2017 --lep muon --bveto -f $folder -p --count #--blinded
#python makeplot.py -y 2017 --lep muon --bveto -f $folder -p --count --signal #--blinded
#python makeplot.py -y 2017 --lep muon --bveto -f $folder -p --count --cut "abs(lepton_Zeppenfeld)<2" #--blinded
##python makeplot.py -y 2017 --lep muon --bveto -f $folder -s #--blinded
#python makeplot.py -y 2017 --lep muon --bveto -f $folder -s --wfake #--blinded
python makeplot.py -y 2017 --lep muon --bveto -f $folder -s --wfake --signal --notstacked #--blinded
#python makeplot.py -y 2017 --lep muon --bveto -f $folder -s --wfake --cut "abs(lepton_Zeppenfeld)<2" #--blinded

#python makeplot.py -y 2017 --lep muon --wjets -f $folder -p --count
#python makeplot.py -y 2017 --lep muon --wjets -f $folder -p --count --cut "abs(lepton_Zeppenfeld)<2"
##python makeplot.py -y 2017 --lep muon --wjets -f $folder -s
#python makeplot.py -y 2017 --lep muon --wjets -f $folder -s --wfake 
#python makeplot.py -y 2017 --lep muon --wjets -f $folder -s --wfake --cut "abs(lepton_Zeppenfeld)<2"

#python makeplot.py -y 2017 --lep muon --ttbar -f $folder -p --count
#python makeplot.py -y 2017 --lep muon --ttbar -f $folder -p --count --cut "abs(lepton_Zeppenfeld)<2"
##python makeplot.py -y 2017 --lep muon --ttbar -f $folder -s
#python makeplot.py -y 2017 --lep muon --ttbar -f $folder -s --wfake 
#python makeplot.py -y 2017 --lep muon --ttbar -f $folder -s --wfake --cut "abs(lepton_Zeppenfeld)<2"

set LD_PRELOAD=libtcmalloc.so

