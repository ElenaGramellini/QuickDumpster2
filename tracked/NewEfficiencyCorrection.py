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





#pionTrueMC_MCCutMin_FileName = "/Users/elenag/Desktop/TrackingStudy/Resolution/60ACuts/AngleCut_"
#pionTrueMC_MCCutMax_FileName = "/Users/elenag/Desktop/TrackingStudy/Resolution/60ACuts/AngleCut_0.15734_histo.root"

pionTrueMC_MCCut_FileName   = "/Users/elenag/Desktop/TrackingStudy/Resolution/60ACuts/AngleCut_0.07954_60Ahisto.root"
pionTrueMC_DataCut_FileName = "/Users/elenag/Desktop/TrackingStudy/Resolution/60ACuts/AngleCut_0.08334_60Ahisto.root"
pionTrueMC_All_FileName     = '/Volumes/Seagate/Elena/TPC/TruePionGen60A.root'
pionRecoMC_FileName         = '/Volumes/Seagate/Elena/TPC/MC60A_Pions.root'



pionTrueMC_MCCut_File   = TFile.Open(pionTrueMC_MCCut_FileName   )
pionTrueMC_DataCut_File = TFile.Open(pionTrueMC_DataCut_FileName )
pionTrueMC_All_File     = TFile.Open(pionTrueMC_All_FileName     )
pionRecoMC_File         = TFile.Open(pionRecoMC_FileName         )


# Get Interacting and Incident plots Reco

intTrue_MCC  = pionTrueMC_MCCut_File.Get("AngleCutTrueXS/hInteractingKE")
incTrue_MCC  = pionTrueMC_MCCut_File.Get("AngleCutTrueXS/hIncidentKE")
intTrue_Data = pionTrueMC_DataCut_File.Get("AngleCutTrueXS/hInteractingKE")
incTrue_Data = pionTrueMC_DataCut_File.Get("AngleCutTrueXS/hIncidentKE")
intTrue_All  = pionTrueMC_All_File.Get("TrueXS/hInteractingKE")
incTrue_All  = pionTrueMC_All_File.Get("TrueXS/hIncidentKE")
intReco      = pionRecoMC_File.Get("RecoXS/hRecoInteractingKE")
incReco      = pionRecoMC_File.Get("RecoXS/hRecoIncidentKE")



# Eff with MC Angle Cut
eff_MCC_Int = intReco.Clone("eff_MCC_Int")
eff_MCC_Int.Sumw2()
eff_MCC_Int.Divide(intTrue_MCC)

eff_MCC_Inc = incReco.Clone("eff_MCC_Inc")
eff_MCC_Inc.Sumw2()
eff_MCC_Inc.Divide(incTrue_MCC)

# Eff with Data Angle Cut
eff_Data_Int = intReco.Clone("eff_Data_Int")
eff_Data_Int.Sumw2()
eff_Data_Int.Divide(intTrue_Data)

eff_Data_Inc = incReco.Clone("eff_Data_Inc")
eff_Data_Inc.Sumw2()
eff_Data_Inc.Divide(incTrue_Data)

# Eff with All Interactions
eff_All_Int = intReco.Clone("eff_All_Int")
eff_All_Int.Sumw2()
eff_All_Int.Divide(intTrue_All)

eff_All_Inc = incReco.Clone("eff_All_Inc")
eff_All_Inc.Sumw2()
eff_All_Inc.Divide(incTrue_All)


# Cross Section Plots
XSTrue_MCC  = intTrue_MCC .Clone("XS_MCC")
XSTrue_Data = intTrue_Data.Clone("XS_Data")
XSTrue_All  = intTrue_All .Clone("XS_All")
XSReco      = intReco     .Clone("XSReco")

XSTrue_MCC .Scale(101.)
XSTrue_Data.Scale(101.)
XSTrue_All .Scale(101.)
XSReco     .Scale(101.)

XSTrue_MCC .Sumw2()
XSTrue_Data.Sumw2()
XSTrue_All .Sumw2()
XSReco     .Sumw2()

XSTrue_MCC .Divide(incTrue_MCC  )
XSTrue_Data.Divide(incTrue_Data )
XSTrue_All .Divide(incTrue_All  )
XSReco     .Divide(incReco      )


outFile = TFile("NewEfficiencyCorrectionPions60A.root","recreate")
outFile.cd()

eff_MCC_Int.Write()
eff_Data_Int.Write()
eff_All_Int.Write()

eff_MCC_Inc.Write()
eff_Data_Inc.Write()
eff_All_Inc.Write()
 
XSTrue_MCC .Write()
XSTrue_Data.Write()
XSTrue_All .Write()
XSReco     .Write()

outFile.Write()
outFile.Close()

raw_input()  



