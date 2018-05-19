from ROOT import *
import os
import math
import argparse


'''
/Volumes/Seagate/Elena/TPC/AngleCut_100A_histo.root
/Volumes/Seagate/Elena/TPC/TruePionGen60A.root


/Volumes/Seagate/Elena/TPC/Data100A.root
/Volumes/Seagate/Elena/TPC/Data60A.root

/Volumes/Seagate/Elena/TPC/MC100A_Electron.root
/Volumes/Seagate/Elena/TPC/MC100A_Muon.root
/Volumes/Seagate/Elena/TPC/MC100A_Pions.root

/Volumes/Seagate/Elena/TPC/MC60A_Electron.root
/Volumes/Seagate/Elena/TPC/MC60A_Muon.root
/Volumes/Seagate/Elena/TPC/MC60A_Pions.root


/Volumes/Seagate/Elena/TPC/XSMCPionWithSecondaries60A_histo.root
'''



# Generated XS 60A 100A  
pionMC_Gen60A  = TFile.Open("/Volumes/Seagate/Elena/TPC/TruePionGen60A.root")
pionMC_Gen100A = TFile.Open("/Volumes/Seagate/Elena/TPC/AngleCut_100A_histo.root")
intTrue60A     = pionMC_Gen60A.Get("TrueXS/hInteractingKE")
incTrue60A     = pionMC_Gen60A.Get("TrueXS/hIncidentKE")
intTrue100A    = pionMC_Gen100A.Get("TrueXS/hInteractingKE")
incTrue100A    = pionMC_Gen100A.Get("TrueXS/hIncidentKE")

# Reco XS 60A 100A  
pionMC_Reco60A  = TFile.Open("/Volumes/Seagate/Elena/TPC/XSMCPionWithSecondaries60A_histo.root")
pionMC_Reco100A = TFile.Open("/Volumes/Seagate/Elena/TPC/MC100A_Pions.root")

intTrue60A_WC2TPC     = pionMC_Reco60A.Get("TrueXS/hInteractingKE")
incTrue60A_WC2TPC     = pionMC_Reco60A.Get("TrueXS/hIncidentKE")
intTrue100A_WC2TPC    = pionMC_Reco100A.Get("TrueXS/hInteractingKE")
incTrue100A_WC2TPC    = pionMC_Reco100A.Get("TrueXS/hIncidentKE")


intReco60A      = pionMC_Reco60A.Get ("RecoXSPionOnly/hRecoInteractingKE")
incReco60A      = pionMC_Reco60A.Get ("RecoXSPionOnly/hRecoIncidentKE")
intReco100A     = pionMC_Reco100A.Get("RecoXSPionOnly/hRecoInteractingKE")
incReco100A     = pionMC_Reco100A.Get("RecoXSPionOnly/hRecoIncidentKE")


# Assign colors
intTrue60A .SetLineColor(kGreen-2)  
incTrue60A .SetLineColor(kGreen-2)  
intTrue100A.SetLineColor(kGreen-2)  
incTrue100A.SetLineColor(kGreen-2)  
intReco60A .SetLineColor(kRed)  
incReco60A .SetLineColor(kRed)  
intReco100A.SetLineColor(kRed)  
incReco100A.SetLineColor(kRed)  

intTrue60A .SetLineWidth(2) 
incTrue60A .SetLineWidth(2) 
intTrue100A.SetLineWidth(2)
incTrue100A.SetLineWidth(2)
intReco60A .SetLineWidth(2) 
incReco60A .SetLineWidth(2) 
intReco100A.SetLineWidth(2)
incReco100A.SetLineWidth(2)


XSTrue60A  = intTrue60A .Clone("XSTrue60A") 
XSTrue100A = intTrue100A.Clone("XSTrue100A")


XSTrue60A_WC2TPC  = intTrue60A_WC2TPC .Clone("XSTrue60A_WC2TPC") 
XSTrue100A_WC2TPC = intTrue100A_WC2TPC.Clone("XSTrue100A_WC2TPC")
XSReco60A  = intReco60A .Clone("XSReco60A") 
XSReco100A = intReco100A.Clone("XSReco100A")

XSTrue60A  .Scale(101.)
XSTrue100A .Scale(101.)
XSTrue60A_WC2TPC  .Scale(101.)
XSTrue100A_WC2TPC .Scale(101.)
XSReco60A  .Scale(101.)
XSReco100A .Scale(101.)

XSTrue60A  .Divide(incTrue60A )
XSTrue100A .Divide(incTrue100A)
XSTrue60A_WC2TPC  .Divide(incTrue60A_WC2TPC )
XSTrue100A_WC2TPC .Divide(incTrue100A_WC2TPC)
XSReco60A  .Divide(incReco60A )
XSReco100A .Divide(incReco100A)


RatioTruths_Int_60A  = intTrue60A_WC2TPC .Clone("RatioTruths_Int_60A")  
RatioTruths_Inc_60A  = incTrue60A_WC2TPC .Clone("RatioTruths_Inc_60A") 
RatioTruths_Int_100A = intTrue100A_WC2TPC.Clone("RatioTruths_Int_100A") 
RatioTruths_Inc_100A = incTrue100A_WC2TPC.Clone("RatioTruths_Inc_100A")
RatioTruths_Int_60A   .Divide(intTrue60A )
RatioTruths_Inc_60A   .Divide(incTrue60A )
RatioTruths_Int_100A  .Divide(intTrue100A)
RatioTruths_Inc_100A  .Divide(incTrue100A)


RatioTruthRecos_Int_60A  = intReco60A .Clone("RatioTruthRecos_Int_60A")  
RatioTruthRecos_Inc_60A  = incReco60A .Clone("RatioTruthRecos_Inc_60A") 
RatioTruthRecos_Int_100A = intReco100A.Clone("RatioTruthRecos_Int_100A") 
RatioTruthRecos_Inc_100A = incReco100A.Clone("RatioTruthRecos_Inc_100A")
RatioTruthRecos_Int_60A   .Divide(intTrue60A_WC2TPC )
RatioTruthRecos_Inc_60A   .Divide(incTrue60A_WC2TPC )
RatioTruthRecos_Int_100A  .Divide(intTrue100A_WC2TPC)
RatioTruthRecos_Inc_100A  .Divide(incTrue100A_WC2TPC)


Efficiency_Int_60A  = intReco60A .Clone("Efficiency_Int_60A")  
Efficiency_Inc_60A  = incReco60A .Clone("Efficiency_Inc_60A") 
Efficiency_Int_100A = intReco100A.Clone("Efficiency_Int_100A") 
Efficiency_Inc_100A = incReco100A.Clone("Efficiency_Inc_100A")
Efficiency_Int_60A   .Divide(intTrue60A)
Efficiency_Inc_60A   .Divide(incTrue60A)
Efficiency_Int_100A  .Divide(intTrue100A)
Efficiency_Inc_100A  .Divide(incTrue100A)




outFile = TFile("EffCorrectionCheck.root","recreate")
outFile.cd()


XSTrue60A .Write()
XSTrue100A.Write()
XSTrue60A_WC2TPC .Write()
XSTrue100A_WC2TPC.Write()
XSReco60A .Write()
XSReco100A.Write()

RatioTruths_Int_60A   .Write()
RatioTruths_Inc_60A   .Write()
RatioTruths_Int_100A  .Write()
RatioTruths_Inc_100A  .Write()

RatioTruthRecos_Int_60A   .Write()
RatioTruthRecos_Inc_60A   .Write()
RatioTruthRecos_Int_100A  .Write()
RatioTruthRecos_Inc_100A  .Write()

Efficiency_Int_60A   .Write()
Efficiency_Inc_60A   .Write()
Efficiency_Int_100A  .Write()
Efficiency_Inc_100A  .Write()

outFile.Write()
outFile.Close()


raw_input()  



