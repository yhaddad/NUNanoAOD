import uproot


HLT_2016 = {
    "DoubleMuon": [
        "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL",
        "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL",
        "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",
        "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ"
    ],
    "DoubleEG": [
        "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"
    ],
    "MuonEG": [
        "HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL",
        "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL",
        "HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL",
        "HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL",
        "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL"
    ],
    "SingleMuon": [
        "HLT_IsoMu20",
        "HLT_IsoTkMu20",
        "HLT_IsoMu22",
        "HLT_IsoTkMu22",
        "HLT_IsoMu24",
        "HLT_IsoTkMu24"
    ],
    "SingleElectron": [
        "HLT_Ele25_eta2p1_WPTight_Gsf",
        "HLT_Ele27_eta2p1_WPLoose_Gsf",
        "HLT_Ele27_WPTight_Gsf",
        "HLT_Ele35_WPLoose_Gsf"
    ]
}


def HLT_Selector(f_name, dataset, year):
    f = uproot.open(f_name)
    HLTs_available = [br for br in f['Events'].keys() if br[:4]=="HLT_"]

    HLTs = eval('HLT_' + str(year))
    HLTs_this = []
    HLTs_other = []
    for dataset_ in HLTs:
        HLTs[dataset_] = [HLT for HLT in HLTs[dataset_] if HLT in HLTs_available]
        if dataset_ == dataset:
            HLTs_this += HLTs[dataset_]
        else:
            HLTs_other += HLTs[dataset_]

    selection = '(' + ' || '.join(HLTs_this) + ') && !(' + ' || '.join(HLTs_other) + ')'
    return selection
