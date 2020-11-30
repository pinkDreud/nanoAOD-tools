set LD_PRELOAD=libtcmalloc.so
set year = 2017
set folder = v2
#python makeplot.py -y $year --merpart --lumi --mertree --folder $folder -d WZ_$year
#python makeplot.py -y $year --merpart --lumi --mertree --folder $folder
set LD_PRELOAD=libtcmalloc.so
python makeplot.py -y $year -p -L electron --folder $folder --sel #-N
#python makeplot.py -y $year -p -L muon --folder $folder --sel #-N
#python makeplot.py -y $year -p -L electron --folder $folder --sel --cut "best_topjet_isbtag==1&&best_Wpjet_isbtag==1"
#python makeplot.py -y $year -p -L electron --folder $folder --sel --cut "best_topjet_isbtag==1&&best_Wpjet_isbtag==0"
#python makeplot.py -y $year -p -L electron --folder $folder --sel --cut "best_topjet_isbtag==0&&best_Wpjet_isbtag==1"
#python makeplot.py -y $year -p -L electron --folder $folder --sel --cut "best_topjet_isbtag==0&&best_Wpjet_isbtag==0"
set LD_PRELOAD=libtcmalloc.so
