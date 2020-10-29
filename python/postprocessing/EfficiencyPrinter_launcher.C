#include "EfficiencyPrinter.C"





void EfficiencyPrinter_launcher(){
    
    string dirTot={"/eos/home-a/apiccine/VBS/nosynch/tageff/"};
    
    vector<string> dirSamples={
        "DY1JetsToLL_2017/",
        "DY2JetsToLL_2017/",
        "DY3JetsToLL_2017/",
        "DY4JetsToLL_2017/",
        "TT_DiLep_2017/",
        "TT_Had_2017/",
        "TT_SemiLep2017/",
        "WJetsHT100to200_2017/",
        "WJetsHT1200to2500_2017/",
        "WJetsHT200to400_2017/",
        "WJetsHT2500toInf_2017/",
        "WJetsHT400to600_2017/",
        "WJetsHT600to800_2017/",
        "WJetsHT70to100_2017/",
        "WJetsHT800to1200_2017/",
        "WpWpJJ_EWK_2017/",
        "WpWpJJ_QCD_2017/",
        "WZ_2017/"
    };

    vector<string> sampleNames={
        "DY1JetsToLL_2017_merged.root",
        "DY2JetsToLL_2017_merged.root",
        "DY3JetsToLL_2017_merged.root",
        "DY4JetsToLL_2017_merged.root",
        "TT_DiLep_2017_merged.root",
        "TT_Had_2017_merged.root",
        "TT_SemiLep2017_merged.root",
        "WJetsHT100to200_2017_merged.root",
        "WJetsHT1200to2500_2017_merged.root",
        "WJetsHT200to400_2017_merged.root",
        "WJetsHT2500toInf_2017_merged.root",
        "WJetsHT400to600_2017_merged.root",
        "WJetsHT600to800_2017_merged.root",
        "WJetsHT70to100_2017_merged.root",
        "WJetsHT800to1200_2017_merged.root",
        "WpWpJJ_EWK_2017_merged.root",
        "WpWpJJ_QCD_2017_merged.root",
        "WZ_2017_merged.root"
    };

    for(int i=sampleNames.size()-1; i<sampleNames.size(); i++){
        string totPath=dirTot+dirSamples[i]+sampleNames[i];
        //cout << totPath << endl;
        EfficiencyPrinter(totPath);

    }



}
