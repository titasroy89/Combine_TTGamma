from ROOT import *
import math
import os
random=TRandom3()

_file  = TFile("/uscms_data/d3/troy2012/CMSSW_8_0_26_patch1/src/TTGammaSemiLep_13TeV/Plotting/histograms/mu/hists.root")
file0 = TFile("Step1_onlyMC.root","recreate")
file0.mkdir("M3")
file0.mkdir("ChHadIso")

misIDEleSF = 1.



observables={"M3": ["M3",5],
	  "ChHad":["noCut_ChIso",1],
           }

process = {"TTGamma_Prompt":["TTGamma"],
	   "TTGamma_NonPrompt":["TTGamma"],
           "TTbar_Prompt": ["TTbar"],
           "TTbar_NonPrompt": ["TTbar"],
           "VGamma_Prompt":["ZGamma", "WGamma"],
           "VGamma_NonPrompt":["ZGamma", "WGamma"],
           "Other_Prompt":[ "TTV", "TGJets", "SingleTop","WJets", "ZJets", "Diboson"],
           "Other_NonPrompt":[ "TTV", "TGJets", "SingleTop","WJets", "ZJets", "Diboson"],
	}	
HistDict={}
for obs in observables:
        #print "now doing", obs	
	HistDict[obs]={}
	for p in process:
		 s = process[p][0]
        #         print "%s_%s"%(observables[obs][0],p)
	#	 print s
	#	 print "%s/phosel_%s_%s"%(s,obs,s)

		 if "_Prompt" in p:
			 HistDict[obs][p]   = _file.Get("%s/phosel_%s_GenuinePhoton_%s"%(s,observables[obs][0],s)).Clone("%s_%s"%(obs,p))
			 HistDict[obs][p].Add(_file.Get("%s/phosel_%s_MisIDEle_%s"%(s,observables[obs][0],s)),misIDEleSF)
		 if "_NonPrompt" in p:
			 HistDict[obs][p]   = _file.Get("%s/phosel_%s_HadronicPhoton_%s"%(s,observables[obs][0],s)).Clone("%s_%s"%(obs,p))
			 HistDict[obs][p].Add(_file.Get("%s/phosel_%s_HadronicFake_%s"%(s,observables[obs][0],s)))
		 		 	
	  	 for s in process[p][1:]:
	#		 print s
			 if "_Prompt" in p:
				 HistDict[obs][p].Add(_file.Get("%s/phosel_%s_GenuinePhoton_%s"%(s,observables[obs][0],s)))
				 HistDict[obs][p].Add(_file.Get("%s/phosel_%s_MisIDEle_%s"%(s,observables[obs][0],s)),misIDEleSF)
			 if "_NonPrompt" in p:
				 HistDict[obs][p].Add(_file.Get("%s/phosel_%s_HadronicPhoton_%s"%(s,observables[obs][0],s)))
				 HistDict[obs][p].Add(_file.Get("%s/phosel_%s_HadronicFake_%s"%(s,observables[obs][0],s)))


                 HistDict[obs][p].Rebin(observables[obs][1])



#print process.keys()	

	
	
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

HistDict = makePseudoData(HistDict,process.keys())

outputFile = TFile("Step3b_onlyMC.root","recreate")

for obs in observables:
	
        outputFile.mkdir(obs)
        for p in process.keys()+["data_obs"]:
                outputFile.mkdir("%s/%s"%(obs,p))
                outputFile.cd("%s/%s"%(obs,p))
                HistDict[obs][p].Write("nominal")


