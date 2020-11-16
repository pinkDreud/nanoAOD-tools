import os
import optparse
import sys

usage = 'python SetAndLaunchMakePlot.py -y year -f folder'
parser = optparse.OptionParser(usage)
parser.add_option('-y', dest='year', type=str, default = '2017', help='Please enter a year, default is 2017')
parser.add_option('-f', dest='folder', type=str, default = 'v3', help='Please enter a folder, default is v2')

(opt, args) = parser.parse_args()

username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])

path = "/eos/user/" + inituser + "/" + username + "/VBS/nosynch/"

dirlist = [dirs for dirs in os.listdir(path) if os.path.isdir(path+dirs) and opt.folder in dirs]
print dirlist

for dirn in dirlist:
    ismerged = False
    for nfile in os.listdir(path+dirn+"/"+os.listdir(path+dirn)[0]):
        if "_merged" in nfile:
            ismerged = True
            break
    
    if ismerged:
        continue

    print "python makeplot.py -y ", opt.year, " --merpart --folder ", dirn
    os.system("python makeplot.py -y " + opt.year + " --merpart --folder " + dirn)

