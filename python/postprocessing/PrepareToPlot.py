import os
import optparse
import sys
from samples.samples import *

usage = 'python3 PrepareToPlot.py -y year -f folder'
parser = optparse.OptionParser(usage)
parser.add_option('-y', dest='year', type=str, default = '2017', help='Please enter a year, default is 2017')
parser.add_option('-f', dest='folder', type=str, default = 'v20', help='Please enter a folder, default is v4')
parser.add_option('-c', dest='check', default = False, action = 'store_true', help='Default runs makeplot')
parser.add_option('-d', dest='dat', type=str, default = 'all', help='Default is all')
parser.add_option('--fake', dest='isfake', default = False, action = 'store_true', help='Default runs for analysis, true for fake ratio')
parser.add_option('--ct', dest='ct', type=str, default = '', help='Default is analysis, otherwise specified CT')

(opt, args) = parser.parse_args()

username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])

crabpath = ''
if opt.ct == 'HT':
    crabpath = "../../crab/macros/files/Fake/HT/"
else:
    crabpath = "../../crab/macros/files/"

#username = 'mmagheri'
#inituser = 'm'

ofolder = ''

#if opt.ct != '':
    #ofolder += "CT" + opt.ct + "_"

ofolder += opt.folder

path = "/eos/home-" + inituser + "/" + username + "/VBS/nosynch/" + ofolder + "/"

#dirlist = [dirs for dirs in os.listdir(path) if os.path.isdir(path+dirs) and opt.folder in dirs]
#datas = opt.dataset + "_" + opt.year

Debug = opt.check # True # False #
split = 50

def DoesSampleExist(samplename):
    if samplename+".txt" not in os.listdir(crabpath):
        return False
    else:
        return True

def AreAllCondored(samplename):
    storelist = [line for line in open(crabpath+samplename+".txt")]

    try:
        condoredlist = os.listdir(path+samplename)
    except:
        condoredlist = []

    if samplename+"_merged.root" in condoredlist:
        condoredlist.remove(samplename+"_merged.root")
    if samplename+".root" in condoredlist:
        condoredlist.remove(samplename+".root")

    lenstore = len(storelist)

    if 'Data' in samplename:
        remainder = int(lenstore%split)
        lenstore = int(lenstore/split)
        if remainder > 0:
            lenstore += 1

    if len(condoredlist) < lenstore:
        print("condored: ", len(condoredlist), "\tlenstore: ", lenstore)
        return False
    elif lenstore==0 and len(condoredlist)==0:
        print("Warning for", samplename, "False flag for crabbed files! need to recrab them")
        return False
    else:
        return True

#print dirlist

#for dirn in dirlist:
#exsamples = [d for d in os.listdir(path+dirn) if os.path.isdir(path+dirn+"/"+d)]
#print exsamples

for k, v in class_dict.items():
    ismerged = False
    doesexist = []
    merging = []

    kpath = path+k+"/"

    if k.startswith('Fake'):
        mergable = False
        for c in v.components:
            if os.path.exists(path + c.label + "/" + c.label + ".root"):
                mergable = True
            else:
                mergable = False
        
        if mergable:
            if Debug:
                print("python3 makeplot.py -y ", opt.year, " --mertree -d " + k + " --folder ", ofolder)
            else:
                os.system("python3 makeplot.py -y " + opt.year + " --mertree -d " + k + " --folder " + ofolder)
        else:
            print(k, "not mergable")
        continue

    if hasattr(v, 'components'):
        for c in v.components:
            if opt.dat != 'all':
                if not str(c.label).startswith(opt.dat):
                    if not k.startswith(opt.dat):
                        continue
            if not DoesSampleExist(c.label):
                print(c.label, "not crabbed yet")
                continue
            cpath = path + c.label + "/"
            if not AreAllCondored(c.label):
            #if not os.path.exists(cpath):
                print(c.label + " not condorly produced yet")
                continue

            doesexist.append(True)
            if True:#not os.path.exists(cpath+c.label+".root"):
                if os.path.exists(cpath+c.label+"_merged.root"):
                    if Debug:
                        print("rm -f " + cpath + c.label + "_merged.root")
                    else:
                        os.system("rm -f " + cpath + c.label + "_merged.root")
                print(c.label + " not merged so far")
                print("Merging and luming " + c.label + "...")
                merging.append(True)
                if Debug:
                    print("python3 makeplot.py -y " + opt.year + " --merpart --lumi -d " + c.label + " --folder " + ofolder)
                else:
                    os.system("python3 makeplot.py -y " + opt.year + " --merpart --lumi -d " + c.label + " --folder " + ofolder)
                print("Merged and lumied!")
            else:
                print(c.label + " is already merged and lumied")

        samplemerge = False

        #print len(doesexist), len(v.components)
        if len(doesexist) == len(v.components):
            if len(merging) == 0:
                if os.path.exists(kpath+k+".root"):
                    print(k + " already merged")
                    samplemerge = False
                else:
                    samplemerge = True
            else:
                samplemerge = True

            if samplemerge:
                if True:#os.path.exists(kpath+k+".root"):
                    if Debug:
                        print("rm -f "+kpath+k+".root")
                    else:
                        os.system("rm -f "+kpath+k+".root")
                if Debug:
                    print("python3 makeplot.py -y ", opt.year, " --mertree -d " + k + " --folder ", ofolder)
                else:
                    os.system("python3 makeplot.py -y " + opt.year + " --mertree -d " + k + " --folder " + ofolder)
        #else:
            #print k + "not ready to be merged"
    else:
        if opt.dat != 'all':
            if not k.startswith(opt.dat):
                continue
        if not DoesSampleExist(k):
            print(k + " not crabbed yet")
            continue
        if not AreAllCondored(k):
        #if not os.path.exists(kpath+k):
            print(k + " not condored at all yet")
            continue

        doesexist.append(True)
        if True:#not os.path.exists(kpath+k+".root"):
            if os.path.exists(kpath+k+"_merged.root"):
                if Debug:
                    print("rm -f " + kpath + k + "_merged.root")
                else:
                    os.system("rm -f " + kpath + k + "_merged.root")
            print(k + " neither merged nor lumied so far")
            print("Merging and luming " + k + "...")
            if Debug:
                print("python3 makeplot.py -y ", opt.year, " --merpart --lumi --mertree -d " + k + " --folder ", ofolder)
            else:
                os.system("python3 makeplot.py -y " + opt.year + " --merpart --lumi --mertree -d " + k + " --folder " + ofolder)
            print("Merged and lumied!")
        else:
            print(k + " is already merged and lumied")
