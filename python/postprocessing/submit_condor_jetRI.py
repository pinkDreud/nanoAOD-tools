from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
import os
import optparse
import sys


usage = 'python submit_condor.py -d dataset_name -f destination_folder --wp working_point'
parser = optparse.OptionParser(usage)
parser.add_option('-d', '--dat', dest='dat', type=str, default = '', help='Please enter a dataset name')
parser.add_option('-f', '--folder', dest='folder', type=str, default = '', help='Please enter a destination folder')
parser.add_option('--wp', dest='wp', type=str, default = '', help='Please enter working point!')
parser.add_option('--max', dest='maxj', type=int, default = 0, help='Please enter working point!')
#parser.add_option('-u', '--user', dest='us', type='string', default = 'ade', help="")
(opt, args) = parser.parse_args()
#Insert here your uid... you can see it typing echo $uid

username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])
if username == 'mmagheri':
    uid = 102889
elif username == 'apiccine':
    uid = 124949
elif username == 'ttedesch':
    uid = 103343

def sub_writer(sample, n, files, folder):
    f = open("condor_jetRI.sub", "w")
    f.write("Proxy_filename          = x509up\n")
    f.write("Proxy_path              = /afs/cern.ch/user/" + inituser + "/" + username + "/private/$(Proxy_filename)\n")
    f.write("universe                = vanilla\n")
    f.write("x509userproxy           = $(Proxy_path)\n")
    f.write("use_x509userproxy       = true\n")
    f.write("should_transfer_files   = YES\n")
    f.write("when_to_transfer_output = ON_EXIT\n")
    f.write("transfer_input_files    = $(Proxy_path), samples/samples.py, skimtree_utils_ssWW_wFakes_jetRI.py, CutsAndValues_bu.py, FR_th2_ele.root, FR_th2_mu.root, FR_th2_tau.root, __init__.py\n")
    f.write("transfer_output_remaps  = \""+ sample.label + "_part" + str(n) + ".root=/eos/home-"+inituser + "/" + username+"/VBS/nosynch/" + folder + "/" + sample.label +"/"+ sample.label + "_part" + str(n) + ".root\"\n")
    f.write("+JobFlavour             = \"workday\"\n") # options are espresso = 20 minutes, microcentury = 1 hour, longlunch = 2 hours, workday = 8 hours, tomorrow = 1 day, testmatch = 3 days, nextweek     = 1 week
    f.write("executable              = tree_skimmer_ssWW_wFakes_jetRI.py\n")
    f.write("arguments               = " + sample.label + " " + str(n) + " " + str(files) + " remote" + "\n")
    #f.write("input                   = input.txt\n")
    f.write("output                  = condor_jetRI/output/"+ sample.label + "_" + opt.wp + "_part" + str(n) + ".out\n")
    f.write("error                   = condor_jetRI/error/"+ sample.label + "_" + opt.wp +  "_part" + str(n) + ".err\n")
    f.write("log                     = condor_jetRI/log/"+ sample.label + "_" + opt.wp +  "_part" + str(n) + ".log\n")

    f.write("queue\n")

if not(opt.dat in sample_dict.keys()):
    print sample_dict.keys()
dataset = sample_dict[opt.dat]
samples = []

if hasattr(dataset, 'components'): # How to check whether this exists or not
    samples = [sample for sample in dataset.components]# Method exists and was used.
else:
    print "You are launching a single sample and not an entire bunch of samples"
    samples.append(dataset)

if not os.path.exists("condor_jetRI/output"):
    os.makedirs("condor_jetRI/output")
if not os.path.exists("condor_jetRI/error"):
    os.makedirs("condor_jetRI/error")
if not os.path.exists("condor_jetRI/log"):
    os.makedirs("condor_jetRI/log")

if(uid == 0):
    print("Please insert your uid")
    exit()
if not os.path.exists("/tmp/x509up_u" + str(uid)):
    os.system('voms-proxy-init --rfc --voms cms -valid 192:00')
os.popen("cp /tmp/x509up_u" + str(uid) + " /afs/cern.ch/user/" + inituser + "/" + username + "/private/x509up")

folder = opt.folder
split = 50
#Writing the configuration file
for sample in samples:
    isMC = True
    opath = "/eos/home-" + inituser + "/" + username + "/VBS/nosynch/" + folder + "/" + sample.label + "/"
    if('Data' in sample.label):
        isMC = False
    if not os.path.exists(opath):
        os.makedirs(opath)
    f = open("../../crab/macros/files/" + sample.label + ".txt", "r")
    files_list = f.read().splitlines()
    print(str(len(files_list)))
    if(isMC):
        for i, files in enumerate(files_list):
            if opt.maxj > 0:
                if i > opt.maxj: break
            if os.path.exists(opath + sample.label + "_part" + str(i) + ".root"):
                continue
            sub_writer(sample, i, files, folder)
            os.popen('condor_submit condor_jetRI.sub')
            print('condor_submit condor_jetRI.sub')
            #os.popen("python tree_skimmer_ssWW.py " " + sample.label + " " + str(i) + " " + str(files))
            print("python tree_skimmer_ssWW_wFakes_jetRI.py " + sample.label + " " + str(i) + " " + str(files) + " remote")
    else:
        for i in range(len(files_list)/split+1):
            if os.path.exists(opath + sample.label + "_part" + str(i) + ".root"):
                continue
            extmax = int(min([split*(i+1), len(files_list)]))
            sub_writer(sample, i,  ",".join( e for e in files_list[split*i:extmax]), folder)
            print('condor_submit condor_jetRI.sub')
            os.popen('condor_submit condor_jetRI.sub')
            #os.popen("python tree_skimmer_ssWW.py " + sample.label + " " + str(i) + " " + ",".join( e for e in files_list[split*i:split*(i+1)]))
            print("python tree_skimmer_ssWW_wFakes_jetRI.py " + sample.label + " " + str(i) + " " + ",".join( e for e in files_list[split*i:extmax]) + " remote")
