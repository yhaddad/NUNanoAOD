# b-tagging efficiency calculation

```btag_all.ipynb``` reads MC samples and fills histograms of pT and &eta;. This notebook runs on [coffea.casa](coffea.casa).
```bTag_Eff.py``` reads the output of ```btag_all.ipynb``` and save calculated b-tagging efficiencies in ROOT files. To run the script, do ```python3 bTag_Eff.py 2016```

There are two separate scripts because ROOT propagates errors in histogram divisions, but [coffea.casa](coffea.casa) doesn't have ROOT.
