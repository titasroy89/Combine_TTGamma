from ROOT import *
import math
import os
random=TRandom3(0)

_file  = TFile("/uscms_data/d3/troy2012/CMSSW_8_0_26_patch1/src/TTGammaSemiLep_13TeV/Plotting/histograms/ele/hists_looseCR1.root")
#file0 = TFile("Step1a_onlyMC.root","recreate")
#file0.mkdir("M3")
#file0.mkdir("ChHadIso")


channels={"EGamma":["MassEGammaMisIDEle","MassEGammaOthers",4],
         }

process_samples ={"Signal":["ZJets","ZGamma","TTGamma","TTbar","WGamma","TTV", "TGJets", "SingleTop","WJets", "Diboson"],
	          "Bkg":[ "ZJets","ZGamma","TTGamma","TTbar","WGamma","TTV", "TGJets", "SingleTop","WJets", "Diboson"],
	          }

HistDict={}

for c in channels:
	HistDict[c]={}
	for p in process_samples:
		 
		 if p=="Signal":
			
		 	HistDict[c][p] = _file.Get("%s/phosel_%s_%s"%(process_samples[p][0],channels[c][0],process_samples[p][0])).Clone("%s_%s"%(channels[c][0],p))
		 else:
			HistDict[c][p] = _file.Get("%s/phosel_%s_%s"%(process_samples[p][0],channels[c][1],process_samples[p][0])).Clone("%s_%s"%(channels[c][1],p))
	  	 for s in process_samples[p][1:]:
			if p=="Signal":
				HistDict[c][p].Add(_file.Get("%s/phosel_%s_%s"%(s,channels[c][0],s)))
			else:
				HistDict[c][p].Add(_file.Get("%s/phosel_%s_%s"%(s,channels[c][1],s)))
                 HistDict[c][p].Rebin(channels[c][2])


print  HistDict
		
	
def makePseudoData(HistDict,processList,processScales = None):

        if processScales==None :processScales = [1.]*len(processList)
        if not len(processList)==len(processScales):
                print "different length of process list and process scales, ignoring scales"
                processScales = [1.]*len(processList)

        for c in HistDict:
                HistDict[c]["data_obs"] = HistDict[c][processList[0]].Clone("%s_data_obs"%c)
                HistDict[c]["data_obs"].Scale(processScales[0])
                for p,scale in zip(processList[1:],processScales[1:]):
                        HistDict[c]["data_obs"].Add(HistDict[c][p],scale)
                for b in range(1,HistDict[c]["data_obs"].GetNbinsX()+1):
                        HistDict[c]["data_obs"].SetBinContent(b,int(random.Poisson(HistDict[c]["data_obs"].GetBinContent(b))))
                        HistDict[c]["data_obs"].SetBinError(b,math.sqrt(HistDict[c]["data_obs"].GetBinContent(b)))
        return HistDict

HistDict = makePseudoData(HistDict,process_samples.keys())

outputFile = TFile("EGamma_CR2.root","recreate")

for c in list(channels)[:1]:
	print c
	outputFile.mkdir("%s/%s"%(c,"data_obs"))
        outputFile.cd("%s/%s"%(c,"data_obs"))
        HistDict[c]["data_obs"].Write("nominal")
        #outputFile.mkdir(obs)

        outputFile.mkdir(c)
        for p in process_samples:#+["data_obs"]:
                outputFile.mkdir("%s/%s"%(c,p))
                outputFile.cd("%s/%s"%(c,p))
                HistDict[c][p].Write("nominal")


