import ROOT
import sys


def make_SF(lep_cat, det_cat, f_in):
    # MC efficiency
    h_eff_MC = f_in.Get(f'h_num_{lep_cat}_{det_cat}_TT').Clone('h_eff_MC')
    h_den_MC = f_in.Get(f'h_den_{lep_cat}_{det_cat}_TT').Clone('h_den_MC')
    h_eff_MC.Divide(h_den_MC)

    # Data efficiency
    h_eff_Data = f_in.Get(f'h_num_{lep_cat}_{det_cat}_data_MET').Clone('h_eff_Data')
    h_den_Data = f_in.Get(f'h_den_{lep_cat}_{det_cat}_data_MET').Clone('h_den_Data')
    h_eff_Data.Divide(h_den_Data)

    # scale factor
    h_SF = h_eff_Data.Clone(f'trgSF{lep_cat}{det_cat}')
    h_SF.Divide(h_eff_MC)

    return h_SF


def make_SF_2016(lep_cat, det_cat, f_in):
    # https://twiki.cern.ch/twiki/bin/view/CMS/PdmVDatasetsUL2016
    k_pre = 19.5 / (19.5 + 16.8)
    k_after = 16.8 / (19.5 + 16.8)

    # MC efficiency pre APV
    h_eff_MC_pre = f_in.Get(f'h_num_{lep_cat}_{det_cat}_TT_pre').Clone('h_eff_MC_pre')
    h_den_MC_pre = f_in.Get(f'h_den_{lep_cat}_{det_cat}_TT_pre').Clone('h_den_MC_pre')
    h_eff_MC_pre.Divide(h_den_MC_pre)

    # MC efficiency after APV
    h_eff_MC_after = f_in.Get(f'h_num_{lep_cat}_{det_cat}_TT_post').Clone('h_eff_MC_after')
    h_den_MC_after = f_in.Get(f'h_den_{lep_cat}_{det_cat}_TT_post').Clone('h_den_MC_after')
    h_eff_MC_after.Divide(h_den_MC_after)

    # combine pre and after
    h_eff_MC_pre.Scale(k_pre)
    h_eff_MC_after.Scale(k_after)
    h_eff_MC = h_eff_MC_pre.Clone('h_eff_MC')
    h_eff_MC.Add(h_eff_MC_after)

    # Data efficiency
    h_eff_Data = f_in.Get(f'h_num_{lep_cat}_{det_cat}_data_MET').Clone('h_eff_Data')
    h_den_Data = f_in.Get(f'h_den_{lep_cat}_{det_cat}_data_MET').Clone('h_den_Data')
    h_eff_Data.Divide(h_den_Data)

    # scale factor
    h_SF = h_eff_Data.Clone(f'trgSF{lep_cat}{det_cat}')
    h_SF.Divide(h_eff_MC)

    return h_SF


def main():
    year = sys.argv[1]
    print('year', year)

    # files containing efficiencies
    f_in = ROOT.TFile.Open(f'TrigEff_{year}.root')
    # files to write scale factors
    f_out = ROOT.TFile.Open(f'histo_triggerEff_sel0_{year}.root', 'recreate')

    # SF as a function of lepton and detector categories
    lep_cats = ['EE', 'EM', 'ME', 'MM']
    det_cats = ['BB', 'BE', 'EB', 'EE']
    for lep_cat in lep_cats:
        for det_cat in det_cats:
            h_SF = make_SF_2016(lep_cat, det_cat, f_in) if year=='2016' else make_SF(lep_cat, det_cat, f_in)
            # save histograms
            f_out.WriteObject(h_SF, f'trgSF{lep_cat}{det_cat}')

    f_out.Close()
    f_in.Close()

    return 0


if __name__ == '__main__':
    main()

