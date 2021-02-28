set LD_PRELOAD=libtcmalloc.so
set year = 2017
set folder = v46
python makeplot.py -y 2017 --lep electron --bveto -f $folder -p #--blinded
python makeplot.py -y 2017 --lep electron --bveto --blinded -f $folder -s #--blinded
python makeplot.py -y 2017 --lep electron --bveto -f $folder -s --wfake #--blinded 
#python makeplot.py -y 2017 --lep electron --wjets -f $folder -p
#python makeplot.py -y 2017 --lep electron --wjets -f $folder -s
#python makeplot.py -y 2017 --lep electron --wjets -f $folder -s --wfake
#python makeplot.py -y 2017 --lep electron --ttbar -f $folder -p
#python makeplot.py -y 2017 --lep electron --ttbar -f $folder -s
#python makeplot.py -y 2017 --lep electron --ttbar -f $folder -s --wfake
python makeplot.py -y 2017 --lep muon --bveto -f $folder -p #--blinded
python makeplot.py -y 2017 --lep muon --bveto -f $folder -s #--blinded
python makeplot.py -y 2017 --lep muon --bveto -f $folder -s --wfake #--blinded
#python makeplot.py -y 2017 --lep muon --wjets -f $folder -p
#python makeplot.py -y 2017 --lep muon --wjets -f $folder -s
#python makeplot.py -y 2017 --lep muon --wjets -f $folder -s --wfake
#python makeplot.py -y 2017 --lep muon --ttbar -f $folder -p
#python makeplot.py -y 2017 --lep muon --ttbar -f $folder -s
#python makeplot.py -y 2017 --lep muon --ttbar -f $folder -s --wfake
set LD_PRELOAD=libtcmalloc.so
