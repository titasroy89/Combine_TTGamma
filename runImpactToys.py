from ROOT import *

import sys
import os
from array import array
import subprocess
from optparse import OptionParser

import json

parser = OptionParser()
parser.add_option("-t", "--toys", dest="toys", default="10",type='int',
                     help="Specify how many toys you want to run on" )
parser.add_option("-d", "--datacard", dest="datacard", default="datacard_Syst_ele_v5.txt",type='str',
                     help="which datacard" )

(options, args) = parser.parse_args()

n_toys =options.toys

rand = TRandom3(0)

def run_commands(listofcommands):
        for command in listofcommands:
                print command
                p = subprocess.Popen(command, shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                f = p.communicate()
		print f
        return


		
datacard=options.datacard

if "ele" in datacard:
	systematics =["TTbar_norm","VGamma_norm","Others_norm","lumi","JER","JECTotal","phosmear","phoscale","BTagSF","Q2","Pdf","PU","EleEff","PhoEff","elesmear","elescale","isr","fsr","shapeDD","MisIDEleshape", "Pdfsignal"]
else:
	systematics =["TTbar_norm","VGamma_norm","Others_norm","lumi","JER","JECTotal","phosmear","phoscale","BTagSF","Q2","Pdf","PU","PhoEff","MuEff","isr","fsr","shapeDD","MisIDEleshape","Pdfsignal"]
for i in range(23):
	systematics.append("prop_binM3_bin%i"%i)
        systematics.append("prop_binM3_control_bin%i"%i)
        
for i in range(13):
	systematics.append("prop_binChHad_bin%i"%i)

systematics.append("prop_binNjet_bin0")

for i_toys in range(n_toys):
	seed = rand.Integer(10000000)

	#seedVar[0] = seed

	commands = ["text2workspace.py %s.txt"%(datacard),
		    "combineTool.py -M Impacts -d %s.root -m 125 --doInitialFit --robustFit 1 -t 1 --expectSignal=1. -s %i"%(datacard,seed),
		    "mv higgsCombine_initialFit_Test.MultiDimFit.mH125.%i.root higgsCombine_initialFit_Test.MultiDimFit.mH125.root"%(seed),
		    "combineTool.py -M Impacts -d %s.root -m 125 --robustFit 1 --doFits -t 1 --expectSignal=1. -s %i"%(datacard,seed)]

	run_commands(commands)

	directoryContents = os.listdir(".")

	systList = []
	commands = []
	for syst in systematics:
        	commands.append("mv higgsCombine_paramFit_Test_%s.MultiDimFit.mH125.%i.root higgsCombine_paramFit_Test_%s.MultiDimFit.mH125.root"%(syst,seed,syst))
       
	run_commands(commands)

	commands=[]
	commands.append("combineTool.py -M Impacts -d %s.root -m 125 -o impacts_%s.json"%(datacard,seed))
	#commands.append("plotImpacts.py -i impacts_%s.json -o impacts_%s -t parameterNames.json"%(seed,seed))


	run_commands(commands)
