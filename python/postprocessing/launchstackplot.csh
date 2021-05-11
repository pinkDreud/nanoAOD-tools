set LD_PRELOAD=libtcmalloc.so
set year = 2017
set folder = v74

#rm -rf /eos/home-a/apiccine/VBS/nosynch/$folder/plot/electron/ #countings
rm -rf /eos/home-a/apiccine/VBS/nosynch/$folder/stack_vsjet2/ #countings
rm -rf /eos/home-a/apiccine/VBS/nosynch/$folder/stack_vsjet4/ #countings

##python makeplot.py -y 2017 --lep electron --bveto -f $folder -p --count #--blinded
##python makeplot.py -y 2017 --lep electron --bveto -f $folder -p --count --signal #--blinded
#python makeplot.py -y 2017 --lep electron --bveto -f $folder -s #--blinded
python makeplot.py -y 2017 --lep electron --bveto -f $folder -s --wfake incl_vsjet2 #--blinded 
python makeplot.py -y 2017 --lep electron --bveto -f $folder -s --wfake sep_vsjet2 #--blinded 
#python makeplot.py -y 2017 --lep electron --bveto -f $folder -s --wfake incl_vsjet4 #--blinded 
#python makeplot.py -y 2017 --lep electron --bveto -f $folder -s --wfake sep_vsjet4 #--blinded 
##python makeplot.py -y 2017 --lep electron --bveto -f $folder -s --wfake incl_vsjet2 --signal --notstacked #--blinded 
python makeplot.py -y 2017 --lep electron --bveto -f $folder -s --wfake sep_vsjet2 --cut "BDT_output>-0.425" #--blinded
python makeplot.py -y 2017 --lep electron --bveto -f $folder -s --wfake incl_vsjet2 --cut "BDT_output>-0.425" #--blinded
#python makeplot.py -y 2017 --lep electron --bveto -f $folder -s --wfake sep_vsjet4 --cut "BDT_output>-0.425" #--blinded
#python makeplot.py -y 2017 --lep electron --bveto -f $folder -s --wfake incl_vsjet4 --cut "BDT_output>-0.425" #--blinded

python makeplot.py -y 2017 --lep electron --bveto -f $folder -s --wfake sep_vsjet2 --cut "BDT_output_ele>-0.536" #--blinded
python makeplot.py -y 2017 --lep electron --bveto -f $folder -s --wfake incl_vsjet2 --cut "BDT_output_ele>-0.536" #--blinded
#python makeplot.py -y 2017 --lep electron --bveto -f $folder -s --wfake sep_vsjet4 --cut "BDT_output_ele>-0.536" #--blinded
#python makeplot.py -y 2017 --lep electron --bveto -f $folder -s --wfake incl_vsjet4 --cut "BDT_output_ele>-0.536" #--blinded


set LD_PRELOAD=libtcmalloc.so

##python makeplot.py -y 2017 --lep electron --wjets -f $folder -p --count 
#python makeplot.py -y 2017 --lep electron --wjets -f $folder -s
python makeplot.py -y 2017 --lep electron --wjets -f $folder -s --wfake incl_vsjet2 
python makeplot.py -y 2017 --lep electron --wjets -f $folder -s --wfake sep_vsjet2 
#python makeplot.py -y 2017 --lep electron --wjets -f $folder -s --wfake incl_vsjet4
#python makeplot.py -y 2017 --lep electron --wjets -f $folder -s --wfake sep_vsjet4

python makeplot.py -y 2017 --lep electron --wjets -f $folder -s --wfake incl_vsjet2 --cut "BDT_output<-0.425" 
python makeplot.py -y 2017 --lep electron --wjets -f $folder -s --wfake sep_vsjet2 --cut "BDT_output<-0.425" 
#python makeplot.py -y 2017 --lep electron --wjets -f $folder -s --wfake incl_vsjet4 --cut "BDT_output<-0.425" 
#python makeplot.py -y 2017 --lep electron --wjets -f $folder -s --wfake sep_vsjet4 --cut "BDT_output<-0.425" 

python makeplot.py -y 2017 --lep electron --wjets -f $folder -s --wfake incl_vsjet2 --cut "BDT_output_ele<-0.536" 
python makeplot.py -y 2017 --lep electron --wjets -f $folder -s --wfake sep_vsjet2 --cut "BDT_output_ele<-0.536" 
#python makeplot.py -y 2017 --lep electron --wjets -f $folder -s --wfake incl_vsjet4 --cut "BDT_output_ele<-0.536" 
#python makeplot.py -y 2017 --lep electron --wjets -f $folder -s --wfake sep_vsjet4 --cut "BDT_output_ele<-0.536" 


set LD_PRELOAD=libtcmalloc.so

##python makeplot.py -y 2017 --lep electron --ttbar -f $folder -p --count
#python makeplot.py -y 2017 --lep electron --ttbar -f $folder -s --wfake incl_vsjet2 
#python makeplot.py -y 2017 --lep electron --ttbar -f $folder -s --wfake sep 
#python makeplot.py -y 2017 --lep electron --ttbar -f $folder -s --wfake incl_vsjet2 --cut "BDT_output<-0.425"
#python makeplot.py -y 2017 --lep electron --ttbar -f $folder -s --wfake incl_vsjet2 --cut "BDT_output_ele<-0.536"
#python makeplot.py -y 2017 --lep electron --ttbar -f $folder -s --wfake sep --cut "BDT_output_ele<-0.536"

set LD_PRELOAD=libtcmalloc.so

#rm -rf /eos/home-a/apiccine/VBS/nosynch/$folder/plot/muon/ #countings

#python makeplot.py -y 2017 --lep muon --bveto -f $folder -p --count #--blinded
##python makeplot.py -y 2017 --lep muon --bveto -f $folder -p --count --signal #--blinded
python makeplot.py -y 2017 --lep muon --bveto -f $folder -s --wfake incl_vsjet2 #--blinded
python makeplot.py -y 2017 --lep muon --bveto -f $folder -s --wfake sep_vsjet2 #--blinded

##python makeplot.py -y 2017 --lep muon --bveto -f $folder -s --wfake incl_vsjet2 --signal --notstacked #--blinded
python makeplot.py -y 2017 --lep muon --bveto -f $folder -s --wfake incl_vsjet2 --cut "BDT_output>-0.425" #--blinded
python makeplot.py -y 2017 --lep muon --bveto -f $folder -s --wfake incl_vsjet2 --cut "BDT_output_mu>-0.399" #--blinded
python makeplot.py -y 2017 --lep muon --bveto -f $folder -s --wfake sep_vsjet2 --cut "BDT_output>-0.425" #--blinded
python makeplot.py -y 2017 --lep muon --bveto -f $folder -s --wfake sep_vsjet2 --cut "BDT_output_mu>-0.399" #--blinded

##python makeplot.py -y 2017 --lep muon --wjets -f $folder -p --count
python makeplot.py -y 2017 --lep muon --wjets -f $folder -s --wfake incl_vsjet2 
python makeplot.py -y 2017 --lep muon --wjets -f $folder -s --wfake sep_vsjet2 

python makeplot.py -y 2017 --lep muon --wjets -f $folder -s --wfake incl_vsjet2 --cut "BDT_output<-0.425"
python makeplot.py -y 2017 --lep muon --wjets -f $folder -s --wfake incl_vsjet2 --cut "BDT_output_mu<-0.399"
python makeplot.py -y 2017 --lep muon --wjets -f $folder -s --wfake sep_vsjet2 --cut "BDT_output<-0.425"
python makeplot.py -y 2017 --lep muon --wjets -f $folder -s --wfake sep_vsjet2 --cut "BDT_output_mu<-0.399"

##python makeplot.py -y 2017 --lep muon --ttbar -f $folder -p --count
#python makeplot.py -y 2017 --lep muon --ttbar -f $folder -s --wfake incl_vsjet2 
#python makeplot.py -y 2017 --lep muon --ttbar -f $folder -s --wfake sep 

set LD_PRELOAD=libtcmalloc.so

