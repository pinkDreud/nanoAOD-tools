import os
import optparse
import sys
from samples.samples import *

usage = 'python SetAndLaunchMakePlot_ALL.py -y year -f folder'
parser = optparse.OptionParser(usage)
parser.add_option('-y', dest='year', type=str, default = '2017', help='Please enter a year, default is 2017')
parser.add_option('-f', dest='folder', type=str, default = 'v4', help='Please enter a folder, default is v4')
#parser.add_option('-d', dest='dataset', type=str, default = 'WpWpJJ_EWK', help='Please enter a dataset, default is signal')

(opt, args) = parser.parse_args()

username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])

#folder = "Eff_Jet" + opt.jetwp + "_Mu" + opt.muwp + "_Ele" + opt.elewp
path = "/eos/home-" + inituser + "/" + username + "/VBS/nosynch/"
dirlist = [dirs for dirs in os.listdir(path) if os.path.isdir(path+dirs) and opt.folder in dirs]
#datas = opt.dataset + "_" + opt.year

Debug = False # True # 

print dirlist

for dirn in dirlist:
    exsamples = [d for d in os.listdir(path+dirn) if os.path.isdir(path+dirn+"/"+d)]
    print exsamples

    for k, v in class_dict.items():
        ismerged = False
        doesexist = True

        kpath = path+dirn+"/"+k+"/"

        if hasattr(v, 'components'):
            for c in v.components:
                cpath = path + dirn + "/" + c.label + "/"
                
                if not os.path.exists(cpath):
                    print c.label + " not condorly produced yet"
                    doesexist = False
                    continue
   
                if not os.path.exists(cpath+c.label+".root"):
                    if os.path.exists(cpath+c.label+"_merged.root"):
                        if Debug:
                            print "rm -f " + cpath + c.label + "_merged.root"
                        else:
                            os.system("rm -f " + cpath + c.label + "_merged.root")
                    print c.label + " not merged so far"
                    print "Merging and luming " + c.label + "..."
                    if Debug:
                        print "python makeplot.py -y " + opt.year + " --merpart --lumi -d " + c.label + " --folder " + dirn
                    else:
                        os.system("python makeplot.py -y " + opt.year + " --merpart --lumi -d " + c.label + " --folder " + dirn)
                    print "Merged and lumied!"
                else:
                    print c.label + " is already merged and lumied"
                    ismerged = True

            if not ismerged and doesexist:
                if os.path.exists(kpath+k+".root"):
                    if Debug:
                        print "rm -f " + kpath + k + ".root"
                    else:
                        os.system("rm -f " + kpath + k + ".root")
                print k + " not merged so far"
                print "Merging lumied trees for " + k + " components..."
                if Debug:
                    print "python makeplot.py -y ", opt.year, " --mertree -d " + k + " --folder ", dirn
                else:
                    os.system("python makeplot.py -y " + opt.year + " --mertree -d " + k + " --folder " + dirn)
   
        else:
            if not os.path.exists(kpath+k):
                print c.label + " not condorly produced yet"
            else:
                if not os.path.exists(kpath+k+".root"):
                    if os.path.exists(kpath+k+"_merged.root"):
                        if Debug:
                            print "rm -f " + kpath + k + "_merged.root"
                        else:
                            os.system("rm -f " + kpath + k + "_merged.root")
                    print k + " neither merged nor lumied so far"
                    print "Merging and luming " + k + "..."
                    if Debug:
                        print "python makeplot.py -y ", opt.year, " --merpart --lumi --mertree -d " + k + " --folder ", dirn
                    else:
                        os.system("python makeplot.py -y " + opt.year + " --merpart --lumi --mertree -d " + k + " --folder " + dirn)
                    print "Merged and lumied!"
                else:
                    print k + "is already merged and lumied"
