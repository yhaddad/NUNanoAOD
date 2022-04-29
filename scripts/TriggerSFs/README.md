# b-tagging efficiency calculation

```trig_all.ipynb``` and ```trig_all_2016.ipynb``` read data and MC samples and fill histograms of leading and trailing lepton pT. These notebooks run on [coffea.casa](https://coffea.casa).<br>
```trig_SF.py``` reads the output of ```btag_all.ipynb``` and save calculated trigger scale factors in ROOT files. To run the script, do ```python3 trig_SF.py 2016```

There are two separate scripts because ROOT propagates errors in histogram divisions, but [coffea.casa](https://coffea.casa) doesn't have ROOT.
