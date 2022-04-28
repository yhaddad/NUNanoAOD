import ROOT
import sys


def make_eff(flavor, f_in):
    # MC efficiency
    h_eff = f_in.Get(f'h_num_{flavor[0]}').Clone(f'{flavor}_eff')
    h_den = f_in.Get(f'h_den_{flavor[0]}').Clone('h_den')
    h_eff.Divide(h_den)

    return h_eff


def main():
    year = sys.argv[1]
    print('year', year)

    # files containing efficiencies
    f_in = ROOT.TFile.Open(f'bTagEff_{year}.root')
    # files to write scale factors
    f_out = ROOT.TFile.Open(f'BTagEff_{year}.root', 'recreate')

    # calculate and write eff
    for flavor in ['bottom', 'charm', 'light']:
        h_eff = make_eff(flavor, f_in)
        f_out.WriteObject(h_eff, f'{flavor}_eff')

    f_out.Close()
    f_in.Close()

    return 0


if __name__ == '__main__':
    main()

