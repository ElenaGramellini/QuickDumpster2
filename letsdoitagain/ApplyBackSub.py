from ROOT import *
import os
import math
import argparse

from ROOT import TEfficiency
from ROOT import gStyle , TCanvas , TGraphErrors
from array import array

def calculateXSPlot(InteractingHisto, IncidentHisto, Name  ):
    XS =  InteractingHisto.Clone(Name)
    XS.Scale(101.10968)
    #XS.Sumw2()
    XS.Divide(IncidentHisto)
    return XS



gStyle.SetOptStat(0)


bkg60A_File   = TFile.Open("Out_2.0Muons_1.0Electrons_60A.root")
bkg100A_File  = TFile.Open("Out_1.0Muons_1.0Electrons_100A.root")
bkg_Int_60A   = bkg60A_File.Get("backgroundCorrection_Int60A")
bkg_Inc_60A   = bkg60A_File.Get("backgroundCorrection_Inc60A")
bkg_Int_100A  = bkg100A_File.Get("backgroundCorrection_Int100A")
bkg_Inc_100A  = bkg100A_File.Get("backgroundCorrection_Inc100A")

correction_File   = TFile.Open("EffCorrectionCheck.root")
XSTrue60A           = correction_File.Get("XSTrue60A")
XSTrue100A          = correction_File.Get("XSTrue100A")
XSRecoMC60A         = correction_File.Get("XSReco60A")
XSRecoMC100A        = correction_File.Get("XSReco100A")
Efficiency_Int_60A  = correction_File.Get("Efficiency_Int_60A")
Efficiency_Inc_60A  = correction_File.Get("Efficiency_Inc_60A")
Efficiency_Int_100A = correction_File.Get("Efficiency_Int_100A")
Efficiency_Inc_100A = correction_File.Get("Efficiency_Inc_100A")


################################################ MC
pionMC_RecoMC60A  = TFile.Open("/Volumes/Seagate/Elena/TPC/XSMCPionWithSecondaries60A_histo.root")
pionMC_RecoMC100A = TFile.Open("/Volumes/Seagate/Elena/TPC/MC100A_Pions.root")

intRecoMC60A      = pionMC_RecoMC60A.Get ("RecoXSPionOnly/hRecoInteractingKE")
incRecoMC60A      = pionMC_RecoMC60A.Get ("RecoXSPionOnly/hRecoIncidentKE")
intRecoMC100A     = pionMC_RecoMC100A.Get("RecoXSPionOnly/hRecoInteractingKE")
incRecoMC100A     = pionMC_RecoMC100A.Get("RecoXSPionOnly/hRecoIncidentKE")

intRecoMC60A_Eff  = intRecoMC60A  .Clone ("intRecoMC60A_Eff") 
incRecoMC60A_Eff  = incRecoMC60A  .Clone ("incRecoMC60A_Eff") 
intRecoMC100A_Eff = intRecoMC100A .Clone("intRecoMC100A_Eff")
incRecoMC100A_Eff = incRecoMC100A .Clone("incRecoMC100A_Eff") 


intRecoMC60A_Eff .Divide(Efficiency_Int_60A)
incRecoMC60A_Eff .Divide(Efficiency_Inc_60A)
intRecoMC100A_Eff.Divide(Efficiency_Int_100A)
incRecoMC100A_Eff.Divide(Efficiency_Inc_100A)

XSRecoMC60A_Eff  = calculateXSPlot(intRecoMC60A_Eff , incRecoMC60A_Eff , "XSRecoMC60A_Eff")
XSRecoMC100A_Eff = calculateXSPlot(intRecoMC100A_Eff, incRecoMC100A_Eff, "XSRecoMC100A_Eff")


## MC Reco

c1=TCanvas("c1" ,"ClosureReco" ,200 ,10 ,500 ,500) #make nice
c1.SetGrid ()
XSTrue60A.SetTitle("Closure Test: Eff Corrected MC Reco on Truth; Kinetic Energy [MeV]; Cross Section")
XSTrue60A.Draw("")
XSTrue100A.Draw("same")
XSTrue60A.GetXaxis().SetRangeUser(0,1200)
XSTrue60A.GetYaxis().SetRangeUser(0,2.0)
XSRecoMC60A_Eff.Draw("same")
XSRecoMC100A_Eff.Draw("same")
#Efficiency_Int_60A.Draw("")
c1.Update()



################################################ Data
pionData_RecoData60A  = TFile.Open("/Volumes/Seagate/Elena/TPC/Data60A.root")
pionData_RecoData100A = TFile.Open("/Volumes/Seagate/Elena/TPC/Data100A.root")

intRecoData60A      = pionData_RecoData60A.Get ("RecoXS/hRecoInteractingKE")
incRecoData60A      = pionData_RecoData60A.Get ("RecoXS/hRecoIncidentKE")
intRecoData100A     = pionData_RecoData100A.Get("RecoXS/hRecoInteractingKE")
incRecoData100A     = pionData_RecoData100A.Get("RecoXS/hRecoIncidentKE")

intRecoData100A.SetLineColor(kRed)
incRecoData100A.SetLineColor(kRed)

intRecoData60A_Bkg  = intRecoData60A  .Clone ("intRecoData60A_Bkg") 
incRecoData60A_Bkg  = incRecoData60A  .Clone ("incRecoData60A_Bkg") 
intRecoData100A_Bkg = intRecoData100A .Clone("intRecoData100A_Bkg")
incRecoData100A_Bkg = incRecoData100A .Clone("incRecoData100A_Bkg") 

intRecoData60A_Bkg .Multiply(bkg_Int_60A)
incRecoData60A_Bkg .Multiply(bkg_Inc_60A)
intRecoData100A_Bkg.Multiply(bkg_Int_100A)
incRecoData100A_Bkg.Multiply(bkg_Inc_100A)

XSRecoData60A_Bkg  = calculateXSPlot(intRecoData60A_Bkg , incRecoData60A_Bkg , "XSRecoData60A_Bkg")
XSRecoData100A_Bkg = calculateXSPlot(intRecoData100A_Bkg, incRecoData100A_Bkg, "XSRecoData100A_Bkg")

XSRecoData60A  = calculateXSPlot(intRecoData60A , incRecoData60A , "XSRecoData60A")
XSRecoData100A = calculateXSPlot(intRecoData100A, incRecoData100A, "XSRecoData100A")


XSRecoData60A.SetLineColor(kBlack)
XSRecoData100A.SetLineColor(kBlack)

## Data Back Sub

c2=TCanvas("c2" ,"Data" ,200 ,10 ,500 ,500) #make nice
c2.SetGrid ()
XSTrue60AC = XSTrue60A.Clone("XSTrue60AC")
XSRecoData60A_Bkg.SetTitle("Bkg Sub; Kinetic Energy [MeV]; Cross Section")
#XSTrue60AC.Draw("")
#XSTrue100A.Draw("same")
XSRecoData60A_Bkg.GetXaxis().SetRangeUser(0,1200)
XSRecoData60A_Bkg.GetYaxis().SetRangeUser(0,2.0)
XSRecoData60A_Bkg.Draw("")
XSRecoData100A_Bkg.Draw("same")
XSRecoData60A.Draw("same")
XSRecoData100A.Draw("same")
legend = TLegend(.44,.70,.84,.89)
legend.AddEntry(XSRecoData60A,"Raw Data 60A  Tot XS")
legend.AddEntry(XSRecoData100A,"Raw Data 100A Tot XS")
legend.AddEntry(XSRecoData60A_Bkg,"Bkg Sub Data 60A  Tot XS")
legend.AddEntry(XSRecoData100A_Bkg,"Bkg Sub Data 100A Tot XS")
legend.Draw("same")
c2.Update()


c3=TCanvas("c3" ,"Data" ,200 ,10 ,500 ,500) #make nice
c3.SetGrid ()
XSRecoData60A_Bkg.Draw("")
XSRecoData100A_Bkg.Draw("same")
XSRecoMC60A.Draw("same")
XSRecoMC100A.Draw("same")

XSRecoMC60A .SetLineColor(kOrange)
XSRecoMC100A.SetLineColor(kGreen-2)
legend2 = TLegend(.44,.70,.84,.89)
legend2.AddEntry(XSRecoMC60A ,"Reco MC 60A  Tot XS")
legend2.AddEntry(XSRecoMC100A,"RecoMC 100A Tot XS")
legend2.AddEntry(XSRecoData60A_Bkg,"Bkg Sub Data 60A  Tot XS")
legend2.AddEntry(XSRecoData100A_Bkg,"Bkg Sub Data 100A Tot XS")
legend2.Draw("same")
c3.Update()


'''
intRecoData60A_Eff_Bkg  = intRecoData60A_Bkg  .Clone ("intRecoData60A_Eff_Bkg ") 
incRecoData60A_Eff_Bkg  = incRecoData60A_Bkg  .Clone ("incRecoData60A_Eff_Bkg ") 
intRecoData100A_Eff_Bkg = intRecoData100A_Bkg .Clone("intRecoData100A_Eff_Bkg")
incRecoData100A_Eff_Bkg = incRecoData100A_Bkg .Clone("incRecoData100A_Eff_Bkg") 

Efficiency_Int_60A_2 = Efficiency_Int_60A  .Clone("Efficiency_Int_60A_2") 
Efficiency_Inc_60A_2 = Efficiency_Inc_60A  .Clone("Efficiency_Inc_60A_2") 
Efficiency_Int_100A_2= Efficiency_Int_100A .Clone("Efficiency_Int_100A_2")
Efficiency_Inc_100A_2= Efficiency_Inc_100A .Clone("Efficiency_Inc_100A_2")


intRecoData60A_Eff_Bkg .Divide(Efficiency_Int_60A_2)
incRecoData60A_Eff_Bkg .Divide(Efficiency_Inc_60A_2)
intRecoData100A_Eff_Bkg.Divide(Efficiency_Int_100A_2)
incRecoData100A_Eff_Bkg.Divide(Efficiency_Inc_100A_2)


XSRecoData60A_Eff_Bkg  = calculateXSPlot(intRecoData60A_Eff_Bkg , incRecoData60A_Eff_Bkg , "XSRecoData60A_Eff_Bkg")
XSRecoData100A_Eff_Bkg = calculateXSPlot(intRecoData100A_Eff_Bkg, incRecoData100A_Eff_Bkg, "XSRecoData100A_Eff_Bkg")

#XSRecoData60A_Eff_Bkg.Sumw2()
#XSRecoData100A_Eff_Bkg.Sumw2()

c4=TCanvas("c4" ,"Data" ,200 ,10 ,500 ,500) #make nice
c4.SetGrid ()
XSRecoData60A_Eff_Bkg.Draw("")
XSRecoData100A_Eff_Bkg.Draw("same")

legend = TLegend(.44,.70,.84,.89)
legend.AddEntry(XSRecoData60A_Eff_Bkg,"Bkg Sub, Eff Corr Data 60A  Tot XS")
legend.AddEntry(XSRecoData100A_Eff_Bkg,"Bkg Sub, Eff Corr Data 100A Tot XS")
legend.Draw("same")
c4.Update()
'''


outFile = TFile("BackgroundSubtractedData.root","recreate")
outFile.cd()

intRecoData60A_Bkg   .Write () 
incRecoData60A_Bkg   .Write () 
intRecoData100A_Bkg  .Write()
incRecoData100A_Bkg  .Write() 
XSRecoData60A.Write()
XSRecoData100A.Write()


outFile.Write()
outFile.Close()


raw_input()  
