from ROOT import *
import os
import math
import argparse

from ROOT import TEfficiency
from ROOT import gStyle , TCanvas , TGraphErrors
from array import array



parser = argparse.ArgumentParser()
parser.add_argument("fname"   , nargs='?', default = '../../../LArIATTrueCrossSec/PionMinusG4.txt', type = str, help="insert fileName")
args    = parser.parse_args()
fname   = args.fname


#Truth from Geant4Table
kineticEnergy = []
crossSec      = []
crossSec_el   = []
crossSec_inel = []
zero          = []


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

title = ""
with open(fname) as f:
    for fLine in f.readlines():
        w = fLine.split()
        if is_number(w[0]):
            runIn    = int(w[0])
            ke       = float(w[1])
            xs_el       = float(w[2])
            xs_in       = float(w[3])
            xstot       = float(w[4])
            kineticEnergy.append(ke)
            crossSec.append(xstot)
            crossSec_el.append(xs_el)
            crossSec_inel.append(xs_in)
            zero.append(0.)
        else:
            if "for" not in fLine: 
                continue
            title =  fLine[9:]


#define some data points . . .
x      = array('f', kineticEnergy )
y      = array('f', crossSec)
exl    = array('f', zero)
exr    = array('f', zero)

nPoints=len(x)
# . . . and hand over to TGraphErros object
gr      = TGraphErrors ( nPoints , x , y     , exl, exr )
gr . SetTitle(title+"; Kinetic Energy [MeV]; Cross Section [barn]")
gr . GetXaxis().SetRangeUser(0,1000)
gr . GetYaxis().SetRangeUser(0,2.)
gr . SetLineWidth(2) ;
gr . SetLineColor(kGreen-2) ;
gr . SetFillColor(0)


## Data
data_FileName = "TrueXS.root"
data_File   = TFile.Open(data_FileName)
interactingPlotString = "TrueXS/hInteractingKE"
incidentPlotString = "TrueXS/hIncidentKE"
data_Int    = data_File.Get(interactingPlotString)
data_Inc    = data_File.Get(incidentPlotString)
XSDataRecoPion = data_Int.Clone("pionMCXSData")
XSDataRecoPion.Sumw2()
data_Inc.Sumw2()
XSDataRecoPion.Scale(101.10968)
XSDataRecoPion.Divide(data_Inc)
XSDataRecoPion.SetLineColor(kBlack)
XSDataRecoPion.SetLineWidth(2)
XSDataRecoPion.SetFillColor(0)




c1=TCanvas("c1" ,"Data" ,200 ,10 ,500 ,500) #make nice
c1.SetGrid ()
gr . Draw ( "APL" ) ;
XSDataRecoPion.Draw("pesame")

legend = TLegend(.44,.70,.84,.89)
legend.AddEntry(gr,"G4 Prediction Tot XS")
legend.AddEntry(XSDataRecoPion,"True XS")
legend.Draw("same")
c1.Update()


raw_input()  
