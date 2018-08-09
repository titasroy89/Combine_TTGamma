from ROOT import *
import subprocess
from array import *
rand = TRandom3(0)

seed = rand.Integer(10000000)
from optparse import OptionParser

#fitParam = "Hadronic_norm"
#fitParam='VGamma_norm'
gROOT.SetBatch(True)
_outputFile = TFile("closuretest.root","recreate")

c1 = TCanvas()#'c1', 'A Simple Graph Example', 200, 10, 700, 500 )

c1.SetFillColor(0)
c1.SetGrid()

parser = OptionParser()

parser.add_option("-c", "--channel", dest="channel", default="mu",type='str',
                  help="Specify which channel mu or ele? default is mu" )
parser.add_option("--Tight","--tight", dest="isTightSelection", default=False,action="store_true",
                     help="Use 4j2t selection" )
parser.add_option("--fit","--fit", dest="isfit", default="1",type='int',
                     help="Using Fit1, Fit2, Fit3" )


(options, args) = parser.parse_args()


isfit = options.isfit
finalState=options.channel
print isfit



datacard = "datacard_Syst_%s_Fit%s.txt"%(finalState,isfit)  
scale = 1.
val=[0.5,0.7,0.9,0.95,1.0,1.05,1.1,1.3,1.5,1.7,2.0,3.0]#,50,100]
#val=[0.5,1.,1.5]
val=[0.4,0.7,0.9,0.95,1.0,1.05,1.1,1.3,1.5,1.7,1.9]
	

fitParamList = ["r","TTbar_norm","VGamma_norm","Others_norm","Hadronic_norm"]
fitParamList = ["r","VGamma_norm","TTbar_norm","Hadronic_norm"]
fitParamList=["r","Hadronic_norm"]
#fitParamList=["SingleTop_norm","TTbar_norm"]
nToys = 10

for fitParam in fitParamList:

    expected_=array('d')
    measured_=array('d')
    expected_err=array('d')
    measured_stderr =array('d')
    if fitParam=="TTbar_norm":
	
	val =[0.3,0.5,0.7,0.8,0.9,0.95,1.0,1.05,1.1,1.15]
    else:
	val=[0.1,0.4,0.7,0.9,0.95,1.0,1.05,1.1,1.3,1.5,1.7,1.9]
    for scale in val:
        expected_.append(scale)
        print seed

        if fitParam=="r":
            command ="combine -M MultiDimFit -t %i --trackParameters r,Hadronic_norm,VGamma_norm,TTbar_norm,lumi,Others_norm  --expectSignal %.2f -s %i %s"%(nToys,scale,seed,datacard)

        else:
            command ="combine -M MultiDimFit -t %i --setParameters %s=%.2f --redefineSignalPOIs r,%s --trackParameters r,Hadronic_norm,VGamma_norm,TTbar_norm,lumi,Others_norm  --expectSignal 1 -s %i %s"%(nToys,fitParam,scale,fitParam,seed,datacard)
#            command ="combine -M MultiDimFit -t 10 --setParameters %s=%.2f --trackParameters r,Hadronic_norm,VGamma_norm,TTbar_norm,SingleTop_norm,lumi,Others_norm  --expectSignal 1 -s %i %s"%(fitParam,scale,seed,datacard)

        print command
        p = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        f = p.communicate()
        
        _file = TFile("higgsCombineTest.MultiDimFit.mH120.%i.root"%seed,"read")
        
        h = TH1F("h","h",11000,-1,10)
        _tree = _file.Get("limit")
        
        print fitParam
        _tree.Draw("trackedParam_%s>>h"%fitParam,"quantileExpected==-1")
        mean = h.GetMean()
        stddev = h.GetStdDev()
        measured_.append(mean)
        measured_stderr.append(stddev)
        print "expected : %.2f"%scale
        print "%-15s : %5s +/- %5s"%(fitParam,"%.3f"%mean,"%.3f"%stddev)


        p = subprocess.Popen("rm higgsCombineTest.MultiDimFit.mH120.%i.root"%seed,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        f = p.communicate()



    print measured_
    print expected_
    for i in range(len(measured_)):
	expected_err.append(0)
    _outputFile.cd()
    gr1 = TGraphErrors(len(expected_),expected_,measured_,expected_err,measured_stderr)
    gr1.Write("%s"%fitParam)

    gr1.SetMarkerStyle(6)
    gr1.SetMarkerSize(1)
    gr1.SetMarkerColor(kBlack)
    gr1.SetLineWidth(1)
    gr1.SetLineColor(kBlack)
    gr1.SetTitle('Bias Test for %s'%fitParam)
    gr1.GetXaxis().SetTitle('value of %s'%fitParam)
    gr1.GetYaxis().SetTitle('measured value of %s'%fitParam)

    gr1.Draw('ALP')
    c1.SaveAs("Closure%s_%s%s.pdf"%(fitParam,finalState,isfit))

