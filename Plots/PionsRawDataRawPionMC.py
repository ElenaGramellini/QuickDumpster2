from ROOT import *
import os
import math
import argparse

from ROOT import TEfficiency
from ROOT import gStyle , TCanvas , TGraphErrors
from array import array



## Data
dataOldGeo_FileName = "/Volumes/Seagate/Elena/TPC/MC60A_Pions.root"
data_FileName = "/Volumes/Seagate/Elena/TPC/Data60A.root"
dataOldGeo_File   = TFile.Open(dataOldGeo_FileName)
data_File   = TFile.Open(data_FileName)


interactingPlotString = "RecoXS/hRecoInteractingKE"
incidentPlotString = "RecoXS/hRecoIncidentKE"
data_Int    = data_File.Get(interactingPlotString)
data_Inc    = data_File.Get(incidentPlotString)

dataOldGeo_Int    = dataOldGeo_File.Get(interactingPlotString)
dataOldGeo_Inc    = dataOldGeo_File.Get(incidentPlotString)

XSDataRecoPion = data_Int.Clone("pionMCXSData")
XSDataRecoPion.Sumw2()
data_Inc.Sumw2()
XSDataRecoPion.Scale(101.10968)
XSDataRecoPion.Divide(data_Inc)
XSDataRecoPion.SetLineColor(kBlack)
XSDataRecoPion.SetLineWidth(2)
XSDataRecoPion.SetFillColor(0)


XSDataOldGeoRecoPion = dataOldGeo_Int.Clone("pionMCXSDataOldGeo")
XSDataOldGeoRecoPion.Sumw2()
dataOldGeo_Inc.Sumw2()
XSDataOldGeoRecoPion.Scale(101.10968)
XSDataOldGeoRecoPion.Divide(dataOldGeo_Inc)
XSDataOldGeoRecoPion.SetLineColor(kRed)
XSDataOldGeoRecoPion.SetLineWidth(2)
XSDataOldGeoRecoPion.SetFillColor(0)


c1=TCanvas("c1" ,"Data" ,200 ,10 ,500 ,500) #make nice
c1.SetGrid ()
XSDataRecoPion.Draw("pe")
XSDataOldGeoRecoPion.Draw("pesame")

legend = TLegend(.44,.70,.84,.89)
legend.AddEntry(XSDataRecoPion,"Raw Data Tot XS")
legend.AddEntry(XSDataOldGeoRecoPion,"Raw MC New Geo Tot XS")
legend.Draw("same")
c1.Update()


raw_input()  
