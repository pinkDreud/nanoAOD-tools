from skimtree_utils import *
import ROOT

infile = "/eos/user/a/apiccine/VBS/nosynch/tageff/WpWpJJ_EWK_2017/WpWpJJ_EWK_2017_part4.root"
chain = ROOT.TChain('events_all')
chain.Add(infile)
tree = InputTree(chain)

for i in range(tree.GetEntries()):
    event       = Event(tree,i)
    passed = Object(event, "pass")#cosi carico tutti i pass_* in unico object
    print passed.lepton_selection# cosi ottengo pass_lepton_selection
