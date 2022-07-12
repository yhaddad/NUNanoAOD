import ROOT
import sys
from scipy.stats import beta


# significant level for efficiency uncertainty calculation
# conf_lev = 68.
conf_lev = 95.
sig_lev = 1 - conf_lev / 100


def set_eff_err(h_eff, h_num, h_den):
    # Use Clopper–Pearson interval for efficiency uncertainty
    for ix in range(1, h_eff.GetNbinsX() + 1):
        for iy in range(1, ix + 1):
            num = h_num.GetBinContent(ix, iy)
            den = h_den.GetBinContent(ix, iy)

            try:
                eff = num / den
            except Exception as e:
                # use defaul uncertainty from .Divide()
                continue

            # error bar not symmetric, e.g. when frac=0 there's no left error
            err_l = eff - beta.ppf(sig_lev / 2, num, den - num + 1)
            err_r = beta.ppf(1 - sig_lev / 2, num + 1, den - num) - eff

            # overestimating uncertainty (to be conservative)
            err_max = max(err_l, err_r)
            h_eff.SetBinError(ix, iy, err_max)

            # print(ix, iy, num, den, err_max)


def make_SF(lep_cat, det_cat, f_in):
    # MC efficiency
    h_num_MC = f_in.Get(f'h_num_{lep_cat}_{det_cat}_TT').Clone('h_num_MC')
    h_den_MC = f_in.Get(f'h_den_{lep_cat}_{det_cat}_TT').Clone('h_den_MC')
    h_eff_MC = h_num_MC.Clone('h_eff_MC')
    h_eff_MC.Divide(h_den_MC)
    set_eff_err(h_eff_MC, h_num_MC, h_den_MC)

    # Data efficiency
    h_num_Data = f_in.Get(f'h_num_{lep_cat}_{det_cat}_data_MET').Clone('h_num_Data')
    h_den_Data = f_in.Get(f'h_den_{lep_cat}_{det_cat}_data_MET').Clone('h_den_Data')
    h_eff_Data = h_num_Data.Clone('h_eff_Data')
    h_eff_Data.Divide(h_den_Data)
    set_eff_err(h_eff_Data, h_num_Data, h_den_Data)

    # scale factor
    h_SF = h_eff_Data.Clone(f'trgSF{lep_cat}{det_cat}')
    h_SF.Divide(h_eff_MC)

    # print('bin (4, 3)')
    # print('MC cont', h_eff_MC.GetBinContent(4, 3), 'MC err', h_eff_MC.GetBinError(4, 3))
    # print('Data cont', h_eff_Data.GetBinContent(4, 3), 'MC err', h_eff_Data.GetBinError(4, 3))
    # print('SF cont', h_SF.GetBinContent(4, 3), 'MC err', h_SF.GetBinError(4, 3))

    return h_SF


def make_SF_2016(lep_cat, det_cat, f_in):
    # https://twiki.cern.ch/twiki/bin/view/CMS/PdmVDatasetsUL2016
    k_pre = 19.5 / (19.5 + 16.8)
    k_after = 16.8 / (19.5 + 16.8)

    # MC efficiency pre APV
    h_num_MC_pre = f_in.Get(f'h_num_{lep_cat}_{det_cat}_TT_pre').Clone('h_num_MC_pre')
    h_den_MC_pre = f_in.Get(f'h_den_{lep_cat}_{det_cat}_TT_pre').Clone('h_den_MC_pre')
    h_eff_MC_pre = h_num_MC_pre.Clone('h_eff_MC_pre')
    h_eff_MC_pre.Divide(h_den_MC_pre)
    set_eff_err(h_eff_MC_pre, h_num_MC_pre, h_den_MC_pre)

    # MC efficiency after APV
    h_num_MC_post = f_in.Get(f'h_num_{lep_cat}_{det_cat}_TT_post').Clone('h_num_MC_post')
    h_den_MC_post = f_in.Get(f'h_den_{lep_cat}_{det_cat}_TT_post').Clone('h_den_MC_post')
    h_eff_MC_post = h_num_MC_post.Clone('h_eff_MC_post')
    h_eff_MC_post.Divide(h_den_MC_post)
    set_eff_err(h_eff_MC_post, h_num_MC_post, h_den_MC_post)

    # combine pre and after
    h_eff_MC_pre.Scale(k_pre)
    h_eff_MC_post.Scale(k_after)
    h_eff_MC = h_eff_MC_pre.Clone('h_eff_MC')
    h_eff_MC.Add(h_eff_MC_post)

    # Data efficiency
    h_num_Data = f_in.Get(f'h_num_{lep_cat}_{det_cat}_data_MET').Clone('h_num_Data')
    h_den_Data = f_in.Get(f'h_den_{lep_cat}_{det_cat}_data_MET').Clone('h_den_Data')
    h_eff_Data = h_num_Data.Clone('h_eff_Data')
    h_eff_Data.Divide(h_den_Data)
    set_eff_err(h_eff_Data, h_num_Data, h_den_Data)

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
            # print('\n'*3)
            # print(lep_cat, det_cat, f_in)
            h_SF = make_SF_2016(lep_cat, det_cat, f_in) if year=='2016' else make_SF(lep_cat, det_cat, f_in)
            # save histograms
            f_out.WriteObject(h_SF, f'trgSF{lep_cat}{det_cat}')

    f_out.Close()
    f_in.Close()

    return 0


if __name__ == '__main__':
    main()

