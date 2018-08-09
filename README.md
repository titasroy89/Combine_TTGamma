To run the fit for ZJets SF on the electron and muon channel separately simply run:

combine -M MultiDimFit datacard_ZJets_*.txt --saveFitResult

Following that run the fit to extract MisIDEle SF:

combine -M MultiDimFit datacard_EGamma.txt --saveFitResult


Finally after implementing the SFs derived from the previous fits in the combine input root file, follow instructions from https://cms-hcomb.gitbooks.io/combine/content/part3/nonstandard.html#nuisance-parameter-impacts
to run on datacard_electrons.txt and datacard_muons.txt. The combination datacard of the two channels is :combination.txt

The input root files listed in the datacard can be found in /uscms_data/d3/troy2012/Combine_TTGamma
