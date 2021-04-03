#set LD_PRELOAD=libtcmalloc.so
set year = 2017
set folder = v64

rm -rf /eos/home-a/apiccine/VBS/nosynch/$folder/plot/electron/ #countings
rm -rf /eos/home-a/apiccine/VBS/nosynch/$folder/stack/ #countings

python3 makeplot.py -y 2017 --lep electron --bveto -f $folder -p --count #--blinded
#python3 makeplot.py -y 2017 --lep electron --bveto -f $folder -p --count --signal #--blinded
#python3 makeplot.py -y 2017 --lep electron --bveto -f $folder -p --count --cut "abs(lepton_Zeppenfeld)<1.8" #--blinded
python3 makeplot.py -y 2017 --lep electron --bveto -f $folder -p --count --cut "BDT_output>-0.32" #--blinded
#python3 makeplot.py -y 2017 --lep electron --bveto -f $folder -s #--blinded
#python3 makeplot.py -y 2017 --lep electron --bveto -f $folder -s --wfake incl #--blinded 
#python3 makeplot.py -y 2017 --lep electron --bveto -f $folder -s --wfake sep #--blinded 
#python3 makeplot.py -y 2017 --lep electron --bveto -f $folder -s --wfake incl --signal --notstacked #--blinded 
#python3 makeplot.py -y 2017 --lep electron --bveto -f $folder -s --wfake incl --cut "abs(lepton_Zeppenfeld)<1.8" #--blinded
#python3 makeplot.py -y 2017 --lep electron --bveto -f $folder -s --wfake sep --cut "abs(lepton_Zeppenfeld)<1.8" #--blinded
#python3 makeplot.py -y 2017 --lep electron --bveto -f $folder -s --wfake incl --cut "BDT_output>0" #--blinded
#python3 makeplot.py -y 2017 --lep electron --bveto -f $folder -s --wfake sep --cut "BDT_output>0" #--blinded

python3 makeplot.py -y 2017 --lep electron --wjets -f $folder -p --count 
#python3 makeplot.py -y 2017 --lep electron --wjets -f $folder -p --count --cut "abs(lepton_Zeppenfeld)<1.8"
python3 makeplot.py -y 2017 --lep electron --wjets -f $folder -p --count --cut "BDT_output<-0.32"
##python3 makeplot.py -y 2017 --lep electron --wjets -f $folder -s
#python3 makeplot.py -y 2017 --lep electron --wjets -f $folder -s --wfake incl 
#python3 makeplot.py -y 2017 --lep electron --wjets -f $folder -s --wfake sep 
#python3 makeplot.py -y 2017 --lep electron --wjets -f $folder -s --wfake incl --cut "abs(lepton_Zeppenfeld)<1.8" 
#python3 makeplot.py -y 2017 --lep electron --wjets -f $folder -s --wfake sep --cut "abs(lepton_Zeppenfeld)<1.8" 
#python3 makeplot.py -y 2017 --lep electron --wjets -f $folder -s --wfake incl --cut "BDT_output>0" 
#python3 makeplot.py -y 2017 --lep electron --wjets -f $folder -s --wfake sep --cut "BDT_output>0" 

python3 makeplot.py -y 2017 --lep electron --ttbar -f $folder -p --count
#python3 makeplot.py -y 2017 --lep electron --ttbar -f $folder -p --count --cut "abs(lepton_Zeppenfeld)<1.8"
python3 makeplot.py -y 2017 --lep electron --ttbar -f $folder -p --count --cut "BDT_output<-0.32"
##python3 makeplot.py -y 2017 --lep electron --ttbar -f $folder -s
#python3 makeplot.py -y 2017 --lep electron --ttbar -f $folder -s --wfake incl 
#python3 makeplot.py -y 2017 --lep electron --ttbar -f $folder -s --wfake sep 
#python3 makeplot.py -y 2017 --lep electron --ttbar -f $folder -s --wfake incl --cut "abs(lepton_Zeppenfeld)<1.8"
#python3 makeplot.py -y 2017 --lep electron --ttbar -f $folder -s --wfake sep --cut "abs(lepton_Zeppenfeld)<1.8"
#python3 makeplot.py -y 2017 --lep electron --ttbar -f $folder -s --wfake incl --cut "BDT_output>0"
#python3 makeplot.py -y 2017 --lep electron --ttbar -f $folder -s --wfake sep --cut "BDT_output>0"

#set LD_PRELOAD=libtcmalloc.so

rm -rf /eos/home-a/apiccine/VBS/nosynch/$folder/plot/muon/ #countings

python3 makeplot.py -y 2017 --lep muon --bveto -f $folder -p --count #--blinded
#python3 makeplot.py -y 2017 --lep muon --bveto -f $folder -p --count --signal #--blinded
#python3 makeplot.py -y 2017 --lep muon --bveto -f $folder -p --count --cut "abs(lepton_Zeppenfeld)<1.8" #--blinded
python3 makeplot.py -y 2017 --lep muon --bveto -f $folder -p --count --cut "BDT_output>-0.32" #--blinded
#python3 makeplot.py -y 2017 --lep muon --bveto -f $folder -s #--blinded
#python3 makeplot.py -y 2017 --lep muon --bveto -f $folder -s --wfake incl #--blinded
#python3 makeplot.py -y 2017 --lep muon --bveto -f $folder -s --wfake sep #--blinded
#python3 makeplot.py -y 2017 --lep muon --bveto -f $folder -s --wfake incl --signal --notstacked #--blinded
#python3 makeplot.py -y 2017 --lep muon --bveto -f $folder -s --wfake incl --cut "abs(lepton_Zeppenfeld)<1.8" #--blinded
#python3 makeplot.py -y 2017 --lep muon --bveto -f $folder -s --wfake sep --cut "abs(lepton_Zeppenfeld)<1.8" #--blinded
#python3 makeplot.py -y 2017 --lep muon --bveto -f $folder -s --wfake incl --cut "BDT_output>0" #--blinded
#python3 makeplot.py -y 2017 --lep muon --bveto -f $folder -s --wfake sep --cut "BDT_output>0" #--blinded

python3 makeplot.py -y 2017 --lep muon --wjets -f $folder -p --count
#python3 makeplot.py -y 2017 --lep muon --wjets -f $folder -p --count --cut "abs(lepton_Zeppenfeld)<1.8"
python3 makeplot.py -y 2017 --lep muon --wjets -f $folder -p --count --cut "BDT_output<-0.32"
##python3 makeplot.py -y 2017 --lep muon --wjets -f $folder -s
#python3 makeplot.py -y 2017 --lep muon --wjets -f $folder -s --wfake incl 
#python3 makeplot.py -y 2017 --lep muon --wjets -f $folder -s --wfake sep 
#python3 makeplot.py -y 2017 --lep muon --wjets -f $folder -s --wfake incl --cut "abs(lepton_Zeppenfeld)<1.8"
#python3 makeplot.py -y 2017 --lep muon --wjets -f $folder -s --wfake sep --cut "abs(lepton_Zeppenfeld)<1.8"
#python3 makeplot.py -y 2017 --lep muon --wjets -f $folder -s --wfake incl --cut "BDT_output>0"
#python3 makeplot.py -y 2017 --lep muon --wjets -f $folder -s --wfake sep --cut "BDT_output>0"

python3 makeplot.py -y 2017 --lep muon --ttbar -f $folder -p --count
#python3 makeplot.py -y 2017 --lep muon --ttbar -f $folder -p --count --cut "abs(lepton_Zeppenfeld)<1.8"
python3 makeplot.py -y 2017 --lep muon --ttbar -f $folder -p --count --cut "BDT_output<-0.32"
##python3 makeplot.py -y 2017 --lep muon --ttbar -f $folder -s
#python3 makeplot.py -y 2017 --lep muon --ttbar -f $folder -s --wfake incl 
#python3 makeplot.py -y 2017 --lep muon --ttbar -f $folder -s --wfake sep 
#python3 makeplot.py -y 2017 --lep muon --ttbar -f $folder -s --wfake incl --cut "abs(lepton_Zeppenfeld)<1.8"
#python3 makeplot.py -y 2017 --lep muon --ttbar -f $folder -s --wfake sep --cut "abs(lepton_Zeppenfeld)<1.8"
#python3 makeplot.py -y 2017 --lep muon --ttbar -f $folder -s --wfake incl --cut "BDT_output>0"
#python3 makeplot.py -y 2017 --lep muon --ttbar -f $folder -s --wfake sep --cut "BDT_output>0"

#set LD_PRELOAD=libtcmalloc.so

