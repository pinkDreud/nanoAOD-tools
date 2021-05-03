#set LD_PRELOAD=libtcmalloc.so
set year = 2017
set folder = v70

#rm -rf /eos/home-a/apiccine/VBS/nosynch/$folder/plot/electron/ #countings
#rm -rf /eos/home-a/apiccine/VBS/nosynch/$folder/stack/ #countings

python3 makeplot.py -y 2017 --lep electron --bveto -f $folder -p --wfake incl_vsjet2 --count #--blinded
python3 makeplot.py -y 2017 --lep electron --bveto -f $folder -p --wfake incl_vsjet2 --count --cut "BDT_output>-0.425" #--blinded
python3 makeplot.py -y 2017 --lep electron --bveto -f $folder -p --wfake incl_vsjet2 --count --cut "BDT_output_ele>-0.536" #--blinded

python3 makeplot.py -y 2017 --lep electron --wjets -f $folder -p --wfake incl_vsjet2 --count
python3 makeplot.py -y 2017 --lep electron --wjets -f $folder -p --wfake incl_vsjet2 --count --cut "BDT_output<-0.425"
python3 makeplot.py -y 2017 --lep electron --wjets -f $folder -p --wfake incl_vsjet2 --count --cut "BDT_output_ele<-0.536"

#python3 makeplot.py -y 2017 --lep electron --ttbar -f $folder -p --wfake incl_vsjet2 --count
#python3 makeplot.py -y 2017 --lep electron --ttbar -f $folder -p --wfake incl_vsjet2 --count --cut "BDT_output<-0.425"
#python3 makeplot.py -y 2017 --lep electron --ttbar -f $folder -p --wfake incl_vsjet2 --count --cut "BDT_output_ele<-0.536"

python3 makeplot.py -y 2017 --lep electron --bveto -f $folder -p --wfake incl_vsjet4 --count #--blinded
python3 makeplot.py -y 2017 --lep electron --bveto -f $folder -p --wfake incl_vsjet4 --count --cut "BDT_output>-0.425" #--blinded
python3 makeplot.py -y 2017 --lep electron --bveto -f $folder -p --wfake incl_vsjet4 --count --cut "BDT_output_ele>-0.536" #--blinded

python3 makeplot.py -y 2017 --lep electron --wjets -f $folder -p --wfake incl_vsjet4 --count
python3 makeplot.py -y 2017 --lep electron --wjets -f $folder -p --wfake incl_vsjet4 --count --cut "BDT_output<-0.425"
python3 makeplot.py -y 2017 --lep electron --wjets -f $folder -p --wfake incl_vsjet4 --count --cut "BDT_output_ele<-0.536"

#python3 makeplot.py -y 2017 --lep electron --ttbar -f $folder -p --wfake incl_vsjet4 --count
#python3 makeplot.py -y 2017 --lep electron --ttbar -f $folder -p --wfake incl_vsjet4 --count --cut "BDT_output<-0.425"
#python3 makeplot.py -y 2017 --lep electron --ttbar -f $folder -p --wfake incl_vsjet4 --count --cut "BDT_output_ele<-0.536"



#rm -rf /eos/home-a/apiccine/VBS/nosynch/$folder/plot/muon/ #countings

python3 makeplot.py -y 2017 --lep muon --bveto -f $folder -p --wfake incl_vsjet2 --count #--blinded
python3 makeplot.py -y 2017 --lep muon --bveto -f $folder -p --wfake incl_vsjet2 --count --cut "BDT_output>-0.425" #--blinded
python3 makeplot.py -y 2017 --lep muon --bveto -f $folder -p --wfake incl_vsjet2 --count --cut "BDT_output_mu>-0.399" #--blinded

python3 makeplot.py -y 2017 --lep muon --wjets -f $folder -p --wfake incl_vsjet2 --count
python3 makeplot.py -y 2017 --lep muon --wjets -f $folder -p --wfake incl_vsjet2 --count --cut "BDT_output<-0.425"
python3 makeplot.py -y 2017 --lep muon --wjets -f $folder -p --wfake incl_vsjet2 --count --cut "BDT_output_mu<-0.399"

#python3 makeplot.py -y 2017 --lep muon --ttbar -f $folder -p --wfake incl_vsjet2 --count
#python3 makeplot.py -y 2017 --lep muon --ttbar -f $folder -p --wfake incl_vsjet2 --count --cut "BDT_output<-0.425"
#python3 makeplot.py -y 2017 --lep muon --ttbar -f $folder -p --wfake incl_vsjet2 --count --cut "BDT_output<-0.399"

python3 makeplot.py -y 2017 --lep muon --bveto -f $folder -p --wfake incl_vsjet4 --count #--blinded
python3 makeplot.py -y 2017 --lep muon --bveto -f $folder -p --wfake incl_vsjet4 --count --cut "BDT_output>-0.425" #--blinded
python3 makeplot.py -y 2017 --lep muon --bveto -f $folder -p --wfake incl_vsjet4 --count --cut "BDT_output_mu>-0.399" #--blinded

python3 makeplot.py -y 2017 --lep muon --wjets -f $folder -p --wfake incl_vsjet4 --count
python3 makeplot.py -y 2017 --lep muon --wjets -f $folder -p --wfake incl_vsjet4 --count --cut "BDT_output<-0.425"
python3 makeplot.py -y 2017 --lep muon --wjets -f $folder -p --wfake incl_vsjet4 --count --cut "BDT_output_mu<-0.399"

#python3 makeplot.py -y 2017 --lep muon --ttbar -f $folder -p --wfake incl_vsjet4 --count
#python3 makeplot.py -y 2017 --lep muon --ttbar -f $folder -p --wfake incl_vsjet4 --count --cut "BDT_output<-0.425"
#python3 makeplot.py -y 2017 --lep muon --ttbar -f $folder -p --wfake incl_vsjet4 --count --cut "BDT_output<-0.399"

