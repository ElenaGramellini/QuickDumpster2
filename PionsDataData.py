from ROOT import *
import os
import math
import argparse

from ROOT import TEfficiency
from ROOT import gStyle , TCanvas , TGraphErrors
from array import array



## Data
data_FileName = "/Volumes/Seagate/Elena/TPC/Data60A.root"
data_File   = TFile.Open(data_FileName)

interactingPlotString = "RecoXS/hRecoInteractingKE"
incidentPlotString = "RecoXS/hRecoIncidentKE"
data_Int    = data_File.Get(interactingPlotString)
data_Inc    = data_File.Get(incidentPlotString)

XSDataRecoPion = data_Int.Clone("pionXS_Data")
XSDataRecoPion.Sumw2()
data_Inc.Sumw2()
XSDataRecoPion.Scale(101.10968)
XSDataRecoPion.Divide(data_Inc)
XSDataRecoPion.SetLineColor(kBlack)
XSDataRecoPion.SetLineWidth(2)
XSDataRecoPion.SetFillColor(0)

c1=TCanvas("c1" ,"Data" ,200 ,10 ,500 ,500) #make nice
c1.SetGrid ()
XSDataRecoPion.Draw("pe")

legend = TLegend(.44,.70,.84,.89)
legend.AddEntry(XSDataRecoPion,"Raw Data Tot XS")
legend.Draw("same")
c1.Update()



outFile = TFile("DataRaw.root","recreate")
outFile.cd()
XSDataRecoPion.Write() 

outFile.Write()
outFile.Close()


raw_input()  
