To run the fit for ZJets SF on the electron and muon channel separately simply run:

combine -M MultiDimFit datacard_ZJets_*.txt --saveFitResult

Following that run the fit to extract MisIDEle SF:

combine -M MultiDimFit datacard_EGamma.txt --saveFitResult


Finally after implementing the SFs derived from the previous fits in the combine input root file, follow instructions from https://cms-hcomb.gitbooks.io/combine/content/part3/nonstandard.html#nuisance-parameter-impacts
to run on datacard_electrons.txt and datacard_muons.txt. The combination datacard of the two channels is :combination.txt

The input root files listed in the datacard can be found in /uscms_data/d3/troy2012/Combine_TTGamma

Some more details about each fit and details about the datacard:

There are three different fits being done in the electron and muon channel separately.

Step 1: Fit to extract the ZJets SF: this is done to account for any mismodeling in ZJets prior to a fit to extract the misidentified electron SF
(where ZJets is the primary contributor)

datacard_ZJets_ele.txt and datacard_ZJets_mu.txt are the two files to do this. The variable is dilepton invariant mass. 
There is a signal(ZJets events) and a background(everything else). both freely floating, no systematics.
ZJets in the final fit (step3 described below) has an uncertainty of 30% assigned to it which covers the uncertainty derived from this fit.

Step 2 : Next the Fit to extract the misidentified SF (ZJets events are scaled by the SF derived in the previous fit).

datacard_EGamma.txt : Only done in the electron as the the variable is the invariant mass of electron and photon.
Signal(all misidentified electron events from every MC sample) and one background 
(all events that are not categorized as misidentified electron from all other MC sample).
both signal and bkg are free floating. No systematic uncertainties.
Uncertainty from this fit is a systematic uncertainty in the final simultaneous fit.

Step 3: Finally the fit to extract the signal strength. All relevant events are scaled by the SFs derived from previous fit before input in Combine.
There are separate datacards for electron and muons: datacard_Syst_ele_Fit4.txt and datacard_Syst_mu_Fit4.txt.

Signal=TTGamma (free floating), Bkg1= TTbar (uncertainty of 5.5% on xsection),
Bkg2 =VGamma  (uncertainty of 30% on xsection) ;

Bkg3=Other (SingleTop, W/ZJets, TTV, Diboson, Multijet)(uncertainty of 30% on xsection) ;
There are 4 channels in this fit: 
a) ChHad : Photon Charge Hadron Isolation
b) M3    : M3 in signal region
c) M3_control : M3 in 0-photon CR
d) Njet  : One bin with all events in a >=4jets,0btag CR to get a better handle on background W/ZGamma

ChHad, M3 and Njet has all signal and background samples divided into Prompt(Isolated) and NonPrompt samples. The misidentified electrons events scaled
by SF from Fit described in step 2 is part of Isolated photons.

A second free floating parameter : Hadronic_norm is a correction factor applied to all NonPrompt events.

Systematics:

Q2: only applied to ttgamma and ttbar\

PDF : This is only applied to ttgamma and ttbar. To study the individual affects on ttbar and ttgamma it is broken up:
Pdf refers to Pdf applied to ttbar and Pdfsignal refers to Pdf applied to ttgamma.
ISR/FSR: Only applied to ttgamma and ttbar. \

shapeDD: Ubcertainty on shape of data-driven templates for nonprompt samples in ChHad varaible.\

MisIDEleshape: Only applied to Isolated photon category for all MC as that category contains misidentified electrons.\

BTagSF: Not applied to Njet-> as it is a 0btag control region\

Any photon related systematic: Not applied to M3_control as it is a 0 photon control region


