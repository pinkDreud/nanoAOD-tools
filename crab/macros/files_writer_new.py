#prende i path da path_writer (crab_paths.txt) e usando gfal-ls scorre su tutti i file e li salva su un file .txt
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
import os
import optparse

usage = 'python files_writer.py -d sample_name --fake -t trig_tag'
parser = optparse.OptionParser(usage)
parser.add_option('-d', '--dat', dest='dat', type=str, default = '', help='Please enter a dataset name')
parser.add_option('--fake', dest = 'fake', default = False, action = 'store_true', help = 'Default runs analysis')
parser.add_option('-t', '--trig', dest='trig', type=str, default = 'Lep', help='Please enter a trigger path')
(opt, args) = parser.parse_args()

print "Is Fake?", opt.fake

if not (opt.trig == "Lep" or opt.trig == "Tau" or opt.trig == "HT"):
    raise ValueError

dirtag = "_Fake" + opt.trig + "/"

if not(opt.dat in sample_dict.keys()):
    print sample_dict.keys()
dataset = sample_dict[opt.dat]
samples = []

if hasattr(dataset, 'components'): # How to check whether this exists or not
    samples = [sample for sample in dataset.components]# Method exists and was used.
else:
    print "You are launching a single sample and not an entire bunch of samples"
    samples.append(dataset)

path = ".."

for sample in samples:
    dirpath = "./files/"
    crabdir = "/crab_" + str(sample.label)
    if opt.fake:
        if "DataEleB" in sample.label or "DataMuB" in sample.label:
            continue
        dirpath = dirpath + "Fake/" + opt.trig + "/"
        crabdir = crabdir + dirtag
    else:
        crabdir = crabdir + "/"

    print "Saving txts in ", dirpath, "\t CrabDir:", crabdir

    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    f = open(dirpath+str(sample.label)+".txt", "w")
    url = os.popen('crab getoutput --xrootd --quantity="all" -d ' + path + crabdir).readlines()

    print("Printing out crabbed files for "+str(sample.label))

    url_dict = {}
    for u in url:
        if 'root' not in u:
            print "Let's split requests to make crab getoutput happy..."
            #print u.split("for ")[-1].split(" ")[0]
            try:
                npaths = int(u.split("for ")[-1].split(" ")[0])
            except:
                continue

            finished = False
            rang = 500
            t = 0
            while not finished:
                intmin = int(t*500+1)
                intmax = int(min((t+1)*500, npaths))
                crabgo = str(intmin)+'-'+str(intmax)
                print 'Finding rootfile produced by jobs', str(crabgo), "..."
                curl = os.popen('crab getoutput --xrootd --jobids=' + str(crabgo) + ' -d ' + path + crabdir).readlines()
                
                cidx = 0
                while cidx < len(curl):
                    cu = curl[cidx]
                    if cu.startswith('The job with id '):
                        cu_err = int(cu.split('The job with id ')[-1].split(' is not')[0])
                        print cu_err, " is missing, retrying without considering it..."
                        crabgo_err = str(intmin) + "-" + str(cu_err-1) + "," + str(cu_err+1) + "-" + str(intmax)
                        print 'Finding rootfile produced by jobs', str(crabgo_err), "..."
                        curl = os.popen('crab getoutput --xrootd --jobids=' + str(crabgo_err) + ' -d ' + path + crabdir).readlines()
                        continue
                    else:
                        if 'hadd_' in cu:
                            idx = int(cu.split("hadd_")[-1].split(".")[0])
                        else:
                            continue

                        url_dict[idx] = cu
                        cidx += 1

                if intmax == npaths:
                    finished = True
                t+=1
            break

        else:
            idx = int(u.split("hadd_")[-1].split(".")[0])
            url_dict[idx] = u

    for u_idx in range(len(url_dict)):
        ru_idx = u_idx + 1
        try:
            f.write(url_dict[ru_idx])
        except:
            continue

    f.close()
