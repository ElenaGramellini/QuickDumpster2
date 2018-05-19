from ROOT import *
import os
import math
import argparse

from ROOT import TEfficiency
from ROOT import gStyle , TCanvas , TGraphErrors
from array import array



gStyle.SetOptStat(0)

################################################ Get Background Correction 
bkgCorrection60AFile = TFile.Open("Out_1.0Muons_1.0Electrons_60A.root")
bkgCorr_Int_60A      = bkgCorrection60AFile.Get("backgroundCorrection_Int60A")
bkgCorr_Inc_60A      = bkgCorrection60AFile.Get("backgroundCorrection_Inc60A")

bkgCorrection100AFile = TFile.Open("Out_1.0Muons_1.0Electrons_100A.root")
bkgCorr_Int_100A      = bkgCorrection100AFile.Get("backgroundCorrection_Int100A")
bkgCorr_Inc_100A      = bkgCorrection100AFile.Get("backgroundCorrection_Inc100A")
bkgCorr_Int_60A.Sumw2()
bkgCorr_Inc_60A.Sumw2()
bkgCorr_Int_100A.Sumw2()
bkgCorr_Inc_100A.Sumw2()

################################################ Get Efficiency Correction 
correction_File   = TFile.Open("EffCorrectionCheck.root")
Efficiency_Int_60A  = correction_File.Get("Efficiency_Int_60A")
Efficiency_Inc_60A  = correction_File.Get("Efficiency_Inc_60A")
Efficiency_Int_100A = correction_File.Get("Efficiency_Int_100A")
Efficiency_Inc_100A = correction_File.Get("Efficiency_Inc_100A")
Efficiency_Int_60A .Sumw2()
Efficiency_Inc_60A .Sumw2()
Efficiency_Int_100A.Sumw2()
Efficiency_Inc_100A.Sumw2()

################################################ Get Raw Data
pionData_RecoData60A  = TFile.Open("/Volumes/Seagate/Elena/TPC/Data60A.root")
pionData_RecoData100A = TFile.Open("/Volumes/Seagate/Elena/TPC/Data100A.root")

intRecoData60A      = pionData_RecoData60A.Get ("RecoXS/hRecoInteractingKE")
incRecoData60A      = pionData_RecoData60A.Get ("RecoXS/hRecoIncidentKE")
intRecoData100A     = pionData_RecoData100A.Get("RecoXS/hRecoInteractingKE")
incRecoData100A     = pionData_RecoData100A.Get("RecoXS/hRecoIncidentKE")

intRecoData60A .Sumw2()
incRecoData60A .Sumw2()
intRecoData100A.Sumw2()
incRecoData100A.Sumw2()

intRecoData60A_Bkg  = intRecoData60A  .Clone ("intRecoData60A_Bkg") 
incRecoData60A_Bkg  = incRecoData60A  .Clone ("incRecoData60A_Bkg") 
intRecoData100A_Bkg = intRecoData100A .Clone("intRecoData100A_Bkg")
incRecoData100A_Bkg = incRecoData100A .Clone("incRecoData100A_Bkg") 

intRecoData60A_Bkg .Sumw2()
incRecoData60A_Bkg .Sumw2()
intRecoData100A_Bkg.Sumw2()
incRecoData100A_Bkg.Sumw2()

intRecoData60A_Bkg .Multiply(bkgCorr_Int_60A)
incRecoData60A_Bkg .Multiply(bkgCorr_Inc_60A)
intRecoData100A_Bkg.Multiply(bkgCorr_Int_100A)
incRecoData100A_Bkg.Multiply(bkgCorr_Inc_100A)
intRecoData60A_Bkg .Sumw2()
incRecoData60A_Bkg .Sumw2()
intRecoData100A_Bkg.Sumw2()
incRecoData100A_Bkg.Sumw2()

c2=TCanvas("c2" ,"Data" ,200 ,10 ,1500 ,500) #make nice
c2.Divide(3,1)
p0 = c2.cd(1)
p0.SetGrid ()
intRecoData60A.SetLineColor(kBlue)
intRecoData60A_Bkg.SetLineColor(kCyan)
intRecoData100A.SetLineColor(kRed-2)
intRecoData100A_Bkg.SetLineColor(kRed)
intRecoData60A.Draw("pesame")
intRecoData100A.Draw("pesame")
intRecoData60A_Bkg.Draw("pesame")
intRecoData100A_Bkg.Draw("pesame")

p1 = c2.cd(2)
p1.SetGrid ()
incRecoData60A.SetLineColor(kBlue)
incRecoData60A_Bkg.SetLineColor(kCyan)
incRecoData100A.SetLineColor(kRed-2)
incRecoData100A_Bkg.SetLineColor(kRed)
incRecoData60A.Draw("pesame")
incRecoData100A.Draw("pesame")
incRecoData60A_Bkg.Draw("pesame")
incRecoData100A_Bkg.Draw("pesame")

p2 = c2.cd(3)
p2.SetGrid ()
XSRecoData60A_Bkg  = intRecoData60A_Bkg  .Clone ("XSRecoData60A_Bkg") 
XSRecoData100A_Bkg = intRecoData100A_Bkg .Clone("XSRecoData100A_Bkg")
XSRecoData60A  = intRecoData60A  .Clone ("XSRecoData60A") 
XSRecoData100A = intRecoData100A .Clone("XSRecoData100A")
#XSRecoData60A_Bkg.Scale(101.)
#XSRecoData100A_Bkg.Scale(101.)
XSRecoData60A_Bkg.Divide(incRecoData60A_Bkg)
XSRecoData100A_Bkg.Divide(incRecoData100A_Bkg)

#XSRecoData60A.Scale(101.)
#XSRecoData100A.Scale(101.)
XSRecoData60A.Divide(incRecoData60A)
XSRecoData100A.Divide(incRecoData100A)

XSRecoData60A.Draw("pe")
XSRecoData100A.Draw("pesame")
XSRecoData60A_Bkg.Draw("pesame")
XSRecoData100A_Bkg.Draw("pesame")
c2.Update()



intRecoData60A_Bkg_Eff  = intRecoData60A_Bkg  .Clone ("intRecoData60A_Bkg_Eff") 
incRecoData60A_Bkg_Eff  = incRecoData60A_Bkg  .Clone ("incRecoData60A_Bkg_Eff") 
intRecoData100A_Bkg_Eff = intRecoData100A_Bkg .Clone("intRecoData100A_Bkg_Eff")
incRecoData100A_Bkg_Eff = incRecoData100A_Bkg .Clone("incRecoData100A_Bkg_Eff") 

intRecoData60A_Bkg_Eff .Sumw2()
incRecoData60A_Bkg_Eff .Sumw2()
intRecoData100A_Bkg_Eff.Sumw2()
incRecoData100A_Bkg_Eff.Sumw2()

intRecoData60A_Bkg_Eff .Divide(Efficiency_Int_60A)
incRecoData60A_Bkg_Eff .Divide(Efficiency_Inc_60A)
intRecoData100A_Bkg_Eff.Divide(Efficiency_Int_100A)
incRecoData100A_Bkg_Eff.Divide(Efficiency_Inc_100A)

intRecoData60A_Bkg_Eff .Sumw2()
incRecoData60A_Bkg_Eff .Sumw2()
intRecoData100A_Bkg_Eff.Sumw2()
incRecoData100A_Bkg_Eff.Sumw2()

Efficiency_Int_60A  .Sumw2()
Efficiency_Inc_60A  .Sumw2()
Efficiency_Int_100A .Sumw2()
Efficiency_Inc_100A .Sumw2()



c3=TCanvas("c3" ,"Data" ,200 ,10 ,1500 ,500) #make nice
c3.Divide(3,1)
p00 = c3.cd(1)
p00.SetGrid ()
intRecoData60A_Bkg_Eff.SetLineColor(kGreen)
intRecoData100A_Bkg_Eff.SetLineColor(kPink)
intRecoData60A_Bkg.Draw("pe")
intRecoData100A_Bkg.Draw("pesame")
intRecoData60A_Bkg_Eff.Draw("pesame")
intRecoData100A_Bkg_Eff.Draw("pesame")

p10 = c3.cd(2)
p10.SetGrid ()
incRecoData60A_Bkg_Eff.SetLineColor(kGreen)
incRecoData100A_Bkg_Eff.SetLineColor(kPink)
incRecoData60A_Bkg.Draw("pe")
incRecoData100A_Bkg.Draw("pesame")
incRecoData60A_Bkg_Eff.Draw("pesame")
incRecoData100A_Bkg_Eff.Draw("pesame")


p02 = c3.cd(3)
p02.SetGrid ()
'''
XSRecoData60A_Bkg  = intRecoData60A_Bkg  .Clone ("XSRecoData60A_Bkg") 
XSRecoData100A_Bkg = intRecoData100A_Bkg .Clone("XSRecoData100A_Bkg")
XSRecoData60A  = intRecoData60A  .Clone ("XSRecoData60A") 
XSRecoData100A = intRecoData100A .Clone("XSRecoData100A")
XSRecoData60A_Bkg.Scale(101.)
XSRecoData100A_Bkg.Scale(101.)
XSRecoData60A_Bkg.Divide(incRecoData60A_Bkg)
XSRecoData100A_Bkg.Divide(incRecoData100A_Bkg)

XSRecoData60A.Scale(101.)
XSRecoData100A.Scale(101.)
XSRecoData60A.Divide(incRecoData60A)
XSRecoData100A.Divide(incRecoData100A)

XSRecoData60A.Draw("pe")
XSRecoData100A.Draw("pesame")
XSRecoData60A_Bkg.Draw("pesame")
XSRecoData100A_Bkg.Draw("pesame")
'''
c3.Update()

'''
## Data Reco

c2=TCanvas("c2" ,"Data" ,200 ,10 ,500 ,500) #make nice
c2.SetGrid ()
XSTrue60AC = XSTrue60A.Clone("XSTrue60AC")
XSTrue60AC.SetTitle("Eff Corrected Data Reco on Truth; Kinetic Energy [MeV]; Cross Section")
XSTrue60AC.Draw("")
XSTrue100A.Draw("same")
XSTrue60A.GetXaxis().SetRangeUser(0,1200)
XSTrue60A.GetYaxis().SetRangeUser(0,2.0)
XSRecoData60A_Eff.Draw("same")
XSRecoData100A_Eff.Draw("same")
#Efficiency_Int_60A.Draw("")
c2.Update()

interactingPlotString = "RecoXS/hRecoInteractingKE"
incidentPlotString = "RecoXS/hRecoIncidentKE"
data_Int    = data_File.Get(interactingPlotString)
data_Inc    = data_File.Get(incidentPlotString)

data_FileName = "/Volumes/Seagate/Elena/TPC/Data60A.root"
data_FileName = "/Volumes/Seagate/Elena/TPC/Data60A.root"
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
'''

raw_input()  
