//Macro to generate the TH2F associated to the fake ratio of electron and muons

void FakeRatio_printer_ele()
{
    Float_t lower_pt[6]={0, 20, 30, 40, 50, 60};
    Float_t lower_eta[5]={0, 1, 1.4, 2, 2.4};

    gStyle->SetOptStat(0);

    TH2F* hFR=new TH2F("h2FRele", "Electron fake ratio", 5, lower_pt, 4, lower_eta);
    
    hFR->SetBinContent(1,1,  0.186);
    hFR->SetBinContent(1,2,  0.211);
    hFR->SetBinContent(1,3,  0.280);
    hFR->SetBinContent(1,4,  0.356);

    hFR->SetBinContent(2,1,  0.030);
    hFR->SetBinContent(2,2,  0.033);
    hFR->SetBinContent(2,3,  0.047);
    hFR->SetBinContent(2,4,  0.095);

    hFR->SetBinContent(3,1,  0.017);
    hFR->SetBinContent(3,2,  0.019);
    hFR->SetBinContent(3,3,  0.036);
    hFR->SetBinContent(3,4,  0.075);

    hFR->SetBinContent(4,1,  0.012);
    hFR->SetBinContent(4,2,  0.005);
    hFR->SetBinContent(4,3,  0.047);
    hFR->SetBinContent(4,4,  0.095);

    hFR->SetBinContent(5,1,  0.051);
    hFR->SetBinContent(5,2,  0.074);
    hFR->SetBinContent(5,3,  0.122);
    hFR->SetBinContent(5,4,  0.149);

    hFR->GetXaxis()->SetTitle("p_{T} [GeV]");
    hFR->GetYaxis()->SetTitle("#eta");
    
    TFile f("TH2F_FakeRatio_ele.root", "recreate"); 
    hFR->Write();
    f.Close();
}

void FakeRatio_printer_mu()
{
    Float_t lower_pt[6]={0, 20, 30, 40, 50, 60};
    Float_t lower_eta[5]={0, 1, 1.4, 2, 2.4};

    gStyle->SetOptStat(0);

    TH2F* hFR=new TH2F("h2FRmu", "Muon fake ratio", 5, lower_pt, 4, lower_eta);
    
    hFR->SetBinContent(1,1,  0.419);
    hFR->SetBinContent(1,2,  0.424);
    hFR->SetBinContent(1,3,  0.494);
    hFR->SetBinContent(1,4,  0.582);

    hFR->SetBinContent(2,1,  0.117);
    hFR->SetBinContent(2,2,  0.102);
    hFR->SetBinContent(2,3,  0.098);
    hFR->SetBinContent(2,4,  0.205);

    hFR->SetBinContent(3,1,  0.104);
    hFR->SetBinContent(3,2,  0.0);
    hFR->SetBinContent(3,3,  0.092);
    hFR->SetBinContent(3,4,  0.053);

    hFR->SetBinContent(4,1,  0.086);
    hFR->SetBinContent(4,2,  0.067);
    hFR->SetBinContent(4,3,  0.049);
    hFR->SetBinContent(4,4,  0.058);

    hFR->SetBinContent(5,1,  0.086);
    hFR->SetBinContent(5,2,  0.108);
    hFR->SetBinContent(5,3,  0.097);
    hFR->SetBinContent(5,4,  0.082);
    
    hFR->GetXaxis()->SetTitle("p_{T} [GeV]");
    hFR->GetYaxis()->SetTitle("#eta");

    TFile f("TH2F_FakeRatio_mu.root", "recreate");
    hFR->Write();

    f.Close();
}

void FakeRatio_printer(){
    FakeRatio_printer_ele();
    FakeRatio_printer_mu();
}
