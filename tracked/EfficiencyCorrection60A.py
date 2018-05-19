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

pionMCTrue_FileName = '/Volumes/Seagate/Elena/TPC/TruePionGen60A.root'
pionMC_FileName     = '/Volumes/Seagate/Elena/TPC/XSMCPionWithSecondaries60A_histo.root'


# Get Interacting and Incident plots Reco
pionMC_File  = TFile.Open(pionMC_FileName)
intReco  = pionMC_File.Get("RecoXSPionOnly/hRecoInteractingKE")
incReco  = pionMC_File.Get("RecoXSPionOnly/hRecoIncidentKE")

# Get Interacting and Incident plots for all true primary in TPC
pionMCTrue   = TFile.Open(pionMCTrue_FileName)
intTrue  = pionMCTrue.Get("TrueXS/hInteractingKE")
incTrue  = pionMCTrue.Get("TrueXS/hIncidentKE")

# Assign colors
intReco.SetLineColor(kRed)  
incReco.SetLineColor(kRed)  
intTrue.SetLineColor(kGreen-2)  
incTrue.SetLineColor(kGreen-2)    

intReco.SetLineWidth(2)  
incReco.SetLineWidth(2)  
intTrue.SetLineWidth(2)  
incTrue.SetLineWidth(2)


legend = TLegend(.54,.52,.84,.70);
legend.AddEntry(intReco        ,"Reconstructed");
legend.AddEntry(intTrue        ,"True With Filters");



# Comparison between plots
c60T1 = TCanvas("c60T1" ,"Interaction" ,200 ,10 ,700 ,700)
c60T1.cd()
c60T1.SetGrid()
intTrue.SetTitle("Interacting Histogram; Interacting KE [MeV]; N Entries")
intTrue.GetXaxis().SetRangeUser(0,1000)
intTrue.Draw("histo")
intReco.Draw("histosames")
legend.Draw("same")
c60T1.Update()

c60T2 = TCanvas("c60T2" ,"Incident" ,200 ,10 ,700 ,700)
c60T2.cd()
c60T2.SetGrid()
incTrue.SetTitle("Incident Histogram; Incitent KE [MeV]; N Entries")
incTrue.GetXaxis().SetRangeUser(0,1000)
incTrue.Draw("histo")
incReco.Draw("histosames")
legend.Draw("same")
c60T2.Update()

c60T3 = TCanvas("c60T3" ,"Cross Section" ,200 ,10 ,700 ,700)
c60T3.cd()
c60T3.SetGrid()
XSTrue = intTrue.Clone("XSTrue")
XSReco = intReco.Clone("XSReco")
XSTrue.Sumw2()
XSReco.Sumw2()
XSTrue.Scale(101.10968)
XSReco.Scale(101.10968)
XSTrue.Divide(incTrue)
XSReco.Divide(incReco)

XSTrue.SetTitle("Cross Section; KE [MeV]; Cross Section [barn]")
XSTrue.GetXaxis().SetRangeUser(0,1000)
XSTrue.Draw("pe")
XSReco.Draw("pesames")
legend.Draw("same")

c60T3.Update()


effCorr_Int         = intReco.Clone("effCorr_Int")
effCorr_Inc         = incReco.Clone("effCorr_Inc")
effCorr_Int         .Sumw2() 
effCorr_Inc         .Sumw2()

effCorr_Int         .Divide(intTrue) 
effCorr_Inc         .Divide(incTrue) 

cEffReal = TCanvas("cEffReal" ,"EffReal Correction" ,200 ,10 ,1400 ,700)
cEffReal.Divide(2,1)
pEff1 = cEffReal.cd(1)
pEff1.SetGrid()
effCorr_Int.SetTitle("Efficiency Correction, Interacting; KE [MeV]; Efficiency Correction")
effCorr_Int.Draw("")
effCorr_Inc.SetLineColor(kRed)

pEff2 = cEffReal.cd(2)
pEff2.SetGrid()
effCorr_Int.SetTitle("Efficiency Correction, Incident; KE [MeV]; Efficiency Correction")
effCorr_Inc.Draw("")
cEffReal.Update()



multEffCorr_Int         = intTrue.Clone("multEffCorr_Int")
multEffCorr_Inc         = incTrue.Clone("multEffCorr_Inc")
multEffCorr_Int         .Sumw2() 
multEffCorr_Inc         .Sumw2()
multEffCorr_Int         .Divide(intReco) 
multEffCorr_Inc         .Divide(incReco) 



cTest = TCanvas("cTest" ,"Cross Section" ,200 ,10 ,700 ,700)
cTest.cd()
cTest.SetGrid()
corrReco_Int         = intReco.Clone("corrReco_Int")
corrReco_Inc         = incReco.Clone("corrReco_Inc")
corrReco_Int.Sumw2()
corrReco_Inc.Sumw2()
corrReco_Int.Multiply(multEffCorr_Int)
corrReco_Inc.Multiply(multEffCorr_Inc)
XSRecoCorrected = corrReco_Int.Clone("XSCorrected")
XSRecoCorrected.Divide(corrReco_Inc)
XSRecoCorrected.Scale(101.10968)

XSTrue.Draw("pe")
XSRecoCorrected.Draw("pesame")
cTest.Update()


cEff = TCanvas("cEff" ,"Eff Correction" ,200 ,10 ,700 ,700)
cEff.cd()
cEff.SetGrid()
multEffCorr_Int.Draw("")
multEffCorr_Inc.SetLineColor(kRed)
multEffCorr_Inc.Draw("same")
multEffCorr_Int.SetTitle("Efficiency Corrections in Incident and Interacting; KE [MeV]; Efficiency Correction")
legend1 = TLegend(.54,.52,.84,.70);
legend1.AddEntry(multEffCorr_Int        ,"Eff Correction for Interacting");
legend1.AddEntry(multEffCorr_Inc        ,"Eff Correction for Incident");
legend1.Draw("same")
cEff.Update()

cEff1 = TCanvas("cEff1" ,"RatioOfRatios" ,200 ,10 ,700 ,700)
cEff1.cd()
cEff1.SetGrid()
RoR = multEffCorr_Int.Clone("RoR")
RoR.Sumw2()
RoR.SetTitle("Ratio of Efficiency Ratios; KE [MeV]; Ratio of Ratios")
RoR.Divide(multEffCorr_Inc)
RoR.Draw("")
cEff1.Update()

outFile = TFile("EfficiencyCorrectionPions60A.root","recreate")
outFile.cd()

intTrue.Write("interactingTrueMC_60A",TObject.kWriteDelete)
incTrue.Write("incidentTrueMC_60A",TObject.kWriteDelete)
intReco.Write("interactingRecoMC_60A",TObject.kWriteDelete)
incReco.Write("incidentRecoMC_60A",TObject.kWriteDelete)

XSTrue              .Write("XSTrue_60A"         ,TObject.kWriteDelete)
multEffCorr_Int     .Write("multEffCorr_Int_60A",TObject.kWriteDelete)
multEffCorr_Inc     .Write("multEffCorr_Inc_60A",TObject.kWriteDelete)
effCorr_Int         .Write("effCorr_Int_60A"    ,TObject.kWriteDelete)
effCorr_Inc         .Write("effCorr_Inc_60A"    ,TObject.kWriteDelete)

outFile.Write()
outFile.Close()

raw_input()  



