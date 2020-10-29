#include "TFile.h"
#include "TH1F.h"
#include "TTreeReader.h"
#include "TTreeReaderValue.h"
#include <iostream>

using namespace std;


void EfficiencyPrinter(TString filename="/eos/home-a/apiccine/VBS/nosynch/tageff/WpWpJJ_EWK_2017/WpWpJJ_EWK_2017_merged.root")
{
    
    int passCuts[10]    =   {0,0,0,0,0,0,0,0,0,0};    
    vector<double> eff;
    string cutNames[10] =   {
        "Total events ",
        "Trigger      ",
        "lep selection",
        "lep veto     ",
        "tau selection",
        "lep/tau ss   ",
        "jet selection",
        "b veto       ",
        "mjj>500 GeV  ",
        "MET>40 GeV   "
    };
//    TFile *fin  =   TFile::Open("/eos/home-a/apiccine/VBS/nosynch/tageff/WpWpJJ_EWK_2017/WpWpJJ_EWK_2017_merged.root");
    TFile*fin =TFile::Open(filename);
    TTreeReader fReader("events_all", fin);  //!the tree reader
    
    // Readers to access the data (delete the ones you do not need).
    TTreeReaderArray<Float_t> w_nominal = {fReader, "w_nominal"};
    TTreeReaderArray<Float_t> lepSF = {fReader, "lepSF"};
    TTreeReaderArray<Float_t> lepUp = {fReader, "lepUp"};
    TTreeReaderArray<Float_t> lepDown = {fReader, "lepDown"};
    TTreeReaderArray<Float_t> puSF = {fReader, "puSF"};
    TTreeReaderArray<Float_t> puUp = {fReader, "puUp"};
    TTreeReaderArray<Float_t> puDown = {fReader, "puDown"};
    TTreeReaderArray<Float_t> PFSF = {fReader, "PFSF"};
    TTreeReaderArray<Float_t> PFUp = {fReader, "PFUp"};
    TTreeReaderArray<Float_t> PFDown = {fReader, "PFDown"};
    TTreeReaderArray<Float_t> q2Up = {fReader, "q2Up"};
    TTreeReaderArray<Float_t> q2Down = {fReader, "q2Down"};
    TTreeReaderArray<Float_t> lepton_pt = {fReader, "lepton_pt"};
    TTreeReaderArray<Float_t> lepton_eta = {fReader, "lepton_eta"};
    TTreeReaderArray<Float_t> lepton_phi = {fReader, "lepton_phi"};
    TTreeReaderArray<Float_t> lepton_mass = {fReader, "lepton_mass"};
    TTreeReaderArray<Int_t> lepton_pdgid = {fReader, "lepton_pdgid"};
    TTreeReaderArray<Float_t> lepton_pfRelIso03 = {fReader, "lepton_pfRelIso03"};
    TTreeReaderArray<Float_t> tau_pt = {fReader, "tau_pt"};
    TTreeReaderArray<Float_t> tau_eta = {fReader, "tau_eta"};
    TTreeReaderArray<Float_t> tau_phi = {fReader, "tau_phi"};
    TTreeReaderArray<Float_t> tau_mass = {fReader, "tau_mass"};
    TTreeReaderArray<Float_t> Leadjet_pt = {fReader, "Leadjet_pt"};
    TTreeReaderArray<Float_t> Leadjet_eta = {fReader, "Leadjet_eta"};
    TTreeReaderArray<Float_t> Leadjet_phi = {fReader, "Leadjet_phi"};
    TTreeReaderArray<Float_t> Leadjet_mass = {fReader, "Leadjet_mass"};
    TTreeReaderArray<Float_t> Leadjet_CSVv2_b = {fReader, "Leadjet_CSVv2_b"};
    TTreeReaderArray<Float_t> Leadjet_DeepFlv_b = {fReader, "Leadjet_DeepFlv_b"};
    TTreeReaderArray<Float_t> Leadjet_DeepCSVv2_b = {fReader, "Leadjet_DeepCSVv2_b"};
    TTreeReaderArray<Float_t> Subleadjet_pt = {fReader, "Subleadjet_pt"};
    TTreeReaderArray<Float_t> Subleadjet_eta = {fReader, "Subleadjet_eta"};
    TTreeReaderArray<Float_t> Subleadjet_phi = {fReader, "Subleadjet_phi"};
    TTreeReaderArray<Float_t> Subleadjet_mass = {fReader, "Subleadjet_mass"};
    TTreeReaderArray<Float_t> Subleadjet_CSVv2_b = {fReader, "Subleadjet_CSVv2_b"};
    TTreeReaderArray<Float_t> Subleadjet_DeepFlv_b = {fReader, "Subleadjet_DeepFlv_b"};
    TTreeReaderArray<Float_t> Subleadjet_DeepCSVv2_b = {fReader, "Subleadjet_DeepCSVv2_b"};
    TTreeReaderArray<Float_t> MET_pt = {fReader, "MET_pt"};
    TTreeReaderArray<Float_t> MET_eta = {fReader, "MET_eta"};
    TTreeReaderArray<Float_t> MET_phi = {fReader, "MET_phi"};
    TTreeReaderArray<Float_t> MET_mass = {fReader, "MET_mass"};
    TTreeReaderArray<Int_t> pass_lepton_selection = {fReader, "pass_lepton_selection"};
    TTreeReaderArray<Int_t> pass_lepton_veto = {fReader, "pass_lepton_veto"};
    TTreeReaderArray<Int_t> pass_tau_selection = {fReader, "pass_tau_selection"};
    TTreeReaderArray<Int_t> pass_charge_selection = {fReader, "pass_charge_selection"};
    TTreeReaderArray<Int_t> pass_jet_selection = {fReader, "pass_jet_selection"};
    TTreeReaderArray<Int_t> pass_b_veto = {fReader, "pass_b_veto"};
    TTreeReaderArray<Int_t> pass_mjj_cut = {fReader, "pass_mjj_cut"};
    TTreeReaderArray<Int_t> pass_MET_cut = {fReader, "pass_MET_cut"};
    TTreeReaderArray<Float_t> w_PDF = {fReader, "w_PDF"};

    while(fReader.Next())
    {
        passCuts[1]++;
        if(pass_lepton_selection[0]==1)     passCuts[2]++;
        else continue;
        if(pass_lepton_veto[0]==1)          passCuts[3]++;
        else continue;
        if(pass_tau_selection[0]==1)        passCuts[4]++;
        else continue;    
        if(pass_charge_selection[0]==1)     passCuts[5]++;
        else continue;
        if(pass_jet_selection[0]==1)        passCuts[6]++;
        else continue;
        if(pass_b_veto[0]==1)               passCuts[7]++;
        else continue;
        if(pass_mjj_cut[0]==1)              passCuts[8]++;
        else continue;
        if(pass_MET_cut[0]==1)              passCuts[9]++;
        else continue;
    }
    
    TH1F* h=(TH1F*)fin->Get("h_genweight"); 
    long nev = h->GetBinContent(1);
    passCuts[0]=nev;

    cout << filename << endl;
    for(int i=0; i<10; i++){
        cout << cutNames[i] << "\t" <<passCuts[i]<< endl;
    
    }

    cout << endl<< endl<< endl;

}


