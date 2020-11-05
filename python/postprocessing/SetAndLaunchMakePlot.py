import os
import optparse
import sys

usage = 'python SetAndLaunchMakePlot.py -y year'
parser = optparse.OptionParser(usage)
parser.add_option('-y', dest='year', type=str, default = '2017', help='Please enter a year, default is 2017')

(opt, args) = parser.parse_args()

username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])

#folder = "Eff_Jet" + opt.jetwp + "_Mu" + opt.muwp + "_Ele" + opt.elewp
path = "/eos/user/" + inituser + "/" + username + "/VBS/nosynch/"
dirlist = [dirs for dirs in os.listdir(path) if os.path.isdir(path+dirs) and "v" in dirs]
print dirlist

for dirn in dirlist:
    ismerged = False

    for nfile in os.listdir(path+dirn+"/"+os.listdir(path+dirn)[0]):
        if "_merged" in nfile:
            ismerged = True
            break
    
    if ismerged:
        continue

    print "python makeplot.py -y ", opt.year, " --merpart --lumi --mertree --folder ", dirn
    os.system("python makeplot.py -y " + opt.year + " --merpart --lumi --mertree --folder " + dirn)

