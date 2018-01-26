from ROOT import *
import subprocess
from array import *
rand = TRandom3(0)

seed = rand.Integer(10000000)

datacard = "datacard_Syst_Step7a.txt"
#fitParam = "Hadronic_norm"
#fitParam='r'
gROOT.SetBatch(True)


c1 = TCanvas('c1', 'A Simple Graph Example', 200, 10, 700, 500 )

c1.SetFillColor(0)
c1.SetGrid()
  
scale = 1.
measured_=array('d')
measured_stderr =array('d')
	
print seed
#for scale in val:
   # expected_.append(scale)
command = "combine -M FitDiagnostics -t 1000 --skipBOnlyFit --trackParameters r,TTbar_norm,Hadronic_norm,VGamma_norm,Others_norm,SingleTop_norm,VJets_norm,lumi -s %i --robustFit 1 --plots --expectSignal=%.2f %s"%(seed, scale, datacard)
print command
p = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
f = p.communicate()

_file = TFile("higgsCombineTest.FitDiagnostics.mH120.%i.root"%seed,"read")

h = TH1F("h","h",11000,-1,10)
_tree = _file.Get("limit")

for fitParam in ["r","TTbar_norm","VGamma_norm","Others_norm","SingleTop_norm","VJets_norm","lumi","Hadronic_norm"]:

	_tree.Draw("trackedParam_%s>>h"%fitParam,"quantileExpected==-1")
	h.Draw()
	c1.SaveAs("%s_spread.pdf"%(fitParam))
        c1.Clear()
	mean = h.GetMean()
	stddev = h.GetStdDev()
	measured_.append(mean)
	measured_stderr.append(stddev)
	print "expected : %.2f"%scale
	print "%-15s : %5s +/- %5s"%(fitParam,"%.3f"%mean,"%.3f"%stddev)


#p = subprocess.Popen("rm higgsCombineTest.FitDiagnostics.mH120.%i.root"%seed,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
#f = p.communicate()
print "Signal_Strength\tTTbar_norm\tVGamma_norm\tOthers_norm,SingleTop_norm,VJets_norm,lumi,Hadronic_norm"
print "%.2f+/-%.2f\t%.2f+/-%.2f\t%.2f+/-%.2f\t%.2f+/-%.2f\t%.2f+/-%.2f\t%.2f+/-%.2f\t%.2f+/-%.2f"%(measured_[0],measured_stderr[0],measured_[1],measured_stderr[1],measured_[2],measured_stderr[2],measured_[3],measured_stderr[3],measured_[4],measured_stderr[4],measured_[5],measured_stderr[5],measured_[6],measured_stderr[6],measured_[7],measured_stderr[7])#,measured_[8],measured_stderr[8],measured_[9],measured_stderr[9],measured_[10],measured_stderr[10],measured_[11],measured_stderr[11],measured_[12],measured_stderr[12])

