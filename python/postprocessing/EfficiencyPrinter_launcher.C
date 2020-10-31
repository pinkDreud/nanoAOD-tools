#include "EfficiencyPrinter.C"

double xSecFinder(string SampleName, int year){
    map<string, double> SampleMap2017;
    SampleMap2017.insert(pair<string, double>("DY1JetsToLL", 877.8));
    SampleMap2017.insert(pair<string, double>("DY2JetsToLL", 304.4));
    SampleMap2017.insert(pair<string, double>("DY3JetsToLL", 111.4));
    SampleMap2017.insert(pair<string, double>("DY4JetsToLL", 44.03));
    SampleMap2017.insert(pair<string, double>("TT_DiLep", 72.1));
    SampleMap2017.insert(pair<string, double>("TT_Had", 377.96));
    SampleMap2017.insert(pair<string, double>("TT_SemiLep", 365.34));
    SampleMap2017.insert(pair<string, double>("WJetsHT70to100", 1292*1.21));
    SampleMap2017.insert(pair<string, double>("WJetsHT100to200", 1395*1.21));
    SampleMap2017.insert(pair<string, double>("WJetsHT200to400", 407.9*1.21));
    SampleMap2017.insert(pair<string, double>("WJetsHT400to600", 57.48*1.21));
    SampleMap2017.insert(pair<string, double>("WJetsHT600to800", 12.87*1.21));
    SampleMap2017.insert(pair<string, double>("WJetsHT800to1200", 5.366*1.21));
    SampleMap2017.insert(pair<string, double>("WJetsHT1200to2500", 1.074*1.21));
    SampleMap2017.insert(pair<string, double>("WJetsHT2500toInf", 0.008001*1.21));
    SampleMap2017.insert(pair<string, double>("WpWpJJ_EWK", 0.0287));
    SampleMap2017.insert(pair<string, double>("WpWpJJ_QCD", 0.02227));
    SampleMap2017.insert(pair<string, double>("/WZ", 27.6));
    auto itr=SampleMap2017.begin();
    for(itr; itr!=SampleMap2017.end(); ++itr){
        
        cout << itr->first << endl;
        size_t found=(SampleName).find(itr->first);
        if(found!=std::string::npos) return itr->second;
    }
    return -1;
};



void EfficiencyPrinter_launcher(){
    
    string dirTot={"/eos/home-a/apiccine/VBS/nosynch/"};

    vector<string> dirWP={
        "Eff_JetM_MuL_EleVL/",
        "Eff_JetT_MuL_EleVL/",
        "Eff_JetVT_MuL_EleVL/",
        "Eff_JetM_MuVL_EleL/",
        "Eff_JetT_MuVL_EleL/",
        "Eff_JetVT_MuVL_EleL/",
        "Eff_JetM_MuL_EleL/",
        "Eff_JetT_MuL_EleL/",
        "Eff_JetVT_MuL_EleL/"
    };

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

    for(int j=0; j<dirWP.size(); j++){

        for(int i=0; i<sampleNames.size(); i++){
            string totPath=dirTot+dirWP[j]+dirSamples[i]+sampleNames[i];
            //cout << totPath << endl;
            //EfficiencyPrinter(totPath);
            cout << totPath << endl;
            cout << xSecFinder(totPath, 2017)<< endl;
        }
    }


}
