from ROOT import *
import math
import os
import sys
random=TRandom3(0)
luminosity = 35860
SFTTGamma_hadronic      =  (4.599*luminosity)/4966371.
SFTTGamma_semilept_Tbar = (4.499/2.)*luminosity/4836134.
SFTTGamma_semilept_T    = (4.499/2.)*luminosity/4791766.
SFTTGamma_dilept        =( 0.899*luminosity)/4907307.
SFTGJets                = (2.967*luminosity)/1556973.


SFTTbarPowheg    = (831.76*luminosity)/77227178.
SFW1jets           = (9493.0*luminosity)/45366416.
SFW2jets           = (3120.0*luminosity)/30318880.
SFW3jets           = (942.3*luminosity)/39268750.
SFW4jets           = (524.2*luminosity)/18751100.

SFDYjetsM50       = (5765.4*luminosity)/122053259.
SFDYjetsM10to50   = (18610.*luminosity)/71301217.

SFTTWtoQQ         = (0.40620*luminosity)/833257.
SFTTWtoLNu        = (0.2043*luminosity)/2160030.
SFTTZtoLL         = (0.2728*luminosity)/5933898.

SFZGamma           = 131.3*luminosity/(2307116. + 14372399.)
SFWGamma           = 585.8*luminosity/(5048404. + 10231838. + 12146594.)

SFWW               = (118.7*luminosity)/6987017.
SFWZ               = 47.13*luminosity/2995783.
SFZZ               = 16.523*luminosity/998018.

SFST_tchannel      = 136.02*luminosity/67225849.
SFST_tbarchannel   = 80.95*luminosity/38810350
SFST_schannel      = 10.32*luminosity/2989123.
SFST_tW            = 35.85*luminosity/6932903.
SFST_tbarW         = 35.85*luminosity/6932903.

_file  = TFile("/uscms_data/d3/troy2012/CMSSW_8_0_26_patch1/src/TTGammaSemiLep_13TeV/Plotting/histograms/mu/hists.root")

misIDEleSF = 1.
systematics=["Pileup","BTagSF","MuEff", "JEC","JER","lumi"]
HistDict={}
HistDict_up={}
HistDict_do={}
_file_up={}
_file_do={}
for sys in systematics:
	HistDict_up[sys]={}
	HistDict_do[sys]={}
        _file_up[sys]=TFile("/uscms_data/d3/troy2012/CMSSW_8_0_26_patch1/src/TTGammaSemiLep_13TeV/Plotting/histograms/mu/hists%s_up.root"%(sys))
        _file_do[sys]=TFile("/uscms_data/d3/troy2012/CMSSW_8_0_26_patch1/src/TTGammaSemiLep_13TeV/Plotting/histograms/mu/hists%s_down.root"%(sys))

#print _file_do
#sys.exit()

observables={"M3": ["M3",10],
	     "ChHad":["noCut_ChIso",1],
	     "M3_control":["M3_control",10]
           }

process_signal = {"TTGamma_Prompt":["TTGamma"],
	   "TTGamma_NonPrompt":["DataMu",SFTTGamma_hadronic,SFTTGamma_semilept_Tbar,SFTTGamma_semilept_T,SFTTGamma_dilept],
           "TTbar_Prompt": ["TTbar"],
           "TTbar_NonPrompt": ["DataMu",SFTTbarPowheg],
           "VGamma_Prompt":["ZGamma", "WGamma"],
           "VGamma_NonPrompt":["DataMu", SFZGamma,SFWGamma],
	   "SingleTop_Prompt":["TGJets", "SingleTop"],
	   "SingleTop_NonPrompt":["DataMu", SFST_tchannel,SFST_tbarchannel,SFST_schannel,SFST_tW,SFST_tbarW],
           "VJets_Prompt":["WJets", "ZJets"],
           "VJets_NonPrompt":["DataMu",SFW1jets,SFW2jets,SFW3jets,SFW4jets,SFDYjetsM10to50,SFDYjetsM50],
           "Other_Prompt":[ "TTV", "Diboson"],
           "Other_NonPrompt":[ "DataMu",SFTTWtoQQ,SFTTWtoLNu,SFTTZtoLL,SFWW,SFZZ,SFWZ],
	}
process_control ={"TTGamma":["TTGamma"],
		  "TTbar":  ["TTbar"],
		  "VGamma":["ZGamma", "WGamma"],
		  "VJets":["WJets", "ZJets"],
		  "SingleTop":["TGJets", "SingleTop"],
		  "Other":[ "TTV", "Diboson"],
		}	


process={}
for obs in observables:
        #print "now doing", obs	
	HistDict[obs]={}
	for sys in systematics:
		HistDict_up[sys][obs]={}
		HistDict_do[sys][obs]={}
        if obs=="M3_control":
		for p in process_control:
			s= process_control[p][0]
			HistDict[obs][p]   = _file.Get("%s/presel_%s_%s"%(s,observables[obs][0],s)).Clone("%s_%s"%(obs,p))
			#for sys in systematics:
			#	HistDict_up[sys][obs][p]= _file_up[sys].Get("%s/presel_%s_%s"%(s,observables[obs][0],s)).Clone("%s_%s"%(obs,p))
			#	HistDict_do[sys][obs][p]= _file_do[sys].Get("%s/presel_%s_%s"%(s,observables[obs][0],s)).Clone("%s_%s"%(obs,p))

			for s in process_control[p][1:]:
				HistDict[obs][p].Add(_file.Get("%s/presel_%s_%s"%(s,observables[obs][0],s)))
		         #	for sys in systematics:
	#				 print sys, _file_up[sys], 
	#				 print "%s/presel_%s_%s"%(s,observables[obs][0],s)
                                         
			#		 HistDict_up[sys][obs][p].Add(_file_up[sys].Get("%s/presel_%s_%s"%(s,observables[obs][0],s)))
			#		 HistDict_do[sys][obs][p].Add(_file_do[sys].Get("%s/presel_%s_%s"%(s,observables[obs][0],s)))
					
			HistDict[obs][p].Rebin(observables[obs][1])
                        #for sys in systematics:
                         #       HistDict_up[sys][obs][p].Rebin(observables[obs][1])
                          #      HistDict_do[sys][obs][p].Rebin(observables[obs][1])			
		
	else:
		

		for p in process_signal:
		 	s = process_signal[p][0]

		 	if "_Prompt" in p:
			 	if obs=="M3":
					HistDict[obs][p]   = _file.Get("%s/phosel_%s_GenuinePho_%s"%(s,observables[obs][0],s)).Clone("%s_%s"%(obs,p))
			 	else:
			 		HistDict[obs][p]   = _file.Get("%s/phosel_%s_GenuinePhoton_%s"%(s,observables[obs][0],s)).Clone("%s_%s"%(obs,p))
			 	HistDict[obs][p].Add(_file.Get("%s/phosel_%s_MisIDEle_%s"%(s,observables[obs][0],s)),misIDEleSF)
#				for sys in systematics:
#					if obs=="M3":
#						HistDict_up[sys][obs][p]= _file_up[sys].Get("%s/phosel_%s_GenuinePho_%s"%(s,observables[obs][0],s)).Clone("%s_%s"%(obs,p))
#						HistDict_do[sys][obs][p]= _file_do[sys].Get("%s/phosel_%s_GenuinePho_%s"%(s,observables[obs][0],s)).Clone("%s_%s"%(obs,p))
#					else:
#						print sys, "%s/phosel_%s_GenuinePhoton_%s"%(s,observables[obs][0],s)
#						print _file_up[sys]
		
#						HistDict_up[sys][obs][p]= _file_up[sys].Get("%s/phosel_%s_GenuinePhoton_%s"%(s,observables[obs][0],s)).Clone("%s_%s"%(obs,p))
#						HistDict_do[sys][obs][p]= _file_do[sys].Get("%s/phosel_%s_GenuinePhoton_%s"%(s,observables[obs][0],s)).Clone("%s_%s"%(obs,p))
#					HistDict_up[sys][obs][p].Add(_file_up[sys].Get("%s/phosel_%s_MisIDEle_%s"%(s,observables[obs][0],s)),misIDEleSF)
#					HistDict_do[sys][obs][p].Add(_file_do[sys].Get("%s/phosel_%s_MisIDEle_%s"%(s,observables[obs][0],s)),misIDEleSF)
													
			if "_NonPrompt" in p:
				o = observables[obs][0]
				if observables[obs][0]=="noCut_ChIso":
					o = "AntiSIEIE_ChIso"
			 	print "%s/phosel_%s_%s"%(s,o,s)
				print _file	
				HistDict[obs][p]=_file.Get("%s/phosel_%s_%s"%(s,o,s)).Clone("%s_%s"%(obs,p))
				HistDict[obs][p].Scale(process_signal[p][1])
                                #print p, process_signal[p][1]
				#HistDict[obs][p]=h1,process_signal[p][1])
				for s in process_signal[p][2:]:
					print s,obs,p
					HistDict[obs][p].Add(_file.Get("%s/phosel_%s_%s"%(process_signal[p][0],o,process_signal[p][0])),s)
				
	#			for sys in systematics:	
					
	#				h2= _file_up[sys].Get("%s/phosel_%s_%s"%(s,observables[obs][0],s)).Clone("%s_%s"%(obs,p))
	#				h3 = _file_do[sys].Get("%s/phosel_%s_%s"%(s,observables[obs][0],s)).Clone("%s_%s"%(obs,p))
	#				for s in process_signal[p][1:]:
						
	#					HistDict_up[sys][obs][p].Add(h2,s)
	#					HistDict_do[sys][obs][p].Add(h3,s)
			for s in process_signal[p][1:]:
				# print s
				if "_Prompt" in p:
					if obs=="M3":
						HistDict[obs][p].Add(_file.Get("%s/phosel_%s_GenuinePho_%s"%(s,observables[obs][0],s)))
					else:
						HistDict[obs][p].Add(_file.Get("%s/phosel_%s_GenuinePhoton_%s"%(s,observables[obs][0],s)))
					HistDict[obs][p].Add(_file.Get("%s/phosel_%s_MisIDEle_%s"%(s,observables[obs][0],s)),misIDEleSF)
					print "%s/phosel_%s_MisIDEle_%s"%(s,observables[obs][0],s)
					print HistDict[obs][p].Integral(-1,-1)
#					for sys in systematics:
					#	print sys, s
					#	print HistDict_up[sys][obs][p]
					#	print _file_up[sys].Get("%s/phosel_%s_GenuinePhoton_%s"%(s,observables[obs][0],s))					
#						if obs=="M3":
#							HistDict_up[sys][obs][p].Add(_file_up[sys].Get("%s/phosel_%s_GenuinePho_%s"%(s,observables[obs][0],s)))	
#							HistDict_do[sys][obs][p].Add(_file_do[sys].Get("%s/phosel_%s_GenuinePho_%s"%(s,observables[obs][0],s)))
#						else:
						#	print sys, _file_up[sys]
						#	print "%s/phosel_%s_GenuinePhoton_%s"%(s,observables[obs][0],s)
#						#	print HistDict_up[sys][obs][p]
#							HistDict_up[sys][obs][p].Add(_file_up[sys].Get("%s/phosel_%s_GenuinePhoton_%s"%(s,observables[obs][0],s)))
#							HistDict_do[sys][obs][p].Add(_file_do[sys].Get("%s/phosel_%s_GenuinePhoton_%s"%(s,observables[obs][0],s)))
#						HistDict_do[sys][obs][p].Add(_file_do[sys].Get("%s/phosel_%s_MisIDEle_%s"%(s,observables[obs][0],s)),misIDEleSF)
#						HistDict_up[sys][obs][p].Add(_file_up[sys].Get("%s/phosel_%s_MisIDEle_%s"%(s,observables[obs][0],s)),misIDEleSF)

			HistDict[obs][p].Rebin(observables[obs][1])
#			for sys in systematics:
#				if "_NonPrompt" in p:continue
#			       	HistDict_up[sys][obs][p].Rebin(observables[obs][1])
#				HistDict_do[sys][obs][p].Rebin(observables[obs][1])



#print process.keys()	

	
	
def makePseudoData(HistDict,processList,variables,processScales = None):
	print processList
        if processScales==None :processScales = [1.]*len(processList)
        if not len(processList)==len(processScales):
                print "different length of process list and process scales, ignoring scales"
                processScales = [1.]*len(processList)

        for c in variables:
		print c
                HistDict[c]["data_obs"] = HistDict[c][processList[0]].Clone("%s_data_obs"%c)
                HistDict[c]["data_obs"].Scale(processScales[0])
                for p,scale in zip(processList[1:],processScales[1:]):
                        HistDict[c]["data_obs"].Add(HistDict[c][p],scale)
                for b in range(1,HistDict[c]["data_obs"].GetNbinsX()+1):
                        HistDict[c]["data_obs"].SetBinContent(b,int(random.Poisson(HistDict[c]["data_obs"].GetBinContent(b))))
                        HistDict[c]["data_obs"].SetBinError(b,math.sqrt(HistDict[c]["data_obs"].GetBinContent(b)))
        return HistDict

#print sorted(observables.keys())
#print "for control",sorted(observables.keys())[2:]
#print "for signal",sorted(observables.keys())[:2]
for c in HistDict:
	if c=="M3_control": 
		HistDict = makePseudoData(HistDict,process_control.keys(), sorted(observables.keys())[2:])
	else:
		HistDict = makePseudoData(HistDict,process_signal.keys(), sorted(observables.keys())[:2])

outputFile = TFile("Step7a.root","recreate")
print HistDict
for obs in observables:
	outputFile.mkdir("%s/%s"%(obs,"data_obs"))
        outputFile.cd("%s/%s"%(obs,"data_obs"))
	HistDict[obs]["data_obs"].Write("nominal")
        outputFile.mkdir(obs)
	if obs=="M3_control":
		 for p in process_control.keys():
			 outputFile.mkdir("%s/%s"%(obs,p))
			 outputFile.cd("%s/%s"%(obs,p))
			 HistDict[obs][p].Write("nominal")
#			 for sys in systematics:
##				HistDict_up[sys][obs][p].Write("%sUp"%(sys))
#				HistDict_do[sys][obs][p].Write("%sDown"%(sys))
	else:

        	for p in process_signal.keys():#+["data_obs"]:
			outputFile.mkdir("%s/%s"%(obs,p))
			outputFile.cd("%s/%s"%(obs,p))
			HistDict[obs][p].Write("nominal")
#			for sys in systematics:
#				HistDict_up[sys][obs][p].Write("%sUp"%(sys))
#				HistDict_do[sys][obs][p].Write("%sDown"%(sys))


