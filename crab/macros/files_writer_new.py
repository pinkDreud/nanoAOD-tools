# prende i path da path_writer (crab_paths.txt) e usando gfal-ls scorre su tutti i file e li salva su un file .txt
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
import os
import optparse

usage = 'python files_writer.py -d sample_name'
parser = optparse.OptionParser(usage)
parser.add_option('-d', '--dat', dest='dat', type=str, default = '', help='Please enter a dataset name')
(opt, args) = parser.parse_args()

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
    if not os.path.exists("./files/"):
        os.makedirs("./files/")
    f = open("./files/"+str(sample.label)+".txt", "w")
    url = os.popen('crab getoutput --xrootd --quantity="all" -d ' + path + '/crab_' + str(sample.label) + '/').readlines()#[0]
    #url = os.popen('crab getoutput --xrootd --jobids=1 -d ' + path + '/crab_' + str(sample.label) + '/').readlines()[0]
    
    print("Printing out crabbed files for "+str(sample.label))
    for u in url:
        #f.write
        if 'root' not in u:
            npaths = int(u.split("for ")[-1].split(" ")[0])

            finished = False
            rang = 500
            t = 0
            while not finished:
                intmin = int(t*500+1)
                intmax = int(min((t+1)*500, npaths))
                crabgo = str(intmin)+'-'+str(intmax)
                curl = os.popen('crab getoutput --xrootd --jobids=' + str(crabgo) + ' -d ' + path + '/crab_' + str(sample.label) + '/').readlines()
                for cu in curl:
                    f.write(cu)
                if intmax == npaths:
                    finished = True
                t+=1
                
            break
        else:
            f.write(u)
f.close()
