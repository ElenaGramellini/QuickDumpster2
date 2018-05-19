from ROOT import *
import os
import math
import argparse

def CalculateErrorRatio (num, numErr, den, denErr):
    if num and den:
        relativeErrorNum   = numErr/num
        relativeErrorDen   = denErr/den
        relativeErrorRatio = TMath.Sqrt(relativeErrorNum*relativeErrorNum + relativeErrorDen*relativeErrorDen)
        ratio = num/den
        totErrorRatio = relativeErrorRatio*ratio
    else :
        totErrorRatio = 10000.
    return totErrorRatio

pionMCNoFilter_FileName = '/Volumes/Seagate/Elena/TPC/TruePionGen.root'
pionMC_FileName = '/Volumes/Seagate/Elena/TPC/XSMCPionWithSecondaries_histo.root'


# Get Interacting and Incident plots Reco
pionMC_File  = TFile.Open(pionMC_FileName)
intTrue  = pionMC_File.Get("TrueXS/hInteractingKE")
incTrue  = pionMC_File.Get("TrueXS/hIncidentKE")
intReco  = pionMC_File.Get("RecoXSPionOnly/hRecoInteractingKE")
incReco  = pionMC_File.Get("RecoXSPionOnly/hRecoIncidentKE")


# Get Interacting and Incident plots for all true primary in TPC
pionMCNoFilter   = TFile.Open(pionMCNoFilter_FileName)
intTrueNoFilter  = pionMCNoFilter.Get("TrueXS/hInteractingKE")
incTrueNoFilter  = pionMCNoFilter.Get("TrueXS/hIncidentKE")

# Assign colors
intReco.SetLineColor(kRed)  
incReco.SetLineColor(kRed)  
intTrue.SetLineColor(kBlue)  
incTrue.SetLineColor(kBlue)
intTrueNoFilter.SetLineColor(kGreen-2)  
incTrueNoFilter.SetLineColor(kGreen-2)    

intReco.SetLineWidth(2)  
incReco.SetLineWidth(2)  
intTrue.SetLineWidth(2)  
incTrue.SetLineWidth(2)
intTrueNoFilter.SetLineWidth(2)  
incTrueNoFilter.SetLineWidth(2)    

legend = TLegend(.54,.52,.84,.70);
legend.AddEntry(intReco        ,"Reconstructed");
legend.AddEntry(intTrue        ,"True With Filters");
legend.AddEntry(intTrueNoFilter,"True No Filters");


# Comparison between plots
c60T1 = TCanvas("c60T1" ,"Interaction" ,200 ,10 ,700 ,700)
c60T1.cd()
c60T1.SetGrid()
intTrueNoFilter.SetTitle("Interacting Histogram; Interacting KE [MeV]; N Entries")
intTrueNoFilter.GetXaxis().SetRangeUser(0,1000)
intTrueNoFilter.Draw("histo")
intTrue.Draw("histosames")
intReco.Draw("histosames")
legend.Draw("same")
c60T1.Update()

c60T2 = TCanvas("c60T2" ,"Incident" ,200 ,10 ,700 ,700)
c60T2.cd()
c60T2.SetGrid()
incTrueNoFilter.SetTitle("Incident Histogram; Incitent KE [MeV]; N Entries")
incTrueNoFilter.GetXaxis().SetRangeUser(0,1000)
incTrueNoFilter.Draw("histo")
incTrue.Draw("histosames")
incReco.Draw("histosames")
legend.Draw("same")
c60T2.Update()

c60T3 = TCanvas("c60T3" ,"Cross Section" ,200 ,10 ,700 ,700)
c60T3.cd()
c60T3.SetGrid()
XSTrueNoFilter= intTrueNoFilter.Clone("XSTrueNoFilter")
XSTrue = intTrue.Clone("XSTrue")
XSReco = intReco.Clone("XSReco")
XSTrueNoFilter.Sumw2()
XSTrue.Sumw2()
XSReco.Sumw2()
XSTrueNoFilter.Scale(101.10968)
XSTrue.Scale(101.10968)
XSReco.Scale(101.10968)
XSTrueNoFilter.Divide(incTrueNoFilter)
XSTrue.Divide(incTrue)
XSReco.Divide(incReco)

XSTrueNoFilter.SetTitle("Cross Section; KE [MeV]; Cross Section [barn]")
XSTrueNoFilter.GetXaxis().SetRangeUser(0,1000)
XSTrueNoFilter.Draw("pe")
XSTrue.Draw("pesames")
XSReco.Draw("pesames")
legend.Draw("same")

c60T3.Update()


effCorr_Int_NotFilt = intReco.Clone("effCorr_Int_NoFilt")
effCorr_Inc_NotFilt = incReco.Clone("effCorr_Inc_NoFilt")
effCorr_Int         = intReco.Clone("effCorr_Int")
effCorr_Inc         = incReco.Clone("effCorr_Inc")
effCorr_Int_NotFilt .Sumw2() 
effCorr_Inc_NotFilt .Sumw2() 
effCorr_Int         .Sumw2() 
effCorr_Inc         .Sumw2()

effCorr_Int_NotFilt .Divide(intTrueNoFilter) 
effCorr_Inc_NotFilt .Divide(incTrueNoFilter) 
effCorr_Int         .Divide(intTrue) 
effCorr_Inc         .Divide(incTrue) 

cEffReal = TCanvas("cEffReal" ,"EffReal Correction" ,200 ,10 ,1400 ,700)
cEffReal.Divide(2,1)
pEff1 = cEffReal.cd(1)
pEff1.SetGrid()
effCorr_Int_NotFilt.SetTitle("Efficiency Correction, Interacting; KE [MeV]; Efficiency Correction")
effCorr_Int_NotFilt.Draw("")
effCorr_Inc_NotFilt.SetLineColor(kRed)

pEff2 = cEffReal.cd(2)
pEff2.SetGrid()
effCorr_Int_NotFilt.SetTitle("Efficiency Correction, Incident; KE [MeV]; Efficiency Correction")
effCorr_Inc_NotFilt.Draw("")
cEffReal.Update()


        
multEffCorr_Int_NotFilt = intTrueNoFilter.Clone("multEffCorr_Int_NoFilt")
multEffCorr_Inc_NotFilt = incTrueNoFilter.Clone("multEffCorr_Inc_NoFilt")
multEffCorr_Int         = intTrue.Clone("multEffCorr_Int")
multEffCorr_Inc         = incTrue.Clone("multEffCorr_Inc")

multEffCorr_Int_NotFilt .Sumw2() 
multEffCorr_Inc_NotFilt .Sumw2() 
multEffCorr_Int         .Sumw2() 
multEffCorr_Inc         .Sumw2()

multEffCorr_Int_NotFilt .Divide(intReco) 
multEffCorr_Inc_NotFilt .Divide(incReco) 
multEffCorr_Int         .Divide(intReco) 
multEffCorr_Inc         .Divide(incReco) 



cTest = TCanvas("cTest" ,"Cross Section" ,200 ,10 ,700 ,700)
cTest.cd()
cTest.SetGrid()
corrReco_Int         = intReco.Clone("corrReco_Int")
corrReco_Inc         = incReco.Clone("corrReco_Inc")
corrReco_Int.Sumw2()
corrReco_Inc.Sumw2()
corrReco_Int.Multiply(multEffCorr_Int_NotFilt)
corrReco_Inc.Multiply(multEffCorr_Inc_NotFilt)
XSRecoCorrected = corrReco_Int.Clone("XSCorrected")
XSRecoCorrected.Divide(corrReco_Inc)
XSRecoCorrected.Scale(101.10968)

XSTrueNoFilter.Draw("pe")
XSRecoCorrected.Draw("pesame")
cTest.Update()


cEff = TCanvas("cEff" ,"Eff Correction" ,200 ,10 ,700 ,700)
cEff.cd()
cEff.SetGrid()
multEffCorr_Int_NotFilt.Draw("")
multEffCorr_Inc_NotFilt.SetLineColor(kRed)
multEffCorr_Inc_NotFilt.Draw("same")
multEffCorr_Int_NotFilt.SetTitle("Efficiency Corrections in Incident and Interacting; KE [MeV]; Efficiency Correction")
legend1 = TLegend(.54,.52,.84,.70);
legend1.AddEntry(multEffCorr_Int_NotFilt        ,"Eff Correction for Interacting");
legend1.AddEntry(multEffCorr_Inc_NotFilt        ,"Eff Correction for Incident");
legend1.Draw("same")
cEff.Update()

cEff1 = TCanvas("cEff1" ,"RatioOfRatios" ,200 ,10 ,700 ,700)
cEff1.cd()
cEff1.SetGrid()
RoR = multEffCorr_Int_NotFilt.Clone("RoR")
RoR.Sumw2()
RoR.SetTitle("Ratio of Efficiency Ratios; KE [MeV]; Ratio of Ratios")
RoR.Divide(multEffCorr_Inc_NotFilt)
RoR.Draw("")
cEff1.Update()

outFile = TFile("EfficiencyCorrectionPions60A.root","recreate")
outFile.cd()

intTrueNoFilter.Write("interactingTrueMC_NoFilt",TObject.kWriteDelete)
incTrueNoFilter.Write("incidentTrueMC_NoFilt",TObject.kWriteDelete)
intTrue.Write("interactingTrueMC",TObject.kWriteDelete)
incTrue.Write("incidentTrueMC",TObject.kWriteDelete)
intReco.Write("interactingRecoMC",TObject.kWriteDelete)
incReco.Write("incidentRecoMC",TObject.kWriteDelete)

XSTrueNoFilter .Write() 
multEffCorr_Int_NotFilt .Write() 
multEffCorr_Inc_NotFilt .Write() 
multEffCorr_Int         .Write() 
multEffCorr_Inc         .Write()

effCorr_Int_NotFilt .Write() 
effCorr_Inc_NotFilt .Write() 
effCorr_Int         .Write() 
effCorr_Inc         .Write()

outFile.Write()
outFile.Close()

raw_input()  



