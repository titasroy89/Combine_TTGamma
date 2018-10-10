from ROOT import *
import CMS_lumi
from optparse import OptionParser


gROOT.SetBatch(True)

from Style import *
thestyle = Style()
gStyle.SetOptTitle(0)
thestyle.SetStyle()
ROOT.gROOT.ForceStyle()
gStyle.SetMarkerStyle(1)
TGaxis.SetMaxDigits(3)
padRatio = 0.25
padOverlap = 0.15

padGap = 0.01

CMS_lumi.writeChannelText = True
CMS_lumi.writeExtraText = True
oneLine = TF1("oneline","1",-9e9,9e9)
oneLine.SetLineColor(kBlack)
oneLine.SetLineWidth(1)
oneLine.SetLineStyle(2)

parser = OptionParser()

parser.add_option("--postfit","--Postfit","--postFit",dest="postfit", default="fitDiagnostics.root",type='str',
                  help="output file from combine with fit values")
parser.add_option("-c","--channel","--channel",dest="channel", default="ele",type='str',
                  help="which channel are you on?")
parser.add_option("--MegammaPlots","--megammaPlots", dest="makeEGammaPlots",action="store_true",default=False,
                     help="Make only plots for e-gamma mass fits" )

parser.add_option("--dilepmass","--dilepmass", dest="Dilepmass",action="store_true",default=False,
                     help="Make only plots for ZJets mass fits" )
parser.add_option("--noScale", dest="Rescale",action="store_false",default=True,
                     help="Option to not rescale M3 plots by bin width" )
parser.add_option("--Tight","--Tight", dest="isTightSelection",default=False,action="store_true",
                  help="Use >=4j >= 1t control region selection" )
parser.add_option("--Tight0b","--Tight0b", dest="isTightSelection0b",default=False,action="store_true",
                  help="Use >=4j, 0t control region selection" )

parser.add_option("--LooseCRe3g1","--looseCRe3g1", dest="isLooseCRe3g1Selection",default=False,action="store_true",
                  help="Use exactly 3j at least 1t control region selection")




(options, args) = parser.parse_args()
TightSelection = options.isTightSelection
LooseCRe3g1Selection = options.isLooseCRe3g1Selection
TightSelection0b =options.isTightSelection0b

postfit = options.postfit
finalState = options.channel
makeEGammaPlots=options.makeEGammaPlots
DiLepmass=options.Dilepmass




if makeEGammaPlots:
	prefit = "Combine_MisIDEle_looseCRe3g1.root"
        _extratext="=3jets,>=1btag"
        ext="e3jet1tag"


elif DiLepmass:
	if finalState=="mu":
		if LooseCRe3g1Selection:
			_extratext=">=2jets,>=1btag"
                 	ext="2jet1tag"
			prefit = "Combine_ZJets_mu_2jet1tag.root"
		elif TightSelection0b:
			_extratext=">=4jets,=0btag"
                        ext="tight0b"
                        prefit = "Combine_ZJets_mu_tight0b.root"
		else:
			_extratext=">=4jets,>=1btag"
                 	ext="signal"
			prefit = "Combine_ZJets_mu_tight.root"
	else:
		if LooseCRe3g1Selection:
			_extratext="=3jets,>=1btag"
                        ext="e3jet1tag"
                        prefit = "Combine_ZJets_ele_e3jets1tag.root"
		elif TightSelection0b:
                        _extratext=">=4jets,=0btag"
                        ext="tight0b"
                        prefit = "Combine_ZJets_ele_tight0b.root"
		else:
			_extratext=">=4jets,>=1btag"
                        ext="signal"
			prefit = "Combine_ZJets_ele_tight.root"
else:

	if finalState=="mu":
		prefit="Combine_withDDTemplateData_v6_mu_binned.root"
		if TightSelection:
			#prefit="Combine_withDDTemplateData_v6_mu_tight_binned_PDF.root"
                         prefit="Combine_withDDTemplateData_v6_mu_tight_binned_PDF.root"
	elif finalState=="ele":	
		prefit="Combine_withDDTemplateData_v6_ele_binned.root"
		if TightSelection:
                      #  prefit="Combine_withDDTemplateData_v6_ele_tight_binned_PDF.root"
                         prefit ="Otherplots_ele_tight.root" #"Combine_withDDTemplateData_v6_ele_tight_binned_PDF.root"
	else:
		prefit="Combine_semilep.root"
	

prefitFile = TFile(prefit,"read")
postfitFile = TFile(postfit,"read")

prefitKeys = prefitFile.GetListOfKeys()
#print prefitKeys
#exit()
observables = [k.GetName() for k in prefitKeys]

observables_AxisTitle = {"M3_control":"M3 (GeV)",
			  "M3":"M3 (GeV)",
			  "ChHad":"Photon Ch. Had. Isolation (GeV)",
			  "Njet":">=4jets,=0btag",
#			  "dRPhotonJet": "dR(#gamma,jet)",
#			  "dRPhotonLepton": "dR(#gamma,lepton) ",
#			  "PhotonEt":"Leading Photon Et (GeV)",
 #                         "PhotonEta":"Leading Photon SC #eta",
#			  "ElectronPt":"Electron p_{T} (GeV)",
#			  "Njets":"Number of jets",
			  }


templates_nominal = [k.GetName() for k in prefitKeys[0].ReadObj().GetListOfKeys()]
print templates_nominal
#exit()
	
templates_signal = ["Other_NonPrompt","VGamma_NonPrompt","TTbar_NonPrompt","TTGamma_NonPrompt","Other_Prompt","VGamma_Prompt","TTbar_Prompt","TTGamma_Prompt"]

templates_control = ["Other","VGamma","TTbar","TTGamma"]

#templates_binned_CR = ["Other_NonPrompt","SingleTop_NonPrompt","VJets_NonPrompt","VGamma_NonPrompt","TTbar_NonPrompt","TTGamma_NonPrompt","Other_Prompt","SingleTop_Prompt","VJets_Prompt","VGamma_Prompt","TTbar_Prompt","TTGamma_Prompt","Other","SingleTop","VJets","VGamma","TTbar","TTGamma"]

#print templates
if finalState=="mu":
	_channelText ="#mu+jets"
        if DiLepmass:
		_channelText ="#mu#mu+jets"
	
elif finalState=="ele":
	_channelText ="e+jets"
        if DiLepmass:
                _channelText ="ee+jets"
else:
	 _channelText ="e+#mu+jets"

Histograms = {}
templates_nominal.remove("data_obs")
#print observables
#observables=["PhotonEt","PhotonEta"]
#observables.remove("ElectronPt")
#observables.remove("MassEGamma")
for obs in observables:
    Histograms[obs] = {}
    if obs=="M3_control":
	templates= templates_control
    else:
	templates=templates_nominal
    for template in templates:
#	print template
        hist = prefitFile.Get("%s/%s/nominal"%(obs,template)).Clone("Postfit_%s_%s"%(obs,template))
        hist.SetNameTitle("Postfit_%s_%s"%(obs,template),"Postfit_%s_%s"%(obs,template))
        hist.Reset()
        postFitHist = postfitFile.Get("%s_postfit/%s"%(obs,template))
        print postfitFile, "%s_postfit/%s"%(obs,template)	
        for b in range(hist.GetNbinsX()+1):
	    print template, hist, postFitHist, b, postFitHist.GetBinContent(b+1)
            hist.SetBinContent(b+1,postFitHist.GetBinContent(b+1))
            hist.SetBinError(b+1,postFitHist.GetBinError(b+1))
        Histograms[obs][template] = hist


outputFileName = "PostFit_%s"%prefit

outputFile = TFile(outputFileName,"recreate")
for obs in observables:
    print obs
    outputFile.mkdir(obs)
    outputFile.cd(obs)
    if obs=="M3_control":
        templates= templates_control
    else:
        templates=templates_nominal
    for template in templates:
	#if finalState=="mu" and template=="VJets_Prompt":continue
	#if template=="WGamma_NonPrompt":continue
#	print obs, template
        Histograms[obs][template].Write()
	
    data = prefitFile.Get("%s/data_obs/nominal"%(obs)).Clone("%s_Data"%obs)
    data.Write()

outputFile.Close()


process_signal = {"TTGamma_Prompt":["t#bar{t}+#gamma Isolated",kOrange],
           "TTGamma_NonPrompt":["t#bar{t}+#gamma Nonprompt",kAzure-4],
           "TTGamma_DD":["t#bar{t}+#gamma Data based",kAzure-4],
           "TTbar_Prompt":["t#bar{t} Isolated",kRed+1],
           "TTbar_NonPrompt": ["t#bar{t} Nonprompt",kAzure],
           "TTbar_DD":["t#bar{t} Data based",kAzure],
           "VGamma_Prompt":["V+#gamma Isolated",kOrange+7],
           "VGamma_NonPrompt":["V+#gamma Nonprompt",kCyan-3],
           "VGamma_DD":["V+#gamma Data based",kCyan-3],
           "SingleTop_Prompt":["SingleTop Isolated",kOrange+3],
           "SingleTop_NonPrompt":["SingleTop Nonprompt",kBlue-10],
           "ZGamma_DD":["Z+#gamma Data based",kCyan-3],
           "WGamma_Prompt":["W+#gamma Isolated",kOrange+5],
           "WGamma_NonPrompt":["W+#gamma Nonprompt",kCyan-8],
           "WGamma_DD":["W+#gamma Data based",kCyan-1],
           "VJets_Prompt":["V+jets Isolated",kRed-4],
           "VJets_NonPrompt":["V+jets Nonprompt",kCyan+3],
           "VJets_DD":["V+jets Data based",kCyan+3],
           "Other_Prompt":["Other Isolated",kOrange-3],
           "Other_NonPrompt":["Other Nonprompt",kAzure+7],
           "Other_DD":["Other Data based",kAzure+7],
           "Other":["Other",kGreen+3],
           "VJets":["V+jets",kCyan-3],
           "VGamma":["V+#gamma",kBlue-4],
           "SingleTop":["SingleTop",kOrange-8],
           "WGamma":["W+#gamma",kBlue-2],
           "TTbar":["t#bar{t}",kRed+1],
           "TTGamma":["t#bar{t}+#gamma",kOrange],

}


infile = TFile(outputFileName,"read")

H = 600
W = 800


# references for T, B, L, R                                                                                                             
T = 0.08*H
B = 0.12*H
L = 0.12*W
R = 0.1*W


canvas = TCanvas('canvas','canvas',800,600)
canvas.SetFillColor(0)
canvas.SetBorderMode(0)
canvas.SetFrameFillStyle(0)
canvas.SetFrameBorderMode(0)
canvas.SetLeftMargin( L/W )
canvas.SetRightMargin( R/W )
canvas.SetTopMargin( T/H )
canvas.SetBottomMargin( B/H )
canvas.SetTickx(0)
canvas.cd()
canvas.ResetDrawn()

canvasRatio = TCanvas('canvasRatio','canvasRatio',W,H)
canvasRatio.SetFillColor(0)
canvasRatio.SetBorderMode(0)
canvasRatio.SetFrameFillStyle(0)
canvasRatio.SetFrameBorderMode(0)
canvasRatio.SetLeftMargin( L/W )
canvasRatio.SetRightMargin( R/W )
canvasRatio.SetTopMargin( T/H )
canvasRatio.SetBottomMargin( B/H )
canvasRatio.SetTickx(0)
canvasRatio.SetTicky(0)
canvasRatio.Draw()
canvasRatio.cd()

pad1 = TPad("zxc_p1","zxc_p1",0,padRatio-padOverlap,1,1)
pad2 = TPad("qwe_p2","qwe_p2",0,0,1,padRatio+padOverlap)
pad1.SetLeftMargin( L/W )
pad1.SetRightMargin( R/W )
pad1.SetTopMargin( T/H/(1-padRatio+padOverlap) )
pad1.SetBottomMargin( (padOverlap+padGap)/(1-padRatio+padOverlap) )
pad2.SetLeftMargin( L/W )
pad2.SetRightMargin( R/W )
pad2.SetTopMargin( (padOverlap)/(padRatio+padOverlap) )
pad2.SetBottomMargin( B/H/(padRatio+padOverlap) )

pad1.SetFillColor(0)
pad1.SetBorderMode(0)
pad1.SetFrameFillStyle(0)
pad1.SetFrameBorderMode(0)
pad1.SetTickx(0)
pad1.SetTicky(0)

pad2.SetFillColor(0)
pad2.SetFillStyle(4000)
pad2.SetBorderMode(0)
pad2.SetFrameFillStyle(0)
pad2.SetFrameBorderMode(0)
pad2.SetTickx(0)
pad2.SetTicky(0)


canvasRatio.cd()
pad1.Draw()
pad2.Draw()

canvas.cd()







canvas.cd()
canvas.ResetDrawn()
CMS_lumi.writeChannelText1 = True
CMS_lumi.writeChannelText = True
CMS_lumi.writeExtraText = True


for obs in observables:#["PhotonEt","PhotonEta"]:#,"ElectronPt","Njets"]:#["dRPhotonJet","dRPhotonLepton"]:["M3","M3_control","ChHad","Njet"]:
	#Dilepmass=options.Dilepmass
	print "doing:",obs 
#	if obs=="M3_control":continue
	legend1= TLegend(0.6, 0.6,0.88,0.88)
	legend1.SetBorderSize(0)
	legend1.SetFillStyle(0)
	print makeEGammaPlots
	if makeEGammaPlots:
		data = infile.Get("%s/%s_Data"%(obs,obs))
#		legend.AddEntry(data,"Data",'pe')
		legend1.AddEntry(data,"Data",'pe')
		
		sig_= infile.Get("%s/Postfit_%s_signal"%(obs,obs))
		sig_.SetLineColor(kGreen+3)
		sig_.SetMarkerColor(kGreen+3)
		sig_.SetLineStyle(9)
		#legend1.AddEntry(sig_,"MisIDEle",'lp')

		bkg_=infile.Get("%s/Postfit_%s_bkg"%(obs,obs))
		bkg_.SetLineColor(kBlue)
		bkg_.SetMarkerColor(kBlue)
		bkg_.SetLineStyle(2)
		#legend1.AddEntry(bkg_,"Others bkg",'lp')
		
		sum_= sig_.Clone("sum")
                sum_.Add(bkg_)
		sum_.SetLineColor(kRed)
		sum_.SetMarkerColor(kRed)
		legend1.AddEntry(sum_,"Sum",'lp')
		legend1.AddEntry(sig_,"Z->ee (e to #gamma)",'lp')
		legend1.AddEntry(bkg_,"Background",'lp')
		
		canvas.cd()
                #sig_.Draw('hist,same')
		#sum_.GetXaxis().SetRangeUser(0.,700.)
                sum_.Draw('hist')
		data.Draw('E,X0,same')
	#	sum_.Draw('hist,same')
                sig_.Draw('hist,same')
                data.SetMarkerStyle(8)
                data.SetMarkerSize(1.0)
                sum_.GetXaxis().SetTitle("e+#gamma invariant mass (GeV)")
                sum_.GetYaxis().SetTitle("Events/5 GeV")
		
		bkg_.Draw('hist,same')
		legend1.Draw("same")
		CMS_lumi.channelText = "e+jets"
		CMS_lumi.CMS_lumi(canvas, 4, 11)
		canvas.SaveAs("EGamma_postfit.pdf")
		canvas.Clear()
		ratio = data.Clone("temp")
                temp = sum_.Clone("temp_MC")

                for i_bin in range(1,temp.GetNbinsX()+1):
                        temp.SetBinError(i_bin,0.)
                ratio.Divide(temp)
                canvasRatio.cd()
                canvasRatio.ResetDrawn()
                canvasRatio.Draw()
                canvasRatio.cd()

                pad1.Draw()
                pad2.Draw()

                pad1.cd()
                pad1.SetLogy(0)
		sum_.GetYaxis().SetRangeUser(0.,700.)
                sum_.Draw('HIST')
		sig_.Draw("same,hist")
		bkg_.Draw("same,hist")
                y2 = pad1.GetY2()
                sum_.GetXaxis().SetTitle('')
                sum_.GetYaxis().SetTitle(data.GetYaxis().GetTitle())
                sum_.SetTitle('')
                sum_.GetXaxis().SetLabelSize(0)
                sum_.GetYaxis().SetLabelSize(gStyle.GetLabelSize()/(1.-padRatio+padOverlap))
                sum_.GetYaxis().SetTitleSize(gStyle.GetTitleSize()/(1.-padRatio+padOverlap))
                sum_.GetYaxis().SetTitleOffset(gStyle.GetTitleYOffset()*(1.-padRatio+padOverlap))
                sum_.GetYaxis().SetTitle("Events/10 GeV")
                data.Draw('E,X0,SAME')
                legend1.Draw("same")


                ratio.GetXaxis().SetLabelSize(gStyle.GetLabelSize()/(padRatio+padOverlap))
                ratio.GetYaxis().SetLabelSize(gStyle.GetLabelSize()/(padRatio+padOverlap))
                ratio.GetXaxis().SetTitleSize(gStyle.GetTitleSize()/(padRatio+padOverlap))
                ratio.GetYaxis().SetTitleSize(gStyle.GetTitleSize()/(padRatio+padOverlap))
                ratio.GetYaxis().SetTitleOffset(gStyle.GetTitleYOffset()*(padRatio+padOverlap-padGap))
                ratio.GetYaxis().SetRangeUser(0.5,1.5)
                ratio.GetYaxis().SetNdivisions(504)
		ratio.GetXaxis().SetTitle("e+#gamma mass (GeV)")
                ratio.GetYaxis().SetTitle("Data/MC")
                CMS_lumi.CMS_lumi(pad1, 4, 11)

                pad2.cd()
                maxRatio = 1.5
                minRatio = 0.5
                ratio.SetMarkerStyle(data.GetMarkerStyle())
                ratio.SetMarkerSize(data.GetMarkerSize())
                ratio.SetLineColor(data.GetLineColor())
                ratio.SetLineWidth(data.GetLineWidth())
                ratio.Draw('e,x0')
                errorband.Divide(temp)
                errorband.Draw('e2,same')
                oneLine.Draw("same")

                canvasRatio.Update()
                canvasRatio.RedrawAxis()
                canvasRatio.SaveAs("EGamma_postfit_ratio.pdf")
			
	
	elif DiLepmass:
                data = infile.Get("%s/%s_Data"%(obs,obs))
                legend1.AddEntry(data,"Data",'pe')

                sig_= infile.Get("%s/Postfit_%s_signal"%(obs,obs))
                sig_.SetLineColor(kGreen+3)
                sig_.SetMarkerColor(kGreen+3)
		sig_.SetLineStyle(9)
                #legend1.AddEntry(sig_,"Z+Jets",'lp')

                bkg_=infile.Get("%s/Postfit_%s_bkg"%(obs,obs))
                bkg_.SetLineColor(kBlue)
                bkg_.SetMarkerColor(kBlue)
		bkg_.SetLineStyle(2)
                #legend1.AddEntry(bkg_,"Background",'lp')


                sum_= sig_.Clone("sum")
                sum_.Add(bkg_)
                sum_.SetLineColor(kRed)
                sum_.SetMarkerColor(kRed)
                legend1.AddEntry(sum_,"Sum",'lp')
		legend1.AddEntry(sig_,"Z+Jets",'lp')
		legend1.AddEntry(bkg_,"Background",'lp')
                canvas.cd()
                sum_.Draw('hist')
                data.Draw('E,X0,same')
		sig_.Draw('hist,same')
                data.SetMarkerStyle(8)
                data.SetMarkerSize(1.0)
	#	if finalState=="mu":
         #       	sum_.GetXaxis().SetTitle("(#mu^{+},#mu^{-}) invariant mass (GeV)")
	#	else:	
	#		sum_.GetXaxis().SetTitle("(e^{+},e^{-}) invariant mass (GeV)")
               # sum_.GetYaxis().SetTitle("Events/5 GeV")

                bkg_.Draw('hist,same')
                legend1.Draw("same")
		CMS_lumi.channelText = _channelText
		CMS_lumi.channelText1 = _extratext
                CMS_lumi.CMS_lumi(canvas, 4, 11)
                canvas.SaveAs("ZJets_postfit_%s_%s.pdf"%(finalState,ext))
                canvas.Clear()
		ratio = data.Clone("temp")
		temp=sum_.Clone("temp_MC")

		for i_bin in range(1,temp.GetNbinsX()+1):
			temp.SetBinError(i_bin,0.)
		ratio.Divide(temp)
		canvasRatio.cd()
		canvasRatio.ResetDrawn()
		canvasRatio.Draw()
		canvasRatio.cd()

		pad1.Draw()
		pad2.Draw()

		pad1.cd()
		#pad1.SetLogy(plotInfo[5])

		sum_.Draw('HIST')
		y2 = pad1.GetY2()
		sum_.GetXaxis().SetTitle('')
		sum_.GetYaxis().SetTitle(data.GetYaxis().GetTitle())
		sum_.SetTitle('')
		sum_.GetXaxis().SetLabelSize(0)
		sum_.GetYaxis().SetLabelSize(gStyle.GetLabelSize()/(1.-padRatio+padOverlap))
		sum_.GetYaxis().SetTitleSize(gStyle.GetTitleSize()/(1.-padRatio+padOverlap))
		sum_.GetYaxis().SetTitleOffset(gStyle.GetTitleYOffset()*(1.-padRatio+padOverlap))
		sum_.GetYaxis().SetTitle("Events/10 GeV")
		sig_.Draw("same,hist")
		bkg_.Draw("same,hist")
		data.Draw('E,X0,SAME')
		legend1.Draw("same")

		ratio.SetTitle('')

		ratio.GetXaxis().SetLabelSize(gStyle.GetLabelSize()/(padRatio+padOverlap))
		ratio.GetYaxis().SetLabelSize(gStyle.GetLabelSize()/(padRatio+padOverlap))
		ratio.GetXaxis().SetTitleSize(gStyle.GetTitleSize()/(padRatio+padOverlap))
		ratio.GetYaxis().SetTitleSize(gStyle.GetTitleSize()/(padRatio+padOverlap))
		ratio.GetYaxis().SetTitleOffset(gStyle.GetTitleYOffset()*(padRatio+padOverlap-padGap))
	        ratio.GetYaxis().SetRangeUser(0.5,1.5)
		ratio.GetYaxis().SetNdivisions(504)
		if finalState=="mu":
                        ratio.GetXaxis().SetTitle("(#mu^{+},#mu^{-}) invariant mass (GeV)")
                else:
                        ratio.GetXaxis().SetTitle("(e^{+},e^{-}) invariant mass (GeV)")

		ratio.GetYaxis().SetTitle("Data/MC")
		CMS_lumi.CMS_lumi(pad1, 4, 11)

		pad2.cd()
		maxRatio = 1.5
		minRatio = 0.5
		ratio.SetMarkerStyle(data.GetMarkerStyle())
		ratio.SetMarkerSize(data.GetMarkerSize())
		ratio.SetLineColor(data.GetLineColor())
		ratio.SetLineWidth(data.GetLineWidth())
		ratio.Draw('e,x0')
		errorband.Divide(temp)
		errorband.Draw('e2,same')
		oneLine.Draw("same")

		canvasRatio.Update()
		canvasRatio.RedrawAxis()
		canvasRatio.SaveAs("ZJets_postfit_%s_%s_ratio.pdf"%(finalState,ext))

                exit()


		
	else:
		
         	sum_ = THStack("hs","hs")
	 	SetOwnership(sum_,True)
	  
		if obs=="M3_control" or obs=="CR_0photon" :
			sampleList = templates_control
		else:
			sampleList = templates_signal


		print infile, "%s/%s_Data"%(obs,obs)	
		data = infile.Get("%s/%s_Data"%(obs,obs))
		print data.Integral()	
		X1 = 0.4
		
		legend= TLegend(X1,0.92-0.07*4,0.88,0.89)
		legend.SetBorderSize(0)
		legend.SetFillStyle(0)

		axisTitle = obs
		if obs in observables_AxisTitle:
			axisTitle = observables_AxisTitle[obs]
		
		if obs=="M3_control" or obs=="CR_0photon":
			#print obs
			legend.AddEntry(data,"Data",'pe')
	                for p in sampleList[::-1]:
			#	print "control:",p
				h1 = infile.Get("%s/Postfit_%s_%s"%(obs,obs,p))
				h1.SetFillColor(process_signal[p][1])
				h1.SetLineColor(process_signal[p][1])
				legend.AddEntry(h1,process_signal[p][0],'f')
			for p in sampleList:
				
				h1 = infile.Get("%s/Postfit_%s_%s"%(obs,obs,p))
				h1.SetFillColor(process_signal[p][1])
				h1.SetLineColor(process_signal[p][1])
				if "M3" in obs: ## problem here ;should be obs=="M3" otherwise will scale M3_control
					h1.Scale(1,"width")
				sum_.Add(h1)




		else:
			legend.SetNColumns(2)
			legend.AddEntry(data,"Data",'pe')
			legend.AddEntry(None,"",'')
			hName = "TTbar_Prompt"
			histsTemp = []
			N=len(sampleList)
			for i in range(N/2):
				p = sampleList[N-i-1]
				print "first:",p
				histsTemp.append(TH1F(p,p,1,0,1))
			#	histsTemp[-1]=(infile.Get("%s/Postfit_%s_%s"%(obs,obs,hName)))
				histsTemp[-1].SetFillColor(process_signal[p][1])
				histsTemp[-1].SetLineColor(process_signal[p][1])
				legend.AddEntry(histsTemp[-1],process_signal[p][0],'f')

				p = sampleList[N/2-i-1]
				histsTemp.append(TH1F(p,p,1,0,1))
				#print "second:",p

			#	histsTemp[-1]=infile.Get("%s/Postfit_%s_%s"%(obs,obs,hName))
				histsTemp[-1].SetFillColor(process_signal[p][1])
				histsTemp[-1].SetLineColor(process_signal[p][1])
				legend.AddEntry(histsTemp[-1],process_signal[p][0],'f')


			for p in sampleList:
			 	hName = p
			 	if finalState=="mu" and p=="VJets_Prompt": hName = "TTbar_Prompt"
			 	h1=infile.Get("%s/Postfit_%s_%s"%(obs,obs,hName))
				h1.SetFillColor(process_signal[p][1])
				h1.SetLineColor(process_signal[p][1])
			#	legend.AddEntry(h1,process_signal[p][0],'f')
				if "M3" in obs or "ChHad" in obs: ##same issue here should be obs=="M3"
					h1.Scale(1,"width")
				sum_.Add(h1)

#		for p in sampleList:
#			if finalState=="mu" and p=="VJets_Prompt":continue		
#			if p=="WGamma_NonPrompt":continue
#			h1 = infile.Get("%s/Postfit_%s_%s"%(obs,obs,p))
#			print process_signal[p][1], p
#			h1.SetFillColor(process_signal[p][1])
#			h1.SetLineColor(process_signal[p][1])
			#if options.Rescale and "M3" in obs:
#			h1.Scale(1,"width")
#			sum_.Add(h1)


	#if options.Rescale and "M3" in obs:
	data.Sumw2(True)
	if obs=="M3" or obs=="ChHad":
		data.Scale(1,"width")
	maxVal = max(sum_.GetMaximum(), data.GetMaximum())
	sum_.SetMaximum(1.5*maxVal)
	if "ChHad" in obs:# or "CR" in obs:
		canvas.SetLogy(1)
	else:
		canvas.SetLogy(0)

	sum_.Draw("hist")
	data.Draw('e,x0,same')
	data.SetMarkerStyle(8)
	data.SetMarkerSize(1.0)
	data.SetLineColor(kBlack)
	data.SetMarkerColor(kBlack)
	
	if obs=="CR_0photon":
                sum_.GetHistogram().GetXaxis().SetBinLabel(1," >=3jet,>=1tag,0pho")
	elif obs=="CR1":
                sum_.GetHistogram().GetXaxis().SetBinLabel(1," ==2jet,>=1tag,>=1pho")
	elif obs=="CR2":
                sum_.GetHistogram().GetXaxis().SetBinLabel(1," >=3jet,=0tag,>=1pho")
	elif obs=="CR3":
		sum_.GetHistogram().GetXaxis().SetBinLabel(1," >=4jet,=0tag,>=1pho")
	else:
		sum_.GetHistogram().GetXaxis().SetTitle("%s"%(axisTitle))
		
	if "M3" in obs or "ChHad" in obs:
		sum_.GetHistogram().GetYaxis().SetTitle("#LT Events / GeV #GT")
	else:
		sum_.GetHistogram().GetYaxis().SetTitle("Events / bin")

	sum_.GetHistogram().SetTitle("%s_Postfit"%(obs))
	legend.Draw("same")
	CMS_lumi.channelText = _channelText
	if obs=="M3_control": CMS_lumi.channelText = _channelText + ", 0-photon"
	CMS_lumi.CMS_lumi(canvas, 4, 11)
	canvas.SaveAs("PostFitPlots_%s_%s_postfit.pdf"%(obs,finalState))
	canvas.Clear()	
	errorband=sum_.GetStack().Last().Clone("error")
    	errorband.Sumw2()
    	errorband.SetLineColor(0)
    	errorband.SetFillColor(kBlack)
    	errorband.SetFillStyle(3245)
    	errorband.SetMarkerSize(0)	
	ratio = data.Clone("temp")
        temp = sum_.GetStack().Last().Clone("temp_error")

        for i_bin in range(1,temp.GetNbinsX()+1):
                temp.SetBinError(i_bin,0.)
        ratio.Divide(temp)
	canvasRatio.cd()
        canvasRatio.ResetDrawn()
        canvasRatio.Draw()
        canvasRatio.cd()

        pad1.Draw()
        pad2.Draw()

        pad1.cd()
        #pad1.SetLogy(plotInfo[5])

        sum_.Draw('HIST')
        y2 = pad1.GetY2()


#       sum_.SetMinimum(1)
        #    pad1.Update()
	if "ChHad" in obs:# or "CR" in obs:
                pad1.SetLogy(1)
        else:
                pad1.SetLogy(0)
        sum_.GetXaxis().SetTitle('')
        sum_.GetYaxis().SetTitle(data.GetYaxis().GetTitle())
	sum_.SetTitle('')
        sum_.GetXaxis().SetLabelSize(0)
        sum_.GetYaxis().SetLabelSize(gStyle.GetLabelSize()/(1.-padRatio+padOverlap))
        sum_.GetYaxis().SetTitleSize(gStyle.GetTitleSize()/(1.-padRatio+padOverlap))
        sum_.GetYaxis().SetTitleOffset(gStyle.GetTitleYOffset()*(1.-padRatio+padOverlap))
	if "M3" in obs or "ChHad" in obs:
        	sum_.GetHistogram().GetYaxis().SetTitle("#LT Events / GeV #GT")
	else:
		sum_.GetHistogram().GetYaxis().SetTitle("Events")
        data.Draw('E,X0,SAME')
        legend.AddEntry(errorband,"Uncertainty","f")
        legend.Draw("same")

        ratio.SetTitle('')

        ratio.GetXaxis().SetLabelSize(gStyle.GetLabelSize()/(padRatio+padOverlap))
        ratio.GetYaxis().SetLabelSize(gStyle.GetLabelSize()/(padRatio+padOverlap))
        ratio.GetXaxis().SetTitleSize(gStyle.GetTitleSize()/(padRatio+padOverlap))
        ratio.GetYaxis().SetTitleSize(gStyle.GetTitleSize()/(padRatio+padOverlap))
        ratio.GetYaxis().SetTitleOffset(gStyle.GetTitleYOffset()*(padRatio+padOverlap-padGap))
        ratio.GetYaxis().SetRangeUser(0.5,1.5)
	ratio.GetYaxis().SetNdivisions(504)
        ratio.GetXaxis().SetTitle(axisTitle)
        ratio.GetYaxis().SetTitle("Data/MC")
        CMS_lumi.CMS_lumi(pad1, 4, 11)

        pad2.cd()
        #for i_bin in range(1,errorband.GetNbinsX()):
        #       errorband.SetBinContent(i_bin,1.)
        maxRatio = 1.5
        minRatio = 0.5
        ratio.SetMarkerStyle(data.GetMarkerStyle())
        ratio.SetMarkerSize(data.GetMarkerSize())
        ratio.SetLineColor(data.GetLineColor())
        ratio.SetLineWidth(data.GetLineWidth())
        ratio.Draw('e,x0')
	errorband.Divide(temp)
	oneLine.Draw("same")
	errorband.Draw("e2,same")

        #    pad2.Update()
        canvasRatio.Update()
        canvasRatio.RedrawAxis()
        canvasRatio.SaveAs("PostFitPlots_%s_%s_postfit_ratio.pdf"%(obs,finalState))

