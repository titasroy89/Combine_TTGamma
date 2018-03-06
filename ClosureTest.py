from ROOT import *
import subprocess
from array import *
rand = TRandom3(0)

seed = rand.Integer(10000000)

datacard = "datacard_Syst_Step7a.txt"
#fitParam = "Hadronic_norm"
fitParam='r'
gROOT.SetBatch(True)


c1 = TCanvas()#'c1', 'A Simple Graph Example', 200, 10, 700, 500 )

c1.SetFillColor(0)
c1.SetGrid()
  
scale = 1.
measured_=array('d')
expected_err=array('d')
measured_stderr =array('d')
val=[0.5,0.7,0.9,0.95,1.0,1.05,1.1,1.3,1.5,1.7,2.0,2.3,2.6,3.0]
expected_=array('d')
	

for scale in val:
    expected_.append(scale)
#    command = "combine -M FitDiagnostics -t 50 --skipBOnlyFit --trackParameters r,Hadronic_norm,VGamma_norm,Others_norm,TTbar_norm -v -1 -s %i --expectSignal=%.2f %s"%(seed, scale, datacard)
    #command ="combine -M FitDiagnostics -t 50 --setParameters Hadronic_norm=%.2f --skipBOnlyFit --trackParameters r,Hadronic_norm,VGamma_norm,Others_norm,TTbar_norm --expectSignal=1 -s %i %s"%(scale,seed,datacard)
    command = "combine -M FitDiagnostics -t 1000 --skipBOnlyFit --trackParameters r,TTbar_norm,Hadronic_norm,VGamma_norm,Others_norm,Pileup,BTagSF,MuEff,JER,phosmear,phoscale,elesmear,elescale,Q2 -s %i  --plots --expectSignal=%.2f %s"%(seed, scale, datacard)
    p = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    f = p.communicate()

    _file = TFile("higgsCombineTest.FitDiagnostics.mH120.%i.root"%seed,"read")

    h = TH1F("h","h",11000,-1,10)
    _tree = _file.Get("limit")

#for fitParam in ["r","TTbar_norm","VGamma_norm","Others_norm","Hadronic_norm"]:

    _tree.Draw("trackedParam_%s>>h"%fitParam,"quantileExpected==-1")
    mean = h.GetMean()
    stddev = h.GetStdDev()
    measured_.append(mean)
    measured_stderr.append(stddev)
    print "expected : %.2f"%scale
    print "%-15s : %5s +/- %5s"%(fitParam,"%.3f"%mean,"%.3f"%stddev)


    p = subprocess.Popen("rm higgsCombineTest.FitDiagnostics.mH120.%i.root"%seed,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    f = p.communicate()

print measured_
print expected_
for i in range(len(measured_)):
	expected_err.append(0)
f = TFile("closuretest.root","recreate")
gr1 = TGraphErrors(len(expected_),expected_,measured_,expected_err,measured_stderr)
gr1.Write("TTGamma")
f.Close()
gr1.SetMarkerStyle(6)
gr1.SetMarkerSize(1)
gr1.SetMarkerColor(kBlack)
gr1.SetLineWidth(1)
gr1.SetLineColor(kBlack)
gr1.SetTitle('Closure test Signal Strength:TTGamma')
gr1.GetXaxis().SetTitle('expected value of')
gr1.GetYaxis().SetTitle('measured value')

gr1.Draw('ALP')
c1.SaveAs("ClosureTTGamma.pdf")
