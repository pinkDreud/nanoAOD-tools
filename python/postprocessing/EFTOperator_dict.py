#default value for anoinput 12 (FT1) is 2 TeV-4 --> no weighting for this value of the coefficient

EFT_operator_names = ["FS0", "FS1", "FM0", "FM1", "FM6", "FM7", "FT0", "FT1", "FT2"]

EFT_idx = {
    "-25": 0,  #weight for lowest value of the EFT coefficient operator in the LHEReweightingWeight array (-25 TeV-4)
    "-20": 1,  #weight for lowest value of the EFT coefficient operator in the LHEReweightingWeight array (-20 TeV-4)
    "-15": 2,  #weight for lowest value of the EFT coefficient operator in the LHEReweightingWeight array (-15 TeV-4)
    "-10": 3,  #weight for lowest value of the EFT coefficient operator in the LHEReweightingWeight array (-10 TeV-4)
    "-5": 4,  #weight for lowest value of the EFT coefficient operator in the LHEReweightingWeight array (-5 TeV-4)
    "0": 5,  #weight for lowest value of the EFT coefficient operator in the LHEReweightingWeight array (0 TeV-4)
    "+5": 6, #weight for the highest value of the EFT coefficient operator in the LHEReweightingWeight array (5 TeV-4)
    "+10": 7, #weight for the highest value of the EFT coefficient operator in the LHEReweightingWeight array (10 TeV-4)
    "+15": 8, #weight for the highest value of the EFT coefficient operator in the LHEReweightingWeight array (15 TeV-4)
    "+20": 9, #weight for the highest value of the EFT coefficient operator in the LHEReweightingWeight array (20 TeV-4)
    "+25": 10, #weight for the highest value of the EFT coefficient operator in the LHEReweightingWeight array (25 TeV-4)
}



EFT_operator = {
  "FS0":{
    "anoInput_number": 1,
    "idx": 1,
    "name": "FS0",
    "max": 25, #TeV^-4, 2.5 e-11 GeV^-4 
  },
  "FS1":{
    "anoInput_number": 2,
    "idx": 2,
    "name": "FS1",
    "max": 50, #TeV^-4, 0.5 e-10 GeV^-4 
  },
  "FM0":{
    "anoInput_number": 3,
    "idx": 3,
    "name": "FM0",
    "max": 25, #TeV^-4, 2.5 e-11 GeV^-4 
  },
  "FM1":{
    "anoInput_number": 4,
    "idx": 4,
    "name": "FM1",
    "max": 25, #TeV^-4, 2.5 e-11 GeV^-4 
  },
  "FM6":{
    "anoInput_number": 9,
    "idx": 5,
    "name": "FM6",
    "max": 25, #TeV^-4, 2.5 e-11 GeV^-4 
  },
  "FM7":{
    "anoInput_number": 10,
    "idx": 6,
    "name": "FM7",
    "max": 50, #TeV^-4, 0.5 e-10 GeV^-4 
  },
  "FT0":{
    "anoInput_number": 11,
    "idx": 7,
    "name": "FT0",
    "max": 2.5, #TeV^-4, 2.5 e-12 GeV^-4 
  },
  "FT1":{
    "anoInput_number": 12,
    "idx": 8,
    "name": "FT1",
    "max": 1, #TeV^-4, 1 e-12 GeV^-4
  },
  "FT2":{
    "anoInput_number": 13,
    "idx": 9,
    "name": "FT2",
    "max": 2.5, #TeV^-4, 2.5 e-12 GeV^-4 
  },
}


