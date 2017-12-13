from ROOT import *
import math
import os
random=TRandom3()

_file  = TFile("/uscms_data/d3/troy2012/CMSSW_8_0_26_patch1/src/TTGammaSemiLep_13TeV/Plotting/histograms/mu/hists.root")
file0 = TFile("Step1_onlyMC.root","recreate")
file0.mkdir("M3")
file0.mkdir("ChHadIso")



channels={"M3":["M3",2],
          "M3_Prompt":["M3_Prompt",1],
          "M3_NonPrompt":["M3_NonPrompt",1],
	  "noCut_ChIso_PromptPhoton":["ChHad_Prompt",1],
          "noCut_ChIso_NonPromptPhoton":["ChHad_NonPrompt",1],
         }


process_samples ={"TTGamma":["TTGamma"],
	    	   "TTbar": ["TTbar"],
	           "VGamma":["ZGamma", "WGamma"],
	           "Other":[ "TTV", "TGJets", "SingleTop","WJets", "ZJets", "Diboson"],
	          }
process = ["TTGamma","TTbar","VGamma","Other"]	
HistDict={}
for c in channels:
	HistDict[c]={}
	for p in process_samples:
		 print "%s/phosel_%s_%s"%(process_samples[p][0],c,process_samples[p][0]) 
		 HistDict[c][p] = _file.Get("%s/phosel_%s_%s"%(process_samples[p][0],c,process_samples[p][0])).Clone("%s_%s"%(channels[c][0],p))
	  	 for s in process_samples[p][1:]:
			 HistDict[c][p].Add(_file.Get("%s/phosel_%s_%s"%(s,c,s)))
                 HistDict[c][p].Rebin(channels[c][1])


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

HistDict = makePseudoData(HistDict,process)

outputFile = TFile("Step3a_onlyMC.root","recreate")

for c in channels:
	if c=="M3":continue
        outputFile.mkdir(c)
        for p in process+["data_obs"]:
                outputFile.mkdir("%s/%s"%(channels[c][0],p))
                outputFile.cd("%s/%s"%(channels[c][0],p))
                HistDict[c][p].Write("nominal")


