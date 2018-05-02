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

pionMCNoFilter_FileName = '/Volumes/Seagate/Elena/MCContamination/TrueAnaPions60A_NoFilter.root'
pionMC_FileName = '/Volumes/Seagate/Elena/MCContamination/MC_XS60AHisto.root'


# Get Interacting and Incident plots Reco
pionMC_File  = TFile.Open(pionMC_FileName)
intTrue  = pionMC_File.Get("TrueXS/hInteractingKE")
incTrue  = pionMC_File.Get("TrueXS/hIncidentKE")
intReco  = pionMC_File.Get("RecoXS/hRecoInteractingKE")
incReco  = pionMC_File.Get("RecoXS/hRecoIncidentKE")


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


        
effCorr_Int_NotFilt = intTrueNoFilter.Clone("effCorr_Int_NoFilt")
effCorr_Inc_NotFilt = incTrueNoFilter.Clone("effCorr_Inc_NoFilt")
effCorr_Int         = intTrue.Clone("effCorr_Int")
effCorr_Inc         = incTrue.Clone("effCorr_Inc")

effCorr_Int_NotFilt .Sumw2() 
effCorr_Inc_NotFilt .Sumw2() 
effCorr_Int         .Sumw2() 
effCorr_Inc         .Sumw2()

effCorr_Int_NotFilt .Divide(intReco) 
effCorr_Inc_NotFilt .Divide(incReco) 
effCorr_Int         .Divide(intReco) 
effCorr_Inc         .Divide(incReco) 


'''
for i in xrange(intTrueNoFilter.GetSize()):
    trueBin_Int    = intTrueNoFilter.GetBinContent(i)
    trueBin_IntErr = intTrueNoFilter.GetBinError(i)
    trueBin_Inc    = incTrueNoFilter.GetBinContent(i)
    trueBin_IncErr = incTrueNoFilter.GetBinError(i)

    recoBin_Int    = intReco.GetBinContent(i)
    recoBin_IntErr = intReco.GetBinError(i)
    recoBin_Inc    = incReco.GetBinContent(i)
    recoBin_IncErr = incReco.GetBinError(i)

    if recoBin_Int: 
        print i,trueBin_Int/recoBin_Int, effCorr_Int_NotFilt.GetBinContent(i), CalculateErrorRatio(trueBin_Int, trueBin_IntErr,  recoBin_Int, recoBin_IntErr), effCorr_Int_NotFilt.GetBinError(i)



    if recoBin_Int*trueBin_Int :
        relErrorInt_reco = recoBin_IntErr/float(recoBin_Int)
        relErrorInt_true = trueBin_IntErr/float(trueBin_Int)
        totErrorInt = TMath.Sqrt(relErrorInt_reco*relErrorInt_reco + relErrorInt_true*relErrorInt_true)
        Int_Correction = trueBin_Int/recoBin_Int
        totErrorInt = totErrorInt*Int_Correction
        ##
        relErrorInc_reco = recoBin_IncErr/float(recoBin_Inc)
        relErrorInc_true = trueBin_IncErr/float(trueBin_Inc)
        totErrorInc = TMath.Sqrt(relErrorInc_reco*relErrorInc_reco + relErrorInc_true*relErrorInc_true)
        Inc_Correction = trueBin_Inc/recoBin_Inc
        totErrorInc = totErrorInc*Inc_Correction
        #print i, "interacting: ", Int_Correction ," +/-" ,totErrorInt , "incident: ", Inc_Correction," +/-" ,totErrorInc
'''


cTest = TCanvas("cTest" ,"Cross Section" ,200 ,10 ,700 ,700)
cTest.cd()
cTest.SetGrid()
corrReco_Int         = intReco.Clone("corrReco_Int")
corrReco_Inc         = incReco.Clone("corrReco_Inc")
corrReco_Int.Sumw2()
corrReco_Inc.Sumw2()
corrReco_Int.Multiply(effCorr_Int_NotFilt)
corrReco_Inc.Multiply(effCorr_Inc_NotFilt)
XSRecoCorrected = corrReco_Int.Clone("XSCorrected")
XSRecoCorrected.Divide(corrReco_Inc)
XSRecoCorrected.Scale(101.10968)

XSTrueNoFilter.Draw("pe")
XSRecoCorrected.Draw("pesame")
cTest.Update()


 
outFile = TFile("EfficiencyCorrectionPions60A.root","recreate")
outFile.cd()

intTrueNoFilter.Write("interactingTrueMC_NoFilt",TObject.kWriteDelete)
incTrueNoFilter.Write("incidentTrueMC_NoFilt",TObject.kWriteDelete)
intTrue.Write("interactingTrueMC",TObject.kWriteDelete)
incTrue.Write("incidentTrueMC",TObject.kWriteDelete)
intReco.Write("interactingRecoMC",TObject.kWriteDelete)
incReco.Write("incidentRecoMC",TObject.kWriteDelete)
effCorr_Int_NotFilt .Write() 
effCorr_Inc_NotFilt .Write() 
effCorr_Int         .Write() 
effCorr_Inc         .Write()

outFile.Write()
outFile.Close()

raw_input()  



