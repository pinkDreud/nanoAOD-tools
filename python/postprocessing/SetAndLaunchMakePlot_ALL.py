import os
import optparse
import sys
from samples.samples import *

usage = 'python SetAndLaunchMakePlot.py -y year -f folder -d sample'
parser = optparse.OptionParser(usage)
parser.add_option('-y', dest='year', type=str, default = '2017', help='Please enter a year, default is 2017')
parser.add_option('-f', dest='folder', type=str, default = '', help='Please enter a folder, default is v3')
parser.add_option('-d', dest='dataset', type=str, default = 'WpWpJJ_EWK', help='Please enter a dataset, default is signal')

(opt, args) = parser.parse_args()

username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])

#folder = "Eff_Jet" + opt.jetwp + "_Mu" + opt.muwp + "_Ele" + opt.elewp
path = "/eos/home-" + inituser + "/" + username + "/VBS/nosynch/"
dirlist = [dirs for dirs in os.listdir(path) if os.path.isdir(path+dirs) and opt.folder in dirs]
datas = opt.dataset + "_" + opt.year

print dirlist

for dirn in dirlist:
    exsamples = [d for d in os.listdir(path+dirn) if os.path.isdir(path+dirn+"/"+d)]

    for k in class_dict.keys():
        ismerged = False
        if k in exsamples:
            if str(k+".root") in os.listdir(path+dirn+"/"+k):
                ismerged = True
                    
        if not True in [bool(k.split("_")[0] in exsample) for exsample in exsamples]:
            ismerged = True

        if ismerged:
            continue

        print "python makeplot.py -y ", opt.year, " --merpart --lumi --mertree -d " + k + " --folder ", dirn
        os.system("python makeplot.py -y " + opt.year + " --merpart --lumi --mertree -d " + k + " --folder " + dirn)
